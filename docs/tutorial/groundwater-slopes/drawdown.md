---
sidebar_position: 4
title: "Rapid drawdown of a reservoir against an embankment"
---
# Rapid drawdown of a reservoir against an embankment

A reservoir stands at the crest of the embankment and the slope is saturated. When the reservoir is drawn down quickly the water no longer supports the face, while the pore pressure inside falls only as the slope drains: the classic critical case for the upstream slope of a dam.

**250 s after drawdown DES brackets the factor of safety at 0.85–0.9 against 0.857 from Bishop on the same pore pressure; at 20000 s, 0.9–0.95 against 0.918. Largest gap between the bracket midpoint and Bishop: 2.5%. The slope that stands dry (FS 1.369) fails on rapid drawdown, and draining restores only part of its strength in this time.**

:::info At a glance

| | |
| --- | --- |
| Dimension | 2D |
| Build | `make ndims=2` from the poromechanics source |
| Inputs | [drawdown.zip](/downloads/poromechanics/drawdown.zip) |
| Checked with | DynEarthSol `97f9794` (poromechanics branch) |

:::

## Problem setup

![Setup](./img/drawdown/setup.png)

**Slope.** The embankment of the strength-reduction page ($H=10$ m, 2:1, $c=10$ kPa, $\phi=20^\circ$, $\psi=0$), saturated: porosity 0.3, saturated unit weight $20\ \mathrm{kN/m^3}$, $k=10^{-13}\ \mathrm{m^2}$, Gardner retention ($\alpha=2.4\times10^{-4}$ Pa$^{-1}$), Bishop $\chi=S_e$.

**Reservoir.** Water stands at the crest. DES loads the face and the toe platform with its pressure, and the slope fills through the crest and the base until its pore pressure is hydrostatic.

**Drawdown.** At $t=0$ the reservoir drops to the toe platform: the water load is removed, the face and the toe platform drain at $p=0$, and the crest and base are sealed. DES computes the undrained response and the drainage that follows.

**What is compared.** At several times, the DES factor of safety by strength reduction (pore pressure held during each trial) against Bishop’s simplified method on the pore pressure and unit weight DES has then.

## Input and how to run

Every file this example needs is in [drawdown.zip](/downloads/poromechanics/drawdown.zip). Run from that folder:

```bash
# Optional: meshes slope.poly at 1 m (crest marked separately from the face) and writes the unstressed, gravity-free state as seed frame 0.
dynearthsol2d seed.cfg
# Optional: restarts from seed frame 0 with gravity and the reservoir at the crest: the face and toe platform carry the water load, and the slope fills through the crest (p = 0) and the base (hydrostatic pressure) for 25000 s, writing reservoir frames 0–100 with checkpoints. The shipped reservoir.chkpt.000100, reservoir.save.000100 and reservoir.info are this result, so both optional stages can be skipped.
dynearthsol2d reservoir.cfg
# The drawdown (same as drawdown.cfg): restarts from reservoir frame 100, removes the water load, drains the face and toe platform at p = 0 and seals the crest and base, then runs 20000 s of drainage. Writes drawdown frames 101–180, one every 250 s, each with a checkpoint for the trials.
dynearthsol2d input.cfg
# A strength-reduction trial at one time after drawdown, here F = 0.85 at 250 s. In the copy set: sim.modelname to a new name (srf250-0.850); restarting_from_modelname = drawdown and restarting_from_frame = 101 (250 s; frames 104, 112, 124, 148 and 180 are 1000, 3000, 6000, 12000 and 20000 s); max_time_in_yr to that frame's time in drawdown.info (third column, s) plus 2000 s, divided by 31556926 (DES’s year, 365.2422 days); output_time_interval_in_yr = 3.168876453507857e-07 (10 s); checkpoint_frame_interval = 100000; rheology_type = elasto-plastic; hydraulic_perm = [1e-25] and fluid_bulk_modulus = [1000.0], which hold the pore pressure during the trial; cohesion0 and cohesion1 = 10000/F Pa; friction_angle0 and friction_angle1 = atan(tan 20°/F) in degrees.
cp input.cfg trial.cfg
# Runs the trial for 2000 s of mass-scaled time. Judge it from the velocity history: if the peak nodal speed over the last frames is below that about three quarters through the run, the slope is coming to rest and F is below the factor of safety; otherwise it is sliding. Repeat with other F to bracket the factor of safety at that time.
dynearthsol2d trial.cfg
```

### Settings that define this example

