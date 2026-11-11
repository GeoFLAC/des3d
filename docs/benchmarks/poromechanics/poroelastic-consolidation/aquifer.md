---
sidebar_position: 5
title: "Pumping subsidence: averaged-aquifer (Bear–Corapcioglu) model"
---
# Pumping subsidence: averaged-aquifer (Bear–Corapcioglu) model

A well pumps a thin poroelastic aquifer. The drawdown spreads radially and the layer contracts, splitting its volume change between areal and vertical strain.

**RMS errors: 0.71% in pressure, 1.97% in areal strain and 1.90% in vertical strain, relative to the largest analytical values.**

:::info At a glance

| | |
| --- | --- |
| Dimension | 3D |
| Build | `make ndims=3` from the poromechanics source |
| Inputs | [aquifer.zip](/downloads/poromechanics/aquifer.zip) |
| Reproduce with | DynEarthSol [`3774df0`](https://github.com/GeoFLAC/DynEarthSol/tree/3774df00ba1708a4f70a836d2073f845653aac64) |

:::

## Problem setup

![Setup](../img/aquifer/setup.png)

**DES slab.** A thin quarter slab, $400\times400$ m and $B=10$ m thick, with a fully penetrating well on its corner edge pumping $Q/4$ ($Q=0.01\ \mathrm{m^3/s}$). Symmetry rollers at $x=0$, $y=0$, a roller base and a traction-free top; the far sides hold the initial pressure and zero normal displacement.

**Reference.** The thickness-averaged (generalised Bear–Corapcioglu) model: vanishing incremental vertical and vertical-shear total stress, horizontal displacement uniform through the thickness. It applies while the slab is thin compared with the radius, up to $O((B/r)^2)$.

**What is compared.** Nodal pressure and element areal and vertical strains for $15\le r\le120$ m at four times, while the pressure front stays inside the slab, on structured meshes.

## Input and how to run

Every file this example needs is in [aquifer.zip](/downloads/poromechanics/aquifer.zip). Run from that folder:

```bash
# Runs the 3D quarter slab on a 5 m hexahedral mesh: the corner well pumps from t = 0 and DES writes frames slab.* at 0, 2500, 5000, 7500 and 10000 s. No mesh or restart file is needed.
dynearthsol3d input.cfg
```

### Settings that define this example

| Setting | Value | What it does here |
| --- | --- | --- |
| `control.has_hydraulic_diffusion` | `true` | turns on Darcy flow, so the drawdown spreads from the well by diffusion |
| `control.has_PT` | `true` | iterates each time step to mechanical equilibrium, so the slab deforms quasi-statically with the pressure (two-way Biot coupling) |
| `control.gravity` | `0` | no gravity: every field is a change from the unstressed, zero-pressure initial state |
| `control.has_moving_mesh` | `false` | keeps the mesh fixed (small strain), as the reference assumes |
| `mesh.meshing_elem_shape` | `1` | structured hexahedra, so the mesh spacing follows mesh.resolution exactly |
| `bc.vbc_y0` | `1` | symmetry plane y = 0: normal displacement fixed (the x = 0 plane is a roller by default) |
| `bc.vbc_z0` | `1` | roller base: vertical displacement fixed, horizontal free; the top is traction-free |
| `bc.hbc_x1` | `1` | far side x = 400 m holds its initial pore pressure (zero change) |
| `bc.hbc_y1` | `1` | far side y = 400 m holds its initial pore pressure (zero change) |
| `bc.num_wells` | `1` | one rate-controlled vertical well, placed on the corner edge x = y = 0 |
| `bc.well_rate` | `[0.0025]` | extraction rate of the quarter well: one quarter of the full rate Q, because the model is one quarter of the slab |
| `bc.well_z_bottom` | `[-10.0]` | screens the well over the whole 10 m thickness (fully penetrating) |
| `mat.hydraulic_perm` | `[1e-12]` | permeability; with fluid viscosity and storage it sets the hydraulic diffusivity |
| `mat.biot_coeff` | `[0.8]` | Biot coefficient, the strength of the pressure–deformation coupling |

[input.cfg](/downloads/poromechanics/aquifer/input.cfg) holds all 44 settings that differ from DES’s defaults; `dynearthsol3d -h` lists every option with its default.

## Output

See [Running the examples](../running.md) for output files, the Python reader and ParaView conversion.

| Field | What to look at |
| --- | --- |
| `pore pressure` | nodal pressure change against radius from the well at each saved time; panel (a) and the pressure error |
| `strain` | element strain tensor: the areal strain is the xx + yy components and the vertical strain the zz component; panel (b) and the strain errors |
| `coordinate` | node positions, used for the radius of nodes and element centres from the well |


## Result: DES and the analytical solution

![Result](../img/aquifer/result.png)

(a) Pressure drop against distance from the well at the first and last saved times: lines are the averaged-aquifer line-well solution, symbols the mean DES value in radius bins with the spread shaded. (b) Areal and vertical contraction at the last time against the analytical solution, which predicts the two to be equal. (c) RMS errors in pressure, areal strain and vertical strain against mesh spacing, with a first-order slope for reference.

This checks two-way coupled pumping deformation against the thickness-averaged model. It does not remove the $O((B/r)^2)$ slab-model difference, which remains at the finest mesh.

To reproduce the whole study behind this figure, from the DES source folder:

```bash
python3 benchmarks/poromechanics/slab_refinement.py dynearthsol3d OUT --resolutions 20 10 5
```

The study’s full numbers: [record.json](/downloads/poromechanics/aquifer/record.json).

## Analytical reference

$$
\lambda=K-2G/3,\quad S_a=S_0+\alpha^2/(\lambda+G),\quad D=\kappa/(\mu S_a)
$$

$$
C_Q=Q\mu/(4\pi\kappa B),\quad u=r^2/(4Dt),\quad p(r,t)=-C_QE_1(u)
$$

$$
e_h=\epsilon_{zz}=\frac{\alpha p}{2(\lambda+G)},\quad\delta=-B\epsilon_{zz}
$$

$$
U_r=-\frac{\alpha C_QDt}{(\lambda+G)r}[uE_1(u)-e^{-u}+1]
$$

$p$ is the pressure change (negative during extraction), $S_a$ is pressure storage in $\mathrm{Pa^{-1}}$, $S_0=\phi/K_f+(\alpha-\phi)/K_s$, $e_h=\epsilon_{xx}+\epsilon_{yy}$ is areal strain, and $\delta$ is positive downward subsidence. The plotted reference is the infinite-domain line-well limit. The full finite-annulus Laplace solution, which includes an additional spatially uniform strain function $h(t)$, is derived below.

### Finite-annulus derivation

Thickness averaging assumes zero incremental vertical stress and negligible
vertical shear. Eliminating vertical strain gives the plane-stress Lamé
coefficient and uniform radial equilibrium function $h(t)$:

$$
\lambda_*=\frac{2G\lambda}{\lambda+2G},\qquad
\varepsilon_{zz}=\frac{\alpha p-\lambda e_h}{\lambda+2G},
$$

$$
e_h=\frac{\alpha p}{2(\lambda+G)}+h(t),\qquad
\varepsilon_v=\frac{\alpha p}{\lambda+G}+\frac{2Gh}{\lambda+2G}.
$$

Integrating areal strain and substituting fluid content give

$$
rU_r=C_w+\frac{\alpha}{2(\lambda+G)}
\int_{r_w}^{r}\rho p(\rho,t)\,d\rho+\frac{h}{2}(r^2-r_w^2),
$$

$$
\zeta=S_ap+ch,\qquad c=\frac{2G\alpha}{\lambda+2G},
$$

$$
S_a\dot p+c\dot h=(\kappa/\mu)\nabla_r^2p.
$$

The well has finite radius $r_w$, with prescribed total extraction rate
$2\pi r_wB(\kappa/\mu)p_r(r_w)=Q$. The outer hydraulic boundary is
$p(R)=0$ or no flow. Either radial mechanical boundary can fix $U_r=0$
or set $\sigma_{rr}=0$, where

$$
\sigma_{rr}=(\lambda_*+2G)h-2GU_r/r.
$$

For the fixed inner boundary $C_w=0$; for a traction-free inner boundary
$C_w=r_w^2(\lambda_*+2G)h/(2G)$. In Laplace space,

$$
\widehat p=A I_0(qr)+B_0K_0(qr)-(c/S_a)\widehat h,
\qquad q^2=sS_a\mu/\kappa.
$$

The two hydraulic conditions and outer mechanical condition form a
$3\times3$ system for $A,B_0,\widehat h$. The Bessel integral in $U_r$ is
analytic. Exponentially scaled bases avoid overflow; a fixed 32-node
Talbot inversion returns the time solution. This is the implementation in
`averaged_aquifer_reference.py`, independent of DES's discretization.
In an infinite domain $h=0$, recovering the closed forms above. A distant
fixed boundary generally gives nonzero $h$ before the pressure front
reaches it, and its strain feeds back into storage. A finite-domain
pressure therefore need not be Theis.

Independent reference checks cover radial finite volumes, sealed fluid
balance, the hydraulic/mechanical boundaries, kinematics, the line-well
limit and steady Thiem flow:

```bash
python3 tests/functional/hydromechanics/check_averaged_aquifer_reference.py -v
```

The zero-horizontal-strain alternative has storage
$S_0+\alpha^2/(\lambda+2G)$ and vertical strain
$\alpha p/(\lambda+2G)$. It is a different mechanical constraint. For a
common pressure change, the plane-stress subsidence is $(1-\nu)$ times
that value; with matching $\alpha$ and $S_0$ and both models calibrated to the same
storativity, the ratio is one half.

## Validity and limits

Linear poroelasticity with constant properties; the thin-slab geometry approaches the averaged model only up to $O((B/r)^2)$, so a small model difference remains at the finest mesh. Two-way coupling with PT; no gravity. Near-well, early-time 3D pressure rises (the Noordbergum effect) are outside the averaged model. A vertical 2D slice cannot represent radial groundwater flow together with subsidence.
