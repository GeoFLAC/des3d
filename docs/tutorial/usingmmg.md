---
sidebar_position: 3
---

# Adaptive mesh refinement in DES3D 

## Parameters for [MMG](https://mmgtools.org)

- `mmg_debug`: Turn on/off *debug* mode. In debug mode, MMG checks if all structures are allocated.
- `mmg_verbose`: Level of verbosity, -1 to 10.
- `mmg_hmax_factor`: Positive number. The maximum possible element size set to be `hmax * param.mesh.resolution`
- `mmg_hmin_factor`: Positive number. The minimum possible element size set to be `hmin * param.mesh.resolution`
- `mmg_hausd_factor`: Global Hausdorff distance (on all boundaries in the mesh). Roughly speaking, allowed difference of the boundary before and after mesh refinement or optimization.

For more MMG parameters, refer to https://mmgtools.github.io/libmmg3d_8h.html#a964a06109019542d04f12263c3fae24d


For instance,
```JSON
mmg_debug = 0
mmg_verbose = 0
mmg_hmax_factor = 10.0
mmg_hmin_factor = 1.0
mmg_hausd_factor = 0.01
```

## What happens during remeshing

### Using MMG for remeshing

One needs to set `usemmg` to `1` in `Makefile`:
```Makefile
usemmg = 1
```

In `Makefile`, the following build parameters are set:
```Makefile
ifeq ($(usemmg), 1)
        # path to MMG3D header files
        MMG_INCLUDE = $(HOME)/opt/mmglib/include

        # path of MMG3D library files, if not in standard system location
        MMG_LIB_DIR = $(HOME)/opt/mmglib/lib

        MMG_CXXFLAGS = -I$(MMG_INCLUDE) -DUSEMMG
        ifeq ($(ndims), 3)
                MMG_LDFLAGS = -L$(MMG_LIB_DIR) -lmmg3d
        else
                MMG_LDFLAGS = -L$(MMG_LIB_DIR) -lmmg2d
        endif
        ifneq ($(OSNAME), Darwin)  # Apple's ld doesn't support -rpath
                MMG_LDFLAGS += -Wl,-rpath=$(MMG_LIB_DIR)
        endif
endif
```

```Makefile
ifeq ($(usemmg), 1)
        CXXFLAGS += $(MMG_CXXFLAGS)
        LDFLAGS += $(MMG_LDFLAGS)
endif
```

When `USEMMG` is defined during the build process with `-DUSEMMG`, `remesh()` function calls `optimize_mesh()`, not `new_mesh()`.

```C++
void remesh(const Param &param, Variables &var, int bad_quality)
{
...
#ifdef THREED
#if defined ADAPT || defined USEMMG
        optimize_mesh(param, var, bad_quality, old_coord, old_connectivity,
                 old_segment, old_segflag);
#else
        new_mesh(param, var, bad_quality, old_coord, old_connectivity,
                 old_segment, old_segflag);
#endif
...
```

### `optimize_mesh()`

#### Options for the bottom boundary

The option `param.mesh.remeshing_option` determines what to do to the bottom boundary during remeshing. However, it does not directly control how MMG performs mesh optimization. 

```C++
/* choosing which way to remesh the boundary */
    switch (param.mesh.remeshing_option) {
    case 0:
        // DO NOT change the boundary
        excl_func = &is_boundary;
        break;
    case 1:
        excl_func = &is_boundary;
        flatten_bottom(old_bcflag, qcoord, -param.mesh.zlength,
                       points_to_delete, min_dist);
        break;
    case 2:
        excl_func = &is_boundary;
        new_bottom(old_bcflag, qcoord, -param.mesh.zlength,
                   points_to_delete, min_dist, qsegment, qsegflag, old_nseg);
        break;
    case 10:
        excl_func = &is_corner;
        break;
    case 11:
        excl_func = &is_corner;
        flatten_bottom(old_bcflag, qcoord, -param.mesh.zlength,
                       points_to_delete, min_dist);
        break;
    case 12:
        flatten_x0(old_bcflag, qcoord, points_to_delete);
        break;
    default:
        std::cerr << "Error: unknown remeshing_option: " << param.mesh.remeshing_option << '\n';
        std::exit(1);
    }
```

#### Workflow

1. Initialization
2. Mesh building in MMG5 format
3. Solution (i.e., metric) field building
	- When a solution filed is provided, MMG's mesh optimization, re-shaping element respecting the original sizes, does NOT occur. Instead, new elements are created as desired according to the parameters.
	- The current default mode in DES3D is to provide a solution field.
	- For this purpose, there is a customizable function, `compute_metric_field()` in `remesh.dxx`. More about this function below.
4. Mesh optimization
5. Mesh-related data update using the optimized MMG5 mesh

<!-- 
#### `compute_metric_filed()`

This is a short function that converts one of the data filed to a metric field. Currently, it scales `plastic_strain` to a solution field. A solution, $h$, at a node is directly used for determining an element size. 

$h$ ranges between $h_{min}$ and $h_{max}$.

- $h_{max} =$ `param.mesh.mmg_hmax_factor * param.mesh.resolution`
- $h =$ $h_{max}/(1 + 10\varepsilon_{pl})$
- $h_{min} = \max (h, $`param.mesh.mmg_hmin_factor * param.mesh.resolution`$)$.

For instance, with

- `param.mesh.resolution = 1e3` (i.e., 1 km)
- `param.mesh.mmg_hmax_factor = 2.0`
- `param.mesh.mmg_hmin_factor = 0.1`
- $\varepsilon_{pl}$ between 0 and 10,

we get

- $h = h_{max} = $ 2 km where $\varepsilon_{pl} = 0$.
- $h =$ 2 km / (1+10 $\varepsilon_{pl}$) where $\varepsilon_{pl} \le 1.9$.
- $h =$ 100 m where $\varepsilon_{pl} > 1.9$.

Here is the full code listing:

```C++
void compute_metric_field(const Variables &var, const Param &param, const conn_t &connectivity, const double resolution, double_vec &metric, double_vec &tmp_result_sg)
{
    /* dvoldt is the volumetric strain rate, weighted by the element volume,
     * lumped onto the nodes.
     */
    std::fill_n(metric.begin(), var.nnode, 0);

#ifdef GPP1X
    #pragma omp parallel for default(none) shared(var,param,connectivity,tmp_result_sg,resolution)
#else
    #pragma omp parallel for default(none) shared(var,param,connectivity,tmp_result_sg)
#endif
    for (int e=0;e<var.nelem;e++) {
        // const int *conn = connectivity[e];
        // double plstrain = resolution/(1.0+5.0*(*var.plstrain)[e]);
        // tmp_result_sg[e] = plstrain * (*var.volume)[e];
        // tmp_result_sg[e] = plstrain * (*var.volume)[e];
        // resolution/(1.0+(*var.plstrain)[e]);
		 double metric = param.mesh.mmg_hmax_factor*param.mesh.resolution / (1.0 + 10.0*(*var.plstrain)[e]);
        metric = std::max(metric, param.mesh.mmg_hmin_factor*param.mesh.resolution);
        tmp_result_sg[e] = metric * (*var.volume)[e];
    }

    #pragma omp parallel for default(none) shared(var,metric,tmp_result_sg)
    for (int n=0;n<var.nnode;n++) {
        for( auto e = (*var.support)[n].begin(); e < (*var.support)[n].end(); ++e)
            metric[n] += tmp_result_sg[*e];
        metric[n] /= (*var.volume_n)[n];
    }
}
``` -->