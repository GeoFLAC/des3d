---
slug: /theory/timeintegration
sidebar_position: 6
---

# Velocity and node position update

The velocity is updated with the damped acceleration, but subject to the
prescribed velocity boundary conditions, that is:

$$
\mathbf{u}_{a}^{t+\Delta t}=\mathbf{u}_{a}^{t}+\Delta t \, \mathbf{a}_{a}^{t+\Delta t}.
$$

The position $\mathbf{x}_{a}$ of the node $a$ is updated by:

$$
\mathbf{x}_{a}^{t+\Delta t}=\mathbf{x}_{a}^{t}+\Delta t \, \mathbf{u}_{a}^{t+\Delta t}.
$$

When `control.has_moving_mesh = yes`, node motion changes the mesh, so
the shape-function derivatives and element volumes are refreshed. With a
fixed mesh, coordinates and these geometric quantities stay fixed.
For the coupled transport and mechanics order, see
[Source layout](../../developer/source-layout.md#one-time-step).
