"""SQLite research ledger for revisioned observations and immutable decisions."""
from contextlib import contextmanager
from datetime import datetime
import hashlib
import json
import sqlite3

SCHEMA = """
CREATE TABLE IF NOT EXISTS deliveries (
    id TEXT PRIMARY KEY, raw BLOB NOT NULL, digest TEXT NOT NULL,
    status TEXT NOT NULL, version_id INTEGER REFERENCES versions(id)
);
CREATE TABLE IF NOT EXISTS versions (
    id INTEGER PRIMARY KEY, source TEXT NOT NULL, entity TEXT NOT NULL,
    revision INTEGER NOT NULL, occurred TEXT NOT NULL, published TEXT,
    received TEXT NOT NULL, admitted TEXT NOT NULL, authority TEXT NOT NULL,
    value TEXT NOT NULL, admission_rule TEXT NOT NULL,
    origin_delivery TEXT NOT NULL REFERENCES deliveries(id),
    UNIQUE (source, entity, revision)
);
CREATE INDEX IF NOT EXISTS versions_cut ON versions(source, entity, admitted, revision);
CREATE TABLE IF NOT EXISTS decisions (
    id TEXT PRIMARY KEY, cut TEXT NOT NULL, frontier INTEGER NOT NULL,
    rule TEXT NOT NULL, keys_json TEXT NOT NULL, result TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS inputs (
    decision TEXT NOT NULL REFERENCES decisions(id),
    version INTEGER NOT NULL REFERENCES versions(id),
    PRIMARY KEY(decision, version)
);
"""


def encode(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'), allow_nan=False)


def utc(value):
    dt = datetime.strptime(value, '%Y-%m-%dT%H:%M:%SZ')
    if dt.isoformat(timespec='seconds') + 'Z' != value:
        raise ValueError('Noncanonical UTC timestamp')
    return value


class Ledger:
    def __init__(self, path):
        self.db = sqlite3.connect(path, isolation_level=None)
        self.db.row_factory = sqlite3.Row
        self.db.execute('PRAGMA foreign_keys=ON')
        self.db.execute('PRAGMA synchronous=FULL')
        self.db.executescript(SCHEMA)

    def close(self):
        self.db.close()

    @contextmanager
    def writing(self):
        self.db.execute('BEGIN IMMEDIATE')
        try:
            yield
            self.db.commit()
        except BaseException:
            self.db.rollback()
            raise

    def receive(self, raw, before_commit=None):
        event = json.loads(raw)
        key = event['source'], event['entity'], event['revision']
        for field in ('source', 'entity', 'delivery', 'authority'):
            if not isinstance(event[field], str) or not event[field].strip():
                raise ValueError(f'Expected a nonempty {field}')
        if type(key[2]) is not int or key[2] < 1:
            raise ValueError('Expected a positive revision')
        occurred, received, admitted = (utc(event[name]) for name in ('occurred', 'received', 'admitted'))
        published = event.get('published')
        if not occurred <= received <= admitted or (published is not None and not occurred <= utc(published) <= received):
            raise ValueError('Invalid chronology')
        authority = event['authority']
        value = encode(event['value'])
        digest = hashlib.sha256(raw).hexdigest()

        with self.writing():
            delivery = self.db.execute('SELECT digest, status FROM deliveries WHERE id=?',
                                       (event['delivery'],)).fetchone()
            if delivery:
                if delivery['digest'] != digest:
                    raise ValueError('Delivery id already refers to different bytes')
                return delivery['status']
            version = self.db.execute('SELECT * FROM versions WHERE source=? AND entity=? AND revision=?',
                                      key).fetchone()
            if version:
                original = tuple(version[k] for k in ('occurred', 'published', 'authority', 'value'))
                status = 'duplicate' if original == (occurred, published, authority, value) else 'conflict'
                self.db.execute('INSERT INTO deliveries VALUES (?, ?, ?, ?, ?)',
                                (event['delivery'], raw, digest, status, version['id']))
            else:
                status = 'admitted'
                self.db.execute('INSERT INTO deliveries VALUES (?, ?, ?, ?, NULL)',
                                (event['delivery'], raw, digest, status))
                row = self.db.execute('''
                    INSERT INTO versions
                    (source, entity, revision, occurred, published, received, admitted,
                     authority, value, admission_rule, origin_delivery)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (*key, occurred, published, received, admitted, authority, value,
                      'chronology-and-identity/1', event['delivery']))
                self.db.execute('UPDATE deliveries SET version_id=? WHERE id=?',
                                (row.lastrowid, event['delivery']))
            if before_commit:
                before_commit()
        return status

    def at(self, keys, cut, frontier=None):
        utc(cut)
        frontier = self.frontier() if frontier is None else frontier
        selected = {}
        for key in sorted(set(keys)):
            row = self.db.execute('''
                SELECT * FROM versions
                WHERE source=? AND entity=? AND admitted<=? AND id<=?
                ORDER BY revision DESC LIMIT 1
            ''', (*key, cut, frontier)).fetchone()
            if row:
                selected[key] = dict(row) | {'value': json.loads(row['value'])}
        return selected

    def frontier(self):
        return self.db.execute('SELECT COALESCE(MAX(id),0) FROM versions').fetchone()[0]

    def diff(self, keys, earlier, later):
        frontier = self.frontier()
        before, after = self.at(keys, earlier, frontier), self.at(keys, later, frontier)
        changed = {}
        for key in sorted(before.keys() | after.keys()):
            old, new = before.get(key), after.get(key)
            if old != new:
                changed[key] = old, new
        return changed

    def decide(self, identity, keys, cut, rule, evaluate):
        keys = tuple(sorted(set(keys)))
        encoded_keys = encode(keys)
        with self.writing():
            existing = self.db.execute('SELECT * FROM decisions WHERE id=?', (identity,)).fetchone()
            if existing:
                if (existing['cut'], existing['rule'], existing['keys_json']) != (cut, rule, encoded_keys):
                    raise ValueError('Decision id already refers to another request')
                return json.loads(existing['result'])
            frontier = self.frontier()
            selected = self.at(keys, cut, frontier)
            result = encode(evaluate(selected))
            self.db.execute('INSERT INTO decisions VALUES (?, ?, ?, ?, ?, ?)',
                            (identity, cut, frontier, rule, encoded_keys, result))
            self.db.executemany('INSERT INTO inputs VALUES (?, ?)',
                                [(identity, row['id']) for row in selected.values()])
            return json.loads(result)

    def trace(self, identity):
        row = self.db.execute('SELECT * FROM decisions WHERE id=?', (identity,)).fetchone()
        if row is None:
            raise KeyError(identity)
        keys = [tuple(key) for key in json.loads(row['keys_json'])]
        selected = self.at(keys, row['cut'], row['frontier'])
        refs = [r[0] for r in self.db.execute('SELECT version FROM inputs WHERE decision=? ORDER BY version',
                                             (identity,))]
        if sorted(r['id'] for r in selected.values()) != refs:
            raise ValueError('Decision lineage does not match the stored frontier')
        return dict(row) | {'result': json.loads(row['result']), 'selected': selected}

    def affected(self, source, entity, revision):
        return [r[0] for r in self.db.execute('''
            SELECT i.decision FROM inputs i JOIN versions v ON i.version=v.id
            WHERE v.source=? AND v.entity=? AND v.revision=? ORDER BY i.decision
        ''', (source, entity, revision))]
