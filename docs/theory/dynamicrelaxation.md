---
sidebar_position: 2
---

# Dynamic Relaxation

Given that our main interest is in long-term tectonic modeling,  high-frequency vibrations are not 
relevant to the overall deformation pattern. A strong and efficient
damping is necessary to achieve quasi-static solutions of the dynamic
equation. Complementarily, force amplification might be needed to
accelerate the transient process to achieve equilibrium. Therefore, we
either damp or amplify the total net force in the discretized nodal
momentum
equation,

  $$
  m_{a}\mathbf{a}_{a}=\mathbf{f}_{a},
  $$

according to the direction of
velocity ([Cundall, 1989](https://doi.org/10.1007/BF00538368)):

$$
ma_{i}  =  (\mathbf{f}_{damped})_{i} =  f_{i}-0.8\,\text{sgn}(u_{i})|f_{i}|,
$$

where subscript $i$ denotes the $i$-th component of a vector and
$\text{sgn}$ denotes the signum function. The motivation for the choice
of damping/amplification is based on the simple observation that in an
under-damped oscillator, the direction of force is always opposite to
the velocity direction, while in an over-damped system, the direction of
the force is parallel to the velocity direction. We found that this
choice of damping/amplification accomplishes the design goals
satisfactorily (i.e., robustly and economically).
