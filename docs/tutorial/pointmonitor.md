---
sidebar_position: 3.5
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
one row every 10 steps, each row holding the step, time, the matched
node/element id, and the requested fields.

`monitor.enabled = yes` requires `num_points > 0` and at least one
`output_*` flag on; otherwise the run stops at input.

## How points are located

Each query point is matched **independently** to the nearest mesh *node*
(for node-based fields) and the nearest *element centroid* (for
element-based fields) — a plain nearest-neighbor search, not interpolation.
The matched ids are written every row as `matched_node`/`matched_elem`, so
you can tell which mesh entity actually produced each row, and they can
differ from each other since the search is independent.

Because there's no interpolation, a query point that doesn't sit exactly on
a node gets the *nearest* node's values, not an interpolated value at the
exact point. If you need an exact match, place `points_x`/`points_y`/`points_z`
at a known mesh vertex — e.g., a `.poly` file vertex — and compare the
`query_*` columns against `coord_*` (with `output_coord = yes`) to confirm
how close the match actually is.

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

Matching runs once at startup and again after every remesh — not every
write — so it's cheap even with many points on a large mesh.

## What gets written

One file per point: `<output_prefix>_point_<i>.csv`, where `i` is the
point's 0-based index in `points_x`/`points_y`/`points_z`. Every row has:

| Column(s) | Always present | Meaning |
|---|---|---|
| `step`, `time_s` | yes | Solver step and model time (seconds) |
| `query_x`[, `query_y`], `query_z` | yes | The coordinate (metres) actually used for this row's search — the original point, or its rebind coordinate after a remesh (see below) |
| `matched_node`, `matched_elem` | yes | The node/element id the row's fields came from |

The remaining columns appear only if their `output_*` flag is on. Node-based
fields read from `matched_node`; element-based fields from `matched_elem`.
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

**Element-based**, using the matched element's centroid:

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
[`initial_stress`](../usage/run#initial-stress): 2D `[xx, zz, xz]`, 3D
`[xx, yy, zz, xy, xz, yz]`.

Every numeric value is written in full double precision
(`%.17e`); `nan`/`inf`/`-inf` are spelled out literally rather than left
blank.

## Rebinding across a remesh

A remesh renumbers nodes and elements, so a monitor point's `matched_node`/
`matched_elem` from before the remesh is meaningless afterward. The monitor
re-runs its nearest-neighbor search right after every remesh, and
`remesh_rebind_mode` controls what coordinate it searches *from*:

- **`pre_remesh_coord`** (default): just before the remesh, the monitor
  records the current physical position of its *previously* matched node
  (or element centroid), and searches from there afterward. The point keeps
  following the same material location as the model deforms — a Lagrangian
  marker that gets re-anchored to the nearest mesh entity at every remesh.
- **`initial_coord`**: always searches from the original `points_x`/`y`/`z`
  value you configured, ignoring how far the model has deformed since. A
  large amount of accumulated deformation can make the matched node/element
  jump across the domain at a remesh, back to whatever is now nearest the
  original fixed coordinate — effectively a fixed-in-space (Eulerian) query
  point, re-sampled at each remesh.

Between remeshes, the match never changes — the monitor always follows
whichever node/element it last matched, step after step, regardless of this
setting. `remesh_rebind_mode` only decides where it looks right after a
remesh.

## Known limitations

:::danger Restarting overwrites existing monitor CSVs
Each monitor file is opened in overwrite mode at startup, including on a
restart (`-r`). If you restart a run with the same `output_prefix`, the
CSVs from before the restart are truncated, not appended to, and the
restarted run's rows start from wherever it resumes — leaving a gap. Copy
or rename the existing `*_point_*.csv` files before restarting a monitored
run, or give the restart leg its own `output_prefix` and concatenate the
files afterward.
:::

- **No interpolation.** See [How points are located](#how-points-are-located)
  above; a query point snaps to the nearest node/element, not a weighted
  blend of its neighbors.
- **The initial state is always written once.** At `step = 0` (a fresh
  start, not a restart), every point's row is written immediately,
  regardless of `step_interval`.
- `step_interval` must be `>= 1`; `num_points` must be `>= 0`.

## Try it

[Rate-and-state friction (2D)](./rate-state-friction) is a full worked
example: it places three monitor points at known `.poly` vertices straddling
a fault band, and its companion notebook reads the resulting
`monitor_point_*.csv` files directly to compute across-band slip velocity,
displacement, and the friction state variable through a seismic cycle.
