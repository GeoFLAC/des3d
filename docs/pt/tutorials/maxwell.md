---
sidebar_position: 2
slug: /tutorial/pt-maxwell
title: Maxwell creep under a held load
description: Compare continued physical creep with an independent discrete Maxwell reference using both PT schemes.
---

# Maxwell creep under a held load

The [elastic tutorial](./elastic.md) reaches equilibrium after the load is
applied and then holds its strain. A Maxwell material continues to creep:
its deviatoric stress relaxes over physical time, and additional deformation
is needed to maintain the prescribed traction. This exercise checks that
PT retains that time-dependent response.

Use the same checked solver, Python environment, single-thread settings,
and [tutorial bundle](/tutorial/pt/pt-tutorial.zip) as the elastic exercise.
Run the commands below from `DynEarthSol-pt-tutorial/pt-tutorial`.

## Change the material, keep the loading

`maxwell-0.cfg` and `maxwell-1.cfg` retain the 1 m cell, roller sides,
clamped base and $-100$ kPa top traction. They run 100 steps of 0.01 s
with a fixed mesh and no hydraulic diffusion. The material settings are:

```cfg
[mat]
rheology_type = maxwell
is_plane_strain = yes
rho0 = [2650]
porosity = [0]
bulk_modulus = [1e7]
shear_modulus = [1e7]
min_viscosity = 1e6
max_viscosity = 1e6
```

Both viscosity bounds fix $\eta=10^6$ Pa s. In 2D,
`is_plane_strain = yes` retains the out-of-plane normal stress in the 3D
constitutive state with zero out-of-plane strain. In 3D the setting has no
effect. The shear relaxation time is $\eta/G=0.1$ s, so the run spans ten
shear relaxation times. As in the elastic tutorial, these configs explicitly
enable the optional running scale; that small-model check does not qualify
its use for general viscous flow.

## Run and compare

```bash
../dynearthsol2d maxwell-0.cfg > maxwell-0.log 2>&1
../dynearthsol2d maxwell-1.cfg > maxwell-1.log 2>&1
python analyze_pt.py maxwell maxwell-0 maxwell-1 --source ..
```

The script checks every component of stress, strain, coordinates and
velocity for finiteness in each saved frame, then compares axial stress,
axial strain and vertical velocity against the independent discrete reference
below. It writes one CSV per model and `maxwell-response.svg/.png`. The checked 2D runs have
maximum normalized field errors below $2.2\times10^{-6}$, within the
script's $5\times10^{-5}$ limit. Normalizers are 100 kPa for stress,
0.01 for strain and 0.5 m/s for velocity.

![Both PT options maintain the imposed stress while Maxwell compression continues over physical time.](/tutorial/pt/maxwell-response.svg)

The axial stress stays near $-100$ kPa. The axial strain continues beyond
the first step, reaching about **−0.00991968 at 1 s**, or 9.920 mm equivalent
shortening. Coordinates remain fixed; the script integrates the top
velocity to reconstruct displacement.

## Independent discrete reference

For homogeneous confined compression, let $e_n=\epsilon_{zz,n}$,
$m_n=K e_n$ be the signed mean normal stress, and $s_n$ the axial
deviatoric stress, so $\sigma_{zz,n}=m_n+s_n$. Start with
$e_0=m_0=s_0=0$. For the prescribed axial traction $T=-10^5$ Pa, define

$$
a=\frac{G\Delta t}{2\eta},\qquad
q=\frac{1-a}{1+a},\qquad
D=\frac{4G}{3(1+a)}.
$$

Crank–Nicolson integration of the Maxwell deviatoric response gives

$$
\Delta e_n=\frac{T-m_{n-1}-q s_{n-1}}{K+D},\qquad
m_n=m_{n-1}+K\Delta e_n,
$$

$$
s_n=q s_{n-1}+D\Delta e_n,\qquad
e_n=e_{n-1}+\Delta e_n.
$$

These are algebraic homogeneous equations, independent of the mesh force
assembly. The analysis script implements this recurrence and checks all
elements, rather than using one PT option as the reference for the other.

This is a check against the **discrete material update** at the selected
physical timestep. Agreement does not establish physical-time convergence.
For the corresponding continuum step-load problem, the post-loading strain
is

$$
e(t)=\frac{T}{K}\left[1-
 \frac{4G/3}{K+4G/3}\exp\left(-\frac{t}{\tau_c}\right)\right],
\qquad \tau_c=\frac{\eta}{G}\frac{K+4G/3}{K}.
$$

The instantaneous elastic jump is $T/(K+4G/3)$; the long-time strain is
$T/K=-0.01$. The first saved DES step includes a finite interval of creep,
so it is not exactly that instantaneous jump. A timestep-refinement study
against this continuum solution is a separate accuracy assessment. The
provided plotting script expects the supplied 100-step, 0.01 s configs.

## What this demonstrates

The held elastic and Maxwell runs test different physical responses.
For elasticity, zero free velocity can preserve a completed loading
increment. For Maxwell rheology, the same candidate still evaluates
constitutive relaxation over the physical dt; a zero-velocity shortcut
cannot suppress creep. Both PT schemes must recover the discrete history.

For the matching 3D exercise, use the 3D build and a fresh output directory
as described in the [elastic tutorial](./elastic.md#repeat-in-3d-or-continue-to-creep).
The same inputs and analysis script apply.

These homogeneous, dry, fixed-grid checks do not qualify moving meshes,
localized softening, arbitrary irreversible loading or hydraulic coupling.
For solver controls and known convergence limits, return to
[Choosing a mechanical solver](../index.md) and the
[validation record](https://github.com/GeoFLAC/DynEarthSol/blob/master/doc/pt-validation-20261006.md).
