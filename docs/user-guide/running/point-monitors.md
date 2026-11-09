---
sidebar_position: 3
slug: /tutorial/pointmonitor
title: Point monitors
---

# Point monitors

The `[monitor]` section writes a lightweight CSV time series for a handful
of fixed locations, independent of the normal field output
(`output_time_interval_in_yr` / `output_step_interval`). Use it when you
need high-time-resolution history at a few points — a fault patch's
velocity and state variable, a borehole site's temperature, a wall's
stress — without paying for a full-field snapshot every step.

## In a nutshell

```cfg
[monitor]
enabled       = yes
step_interval = 10          # write every 10 solver steps
num_points    = 2
points_x      = [50e3, 50e3]
points_z      = [-4e3, -6e3]   # 2D: second coordinate; 3D: use points_y too
points_unit   = m
output_prefix = output/monitor
output_coord     = yes
output_velocity  = yes
output_stress    = yes
```

This writes `output/monitor_point_0.csv` and `output/monitor_point_1.csv`,
one row every 10 steps, each row holding the step, time, the point's current
position, the node and element sampled, the requested fields and the row
kind (see [Remeshing and restart](#remeshing-and-restart)).

`monitor.enabled = yes` requires `num_points > 0` and at least one
`output_*` flag on; otherwise the run stops at input.

## How points are located

Each monitor point is a tracer, like a marker. It is placed at
`points_x`/`points_y`/`points_z`, keeps its position inside its element as
the mesh moves, and so follows the material through deformation, remeshing
and restart. `monitor.point_type` chooses what a row reports:

| `point_type` | Node fields (velocity, temperature, ...) | Element fields (stress, plastic strain, ...) |
| --- | --- | --- |
| `particle` (default) | interpolated at the point | from the element that contains the point |
| `grid` | from the node nearest the point | from the element whose centroid is nearest the point |

The columns `query_*` hold the point's current position, and
`matched_node`/`matched_elem` the node and element that were sampled. A point
that leaves the mesh reports NaN (particle) or its nearest node (grid), with
one warning.

- `points_x`, `points_z`: in 2D, the two in-plane coordinates.
- `points_x`, `points_y`, `points_z`: in 3D, all three.
- `points_unit`: `mm`, `cm`, `m`, or `km` — one unit for every coordinate of
  every point.

:::caution 2D legacy alias
In a 2D build, `points_y` is accepted as an alias for `points_z` *only when
`points_z` is left empty* (`[]`). This exists for old 2D configs written
before `points_y` meant the 3D y-coordinate; in a 2D config, write the
depth/vertical coordinate as `points_z`, not `points_y`, to avoid relying on
the alias.
:::

## What gets written

One file per point: `<output_prefix>_point_<i>.csv`, where `i` is the
point's 0-based index in `points_x`/`points_y`/`points_z`. Every row has:

| Column(s) | Always present | Meaning |
|---|---|---|
| `step`, `time_s` | yes | Solver step and model time (seconds) |
| `query_x`[, `query_y`], `query_z` | yes | The point's current position (metres) |
| `matched_node`, `matched_elem` | yes | The node nearest the point, and the element sampled (see [How points are located](#how-points-are-located)) |
| `row` | yes, last column | `0` regular, `1` before a remesh, `2` after a remesh (see [Remeshing and restart](#remeshing-and-restart)) |

The remaining columns appear only if their `output_*` flag is on, between
`matched_elem` and `row`. Node-based fields are interpolated at the point
(`particle`) or read from `matched_node` (`grid`); element-based fields come
from `matched_elem`.
Any field a flag requests that the run doesn't actually have (e.g. pore
pressure without poroelasticity) comes out as `nan`, like a missing or
out-of-range match (`matched_node`/`matched_elem = -1`) would.

**Node-based** (one column per field, or `NDIMS` columns for a vector):

| Flag | Column(s) | Source |
|---|---|---|
| `output_coord` | `coord_x`[`_y`]`_z` | Current node position (m) |
| `output_velocity` | `velocity_x`[`_y`]`_z` | Node velocity |
| `output_force` | `force_x`[`_y`]`_z` | Node force |
| `output_temperature` | `temperature` | |
| `output_pore_pressure` | `pore_pressure` | Poroelastic models only |
| `output_bcflag` | `bcflag` | Boundary-condition flag bitmask, as an integer |

**Element-based**, from the sampled element:

| Flag | Column(s) | Source |
|---|---|---|
| `output_stress` | `stress_0`...`stress_{NSTR-1}` | See component order below |
| `output_strain` | `strain_0`...`strain_{NSTR-1}` | |
| `output_strain_rate` | `strain_rate_0`...`strain_rate_{NSTR-1}` | |
| `output_plastic_strain` | `plastic_strain` | |
| `output_plastic_strain_rate` | `plastic_strain_rate` | |
| `output_radiogenic_source` | `radiogenic_source` | |
| `output_density` | `density` | Current effective density, not just `rho0` |
| `output_viscosity` | `viscosity` | Current effective viscosity |
| `output_mesh_quality` | `mesh_quality` | Same metric that triggers remeshing — see [Adaptive mesh refinement with MMG](./usingmmg) |
| `output_material` | `material` | Index of the material with the most markers in the element |
| `output_dynamic_friction` | `dynamic_friction` | |
| `output_state_variable` | `state_variable` | Rate-and-state friction's state variable — see [Rate-and-state friction](./rate-state-friction) |

`NSTR` is 3 in 2D and 6 in 3D, in the same component order as
[`initial_stress`](../model-setup/initial-stress.md): 2D `[xx, zz, xz]`, 3D
`[xx, yy, zz, xy, xz, yz]`.

Every numeric value is written in full double precision
(`%.17e`); `nan`/`inf`/`-inf` are spelled out literally rather than left
blank.

## Remeshing and restart

A remesh rebuilds the mesh, so each point is located again at the position
it had just before the remesh. A remesh also remaps element fields, which
smooths them slightly. To show that, the last CSV column, `row`, marks what
each row records:

| `row` | Written |
| --- | --- |
| `0` | every `step_interval` steps: the regular series |
| `1` | just before a remesh that falls between monitor steps |
| `2` | just after a remesh, with the remapped values (only with `remesh_output = both`) |

`monitor.remesh_output = before` (default) writes rows 0 and 1;
`both` also writes row 2. A remesh on a monitor step needs no row 1: the
regular row already records that state. Filter on `row == 0` for an evenly
spaced series, and compare rows 1 and 2 of one step to see how much a remesh
changed a value.

The checkpoint stores each point's position and element, so a restart
continues the same points. Restarting keeps the rows a CSV already holds up
to the restart step and continues the series in the same file.

## Notes

- **The initial state is always written once.** At `step = 0` (a fresh
  start, not a restart), every point's row is written immediately,
  regardless of `step_interval`.
- `step_interval` must be `>= 1`; `num_points` must be `>= 0`.
- Rows `1` and `2` fall between monitor steps, so a series that includes them
  is not evenly spaced in steps or time.

## Try it

[Rate-and-state friction (2D)](./rate-state-friction) is a full worked
example: it places three monitor points at known `.poly` vertices straddling
a fault band, and its companion notebook reads the resulting
`monitor_point_*.csv` files directly to compute across-band slip velocity,
displacement, and the friction state variable through a seismic cycle.
