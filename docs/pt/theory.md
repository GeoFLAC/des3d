---
sidebar_position: 1
slug: /theory/pt
title: Theory
---

# Theory

With `control.has_PT = yes`, DES3D solves for quasi-static mechanical
equilibrium within a physical timestep. The finite-element force assembly
uses the [spatial discretization](../theory/theory.md#discretization) shared with the
explicit momentum path. PT adds an inner relaxation loop whose candidates
all refer to the same physical increment. Configuration and diagnostic
details are in [Choosing a mechanical solver](./index.md).

## One physical increment, many trials

Let $H_n$ denote the material history at the start of a physical step,
$\Delta t$ its physical duration, and $\mathbf{x}_n$ its reference mesh.
Each candidate velocity $\mathbf{v}^{(k)}$ defines a constitutive trial

$$
H^{(k)}=\mathcal{C}\left(H_n,\nabla\mathbf{v}^{(k)},
\Delta t;\mathbf{x}_n\right).
$$

$\mathcal{C}$ is the existing material update, including applicable plastic,
viscous and frictional history. Every evaluation restores $H_n$ first.
Consequently, $k$ trials do not represent $k\Delta t$ of aging or viscous
relaxation. Mixed stress correction is applied before candidate force
evaluation. Acceptance commits the full constitutive candidate.

Thermal diffusion advances temperature once before a physical PT solve,
and temperature remains fixed during its trials. Hydraulic transport,
mesh motion, stress rotation and remeshing follow accepted mechanics outside
the loop. Gradients, volumes, facet areas and normals remain on the reference
mesh during mechanics. For moving-mesh physical steps, height-dependent
foundation, water and side-support pressures include the candidate vertical
displacement in their height argument. This is an incremental pressure-load
correction, not a complete finite-deformation follower-load formulation.

## Force balance in the admissible velocity space

Write the undamped assembled force as

$$
\mathbf{f}=\mathbf{f}^{\mathrm{int}}
 +\mathbf{f}^{\mathrm{bc}}+\mathbf{f}^{\mathrm{ext}}.
$$

Let $P$ be the orthogonal projector onto admissible homogeneous velocity
perturbations, and let $r$ be its total free rank. PT measures

$$
R=\sqrt{\frac{\lVert P\mathbf{f}\rVert_2^2}{r}},\qquad r>0.
$$

For $r=0$, the free residual is defined as zero. On axis-aligned roller
boundaries this removes constrained force components. Oblique constraints
require projection onto their free directions. Support reactions are
excluded; applied tractions, body forces and foundation loads remain.
Artificial damping is excluded as well. The units are N/m in 2D and N in 3D.

The affine velocity constraints enforce prescribed motion. Their homogeneous
counterparts define the perturbation space. DES3D retains the ordered
boundary dispatch and corner precedence of its boundary conditions;
arbitrary contradictory prescriptions are not simultaneously enforced.

The default acceptance threshold uses an absolute tolerance plus a relative
tolerance times the first warm candidate's residual. The alternative
running-scale criterion and its limitations are given in the
[convergence reference](./index.md#understand-convergence).

## Starting candidates

The previous physical velocity supplies the warm start. If that candidate
already meets the threshold, it is accepted. Otherwise, a physical solve
can also evaluate the affine prescribed velocity with zero free motion,
and retain the finite candidate with the smaller residual. Both candidates
evaluate the complete physical-dt constitutive response.

This matters for a held elastic load: reusing the previous loading velocity
could apply the same compression again. Zero free motion can represent its
equilibrium. For a Maxwell material, however, zero velocity still permits
constitutive relaxation over $\Delta t$ and need not satisfy the imposed
traction. A new equilibrium velocity must then produce continued creep.
The [elastic](./tutorials/elastic.md) and [Maxwell](./tutorials/maxwell.md)
tutorials demonstrate the distinction.

## Relaxation schemes

`PT_option = 0` uses localized dual-time stress/velocity relaxation. Its
factors depend on mesh heights, effective viscosity, `PT_CFL` and `PT_Re`,
following the effective-viscosity/dual-time approach of
[Räss et al. (2022)](https://gmd.copernicus.org/articles/15/5757/2022/).
Lagged stress is solver scratch; acceptance always checks the full
constitutive candidate.

`PT_option = 1` uses adaptive dynamic relaxation. A Gershgorin row-sum
construction supplies nodal fictitious masses from the elastic/viscous
velocity stiffness. A secant Rayleigh quotient estimates a low mode for
adaptive damping; momentum is discarded when it opposes the current force.
There is no lagged stress, and `PT_CFL` and `PT_Re` are unused.

The row-sum construction bounds the magnitude of eigenvalues of the
mass-scaled linear reference operator. It does not prove stability of the
full nonlinear constrained problem. Both options share the force criterion,
material acceptance and rollback behavior.

## Initial equilibrium and diagnostic time level

Initial body-force equilibration uses homogeneous supports and the
instantaneous material skeleton, without transport, viscous relaxation or
physical frictional aging. Plastic history is committed only for the
accepted initial candidate. Maxwell and EVP initialization use their
instantaneous skeletons; a pure viscous material has no such skeleton and
is rejected for this initialization. Initial equilibrium precedes frame-zero
output and monitor initialization, and completion is checkpointed.

The saved `PT residual force` describes the accepted reference-geometry
solve **before** hydraulic transport, mesh motion and stress rotation. For
physical steps with thermal diffusion enabled, temperature has already been
advanced. The report's `stage=before_physical_updates` refers to the later
updates, not the preceding thermal stage. A force reconstructed from
saved post-rotation stress can differ slightly, even on a fixed mesh.
Remeshing invalidates this diagnostic until another solve is accepted.
See [PT force output](../usage/visualize.md#pt-force-output).

Neither relaxation scheme can produce a stable quasi-static equilibrium
where the model has none. Strain softening can introduce negative stiffness;
changing the numerical relaxation does not supply physical regularization.
The [implementation notes](https://github.com/GeoFLAC/DynEarthSol/blob/master/doc/pt-solver.md)
and [validation record](https://github.com/GeoFLAC/DynEarthSol/blob/master/doc/pt-validation-20261006.md)
separate demonstrated cases from unresolved convergence limits.
