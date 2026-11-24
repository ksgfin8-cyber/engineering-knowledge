"""Sonda de la revisión histórica de F001 para el caso de dos elementos."""

import importlib.machinery
import importlib.util
import json
import sys
from pathlib import Path

source = Path(sys.argv[1]).resolve()
loader = importlib.machinery.SourceFileLoader("f001_candidate", str(source))
spec = importlib.util.spec_from_loader(loader.name, loader)
module = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = module
loader.exec_module(module)

data = [2, 1]
expected = [1, 2]


def check(role, sorter):
    values = data.copy()
    failure = None
    try:
        sorter(values)
    except AssertionError as error:
        failure = {"type": type(error).__name__, "message": str(error)}
    return {"role": role, "passes": failure is None and values == expected,
            "observed": {"output": values, "exception": failure}}


print(json.dumps({
    "inputs": {"sequence": data, "expected": expected},
    "cases": [
        check("positive", list.sort),
        check("negative", lambda values: None),
        check("candidate", lambda values: module.mergesort(values, 1, len(values))),
    ],
}, ensure_ascii=False))
