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
density, while the fictitious increase in mass keeps the inertial forces
small compared with the other forces at play in these simulations. The
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
As $c_{1}$ approaches $10^{12},$ the fictitious density approaches the
material (true) density. 

The optimal value of $c_{1}$ depends on the
rheology parameters, resolution, and domain size. We find that $c_{1}$
in the range of **$10^{4}$** to **$10^{8}$** is adequate for our simulation
targets. 

Unfortunately, the choice of $c_{1}$ is currently empirical. We
are working to devise a consistent way of finding the optimal value of
$c_{1}$.
