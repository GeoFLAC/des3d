---
sidebar_position: 1
---

# Manual installation of DES3D

Docker image coming soon!

## Requirements

1.  A C++ compiler that supports C++11 standard. GNU g++ 5.0 or
    newer will suffice
2.  **Boost::Program_options** library. Version 1.42 or newer. Boost is a large set of libraries. 
    To install only `program_options` library, follow these stpes:
    1. First download the source code from [https://www.boost.org]. 
    2. In the untarred source directory, run:

        ``` console
        ./bootstrap.sh
        ```

        In the same directory, build the library by running:

        ``` console
        ./b2 --with-program_options -q
        ```
3.  Python 3.2+
4.  Numpy for post-processing
5.  Optional: 
    1. [MMG3D](https://www.mmgtools.org/mmg-remesher-downloads): An optional mesh adaptation library. Used for remeshing in DES3D.
    2. `Exodus`: For importing a mesh in the *ExodusII* format. Available as a part of
    SEACAS project [https://github.com/gsjaardema/seacas/]

## Configuration

### Required dependencies

#### `boost::program_options`

Modify `BOOST_ROOT_DIR` in Makefile if you manually built or installed
boost library. If you followed the instructions above to build
`Boost::Program_options` library, set `BOOST_ROOT_DIR` to the untarred
boost directory.

### Build options

| Parameter Name | Possible Values | Description |
|----------------|-----------------|-------------|
| `ndims`        | `2`, `3`        | Choose `2` for two-dimensional models (`dynearthsol2d`) or `3` for three-dimensional models (`dynearthsol3d`). |
| `opt`          | `0`, `1`, `2`, `3` | Integer value for optimization level. |
| `openacc`      | `0`, `1`        | Disable (`0`) or enable (`1`) OpenACC build. |
| `openmp`       | `0`, `1`        | Disable (`0`) or enable (`1`) OpenMP build. |
| `nprof`       | `0`, `1`        | Disable (`0`) or enable (`1`) profiling with nprof. |
| `gprof`       | `0`, `1`        | Disable (`0`) or enable (`1`) profiling with gprof. |
| `usemmg`       | `0`, `1`        | Disable (`0`) or enable (`1`) mesh optimization during remeshing with mmg. |
| `useexo`       | `0`, `1`        | Disable (`0`) or enable (`1`) import of an .exo mesh, usually created with the meshing software, CUBIT. Note: Only a 3D mesh can be imported currently.|

### Optional external libraries

#### `ExodusII`
If you want to import an `ExodusII` mesh (.exo), 
- install [SEACAS](https://github.com/sandialabs/seacas) enabling exodus support
- set `useexo = 1` and `ndims = 3`. Only 3D exodus mesh can be imported. 
- set `EXO_INCLUDE` and `EXO_LIB_DIR` in `Makefile` based on the SEACAS installation path.

#### `MMG`
Install this library if adaptive mesh optimization is desired: e.g., finer elements where plastic strain is localized.

- install [MMG](https://github.com/MmgTools/mmg)
- set `usemmg = 1`. Both `dims=2` and `3` are supported.
- set `MMG_INCLUDE` and `MMG_LIB_DIR` based on the MMG installation paths.
- For further information, see [Adaptive mesh refinement with MMG](https://geoflac.github.io/des3d/docs/tutorial/usingmmg)

## Building

```BASH
$ make
```

Build options can be set on the command line without editing `Makefile`: e.g.,

-   To build optimized executable (default optimization level, 1): `make`
-   To build a debugging executable: `make opt=0` 
-   To build the executable without `OpenMP`: `make openmp=0` 
    - This build is necessary to debug the code under `valgrind`.