| Setting | Value | What it does here |
| --- | --- | --- |
| `sim.restarting_from_modelname` | `reservoir` | starts from the filled reservoir state written by reservoir.cfg |
| `sim.restarting_from_frame` | `100` | uses reservoir frame 100, the slope with hydrostatic pore pressure under the full reservoir |
| `sim.max_time_in_yr` | `0.001425994510149279 yr = 45000 s` | end time counted from the start of the reservoir stage: 25000 s of filling plus 20000 s of drainage |
| `sim.checkpoint_frame_interval` | `1` | writes a restart checkpoint with every frame, so a strength-reduction trial can start at any saved time |
| `control.has_hydraulic_diffusion` | `true` | turns on Darcy flow, so the slope drains through the face after drawdown |
| `bc.has_water_loading` | `no` | removes the reservoir's pressure on the face and toe platform (it is on in reservoir.cfg) |
| `bc.hbc_z1` | `2` | drains the face and toe platform: pore pressure held at 0 (the crest is marked as a separate boundary in slope.poly and stays sealed) |
| `mat.retention_model` | `[3]` | Gardner exponential retention, so the slope desaturates where the pressure turns negative |
| `mat.retention_alpha` | `[0.00024]` | Gardner parameter: how quickly saturation falls with suction |
| `mat.residual_saturation` | `[0.05]` | saturation left at high suction |
| `mat.hydraulic_perm` | `[1e-13]` | permeability; drainage takes thousands of seconds, slow against the mass-scaled mechanics |
| `mat.bulk_modulus_s` | `[1e20]` | incompressible grains (with Biot coefficient 1) |
| `mat.rho0` | `[2483.9085481287316]` | grain density chosen so the saturated unit weight is 20 kN/m³ |
| `mat.rheology_type` | `elastic` | elastic during drainage; each trial switches to Mohr–Coulomb elasto-plasticity |

[input.cfg](/downloads/poromechanics/drawdown/input.cfg) holds all 58 settings that differ from DES’s defaults; `dynearthsol2d -h` lists every option with its default.

## Output

DES writes `drawdown.info` (one line per saved frame: frame, step, time in seconds), `drawdown.save.NNNNNN` (the fields of each saved frame) and `drawdown.chkpt.NNNNNN` (checkpoints to restart from). `sim.output_step_interval` and `sim.output_time_interval_in_yr` set how often a frame is saved.

Set `DES_SOURCE` and `PYTHONPATH` as described in [Running the examples](../../benchmarks/poromechanics/running.md) before using the Python reader or converter.

| Field | What to look at |
| --- | --- |
| `pore pressure` | pressure (and suction above the zero contour) at each saved time after drawdown; panel (a) and the input to Bishop's method |
| `velocity` | in a trial, integrated in time it gives the displacement of the mechanism in panel (c); its peak over the mesh decides rest or sliding |
| `coordinate` | node positions of the fixed mesh, for the maps and for interpolating the pore pressure on Bishop's slices |

Read a frame in Python:

```python
from Dynearthsol import Dynearthsol      # in the DES source folder
model = Dynearthsol('drawdown')
frame = model.frames[-1]                 # model.time[i] is the time of frame i, in seconds
x = model.read_field(frame, 'coordinate')
value = model.read_field(frame, 'pore pressure')
```

View it in ParaView after `python3 "$DES_SOURCE/2vtk.py" -g drawdown`.

## Result: DES and the analytical solution

![Result](./img/drawdown/result.png)

(a) Pore pressure at the first comparison time after drawdown, with the zero-pressure contour and Bishop's critical circle on the same pore pressure. (b) Factor of safety against time after drawdown: Bishop's method on the DES pore pressure (line and circles) and the DES strength-reduction bracket, from the last F at rest to the first F sliding (bars). (c) Displacement in the first sliding trial at the first comparison time, with Bishop's circle.

This joins the verified pieces in the problem dam engineers check first: the undrained response to unloading, unsaturated drainage and effective-stress plasticity. Limit equilibrium needs the pore pressure as an input; DES computes it and finds the mechanism.

To reproduce the whole study behind this figure, from the DES source folder:

```bash
python3 benchmarks/poromechanics/drawdown_slope.py dynearthsol2d OUT --spacings 1
```

The study’s full numbers: [record.json](/downloads/poromechanics/drawdown/record.json).

## Analytical reference

$$
FS=\frac{\sum\left[c\,b+(W-\chi p\,b)\tan\phi\right]/m_\alpha}{\sum W\sin\alpha}
$$

$$
m_\alpha=\cos\alpha\left(1+\frac{\tan\alpha\tan\phi}{FS}\right)
$$

$$
W=b\int_{z_b}^{z_s}\gamma\,dz
$$

$$
\gamma=g\left[\rho_s(1-n)+\rho_f\,n\,S\right]
$$

$p$ and $S$ are DES’s pore pressure and saturation at that time, $\chi=S_e$ (Bishop), $n$ the porosity; the other symbols are those of the strength-reduction page.

### Derivation

Before drawdown the reservoir’s pressure on the face balances the pore pressure inside: only buoyant weight drives sliding. Removing the water removes that support at once, and the undrained response lowers the pore pressure by about the removed load; the remaining pressure then drains through the face. The factor of safety is lowest just after drawdown and recovers as the slope drains.

A strength-reduction trial holds the pore pressure: no flow, and a compressible pore fluid so that deformation does not change it. With a stiff fluid the trial would be undrained and excess pore pressure of order 10 kPa would lower the factor of safety below limit equilibrium.

Morgenstern (1963), Géotechnique 13(2), 121–131 (stability charts for rapid drawdown); Bishop (1955), Géotechnique 5(1), 7–17.

## Validity and limits

No exact solution: Bishop’s method needs the pore pressure as an input, here taken from DES, so the comparison checks the mechanics given the hydraulics. 2D, small strain; drawdown is instantaneous; the earliest comparison is a few hundred seconds after drawdown, once the mass-scaled mechanics has settled.

## Reproduction

[Commands, solver hashes and portable inputs](../../benchmarks/poromechanics/running.md).
