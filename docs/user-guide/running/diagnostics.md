---
sidebar_position: 2
slug: /user-guide/diagnostics
title: Provenance, warnings and exit codes
---

# Provenance, warnings and exit codes

Every run records where it came from, and stops with a numbered exit code
when something goes wrong.

## Provenance

Every build, run and frame records where it came from:

| What | Where |
|---|---|
| The build | in the executable, as a `build.snapshot` block: `strings <exe> \| grep '^build\.snapshot\.'` |
| The run | in `<modelname>.manifest`, beside the model's output |
| Each frame or checkpoint | a `/provenance` group (HDF5) or a `provenance` record (des-binary) in the file itself |

The manifest uses the cfg format: `[runtime.model]`, `[runtime.host]`, `[runtime.device]`,
`[runtime.threads]` and `[runtime.env]` first, then the build's own `[build.*]` sections, closed
by `[runtime.end]` once the time loop ends (a record without it died, was killed, or is still
running). Its first fields, `end_time`, `stopped_by` and `wall_time`, are enough to see how every
run of a sweep ended:

```console
grep -A3 '^[runtime.end]' */*.manifest
```

A restart appends its record rather than starting the file over. The same sections print to the
screen once at run start, one line each as `[build][...]` then `[runtime][...]`; set
`sim.has_runtime_info_display = no` to silence them:

```cfg
[sim]
has_runtime_info_display = no
```

`make snapshot_diff=1` (off by default) also embeds the working-tree diff in the executable, so
`build.code-changes` in the manifest is more than a note that it wasn't captured.

A GPU build that finds no device exits `52` (see [Exit codes](#exit-codes)) after appending its
manifest record, so the attempt is on record even though the run never started.

The full field-by-field reference is
[`doc/provenance.md`](https://github.com/GeoFLAC/DynEarthSol/blob/master/doc/provenance.md) in
the DynEarthSol repository.

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

## Exit codes

DES3D exits with a two-digit code that is printed together with its category.
The first digit is the category (`1x` is yours to fix, `2x` the environment,
`3x`–`6x` the code itself) and the second the specific cause:

| Code | Meaning |
|------|---------|
| `0` | Normal exit |
| `10` / `11` | Config error / bad value or unknown option |
| `12` | Malformed `.poly` or `.exo` file |
| `20` / `21` / `22` | Cannot open file / read or write failed (HDF5) / restart mismatch |
| `30` / `31` | Unsupported in this `NDIMS` / library not built in |
| `40` / `41` / `42` | Triangle or TetGen / MMG / mesh quality or topology |
| `50` / `51` / `52` | NaN or non-finite value / marker or geometry lookup / resource exhausted |
| `53` | GoSPL coupling step failed |
| `54` | PT mechanical solve did not converge |
| `60` / `61` | Assertion violated / unreachable branch |

Errors in the configuration file stop the run with `10` or `11` and a message
naming the problem. For example, every `mattype_*` index is checked against
`num_materials` at startup, and an out-of-range one exits with `11` naming the
parameter.

A NaN velocity stops the run with `50` instead of continuing to write frames.
The run prints a single line summarizing the affected fields, their counts and
the first bad element and node. A GPU build that finds no device at startup
exits `52`, after appending its manifest record; see [Provenance](#provenance).
A failed GoSPL coupling step (built with `usegospl=1`) stops the run with
`53` instead of silently dropping that interval's erosion; see
[Coupling with GoSPL](../../tutorial/advanced/couplinggospl.md).
PT reaching its iteration limit exits with `54` after restoring the
physical-start mechanical history; a nonfinite PT candidate exits with `50`.
Stagnation warnings alone do not stop a PT solve. See [PT controls](../numerical-controls/solver.md).
Scripts that test for specific exit statuses need updating: earlier builds used
`1`, `2`, `10`, `11` and `12` with different meanings.
