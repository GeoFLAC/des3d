---
sidebar_position: 5
---

# Velocity and traction boundary conditions {#boundary-conditions}

DES3D's six box faces — `x0`/`x1` (west/east), `y0`/`y1` (south/north, 3D
only), `z0`/`z1` (bottom/top) — each take an independent boundary condition,
set entirely in the `[bc]` section. Three systems can act on a face, and
they compose additively rather than replacing one another:

- **Velocity (Dirichlet)**: `vbc_*` fixes components of velocity outright.
- **Traction (Neumann)**: `stress_bc_*` adds a prescribed force.
- **Automatic gravity-driven support**: applied wherever a face's normal
  direction is left free, so "free" under gravity is not the same as "zero
  force" (see [Automatic boundary support under gravity](#automatic-boundary-support-under-gravity)).

A custom (non-rectangular) mesh can also define up to four extra "slant"
boundary planes, `n0`–`n3`, covered at the end.

## Velocity boundary conditions

Each face takes a `vbc_<face>` type code and a `vbc_val_<face>` value
(m/s). The default model (`vbc_x0 = vbc_x1 = 1`, with opposite-signed
values) is a divergent box: both side walls move apart.

```cfg
[bc]
vbc_x0 = 1
vbc_val_x0 = -1e-9   # m/s
vbc_x1 = 1
vbc_val_x1 = 1e-9    # m/s
```

`vbc_x0`/`vbc_x1` (and, in 3D, `vbc_y0`/`vbc_y1`) are **lateral faces** —
their normal is horizontal, and in 3D they distinguish three independent
components: the normal direction, the in-plane lateral-shear direction, and
the vertical (z) direction. `vbc_z0`/`vbc_z1` are the **top/bottom faces**
and use a different, smaller set of codes, covered in their own table
below.

### Lateral faces (`x0`, `x1`, `y0`, `y1`)

In 2D there is no separate out-of-plane direction, so the "z" column below
doesn't apply; the single non-normal component is the "lateral-shear"
column, which in 2D is the vertical (z) direction itself.

| Type | Normal component | Lateral-shear component | z component (3D only) |
|------|-------------------|--------------------------|--------------|
| `0` | Free | Free | Free |
| `1` | Fixed (`vbc_val_*`) | Free | Free |
| `2` | Free | Fixed at 0 | Fixed at 0 |
| `3` | Fixed (`vbc_val_*`) | Fixed at 0 | Fixed at 0 |
| `4` | **2D:** normal fixed at 0, lateral-shear (=z) fixed (`vbc_val_*`). **3D:** normal free, lateral-shear fixed (`vbc_val_*`), z fixed at 0 | | |
| `5` *(3D only)* | Fixed at 0 | Fixed (`vbc_val_*`) | Fixed at 0 |
| `6` | Fixed (`vbc_val_*`) | Fixed (`vbc_val_*_l`) | Free |
| `7` *(3D only)* | Fixed (`vbc_val_*`) | Fixed at 0 | Free |

:::caution Type 4 means different things in 2D and 3D
Every other type keeps the same meaning in 2D and 3D, but `4` doesn't: in
2D it's a "tangential loading" mode (normal pinned to 0, the single
tangential/vertical component prescribed); in 3D the normal is left free
instead, and it's the lateral-shear component that gets prescribed while
`z` is pinned to 0. Don't reuse a 2D type-4 config verbatim in 3D.
:::

:::caution Types `11` and `13` don't apply here
`11` and `13` exist only for the slant boundaries (`vbc_n0`–`vbc_n3`,
below) and are silently ignored — the face stays fully free — if set on
`vbc_x0`, `vbc_x1`, `vbc_y0`, or `vbc_y1`. Unlike `vbc_n0`–`vbc_n3`, these
six parameters aren't validated at startup, so a typo here doesn't stop
the run; check that the boundary actually moved as intended.
:::

