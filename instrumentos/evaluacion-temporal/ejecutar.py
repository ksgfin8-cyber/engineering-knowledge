"""Transform an immutable daily VIX snapshot and score two causal references."""
import argparse
import csv
from datetime import date, datetime, time, timedelta, timezone
from fractions import Fraction
import hashlib
import io
import json
from pathlib import Path
from statistics import mean

SOURCE = '3dbea23c70cc2afbeeec8ac232c9ec72ac26ac21'
RAW_HASH = '570e05630c9a5e7350d0c3dbe3acc58e793cb5248181ab0e949c121cc082fb83'
SAMPLE = date(2025, 1, 1)
COLUMNS = ['DATE', 'OPEN', 'HIGH', 'LOW', 'CLOSE']


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def jsonline(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'), allow_nan=False) + '\n'


def release(day):
    return datetime.combine(day + timedelta(days=1), time(), timezone.utc)


def milli(value):
    points = Fraction(value) * 1000
    if points.denominator != 1 or points <= 0:
        raise ValueError('Expected a positive multiple of 0.001 VIX points')
    return int(points)


def from_csv(raw, quarantine=None):
    reader = csv.DictReader(io.StringIO(raw.decode('ascii'), newline=''))
    if reader.fieldnames != COLUMNS:
        raise ValueError('Unexpected CSV schema')
    for line, row in enumerate(reader, 2):
        if set(row) != set(COLUMNS) or None in row.values():
            raise ValueError(f'Invalid CSV line {line}')
        day = date.fromisoformat(row['DATE'])
        opening, high, low, close = (milli(row[field]) for field in COLUMNS[1:])
        if not low <= min(opening, close) <= max(opening, close) <= high:
            if quarantine is None:
                raise ValueError(f'OHLC contradiction on line {line}')
            quarantine.append({'line': line, 'reason': 'OHLC_CONTRADICTION', 'source_row': row})
            continue
        yield {'session': day.isoformat(), 'available_at': release(day).isoformat(),
               'revision': 1, 'close_milli': close}


def normalize(raw_events, expected=()):
    seen = {}
    duplicates = 0
    for row in raw_events:
        day = date.fromisoformat(row['session'])
        available = datetime.fromisoformat(row['available_at'])
        if available.utcoffset() != timedelta(0) or available < release(day):
            raise ValueError('Availability precedes the simulated release or is not UTC')
        if type(row['close_milli']) is not int or row['close_milli'] <= 0:
            raise ValueError('Invalid close')
        if type(row['revision']) is not int or row['revision'] <= 0:
            raise ValueError('Invalid revision')
        identity = (row['session'], row['revision'])
        if identity in seen:
            if seen[identity] != row:
                raise ValueError(f'Conflicting revision {identity}')
            duplicates += 1
        seen[identity] = row
    previous = {}
    for row in sorted(seen.values(), key=lambda a: (a['session'], a['revision'])):
        session = row['session']
        available = datetime.fromisoformat(row['available_at'])
        if session in previous and available <= previous[session]:
            raise ValueError('Revisions must have strictly increasing availability')
        previous[session] = available
    ordered = sorted(seen.values(), key=lambda a: (datetime.fromisoformat(a['available_at']), a['session']))
    report = {'accepted': len(ordered), 'duplicate': duplicates, 'revisions': len(ordered) - len(previous),
              'missing_expected_sessions': sorted(set(expected).difference(previous))}
    return ordered, report


def stream_forecasts(events, dates, window):
    versions = {}
    labels = sorted({row['session'] for row in events})
    iterator = iter(events)
    upcoming = next(iterator, None)
    for origin in dates:
        cutoff = release(date.fromisoformat(origin))
        while upcoming is not None and datetime.fromisoformat(upcoming['available_at']) <= cutoff:
            versions[upcoming['session']] = upcoming
            upcoming = next(iterator, None)
        eligible = [versions[key] for key in labels if key <= origin and key in versions]
        if len(eligible) < window:
            continue
        used = eligible[-window:]
        yield {'origin': origin, 'cutoff': cutoff.isoformat(), 'last_milli': used[-1]['close_milli'],
               'mean_milli': mean(Fraction(row['close_milli']) for row in used),
               'information': [[row['session'], row['revision']] for row in used]}


def score(events, window):
    last_revision = {row['session']: row['close_milli'] for row in events}
    dates = sorted(last_revision)
    target_of = dict(zip(dates, dates[1:]))
    origins = [origin for origin in dates[:-1] if origin >= SAMPLE.isoformat()]
    for row in stream_forecasts(events, origins, window):
        target = target_of[row['origin']]
        avg = row.pop('mean_milli')
        actual = last_revision[target]
        yield {**row, 'target': target, 'target_milli': actual, 'mean_milli_ratio': str(avg),
               'ae_last_milli': abs(actual - row['last_milli']), 'ae_mean_milli_ratio': str(abs(actual - avg))}


def run(raw_path, output, window, quarantine_ohlc=False):
    if window < 1:
        raise ValueError('Window must be positive')
    raw = raw_path.read_bytes()
    if sha(raw) != RAW_HASH:
        raise ValueError('Unexpected raw snapshot SHA-256')
    quarantine = [] if quarantine_ohlc else None
    data, intake = normalize(from_csv(raw, quarantine))
    rejected = quarantine or []
    output.mkdir(parents=True, exist_ok=False)
    (output / 'bruto.csv').write_bytes(raw)
    quarantine_path = output / 'cuarentena.jsonl'
    quarantine_path.write_text(''.join(map(jsonline, rejected)), encoding='utf-8')
    dataset = output / 'observaciones.jsonl'
    dataset.write_text(''.join(map(jsonline, data)), encoding='utf-8')
    data_from_disk = [json.loads(line) for line in dataset.read_text(encoding='utf-8').splitlines()]
    rows = list(score(data_from_disk, window))
    if not rows:
        raise ValueError('Empty evaluation sample')
    evaluation = output / 'evaluacion.jsonl'
    evaluation.write_text(''.join(map(jsonline, rows)), encoding='utf-8')
    manifest = {'source_commit': SOURCE, 'raw_sha256': sha(raw), 'dataset_sha256': sha(dataset.read_bytes()),
                'evaluation_sha256': sha(evaluation.read_bytes()), 'observations': intake,
                'quarantine_sha256': sha(quarantine_path.read_bytes()), 'quarantined': len(rejected),
                'ohlc_policy': 'QUARANTINE' if quarantine_ohlc else 'REJECT_SNAPSHOT',
                'rules': 'vix-snapshot-replay/1', 'availability': 'SIMULATED_NEXT_UTC_MIDNIGHT',
                'window': window, 'origins': len(rows), 'first_origin': rows[0]['origin'],
                'last_origin': rows[-1]['origin'], 'last_target': rows[-1]['target'],
                'mae_last_vix_points': float(mean(row['ae_last_milli'] for row in rows) / 1000),
                'mae_mean_vix_points': float(mean(Fraction(row['ae_mean_milli_ratio']) for row in rows) / 1000)}
    (output / 'manifiesto.json').write_text(jsonline(manifest), encoding='utf-8')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('raw', type=Path)
    parser.add_argument('output', type=Path)
    parser.add_argument('--window', type=int, default=5)
    parser.add_argument('--quarantine-ohlc', action='store_true')
    args = parser.parse_args()
    run(args.raw, args.output, args.window, args.quarantine_ohlc)
