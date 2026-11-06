---
sidebar_position: 1
---

# Manual installation of DES3D

## Docker

If you would rather not install the dependencies yourself, build a Docker
image from the repository root. `build.sh` sets the dimension (`NDIMS=2`) and
the compiler (`gcc-11`; also `gcc-8` and `clang-14`) at its top: edit them
there or pass them in the environment.

```console
./build.sh
docker run --rm -it dynearthsol/gcc-11
```

`GOSPL=1 ./build.sh` builds `dynearthsol/gcc-11-gospl` instead: a 3D executable
with GoSPL coupling, the `gospl` conda environment and `gospl_extensions`
included, so no conda setup is needed on the host. See
[Coupling with GoSPL](../tutorial/couplinggospl.md#running-with-docker) for how to run it.

The rest of this page covers building from source.

## Requirements

1. A C++17 compiler: GNU g++ 8 or newer, NVIDIA nvc++ 25.7 or newer,
   or Clang 5 or newer. Apple Clang is also supported.
2. Make and Git. The CLI11 config parser is vendored in the source tree;
   Boost is no longer required by current builds.
3. Python 3 with NumPy and SciPy for the Python tools. Add `h5py` to read
   VTKHDF output and Matplotlib for the PT tutorial figures.
4. On macOS, an OpenMP runtime such as Homebrew's `libomp`.
5. Optional libraries: [MMG](https://github.com/MmgTools/mmg) for adaptive
   remeshing (bundled as a submodule), ExodusII from
   [SEACAS](https://github.com/sandialabs/seacas) for 3D mesh import, and
   HDF5 for VTKHDF output.

These requirements describe Latest. For an older release, select its
manual version and use the dependencies in that release's README. See the
[current solver README](https://github.com/GeoFLAC/DynEarthSol#building-des)
for platform package commands.

### Submodules (mmg, nanoflann, knn-bvh)

`mmg`, `nanoflann`, and `knn-bvh` are bundled as git submodules and
built automatically by `make`; no separate installation or path
configuration is required. After cloning, initialize them once:

```console
git submodule update --init --recursive
```

`make` will also auto-initialize stale submodules, but running the
command above explicitly after cloning is recommended.

## Configuration

### Build options

| Parameter Name | Possible Values | Description |
|----------------|-----------------|-------------|
| `ndims`        | `2`, `3`        | Choose `2` for two-dimensional models (`dynearthsol2d`) or `3` for three-dimensional models (`dynearthsol3d`). |
| `opt`          | `0`, `1`, `2`, `3` | Integer value for optimization level. |
| `openacc`      | `0`, `1`        | Disable (`0`) or enable (`1`) OpenACC build. |
| `GPU_CC`       | compute capability, e.g. `80`, `90` | GPU compute capability to target when `openacc=1`. Defaults to the capability of the GPU detected on the host (via `nvidia-smi`), or `80` if none is detected. `make config` prints the value in use. |
| `openmp`       | `0`, `1`        | Disable (`0`) or enable (`1`) OpenMP build. |
| `nprof`       | `0`, `1`        | Disable (`0`) or enable (`1`) profiling with nprof. |
| `gprof`       | `0`, `1`        | Disable (`0`) or enable (`1`) profiling with gprof. |
| `usemmg`       | `0`, `1`        | Disable (`0`) or enable (`1`) mesh optimization during remeshing with mmg. |
| `useexo`       | `0`, `1`        | Disable (`0`) or enable (`1`) import of an .exo mesh, usually created with the meshing software, CUBIT. Note: Only a 3D mesh can be imported currently.|
| `hdf5`         | `0`, `1`        | Enable HDF5-based VTKHDF output (see [Visualizing outputs](./visualize.md)). Paths are auto-detected on Linux and macOS via `pkg-config` and the usual install layouts; override with `HDF5_INCLUDE_DIR` / `HDF5_LIB_DIR` if the wrong install is picked up or the build stops with install advice. |

### Optional external libraries

#### `ExodusII`
If you want to import an `ExodusII` mesh (.exo), 
- install [SEACAS](https://github.com/sandialabs/seacas) enabling exodus support
- set `useexo = 1` and `ndims = 3`. Only 3D exodus mesh can be imported. 
- set `EXO_INCLUDE` and `EXO_LIB_DIR` in `Makefile` based on the SEACAS installation path.

#### `MMG`
MMG is bundled as a git submodule and built automatically; no manual
installation or path configuration is needed. To enable it:

- set `usemmg = 1` (both `ndims=2` and `ndims=3` are supported).

For further information, see [Adaptive mesh refinement with MMG](https://geoflac.github.io/des3d/docs/tutorial/usingmmg).

#### `HDF5`
For outputting model results in the HDF5-based VTKHDF format (compressed,
often ~50% smaller, and viewable directly in ParaView without conversion):

- install HDF5 with your package manager (`brew install hdf5` on macOS,
  `apt install libhdf5-dev` on Debian/Ubuntu, `dnf install hdf5-devel` on
  Fedora/RHEL); it is commonly pre-installed already.
- set `hdf5 = 1`. `make` locates the include/lib paths itself via
  `pkg-config` and standard install layouts; set `HDF5_INCLUDE_DIR` and
  `HDF5_LIB_DIR` to override.

See [Visualizing outputs](./visualize.md) for the VTKHDF file format and the
`2vtk.py --update-vtkhdf` workflow.

## Building

```BASH
$ make
```

Build options can be set on the command line without editing `Makefile`: e.g.,

-   To build optimized executable (default optimization level, 2): `make`
-   To build a debugging executable: `make opt=0` 
-   To build the executable without `OpenMP`: `make openmp=0` 
    - This build is necessary to debug the code under `valgrind`.

### macOS (Apple Silicon)

Apple's built-in Clang supports OpenMP compilation but ships no OpenMP
runtime. Install the runtime with Homebrew:

```console
brew install libomp
```

Then a plain build finds everything on its own, no paths to edit and none
to pass on the command line:

```console
make ndims=2
```

OpenMP is searched at the Homebrew prefix matching the machine's
architecture (`/opt/homebrew` on Apple Silicon, `/usr/local` on Intel), not
via `PATH`; this matters on a Mac that has ever used both prefixes, where
`PATH` often points at an install of the wrong architecture. If a build picks
up something unexpected:

```console
make config       # prints the compiler and every resolved dependency path
make check-deps   # validates dependencies (fatal on macOS) without building
```

`OPENMP_ROOT_DIR` can be set on the command line to force
a specific runtime install when the search doesn't find the right one.

At startup, DES3D automatically sets `OMP_WAIT_POLICY=active` on macOS
to avoid a performance regression caused by `libomp`'s default
zero-blocktime on Apple Silicon. You can override this by setting the
variable in your environment before running the executable.
