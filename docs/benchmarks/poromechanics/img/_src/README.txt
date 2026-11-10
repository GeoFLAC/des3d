# Poromechanics figure sources

Set `DES_DIR` to a DynEarthSol checkout. NumPy, SciPy, Matplotlib and the DES
Python reader are required. These scripts read saved study folders; DES study
runners and their pass/fail checks remain in DynEarthSol.

```sh
export DES_DIR=/path/to/DynEarthSol
python3 prepare_figures.py /path/to/saved/consolidation
python3 plot_storage.py /path/to/saved/storage-comparison
python3 plot_studies.py refinement /path/to/saved/refinement
python3 plot_studies.py methods /path/to/saved/mechanical-methods
python3 recovery.py /path/to/saved/pore-recovery /new/figures
python3 plot_elder.py /path/to/saved/elder /path/to/saved/reference.npz /new/elder
```

The `qualify_*.py` modules expose `build(study, output, record_source, ...)`
for individual comparisons. `record_source(path)` records every consumed
file; `output` contains `figures/` and `data/`. Their module docstrings give
the additional study/control arguments. References and checks are imported
from `DES_DIR`, with no copied implementations here. The five slope and
groundwater application builders live beside their tutorial figures.
`setup_drawings.py OUTPUT --only CASE` writes the geometry and boundary
schematics, using the same `diagram_style.py` as the result plots.
