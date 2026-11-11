---
sidebar_position: 4.5
slug: /theory/rheology
title: Rheology
description: The material laws DES offers, how each updates the stress, the power-law creep viscosity, strain softening, the tension cut-off and how materials mix in an element.
---

# Rheology

Each element carries one rheology, chosen for the whole model by
`mat.rheology_type`, and per-material parameters given as lists, one value
per material. This page gives the laws and their parameters. How the stress
is integrated over a time step, the visco-elastic update and the
Mohr–Coulomb return, is in [Constitutive update](./solution-scheme/constitutive.md).

Sign convention: stress and strain are positive in tension. In 2D the
strain and stress have the components $xx$, $zz$ and $xz$.

## The rheologies

| `rheology_type` | Stress update |
| --- | --- |
| `elastic` | linear elasticity |
| `viscous` | linear viscous flow, with incompressibility enforced by the bulk modulus (experimental) |
| `maxwell` | elastic and viscous in series |
| `elasto-plastic` | elasticity with Mohr–Coulomb plasticity |
| `elasto-visco-plastic` | Maxwell or elasto-plastic, whichever gives the smaller stress |
| `elasto-plastic-rate-state-friction` | elasto-plastic, with the friction coefficient from [rate-and-state friction](./rate-state-friction.md) |
| `elasto-visco-plastic-rate-state-friction` | elasto-visco-plastic, with rate-and-state friction |

Short aliases ending in `-rsf` are accepted for the last two.

## Elasticity

The stress increment from a strain increment $\Delta\boldsymbol\varepsilon$ is

$$
\Delta\sigma_{ij} = 2G\,\Delta\varepsilon_{ij} + \lambda\,\Delta\varepsilon_{kk}\,\delta_{ij},
\qquad \lambda = K - \tfrac{2}{3}G,
$$

with the bulk modulus $K$ (`mat.bulk_modulus`) and shear modulus $G$
(`mat.shear_modulus`). With pore-fluid flow the update acts on the effective
stress; see [Poromechanics](./poromechanics.md).

In 2D, `mat.is_plane_strain = yes` keeps the out-of-plane strain at zero and
tracks the out-of-plane stress $\sigma_{yy}$, which then enters the plastic
yield test. Without it, the 2D update uses only the in-plane components.

## Viscous flow and the creep law

`viscous`, `maxwell` and the visco-plastic rheologies take their viscosity
from a power-law creep law (Chen & Morgan, 1990):

$$
\eta = \tfrac{1}{4}\,\dot\varepsilon_{II}^{\,1/n - 1}
\left(\tfrac{3}{4}A\right)^{-1/n}
\exp\!\left(\frac{E + V\sigma_m}{nRT}\right)\times 10^{6}\ \text{Pa s},
$$

where

| Symbol | Meaning | Parameter |
| --- | --- | --- |
| $n$ | stress exponent | `mat.visc_exponent` |
| $A$ | pre-exponential coefficient, in MPa$^{-n}$ s$^{-1}$ | `mat.visc_coefficient` |
| $E$ | activation energy, J/mol | `mat.visc_activation_energy` |
| $V$ | activation volume, m³/mol | `mat.visc_activation_volume` |
| $\dot\varepsilon_{II}$ | second invariant of the strain rate, at least $10^{-30}$ s⁻¹ | |
| $\sigma_m$ | mean stress, $\mathrm{tr}\,\boldsymbol\sigma/N_{dim}$, positive in tension | |
| $T$ | element temperature, the mean of its nodes, K | |
| $R$ | 8.3144 J/mol/K | |

The factor $10^6$ converts MPa s to Pa s. Because $\sigma_m$ is positive in
tension, compression ($\sigma_m < 0$) lowers the viscosity when $V > 0$; the
common form $\exp[(E + PV)/(nRT)]$ with pressure $P = -\sigma_m$ corresponds
to entering $-V$ here. The result is clipped to
[`mat.min_viscosity`, `mat.max_viscosity`] (defaults $10^{18}$ and
$10^{24}$ Pa s). A constant viscosity is obtained with
`min_viscosity = max_viscosity`, as in the
[Maxwell benchmark](../benchmarks/mechanics/maxwell.md).

The `viscous` rheology sets the deviatoric stress to
$2\eta\,\mathrm{dev}(\dot{\boldsymbol\varepsilon})$ and the mean stress to
$K$ times the volumetric strain. `maxwell` integrates elastic and viscous
deformation in series over the step; its relaxation time is $\eta/G$.

## Plasticity

`elasto-plastic` limits the stress by the Mohr–Coulomb shear criterion and a
tension cut-off,

