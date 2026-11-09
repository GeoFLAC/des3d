---
sidebar_position: 6
slug: /getting-started/troubleshooting
title: Troubleshooting
description: Common problems when building and running DynEarthSol, and where to look first.
---

# Troubleshooting

When a run stops, DynEarthSol prints a two-digit exit code and its category.
The first digit says where to look: `1x` is the input, `2x` the environment
(files, libraries), and `3x`–`6x` the computation or the code itself. The
full table is in [exit codes](../user-guide/running/diagnostics.md#exit-codes).

## Building

| Symptom | Check |
| --- | --- |
| HDF5 headers or library not found | Install the development package (`libhdf5-dev` on Ubuntu, `hdf5` with Homebrew). Python's `h5py` does not provide it. Set `HDF5_INCLUDE_DIR` and `HDF5_LIB_DIR` only if the wrong installation is picked up. Or build without it: `make hdf5=0`. |
| `omp.h` or `libomp` not found on macOS | `brew install libomp`, then rebuild. |
| Missing `nanoflann`, `knn-bvh` or `mmg` sources | The repository uses submodules: clone with `--recursive`, or run `git submodule update --init`. |
| An option a page uses is not recognized | The executable is from an older revision. Check `./dynearthsol2d -h` and the revision a tutorial was checked with (its *At a glance* box). |

See [Installation](./installation.md) for dependencies and build options.

## Starting a run

| Symptom | Check |
| --- | --- |
| Exit `10` or `11` before the first step | A configuration error: a misspelled or retired parameter, or a value out of range. The message names the parameter. Look it up in the [parameter reference](../reference/parameters.md). |
| Exit `12` | The `.poly` or `.exo` mesh file is malformed. See [making a mesh with a `.poly` file](../user-guide/model-setup/poly-meshes.md). |
| `.poly` file not found | Run from the directory that holds both the input file and the `.poly` file, or give its path in `mesh.poly_filename`. |
| Exit `21` or `22` when restarting | The checkpoint does not match this executable: it was written by an older file-format revision or lacks records this version needs. See [checkpointing and restart](../user-guide/running/restart.md). |
| Exit `30` or `31` | The feature is not available in this dimension, or the executable was built without the library it needs (for example MMG or GoSPL). |

## During a run

| Symptom | Check |
| --- | --- |
| Exit `50`: NaN or non-finite value | The run prints the affected fields and the first bad element and node. Common causes are a time step too large (`control.dt_fraction`), a `control.inertial_scaling` so small that inertia dominates (see [mass scaling](../theory/solution-scheme/massscaling.md)), or a badly distorted mesh. |
| Exit `54`: PT did not converge | See the PT controls in [choosing a mechanical solver](../user-guide/numerical-controls/solver.md). |
| Exit `40`–`42`: meshing failed | The mesh became too distorted for Triangle, TetGen or MMG to rebuild. Check the quality settings in `[mesh]` and the [remeshing](../theory/remeshing.md) options. |
| Warning that element groups may share nodes | A possible OpenMP race. Increase the resolution or use fewer threads. |
| Very slow on a small mesh | Too many threads for the work: set `OMP_NUM_THREADS=1` (or a few) and `OMP_DYNAMIC=FALSE`. |

## Output

| Symptom | Check |
| --- | --- |
| No `.vtkhdf` files | VTKHDF needs an HDF5 build (`hdf5=1`). Otherwise convert the binary frames with `2vtk.py`. |
| `2vtk.py` skips frames of a restarted run | Convert with `2vtk.py -g <restarted modelname>` to include the parent run's frames. See [visualizing outputs](./visualize.md#restarted-models). |
| Lost `.info` file | `utils/recreate_info.py` rebuilds it from the frame files. |

## Getting help

If the problem remains, open an issue in the
[DynEarthSol issue tracker](https://github.com/GeoFLAC/DynEarthSol/issues)
with the input file, the exit code and message, and the run's
`<modelname>.manifest`, which records how the executable was built and run.
