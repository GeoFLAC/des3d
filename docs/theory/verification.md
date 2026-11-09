---
sidebar_position: 9
slug: /theory/verification
title: Verification and benchmarks
description: The checks that compare DynEarthSol with reference solutions, the regression tests that guard its results, and the older benchmark inputs.
---

# Verification and benchmarks

DynEarthSol is checked at three levels: against reference solutions for
individual processes, against stored results to catch unintended changes,
and by functional tests that run in continuous integration. All of them live
in the DynEarthSol repository.

## Comparisons with reference solutions

These checks have a script that runs DES, computes an independent reference
and reports the difference.

| Check | What it tests | Where | Documented in |
| --- | --- | --- | --- |
| Simple shear, elastoplastic and RSF | Stress of static-friction, steady-state and aging-law RSF against closed-form solutions; zero-velocity healing against the discrete update | `benchmarks/simple_shear_rsf/` | [Checking the friction law in simple shear](../tutorial/tectonics/rsf/simple-shear.md) |
| Confined elastic loading (PT) | Stress and strain of a confined cell against the constrained-modulus solution, for both PT schemes | PT tutorial bundle | [Elastic loading and equilibrium](../tutorial/fundamentals/elastic.md) |
| Maxwell creep (PT) | Continued creep under a held load against a discrete Maxwell reference | PT tutorial bundle | [Maxwell creep](../tutorial/fundamentals/maxwell.md) |
| Shear-band localization | Band dips in EP and EP-RSF extension against the Arthur angle (52.5°) | `benchmarks/DESv2.0/rsf/localization/` | its README |
| Plane-strain elastic update | The 2D plane-strain stress update, including the out-of-plane stress | `tests/functional/plane_strain_elastic/` | – |
| Homogeneous initial stress | `ic.initial_stress_option = 1` produces the prescribed tensor | `tests/functional/initial_stress/` | [Initial stress](../user-guide/model-setup/initial-stress.md) |
| RSF controls | Slip-rate options and the state-change time-step limit | `tests/functional/rsf_controls/` | [Rate-and-state friction](./rate-state-friction.md) |

Under `tests/residual-assembly-test/`, component checks call the production
routines directly. They cover nodal force assembly (cancellation, traction,
gravity, damping), PT constraints and failed constitutive trials, with
OpenMP, AddressSanitizer and OpenACC builds.

## Regression tests

`benchmarks-cores/` guards against unintended changes in results. A run of a
reference case is stored, and later runs are compared field by field:

```console
cd benchmarks-cores
make set                 # run once with the current executable and store the result
make cmp                 # rerun and compare with the stored result
make fresh-restart-cmp   # run, restart from a checkpoint and compare: restart determinism
```

`CASE` selects the input (default `test-3d-equ-tiny.cfg`), `NDIMS` the
dimension and `OMP` the thread count. The comparison script `compare.py`
reports the relative difference of every field and fails above $10^{-8}$ or
on a non-finite value. A change to the solver that may alter results is
checked by `make set` with the parent revision and `make cmp` with the
change; see [Testing](../developer/testing.md).

## Continuous integration

Every pull request to DynEarthSol builds the code with several compilers and
options (GCC 8–15, C++20 compatibility, macOS, NVHPC for OpenACC, MMG,
ExodusII and GoSPL builds) and runs the functional tests:

- a 3D elasto-visco-plastic model with remeshing and a temperature dome, and
  its restart determinism;
- a 2D elastoplastic model on an irregular mesh with remeshing, and its
  restart determinism;
- the plane-strain elastic update and homogeneous initial stress checks;
- a subset of the RSF simple-shear benchmark;
- rejection of malformed input files;
- a 3D run in a debug build to catch memory errors.

## Older benchmark inputs

`benchmarks/` also holds inputs from earlier versions. They are useful
starting points, but have no automated check, and some plotting scripts were
written for earlier Python versions and the earlier output reader.

| Input | Problem |
| --- | --- |
| `1d-consolidation-*.cfg`, `1d_consolidation-plot.ipynb` | One-dimensional consolidation in 2D and 3D, loaded by traction or by water |
| `2d-consolidation.cfg`, `2d_consolidation-plot.ipynb` | Two-dimensional consolidation |
| `diffusion.cfg`, `diffusion-plot.py` | Cooling of a half-space, compared with the error-function solution |
| `oedometer-2d.cfg`, `oedometer-2d-plot.py` | Elastoplastic oedometer test against its analytical path |
| `maxwell.cfg`, `maxwell.diff` | Maxwell relaxation; the patch adds the needed output |
| `acm-error-est.cfg`, `acm-error-est.diff` | Remapping error during remeshing; the patch varies the interpolation |
| `core-complex_mesh_opt.cfg`, `core-complex_new_mesh.cfg` | The core-complex model with two remeshing strategies |
