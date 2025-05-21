---
sidebar_position: 5
---

# Constitutive update

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

$$
\textrm{dev}(\Delta\boldsymbol{\epsilon})=\frac{\textrm{dev}(\Delta\boldsymbol{\sigma}_{ve})}{2G}+\frac{\textrm{dev}(\boldsymbol{\sigma}_{ve})\Delta t}{2\eta}
$$

Substituting $\Delta\boldsymbol{\epsilon}$ with
$\boldsymbol{\epsilon}^{t+\Delta t}-\boldsymbol{\epsilon}^{t},$
$\Delta\boldsymbol{\sigma}_{ve}$ with
$\boldsymbol{\sigma}_{ve}^{t+\Delta t}-\boldsymbol{\sigma}^{t}$, and
$\boldsymbol{\sigma}_{ve}$ with $(\boldsymbol{\sigma}_{ve}^{t+\Delta
  t}+\boldsymbol{\sigma}^{t})/2$, the equation above is reduced to:

$$
\textrm{dev}(\boldsymbol{\sigma}_{ve}^{t+\Delta t})=\dfrac{\left(1-\frac{G\Delta t}{2\eta}\right)\textrm{dev}(\boldsymbol{\sigma}^{t})+2G\textrm{\ensuremath{\cdot}dev}(\boldsymbol{\epsilon}^{t+\Delta t}-\boldsymbol{\epsilon}^{t})}{1+\frac{G\Delta t}{2\eta}}
$$

The isotropic stress components are updated based on the volume change.
As a result, the visco-elastic stress is:

$$
\boldsymbol{\sigma}_{ve}^{t+\Delta
    t}=\textrm{dev}(\boldsymbol{\sigma}_{ve}^{t+\Delta t})+\Delta t \ K_{s}\textrm{tr}(\boldsymbol{\dot{\epsilon}}^{t+\Delta t})\mathbf{I}.
$$

The elasto-plastic stress $\boldsymbol{\sigma}_{ep}$ is computed using
linear elasticity and the Mohr-Coulomb (MC) failure criterion with a
general (associative or non-associative) flow rule. Following a standard
operator-splitting scheme [e.g.,
@Lubliner1990; @SimoHugh2004; @Wilkins1964a], an elastic trial stress
$\boldsymbol{\sigma}_{\text{el}}^{t+\Delta t}$ is first calculated as

$$
\boldsymbol{\sigma}_{\text{el}}^{t+\Delta t}=\boldsymbol{\sigma}^t 
+ (K_s - \frac{2}{3}G)\textrm{tr}(\boldsymbol{\dot{\epsilon}}^{t+\Delta t})\mathbf{I}\Delta t
+ 2G\boldsymbol{\dot{\epsilon}}^{t+\Delta t}\Delta t.
$$

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

$$
f_{s}(\sigma_{1},\sigma_{3})=\sigma_{1}-N_{\phi}\sigma_{3}+2C\sqrt{N_{\phi}},
$$

where $\sigma_{1}$ and $\sigma_{3}$ are the maximal and minimal
compressive principal stresses with the sign convention that tension is
positive (i.e., $\sigma_1\le\sigma_2\le\sigma_3$), $C$ is the material's
cohesion, $N_{\phi} = \frac{1+\sin\phi}{1-\sin\phi}$,
$\sqrt{N_{\phi}} =\frac{\cos\phi}{1-\sin\phi}$, and $\phi$ is an
internal friction angle ($<90^{\circ}$). The yield function for
*tensile* failure is defined as

$$
f_{t}(\sigma_{3})=\sigma_{3}-\sigma_{t},
$$

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

$$
\begin{aligned}
  f_{h}(\sigma_{1},\sigma_{3})  &=  \sigma_{3}-\sigma_{t}
  +\left(\sqrt{N_{\phi}^{2}+1}+N_{\phi}\right)
  \left(\sigma_{1}-N_{\phi}\sigma_{t}+2C\sqrt{N_{\phi}}\right).
\end{aligned}
$$

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

$$
g_{s}\left(\sigma_{1},\sigma_{3}\right)=\sigma_{1}-\frac{1+\sin\psi}{1-\sin\psi}\sigma_{3},
$$

where $\psi$ is the dilation angle. Likewise, the *tensile* flow
potential is given as

$$
g_{t}\left(\sigma_{3}\right)=\sigma_{3}-\sigma_{t}.
$$

In the presence of plasticity, the total strain increment
$\Delta\boldsymbol{\epsilon}$ is given by

$$
\Delta\boldsymbol{\epsilon}=\Delta\boldsymbol{\epsilon}_{\text{el}}+
      \Delta\boldsymbol{\epsilon}_{\text{pl}},
$$

