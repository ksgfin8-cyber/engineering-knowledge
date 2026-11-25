"""Run the preregistered oracles and real process interruptions."""
from itertools import permutations
import json
import os
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory

from registro import Ledger, encode

HERE = Path(__file__).resolve().parent
ECONOMY = ('BEA', 'real-gdp-growth/2024Q1')
BEA_CUTS = ['2024-04-25T12:29:59Z', '2024-05-30T12:29:59Z', '2024-05-30T12:30:00Z',
            '2024-05-30T12:30:02Z', '2024-06-28T00:00:00Z', '2024-09-26T12:30:00Z']
EXPECTED_BEA = [None, 16, 16, 13, 14, 16]
LOG_IDS = ['G1', 'G2', 'G3', 'G4']
LOG_CUT = '2024-10-02T12:00:00Z'
CORRECTED = '2024-10-03T12:00:00Z'
LOG_KEYS = [(source, identity) for source in ('dispatch', 'receipt') for identity in LOG_IDS]


def envelope(delivery, key, revision, value, occurred, received, admitted, authority, published=None):
    return dict(delivery=delivery, source=key[0], entity=key[1], revision=revision, value=value,
                occurred=occurred, received=received, admitted=admitted, published=published, authority=authority)


def raw(event):
    return (encode(event) + '\n').encode()


def expect_error(call, fragment):
    try:
        call()
    except ValueError as e:
        assert fragment in str(e), str(e)
    else:
        raise AssertionError(f'Expected failure: {fragment}')


def bea_events():
    source = json.loads((HERE.parent / 'siguiente-generacion/bea.json').read_text())
    for i, row in enumerate(source['releases'], 1):
        stamp = row['available']
        received = '2024-05-30T12:30:01Z' if i == 2 else stamp
        admitted = '2024-05-30T12:30:02Z' if i == 2 else stamp
        yield envelope(f'bea/{i}', ECONOMY, i, row['tenths'], '2024-03-31T23:59:59Z',
                       received, admitted, row['source'], stamp)


def scalar(rows):
    item = rows.get(ECONOMY)
    return None if item is None else item['value']


def threshold(rows):
    value = scalar(rows)
    return None if value is None else value >= 15


def file_reference(events, cuts):
    # Independent, direct scan of the economic fixture, with actual frontiers fixed.
    result = []
    for cut in cuts:
        eligible = [event for event in events if event['admitted'] <= cut]
        result.append(max(eligible, key=lambda event: event['revision'])['value'] if eligible else None)
    return result


def economic(db):
    source = list(bea_events())
    for event in (source[0], source[2], source[1], source[3]):
        assert db.receive(raw(event)) == 'admitted'
    result = [scalar(db.at([ECONOMY], cut)) for cut in BEA_CUTS]
    assert result == EXPECTED_BEA == file_reference(source, BEA_CUTS)
    # Negative design control: last row physically inserted among eligible rows.
    insertion_order = db.db.execute('''
        SELECT value FROM versions WHERE source=? AND entity=? AND admitted<=?
        ORDER BY id DESC LIMIT 1
    ''', (*ECONOMY, BEA_CUTS[4])).fetchone()
    assert json.loads(insertion_order['value']) == 13 and result[4] == 14
    decisions = [db.decide(f'gdp/{i}', [ECONOMY], cut, 'gdp-threshold/1', threshold)
                 for i, cut in enumerate(BEA_CUTS)]
    assert decisions == [None, True, True, False, False, True]
    saved = db.trace('gdp/4')
    assert saved['result'] is False and threshold(saved['selected']) is False
    assert db.affected(*ECONOMY, 3) == ['gdp/4']
    diff = db.diff([ECONOMY], BEA_CUTS[2], BEA_CUTS[3])[ECONOMY]
    assert [d['revision'] for d in diff] == [1, 2]
    duplicate = source[2] | {'delivery': 'bea/retransmission'}
    conflict = duplicate | {'delivery': 'bea/conflict', 'value': 99}
    assert db.receive(raw(duplicate)) == 'duplicate'
    assert db.receive(raw(conflict)) == 'conflict'
    assert db.receive(raw(conflict)) == 'conflict'
    assert scalar(db.at([ECONOMY], BEA_CUTS[4])) == 14
    illegal = duplicate | {'delivery': 'invalid-clock', 'received': '2024-06-27T12:29:59Z'}
    expect_error(lambda: db.receive(raw(illegal)), 'Invalid chronology')
    audit = db.db.execute('SELECT raw, status FROM deliveries WHERE id=?', ('bea/conflict',)).fetchone()
    assert audit['raw'] == raw(conflict) and audit['status'] == 'conflict'
    expect_error(lambda: db.receive(raw(duplicate | {'value': 100})), 'different bytes')
    # Synthetic backfill deliberately carries an effective admission earlier than an already recorded decision.
    backfill = source[3] | {
        'delivery': 'synthetic-backfill', 'revision': 5, 'value': 17, 'published': None,
        'received': '2024-06-28T00:00:00Z', 'admitted': '2024-06-28T00:00:00Z',
        'authority': 'backfill-fixture',
    }
    assert db.receive(raw(backfill)) == 'admitted'
    assert scalar(db.at([ECONOMY], BEA_CUTS[4])) == 17
    assert db.trace('gdp/4') == saved
    assert db.decide('gdp/4', [ECONOMY], BEA_CUTS[4], 'gdp-threshold/1', threshold) is False
    expect_error(lambda: db.decide('gdp/4', [ECONOMY], BEA_CUTS[5], 'gdp-threshold/1', threshold),
                 'another request')
    return {'cut_values_tenths': result, 'latest_only_wrong': sum(x != 16 for x in result),
            'decisions_changed_by_latest_only': sum(x is False for x in decisions),
            'arrival_order_wrong_at_june': 13,
            'backfill_current_value': 17, 'historical_value_preserved': scalar(saved['selected']),
            'duplicate': 'duplicate', 'conflict': 'conflict', 'affected_by_revision_3': ['gdp/4']}


