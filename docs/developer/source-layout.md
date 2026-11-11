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
| Pore fluid and sources | `hydraulics.cxx/.hpp` (pressure, Darcy flux, inventories and hydraulic remap), `unsaturated.hpp` (retention and local state conversion), `point_sources.cxx/.hpp` (shared fluid/heat point mapper) |
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

The mechanical update, transport ordering and next-step mass must refer to
the same physical interval:

1. Refresh current material properties. In the default content model,
   advance temperature when transport is enabled.
2. Evaluate strain rate and its nodal mixed projection. Coupled ordinary
   explicit/GVS mechanics advances default-model pressure before stress,
   force and velocity. PT instead trials the physical constitutive interval
   to equilibrium and accepts one mechanical state.
3. Commit accepted shear work once. In the default fixed-stress path,
   advance pressure from accepted mechanics and then update porosity.
4. Apply phase changes on their ten-step cadence. Apply velocity
   constraints and update moving geometry or fixed-mesh GVS masses.
5. The optional finite-density path advances its inventories through
   `HydraulicStep`. Its explicit/GVS correction uses the current pressure
   for one accepted momentum update, restoring the original interval/mass
   after any geometry predictor. Only then select the next GVS interval.
6. Rotate stress with the saved current physical interval, update monitors,
   track events and write outputs. Check mesh quality and remesh when needed.

See [Poromechanics](../theory/poromechanics.md#coupling-in-time) for capacity
selection and [PT](../theory/solution-scheme/pt.md) for trial/commit ownership.
Transport substeps do not repeat plastic, porosity or RSF histories.

## Increment and energy ownership

`dppressure` stores $p_{\rm old}-p_{\rm new}$, integrated over the physical
interval. Each element applies its own Biot coefficient and retention law.
Its Bishop increment uses $S_e(p_{\rm old})p_{\rm old}-S_e(p_{\rm new})p_{\rm new}$;
saturated elements retain the saturated arithmetic. Hydraulic scratch
increments and the next rheology call can belong to different time levels,
so sharing an element calculation does not permit reusing a scratch value
without checking its ownership. Checkpoints record whether the pressure
increment was consumed; a pressure correction must not repeat the plastic
return or consume that increment twice.

PT trials restore the same constitutive baseline until acceptance. Only the
accepted caller transfers nonelastic work to pending heat. This reservoir
is extensive energy: changing the next timestep changes its conversion to
a rate, rather than the stored energy. Checkpoints and remapping retain it
separately from temperature. Physical water supplies fluid heat capacity;
the numerical fixed-stress buffer supplies neither density nor sensible
heat. See [thermal evolution](../theory/thermalevolution.md) and
[poromechanics](../theory/poromechanics.md) for the declared energy models.

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
