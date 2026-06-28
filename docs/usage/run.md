---
sidebar_position: 2
---

# Running DES3D {#running_des3d}

``` console
dynearthsol2d input.cfg
```

or

``` console
dynearthsol3d input.cfg
```

-   Several example input files are provided under `examples/`
    directory. The format of the input file is described in
    `examples/defaults.cfg`.
-   Benchmark cases with analytical solution can be found under
    `benchmarks/` directory.
-   Execute the executable with `-h` flag to see the available input
    parameters and their descriptions.

## Progress reporting

The `sim.info_display_step_interval` parameter controls how often
DES3D prints a status line to the screen:

```cfg
info_display_step_interval = 10   # print progress every 10 simulation steps
```

This parameter replaced the older `info_display_interval` (which was
wall-clock seconds) as of 2026. The value must be a positive multiple
of `mesh.quality_check_step_interval`; DES3D will round it up
automatically and notify you if an adjustment is made.

## Checkpointing and restart

DES3D writes checkpoint files at regular intervals so that a simulation
can be resumed after interruption. As of 2026, restarts are
**deterministic**: a restarted run produces bit-for-bit identical output
to one that never stopped. The following state is now fully persisted in
the checkpoint:

- `dt` and `dt_PT` (time step)
- `max_global_vel_mag`
- `reference_frame_time`
- `info_display_next_step`
- `dhacc` (surface marker correction)
- `strain_rate`, `viscosity`, `volume_old`

To restart from a checkpoint, run the executable with the same config
file. DES3D detects the most recent checkpoint automatically.

## Run-time warnings

-   While running, DES3D might print warnings on screen. An example is
    the warning about the potential race condition: e.g.,

``` console
****************************************************************
*    Warning: egroup-0 and egroup-2 might share common nodes.
*             There is some risk of racing conditions.
*             Please either increase the resolution or
*             decrease the number OpenMP threads.
****************************************************************
```

-   Please do pay attention and follow given suggestions if any.
