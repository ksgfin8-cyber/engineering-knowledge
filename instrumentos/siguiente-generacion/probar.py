"""Small discriminating experiments. No third-party dependencies."""
import json
from pathlib import Path
import sqlite3


def selection(releases, cuts):
    events = sorted(releases, key=lambda event: event['available'])
    assert len({event['available'] for event in events}) == len(events)
    return [next((e['tenths'] for e in reversed(events) if e['available'] <= cut), None)
            for cut in cuts]


def publication_test():
    source = json.loads(Path(__file__).with_name('bea.json').read_text())
    releases = source['releases']
    cuts = ['2024-04-25T12:29:59Z', '2024-05-30T12:29:59Z', '2024-05-30T12:30:00Z',
            '2024-06-28T00:00:00Z', '2024-09-26T12:30:00Z']
    observed = selection(releases, cuts)
    assert observed == [None, 16, 13, 14, 16]
    assert selection(releases[:-1], cuts[:4]) == observed[:4]
    assert selection(list(reversed(releases)), cuts) == observed
    decisions = [None if value is None else value >= 15 for value in observed]
    assert decisions == [None, True, False, False, True]
    return {'cut_to_value_tenths': list(zip(cuts, observed)), 'threshold_decisions': decisions,
            'latest_only_disagrees_at': sum(value != releases[-1]['tenths'] for value in observed)}


def reconcile_python(left, right, tolerance):
    def index(rows):
        values = {}
        for key, quantity in rows:
            if key in values and values[key] != quantity:
                raise ValueError(f'Conflicting quantity: {key}')
            values[key] = quantity
        return values

    a, b = index(left), index(right)
    rows = []
    for key in sorted(a.keys() | b.keys()):
        x, y = a.get(key), b.get(key)
        if x is None:
            status = 'MISSING_LEFT'
        elif y is None:
            status = 'MISSING_RIGHT'
        else:
            status = 'MATCH' if abs(x - y) <= tolerance else 'QUANTITY_MISMATCH'
        rows.append((key, x, y, status))
    return rows


def reconcile_sql(left, right, tolerance):
    conn = sqlite3.connect(':memory:')
    try:
        conn.execute('CREATE TABLE input (side TEXT, id TEXT, qty INTEGER NOT NULL)')
        conn.executemany('INSERT INTO input VALUES (?, ?, ?)',
                         [(side, key, qty) for side, rows in [('A', left), ('B', right)] for key, qty in rows])
        conflict = conn.execute('''
            SELECT id FROM input GROUP BY side, id
            HAVING MIN(qty) <> MAX(qty) ORDER BY id LIMIT 1
        ''').fetchone()
        if conflict:
            raise ValueError(f'Conflicting quantity: {conflict[0]}')
        return conn.execute('''
            WITH paired AS (
                SELECT id,
                       MAX(CASE WHEN side='A' THEN qty END) AS a,
                       MAX(CASE WHEN side='B' THEN qty END) AS b
                FROM input GROUP BY id
            )
            SELECT id, a, b,
                CASE WHEN a IS NULL THEN 'MISSING_LEFT'
                     WHEN b IS NULL THEN 'MISSING_RIGHT'
                     WHEN ABS(a-b) > ? THEN 'QUANTITY_MISMATCH'
                     ELSE 'MATCH' END
            FROM paired ORDER BY id
        ''', (tolerance,)).fetchall()
    finally:
        conn.close()


def logistics_test():
    left = [('G1', 2), ('G2', 4), ('G2', 4), ('G3', 1)]
    right = [('G4', 5), ('G2', 5), ('G1', 2)]
    expected = [('G1', 2, 2, 'MATCH'), ('G2', 4, 5, 'QUANTITY_MISMATCH'),
                ('G3', 1, None, 'MISSING_RIGHT'), ('G4', None, 5, 'MISSING_LEFT')]
    expected_changed = [*expected[:1], ('G2', 4, 5, 'MATCH'), *expected[2:]]
    for run in (reconcile_python, reconcile_sql):
        assert run(left, right, 0) == expected
        assert run(left, right, 1) == expected_changed
        assert run(list(reversed(left)), right, 1) == expected_changed
        try:
            run([*left, ('G2', 99)], right, 0)
        except ValueError as error:
            assert str(error) == 'Conflicting quantity: G2'
        else:
            raise AssertionError('Conflicting records escaped validation')
    return {'strict': expected, 'tolerant': expected_changed, 'source_edit_required': False}


def adaptive(labels):
    result = []
    history = []
    for actual in labels:
        result.append(history[-1] if len(history) >= 2 and history[-1] == history[-2] else 0)
        history.append(actual)
    return result


def utility(actions, labels):
    return {'utility': sum(0 if a == 0 else 1 if a == y else -2 for a, y in zip(actions, labels)),
            'actions': sum(a != 0 for a in actions)}


def model_test():
    stable = [1] * 16
    broken = [1] * 8 + [-1] * 8
    alternating = [1, -1] * 8
    assert adaptive(stable)[:9] == adaptive(broken)[:9]
    assert adaptive(broken)[8:11] == [1, 0, -1]
    observations = {}
    for name, labels in [('stable', stable), ('break', broken), ('alternating', alternating)]:
        observations[name] = {policy: utility(actions, labels) for policy, actions in [
            ('fixed', [1] * len(labels)), ('abstain', [0] * len(labels)), ('adaptive', adaptive(labels))]}
    wins, dominated = 0, 0
    for case in observations.values():
        adapt = case['adaptive']['utility']
        alternatives = [case[name]['utility'] for name in ('fixed', 'abstain')]
        wins += adapt > max(alternatives)
        dominated += adapt < min(alternatives)
    return {'scenarios': observations, 'wins_against_both': wins, 'strictly_dominated': dominated,
            'advance_under_local_gate': wins >= 2 and dominated == 0}


if __name__ == '__main__':
    assert __debug__, 'Run with assertions enabled'
    print(json.dumps({'bea': publication_test(), 'logistics': logistics_test(), 'model': model_test()},
                     indent=2, sort_keys=True))
