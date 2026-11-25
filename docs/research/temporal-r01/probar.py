"""Run the pre-registered temporal comparison with two local stores."""
from hashlib import sha256
import json
from pathlib import Path
import sys
from tempfile import TemporaryDirectory

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "instrumentos/registro-versionado"))
from registro import Ledger

KEY = ("local", "serie")
RULE = "P1/persistencia-v1"
H = "2026-01-02T12:00:00Z"
R = "2026-01-03T12:00:00Z"
P = "2026-01-04T12:00:00Z"
AFTER = "2026-01-04T12:06:00Z"


def forecast(row, delivery):
    return {"revision": row["revision"], "entrega": row[delivery],
            "pronostico": row["value"], "referencia": 10}


class Archive:
    """Single writer. Keep original bytes and checkpoint the exact prefix."""

    def __init__(self, directory):
        self.log = directory / "entregas.jsonl"
        self.directory = directory
        self.log.touch(exist_ok=True)

    @staticmethod
    def versions(raw):
        versions = {}
        for line in raw.splitlines():
            row = json.loads(line)
            key = row["source"], row["entity"], row["revision"]
            versions.setdefault(key, row)
        return versions

    def receive(self, raw):
        row = json.loads(raw)
        key = row["source"], row["entity"], row["revision"]
        prior = self.versions(self.log.read_bytes()).get(key)
        fields = ("occurred", "published", "authority", "value")
        if prior is None:
            status = "admitted"
        elif tuple(prior[f] for f in fields) == tuple(row[f] for f in fields):
            status = "duplicate"
        else:
            status = "conflict"
        with self.log.open("ab") as stream:
            stream.write(raw)
        return status

    def query(self, cut, raw=None):
        if raw is None:
            raw = self.log.read_bytes()
        eligible = (row for key, row in self.versions(raw).items()
                    if key[:2] == KEY and row["admitted"] <= cut)
        return forecast(max(eligible, key=lambda row: row["revision"]), "delivery")

    def decide(self, name, cut):
        raw = self.log.read_bytes()
        result = self.query(cut, raw)
        checkpoint = {"cut": cut, "rule": RULE, "key": list(KEY),
                      "frontier": len(raw), "sha256": sha256(raw).hexdigest(),
                      "result": result}
        with (self.directory / name).open("x") as stream:
            json.dump(checkpoint, stream)
        return result

    def trace(self, name):
        checkpoint = json.loads((self.directory / name).read_text())
        with self.log.open("rb") as stream:
            raw = stream.read(checkpoint["frontier"])
        assert sha256(raw).hexdigest() == checkpoint["sha256"], checkpoint
        assert checkpoint["rule"] == RULE and checkpoint["key"] == list(KEY)
        result = self.query(checkpoint["cut"], raw)
        assert result == checkpoint["result"], (result, checkpoint)
        return result

    def close(self):
        pass


class SQLite:
    def __init__(self, directory):
        self.ledger = Ledger(directory / "registro.sqlite")

    def receive(self, raw):
        return self.ledger.receive(raw)

    def query(self, cut):
        return self.evaluate(self.ledger.at([KEY], cut))

    @staticmethod
    def evaluate(selected):
        return forecast(selected[KEY], "origin_delivery")

    def decide(self, name, cut):
        return self.ledger.decide(name, [KEY], cut, RULE, self.evaluate)

    def trace(self, name):
        trace = self.ledger.trace(name)
        assert trace["rule"] == RULE
        result = self.evaluate(trace["selected"])
        assert result == trace["result"], (result, trace["result"])
        return result

    def close(self):
        self.ledger.close()


def exercise(store_type, deliveries):
    with TemporaryDirectory() as directory:
        root = Path(directory)
        store = store_type(root)
        status = [store.receive(deliveries[0])]
        report = {"H inicial": store.decide("H", H)}
        status.append(store.receive(deliveries[1]))
        store.close()
        store = store_type(root)
        report["H reconstruida"] = store.trace("H")
        report["Retrospectiva"] = store.query(R)
        status.append(store.receive(deliveries[2]))
        report["Retrospectiva tras retransmision"] = store.query(R)
        report["P inicial"] = store.decide("P", P)
        status.append(store.receive(deliveries[3]))
        store.close()
        store = store_type(root)
        report["P reconstruida"] = store.trace("P")
        report["P consultada tras perturbacion"] = store.query(P)
        report["H tras perturbacion"] = store.trace("H")
        report["Corte posterior"] = store.query(AFTER)
        report["Estado de entregas"] = status
        if store_type is Archive:
            assert store.log.read_bytes() == b"".join(deliveries)
        else:
            stored = store.ledger.db.execute("SELECT raw FROM deliveries ORDER BY rowid")
            assert [raw for (raw,) in stored] == deliveries
        store.close()
        return report


def main():
    deliveries = (HERE / "entregas.jsonl").read_bytes().splitlines(keepends=True)
    expected = {
        "H inicial": (1, "D1", 10),
        "H reconstruida": (1, "D1", 10),
        "Retrospectiva": (2, "D2", 14),
        "Retrospectiva tras retransmision": (2, "D2", 14),
        "P inicial": (2, "D2", 14),
        "P reconstruida": (2, "D2", 14),
        "P consultada tras perturbacion": (2, "D2", 14),
        "H tras perturbacion": (1, "D1", 10),
        "Corte posterior": (3, "D4", 99),
    }
    for store_type in (Archive, SQLite):
        report = exercise(store_type, deliveries)
        print(json.dumps({store_type.__name__: report}, sort_keys=True))
        for label, (revision, delivery, value) in expected.items():
            assert report[label] == {"revision": revision, "entrega": delivery,
                                     "pronostico": value, "referencia": 10}, label
        assert report["Estado de entregas"] == ["admitted", "admitted", "duplicate", "admitted"]

    rows = Archive.versions(b"".join(deliveries[:2]))
    negative = forecast(max(rows.values(), key=lambda row: row["revision"]), "delivery")
    print(json.dumps({"control H sin corte": negative}, sort_keys=True))
    assert negative == {"revision": 2, "entrega": "D2", "pronostico": 14, "referencia": 10}


if __name__ == "__main__":
    main()
