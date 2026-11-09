---
slug: /theory/poromechanics
sidebar_position: 6
---

# Poromechanics

DES3D can couple the flow of one pore fluid with deformation of the solid
skeleton. Pore pressure changes the effective stress and therefore the
strength, and deformation changes the pore pressure. Optional extensions
cover partly saturated ground, groundwater heat transport, thermal
pressurization, evolving porosity and permeability, and an immobile matrix
reservoir. Like the mechanics, every part of the update is explicit: there
is no global linear or nonlinear solve.

Hydraulics is enabled with `control.has_hydraulic_diffusion = yes`.

## Conventions

Stress and strain are positive in tension, as elsewhere in DES3D. Pore
pressure $p$ is positive in compression, so suction is $-p$. The vertical
coordinate $z$ points up, and gravity acts in $-z$. The volumetric strain is
$\varepsilon_v$ and the mean stress $\sigma_m$.

## Governing equations

### Effective stress

The skeleton responds to the effective stress
([Biot, 1941](https://doi.org/10.1063/1.1712886)):

$$
\boldsymbol\sigma' = \boldsymbol\sigma + \alpha\,p\,\mathbf I,
$$

where $\boldsymbol\sigma$ is the total stress and $\alpha$ the Biot–Willis
coefficient (`mat.biot_coeff`). With
`mat.derive_biot_coeff_from_bulk_moduli = yes`, DES3D sets
$\alpha = 1 - K/K_s$ from the drained bulk modulus $K$ (`mat.bulk_modulus`)
and the grain modulus $K_s$ (`mat.bulk_modulus_s`)
([Biot and Willis, 1957](https://doi.org/10.1115/1.4011606)).

The plastic models use the effective stress in their yield functions. A
rise in pore pressure moves the Mohr circle toward failure without changing
the deviatoric stress. The stored stress remains the total stress, which
balances the external loads.

### Fluid content

The change in fluid volume per unit bulk volume is
([Rice and Cleary, 1976](https://doi.org/10.1029/RG014i002p00227))

$$
\zeta = \alpha\,\varepsilon_v + \frac{p}{M} - \beta\,(T - T_0),
\qquad
\frac1M = \frac{\phi}{K_f} + \frac{\alpha-\phi}{K_s},
$$

with porosity $\phi$ (`mat.porosity`), fluid bulk modulus $K_f$
(`mat.fluid_bulk_modulus`) and Biot modulus $M$. The thermal term applies
only with thermal pressurization (below). Valid materials satisfy
$0 \le \phi \le \alpha \le 1$.

### Darcy flow

The Darcy flux is

$$
\mathbf q = -\frac{k_r}{\mu}\,\mathbf k\,
\left(\nabla p + \rho_f\, g\,\mathbf e_z\right),
$$

where $\mu$ is the fluid viscosity (`mat.fluid_visc`), $\rho_f$ the
reference fluid density (`mat.fluid_rho0`) and $k_r$ the relative
permeability ($k_r=1$ when saturated). The permeability tensor is the
scalar intrinsic permeability (`mat.hydraulic_perm`, m²) times a
dimensionless symmetric positive-definite tensor
(`mat.permeability_tensor = [xx,yy,zz,xy,xz,yz]`, isotropic by default). In
2D its x–z part is used. Fluid mass balance closes the system:

$$
\frac{\partial \zeta}{\partial t} + \nabla\cdot\mathbf q = Q,
$$

where $Q$ is a volumetric source from wells or point sources.

### Weight of the saturated rock

The bulk density used for gravity and inertia is the mixture

$$
\rho = (1-\phi)\,\rho_s + \phi\, S\,\rho_f ,
$$

with solid density $\rho_s$ (`mat.rho0`) and saturation $S$ ($S=1$ when
saturated). The same density loads a wet Winkler foundation. Without
hydraulics, DES3D uses the solid density alone.

## Coupling in time

Each physical step advances mechanics once and pressure over the same
interval. Which quantity drives the pressure depends on the mechanical
solver.

**Strain-driven form (explicit mechanics, including global velocity
scaling).** Pressure advances first, from the strain rate projected from
the current velocity:

$$
\frac1M\,\dot p = -\alpha\,\dot\varepsilon_v - \nabla\cdot\mathbf q + Q .
$$

The stress and nodal forces then use the new pressure. This is the undrained
response of the Biot equations, so with physical inertia it carries the
fast and slow compressional waves.

**Fixed-stress form (PT mechanics).** Mechanics first reaches equilibrium for
the step. Pressure then follows from the accepted change in mean total
stress, with the fixed-stress storage
([Kim et al., 2011](https://doi.org/10.1016/j.cma.2010.12.022)):

$$
S_\sigma\,\Delta p = -\frac{\alpha}{K_b}\,\Delta\sigma_m
- \Delta t\,(\nabla\cdot\mathbf q - Q),
\qquad
S_\sigma = \frac1M + \frac{\alpha^2}{K_b}.
$$

$K_b = K$ in 3D. In 2D, $\sigma_m$ is the in-plane mean stress and
$K_b = K + G/3$. The pressure change enters the effective stress in the next
mechanical update. Saving it in checkpoints makes restarts exact. Because
mechanics sees the pressure one step late, the coupling error is first
order in $\Delta t$.

`control.has_poroelastic_pressure_feedback = no` removes the mechanical
source term (the $\dot\varepsilon_v$ or $\Delta\sigma_m$ term). Pressure
still diffuses and still acts on the effective stress. The storage stays as
above. This gives a flow-only model on a deforming or fixed skeleton.

### Hydraulic substeps

Pressure diffusion often needs smaller steps than mechanics. Within each
physical step DES3D advances pressure in explicit substeps. Their size is
set by the assembled lumped storage and conductance, so the update is
stable for any physical step, including `control.fixed_dt`. Mechanics,
porosity and other histories advance once per physical step. Scheduled
boundary values and sources are integrated exactly over each substep.

## Boundary and initial conditions

Each face has a hydraulic type, `bc.hbc_x0` to `bc.hbc_z1` (y faces in 3D
only):

| Type | Condition |
| --- | --- |
| `0` | No normal flow (default) |
| `1` | Hold the initial nodal pressure |
| `2` | Prescribed pressure from `bc.hbc_pressure` (Pa) |
| `3` | Prescribed outward Darcy flux from `bc.hbc_flux` (m/s) |

`bc.hbc_pressure` and `bc.hbc_flux` list six values in the order
x0 x1 y0 y1 z0 z1. A shared piecewise-linear multiplier,
`bc.hbc_schedule_time_in_yr` and `bc.hbc_schedule_ratio` with
`bc.num_hbc_schedule` entries, scales types 2 and 3 in time. A repeated time
makes a step; the ratio is held outside the table. Two faces that meet must
prescribe the same pressure at their shared nodes.

`ic.pore_pressure_option` sets the initial pressure:

| Value | Initial pressure |
| --- | --- |
| `0` (default) | Hydrostatic, $p = -\rho_f g\,(z - z_w)$ with water table $z_w$ = `ic.water_table_z`, plus `ic.excess_pore_pressure` away from the boundaries |
| `1` | Linear in $x$ between the pressures prescribed on the x0 and x1 faces |
| `2` | Uniform, `ic.pore_pressure_value` |

Above the water table the hydrostatic pressure is negative (suction).

## Wells and point sources

**Wells** are vertical screens with a prescribed volume rate:
`bc.num_wells`, `bc.well_x`, `bc.well_y` (3D), `bc.well_z_top`,
`bc.well_z_bottom` and `bc.well_rate`. The rate is m³/s in 3D and m²/s per
unit out-of-plane length in 2D; positive extracts. The rate is spread
uniformly along the screen and integrated exactly against the element shape
functions. All wells share one schedule, `bc.well_schedule_time_in_yr` and
`bc.well_schedule_ratio`. Each step applies the exact time average of the
schedule, so the pumped volume does not depend on the step size.

**Point sources** (`[injection]` section) supply or extract fluid at chosen
points, with a constant rate or a total amount over a time window. Positive
rates supply fluid. With fluid heat advection, an injected temperature can
be set. A parallel `[heat_injection]` section supplies heat at points.

## Partly saturated flow

Setting `mat.retention_model` to a nonzero value per material enables
Richards flow ([Richards, 1931](https://doi.org/10.1063/1.1745010)) with
the gas phase at zero gauge pressure. With suction $s=\max(-p,0)$, effective
saturation $S_e$ and residual saturation $S_r$
(`mat.residual_saturation`), the saturation is
$S = S_r + (1-S_r)\,S_e$:

| `retention_model` | $S_e$ | $k_r$ |
| --- | --- | --- |
| `0` | 1 (saturated) | 1 |
| `1` van Genuchten–Mualem | $\left[1+(a s)^n\right]^{-m}$, $m=1-1/n$ | $S_e^{1/2}\left[1-\left(1-S_e^{1/m}\right)^m\right]^2$ |
| `2` Brooks–Corey–Burdine | $(a s)^{-n}$ for $a s>1$, else 1 | $S_e^{3+2/n}$ |
| `3` Gardner | $e^{-a s}$ | $S_e$ |

Here $a$ is `mat.retention_alpha` (1/Pa) and $n$ is `mat.retention_n`
([van Genuchten, 1980](https://doi.org/10.2136/sssaj1980.03615995004400050002x);
[Mualem, 1976](https://doi.org/10.1029/WR012i003p00513)). For Brooks–Corey,
$1/a$ is the air-entry pressure and $n$ the pore-size index.

The fluid content becomes $\phi S(p) + p/M$ plus the mechanical term. DES3D
updates the nodal content explicitly and inverts it for pressure node by
node. The content is a monotone function of pressure, so each inversion has
one root. Effective stress uses Bishop's form with $\chi = S_e$
([Lu et al., 2010](https://doi.org/10.1029/2009WR008646)):

$$
\boldsymbol\sigma' = \boldsymbol\sigma + \alpha\,S_e(p)\,p\,\mathbf I .
$$

Suction therefore adds apparent cohesion to a partly saturated slope.
Retention cannot yet be combined with evolving porosity, thermal
pressurization or matrix exchange.

## Evolving porosity and permeability

With `mat.porosity_model = 1`, porosity follows the deformation through an
element history, the pore strain $\varepsilon_\phi$. Each step adds

$$
\Delta\varepsilon_\phi = \Delta\varepsilon_v + \frac{\Delta p}{K_s}
- \alpha_s\,\Delta T,
\qquad
\phi = \alpha - (\alpha - \phi_0)\,e^{-\varepsilon_\phi},
$$

where $\alpha_s$ is the solid thermal expansivity (`mat.alpha`, used only
with thermal pressurization) and $\phi_0$ the material porosity. A step that
would leave $0<\phi\le\alpha$ stops the run with a diagnostic.

`mat.permeability_model` lets permeability follow porosity:

| Value | Permeability |
| --- | --- |
| `0` (default) | Fixed, $k = k_0$ |
| `1` Kozeny–Carman | $k = k_0\,\left(\dfrac{\phi}{\phi_0}\right)^3\left(\dfrac{1-\phi_0}{1-\phi}\right)^2$ |
| `2` power law | $k = k_0\,(\phi/\phi_0)^n$, $n$ = `mat.permeability_exponent` |

([Costa, 2006](https://doi.org/10.1029/2005GL025134);
[Yang et al., 2021](https://doi.org/10.1029/2021JB021787)).

## Matrix storage

`mat.matrix_storage` (1/Pa per bulk volume) and `mat.matrix_exchange`
(1/(Pa s)) add an immobile reservoir to each element, as in a double-porosity
medium ([Warren and Root, 1963](https://doi.org/10.2118/426-PA)). The
reservoir exchanges fluid with the mobile pressure at the rate
$q = c_x\,(p - p_m)$. It starts at the mobile pressure, and the volume it
gains is removed from the flow exactly. Its pressure is saved as
`matrix pressure`.

## Heat transport and thermal pressurization

### Advection by groundwater

With `control.has_fluid_thermal_advection = yes`, temperature is carried by
the Darcy flux:

$$
C\,\dot T + \rho_f c_f\,\mathbf q\cdot\nabla T = \nabla\cdot(\lambda\nabla T) + r,
\qquad
C = (1-\phi)\rho_s c_s + \phi\,\rho_f c_f,
$$

with fluid heat capacity $c_f$ (`mat.fluid_heat_capacity`). The fluid
density in Darcy gravity varies with temperature (Boussinesq),
$\rho_f[1-\alpha_f(T-T_0)]$, with $\alpha_f$ = `mat.fluid_alpha` and $T_0$
the surface temperature. This drives free convection. Heat diffusion also
runs in explicit substeps within each physical step. Thermal boundary types
`bc.tbc_x0` to `bc.tbc_z1` select insulated (0) or prescribed-temperature (1)
faces, with values in `bc.tbc_val_*` (K).

### Thermal pressurization

With `control.has_thermal_pressurization = yes`, heating expands both the
solid and the pore fluid
([McTigue, 1986](https://doi.org/10.1029/JB091iB09p09533);
[Rice, 2006](https://doi.org/10.1029/2005JB004006)). The solid adds a
thermal stress $-K\alpha_s\Delta T$ to each normal component, and the fluid
content gains the term $-\beta(T-T_0)$ with

$$
\beta = \phi\,\alpha_f + (\alpha - \phi)\,\alpha_s .
$$

In a sealed or poorly drained region, heating therefore raises pore
pressure and lowers effective stress. It requires hydraulic and thermal
diffusion and an elastic bulk response.

## Remeshing

After a remesh, nodal pressure is interpolated onto the new mesh like other
nodal fields. For saturated material with fixed properties, DES3D then
adjusts the pressure on free nodes by a common offset, so the total linear
Biot content $\int\zeta\,dV$ is the same before and after the remesh.
Prescribed-pressure nodes keep their values. The content changes only
where the domain itself gains or loses volume. This is a global constraint;
it does not conserve content element by element. Partly saturated material
and evolving porosity are interpolated without this adjustment.

## Output

Saved frames contain `pore pressure` and, when the corresponding model is
active, `porosity`, `permeability`, `saturation`, `effective saturation`,
`relative permeability` and `matrix pressure`. The field `fluid balance` lists, for the last step, the
change in stored fluid, the mechanical and thermal source, well extraction,
net boundary inflow and their residual. The residual measures how well the
discrete update balances its own fluid volume.

## Parameters

| Parameter | Default | Meaning |
| --- | --- | --- |
| `control.has_hydraulic_diffusion` | `no` | Enable pore-pressure transport |
| `control.has_poroelastic_pressure_feedback` | `yes` | Let deformation drive pore pressure |
| `mat.porosity` | `[0.0]` | Porosity $\phi_0$ |
| `mat.hydraulic_perm` | `[1e-14]` | Intrinsic permeability $k_0$ (m²) |
| `mat.permeability_tensor` | `[1,1,1,0,0,0]` | Dimensionless anisotropy tensor |
| `mat.fluid_visc` | `[1.002e-3]` | Fluid viscosity $\mu$ (Pa s) |
| `mat.fluid_rho0` | `[1000]` | Reference fluid density $\rho_f$ (kg/m³) |
| `mat.fluid_bulk_modulus` | `[2.17e9]` | Fluid bulk modulus $K_f$ (Pa) |
| `mat.fluid_alpha` | `[2.07e-4]` | Fluid thermal expansivity $\alpha_f$ (1/K) |
| `mat.fluid_heat_capacity` | `[4180]` | Fluid heat capacity $c_f$ (J/(kg K)) |
| `mat.biot_coeff` | `[1.0]` | Biot–Willis coefficient $\alpha$ |
| `mat.bulk_modulus_s` | `[37e9]` | Grain bulk modulus $K_s$ (Pa) |
| `mat.derive_biot_coeff_from_bulk_moduli` | `no` | Use $\alpha = 1 - K/K_s$ |
| `mat.retention_model` | `[0]` | `0` saturated, `1` van Genuchten–Mualem, `2` Brooks–Corey, `3` Gardner |
| `mat.retention_alpha` | `[1e-4]` | Retention parameter $a$ (1/Pa) |
| `mat.retention_n` | `[2]` | Retention exponent $n$ |
| `mat.residual_saturation` | `[0]` | Residual saturation $S_r$ |
| `mat.porosity_model` | `0` | `0` fixed, `1` evolving with deformation |
| `mat.permeability_model` | `0` | `0` fixed, `1` Kozeny–Carman, `2` power law |
| `mat.permeability_exponent` | `[3]` | Power-law exponent $n$ |
| `mat.matrix_storage`, `mat.matrix_exchange` | `[0]`, `[0]` | Immobile reservoir storage (1/Pa) and exchange coefficient (1/(Pa s)) |
| `control.has_fluid_thermal_advection` | `no` | Heat transport by Darcy flow |
| `control.has_thermal_pressurization` | `no` | Thermal stress and thermal fluid content |
| `bc.hbc_x0` … `bc.hbc_z1` | `0` | Hydraulic boundary type per face |
| `bc.hbc_pressure`, `bc.hbc_flux` | zeros | Face values for types 2 and 3 |
| `ic.pore_pressure_option` | `0` | Initial pressure field |
| `ic.water_table_z` | `0` | Initial water-table height (m) |

## References

- Biot, M. A. (1941). General theory of three-dimensional consolidation.
  *Journal of Applied Physics*, 12(2), 155–164.
  https://doi.org/10.1063/1.1712886
- Biot, M. A., and Willis, D. G. (1957). The elastic coefficients of the
  theory of consolidation. *Journal of Applied Mechanics*, 24, 594–601.
  https://doi.org/10.1115/1.4011606
- Costa, A. (2006). Permeability-porosity relationship: A reexamination of
  the Kozeny-Carman equation based on a fractal pore-space geometry
  assumption. *Geophysical Research Letters*, 33, L02318.
  https://doi.org/10.1029/2005GL025134
- Kim, J., Tchelepi, H. A., and Juanes, R. (2011). Stability and
  convergence of sequential methods for coupled flow and geomechanics:
  Fixed-stress and fixed-strain splits. *Computer Methods in Applied
  Mechanics and Engineering*, 200, 1591–1606.
  https://doi.org/10.1016/j.cma.2010.12.022
- Lu, N., Godt, J. W., and Wu, D. T. (2010). A closed-form equation for
  effective stress in unsaturated soil. *Water Resources Research*, 46,
  W05515. https://doi.org/10.1029/2009WR008646
- McTigue, D. F. (1986). Thermoelastic response of fluid-saturated porous
  rock. *Journal of Geophysical Research*, 91(B9), 9533–9542.
  https://doi.org/10.1029/JB091iB09p09533
- Mualem, Y. (1976). A new model for predicting the hydraulic conductivity
  of unsaturated porous media. *Water Resources Research*, 12(3), 513–522.
  https://doi.org/10.1029/WR012i003p00513
- Rice, J. R. (2006). Heating and weakening of faults during earthquake
  slip. *Journal of Geophysical Research*, 111, B05311.
  https://doi.org/10.1029/2005JB004006
- Rice, J. R., and Cleary, M. P. (1976). Some basic stress diffusion
  solutions for fluid-saturated elastic porous media with compressible
  constituents. *Reviews of Geophysics*, 14(2), 227–241.
  https://doi.org/10.1029/RG014i002p00227
- Richards, L. A. (1931). Capillary conduction of liquids through porous
  mediums. *Physics*, 1, 318–333. https://doi.org/10.1063/1.1745010
- van Genuchten, M. T. (1980). A closed-form equation for predicting the
  hydraulic conductivity of unsaturated soils. *Soil Science Society of
  America Journal*, 44, 892–898.
  https://doi.org/10.2136/sssaj1980.03615995004400050002x
- Warren, J. E., and Root, P. J. (1963). The behavior of naturally
  fractured reservoirs. *SPE Journal*, 3(3), 245–255.
  https://doi.org/10.2118/426-PA
- Yang, Z., Yehya, A., Iwalewa, T. M., and Rice, J. R. (2021). Effect of
  permeability evolution in fault damage zones on earthquake recurrence.
  *Journal of Geophysical Research: Solid Earth*, 126, e2021JB021787.
  https://doi.org/10.1029/2021JB021787
