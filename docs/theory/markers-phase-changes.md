---
sidebar_position: 6.5
slug: /theory/markers-phase-changes
title: Markers and phase changes
description: How Lagrangian markers carry material identity through deformation and remeshing, how they set element properties, and the pressure–temperature rules that turn one material into another.
---

# Markers and phase changes

The mesh moves with the material, but it is rebuilt when it distorts, and
an element then no longer holds one rock. DES therefore tracks material
identity with markers: points that move with the deformation, each carrying
a material index. An element's properties are the marker-weighted means
described in [Rheology](./rheology.md#several-materials-in-one-element).

## Markers

Each marker stores the element that contains it and its barycentric
coordinates there, so it moves exactly with the element and needs no
search while the mesh only deforms. After remeshing, every marker is
located in the new mesh.

**Initial markers.** `markers.init_marker_option = 1` scatters
`markers.markers_per_element` markers randomly in each element (seeded by
`markers.random_seed`); `2` places them on a regular grid with spacing
`markers.init_marker_spacing`, in units of `mesh.resolution`. Their
material comes from `mat.mattype_option`: `0` takes the region of a
`.poly` mesh, `1` assigns horizontal layers at `mat.mattype_layer_depths`
(in units of `mesh.zlength`), and `101` calls a custom routine in the
source.

**Replenishment.** Remeshing and stretching can leave an element with few
markers. When it holds fewer than `markers.min_num_markers_in_element`, a
marker is added. Its material follows `markers.replenishment_option`: `0`
material 0, `1` drawn from the materials of the element and its neighbours
in proportion, `2` the material of the nearest marker; the
[parameter reference](../reference/parameters.md) lists the other options.

## Phase changes

A phase change converts a marker from one material to another when its
pressure and temperature cross a reaction boundary; the element properties
then follow the new marker counts. `mat.phase_change_option` selects the
rules:

| Option | Rules |
| --- | --- |
| 0 | none (default) |
| 1 | a fixed set of subduction rules on fixed material indices 0–7 |
| 3 | the subduction rule engine: rules switched on one by one, materials named by parameters |
| 101 | a custom routine in `phasechanges.cxx` |

Phase changes need at least two materials.

### Option 3: the subduction rule engine

Each rule converts the material named by one `mat.mattype_*` parameter into
another when its predicate holds. Depth $d$ is measured below the current
local free surface; temperature $T$ is in °C below. The pressure $P$
(compression positive) is the mean stress of the marker's element with
`mat.phase_change_pressure_option = 0`, so tectonic over- and
underpressure move the boundaries, or the lithostatic reference pressure at
that depth with `1`.

| Switch | Conversion | Boundary |
| --- | --- | --- |
| `mat.has_eclogitization` (on) | oceanic crust → eclogite | $T \ge 400$, $d \ge 20$ km, $P \ge -0.3 + 0.0022\,T$ GPa and $P \ge 20.1 - 0.0375\,T$ GPa (Hacker et al., 2003) |
| `mat.has_serpentinization` (on) | mantle above wet slab crust → serpentinite | inside the antigorite stability field (Ulmer & Trommsdorff, 1995) and within `mat.serpentinization_thickness` above oceanic crust or sediment, no deeper than `mat.serpentinization_max_depth` |
| `mat.has_serpentinization` (on) | serpentinite → mantle | $T \ge 550$ and outside the antigorite field |
| `mat.has_hydrous_mantle_dehydration` (off) | hydrous (chlorite-bearing) mantle → mantle | $T \ge 880 - 3.5\times10^{-8}\,(d - 62\ \text{km})^2$, $d$ in m (Grove et al., 2009) |
| `mat.has_sediment_metamorphism` (off) | sediment → sedimentary rock | $T \ge 80$ and $d \ge 2$ km |
| | sedimentary rock → metasediment | $T \ge 250$ or $d \ge 7$ km |
| | metasediment → schist | $P \ge 0.88 - 0.176\,(710.8 - T)/48.5$ GPa, a metapelite dehydration boundary (Wei et al., 2004) |

The antigorite field is the wedge between the lines through (730 °C,
2.1 GPa)–(500 °C, 7.5 GPa) and (730 °C, 2.1 GPa)–(650 °C, 0.2 GPa). Using
one field for both serpentinite rules means no pressure and temperature
satisfy both, so a marker cannot flip back and forth.

**Where the mantle serpentinizes.** Water released by the slab hydrates
the mantle above it. DES finds the slab with a background grid of cells of
size `mesh.vt_size` (in units of `mesh.resolution`): a cell is wet crust when
more than `mat.wet_crust_fraction_threshold` of its markers are oceanic
crust, sediment or sedimentary rock. A mantle marker serpentinizes when such
a cell lies below it within `mat.serpentinization_thickness`, optionally
only if the marker is also horizontally within the wet crust's extent plus
`mat.serpentinization_wet_crust_margin`.

Each active rule needs its source and target materials set
(`mat.mattype_oceanic_crust`, `mat.mattype_eclogite`,
`mat.mattype_serpentinite`, `mat.mattype_mantle`,
`mat.mattype_hydrous_mantle`, `mat.mattype_sediment`,
`mat.mattype_sediment_rock`, `mat.mattype_metasediment`,
`mat.mattype_schist`); DES stops at start-up if one is missing, out of
range or equal to its target. The rules and boundaries follow those of
GeoFLAC. The [subduction tutorial](../tutorial/tectonics/rifting-subduction.md)
uses this option.

### Option 1: simple subduction rules

Option 1 uses fixed material indices: 0 mantle, 1 serpentinized mantle,
2 oceanic crust, 3 eclogite, 4 sediment, 5 schist, 6 and 7 upper and lower
continental crust, and the pressure is always the lithostatic reference
pressure. Oceanic crust becomes eclogite above 500 °C and
$P > -0.3 + 0.0022\,T_K$ GPa, with $T_K$ in kelvin; sediment becomes schist above 650 °C deeper
than 20 km; serpentinite returns to mantle above 550 °C past the
(730 °C, 2.1 GPa)–(500 °C, 7.5 GPa) line. With
`control.has_hydration_processes = yes`, crust and sediment hotter than
150 °C release water as separate hydrous markers, which rise at
`control.hydration_migration_speed`; mantle below 550 °C that holds a hydrous
marker becomes serpentinite.

## References

Grove, T. L., Till, C. B., Lev, E., Chatterjee, N., & Médard, E. (2009).
Kinematic variables and water transport control the formation and location
of arc volcanoes. *Nature*, 459, 694–697.

Hacker, B. R., Abers, G. A., & Peacock, S. M. (2003). Subduction factory
1. Theoretical mineralogy, densities, seismic wave speeds, and H₂O
contents. *Journal of Geophysical Research*, 108(B1), 2029.

Ulmer, P., & Trommsdorff, V. (1995). Serpentine stability to mantle depths
and subduction-related magmatism. *Science*, 268, 858–861.

Wei, C., Powell, R., & Clarke, G. L. (2004). Calculated phase equilibria
for low- and medium-pressure metapelites in the KFMASH and KMnFMASH
systems. *Journal of Metamorphic Geology*, 22, 495–508.
