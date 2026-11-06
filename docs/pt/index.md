---
sidebar_position: 0
slug: /usage/pt
title: Pseudo-transient mechanics
---

# Pseudo-transient mechanics

DES3D offers two mechanical solution paths. The default,
`control.has_PT = no`, advances the explicit momentum equation using the
configured damping and mass scaling. With `control.has_PT = yes`, a
**pseudo-transient (PT)** solve seeks mechanical equilibrium within each
physical timestep.

PT is useful when each physical increment should satisfy a stated force
balance tolerance. Its pseudo iterations are a numerical relaxation
process; they do not resolve physical wave propagation. Assess a dynamic
problem using the explicit momentum formulation and appropriate inertia,
mass scaling and timestep choices.

This page covers solver selection and controls. The [theory](./theory.md)
explains the method; the tutorials progress from
[elastic loading and equilibrium](./tutorials/elastic.md) to
[Maxwell creep under a held load](./tutorials/maxwell.md).

## Physical steps and pseudo iterations

A physical step has a physical duration, controlled by the usual timestep
settings such as `control.fixed_dt` (seconds). Thermal diffusion, when
enabled, advances temperature once before the PT solve; temperature then
remains fixed during the mechanical trials. During the PT solve:

1. The reference mesh and the physical-start material history are held fixed.
2. Each candidate velocity is constrained by the velocity boundary conditions.
3. The constitutive law evaluates the candidate over the **same physical dt**,
   starting again from the physical-start history.
4. The solver accepts one candidate when its projected force residual meets
   the tolerance. Hydraulic transport, mesh motion and stress rotation then
   follow in their physical update stages.

Increasing the number of pseudo iterations does not repeatedly advance
plastic strain, viscous relaxation or frictional aging. It also does not
improve physical-time resolution; check the physical timestep separately.
See [PT mechanics](./theory.md) for the equations and acceptance contract.

## Enable PT and choose an iteration scheme

These options belong in the input file's existing `[control]` section:

```cfg
[control]
has_PT = yes
PT_option = 0
PT_max_iter = 5000
PT_relative_tolerance = 1e-6
PT_absolute_tolerance = 0
```

| Parameter | Default | Meaning |
|---|---|---|
| `has_PT` | `no` | Use a PT mechanical solve for each physical step. |
| `PT_option` | `0` | `0`: localized dual-time stress/velocity relaxation; `1`: adaptive dynamic relaxation (ADR). |
| `PT_max_iter` | `5000` | Maximum loop passes in one mechanical solve. |
| `PT_CFL` | `0.25` | Pseudo-time relaxation control for option 0. Unused by option 1. |
| `PT_Re` | `14.90188239869415` | Dual-time relaxation control for option 0. Unused by option 1. |
| `PT_relative_tolerance` | `1e-6` | Relative force tolerance in the default convergence mode. |
| `PT_absolute_tolerance` | `0` | Absolute force tolerance, in N/m in 2D or N in 3D. |
| `PT_use_running_scale` | `no` | Use the alternative load-history scale for physical solves. |
| `PT_stagnation_window` | `500` | Warn after this many iterations without a new best residual; `0` disables the warning. |

Both schemes use the same constitutive candidates, force residual,
acceptance test and failure handling. Option 1 derives fictitious masses
from an elastic/viscous reference stiffness and adapts its damping. Compare
the options on a checked model; an iteration advantage in one example does
not establish a general speedup. The legacy `damping_factor` is not a PT
convergence control: artificial damping is excluded from the PT residual.

