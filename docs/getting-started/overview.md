---
sidebar_position: 1
slug: /intro
title: Overview
---

# DynEarthSol

**DynEarthSol** (Dynamic Earth Solver, also called DES or DES3D) is an
explicit Lagrangian finite element code for deforming rock in 2D and 3D. It
solves the momentum balance and heat transfer for elastic, viscoelastic and
elasto-visco-plastic materials on unstructured triangular and tetrahedral
meshes, which it rebuilds as they distort. It was built for long-term
deformation of the lithosphere, and now also covers earthquake cycles,
quasi-static equilibrium and coupled surface processes. The same source
builds `dynearthsol2d` and `dynearthsol3d`, for CPUs with OpenMP or GPUs
with OpenACC.

## What DynEarthSol can model

| Problem | Main ingredients | Start here |
| --- | --- | --- |
| Rifting, subduction and core complexes | Strain-weakening plasticity, weak zones, remeshing, markers, phase changes | [Rifting and subduction](../tutorial/tectonics/rifting-subduction.md) |
| Convergent wedges | Basal décollement friction, `.poly` geometry | [Convergent wedges](../tutorial/tectonics/accretionary-wedge.md) |
| Earthquake cycles and slow slip | Rate-and-state friction, global velocity scaling | [Rate-and-state friction](../theory/rate-state-friction.md), [Creep or earthquakes](../tutorial/tectonics/rsf/earthquake-cycles.md) |
| Static and slowly loaded equilibrium | Pseudo-transient (PT) mechanics | [Choosing a mechanical solver](../user-guide/numerical-controls/solver.md), [Elastic loading](../tutorial/fundamentals/elastic.md) |
| Landscape and tectonics together | Coupling with GoSPL | [Coupling with GoSPL](../tutorial/advanced/couplinggospl.md) |
| Thermal evolution | Heat conduction in the deforming (Lagrangian) mesh | [Thermal evolution](../theory/thermalevolution.md) |
| Strongly distorting domains | Adaptive remeshing with Triangle, TetGen or MMG | [Remeshing](../theory/remeshing.md), [MMG](../user-guide/numerical-controls/mmg.md) |

## How it works, in brief

- **Explicit time integration.** Nodal velocities are advanced from the
  force balance, with no global matrix to solve.
- **Mass scaling.** Inertia is scaled so that a stable explicit step spans
  years in tectonic models; global velocity scaling adapts it from loading
  to rupture.
- **Nodal mixed discretization** avoids volumetric locking of linear
  elements.
- **Lagrangian mesh with remeshing.** The mesh moves with the material and
  is rebuilt when its quality drops; markers carry material identity.
- **Pseudo-transient mechanics** (optional) iterates to equilibrium within
  each physical step.

See [Theory](/docs/category/theory) for the formulation.

## Where to start

| If you want to | Read |
| --- | --- |
| Install and run a first model | [Installation](./installation.md) → [Running DynEarthSol](./run.md) → [Visualizing outputs](./visualize.md) |
| Set up your own model | [User guide](/docs/category/user-guide) and the [configuration file](../reference/configuration.md) |
| Learn by example | [Tutorials](/docs/category/tutorial) |
| Model earthquake cycles | [Rate-and-state theory](../theory/rate-state-friction.md) → [Simple-shear check](../tutorial/tectonics/rsf/simple-shear.md) → [Creep or earthquakes](../tutorial/tectonics/rsf/earthquake-cycles.md) |
| Solve for equilibrium | [Choosing a mechanical solver](../user-guide/numerical-controls/solver.md) → [Fundamental mechanics](/docs/category/fundamental-mechanics) |

## Versions

This manual follows the current DynEarthSol source ("Latest"). Manuals for
tagged releases are in the version menu at the top right. Use the one that
matches your executable: parameters and file formats change between
releases.

## How to cite

Please cite the DES3D v2.0 paper (preprint):

> Shyu, C. J., Lee, S., Ding, X., Keum, J., Tan, E., Lavier, L. L., & Choi, E. (2026). DynEarthSol v2.0: An efficient explicit Lagrangian solver for geodynamics, surface processes, and earthquake-cycle dynamics. *EGUsphere* [preprint, in review for *Solid Earth*]. DOI:[10.5194/egusphere-2026-2922](https://doi.org/10.5194/egusphere-2026-2922)

and the original method paper:

> Choi, E., Tan, E., Lavier, L. L., & Calo, V. M. (2013). DynEarthSol2D: An efficient unstructured finite element method to study long-term tectonic deformation. *Journal of Geophysical Research: Solid Earth*, 118(5), 2429–2444. DOI:[10.1002/jgrb.50148](https://doi.org/10.1002/jgrb.50148)

To cite the software itself, use DOI:[10.5281/zenodo.20293557](https://doi.org/10.5281/zenodo.20293557).
This DOI covers every archived release, both the software (`v2.x.x`) and the
benchmark datasets (`benchmarks-v2.x.x`), and it opens the list of all
versions. To cite the exact version you used, pick the matching software
release from that list, or take its DOI from the
[releases page](https://github.com/GeoFLAC/DynEarthSol/releases) or from the
`CITATION.cff` file shipped with that release.

## Getting help

Report problems and ask questions in the
[DynEarthSol issue tracker](https://github.com/GeoFLAC/DynEarthSol/issues).

:::tip Using an AI assistant to get oriented
If you're new to DES3D, one effective way to get started is working through
model setup with an AI coding assistant. Point it at this documentation site
and any background papers relevant to your problem, then describe the
tectonic scenario you want to model in plain language, geometry, timing,
boundary conditions, the processes involved, and iterate on the resulting
`.cfg` file together. Treat its output as a draft to check against this
manual and your own understanding of the parameters, not a substitute for
either.
:::
