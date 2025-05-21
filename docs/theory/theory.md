---
sidebar_position: 1
---

# Solution schemes in DES3D

## Equation of motion

DES3D solves the equation of motion, i.e., linear momentum balance equation, in the following fully dynamic form:

  $$
  \rho\dot{\mathbf{u}}=\nabla\cdot\boldsymbol{\sigma}+\rho\mathbf{g}
  $$

  where $\rho$ is the material density, $\mathbf{u}$ is the velocity
  vector, $\boldsymbol{\sigma}$ is the total (Cauchy) stress tensor, and
  $\mathbf{g}$ is the acceleration of gravity. The dot above $\mathbf{u}$
  indicates total time derivative while bold face indicates a vector or
  tensor. The spatial gradient is denoted by $\nabla$, the inner product
  between vectors is denoted by $\cdot$, while $\nabla\cdot$ represents
  the divergence operator. 

  This equation must be complemented with
  appropriate initial and boundary conditions. The motion is described using a **Lagrangian
  formulation**.

  ## Discretization

  The momentum equation is discretized using a two- or three-dimensional (2D or 3D),
  unstructured mesh. The displacement $\mathbf{x}$,
  velocity $\mathbf{u}$, acceleration $\mathbf{a}$, force $\mathbf{f}$,
  and temperature $T$ are nodal values on linear (P1) elements while other
  physical quantities (e.g., stress $\boldsymbol{\sigma}$ and strain
  $\boldsymbol{\epsilon}$) and material properties (e.g., density $\rho$
  and viscosity $\eta$) are evaluated on the one-point quadrature in the elements; 
  and thus are piecewise constant (P0).

  A weak form of the momentum balance equation is constructed by the standard finite element method.
  The velocity function $\mathbf{u}$ is expanded with piecewise linear basis functions:

  $$
  \mathbf{u}(\mathbf{x}) = \sum_{a} \mathbf{u}_{a} \N_{a}(\mathbf{x}),
  $$
  
  where $\N_{a}(\mathbf{x})$ is the basis function associated with global node number $a$ in the mesh with the property, $\N_{i}(\mathbf{x}_{j})=\delta_{ij}$ for the coordinates of $j$-th node, $\mathbf{x}_{j}$.
  
  $\N_{a}(\mathbf{x})$'s are also used as weighting functions and multipled to both sides of the equation, and the product is integrated over the domain:
  
  $$
  \int_{\Omega} \N_{a} \rho\dot{\mathbf{u}}\,d\Omega =\int_{\Omega} \N_{a} \left( \nabla\cdot\boldsymbol{\sigma}+\rho\mathbf{g} \right) \,d\Omega, \quad a=0,\ldots,N,
  $$
  
  where $N+1$ is the total number of nodes in a mesh.
  
  Plugging in the finite dimensional representation of $\mathbf{u}$ and carrying out the element-to-global assemablage, 
  we obtain the following equation for the acceleration $\mathbf{a}_a$ of every node $a$:

  $$
  m_{a}\mathbf{a}_{a}=\mathbf{f}_{a}=\mathbf{f}_{a}^{int}+\mathbf{f}_{a}^{bc}+\mathbf{f}_{a}^{ext}.
  $$

  $m_{a}$ is the nodal mass given by

  $$
  m_{a}=\sum_{e}\left(\int_{\Omega_{e}}N_{e}^{a}\rho_{f}d\Omega\right)
    =\sum_{e}\left(\rho_f\int_{\Omega_{e}}N_{e}^{a}d\Omega\right)
    =\sum_{e}^{a\in e}\left(\frac{1}{M}\rho_{f}\Omega_{e}\right),
  $$
  
where $\Omega_e$ is the area (volume in 3D) of the element $e$, $N_{a}^{e}$ is $N_{a}$ confined to element $e$,
and $M$ is the number of apexes of an element (i.e., $M=3$ for 2D
triangles and $M=4$ for 3D tetrahedra.) The summation should be
understood as done for all the elements having node $a$ as an apex. 

