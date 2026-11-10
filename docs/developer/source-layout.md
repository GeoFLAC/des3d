---
sidebar_position: 1
slug: /developer/source-layout
title: Source code layout
description: Where each part of DynEarthSol lives and the order of work in one time step.
---

# Source code layout

DynEarthSol is a single C++17 code base in the repository root. The same
sources build `dynearthsol2d` and `dynearthsol3d`: the dimension is fixed at
compile time (`make ndims=2` or `ndims=3`) through `NDIMS`, `NODES_PER_ELEM`
and `NSTR`, so every change must compile in both.

## Files

| Area | Files |
| --- | --- |
| Main program and time loop | `dynearthsol.cxx` |
| Input parameters | `input.cxx` (declaration, reading, validation), `parameters.hpp` (the `Param` structs and shared variables) |
| Mesh generation and remeshing | `mesh.cxx`, `remeshing.cxx`, `mmg_utils.cxx`, with the bundled Triangle and TetGen |
| Field updates | `fields.cxx` (strain rate, force, velocity, temperature), `geometry.cxx` (volumes, time step, nodal masses) |
| Constitutive models | `rheology.cxx` (stress update), `matprops.cxx` (material properties, friction laws) |
| Pseudo-transient mechanics | `pseudo_transient.cxx` |
| Boundary and initial conditions | `bc.cxx`, `ic.cxx`, `ic-read-temp.cxx` |
| Markers and phase changes | `markerset.cxx`, `phasechanges.cxx` |
| Interpolation during remeshing | `nn-interpolation.cxx`, `brc-interpolation.cxx`, `barycentric-fn.cxx`, `knn.cxx` |
| Output, checkpoints and monitors | `output.cxx`, `binaryio.cxx`, `monitor.cxx`, `ats_output_scheduler.cxx`, `runtime_info.cxx` |
| Earthquake tracking | `earthquake_state.cxx` |
| Shared helpers | `utils.hpp`, `utils.cxx` (including `die()` and the exit codes), `constants.hpp` |
| Python tools | `Dynearthsol.py` (output reader), `2vtk.py` (VTK conversion) |
| Bundled libraries | `nanoflann`, `knn-bvh`, `mmg` (git submodules), `third_party/CLI11`, `triangle`, `tetgen` |

## One time step

With explicit mechanics, each step in `dynearthsol.cxx` does, in order:

1. heat diffusion (`update_temperature`), when enabled;
2. mechanics: strain rate, stress update (`update_stress`), nodal forces
   (`update_force`) and velocities (`update_velocity`). With
   `control.has_PT`, this block is replaced by a pseudo-transient solve
   for the step;
3. pore pressure (`update_pore_pressure`), when enabled;
4. phase changes, every ten steps;
5. velocity boundary conditions and the mesh update (`update_mesh`): node
   positions, volumes, and with global velocity scaling the next time step
   (`compute_dt`) and masses (`compute_mass`);
6. stress rotation (`rotate_stress`), monitor output and slow updates;
7. event tracking for RSF models and output of frames and checkpoints;
8. the mesh quality check and, when needed, remeshing (`remesh_if_needed`).

## Conventions

The development notes in the repository's
[`CONTRIBUTING.md`](https://github.com/GeoFLAC/DynEarthSol/blob/master/CONTRIBUTING.md)
are the authority. In short:

- Parallel loops use `#pragma omp parallel for default(none)` with every
  variable listed, and keep the paired OpenACC clauses in step.
- The code must also compile as C++20 and with GCC 8 or later.
- Errors exit through `die(EXIT_...)`, never a bare `exit()`; the first digit
  of the code is the category (see
  [exit codes](../user-guide/running/diagnostics.md#exit-codes)).
- Bulk output uses C-style I/O; avoid creating objects in inner loops, and
  avoid static and global variables.
