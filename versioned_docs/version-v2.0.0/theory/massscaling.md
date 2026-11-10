---
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

The optimal value of $c_{1}$ depends on the
rheology parameters, resolution, and domain size. We find that $c_{1}$
in the range of **$10^{4}$** to **$10^{8}$** is adequate for our simulation
targets. 

Unfortunately, the choice of $c_{1}$ is currently empirical. We
are working to devise a consistent way of finding the optimal value of
$c_{1}$.
