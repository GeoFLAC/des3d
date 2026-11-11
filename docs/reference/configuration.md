---
sidebar_position: 1
slug: /reference/configuration
title: Configuration file
description: The sections of a DynEarthSol input file and where to find every parameter, its default and its meaning.
---

# Configuration file

A DynEarthSol model is described by one input file in INI format, passed to
the executable:

```console
dynearthsol2d model.cfg
```

Each parameter belongs to a section, and its full name is
`section.parameter`, for example `mat.rheology_type`. Inside the file it is
written under its section header:

```ini
[mat]
rheology_type = elasto-plastic
```

Parameters left out take their defaults. Lists are written in brackets,
`[1, 2, 3]`, with one value per material where a parameter is set per
material. A single value applies to every material.

## Sections

| Section | Controls |
| --- | --- |
| `[sim]` | Model name, run length, output and checkpoint intervals, restart |
| `[mesh]` | Domain size, mesh generation, resolution, quality checks and remeshing |
| `[markers]` | Lagrangian markers that carry material identity |
| `[control]` | Gravity, time stepping, mass scaling, damping, the PT solver, and heat and fluid transport |
| `[bc]` | Velocity, traction, thermal and hydraulic boundary conditions, surface processes |
| `[ic]` | Initial temperature, stress, weak zones and material layout |
| `[mat]` | Rheology and material properties, per material |
| `[monitor]` | Point monitors written as CSV time series |
| `[debug]` | Diagnostic output |

## Finding a parameter

The [configuration parameters](./parameters.md) page lists every parameter
with its type, default and description. It is generated from the
executables, which remain the authoritative list for their own version. Run
one with `-h` to print the same information for the build you are using:

```console
./dynearthsol2d -h
./dynearthsol2d -h | grep -A2 'rsf'
```

`examples/defaults.cfg` in the DynEarthSol repository lists the parameters
by section with their default values and short comments. The
`examples/` and `benchmarks/` directories contain complete working inputs.

The User guide and Theory pages describe the parameters that belong to each
feature:

| Feature | Page |
| --- | --- |
| Boundary conditions | [Velocity and traction](../user-guide/model-setup/boundary-conditions.md), [temperature](../user-guide/model-setup/temperature.md) |
| Initial stress | [Initial stress](../user-guide/model-setup/initial-stress.md) |
| Weak zones | [Weak zones](../user-guide/model-setup/weak-zones.md) |
| Mechanical solver | [Choosing a mechanical solver](../user-guide/numerical-controls/solver.md) |
| Remeshing | [Remeshing](../theory/remeshing.md), [MMG](../user-guide/numerical-controls/mmg.md) |
| Rate-and-state friction | [Rate-and-state friction](../theory/rate-state-friction.md#parameters) |
| Point monitors | [Point monitors](../user-guide/running/point-monitors.md) |
| Restart | [Checkpointing and restart](../user-guide/running/restart.md) |

An unknown or misspelled parameter stops the run with exit code `11`
before any computation; see [exit codes](../user-guide/running/diagnostics.md#exit-codes).