`control.PT_jump` has been removed. Delete it from older input files. The
parameter reference is [`examples/defaults.cfg`](https://github.com/GeoFLAC/DynEarthSol/blob/master/examples/defaults.cfg),
also available through `./dynearthsol2d --help`.

## Understand convergence

The solver assembles **undamped** nodal forces, including gravity, applied
tractions and foundation loads. It projects these forces onto the velocity
directions the boundary conditions leave free. Constrained support reactions
therefore do not count as disequilibrium. The residual is the root mean
square (RMS) force over the free rank; an entirely constrained model has zero
free residual.

With the default `PT_use_running_scale = no`, acceptance requires

$$
R \leq \mathrm{PT\_absolute\_tolerance}
 + \mathrm{PT\_relative\_tolerance}\,R_{\mathrm{warm}}.
$$

$R_{\mathrm{warm}}$ is the first candidate's force imbalance, using the
preceding physical velocity. It is not the gross prestress. If that trial
does not converge, the solver may compare it with a candidate having zero
free velocity and retain the smaller finite residual. That comparison does
not change the relative-tolerance reference.

Absolute tolerance is a **nodal force RMS**, not a traction or stress in Pa.
Its meaning depends on dimension and mesh. A relative-only target can become
smaller than floating-point cancellation permits as the warm residual
shrinks. Inspect the printed residual and threshold when diagnosing a
failure near an already equilibrated state.

### Optional running scale

The elastic and Maxwell tutorials explicitly set:

```cfg
[control]
PT_use_running_scale = yes
```

For physical steps this replaces the default criterion with

$$
R \leq \max\left(10^{-6}R_n,\;
 1000\,\epsilon_{\mathrm{double}}F_{\mathrm{abs}}\right).
$$

$R_n$ tracks the largest first warm residual of accepted physical solves,
including the current candidate when eligible. $F_{\mathrm{abs}}$ is an
absolute assembled element-force magnitude scale from the first trial,
held fixed during that solve. The second term is a heuristic roundoff
allowance, not a bound on stress or displacement error.

Initial equilibration still uses the absolute/relative criterion. Explicitly
setting either tolerance with running scale enabled prints a warning because
those settings no longer control physical-step convergence. Initial
equilibration does not enter the running history. Remeshing retains the
history but excludes the first successful post-remesh solve from increasing it.

An earlier large load can make this criterion too permissive for a later
small perturbation. Its general use with history-dependent plastic, viscous
or rate-and-state laws remains unvalidated beyond the documented examples.
Use it with a known reference response and assess sensitivity to the loads,
timestep and mesh. The solver default remains `no`.

## Read a PT report

With `sim.info_display_step_interval = 1` and
`mesh.quality_check_step_interval = 1`, every physical step prints a record:

```text
PT step=2 status=converged iterations=1 residual=0.0342014 initial=0.0342014 threshold=0.0353553 warm_initial=35355.3 evaluations=2 stage=before_physical_updates
```

This shortened record comes from the 2D elastic tutorial, option 0.

| Field | Interpretation |
|---|---|
| `step` | Physical simulation step. |
| `status` | `converged`, `max_iterations` or `nonfinite`. |
| `iterations` | PT loop passes. A value of 1 means no relaxation update was needed. |
| `evaluations` | Full constitutive/force trials, including candidate comparisons and restoration. |
| `initial` | Residual of the selected starting candidate. |
| `warm_initial` | First warm candidate's residual; the reference for default relative convergence. |
| `residual`, `threshold` | Accepted residual and its acceptance limit. |
| `stage` | For physical steps: after any thermal update, before hydraulic transport, mesh motion and stress rotation. |

The accepted vector is saved as `PT residual force`, supported by
`Dynearthsol.py` and `2vtk.py`. Legacy `force` retains damping and support
reactions. See [PT force output](../usage/visualize.md#pt-force-output) before comparing
these fields or recomputing force from saved stress.

## Failure, restart and limits

A stagnation warning does not stop the solve or relax the tolerance. Reaching
`PT_max_iter` without convergence exits with **54**; a nonfinite candidate
exits with **50**. Mechanical history is restored and the failed candidate
does not proceed to output, hydraulic transport or mesh motion. This restores
mechanical history; an earlier thermal update is not rolled back. Review the
loading, constraints, physical timestep and attainable tolerance before changing the
iteration limit.

[Restart](../usage/run.md#checkpointing-and-restart) requires an explicitly selected
checkpoint. With unchanged controls, PT restores the saved velocity,
next-step dt and velocity scale without repeating completed initial
equilibration. Running scale also requires its checkpointed history; old
checkpoints without that history cannot restart with it enabled. Hydraulic
checkpoints require the pending pressure increment consumed by the next
mechanical step. Use one OpenMP thread for byte-exact continuation;
multi-thread ADR reductions can differ in the last bits.

PT establishes equilibrium on the reference configuration. It does not
guarantee equilibrium after mesh motion, convergence through strain
softening, or accuracy for arbitrary hydraulic coupling. Start with the
[elastic tutorial](./tutorials/elastic.md), then the
[Maxwell creep tutorial](./tutorials/maxwell.md). The
[solver notes and validation limits](https://github.com/GeoFLAC/DynEarthSol/blob/master/doc/pt-solver.md)
describe the available qualification in detail.
