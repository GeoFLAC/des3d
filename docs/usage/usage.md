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
    1. [MMG](https://github.com/MmgTools/mmg): mesh adaptation library for adaptive remeshing. Bundled as a git submodule — no separate installation required (see below).
    2. `Exodus`: For importing a mesh in the *ExodusII* format. Available as a part of
    SEACAS project [https://github.com/gsjaardema/seacas/]

### Submodules (mmg, nanoflann, knn-bvh)

`mmg`, `nanoflann`, and `knn-bvh` are bundled as git submodules and
built automatically by `make` — no separate installation or path
configuration is required. After cloning, initialize them once:

```console
git submodule update --init --recursive
```

`make` will also auto-initialize stale submodules, but running the
command above explicitly after cloning is recommended.

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
| `use_gpu_knn`  | `0`, `1`        | Enable GPU-accelerated k-nearest-neighbour search via BVH (requires `openacc = 1`). Reduces remeshing time by ~61 % on GPU. Requires the `knn-bvh` submodule. |
| `SOA`          | `0`, `1`        | Enable Structure-of-Arrays memory layout for `Array2D`. Improves remeshing speed by >2× on CPU and is beneficial on GPU (H100). Default off. |
| `hdf5`         | `0`, `1`        | Enable HDF5-based VTKHDF output (see [Visualizing outputs](./visualize)). Paths are auto-detected on Linux and macOS via `pkg-config` and the usual install layouts; override with `HDF5_INCLUDE_DIR` / `HDF5_LIB_DIR` if the wrong install is picked up or the build stops with install advice. |

### Optional external libraries

#### `ExodusII`
If you want to import an `ExodusII` mesh (.exo), 
- install [SEACAS](https://github.com/sandialabs/seacas) enabling exodus support
- set `useexo = 1` and `ndims = 3`. Only 3D exodus mesh can be imported. 
- set `EXO_INCLUDE` and `EXO_LIB_DIR` in `Makefile` based on the SEACAS installation path.

#### `MMG`
MMG is bundled as a git submodule and built automatically — no manual
installation or path configuration is needed. To enable it:

- set `usemmg = 1` (both `ndims=2` and `ndims=3` are supported).

For further information, see [Adaptive mesh refinement with MMG](https://geoflac.github.io/des3d/docs/tutorial/usingmmg).

#### `HDF5`
For outputting model results in the HDF5-based VTKHDF format (compressed,
often ~50% smaller, and viewable directly in ParaView without conversion):

- install HDF5 with your package manager (`brew install hdf5` on macOS,
  `apt install libhdf5-dev` on Debian/Ubuntu, `dnf install hdf5-devel` on
  Fedora/RHEL) — it is commonly pre-installed already.
- set `hdf5 = 1`. `make` locates the include/lib paths itself via
  `pkg-config` and standard install layouts; set `HDF5_INCLUDE_DIR` and
  `HDF5_LIB_DIR` to override.

See [Visualizing outputs](./visualize) for the VTKHDF file format and the
`2vtk.py --update-vtkhdf` workflow.

## Building

```BASH
$ make
```

Build options can be set on the command line without editing `Makefile`: e.g.,

-   To build optimized executable (default optimization level, 1): `make`
-   To build a debugging executable: `make opt=0` 
-   To build the executable without `OpenMP`: `make openmp=0` 
    - This build is necessary to debug the code under `valgrind`.

### macOS (Apple Silicon)

Apple's built-in Clang implements the OpenMP pragmas but ships no OpenMP
runtime, and there is no system Boost either, so both have to come from a
package manager. Install them with Homebrew:

```console
brew install boost libomp
```

Then a plain build finds everything on its own — no paths to edit and none
to pass on the command line:

```console
make ndims=2
```

Boost and OpenMP are searched at the Homebrew prefix matching the machine's
architecture (`/opt/homebrew` on Apple Silicon, `/usr/local` on Intel), not
via `PATH` — this matters on a Mac that has ever used both prefixes, where
`PATH` often points at an install of the wrong architecture. If a build picks
up something unexpected:

```console
make config       # prints the compiler and every resolved dependency path
make check-deps   # validates dependencies (fatal on macOS) without building
```

`OPENMP_ROOT_DIR` / `BOOST_ROOT_DIR` can be set on the command line to force
a specific install when the search doesn't find the right one.

At startup, DES3D automatically sets `OMP_WAIT_POLICY=active` on macOS
to avoid a performance regression caused by `libomp`'s default
zero-blocktime on Apple Silicon. You can override this by setting the
variable in your environment before running the executable.
