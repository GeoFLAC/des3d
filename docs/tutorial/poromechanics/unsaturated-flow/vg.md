---
sidebar_position: 1
title: "Steady infiltration: van Genuchten law"
---
# Steady infiltration: van Genuchten law

A constant inflow from the top produces a steady suction profile above a water table at the base. The van Genuchten law has no air-entry pressure, so the soil desaturates as soon as the pressure falls below zero.

**Largest pressure error: 5.69 Pa, 0.96% of the profile range.**

:::info At a glance

| | |
| --- | --- |
| Dimension | 2D |
| Build | `make ndims=2` from the poromechanics source |
| Inputs | [vg.zip](/downloads/poromechanics/vg.zip) |
| Checked with | DynEarthSol `97f9794` (poromechanics branch) |

:::

## Problem setup

![Setup](../img/vg/setup.png)

**Water boundaries.** Constant downward inflow $I=1.38889\times10^{-6}$ m/s at the top. Base pressure zero; sides sealed.

**Retention law.** Pressure-based $\alpha_p=5\times10^{-4}$ Pa$^{-1}$, $n=2$, residual saturation $S_r=0.1$. Gravity points downward.

**Mechanical conditions and comparison.** Side-normal displacement and base vertical displacement fixed; traction-free top. Start hydrostatic and compare the final steady pressure profile.

## Input and how to run

Every file this example needs is in [vg.zip](/downloads/poromechanics/vg.zip). Run from that folder:

```bash
# Runs the 2D column with fixed 300 s steps for about 23 days (2e6 s), long enough to reach the steady profile. DES writes column.save.* at the start, halfway and at the end; the page compares the last frame.
dynearthsol2d input.cfg
```

### Settings that define this example

| Setting | Value | What it does here |
| --- | --- | --- |
| `control.has_hydraulic_diffusion` | `true` | turns on Darcy flow, here partly saturated (Richards) flow |
| `control.has_PT` | `true` | PT solver: mechanical equilibrium is reached by iteration within each step |
| `control.gravity` | `9.81` | gravity drives the downward flow and sets the hydrostatic start |
| `sim.max_time_in_yr` | `0.06337752907015713 yr = 2e+06 s` | about 2e6 s in fixed 300 s steps, long enough for the column to reach steady state |
| `sim.output_time_interval_in_yr` | `0.031688764535078566 yr = 1e+06 s` | a frame halfway and one at the end |
| `bc.hbc_z0` | `2` | type 2: the base is held at the pressure in bc.hbc_pressure, here 0, the water table |
| `bc.hbc_z1` | `3` | type 3: the top has the prescribed flux in bc.hbc_flux |
| `bc.hbc_flux` | `[0,0,0,0,0,-1.388888888888889e-06]` | outward Darcy flux per face; the top value −1.389e-6 m/s is an inflow of half the saturated conductivity |
| `ic.water_table_z` | `-1.0` | starts hydrostatic with the water table at the base (z = −1 m) |
| `mat.retention_model` | `[1]` | 1: van Genuchten retention with Mualem relative permeability (n is retention_n, default 2) |
| `mat.retention_alpha` | `[5e-4]` | pressure-based retention parameter α_p = 5e-4 1/Pa |
| `mat.residual_saturation` | `[0.1]` | residual saturation S_r = 0.1 |
| `mat.fluid_bulk_modulus` | `[40000.0]` | deliberately small (4e4 Pa) to allow a larger stable flow step; storage does not affect the steady profile |
| `mat.hydraulic_perm` | `[2.8372409106354064e-13]` | gives saturated conductivity K_s = 2.78e-6 m/s (1 cm/h) |

[input.cfg](/downloads/poromechanics/vg/input.cfg) holds all 53 settings that differ from DES’s defaults; `dynearthsol2d -h` lists every option with its default.

## Output

DES writes `column.info` (one line per saved frame: frame, step, time in seconds), `column.save.NNNNNN` (the fields of each saved frame) and `column.chkpt.NNNNNN` (checkpoints to restart from). `sim.output_step_interval` and `sim.output_time_interval_in_yr` set how often a frame is saved.

Set `DES_SOURCE` and `PYTHONPATH` as described in [Running the examples](../running.md) before using the Python reader or converter.

| Field | What to look at |
| --- | --- |
| `pore pressure` | the steady pressure profile at the last frame, compared with the reference |
| `coordinate` | the height of each node above the base |

Read a frame in Python:

```python
from Dynearthsol import Dynearthsol      # in the DES source folder
model = Dynearthsol('column')
frame = model.frames[-1]                 # model.time[i] is the time of frame i, in seconds
x = model.read_field(frame, 'coordinate')
value = model.read_field(frame, 'pore pressure')
```

View it in ParaView after `python3 "$DES_SOURCE/2vtk.py" column`.

## Result: DES and the analytical solution

![Result](../img/vg/result.png)

Steady pressure (kPa) against height above the water table at the end of the run: DES nodes (circles) and the steady-infiltration reference for the van Genuchten–Mualem law (line).

This checks the retention-dependent conductivity and the flux boundary. It does not test transient storage or coupled slope behaviour.

To reproduce the whole study behind this figure, from the DES source folder:

```bash
python3 tests/functional/hydromechanics/check_unsaturated_column.py dynearthsol2d OUT
```

The study’s full numbers: [record.json](/downloads/poromechanics/vg/record.json).

## Analytical reference

$$
s=\max(-p,0),\quad m=1-1/n,\quad S_e=[1+(\alpha_p s)^n]^{-m},\quad S=S_r+(1-S_r)S_e
$$

$$
k_r=S_e^{1/2}\left[1-(1-S_e^{1/m})^m\right]^2
$$

$$
J=I/K_s,\quad \gamma=\rho_fg,\quad \frac{dp}{dz}=\gamma\left(\frac{J}{k_r(p)}-1\right),\quad p(0)=0
$$

$$
z=\frac{1}{\gamma}\int_{p(z)}^0\frac{k_r(\xi)}{k_r(\xi)-J}\,d\xi
$$

Elevation $z$ runs upward from the water-table base. $I$ is positive downward infiltration, $K_s=\kappa\rho_f g/\mu$ saturated hydraulic conductivity, $J=0.5$ and $\gamma=9810\ \mathrm{Pa/m}$. The integral is an implicit analytical relation, evaluated by high-accuracy integration of its equivalent first-order ODE.

### Derivation

At steady state $q_z=-I$ is constant. Darcy flow with $z$ upward includes both pressure and gravity. Rearranging and separating variables gives the integral shown above, starting from $p=0$ at $z=0$.

$$
-I=-\frac{\kappa k_r(p)}{\mu}(p_z+\gamma),\quad dz=-\frac{k_r(p)}{\gamma[k_r(p)-J]}\,dp
$$

For $0<J<1$ the pressure decreases with elevation toward the suction at which $k_r=J$. The integral diverges at that limiting pressure. Storage and elastic compressibility do not enter this steady relation. The analytical relation is evaluated with an independent high-accuracy ODE solver; no DES output or fitting parameter is used.

The implicit relation is derived from steady Darcy flow; evaluated by DOP853 (rtol 10⁻¹², atol 10⁻⁹ Pa) in unsaturated_reference.py.

## Validity and limits

Homogeneous, steady one-dimensional flow, constant gravity and prescribed flux. This is not a closed-form pressure profile. Storage drops out of the steady equation; the deliberately reduced fluid modulus shortens the run (a larger stable flow step) and does not test transient storage.

## Reproduction

[Commands, solver hashes and portable inputs](../running.md).
