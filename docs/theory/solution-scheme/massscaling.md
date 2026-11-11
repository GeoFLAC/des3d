---
slug: /theory/massscaling
sidebar_position: 3
---

# Mass scaling

The Courant-Friedrichs-Lewy (CFL) condition imposes a fundamental limit
on the time step size for an explicit time marching scheme. In the
explicit time integration used in DynEarthSol, the $P$-wave velocity sets
the largest possible time step size. For instance, using relevant
parameters for lithospheric modeling, a $P$-wave speed of $\sim10^{3}$
m/s and an element size of $\sim10^{3}$ m yield a stable time step size
of $\sim$ 1 s. With this stringent upper limit for the time step size, a
typical LTM simulation would take an excessively large number of time
steps to reach the targeted amount of deformation (e.g., $O(10^{13})$
steps for 1 Myrs of model time).

To overcome this drawback, a mass scaling technique is applied. We
adjust each nodal mass (density) to achieve a stable time step size
which is orders of magnitude larger than the one allowed by the physical
density. Increasing mass also increases inertia at a given acceleration;
the approximation is useful only when the resulting inertial forces remain
small relative to the mechanical loads. Check that separation for the
chosen loading path. The
time step size increases when the elastic wave speed, $u_{elastic}$, is
made comparable to the tectonic speed, $u_{tectonic}$, ($\sim10^{-9}$
m/s). We achieve this time-step size increase by scaling the density as
follows:

$$
u_{\text{elastic}}=\sqrt{K_{s}/\rho_{f}}=c_{1}u_{\text{tectonic}},
$$

where $K_{s}$ is the bulk modulus of the material, $\rho_{f}$ is a
fictitious scaled density and $c_{1}$ is a constant.

## Range of $c_{1}$ values

When $c_{1}$ is too
small, that is, the density is scaled up too high, dynamic instabilities
might occur. In this case, the fictitious elastic wave is too slow to
relax the stress back to quasi-equilibrium, therefore the kinetic energy
becomes too large, breaking the assumption of the quasi-static
state. When the density scaling is insufficient
(i.e., $c_{1}$ is too large), the simulation becomes too time consuming.
The density approaches its physical value when
$c_1 u_{\text{tectonic}}$ approaches the bulk-based speed
$\sqrt{K_s/\rho}$. There is no universal value of $c_1$ for this transition.

`control.inertial_scaling` sets $c_1$ when `control.is_quasi_static = yes`
with ordinary explicit/GVS mechanics. The coupled-method comparisons
include $10^4$, $10^5$ and $10^6$; no single value establishes equilibrium
for every load, material or mesh. Compare physical-step refinement, force
residuals and observables, especially for sudden traction. With
`is_quasi_static = no`, the inertial mass is physical and this scaling
parameter has no effect. PT has a separate pseudo-time relaxation.

## Reference speed for global velocity scaling

When `use_global_velocity_scaling` is enabled, the mass-scaled density and
the elastic time step are limited by an elastic wave speed derived from the
material moduli. `mass_scaling_reference_speed` selects which modulus sets
that ceiling:

| Value | Ceiling | Notes |
|-------|---------|-------|
| `shear` (default) | $\sqrt{G/\rho}$ | Historical behavior. |
| `bulk` | $\sqrt{K_s/\rho}$ | Uses the bulk modulus instead. |

Leaving the option at its default reproduces earlier results.