where $\Delta\boldsymbol{\epsilon}_{\text{el}}$ and
$\Delta\boldsymbol{\epsilon}_{\text{pl}}$ are the elastic and plastic
strain increments, respectively. The plastic strain increment is normal
to the flow potential surface and can be written as

$$\Delta\boldsymbol{\epsilon}_{\text{pl}}=\beta\frac{\partial
  g}{\partial\boldsymbol{\sigma}},
$$

where $\beta\,$ is the plastic flow magnitude. $\beta\,$ is computed by
requiring that the updated stress state lies on the yield surface,

$$f\left(\boldsymbol{\sigma}_{ep}^{t+\Delta t}\right)=f\left(\boldsymbol{\sigma}^{t}+\Delta\boldsymbol{\sigma}_{ep}\right)=0.
$$

In the principal component representation,
$\sigma_{A}=E_{AB}\epsilon_{B}$ where $\sigma_{A}$ and $\epsilon_{A}$
are the principal stress and strain, respectively, and $\boldsymbol{E}$
is a corresponding elastic moduli matrix with components:

$$
\begin{aligned}
E_{AB}&=\left(K_s-\frac{2}{3}G\right)&&\text{if   }A\ne B,\\
E_{AB}&=\left(K_s+\frac{4}{3}G\right) &&\text{otherwise.}
\end{aligned}
$$

By applying the consistency
condition [\[eq:consistency condition\]](#eq:consistency condition){reference-type="eqref"
reference="eq:consistency condition"} and using
$\boldsymbol{\sigma}_{\text{el}}^{t+\Delta
  t}=\boldsymbol{\sigma}^{t}+\boldsymbol{E}\cdot\Delta\boldsymbol{\epsilon}$
(in the principal component representation), we obtain the following
formulae for $\beta$

$$
\beta\,=\frac{\sigma_{\text{el},1}^{t+\Delta t}-N_{\phi}\sigma_{\text{el},3}^{t+\Delta t}+2C\sqrt{N_{\phi}}}{\sum_B\left(E_{1B}\frac{\partial g_{s}}{\partial\sigma_{B}}-N_{\phi}E_{3B}\frac{\partial g_{s}}{\partial\sigma_{B}}\right)}
  \qquad\text{for shear failure,}
$$

and

$$
\beta\,=\frac{\sigma_{\text{el},3}^{t+\Delta t}-\sigma_{t}}{\frac{\partial g_{t}}{\partial\sigma_{3}}}
  \qquad\text{for tensile failure.}
$$

Likewise, $\partial g/\partial \boldsymbol{\sigma}$ takes different
forms according to the failure mode:

$$\begin{split}
    \partial g/\partial \sigma_{1} & = 1 \\
    \partial g/\partial \sigma_{2} & = 0 \\
    \partial g/\partial \sigma_{3} & = -\frac{1+\sin\psi}{1-\sin\psi}
  \end{split}
  \qquad\text{(for shear failure,)}
$$

and

$$\begin{split}
    \partial g/\partial \sigma_{1} & = 0 \\
    \partial g/\partial \sigma_{2} & = 0 \\
    \partial g/\partial \sigma_{3} & = 1
  \end{split}
  \qquad\text{(for tensile failure.)}
$$

Once $\Delta\boldsymbol{\epsilon}_{pl}$ is computed, $\boldsymbol{\sigma}_{ep}$ is updated
as

$$
\boldsymbol{\sigma}_{ep} = \boldsymbol{\sigma}_{\text{el}}^{t+\Delta t} - \boldsymbol{E}\cdot\Delta\boldsymbol{\epsilon}_{\text{pl}}.
$$

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

$$
\check{\dot{\boldsymbol{\sigma}}} = \dot{\boldsymbol{\sigma}} - \boldsymbol{\omega}\cdot\boldsymbol{\sigma} + \boldsymbol{\sigma}\cdot\boldsymbol{\omega},
$$

where $\boldsymbol{\omega}$ is the spin tensor, which is defined as,

$$
\omega_{ij}=\dfrac{1}{2}\left(\dfrac{\partial u_i}{\partial
  x_j}-\dfrac{\partial u_j}{\partial x_i}\right).
$$

Based on this definition, the new objective stress
($\check{\boldsymbol{\sigma}}^{t+\Delta t}$) is,

$$
\check{\boldsymbol{\sigma}}^{t+\Delta t} = \boldsymbol{\sigma}^{t+\Delta t} + \Delta t(\boldsymbol{\sigma}^{t+\Delta t}\cdot\boldsymbol{w}^{t+\Delta t} - \boldsymbol{w}^{t+\Delta t}\cdot\boldsymbol{\sigma}^{t+\Delta t}),
$$

where $\boldsymbol{\sigma}^{t+\Delta t}$ is the updated stress equal to
either $\boldsymbol{\sigma}_{ve}$ or $\boldsymbol{\sigma}_{ep}$,
depending on which has a lower value of $J_2$.