| :point_up: Two features to note |
|:----------------------------|
| Fictitious density, $\rho_f$, instead of the true density, $\rho$, is used in the definition of $m_a$. |
| Row-sum mass lumping is applied to obtain a diagonal mass matrix. |

The total force $\mathbf{f}_{a}$ is
composed of three parts: the internal, boundary, and external forces.
The internal force, $\mathbf{f}_{a}^{int}$, is defined as:

$$
\begin{aligned}
  \mathbf{f}_{a}^{int}&=\sum_{e}\left(\int_{\Omega_{e}}\frac{\partial
      N_{a}^{e}}{\partial\mathbf{x}}\cdot\boldsymbol{\sigma}d\Omega\right)
  =\sum_{e}\left(\frac{\partial N_{a}^{e}}{\partial\mathbf{x}}
  \cdot\boldsymbol{\sigma}\int_{\Omega_{e}}d\Omega\right) \nonumber \\
  &=\sum_{e}^{a\in e}\left(\frac{\partial
      N_{a}^{e}}{\partial\mathbf{x}}\cdot\boldsymbol{\sigma}\Omega_{e}\right).
\end{aligned}
$$

Neumann boundary conditions are tractions prescribed on the surface of
the body. These tractions yield a boundary force denoted
$\mathbf{f}_{a}^{bc}$:

$$
\mathbf{f}_{a}^{bc}=\sum_{e}\left(\oint_{\partial\Omega_{e}}-N_{a}^{e}\boldsymbol{\sigma}\cdot\mathbf{n}dL \right)
=-\sum_{e}^{a\in s,\: s\in\partial\Omega_{e}}\left(\frac{1}{M-1}\boldsymbol{\sigma}_{s}\cdot\mathbf{n}_{s}L_{s}\right).
$$

The summation is over the boundary segment $s$, which has a length
$L_{s}$ (surface area in 3D), the outward, unit normal vector
$\mathbf{n}$, and a prescribed (constant) stress
$\boldsymbol{\sigma}_{s}$ on the Neumann boundary. The external force,
$\mathbf{f}_{a}^{ext}$, is given by:

$$
\mathbf{f}_{a}^{ext}=\sum_{e}\left(\int_{\Omega_{e}}N_{a}^{e}\rho\mathbf{g}d\Omega\right)
=\sum_{e}\left(\rho\mathbf{g}\int_{\Omega_{e}}N_{a}^{e}d\Omega\right)
=\sum_{e}^{a\in e}\left(\frac{1}{M}\rho\mathbf{g}\Omega_{e}\right).
$$

When deriving the equations above, we utilize the fact that $\rho_f$,
$\rho$, $\frac{\partial N_{a}^{e}}{\partial\mathbf{x}}$,
$\boldsymbol{\sigma}$, and $\mathbf{g}$ are constants on each element,
and these identities:

$$
\int_{\Omega_e}d\Omega=\Omega_{e}, \quad
\int_{\Omega_e}N_{a}^{e}d\Omega=\frac{1}{M}\Omega_{e}, \quad
\oint_{\partial\Omega_{e}}N_{a}^{e}dL=\frac{1}{M-1}L_s.
$$

## The Rest of the solution scheme

We are interested in tectonic deformation, 
which can be properly simulated in a quasi-static fashion. 
Thus, we apply a technique called **dynamic relaxation**, 
which enables us to achieve a static equilibrium
from the dynamic momentum equation by damping out the intertial force.
Additionally, using **mass scaling**, we substitute the true density by a
fictitious scaled density that allows us to increase the size of
admissible stable time steps in the explicit time integration scheme.
That is, using the resulting **scaled** acceleration and velocity, we
compute an instantaneous velocity and position of each node in the mesh,
which updates the model geometry at each time step.