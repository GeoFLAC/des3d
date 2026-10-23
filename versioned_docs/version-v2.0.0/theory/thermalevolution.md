---
sidebar_position: 7
---

# Modeling thermal evolution

Thermal evolution of lithosphere is often one of the key components of
the long-term tectonics and is modeled by solving the heat equation:

$$
\rho c_{p}\dot{T}=k\nabla^{2}T,
$$

where $T$ is the temperature field while $c_{p}$ and $k$ are the heat
capacity and the thermal conductivity of the lithosphere material.
Multiplying by a weighting function on both sides and integrating by
parts over the domain, we get

$$
C_{a}\dot{T}_{a}^{t+\Delta t}=-\sum_{e}^{a\in e,\: b\in e}\left(kD_{ab}T_{b}^{t}\Omega_{e}\right) + \sum_{e}^{a\in s,\: s\in\partial\Omega_{e}}\left(\frac{1}{M-1}\mathbf{q_{s}}\cdot\mathbf{n}_{s}L_{s}\right),
$$

where the diffusion matrix

$$
D_{ab}=\sum_{a,b\in e}\sum_i\frac{\partial
    N_{a}^{e}}{\partial x_{i}}\frac{\partial N_{b}^{e}}{\partial x_{i}}
$$

is evaluated at the barycenter of each element since we use constant
strain triangles (linear finite elements on simplexes). The lumped
thermal capacitance (mass) is given by,

$$
C_{a}=\sum_{e}^{a\in e}\left(\frac{1}{M}\rho c_{p}\Omega_{e}\right),
$$

and $\mathbf{q_{s}}$ is the prescribed boundary heat flux on a segment
$s$. Then, the temperature is updated explicitly as:

$$
T_{a}^{t+\Delta t}=T_{a}^{t}+\Delta t\,\dot{T}_{a}^{t+\Delta t}.
$$

The stability condition for the explicit integration of temperature is
usually satisfied by the time step size determined by the scaled wave
speed, but if a stable time step size for heat diffusion is smaller, it
becomes the global time step size.
