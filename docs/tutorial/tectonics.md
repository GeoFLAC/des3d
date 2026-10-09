---
sidebar_position: 6
title: Tectonic rifting and subduction
description: Set up, run and interpret continental rifting and subduction models with DynEarthSol
---

# Tectonic rifting and subduction

This tutorial walks through two classic long-term tectonic models with
DynEarthSol: **continental rifting** driven by far-field extension, and
**subduction** of an oceanic plate beneath an overriding plate. Both use the
bundled 2D examples as a starting point, so you can run them as they are and
then modify one ingredient at a time.

{/* TODO: one-paragraph motivation — why these two cases, what they teach about
    DES (elasto-visco-plastic rheology, weak-zone localization, remeshing,
    markers). */}

## What you will learn

- How a DES `.cfg` file is organized and which sections matter for tectonics
- How the elasto-visco-plastic rheology produces faults (strain localization)
- How to seed deformation with a weak zone and drive it with velocity boundary conditions
- How to build a layered or slab-shaped initial geometry with a `.poly` file
- How to read the output: plastic strain, viscosity, temperature, topography

## Prerequisites

Before starting, ensure you have:

- ✅ DynEarthSol compiled in 2D (`make ndims=2`); see [Build](../usage/usage)
- ✅ Python 3 with `numpy` for `2vtk.py`
- ✅ [ParaView](https://www.paraview.org/) or another VTK viewer
- ✅ Read [Making a complex mesh with `.poly` file](./usingpolyfile) (needed for Part 2)

:::tip Which build?
The examples in this tutorial are 2D. A 3D build (`make`) runs the same
physics but at a much higher cost; see
[Velocity boundary conditions (3D)](./vbc) when you are ready to go 3D.
:::

{/* TODO: expected runtime on a laptop for each part, number of threads. */}

## How the model works

{/* TODO: short physics background, one subsection per ingredient. Keep the
    math minimal and link to docs/theory/ pages where they exist. */}

### Rheology

DynEarthSol's `elasto-visco-plastic` rheology combines three responses in
every element:

| Component | Controls | Key parameters |
|-----------|----------|----------------|
| Elastic | Short-term stress build-up | `bulk_modulus`, `shear_modulus` |
| Viscous (power-law creep) | Ductile flow in the hot lower crust and mantle | `visc_exponent`, `visc_coefficient`, `visc_activation_energy`, `min_viscosity`, `max_viscosity` |
| Plastic (Mohr–Coulomb) | Brittle faulting in the cold upper crust | `cohesion0/1`, `friction_angle0/1`, `dilation_angle0/1`, `pls0/1` |

{/* TODO: explain strain softening — cohesion and friction angle drop from
    the "0" to the "1" value as plastic strain goes from pls0 to pls1; this is
    what makes faults localize. Possibly a small sketch. */}

### Seeding deformation: the weak zone

{/* TODO: why a weak zone is needed (symmetry breaking), what
    weakzone_option = 3 (Gaussian) does, where it sits in the rifting example
    (xcenter 0.5, zcenter 0.2). Link to ./weakzone for the other options. */}

### Driving deformation: velocity boundary conditions

{/* TODO: vbc_x0 / vbc_x1 = 1 (prescribed normal velocity), sign convention,
    what 1e-9 m/s is in cm/yr (~3.2 cm/yr full rate), Winkler foundation at the
    bottom, free top surface. For subduction: how the slab is pushed or pulled. */}

### Thermal structure

{/* TODO: initial geotherm (oceanic_plate_age_in_yr, surface/mantle
    temperature), how temperature feeds back into viscosity, isostatic
    adjustment phase (isostasy_adjustment_time_in_yr). */}

### Remeshing and markers

{/* TODO: why Lagrangian meshes need remeshing under large strain,
    remeshing_option = 11, quality_check_step_interval, min_quality; markers
    carry material identity across remeshes (init_marker_option). Link to
    ../theory/remeshing and ./usingmmg. */}

## Part 1: Continental rifting

The bundled example
[`examples/rifting-2d.cfg`](https://github.com/GeoFLAC/DynEarthSol/blob/master/examples/rifting-2d.cfg)
with its mesh file `rifting-2d.poly` stretches a two-layer lithosphere
(crust over mantle) at a constant rate.

| | Setting |
|---|---|
| Domain | 500 × 150 km, 6 km base resolution, two materials (crust, mantle) |
| Forcing | ±1e-9 m/s (≈3.2 cm/yr per side, 6.3 cm/yr total) extension in x |
| Duration | 2 Myr, output every 10 kyr |
| Rheology | `elasto-visco-plastic`, cohesion softening 40 → 4 MPa over 0.1 plastic strain |
| Weak zone | Gaussian (`weakzone_option = 3`), 5 km standard deviation, centered at mid-x |
| Thermal | 100 Myr plate cooling geotherm |

### Step 1: Walk through the configuration

{/* TODO: show the cfg section by section with a sentence per block.
    Suggested blocks: [sim], [mesh], [markers], [bc], [ic], [mat]. */}

```cfg title="rifting-2d.cfg (excerpt)"
[mesh]
meshing_option = 90
poly_filename = rifting-2d.poly
xlength = 500e3
zlength = 150e3
resolution = 6e3
remeshing_option = 11

[bc]
vbc_x0 = 1
vbc_x1 = 1
vbc_val_x0 = -1e-9
vbc_val_x1 = 1e-9

[ic]
weakzone_option = 3
weakzone_standard_deviation = 5e3
weakzone_xcenter = 0.5
weakzone_zcenter = 0.2
weakzone_plstrain = 1
oceanic_plate_age_in_yr = 100e6
```

The parameters you will change most often:

| Parameter | What it sets |
|-----------|--------------|
| `vbc_val_x0`, `vbc_val_x1` | Extension rate at each side wall, m/s |
| `weakzone_xcenter`, `weakzone_zcenter` | Where the rift nucleates (normalized 0–1) |
| `cohesion1`, `friction_angle1` | Strength after softening; lower = sharper faults |
| `pls1` | How much plastic strain is needed to fully soften |
| `oceanic_plate_age_in_yr` | Thermal age, hence strength, of the lithosphere |
| `min_viscosity` | Viscosity floor; also sets the time step |
| `resolution` | Element size; faults are a few elements wide |

### Step 2: Run

```bash
cd DynEarthSol/examples
OMP_NUM_THREADS=4 ../dynearthsol2d rifting-2d.cfg
```

{/* TODO: what the log prints, how to tell it is progressing, where output
    goes (modelname = result → result.save.*), roughly how long it takes. */}

### Step 3: Visualize

```bash
python ../2vtk.py result
```

Open `result.*.vtu` in ParaView. Fields to look at:

- **plastic strain** — the fault pattern
- **viscosity** — the brittle–ductile transition
- **temperature** — thinning of the thermal lithosphere
- **surface topography** — rift valley and flank uplift

{/* TODO: figure — plastic strain at 3–4 times, e.g. 0.5, 1.0, 1.5, 2.0 Myr.
    Save to ./img/tectonics/rifting-plstrain.png */}

{/* TODO: uncomment once the figure exists
![Plastic strain during rifting](./img/tectonics/rifting-plstrain.png)
*/}

Things to look for as the run proceeds:

{/* TODO: fill in — conjugate faults at the weak zone, migration of
    faulting, necking of the mantle lithosphere, asymmetric vs symmetric rift. */}

### Exercise 1: change the extension rate

| Run | `vbc_val_x0/x1` | What you should see |
|-----|-----------------|---------------------|
| Reference | `∓1e-9` | {/* TODO */} |
| Slow | `∓3e-10` | {/* TODO: more thermal relaxation, wider rift? */} |
| Fast | `∓3e-9` | {/* TODO: narrow rift, less heat loss? */} |

### Exercise 2: change the strength

{/* TODO: vary cohesion1 / friction_angle1 / pls1; or the thermal age.
    One-parameter-at-a-time rule, keep a log. */}

### Exercise 3: move the weak zone

{/* TODO: weakzone_zcenter in crust vs mantle; two weak zones with
    weakzone_option = 5 (link to ./weakzone#multi-segment-weak-zones-weakzone_option--5). */}

## Part 2: Subduction

{/* TODO: decide which bundled or new example this part uses. Options:
    (a) a new examples/subduction-2d.cfg + .poly to add upstream,
    (b) build it from rifting-2d.poly by adding a slab region.
    Fill the table below once the setup is fixed. */}

| | Setting |
|---|---|
| Domain | {/* TODO */} |
| Materials | {/* TODO: oceanic crust, oceanic mantle lithosphere, continental crust, asthenosphere, weak decoupling layer */} |
| Forcing | {/* TODO: kinematic push on the oceanic side, or free (slab-pull driven) */} |
| Duration | {/* TODO */} |
| Rheology | {/* TODO */} |
| Thermal | {/* TODO: oceanic plate age, continental geotherm */} |

### Step 1: Build the initial geometry

A subducting slab needs a pre-existing dipping interface, which the Gaussian
weak zone of Part 1 cannot provide. Build it with a `.poly` file instead,
following [Making a complex mesh with `.poly` file](./usingpolyfile).

{/* TODO: sketch of the geometry with region numbers; the poly file listing
    (nodes, segments, regions); which region is which material. Save the
    sketch to ./img/tectonics/subduction-geometry.svg */}

{/* TODO: uncomment once the figure exists
![Initial subduction geometry](./img/tectonics/subduction-geometry.svg)
*/}

```poly title="subduction-2d.poly (excerpt)"
# TODO
```

### Step 2: Walk through the configuration

{/* TODO: what differs from the rifting case — more materials, mattype_mantle,
    convergent vbc, weak layer along the plate interface, possibly
    phase_change_option, surface processes. */}

```cfg title="subduction-2d.cfg (excerpt)"
# TODO
```

| Parameter | What it sets |
|-----------|--------------|
| {/* TODO */} | |

### Step 3: Run and visualize

```bash
cd DynEarthSol/examples
OMP_NUM_THREADS=4 ../dynearthsol2d subduction-2d.cfg
python ../2vtk.py result
```

{/* TODO: figure — material/marker field and viscosity at several times.
    Save to ./img/tectonics/subduction-evolution.png */}

{/* TODO: uncomment once the figure exists
![Subduction evolution](./img/tectonics/subduction-evolution.png)
*/}

Things to look for as the run proceeds:

{/* TODO: slab bending and dip, trench retreat or advance, forearc
    deformation, mantle wedge flow, remeshing events and marker preservation. */}

### Exercise 4: plate interface strength

{/* TODO: vary the weak layer friction angle; too strong → coupling, no
    subduction; too weak → ... */}

### Exercise 5: convergence rate and slab age

{/* TODO */}

## Troubleshooting

{/* TODO: collect real messages as they come up. Candidates below. */}

| Symptom | Cause and fix |
|---------|---------------|
| Run stops with a mesh-quality error | {/* TODO: lower min_quality, more frequent quality_check_step_interval, or smaller resolution */} |
| Time step collapses (very small `dt`) | {/* TODO: dt is Maxwell-limited, dt ≈ 0.5 min_viscosity / shear_modulus; raise min_viscosity */} |
| Deformation does not localize | {/* TODO: weak zone too small or softening too mild */} |
| Everything sinks or rises at the start | {/* TODO: isostasy_adjustment_time_in_yr, reference density, ref_pressure_option */} |
| Slab does not subduct | {/* TODO: interface too strong, slab too buoyant */} |

## Next Steps

- Copy the example pair to start your own model, rather than writing configs from scratch
- Add surface processes with [GoSPL coupling](./couplinggospl)
- Refine the mesh around faults with [MMG](./usingmmg)
- Go to 3D: [Velocity boundary conditions (3D)](./vbc) and
  [Weak zones](./weakzone) for oblique and multi-segment rifts
{/* TODO: add a references bullet — Choi et al. 2013 (DES paper), rifting and
    subduction benchmark papers. */}
