"""Ejecuta una sonda de dominio y valida un registro de caracterización v0.1."""

import argparse
import json
import math
import subprocess
import sys
import time


def require(condition, message):
    if not condition:
        raise ValueError(message)


def validate_probe(probe):
    require(isinstance(probe, dict) and isinstance(probe.get("inputs"), dict),
            "La sonda debe indicar sus entradas")
    cases = probe.get("cases")
    require(isinstance(cases, list) and len(cases) == 3,
            "Se requieren control positivo, negativo y candidato")
    require([case.get("role") for case in cases] == ["positive", "negative", "candidate"],
            "Orden de casos inválido")
    for case in cases:
        require(isinstance(case.get("observed"), dict), "Falta la observación")
        require(type(case.get("passes")) is bool, "Falta resultado booleano")
    require(cases[0]["passes"], "Falló el control positivo")
    require(not cases[1]["passes"], "El control negativo escapó")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--candidate", required=True)
    parser.add_argument("--revision", required=True)
    parser.add_argument("--protocol", required=True)
    parser.add_argument("command", nargs=argparse.REMAINDER)
    args = parser.parse_args()
    command = args.command[1:] if args.command[:1] == ["--"] else args.command
    if not command:
        parser.error("Indique el comando de la sonda después de --")

    record = {
        "schema": "characterization/0.1",
        "candidate": args.candidate,
        "revision": args.revision,
        "protocol": args.protocol,
    }
    start = time.perf_counter()
    try:
        run = subprocess.run(command, capture_output=True, text=True, timeout=30)
        require(run.returncode == 0, f"Sonda terminó con código {run.returncode}: {run.stderr.strip()}")
        probe = json.loads(run.stdout)
        validate_probe(probe)
        record.update(probe=probe, status="cumple" if probe["cases"][2]["passes"] else "refuta")
    except (OSError, subprocess.TimeoutExpired, ValueError, TypeError, AttributeError) as error:
        record.update(status="error_de_sondeo", error=str(error))
    elapsed = time.perf_counter() - start
    assert math.isfinite(elapsed)
    print(json.dumps(record, ensure_ascii=False, sort_keys=True, allow_nan=False))
    print(f"tiempo_sonda_s={elapsed:.6f}", file=sys.stderr)
    return 1 if record["status"] == "error_de_sondeo" else 0


if __name__ == "__main__":
    sys.exit(main())