:::caution Sign convention: literal axis direction, not inward/outward
Unlike the slant-boundary values below, `vbc_val_x0`, `vbc_val_x1`, etc. are
the literal signed velocity along the global axis — not relative to
inward/outward. A positive `vbc_val_x1` moves the east wall further east
(outward, extension); a positive `vbc_val_x0` moves the west wall further
*east* too, i.e. **inward** (convergence), since `x0` is already at the
low-x end. The divergent-box default above uses a negative value on `x0`
and a positive one on `x1` precisely because both push outward.
:::

### Top and bottom faces (`z0`, `z1`)

`vbc_z0`/`vbc_z1` use their own, smaller set of codes — not the lateral
table above:

| Type | Horizontal component(s) | Normal (z) component |
|------|--------------------------|------------------------|
| `0` | Free | Free |
| `1` | Free | Fixed (`vbc_val_*`) |
| `2` | Fixed at 0 | Free |
| `3` | Fixed at 0 | Fixed (`vbc_val_*`) |
| `4` | Fixed (`vbc_val_*`) | Fixed at 0 |

In 3D, type `4` fixes *both* horizontal components (x and y) to the same
scalar `vbc_val_*`, so it's only meaningful for a uniformly-sliding lid, not
independent x/y rates.

:::caution `vbc_z0 = 4` is 2D only
Unlike `vbc_z1`, `vbc_z0`'s type `4` only exists in the 2D build; a 3D
build silently ignores it (the face stays free), the same trap as types
`11`/`13` above.
:::

### Case 6: independent normal and lateral-shear velocity

Type `6` is the only one that lets you set both the normal and
lateral-shear velocity to independent non-zero values, useful for
transtensional/transpressional setups. See
[Velocity boundary conditions (3D)](../tutorial/vbc) for a worked example
with `examples/oblique-rift-3d.cfg`.

### Time-varying velocity (2D only)

`x0`/`x1` can ramp through a sequence of rate multipliers over time:

```cfg
[bc]
num_vbc_period_x0 = 2
vbc_period_x0_time_in_yr = [1e6, 2e6]   # end time of each period
vbc_period_x0_ratio = [1., 0.5]         # vbc_val_x0 multiplier during each period
```

### Depth-varying velocity profile (2D only)

The normal velocity on `x0`/`x1` (types `1`, `3`, `6`) can also vary
piecewise-linearly with depth, as a fraction of `vbc_val_x0`/`vbc_val_x1`,
using two interior break points as a fraction of the boundary's height
(`0` = top, `1` = bottom):

```cfg
[bc]
vbc_val_division_x0_min = 0.3   # upper break point (fraction of height from the top)
vbc_val_division_x0_max = 0.7   # lower break point
vbc_val_x0_ratio0 = 1.0   # ratio at the top
vbc_val_x0_ratio1 = 1.0   # ratio at vbc_val_division_x0_min
vbc_val_x0_ratio2 = 0.5   # ratio at vbc_val_division_x0_max
vbc_val_x0_ratio3 = 0.5   # ratio at the bottom
```

### Other velocity controls

| Parameter | Effect |
|---|---|
| `bottom_shear_zone_thickness` | For `vbc_x0 = 3`, 2D only: ramps the x-velocity linearly to zero within this thickness (km) of the bottom, instead of a step. |
| `vbc_val_z1_loading_period` | After this much model time, `vbc_z1` is forced to `0` (free) regardless of its configured type — useful for a loading phase followed by free relaxation. |

## Traction (Neumann / stress) boundary conditions

Each face also takes a `stress_bc_<face>` type and `stress_val_<face>`
magnitude (Pa):

```cfg
[bc]
stress_bc_x1 = 1       # traction in the x direction
stress_val_x1 = -1e8   # Pa; negative = compression (pushes inward)
```

| Type | Meaning |
|---|---|
| `0` (default) | No traction boundary condition |
| `1` | Traction in the x direction |
| `2` *(3D only)* | Traction in the y direction |
| `3` | Traction in the z direction |