def bounded_order_check():
    count = 0
    for events in permutations(bea_events()):
        db = Ledger(':memory:')
        try:
            for event in events:
                db.receive(raw(event))
            assert [scalar(db.at([ECONOMY], cut)) for cut in BEA_CUTS] == EXPECTED_BEA
            count += 1
        finally:
            db.close()
    assert count == 24
    return count


def logistics_events():
    for src, codes in [('dispatch', [('G1', 2), ('G2', 4), ('G3', 1)]),
                       ('receipt', [('G1', 2), ('G2', 5), ('G4', 5)])]:
        for key, value in codes:
            yield envelope(f'{src}/{key}/1', (src, key), 1, value, '2024-10-01T12:00:00Z', LOG_CUT,
                           LOG_CUT, f'{src}-fixture/{key}')


def reconcile(rows, tolerance):
    result = {}
    for key in LOG_IDS:
        sent, got = (rows.get((side, key)) for side in ('dispatch', 'receipt'))
        if sent is None:
            result[key] = 'MISSING_DISPATCH'
        elif got is None:
            result[key] = 'AWAITING_RECEIPT'
        elif abs(sent['value'] - got['value']) > tolerance:
            result[key] = 'DIFFERENCE'
        else:
            result[key] = 'MATCH'
    return result


def logistics(db):
    records = list(logistics_events())
    for event in records:
        assert db.receive(raw(event)) == 'admitted'
    base = {'G1': 'MATCH', 'G2': 'DIFFERENCE', 'G3': 'AWAITING_RECEIPT', 'G4': 'MISSING_DISPATCH'}
    changed = base | {'G2': 'MATCH'}
    assert db.decide('log/v1', LOG_KEYS, LOG_CUT, 'tolerance-zero/1',
                     lambda rows: reconcile(rows, 0)) == base
    assert db.decide('log/v2', LOG_KEYS, LOG_CUT, 'tolerance-one/1',
                     lambda rows: reconcile(rows, 1)) == changed
    saved = db.trace('log/v1')
    correction = next(e for e in records if e['source'] == 'receipt' and e['entity'] == 'G2')
    correction |= {'delivery': 'receipt/G2/2', 'revision': 2, 'value': 4, 'authority': 'receipt-fixture/G2-correction',
                   'received': CORRECTED, 'admitted': CORRECTED}
    assert db.receive(raw(correction)) == 'admitted'
    assert db.decide('log/corrected', LOG_KEYS, CORRECTED, 'tolerance-zero/1',
                     lambda rows: reconcile(rows, 0)) == changed
    assert db.trace('log/v1') == saved
    assert reconcile(saved['selected'], 0) == saved['result']
    assert db.affected('receipt', 'G2', 1) == ['log/v1', 'log/v2']
    assert ('receipt', 'G3') not in saved['selected']
    assert saved['result']['G3'] == 'AWAITING_RECEIPT'
    return {'zero': base, 'one': changed, 'corrected_zero': changed,
            'affected_by_correction': ['log/v1', 'log/v2'],
            'web_rule_regression': {'prepared_without_receipt': 'AWAITING_RECEIPT',
                                    'matches_with_receipt': 'MATCH'}}


def child(path, delivery_path, stage):
    ledger = Ledger(path)
    hook = (lambda: os._exit(71)) if stage == 'before' else None
    ledger.receive(Path(delivery_path).read_bytes(), hook)
    os._exit(72)


def interruption(root):
    event = raw(next(iter(logistics_events())))
    payload = root / 'event.json'
    payload.write_bytes(event)
    clean = Ledger(root / 'clean.sqlite')
    assert clean.receive(event) == 'admitted'
    expected = clean.at(LOG_KEYS, LOG_CUT)
    clean.close()
    results = {}
    for stage, code, durable in [('before', 71, 0), ('after', 72, 1)]:
        file = root / (stage + '.sqlite')
        work = subprocess.run([sys.executable, __file__, '--child', str(file), str(payload), stage],
                              check=False, capture_output=True, timeout=10)
        assert work.returncode == code, work.stderr
        recovered = Ledger(file)
        count = recovered.db.execute('SELECT COUNT(*) FROM deliveries').fetchone()[0]
        assert count == durable
        assert recovered.frontier() == durable
        assert recovered.receive(event) == 'admitted'
        assert recovered.at(LOG_KEYS, LOG_CUT) == expected
        assert recovered.db.execute('SELECT COUNT(*) FROM deliveries').fetchone()[0] == 1
        recovered.close()
        results[stage] = {'durable_before_retry': durable, 'same_as_clean': True}
    return results


def main():
    with TemporaryDirectory() as tmp:
        root = Path(tmp)
        db = Ledger(root / 'one.sqlite')
        result = {'economy': economic(db), 'logistics': logistics(db), 'interruption': interruption(root),
                  'bounded_permutations': bounded_order_check()}
        db.close()
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == '__main__':
    assert __debug__, 'Run with assertions enabled'
    if sys.argv[1:2] == ['--child']:
        child(*sys.argv[2:])
    else:
        main()
