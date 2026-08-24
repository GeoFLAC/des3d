---
sidebar_position: 5
title: Weak zones
---

# Weak zones

DES3D supports several ways to define fault-like weak zones that focus
deformation in a model.

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