:::caution Match the type to the face's own normal direction
The traction is resolved onto the facet through its outward normal, so it
only has an effect when the type matches the face's own normal axis:
type `1` on `x0`/`x1`, type `2` on `y0`/`y1`, type `3` on `z0`/`z1`. Any
other combination computes a force along a direction the face has no
normal component in, and silently applies zero force.
:::

With the type matched to the face, the sign is consistent with ordinary
stress convention: a **positive** value is tension (pulls the boundary
outward), a **negative** value is compression (pushes it inward) — on
both the "low" (`x0`/`y0`/`z0`) and "high" (`x1`/`y1`/`z1`) side of each
axis, since the outward normal itself flips sign between them.

A traction BC only matters where the corresponding `vbc_*` leaves that
face's normal component free (type `0` or `2`); if the normal is
Dirichlet-fixed, the velocity solve overwrites it regardless of any force
applied there.

## Automatic boundary support under gravity

With gravity on (`control.gravity != 0`), the **lateral** faces (`x0`,
`x1`, `y0`, `y1`) automatically receive a lithostatic ("Archimedes")
support pressure from the exterior column — via `control.ref_pressure_option`
— whenever their normal is free; otherwise a merely "free" sidewall would
let material flow out under its own weight with nothing pushing back.

`z0` and `z1` work differently: each gets support only if its own flag is
on, and **nothing at all** — not even the lithostatic default — if that
flag is off and the face is otherwise free.

| Face | Support | Controlled by |
|---|---|---|
| `z0` (bottom) | Winkler foundation: hydrostatic pressure from a virtual fluid of the local material's density (+ `winkler_delta_rho`) below the model | `has_winkler_foundation` (default **on**), `winkler_delta_rho` (kg/m³) |
| `z1` (top) | Hydrostatic water load on any part of the surface below `control.surf_base_level` | `has_water_loading` (default **on**), `sea_water_density` (kg/m³, default 1030) |

:::caution Winkler and water loading override `vbc_z0`/`vbc_z1`
If `has_winkler_foundation` is on, `vbc_z0` is forced to `0` (with a
warning) regardless of what you set — the foundation needs the bottom
free to supply its own support. The same happens to `vbc_z1` when
`has_water_loading` is on. Turn the relevant flag off first if you need a
Dirichlet velocity BC on that face instead — and if you do, remember `z0`/`z1`
then has no automatic support at all, unlike the lateral faces.
:::

An alternative (or additional) bottom support is a simple elastic
foundation — a restoring force proportional to each bottom node's total
vertical displacement from its initial position:

```cfg
[bc]
has_elastic_foundation = yes
elastic_foundation_constant = 1e11   # default
```

It is off by default and, unlike Winkler/water loading, does not force
`vbc_z0` to free — the two can be combined with an explicit Dirichlet
condition if you choose to.

See [Solution scheme in DES3D](../theory/theory#equation-of-motion) for the
Neumann boundary force derivation these all feed into.

## Slant boundaries (custom meshes)

A mesh with non-rectangular boundaries (e.g. imported `.poly`/`.exo`
geometry) can define up to four additional planar boundaries, `n0`–`n3`,
each independently of the box faces above:

```cfg
[bc]
vbc_n0 = 1          # only 1, 3, 11, 13 are supported
vbc_val_n0 = -1e-9   # m/s, outward normal direction is positive
```

Only types `1`, `3`, `11`, and `13` are supported (anything else is
rejected at startup, unlike the axis-aligned faces above):

| Type | Normal component | Tangential component |
|---|---|---|
| `1` | Fixed (`vbc_val_n*`) | Free |
| `3` | Fixed (`vbc_val_n*`) | Fixed at 0 |
| `11` *(3D only)* | Fixed, horizontal part of the normal only (`vbc_val_n*`) | Free (including z) |
| `13` *(3D only)* | Fixed, horizontal part of the normal only (`vbc_val_n*`) | Fixed at 0 (including z) |

Unlike the axis-aligned faces above, **the sign here is relative to the
outward normal**: a positive value always points out of the domain.
