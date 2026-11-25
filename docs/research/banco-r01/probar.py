"""Exercise two transitions for one confirmation consumer."""
import json


def run(events, mutate_on_receipt):
    admitted_ids = set()
    memory = 0
    trace = []
    for event in events:
        if mutate_on_receipt:
            memory += 1
        admitted = event not in admitted_ids
        if admitted:
            admitted_ids.add(event)
            if not mutate_on_receipt:
                memory += 1
        decision = "actuar" if memory >= 2 else "abstenerse"
        trace.append({"evento": event, "admitido": admitted,
                      "memoria": memory, "decision": decision})
    return trace


def main():
    cases = (
        ("una", ("A",), [(1, "abstenerse")]),
        ("retransmision", ("A", "A"), [(1, "abstenerse"), (1, "abstenerse")]),
        ("limpia", ("A", "B"), [(1, "abstenerse"), (2, "actuar")]),
    )
    for design, early in (("A/al_admitir", False), ("B/al_recibir", True)):
        differences = []
        clean_final = None
        for case, events, oracle in cases:
            trace = run(events, early)
            print(json.dumps({"diseno": design, "caso": case, "traza": trace}))
            assert len(trace) == len(oracle)
            for step, (observed, expected) in enumerate(zip(trace, oracle), 1):
                actual = observed["memoria"], observed["decision"]
                if actual != expected:
                    differences.append({"caso": case, "paso": step,
                                        "esperado": expected, "observado": actual,
                                        "admitido": observed["admitido"]})
            if case == "limpia":
                clean_final = trace[-1]["decision"]
        print(json.dumps({"diseno": design, "divergencias": differences,
                          "salida_final_limpia": clean_final}))
        assert clean_final == "actuar"
        expected_differences = [] if not early else [
            {"caso": "retransmision", "paso": 2, "esperado": (1, "abstenerse"),
             "observado": (2, "actuar"), "admitido": False}
        ]
        assert differences == expected_differences, differences


if __name__ == "__main__":
    main()
