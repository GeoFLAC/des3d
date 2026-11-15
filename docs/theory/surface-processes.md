---
sidebar_position: 6.7
slug: /theory/surface-processes
title: Surface processes
description: How DES changes its top surface by erosion and deposition, from hillslope diffusion to terrigenous, hemipelagic and pelagic sedimentation, and how deposited material becomes sediment markers.
---

# Surface processes

Tectonics builds relief, and erosion and sedimentation reshape it, which in
turn changes the loads that drive deformation. DES moves the nodes of its
top surface by a height change $\Delta h$ each step and records the new
material with markers. `control.surface_process_option` selects how
$\Delta h$ is computed:

| Option | Surface process | Dimensions |
| --- | --- | --- |
| 0 | none (default) | 2D, 3D |
| 1 | diffusion of topography | 2D, 3D |
| 11 | coupling to the landscape evolution model GoSPL (build with `usegospl=1`) | 3D |
| 101 | a custom routine in the source | 2D, 3D |
| 102 | diffusion with terrigenous, hemipelagic and pelagic deposition | 2D |

## Diffusion of topography

Option 1 treats hillslope transport as diffusion of the surface height
$h$,

$$
\frac{\partial h}{\partial t} = \kappa_s \nabla^2 h ,
$$

with the diffusivity $\kappa_s$ = `control.surface_diffusivity` (m²/s). It
is applied explicitly on the top nodes, using the slopes of the adjacent
surface facets; the ends of the surface reflect, so no material leaves
through the sides. In 2D the base level `control.surf_base_level` divides
land from sea: erosion above it is scaled by
`control.surf_diff_ratio_terrig` and deposition below it by
`control.surf_diff_ratio_marine`.

## Marine deposition (2D)

Option 102 adds three sources of sediment to the diffusion.

**Terrigenous.** Sediment arrives from both ends of the profile at the
cross-sectional rate `control.terrig_sediment_area` (m²/s) and fills the
basins below base level. Within a basin it spreads by diffusion whose
coefficient decays with water depth $d$,

$$
\kappa(d) = C_0\,e^{-C_1 d},
$$

with $C_0$ = `control.terrig_sediment_diffusivity` and $C_1$ =
`control.terrig_depth_coefficient`, so it settles mostly near the shore. A
basin that fills passes the rest of the supply on.

**Hemipelagic and pelagic.** Below base level, sediment settles from
suspension at

$$
\frac{dh}{dt} = r_h \exp\!\left[-\left(\frac{d - d_h}{w_h}\right)^2\right]
+ r_p\left[1 - \exp\!\left(-\frac{d^2}{w_p^2}\right)\right],
$$

a hemipelagic band centred at depth $d_h$ = `control.hemipelagic_max_depth`
with width $w_h$ = `control.hemipelagic_width` and rate $r_h$ =
`control.hemipelagic_sedimentation_rate`, and a pelagic rain $r_p$ =
`control.pelagic_sedimentation_rate` that reaches its full rate over the
depth $w_p$ = `control.pelagic_increasing_width`.

## Sediment markers

Moving the surface changes the volume of the top elements. At every mesh
quality check (`mesh.quality_check_step_interval`), the markers of the
top elements are relocated for the accumulated surface change, and
elements that gained volume receive new markers of material
`mat.mattype_sediment`, stamped with their deposition time. The
sediment can then be followed through burial and, with
`mat.phase_change_option = 3`, compaction and metamorphism; see
[Markers and phase changes](./markers-phase-changes.md).
`mesh.meshing_sediment = yes` refines the mesh in sediment during
remeshing.

## Water load

With `bc.has_water_loading = yes`, parts of the top surface below
`control.surf_base_level` carry the weight of sea water of density
`bc.sea_water_density`, so the base level is also the sea level.

## Coupling to GoSPL

Option 11 hands the surface to GoSPL, a landscape evolution model with
river incision, hillslope processes and deposition. Every coupling
interval DES sends the velocity of its top surface; GoSPL evolves its own
surface and returns the height change. The setup, build and parameters are
in the [GoSPL tutorial](../tutorial/advanced/couplinggospl.md).

## Parameters

| Parameter | Meaning | Default |
| --- | --- | --- |
| `control.surface_process_option` | see the table above | 0 |
| `control.surface_diffusivity` | $\kappa_s$ (m²/s) | 1e-6 |
| `control.surf_base_level` | base level and sea level (m) | 0 |
| `control.surf_diff_ratio_terrig`, `control.surf_diff_ratio_marine` | diffusivity ratios on land and under water | 1, 1 |
| `control.terrig_sediment_area` | terrigenous supply per unit width (m²/s) | 3.17e-7 |
| `control.terrig_sediment_diffusivity`, `control.terrig_depth_coefficient` | $C_0$ (m²/s), $C_1$ (1/m) | 3.17e-6, 5e-4 |
| `control.hemipelagic_sedimentation_rate`, `control.hemipelagic_max_depth`, `control.hemipelagic_width` | $r_h$ (m/s), $d_h$, $w_h$ (m) | 3.17e-11, 40, 90 |
| `control.pelagic_sedimentation_rate`, `control.pelagic_increasing_width` | $r_p$ (m/s), $w_p$ (m) | 1.585e-12, 30 |
| `mat.mattype_sediment` | material of deposited sediment | 0 |
| `mesh.meshing_sediment` | refine sediment during remeshing | no |
