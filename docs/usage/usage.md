---
sidebar_position: 1
---

# Manual installation

## Requirements

1.  A **C++ compiler** that supports C++11 standard. GNU g++ 5.0 or
    newer will suffice
2.  **Boost::Program_options** library. Version 1.42 or newer. To
    install only this library, first download the source code from
    [https://www.boost.org]. In the untarred source directory, run

``` console
./bootstrap.sh
```

In the same directory, build the library by running

``` console
./b2 --with-program_options -q
```

3.  [MMG3D](https://www.mmgtools.org/mmg-remesher-downloads)
4.  Python 3.2+
5.  Numpy for post-processing
6.  Optional: For importing a mesh in the *ExodusII* format, you need to
    install the library, `exodus`, which is available as a part of
    SEACAS project [https://github.com/gsjaardema/seacas/]

## Configuration

Modify `BOOST_ROOT_DIR` in Makefile if you manually built or installed
boost library. If you followed the instructions above to build
`Boost::Program_options` library, set `BOOST_ROOT_DIR` to the untarred
boost directory.

If you want to import an `ExodusII` mesh (.exo), 
- set `useexo = 1` and `ndims = 3`. Only 3D exodus mesh can be imported. 
- set `EXO_INCLUDE` and `EXO_LIB_DIR` paths.

## Building

-   Run `make` to build optimized executable.
-   Or run `make opt=0` to build a debugging executable.
-   Or run `make openmp=0` to build the executable without `OpenMP`.
    This is necessary to debug the code under valgrind.
