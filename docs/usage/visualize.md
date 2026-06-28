---
sidebar_position: 3
---

# Visualizing outputs {#visualization}

## Converting output to VTK format

To convert the binary output files to VTU files, run

``` console
2vtk.py modelname
```

`modelname` should be the one defined in the config file.

To see full usage information (including options for marker data VTP files), run

``` console
2vtk.py -h
```

The processed VTU (node and cell data) and VTP (marker data) files can
be visualized with [ParaView](https://paraview.org) or
[VisIt](https://visit-dav.github.io/visit-website/index.html).

Some outputs can be disabled by editing `2vtk.py` and `output.cxx`.

## VTKHDF output format

DES3D can write output in the **VTKHDF** format (`.vtkhdf`), a
self-contained HDF5-based format supported by ParaView 5.11+. VTKHDF
files bundle all time steps into a single file, making them easier to
manage for long runs than the equivalent per-step VTU collection.

### Updating an existing VTKHDF file

The `-u` / `--update-vtkhdf` flag lets you add or recompute derived
fields (e.g., strain-rate invariants, second invariant of stress) in an
existing `.vtkhdf` file without regenerating it from scratch. This is
useful when you want to add a newly supported output quantity to a
completed run.

```console
2vtk.py --update-vtkhdf modelname.vtkhdf
```

**Requirements:** `h5py` must be installed (`pip install h5py` or
`conda install h5py`).

**Safety:** The update is performed in-place. Back up your file before
running if it is large or irreplaceable. The script prints a warning and
exits if the target file does not look like a valid VTKHDF file.

:::caution HDF5 file locking
On some parallel or network filesystems, HDF5 file locking can cause a
`BlockingIOError`. DES3D disables HDF5 locking automatically when
writing VTKHDF output. If you encounter this error when running `2vtk.py`
externally, set `HDF5_USE_FILE_LOCKING=FALSE` in your environment.
:::
