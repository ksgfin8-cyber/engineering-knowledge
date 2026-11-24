from datetime import date, timedelta
from fractions import Fraction
import unittest

from ejecutar import from_csv, normalize, release, stream_forecasts


def row(day, close, rev=1, delay=0):
    return {'session': day.isoformat(), 'close_milli': close, 'revision': rev,
            'available_at': (release(day) + timedelta(days=delay)).isoformat()}


class TemporalTest(unittest.TestCase):
    start = date(2025, 1, 1)

    def daily(self, index, **kwargs):
        return row(self.start + timedelta(days=index), 1000 * (index + 1), **kwargs)

    def test_missing_duplicate_and_late(self):
        first = self.daily(0)
        late = self.daily(1, delay=2)
        fourth = self.daily(3)
        dates = [(self.start + timedelta(days=i)).isoformat() for i in range(4)]
        data, audit = normalize([fourth, late, first, first.copy()], dates)
        self.assertEqual(audit['duplicate'], 1)
        self.assertEqual(audit['missing_expected_sessions'], [dates[2]])
        origins = list(stream_forecasts(data, dates, 1))
        self.assertEqual([a['last_milli'] for a in origins], [1000, 1000, 1000, 4000])
        self.assertEqual([a['session'] for a in data], [dates[0], dates[1], dates[3]])

    def test_revision_only_after_availability(self):
        original = self.daily(0)
        changed = {**self.daily(0, rev=2, delay=1), 'close_milli': 9000}
        second = self.daily(1)
        data, audit = normalize([changed, second, original])
        rows = list(stream_forecasts(data, [original['session'], second['session']], 1))
        self.assertEqual(audit['revisions'], 1)
        self.assertEqual([r['last_milli'] for r in rows], [1000, 2000])
        rows = list(stream_forecasts(data, [original['session'], second['session']], 2))
        self.assertEqual(rows[0]['mean_milli'], Fraction(5500))
        self.assertEqual(rows[0]['information'][0], [original['session'], 2])

    def test_conflict(self):
        first = self.daily(0)
        with self.assertRaisesRegex(ValueError, 'Conflicting revision'):
            normalize([first, {**first, 'close_milli': 9000}])

    def test_invalid_csv(self):
        raw = b'DATE,OPEN,HIGH,LOW,CLOSE\n2025-01-01,10,8,5,9\n'
        with self.assertRaisesRegex(ValueError, 'OHLC contradiction'):
            list(from_csv(raw))
        quarantine = []
        self.assertEqual(list(from_csv(raw, quarantine)), [])
        self.assertEqual(quarantine[0]['line'], 2)
        self.assertEqual(quarantine[0]['source_row']['CLOSE'], '9')

    def test_known_mean_and_future_perturbation(self):
        data = [self.daily(i) for i in range(7)]
        altered = [*data[:5], *[{**row, 'close_milli': 9000} for row in data[5:]]]
        dates = [row['session'] for row in data]
        left, right = (list(stream_forecasts(normalize(values)[0], dates, 5)) for values in (data, altered))
        self.assertEqual(left[0]['mean_milli'], Fraction(3000))
        self.assertEqual(left[0], right[0])
        self.assertNotEqual(left[1]['mean_milli'], right[1]['mean_milli'])


if __name__ == '__main__':
    unittest.main()
