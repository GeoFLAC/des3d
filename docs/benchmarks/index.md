---
sidebar_position: 0
slug: /benchmarks
title: Benchmarks
description: How DynEarthSol compares with analytical, theoretical and independent solutions, and the regression and functional tests that guard its results.
---

# Benchmarks

Each benchmark runs DES on a problem with a known answer, an analytical
solution, a theoretical prediction or an independent calculation, and shows
how close DES comes and where the comparison stops. The inputs are in the
DynEarthSol repository; each page says how to run them and what to expect.

DynEarthSol is also checked against stored results to catch unintended
changes, and by functional tests that run in continuous integration; both are
listed below.

## Benchmarks in this section

| Benchmark | Compared with | Inputs |
| --- | --- | --- |
| [Shear bands with and without rate-and-state friction](./geodynamics/localization.md) | Band dips against the Arthur angle | `benchmarks/DESv2.0/rsf/localization/` |
| [Checking the friction law in simple shear](./faults-friction/simple-shear.md) | Closed-form stresses for static friction and steady-state and aging-law RSF | `benchmarks/simple_shear_rsf/` |
| [Elastoplastic oedometer test](./mechanics/oedometer.md) | Closed-form Mohr–Coulomb stress path under uniaxial strain | `benchmarks/oedometer-2d.cfg` |
| [Maxwell stress build-up in pure shear](./mechanics/maxwell.md) | Maxwell response at a constant strain rate | `benchmarks/maxwell.cfg` |
| [Cooling of a half-space](./heat/half-space-cooling.md) | Error-function profile in 2D and 3D | `benchmarks/diffusion.cfg` |
| [Rate-and-state friction under a velocity step](./faults-friction/rsf-velocity-step.md) | Closed-form RSF response to a step in slip rate | `benchmarks/hydromechanics/` |
| [Fault-zone heating at fixed normal traction](./faults-friction/fault-heat.md) | Thermal weakening by shear heating: shear resistance, temperature and pore pressure against a differential reference | `benchmarks/hydromechanics/` |
| [Poromechanics](./poromechanics/index.md), 32 benchmarks | Consolidation, groundwater and unsaturated flow, openings, injection and heat transport against analytical and independent solutions | `benchmarks/hydromechanics/`, `tests/functional/hydromechanics/` |

## Other comparisons with reference solutions

These checks compare DES with a reference solution inside a tutorial or a
functional test.

| Check | What it tests | Where | Documented in |
| --- | --- | --- | --- |
| Confined elastic loading (PT) | Stress and strain of a confined cell against the constrained-modulus solution, for both PT schemes | PT tutorial bundle | [Elastic loading and equilibrium](../tutorial/fundamentals/elastic.md) |
| Maxwell creep (PT) | Continued creep under a held load against a discrete Maxwell reference | PT tutorial bundle | [Maxwell creep](../tutorial/fundamentals/maxwell.md) |
| Plane-strain elastic update | The 2D plane-strain stress update, including the out-of-plane stress | `tests/functional/plane_strain_elastic/` | – |
| Homogeneous initial stress | `ic.initial_stress_option = 1` produces the prescribed tensor | `tests/functional/initial_stress/` | [Initial stress](../user-guide/model-setup/initial-stress.md) |
| RSF controls | Slip-rate options and the state-change time-step limit | `tests/functional/rsf_controls/` | [Rate-and-state friction](../theory/rate-state-friction.md) |

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
