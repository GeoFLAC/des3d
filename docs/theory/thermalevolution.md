---
sidebar_position: 7
---

# Modeling thermal evolution

Thermal evolution of lithosphere is often one of the key components of
the long-term tectonics and is modeled by solving the heat equation:

::: linenomath*
$$\rho c_{p}\dot{T}=k\nabla^{2}T,
$$
:::

where $T$ is the temperature field while $c_{p}$ and $k$ are the heat
capacity and the thermal conductivity of the lithosphere material.
Multiplying by a weighting function on both sides and integrating by
parts over the domain, we get

::: linenomath*
$$C_{a}\dot{T}_{a}^{t+\Delta t}=-\sum_{e}^{a\in e,\: b\in e}\left(kD_{ab}T_{b}^{t}\Omega_{e}\right) + \sum_{e}^{a\in s,\: s\in\partial\Omega_{e}}\left(\frac{1}{M-1}\mathbf{q_{s}}\cdot\mathbf{n}_{s}L_{s}\right),
$$
:::

where the diffusion matrix

::: linenomath*
$$D_{ab}=\sum_{a,b\in e}\sum_i\frac{\partial
    N_{a}^{e}}{\partial x_{i}}\frac{\partial N_{b}^{e}}{\partial x_{i}}$$
:::

is evaluated at the barycenter of each element since we use constant
strain triangles (linear finite elements on simplexes). The lumped
thermal capacitance (mass) is given by,

::: linenomath*
$$C_{a}=\sum_{e}^{a\in e}\left(\frac{1}{M}\rho c_{p}\Omega_{e}\right),$$
:::

and $\mathbf{q_{s}}$ is the prescribed boundary heat flux on a segment
$s$. Then, the temperature is updated explicitly as:

::: linenomath*
$$T_{a}^{t+\Delta t}=T_{a}^{t}+\Delta t\,\dot{T}_{a}^{t+\Delta t}.
$$
:::

The stability condition for the explicit integration of temperature is
usually satisfied by the time step size determined by the scaled wave
speed, but if a stable time step size for heat diffusion is smaller, it
becomes the global time step size.

## Remeshing {#sc:remeshing}

We assess the mesh quality at fixed temporal intervals and use specific
quality measures to decide whether to keep using the present mesh or
remesh. For example, if the smallest angle of an element is less than a
certain prescribed value, we remesh. A group of nodes in the deformed
mesh is removed from the mesh if any of the following criteria is met.
For instance, if the deformed or displaced boundary is restored to the
initial configuration, some nodes may be left outside of the boundaries
of the new domain. Internal nodes, if surrounded only by small elements,
may be removed from the point set to be remeshed. Once all criteria are
enforced, a final list of nodes is collected. These nodes are provided
to the *Triangle* library [@Shewchuk1996] to construct a new
triangulation of the domain. At this stage, new nodes might be inserted
into the mesh or the mesh topology changed through edge-flipping during
the triangulation (Fig. [1](#fig:edgeflipping){reference-type="ref"
reference="fig:edgeflipping"}). This type of remeshing has been proposed
as a way of solving large deformation problems in the Lagrangian
framework [@Braun1994]. After the new mesh is created, the boundary
conditions, derivatives of shape function, and mass matrix have to be
re-calculated.

When most of the deformation is focused in and around a few deformation
zones like shear bands, most of the elements outside of the zones deform
only slightly and thus mostly remain unaffected by remeshing. The high
degree of similarity between the new and old meshes makes projecting the
fields of variables between the meshes very easy. For nodes and elements
unaffected by remeshing, which are the majority, a simple injection
suffices. That is, the data of the nodes and elements of the old mesh
are mapped onto the nodes and elements which are collocated with them in
the new mesh.

When deformation is not localized but distributed over a broad region of
the domain, remeshing might result in a new mesh that is very different
from the old one. Then, an inter-mesh mapping of variables becomes
necessary. For data associated to nodes (e.g., velocity and
temperature), we use linear interpolation of the data from the old mesh
to evaluate the field at the new nodal location. For data associated to
elements (e.g., strain and stress), we use a nearest-neighbor mapping.
 -->
