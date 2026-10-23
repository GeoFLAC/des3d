---
sidebar_position: 3
---

# Visualizing outputs {#visualization}

To convert the binary output files to VTU files, run

``` console
2vtk.py modelname
```

`modelname` should be the one defined in the config file.

To see more usage information, i.e., producing .VTP files for marker
data, run

``` console
2vtk.py -h
```

-   Some of the simulation outputs can be disabled by editing `2vtk.py`
    and `output.cxx`. A more convenient control will be provided in the
    future.
-   The processed VTU (node and cell data) and VTP (marker data) files
    can be visualized with [Paraview](https://paraview.org) or
    [Visit](https://visit-dav.github.io/visit-website/index.html).
