"""Locate the DES reader, reference solutions and study checks."""
import os
import sys
from pathlib import Path

ROOT = Path(os.environ.get('DES_DIR', '.')).resolve()
if not (ROOT/'Dynearthsol.py').is_file():
    raise RuntimeError('Set DES_DIR to the DynEarthSol checkout')
sys.path[:0] = [str(ROOT), str(ROOT/'benchmarks/poromechanics'),
                str(ROOT/'tests/functional'), str(ROOT/'tests/functional/hydromechanics')]

# The checked model revision predates the separation of plotting and checking.
if not (ROOT/'benchmarks/poromechanics/consolidation.py').is_file():
    import importlib.util
    spec = importlib.util.spec_from_file_location('consolidation', ROOT/'benchmarks/poromechanics/prepare_figures.py')
    legacy = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(legacy)
    sys.modules['consolidation'] = legacy
