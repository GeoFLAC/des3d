---
sidebar_position: 8
---

# Remeshing

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
