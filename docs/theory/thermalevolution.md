---
sidebar_position: 7
title: Heat transport
description: The heat equation DES solves, its sources (radiogenic, shear and injected heat), groundwater heat advection, the explicit finite-element update with sub-steps, and how temperature feeds back on density and stress.
---

# Heat transport

Temperature controls the viscosity of rock, its density and, with pore
fluid, its pore pressure. DES solves the heat equation on the same
Lagrangian mesh as the mechanics:

$$
\rho c_p \frac{dT}{dt} = \nabla\cdot(k\nabla T) + \rho H + Q_s + Q_i,
$$

where $T$ is temperature, $\rho$ density, $c_p$ heat capacity
(`mat.heat_capacity`), $k$ thermal conductivity (`mat.therm_cond`), $H$
radiogenic heat production per unit mass, $Q_s$ shear heating and $Q_i$
heat injected at points or with fluid. Because the mesh moves with the
material, $dT/dt$ is the rate following the material: heat is carried by
the deformation without a separate advection term. When the mesh is
remeshed, nodal temperature is interpolated to the new nodes; see
[Remeshing](./remeshing.md).

## Discretization

Multiplying by a weighting function and integrating by parts over the
domain gives, for node $a$,

$$
C_{a}\dot{T}_{a}=-\sum_{e\ni a}\Big(k_e\,\Omega_e\sum_{b\in e}D_{ab}T_{b}\Big) + \sum_{e\ni a}\frac{\rho_e H_e\,\Omega_e}{M} + \dots,
\qquad
D_{ab}=\sum_i\frac{\partial N_{a}}{\partial x_{i}}\frac{\partial N_{b}}{\partial x_{i}},
$$

with $M$ the number of nodes per element, the element volume $\Omega_e$
and the linear shape functions $N_a$, whose gradients are constant in each
simplex. The thermal mass is lumped:

$$
C_{a}=\sum_{e\ni a}\frac{\rho_e c_{p,e}\,\Omega_{e}}{M}.
$$

The temperature is updated explicitly, $T_a \leftarrow T_a + \Delta t\,\dot T_a$.
The explicit update is stable only below a diffusion time step of order
$\rho c_p h^2/k$. When the mechanical time step is longer, DES divides it into
as many equal thermal sub-steps as stability requires and applies the
sources over each sub-step; the mechanical step is not shortened.

## Boundary conditions

Each side of the box is either insulated or held at a fixed temperature,
set by `bc.tbc_x0` … `bc.tbc_z1` (0 insulated, 1 fixed) with the value
`bc.tbc_val_*`. By default only the top is fixed, at
`bc.surface_temperature`. A fixed value applies from the start, so a value
that differs from the initial temperature is part of the initial state; see
[Temperature](../user-guide/model-setup/temperature.md) for the initial
profiles. There is no prescribed boundary heat flux; heat can be added
through the sources below.

## Heat sources

**Radiogenic heat.** For the continental initial profiles
(`ic.temperature_option = 2` or `3`), the heat production of each layer,
`mat.radiogenic_heat_prod` (W/kg) of the material named in
`ic.radiogenic_heat_mat_in_layer`, is stored in each element. It stays with
the element, is remapped on remeshing and heats the model throughout the
run. The field is written as `radiogenic source`.

**Shear heating.** With `control.has_shear_heating = yes`, all the viscous
and plastic work accepted in a step becomes heat in the next thermal update,
with unit efficiency. The initial pseudo-transient equilibration does not
generate heat.

**Injected heat.** `[heat_injection]` adds heat at points on a schedule, and
`[injection]` fluid injected at a prescribed temperature carries its
enthalpy into the model; see [Poromechanics](./poromechanics.md).

## Groundwater heat advection

With pore-fluid flow and `control.has_fluid_thermal_advection = yes`, Darcy
flow also carries heat, and the heat capacity becomes that of the
rock–water mixture,
$C = (1-\phi)\rho_s c_s + \phi\rho_f c_f$. The advective term is added to
the same explicit update as a Galerkin operator with added graph diffusion,
which keeps the update free of new extremes; with no flow it reduces to
ordinary conduction. The thermal sub-steps then also respect the advective
limit. Buoyancy from
fluid thermal expansion (`mat.fluid_alpha`) couples the flow to temperature.
The formulation and its checks are in [Poromechanics](./poromechanics.md)
and the [heat and groundwater benchmarks](../benchmarks/poromechanics/index.md).

## Coupling back to mechanics

**Density.** The density of each material falls with temperature,

$$
\rho = \rho_0\,\big[1 - \alpha\,(T - 273\ \text{K})\big],
$$

with the volumetric thermal expansion $\alpha$ (`mat.alpha`, default
$3\times10^{-5}$ K⁻¹). This drives thermal buoyancy and also enters the
thermal mass, so with $\alpha \ne 0$ the diffusivity $k/(\rho c_p)$ varies
slightly with temperature; the [half-space cooling
benchmark](../benchmarks/heat/half-space-cooling.md) shows the effect.

**Viscosity.** Creep viscosity depends exponentially on temperature; see
[Rheology](./rheology.md).

**Thermal stress.** With pore-fluid flow enabled, a temperature change also
changes the stress through the drained thermal expansion $K\alpha\,\Delta T$
and, through the fluid, the pore pressure (thermal pressurization). Without
pore-fluid flow, thermal expansion acts only through the density.

## Parameters

| Parameter | Meaning | Default |
| --- | --- | --- |
| `control.has_thermal_diffusion` | solve conduction; if `no`, temperature only moves with the material | yes |
| `mat.heat_capacity`, `mat.therm_cond` | $c_p$ (J/kg/K), $k$ (W/m/K) | [1e3], [3] |
| `mat.alpha` | volumetric thermal expansion (1/K) | [3e-5] |
| `mat.radiogenic_heat_prod` | heat production (W/kg) used by the layered initial profiles | [0] |
| `bc.tbc_*`, `bc.tbc_val_*` | thermal boundary type and value per side | top fixed |
| `bc.surface_temperature`, `bc.mantle_temperature` | top and mantle temperatures (K) | 273, 1600 |
| `control.has_shear_heating` | convert viscous and plastic work to heat | no |
| `control.has_fluid_thermal_advection` | heat advection by Darcy flow | no |
