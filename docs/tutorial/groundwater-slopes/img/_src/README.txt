# Groundwater and slope figure sources

Set `DES_DIR` to the DynEarthSol checkout. Each `qualify_*.py` exposes the
`build` function described in its docstring and reads a saved study folder.
Shared style, plotting helpers and setup drawings are imported from
`docs/benchmarks/poromechanics/img/_src/`. Numerical study runners remain in
DynEarthSol; no simulation is started by these builders.
