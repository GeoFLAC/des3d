---
sidebar_position: 1
---

# Overview of the solution schemes in DES3D

## Equation of motion

DES3D solves the equation of motion, i.e., linear momentum balance equation, in the following fully dynamic form:

$$
\rho\dot{\mathbf{u}}=\nabla\cdot\boldsymbol{\sigma}+\rho\mathbf{g}
\tag{1}
$$

where $\rho$ is the material density, $\bm{u}$ is the velocity
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

A weak form of the momentum balance equation is constructed by the standard finite element method: 
A weighting function is multipled on both sides and the
product is integrated over the domain. After integrating by parts and
applying Gauss theorem, we obtain the following equation for the
acceleration $\mathbf{a}_a$ of every node $a$:

$$
m_{a}\mathbf{a}_{a}=\mathbf{f}_{a}=\mathbf{f}_{a}^{int}+\mathbf{f}_{a}^{bc}+\mathbf{f}_{a}^{ext},
$$

where $m_{a}$ is the nodal mass given by

$$m_{a}=\sum_{e}\left(\int_{\Omega_{e}}N_{e}^{a}\rho_{f}d\Omega\right)
  =\sum_{e}\left(\rho_f\int_{\Omega_{e}}N_{e}^{a}d\Omega\right)
  =\sum_{e}^{a\in e}\left(\frac{1}{M}\rho_{f}\Omega_{e}\right),
