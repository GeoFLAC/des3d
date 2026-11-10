---
sidebar_position: 4
---

# Nodal Mixed Discretization

The linear triangular elements used in DynEarthSol2D are known to suffer
volumetric locking when subject to incompressible deformations. 
Since incompressible plastic or viscous flow are often
needed in LTM, we adopt an anti-volumetric locking correction based on
the nodal mixed discretization (NMD)
methodology (e.g., [De Micheli and Mocellin, 2009](https://dx.doi.org/10.1002/nme.2539)).

The strain rate of element $e$, $\boldsymbol{\dot{\epsilon}}_e$, is
computed from the velocity:

$$
\dot{\epsilon}_{e,ij}^{t+\Delta t}=\frac{1}{2}\sum_{a\in e}\left(\frac{\partial N_{a}^{e}}{\partial x_{i}}u_{a,j}^{t+\Delta t}+\frac{\partial N_{a}^{e}}{\partial x_{j}}u_{a,i}^{t+\Delta t}\right),
$$

where $i$, $j$ are spatial indices. The strain rate tensor can be
decomposed into the deviatoric and the isotropic parts:

$$
\boldsymbol{\dot{\epsilon}}_{e}=\textrm{dev}(\boldsymbol{\dot{\epsilon}}_{e})+\frac{1}{D}\textrm{tr}(\boldsymbol{\dot{\epsilon}}_{e})\mathbf{I},
$$

where $\textrm{dev}(\cdot)$ represents an operator returning the
deviatoric tensor, $\textrm{tr}(\cdot)$ is an operator returning the
trace of the projected tensor. $D=2$ for the in-plane projection in 2D
and $D=3$ in 3D. This is the dimension of the projected field, not the
number of physical normal stresses. A plane-strain assumption does not add
an out-of-plane component to this strain-rate projection.

The basic idea is to average volumetric strain rate over a group of
neighboring elements and then replace each element's volumetric strain
rate with the averaged one. The NMD method first assigns an area (volume
in 3D) average of the trace of $\boldsymbol{\dot{\epsilon}}_e$ to each
node $a$:

$$
\dot{\varepsilon}_{a}=\frac{\displaystyle \sum_{e}^{a\in e}\textrm{tr}(\boldsymbol{\dot{\epsilon}}_{e})\Omega_{e}}{\displaystyle \sum_{e}^{a\in e}\Omega_{e}}.
$$

Then the nodal field $\dot{\varepsilon}_a$ is interpolated back to the
element to retrieve an averaged volumetric strain rate for an element
$e$:

$$
\bar{\dot{\epsilon}}_{e}=\sum_{a\in e}\frac{1}{M}\dot{\varepsilon}_{a},
$$

where, as before, $M$ is the number of apexes in an element. 

Finally, the averaged volumetric strain rate of an element is used to modify the
original strain rate tensor. The anti-locking modification replaces the
isotropic part with $\bar{\dot{\epsilon}}_{e}$:

$$
\boldsymbol{\dot{\epsilon}}_{e}'=\textrm{dev}
(\boldsymbol{\dot{\epsilon}}_{e})+\frac{1}{D}\bar{\dot{\epsilon}}_{e}\mathbf{I}
$$

This modified strain rate tensor substitutes the original strain rate
tensor when updating strain tensor and in defining constitutive update.
For the sake of brevity, we drop the prime and use
$\boldsymbol{\dot{\epsilon}}$ to refer the modified strain rate tensor
from now on.

The strain tensor $\boldsymbol{\epsilon}$ is accumulated:

$$
\boldsymbol{\epsilon}_{e}^{t+\Delta t}=\boldsymbol{\epsilon}_{e}^{t}+\Delta t \, \dot{\boldsymbol{\epsilon}}_{e}^{t+\Delta t}
$$
