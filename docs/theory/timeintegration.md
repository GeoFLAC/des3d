---
sidebar_position: 6
---

# Velocity and displacement update

The velocity is updated with the damped acceleration, but subject to the
prescribed velocity boundary conditions, that is:

$$
\mathbf{u}_{a}^{t+\Delta t}=\mathbf{u}_{a}^{t}+\Delta t \, \mathbf{a}_{a}^{t+\Delta t}.
$$

The position $\mathbf{x}_{a}$ of the node $a$ is updated by:

$$
\mathbf{x}_{a}^{t+\Delta t}=\mathbf{x}_{a}^{t}+\Delta t \, \mathbf{u}_{a}^{t+\Delta t}.
$$

Since the mesh is changed, the shape function derivates $N_{a}^{e}$ and
the element volume $\Omega_{e}$ are updated every time step.