$$
<!--
$\Omega_e$ is the area (volume in 3D) of the element $e$, $N_{a}^{e}$ is
the linear shape function associated with the node $a$ in the element
$e$, and $M$ is the number of apexes of an element ($M=3$ for 2D
triangles and $M=4$ for 3D tetrahedra). The summation should be
understood as done for all the elements having node $a$ as an apex. A
fictitious density, $\rho_f$, instead of the true density, $\rho$, is
used in the definition of $m_a$
in [\[eq:mA\]](#eq:mA){reference-type="eqref" reference="eq:mA"}.
Additionally, row-sum mass lumping is applied to obtain a diagonal mass
matrix in [\[eq:mA\]](#eq:mA){reference-type="eqref" reference="eq:mA"}.
We discuss the definition of $\rho_f$ in
Section [2.1.2](#sc:masss.caling){reference-type="ref"
reference="sc:masss.caling"}. The total force $\mathbf{f}_{a}$ is
composed of three parts: the internal, boundary, and external forces.
The internal force, $\mathbf{f}_{a}^{int}$, is defined as:

::: linenomath*
$$\begin{aligned}
  \mathbf{f}_{a}^{int}&=\sum_{e}\left(\int_{\Omega_{e}}\frac{\partial
      N_{a}^{e}}{\partial\mathbf{x}}\cdot\boldsymbol{\sigma}d\Omega\right)
  =\sum_{e}\left(\frac{\partial N_{a}^{e}}{\partial\mathbf{x}}
  \cdot\boldsymbol{\sigma}\int_{\Omega_{e}}d\Omega\right) \nonumber \\
  &=\sum_{e}^{a\in e}\left(\frac{\partial
      N_{a}^{e}}{\partial\mathbf{x}}\cdot\boldsymbol{\sigma}\Omega_{e}\right).
\end{aligned}$$
:::

Neumann boundary conditions are tractions prescribed on the surface of
the body. These tractions yield a boundary force denoted
$\mathbf{f}_{a}^{bc}$:

::: linenomath*
$$
\mathbf{f}_{a}^{bc}=\sum_{e}\left(\oint_{\partial\Omega_{e}}-N_{a}^{e}\boldsymbol{\sigma}\cdot\mathbf{n}dL \right)
=-\sum_{e}^{a\in s,\: s\in\partial\Omega_{e}}\left(\frac{1}{M-1}\boldsymbol{\sigma}_{s}\cdot\mathbf{n}_{s}L_{s}\right).$$
:::

The summation is over the boundary segment $s$, which has a length
$L_{s}$ (surface area in 3D), the outward, unit normal vector
$\mathbf{n}$, and a prescribed (constant) stress
$\boldsymbol{\sigma}_{s}$ on the Neumann boundary. The external force,
$\mathbf{f}_{a}^{ext}$, is given by:

::: linenomath*
$$\mathbf{f}_{a}^{ext}=\sum_{e}\left(\int_{\Omega_{e}}N_{a}^{e}\rho\mathbf{g}d\Omega\right)
=\sum_{e}\left(\rho\mathbf{g}\int_{\Omega_{e}}N_{a}^{e}d\Omega\right)
=\sum_{e}^{a\in e}\left(\frac{1}{M}\rho\mathbf{g}\Omega_{e}\right).$$
:::

When deriving the equations above, we utilize the fact that $\rho_f$,
$\rho$, $\frac{\partial N_{a}^{e}}{\partial\mathbf{x}}$,
$\boldsymbol{\sigma}$, and $\mathbf{g}$ are constants on each element,
and these identities:

::: linenomath*
$$\int_{\Omega_e}d\Omega=\Omega_{e}, \quad
\int_{\Omega_e}N_{a}^{e}d\Omega=\frac{1}{M}\Omega_{e}, \quad
\oint_{\partial\Omega_{e}}N_{a}^{e}dL=\frac{1}{M-1}L_s.$$
:::

We are interested in tectonic deformation, which can be properly
simulated in a quasi-static fashion. Thus, we apply a technique called
"dynamic relaxation," which enables us to achieve a static equilibrium
from the dynamic momentum equation by damping out the intertial force.
Additionally, using "mass scaling," we substitute the true density by a
fictitious scaled density that allows us to increase the size of
admissible stable time steps in the explicit time integration scheme.
That is, using the resulting "scaled" acceleration and velocity, we
compute an instantaneous velocity and position of each node in the mesh,
which updates the model geometry at each time step. Each of these
modifications is detailed in the following sections.

### Dynamic relaxation

Given that our focus lies in LTM, high-frequency vibrations are not
relevant to the overall deformation pattern. A strong and efficient
damping is necessary to achieve quasi-static solutions of the dynamic
equation. Complementarily, force amplification might be needed to
accelerate the transient process to achieve equilibrium. Therefore, we
either damp or amplify the total net force in the discretized nodal
momentum
equation [\[eq:nodalmotion\]](#eq:nodalmotion){reference-type="eqref"
reference="eq:nodalmotion"} according to the direction of
velocity [@Cundall1989]:

::: linenomath*
$$ma_{i}  =  (\mathbf{f}_{damped})_{i} =  f_{i}-0.8\,\text{sgn}(u_{i})|f_{i}|,$$
:::

where subscript $i$ denotes the $i$-th component of a vector and
$\text{sgn}$ denotes the signum function. The motivation for the choice
of damping/amplification is based on the simple observation that in an
under-damped oscillator, the direction of force is always opposite to
the velocity direction, while in an over-damped system, the direction of
the force is parallel to the velocity direction. We found that this
choice of damping/amplification accomplishes the design goals
satisfactorily (i.e., robustly and economically).

### Mass scaling {#sc:masss.caling}

The Courant-Friedrichs-Lewy (CFL) condition imposes a fundamental limit
on the time step size for an explicit time marching scheme. In the
explicit EVP approach used in DynEarthSol2D, the $p$-wave velocity sets
the largest possible time step size. For instance, using relevant
parameters for lithospheric modeling, a $p$-wave speed of $\sim10^{3}$
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

::: linenomath*
$$u_{elastic}=\sqrt{K_{s}/\rho_{f}}=c_{1}u_{tectonic},$$
:::

where $K_{s}$ is the bulk modulus of the material, $\rho_{f}$ is a
fictitious scaled density and $c_{1}$ is a constant. When $c_{1}$ is too
small, that is, the density is scaled up too high, dynamic instabilities
might occur. In this case, the fictitious elastic wave is too slow to
relax the stress back to quasi-equilibrium, therefore the kinetic energy
becomes too large, breaking the assumption of the quasi-static
state [e.g., @Chung1998]. When the density scaling is insufficient
(i.e., $c_{1}$ is too large), the simulation becomes too time consuming.
As $c_{1}$ approaches $10^{12},$ the fictitious density approaches the
material (true) density. The optimal value of $c_{1}$ depends on the
rheology parameters, resolution, and domain size. We find that $c_{1}$
in the range of $10^{4}$ to $10^{8}$ is adequate for our simulation
targets. Unfortunately, the choice of $c_{1}$ is currently empirical. We
are working to devise a consistent way of finding the optimal value of
$c_{1}$.

## Nodal Mixed Discretization

The linear triangular elements used in DynEarthSol2D are known to suffer
volumetric locking when subject to incompressible deformations [e.g.,
@Hughes2000]. Since incompressible plastic or viscous flow are often
needed in LTM, we adopt an anti-volumetric locking correction based on
the nodal mixed discretization (NMD)
methodology [@Detournay2006; @DeMicheli2009].

The strain rate of element $e$, $\boldsymbol{\dot{\epsilon}}_e$, is
computed from the velocity:

::: linenomath*
$$\dot{\epsilon}_{e,ij}^{t+\Delta t}=\frac{1}{2}\sum_{a\in e}\left(\frac{\partial N_{a}^{e}}{\partial x_{i}}u_{a,j}^{t+\Delta t}+\frac{\partial N_{a}^{e}}{\partial x_{j}}u_{a,i}^{t+\Delta t}\right),$$
:::

where $i$, $j$ are spatial indices. The strain rate tensor can be
decomposed into the deviatoric and the isotropic parts:

::: linenomath*
$$\boldsymbol{\dot{\epsilon}}_{e}=\textrm{dev}(\boldsymbol{\dot{\epsilon}}_{e})+\frac{1}{D}\textrm{tr}(\boldsymbol{\dot{\epsilon}}_{e})\mathbf{I},$$
:::

where $\textrm{dev}(\cdot)$ represents an operator returning the
deviatoric tensor, $\textrm{tr}(\cdot)$ is an operator returning the
trace of the tensor, $D$ is the number of diagonal terms of the tensor
(2 for 2D case and 3 for 3D or plain strain cases), and $\mathbf{I}$ is
an appropriate identity tensor. (When plane strain description is used,
that is, $\epsilon_{yy}=0$ and ${\dot\epsilon}_{yy}=0$, but
$\sigma_{yy}$ can be non-zero and must be included in the calculation.)

The basic idea is to average volumetric strain rate over a group of
neighboring elements and then replace each element's volumetric strain
rate with the averaged one. The NMD method first assigns an area (volume
in 3D) average of the trace of $\boldsymbol{\dot{\epsilon}}_e$ to each
node $a$:

::: linenomath*
$$\dot{\varepsilon}_{a}=\frac{\displaystyle \sum_{e}^{a\in e}\textrm{tr}(\boldsymbol{\dot{\epsilon}}_{e})\Omega_{e}}{\displaystyle \sum_{e}^{a\in e}\Omega_{e}}.$$
:::

Then the nodal field $\dot{\varepsilon}_a$ is interpolated back to the
element to retrieve an averaged volumetric strain rate for an element
$e$:

::: linenomath*
$$\bar{\dot{\epsilon}}_{e}=\sum_{a\in e}\frac{1}{M}\dot{\varepsilon}_{a}.$$
:::

where, as before, $M$ is the number of apexes in an element. Finally,
the averaged volumetric strain rate of an element is used to modify the
original strain rate tensor. The anti-locking modification replaces the
isotropic part with $\bar{\dot{\epsilon}}_{e}$:

::: linenomath*
$$\boldsymbol{\dot{\epsilon}}_{e}'=\textrm{dev}
(\boldsymbol{\dot{\epsilon}}_{e})+\frac{1}{D}\bar{\dot{\epsilon}}_{e}\mathbf{I}$$
:::

This modified strain rate tensor substitutes the original strain rate
tensor when updating strain tensor and in defining constitutive update.
For the sake of brevity, we drop the prime and use
$\boldsymbol{\dot{\epsilon}}$ to refer the modified strain rate tensor
from now on.

The strain tensor $\boldsymbol{\epsilon}$ is accumulated:

::: linenomath*
$$\boldsymbol{\epsilon}_{e}^{t+\Delta t}=\boldsymbol{\epsilon}_{e}^{t}+\Delta t \, \dot{\boldsymbol{\epsilon}}_{e}^{t+\Delta t}$$
:::

## Constitutive update

The stress tensor is updated using the strain rate and strain tensors
according to an appropriate constitutive relationship. Since the stress
update calculations are performed at the element level, we drop the
subscript $e$ to simplify notation. The EVP material model is
approximated by a composite rheology which uses visco-elastic and
elasto-plastic sub-models. With the bulk modulus $K_{s}$, shear modulus
$G$, viscosity $\eta$, cohesion $C$, and internal friction angle $\phi$,
we calculate the visco-elastic stress $\boldsymbol{\sigma}_{ve}$ and the
elasto-plastic stress $\boldsymbol{\sigma}_{ep}$.

The visco-elastic stress increment $\Delta\boldsymbol{\sigma}_{ve}$ is
calculated assuming a linear Maxwell material, where a total deviatoric
strain increment $\Delta\boldsymbol{\epsilon}$ is composed of the
elastic and the viscous components while the deviatoric stress increment
is identical for each component:

::: linenomath*
$$\textrm{dev}(\Delta\boldsymbol{\epsilon})=\frac{\textrm{dev}(\Delta\boldsymbol{\sigma}_{ve})}{2G}+\frac{\textrm{dev}(\boldsymbol{\sigma}_{ve})\Delta t}{2\eta}$$
:::

Substituting $\Delta\boldsymbol{\epsilon}$ with
$\boldsymbol{\epsilon}^{t+\Delta t}-\boldsymbol{\epsilon}^{t},$
$\Delta\boldsymbol{\sigma}_{ve}$ with
$\boldsymbol{\sigma}_{ve}^{t+\Delta t}-\boldsymbol{\sigma}^{t}$, and
$\boldsymbol{\sigma}_{ve}$ with $(\boldsymbol{\sigma}_{ve}^{t+\Delta
  t}+\boldsymbol{\sigma}^{t})/2$, the equation above is reduced to:

::: linenomath*
$$\textrm{dev}(\boldsymbol{\sigma}_{ve}^{t+\Delta t})=\dfrac{\left(1-\frac{G\Delta t}{2\eta}\right)\textrm{dev}(\boldsymbol{\sigma}^{t})+2G\textrm{\ensuremath{\cdot}dev}(\boldsymbol{\epsilon}^{t+\Delta t}-\boldsymbol{\epsilon}^{t})}{1+\frac{G\Delta t}{2\eta}}$$
:::

The isotropic stress components are updated based on the volume change.
As a result, the visco-elastic stress is:

::: linenomath*
$$\boldsymbol{\sigma}_{ve}^{t+\Delta
    t}=\textrm{dev}(\boldsymbol{\sigma}_{ve}^{t+\Delta t})+\Delta t \ K_{s}\textrm{tr}(\boldsymbol{\dot{\epsilon}}^{t+\Delta t})\mathbf{I}.$$
:::

The elasto-plastic stress $\boldsymbol{\sigma}_{ep}$ is computed using
linear elasticity and the Mohr-Coulomb (MC) failure criterion with a
general (associative or non-associative) flow rule. Following a standard
operator-splitting scheme [e.g.,
@Lubliner1990; @SimoHugh2004; @Wilkins1964a], an elastic trial stress
$\boldsymbol{\sigma}_{\text{el}}^{t+\Delta t}$ is first calculated as

::: linenomath*
$$\boldsymbol{\sigma}_{\text{el}}^{t+\Delta t}=\boldsymbol{\sigma}^t 
+ (K_s - \frac{2}{3}G)\textrm{tr}(\boldsymbol{\dot{\epsilon}}^{t+\Delta t})\mathbf{I}\Delta t
+ 2G\boldsymbol{\dot{\epsilon}}^{t+\Delta t}\Delta t.$$
:::

If the elastic trial stress, $\boldsymbol{\sigma}_{\text{el}}^{t+\Delta
  t}$, is on or within a yield surface, that is,
$f\left(\boldsymbol{\sigma}_{\text{el}}^{t+\Delta t}\right)\geq0,$ where
$f$ is the yield function, then the stress does not need a plastic
correction. So, $\boldsymbol{\sigma}^{t+\Delta t}_{ep}$ is set to be
equal to $\boldsymbol{\sigma}_{\text{el}}^{t+\Delta t}$. However, if
$\boldsymbol{\sigma}_{\text{el}}^{t+\Delta t}$ is outside the yield
surface, we project it onto the yield surface using a return-mapping
algorithm [@SimoHugh2004].

In the case of a Mohr-Coulomb material, it is convenient to express the
yield function for *shear failure* in terms of principal stresses:

::: linenomath*
$$f_{s}(\sigma_{1},\sigma_{3})=\sigma_{1}-N_{\phi}\sigma_{3}+2C\sqrt{N_{\phi}},
$$
:::

where $\sigma_{1}$ and $\sigma_{3}$ are the maximal and minimal
compressive principal stresses with the sign convention that tension is
positive (i.e., $\sigma_1\le\sigma_2\le\sigma_3$), $C$ is the material's
cohesion, $N_{\phi} = \frac{1+\sin\phi}{1-\sin\phi}$,
$\sqrt{N_{\phi}} =\frac{\cos\phi}{1-\sin\phi}$, and $\phi$ is an
internal friction angle ($<90^{\circ}$). The yield function for
*tensile* failure is defined as

::: linenomath*
$$f_{t}(\sigma_{3})=\sigma_{3}-\sigma_{t},
$$
:::

where $\sigma_{t}$ is the tension cut-off. If a value for the tension
cut-off is given as a parameter, the smallest value between the
theoretical limit ($C/\tan\phi$) and the given value is assigned to
$\sigma_{t}$. This comparison is required because the theoretical limit
is not constant in the strain weakening case, where the material
cohesion, $C$, and the friction angle $\phi$ may change.

To guarantee a unique decision on the mode of yielding (shear versus
tensile), we define an additional function,
$f_{h}(\sigma_{1},\sigma_{3})$, which bisects the obtuse angle made by
two yield functions on the $\sigma_1$-$\sigma_3$ plane, as

::: linenomath*
$$\begin{aligned}
  f_{h}(\sigma_{1},\sigma_{3})  &=  \sigma_{3}-\sigma_{t}
  +\left(\sqrt{N_{\phi}^{2}+1}+N_{\phi}\right)
  \left(\sigma_{1}-N_{\phi}\sigma_{t}+2C\sqrt{N_{\phi}}\right).
\end{aligned}$$
:::

Once yielding is identified, that is, $f_{s}( \sigma_{el,1},
\sigma_{el,3})<0$ or $f_{t}(\sigma_{el,3})>0$, the mode of failure
(shear or tensile) is decided based on the value of $f_{h}$, in other
words, shear failure occurs if $f_{h}(\sigma_{el,1},\sigma_{el,3})<0$,
tensile failure occurs otherwise.

The flow rule for frictional materials is in general non-associative,
that is, the direction of plastic flow in the principal stress space
during plastic flow is not the same as the direction of the vector
normal to the yield surface. As in the definitions of yield functions,
the plastic flow potential for *shear* failure in the Mohr-Coulomb model
can be defined as

::: linenomath*
$$g_{s}\left(\sigma_{1},\sigma_{3}\right)=\sigma_{1}-\frac{1+\sin\psi}{1-\sin\psi}\sigma_{3},
$$
:::

where $\psi$ is the dilation angle. Likewise, the *tensile* flow
potential is given as

::: linenomath*
$$g_{t}\left(\sigma_{3}\right)=\sigma_{3}-\sigma_{t}.
$$
:::

In the presence of plasticity, the total strain increment
$\Delta\boldsymbol{\epsilon}$ is given by

::: linenomath*
$$\Delta\boldsymbol{\epsilon}=\Delta\boldsymbol{\epsilon}_{\text{el}}+
      \Delta\boldsymbol{\epsilon}_{\text{pl}},
$$
:::

where $\Delta\boldsymbol{\epsilon}_{\text{el}}$ and
$\Delta\boldsymbol{\epsilon}_{\text{pl}}$ are the elastic and plastic
strain increments, respectively. The plastic strain increment is normal
to the flow potential surface and can be written as

::: linenomath*
$$\Delta\boldsymbol{\epsilon}_{\text{pl}}=\beta\frac{\partial
  g}{\partial\boldsymbol{\sigma}},
$$
:::

where $\beta\,$ is the plastic flow magnitude. $\beta\,$ is computed by
requiring that the updated stress state lies on the yield surface,

::: linenomath*
$$f\left(\boldsymbol{\sigma}_{ep}^{t+\Delta t}\right)=f\left(\boldsymbol{\sigma}^{t}+\Delta\boldsymbol{\sigma}_{ep}\right)=0.
$$
:::

In the principal component representation,
$\sigma_{A}=E_{AB}\epsilon_{B}$ where $\sigma_{A}$ and $\epsilon_{A}$
are the principal stress and strain, respectively, and $\boldsymbol{E}$
is a corresponding elastic moduli matrix with components:

::: linenomath*
$$\begin{aligned}
E_{AB}&=\left(K_s-\frac{2}{3}G\right)&&\text{if   }A\ne B,\\
E_{AB}&=\left(K_s+\frac{4}{3}G\right) &&\text{otherwise.}
\end{aligned}$$
:::

By applying the consistency
condition [\[eq:consistency condition\]](#eq:consistency condition){reference-type="eqref"
reference="eq:consistency condition"} and using
$\boldsymbol{\sigma}_{\text{el}}^{t+\Delta
  t}=\boldsymbol{\sigma}^{t}+\boldsymbol{E}\cdot\Delta\boldsymbol{\epsilon}$
(in the principal component representation), we obtain the following
formulae for $\beta$

::: linenomath*
$$\beta\,=\frac{\sigma_{\text{el},1}^{t+\Delta t}-N_{\phi}\sigma_{\text{el},3}^{t+\Delta t}+2C\sqrt{N_{\phi}}}{\sum_B\left(E_{1B}\frac{\partial g_{s}}{\partial\sigma_{B}}-N_{\phi}E_{3B}\frac{\partial g_{s}}{\partial\sigma_{B}}\right)}
  \qquad\text{(for shear failure,)}
$$
:::

and

::: linenomath*
$$\beta\,=\frac{\sigma_{\text{el},3}^{t+\Delta t}-\sigma_{t}}{\frac{\partial g_{t}}{\partial\sigma_{3}}}
  \qquad\text{(for tensile failure.)}
$$
:::

Likewise, $\partial g/\partial \boldsymbol{\sigma}$ takes different
forms according to the failure mode:

::: linenomath*
$$\begin{split}
    \partial g/\partial \sigma_{1} & = 1 \\
    \partial g/\partial \sigma_{2} & = 0 \\
    \partial g/\partial \sigma_{3} & = -\frac{1+\sin\psi}{1-\sin\psi}
  \end{split}
  \qquad\text{(for shear failure,)}
$$
:::

and

::: linenomath*
$$\begin{split}
    \partial g/\partial \sigma_{1} & = 0 \\
    \partial g/\partial \sigma_{2} & = 0 \\
    \partial g/\partial \sigma_{3} & = 1
  \end{split}
  \qquad\text{(for tensile failure.)}
$$
:::

Once $\Delta\boldsymbol{\epsilon}_{pl}$ is computed as in
[\[eq:plastic strain increment\]](#eq:plastic strain increment){reference-type="eqref"
reference="eq:plastic strain increment"} using [\[eq:flow parameter for
  shear failure\]](#eq:flow parameter for
  shear failure){reference-type="eqref" reference="eq:flow parameter for
  shear failure"} and
[\[eq:flow direction for shear failure\]](#eq:flow direction for shear failure){reference-type="eqref"
reference="eq:flow direction for shear failure"} or
[\[eq:flow parameter for tensile failure\]](#eq:flow parameter for tensile failure){reference-type="eqref"
reference="eq:flow parameter for tensile failure"} and [\[eq:flow
  direction for tensile failure\]](#eq:flow
  direction for tensile failure){reference-type="eqref"
reference="eq:flow
  direction for tensile failure"}, $\boldsymbol{\sigma}_{ep}$ is updated
as

::: linenomath*
$$\boldsymbol{\sigma}_{ep} = \boldsymbol{\sigma}_{\text{el}}^{t+\Delta t} - \boldsymbol{E}\cdot\Delta\boldsymbol{\epsilon}_{\text{pl}}.$$
:::

in the principal component representation and transformed back to the
orignal coordinate system.

After the visco-elastic stress $\boldsymbol{\sigma}_{ve}$ and
elasto-plastic stress $\boldsymbol{\sigma}_{ep}$ are evaluated, we
compute the second invariant of the deviatoric components of each. If
the visco-elastic stress has a smaller second invariant ($J_2$),
$\boldsymbol{\sigma}_{ve}$ is be used as the updated stress; otherwise,
$\boldsymbol{\sigma}_{ep}$ is used.

The fundamental deformation measures in DynEarthSol2D are strain rates.
Thus, the stress update by rate-independent constitutive models like
elasto-plastic stresses need to be considered as the time-integration of
the rate form of the corresponding stresses. Since a stress rate is not
frame-indifferent in general, an objective (or co-rotational) stress
rate needs to be constructed and integrated instead. The Jaumann stress
rate is our choice for DynEarthSol2D among the possible objective rates
because of its simplicity.

The Jaumann stress rate ($\check{\dot{\sigma}}$) is defined as

::: linenomath*
$$\check{\dot{\boldsymbol{\sigma}}} = \dot{\boldsymbol{\sigma}} - \boldsymbol{\omega}\cdot\boldsymbol{\sigma} + \boldsymbol{\sigma}\cdot\boldsymbol{\omega},$$
:::

where $\boldsymbol{\omega}$ is the spin tensor, which is defined as,

::: linenomath*
$$\omega_{ij}=\dfrac{1}{2}\left(\dfrac{\partial u_i}{\partial
  x_j}-\dfrac{\partial u_j}{\partial x_i}\right).$$
:::

Based on this definition, the new objective stress
($\check{\boldsymbol{\sigma}}^{t+\Delta t}$) is,

::: linenomath*
$$\check{\boldsymbol{\sigma}}^{t+\Delta t} = \boldsymbol{\sigma}^{t+\Delta t} + \Delta t(\boldsymbol{\sigma}^{t+\Delta t}\cdot\boldsymbol{w}^{t+\Delta t} - \boldsymbol{w}^{t+\Delta t}\cdot\boldsymbol{\sigma}^{t+\Delta t}),$$
:::

where $\boldsymbol{\sigma}^{t+\Delta t}$ is the updated stress equal to
either $\boldsymbol{\sigma}_{ve}$ or $\boldsymbol{\sigma}_{ep}$,
depending on which has a lower value of $J_2$.

## Velocity and displacement update

The velocity is updated with the damped acceleration, but subject to the
prescribed velocity boundary conditions, that is:

::: linenomath*
$$\mathbf{u}_{a}^{t+\Delta t}=\mathbf{u}_{a}^{t}+\Delta t \, \mathbf{a}_{a}^{t+\Delta t}.$$
:::

The position $\mathbf{x}_{a}$ of the node $a$ is updated by:

::: linenomath*
$$\mathbf{x}_{a}^{t+\Delta t}=\mathbf{x}_{a}^{t}+\Delta t \, \mathbf{u}_{a}^{t+\Delta t}.$$
:::

Since the mesh is changed, the shape function derivates $N_{a}^{e}$ and
the element volume $\Omega_{e}$ are updated every time step.

## Modeling thermal evolution

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
