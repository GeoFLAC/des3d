---
sidebar_position: 0.5
slug: /theory/governing-equations
title: Governing equations
description: The balance laws DES solves, the unknowns and sign conventions, and where each equation and its numerical treatment is described.
---

# Governing equations

DynEarthSol follows the deforming material with a Lagrangian mesh: nodes
move with the velocity, so every quantity below is carried by the material
and time derivatives follow it. This page collects the equations and the
conventions; each section links to the page that treats it in detail.

## Unknowns and conventions

| Quantity | Where it lives | Symbol |
| --- | --- | --- |
| velocity, position | nodes | $\mathbf{u}$, $\mathbf{x}$ |
| temperature | nodes | $T$ |
| pore pressure (with fluid flow) | nodes | $p$ |
| stress, strain, plastic strain | elements | $\boldsymbol\sigma$, $\boldsymbol\varepsilon$, $\varepsilon_p$ |
| material identity | markers | |

Stress and strain are positive in tension; pore pressure is positive in
compression. Depth is negative $z$ (the top of the box is at $z = 0$). In
2D the coordinates are $x$ and $z$. Elements are linear simplices
(triangles in 2D, tetrahedra in 3D), so strain and stress are constant in
each element.

## Momentum

$$
\rho\,\frac{d\mathbf{u}}{dt} = \nabla\cdot\boldsymbol\sigma + \rho\,\mathbf{g}.
$$

DES integrates this equation explicitly. For slow tectonic deformation the
inertia is scaled up ([mass scaling](./solution-scheme/massscaling.md)) and
damped ([dynamic relaxation](./solution-scheme/dynamicrelaxation.md)) so
that each step stays close to equilibrium, or each physical step is solved
to equilibrium by [pseudo-transient iteration](./solution-scheme/pt.md).
See [Solution scheme](./solution-scheme/index.md).

## Constitutive law

The stress follows the strain history through the material's rheology:
elastic, viscous, Maxwell, elasto-plastic or elasto-visco-plastic, with
optional rate-and-state friction. The stress rate is objective: after the
constitutive update of each step, the stress and strain are rotated by the
element's spin (the Jaumann rate). See [Rheology](./rheology.md) for the laws,
[Constitutive update](./solution-scheme/constitutive.md) for their
integration and [Rate-and-state friction](./rate-state-friction.md).

## Density

The density of an element varies with temperature only,
$\rho = \rho_0[1 - \alpha(T - 273\ \text{K})]$, averaged over the materials
of its markers; it does not change with pressure or volumetric strain. It
enters the momentum balance through gravity, while volume change is
resisted by the bulk modulus in the constitutive law.

## Energy

$$
\rho c_p \frac{dT}{dt} = \nabla\cdot(k\nabla T) + \rho H + Q_s + Q_i,
$$

with radiogenic, shear and injected heat. See [Heat transport](./thermalevolution.md).

## Pore fluid

With `control.has_hydraulic_diffusion = yes`, the stress in the momentum
balance is the total stress of a fluid-saturated or partly saturated solid,
$\boldsymbol\sigma = \boldsymbol\sigma' - \alpha_B\,p\,\mathbf{I}$ for
effective stress $\boldsymbol\sigma'$ and Biot coefficient $\alpha_B$, and
the pore pressure obeys a fluid mass balance with Darcy flow. See
[Poromechanics](./poromechanics.md).

## Material and surface changes

Markers carry material identity and change it by
[phase changes](./markers-phase-changes.md); the top surface erodes and
receives sediment by [surface processes](./surface-processes.md); and the
mesh is rebuilt when it distorts, with fields mapped to the new mesh
([Remeshing](./remeshing.md)).

## Initial and boundary conditions

Velocity, traction, temperature and pressure conditions and the initial
temperature, stress and weak zones are set per model; see the
[User guide](../user-guide/model-setup/boundary-conditions.md).
