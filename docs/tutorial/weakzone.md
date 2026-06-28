---
sidebar_position: 4
title: Weak zones and velocity boundary conditions
---

# Weak zones and velocity boundary conditions (3D)

DES3D supports several ways to prescribe velocity boundary conditions
(VBCs) on the lateral faces of a 3D model and to define fault-like weak
zones that focus deformation. This page documents the features added in 2026.

## Lateral-face VBC cases

Each lateral face (`x0`, `x1`, `y0`, `y1`) can be assigned an
independent VBC case. The case number is set via `bc.vbc_x0`, `bc.vbc_x1`,
`bc.vbc_y0`, `bc.vbc_y1`.

| Case | Normal component | Lateral-shear component | Vertical |
|------|-----------------|------------------------|---------|
| 0 | Free | Free | Free |
| 1 | Fixed (`vbc_val_*`) | Free | Free |
| 2 | Free | Fixed (0) | Free |
| 3 | Fixed | Fixed (0) | Free |
| 4 | Free | Free | Fixed (0) |
| 5 | Fixed | Fixed | Free |
| **6** | **Fixed (`vbc_val_*`)** | **Fixed (`vbc_val_*_l`)** | **Free** |

**Case 6** is new and allows setting both the normal and lateral-shear
velocities to independent non-zero values. It is useful for
transtensional or transpressional boundary conditions.

### New parameters for case 6

```cfg
bc.vbc_x0 = 6
bc.vbc_val_x0   = -0.01   # normal velocity (m/yr)
bc.vbc_val_x0_l =  0.005  # lateral-shear velocity (m/yr)

bc.vbc_x1 = 6
bc.vbc_val_x1   =  0.01
bc.vbc_val_x1_l = -0.005
```

See `examples/oblique-rift-3d.cfg` for a complete transtensional rifting
example using case 6.

## Multi-segment weak zones (`weakzone_option = 4`)

For models that require more than one pre-existing fault (e.g.,
conjugate normal faults or a step-over fault system), use
`weakzone_option = 4`. This option accepts an arbitrary number of planar
fault segments, each defined by its own orientation and spatial bounds.

Each segment uses a `General_planar_zone` formulation with a proper
unit-normal, avoiding the `tan(azimuth)` numerical singularity of the
older `Planar_zone`.

### Configuration

```cfg
weakzone_option = 4
weakzone_num_segments = 2    # number of fault segments

# Segment 0
weakzone_segments_0_azimuth      = 30.0   # degrees from north
weakzone_segments_0_dip          = 60.0   # degrees from horizontal
weakzone_segments_0_x_min        = 50e3   # bounding box x (m)
weakzone_segments_0_x_max        = 150e3
weakzone_segments_0_y_min        = 0.0
weakzone_segments_0_y_max        = 200e3
weakzone_segments_0_depth_min    = 0.0
weakzone_segments_0_depth_max    = 30e3

# Segment 1
weakzone_segments_1_azimuth      = -30.0
weakzone_segments_1_dip          = 60.0
weakzone_segments_1_x_min        = 150e3
weakzone_segments_1_x_max        = 250e3
weakzone_segments_1_y_min        = 0.0
weakzone_segments_1_y_max        = 200e3
weakzone_segments_1_depth_min    = 0.0
weakzone_segments_1_depth_max    = 30e3
```

See `examples/conjugate-faults-3d.cfg` for a two-segment conjugate
normal-fault setup.

:::tip Number of segments
`weakzone_num_segments` can be set to any positive integer. Add a
`weakzone_segments_N_*` block for each segment index `N = 0, 1, …`.
:::

## Gaussian weak zone initial condition (IC case 4)

`initial_weakzone_option = 4` places a planar weak zone whose along-strike
width follows a Gaussian envelope in map view. This is useful for
localising the initial failure to the centre of the model domain while
tapering to zero at the lateral edges.

```cfg
initial_weakzone_option  = 4
weakzone_azimuth         = 0.0    # strike direction (degrees from north)
weakzone_dip             = 60.0   # dip angle
weakzone_gaussian_width  = 50e3   # half-width at 1/e (m)
```

See `gospl_driver/examples/gaussian-weakzone-3d-with-gospl.cfg` for an
example that combines this IC with GoSPL surface-process coupling.