$$
f_s = \sigma_1 - N_\phi\,\sigma_3 + 2c\sqrt{N_\phi},\qquad
f_t = \sigma_3 - \sigma_t,\qquad
N_\phi = \frac{1 + \sin\phi}{1 - \sin\phi},
$$

with $\sigma_1 \le \sigma_2 \le \sigma_3$ the principal stresses (so
$\sigma_1$ is the most compressive), cohesion $c$ and friction angle
$\phi$. The stress is admissible while $f_s \ge 0$ and $f_t \le 0$. Plastic
flow in shear follows the dilation angle $\psi$ through
$N_\psi = (1 + \sin\psi)/(1 - \sin\psi)$, which may differ from $\phi$
(non-associated flow). The tension cut-off is

$$
\sigma_t = \min\!\left(\texttt{mat.max\_tension},\ \frac{c}{\tan\phi}\right),
$$

or `max_tension` alone when $\phi = 0$. The return to the yield surface,
including the edge where two shear faces meet, is described in
[Constitutive update](./solution-scheme/constitutive.md).

### Strain softening

Cohesion, friction angle and dilation angle change linearly with the
accumulated plastic strain $\varepsilon_p$ between two values:

$$
c(\varepsilon_p) = \begin{cases}
c_0, & \varepsilon_p < \varepsilon_{p0}\\[2pt]
c_0 + \dfrac{\varepsilon_p - \varepsilon_{p0}}{\varepsilon_{p1} - \varepsilon_{p0}}\,(c_1 - c_0), & \varepsilon_{p0} \le \varepsilon_p < \varepsilon_{p1}\\[8pt]
c_1, & \varepsilon_p \ge \varepsilon_{p1}
\end{cases}
$$

and likewise for $\phi$ and $\psi$. The parameters are `mat.pls0` and
`mat.pls1` ($\varepsilon_{p0}$, $\varepsilon_{p1}$), `mat.cohesion0` and
`mat.cohesion1`, `mat.friction_angle0` and `mat.friction_angle1`, and
`mat.dilation_angle0` and `mat.dilation_angle1` (degrees). Equal start
and end values give a material without softening. Softening is what lets a
brittle layer localize into shear bands; see the
[shear-band benchmark](../benchmarks/geodynamics/localization.md).

## Elasto-visco-plastic

`elasto-visco-plastic` computes both a Maxwell stress and an elasto-plastic
stress from the same strain increment and keeps the one with the smaller
second invariant. Cold, strong regions are therefore limited by
plasticity and hot, weak regions by viscous creep, with no separate switch.
Plastic strain accumulates only in elements that take the elasto-plastic
stress.

## Several materials in one element

Each element records how many markers of each material it holds. Its
properties are marker-weighted means. The viscosity and the bulk and shear
moduli are harmonic means, for example

$$
\frac{1}{\eta_e} = \sum_m \frac{w_m}{\eta_m},
$$

where $w_m$ is the fraction of the element's markers of material $m$. The
strength parameters (cohesion, friction and dilation angles), the heat
capacity and the thermal conductivity are arithmetic means. The harmonic
mean lets a weak material control an element it shares with a strong one.

## Parameters

| Parameter | Meaning | Default |
| --- | --- | --- |
| `mat.rheology_type` | rheology, see the table above | required |
| `mat.num_materials` | number of materials; lists take one value per material | 1 |
| `mat.bulk_modulus`, `mat.shear_modulus` | $K$, $G$ (Pa) | [128.2e9], [80.5e9] |
| `mat.visc_exponent`, `mat.visc_coefficient` | $n$, $A$ | [3.05], [1.25e-1] |
| `mat.visc_activation_energy`, `mat.visc_activation_volume` | $E$, $V$ | [3.76e5], [0] |
| `mat.min_viscosity`, `mat.max_viscosity` | viscosity limits (Pa s) | 1e18, 1e24 |
| `mat.pls0`, `mat.pls1` | plastic strain where softening starts and ends | [0], [0.1] |
| `mat.cohesion0`, `mat.cohesion1` | cohesion before and after softening (Pa) | [4e7], [4e6] |
| `mat.friction_angle0`, `mat.friction_angle1` | friction angle (°) | [30], [5] |
| `mat.dilation_angle0`, `mat.dilation_angle1` | dilation angle (°) | [0], [0] |
| `mat.max_tension` | upper limit of the tension cut-off (Pa) | 1e9 |
| `mat.is_plane_strain` | plane-strain update in 2D | no |

Most models set their own values. All parameters are listed in the
[parameter reference](../reference/parameters.md).

## Reference

Chen, Y., & Morgan, W. J. (1990). A nonlinear rheology model for mid-ocean
ridge axis topography. *Journal of Geophysical Research*, 95(B11),
17583–17604.
