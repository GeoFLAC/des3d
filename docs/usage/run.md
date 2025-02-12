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
