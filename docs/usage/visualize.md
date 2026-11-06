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

Choose saved fields with the `[sim]` output settings in
`examples/defaults.cfg`, such as `has_marker_output` and
`is_outputting_averaged_fields`.

### PT force output

Accepted [PT solves](./pt.md) can save an optional nodal vector,
`PT residual force`. The Python reader and `2vtk.py` support this field.

| Field | Meaning |
|---|---|
| `force` | Legacy force, including artificial damping and constrained reactions. |
| `PT residual force` | Accepted undamped force projected onto admissible velocity perturbations. |

The PT vector's free-rank RMS is the reported residual, in N/m in 2D or N
in 3D. It describes the accepted solve on its reference geometry, **before**
hydraulic transport, mesh motion and stress rotation. For physical steps
with thermal diffusion enabled, temperature has already been advanced;
the report's `stage=before_physical_updates` does not precede that thermal
stage. This diagnostic time level is retained even when other output fields
are averaged. Force reassembled
from saved post-rotation stress can therefore differ from this diagnostic.

The vector is absent before any accepted solve, after remeshing until a
new solve is accepted, and at failed solves. New saves preserve it across
restart; older saves remain readable and acquire it after the next accepted
solve. It adds no checkpoint requirement. During binary-to-VTU conversion,
`2vtk.py` reports once if selected frames lack it and preserves the field
where available. An initial-frame notice can be expected in the
[elastic tutorial](../tutorial/pt-elastic.md).

### Restarted models

`2vtk.py` follows a restarted model's `.manifest` back to its parent, so the
whole series converts as one:

```console
2vtk.py modelname-r
```

Without `-g`, frames from the parent that were already converted are linked
in under the restarted name (`modelname-r.000000.vtu -> modelname.000000.vtu`,
and so on); any parent frame with no `.vtu` yet prints a warning naming it,
instead of being silently skipped. `2vtk.py -g modelname-r` converts the
parent's frames first, so the series runs from frame 0.

Each frame also carries its own origin — which model and machine wrote it,
and, on a restart, what it restarted from — as described in
[Provenance](./run.md#provenance).

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

Combined with `-g` on a restarted model, `2vtk.py -u -g modelname-r.vtkhdf`
writes a `.vtkhdf.series` file in place alongside it, one entry per frame
across the whole restart chain, so ParaView opens the run as a single series
instead of one file per restart leg.

**Requirements:** `h5py` must be installed (`pip install h5py` or
`conda install h5py`).

**Safety:** The update is performed in-place. Back up your file before
running if it is large or irreplaceable. The script prints a warning and
exits if the target file does not look like a valid VTKHDF file.

:::caution HDF5 file locking
On some parallel or network filesystems, HDF5 file locking can cause a
`BlockingIOError`. DES3D disables HDF5 locking automatically when
writing VTKHDF output, so ParaView can open a frame while a run is still
writing it. If you encounter this error when running `2vtk.py`
externally, set `HDF5_USE_FILE_LOCKING=FALSE` in your environment.

The trade-off: with locking off, two runs that share a `modelname` are no
longer refused, and will corrupt each other's file. Give every run its own
`modelname`.
:::
