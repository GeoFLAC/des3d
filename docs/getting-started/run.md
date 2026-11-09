---
sidebar_position: 3
slug: /usage/run
---

# Running DynEarthSol {#running_des3d}

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

For a force-balanced mechanical solve within each physical timestep, see
[Choosing a mechanical solver (PT)](../user-guide/numerical-controls/solver.md) and the
[elastic-loading tutorial](../tutorial/fundamentals/elastic.md).

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

## Going further

- [Restarting from a checkpoint](../user-guide/running/restart.md)
- [Provenance, warnings and exit codes](../user-guide/running/diagnostics.md)
- [Initial stress](../user-guide/model-setup/initial-stress.md)
- [Choosing a mechanical solver](../user-guide/numerical-controls/solver.md)
