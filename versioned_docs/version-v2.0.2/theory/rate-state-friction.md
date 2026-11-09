---
slug: /theory/rate-state-friction
sidebar_position: 9
---

# Rate-and-state friction

DES3D models faults as finite-width shear zones in a continuum. A
rate-and-state friction (RSF) law sets the friction angle of the
Mohr–Coulomb plastic model in every element. The friction coefficient then
depends on how fast the element slips and on its slip history, so a fault
can creep, heal, nucleate an instability and rupture within one simulation.
The approach follows
[Tong and Lavier (2018)](https://doi.org/10.1038/s41467-018-06390-z);
[Herrendörfer et al. (2018)](https://doi.org/10.1029/2017JB015225) describe
a related invariant formulation.

This page gives the friction law, how DES3D measures slip rate in an
element, and how the law enters the plastic update. It then describes
global velocity scaling, which lets one model run through slow loading and
fast rupture, and the other numerical controls.

## Friction law

The friction coefficient is

$$
\mu = \mu_0 + a\ln\frac{V}{V_0} + b\ln\frac{V_0\,\theta}{D_c},
$$

where $V$ is the slip rate, $\theta$ the state variable (a time),
$V_0$ a reference slip rate, $D_c$ the characteristic slip distance, and
$a$ and $b$ the direct-effect and evolution-effect parameters
([Dieterich, 1979](https://doi.org/10.1029/JB084iB05p02161);
[Ruina, 1983](https://doi.org/10.1029/JB088iB12p10359)).
The reference coefficient $\mu_0$ is the tangent of the element's
Mohr–Coulomb friction angle, so $\mu=\mu_0$ when the element slides
steadily at $V_0$.

The state variable evolves by one of two laws. The aging law
([Dieterich, 1979](https://doi.org/10.1029/JB084iB05p02161);
[Ruina, 1983](https://doi.org/10.1029/JB088iB12p10359)) lets a fault
heal while it is stationary:

$$
\frac{d\theta}{dt} = 1 - \frac{V\theta}{D_c}.
$$

The slip law ([Ruina, 1983](https://doi.org/10.1029/JB088iB12p10359))
changes the state only while the fault slips:

$$
\frac{d\theta}{dt} = -\frac{V\theta}{D_c}\ln\frac{V\theta}{D_c}.
$$

Under both laws, steady sliding at rate $V$ gives $\theta_{ss}=D_c/V$ and
the steady-state friction

$$
\mu_{ss} = \mu_0 + (a-b)\ln\frac{V}{V_0}.
$$

A material with $a-b>0$ is velocity strengthening: it strengthens as it
slides faster and creeps stably. A material with $a-b<0$ is velocity
weakening and can become unstable
([Marone, 1998](https://doi.org/10.1146/annurev.earth.26.1.643);
[Scholz, 1998](https://doi.org/10.1038/34097)).

`mat.state_var_model` selects the law:

| Value | Law | Friction |
| --- | --- | --- |
| `0` (default) | No state evolution | $\mu_{ss}$ at the current slip rate |
| `1` | Aging law | full law |
| `2` | Slip law | full law |

With `0` the friction follows the current slip rate instantly. This is
steady-state friction and needs no $D_c$.

## Slip rate in a continuum element

The law needs a slip rate, but an element carries a strain rate. DES3D
offers two measures, chosen with `control.rsf_slip_rate_projection_option`.

**Option 1: strain-rate invariant (recommended).** The slip rate is the
shear across one element width,

$$
V = 2\,w\,\dot\varepsilon_{II},
\qquad
\dot\varepsilon_{II} = \sqrt{\tfrac12\,\dot\varepsilon'_{ij}\dot\varepsilon'_{ij}},
$$

where $\dot\varepsilon'$ is the deviatoric strain rate and $w$ is the
element's smallest altitude: twice the area divided by the longest edge in
2D, three times the volume divided by the largest face in 3D. For simple
shear at engineering rate $\dot\gamma$, $\dot\varepsilon_{II}=\dot\gamma/2$
and $V=w\dot\gamma$, the velocity jump across the element. A shear band
wider than one element shares its slip among its elements, each with its own
rate and state. The measure is independent of rigid motion and of the
reference frame. The DES v2 benchmarks use it.

**Option 0: velocity projection (default, historical).** The element's mean
velocity is projected onto the direction of maximum shear stress, which lies
at 45° to the principal stress axes. In 3D the projection is onto the plane
of maximum shear. This measures the velocity of the element, not a velocity
difference, so it depends on the reference frame: a block that translates
rigidly reports slip. The option is kept so that earlier models reproduce.

Each rate is floored at $10^{-16}$ m/s before it enters the law, so the
logarithms stay finite in a locked element.

## Coupling with the plastic model

RSF is available as `mat.rheology_type = elasto-plastic-rate-state-friction`
(alias `elasto-plastic-rsf`) and
`elasto-visco-plastic-rate-state-friction` (`elasto-visco-plastic-rsf`).
They are the elasto-plastic and elasto-visco-plastic models of the
[constitutive update](./constitutive.md) with one change:
the friction angle in the Mohr–Coulomb yield function is

$$
\phi = \arctan\mu .
$$

A higher friction coefficient raises the yield stress. A slipping
velocity-weakening element lowers its own strength, which concentrates the
strain further. Cohesion, dilation angle and tension cutoff are unchanged.
They still weaken with plastic strain between `mat.pls0` and `mat.pls1`.
The reference friction angle also weakens: $\mu_0=\tan\phi_0$ follows
`mat.friction_angle0` to `mat.friction_angle1` as plastic strain grows.

The normal stress that resists slip is the one in the Mohr–Coulomb
criterion. It is not an input. It comes from the stress field, including
lithostatic load and tectonic stress.

### Order of the update

In each element and each step, DES3D:

1. computes $V$ from the current strain rate (option 1) or velocity
   (option 0);
2. advances the state explicitly with the step $\Delta t$,
   $\theta^{n+1} = \theta^n + \Delta t\,\dot\theta(V,\theta^n)$;
3. evaluates $\mu(V,\theta^{n+1})$ and $\phi=\arctan\mu$;
4. performs the elasto-plastic (or elasto-visco-plastic) stress update with
   that friction angle.

With several materials in an element, $a$, $b$, $V_0$ and $D_c$ are
averaged over the element's markers, as are the friction angles.

### Bounds

The update keeps the law finite in extreme states:

| Quantity | Bound |
| --- | --- |
| $\theta$ | $10^{-12}$ to $10^{12}$ s |
| $V$ in the law | at least $10^{-16}$ m/s |
| $\mu$ | at least $10^{-6}$ |
| $V\theta/D_c$ in the slip law | at least $10^{-10}$; a step that would make $\theta\le0$ resets it to $D_c/V$ |

The state starts at steady state at the reference rate,
$\theta_0 = D_c/V_0$, so $\mu=\mu_0$ at the start. The state is saved in checkpoints as `friction state variable`; the
friction coefficient is recomputed from it on restart.

## Global velocity scaling

### Why RSF needs it

An earthquake cycle spans loading at plate rates, about $10^{-9}$ m/s for
hundreds of years, and slip near 1 m/s for seconds. With physical density,
an explicit step is limited by the elastic wave speed to milliseconds, and a
300-year interseismic period would need about $10^{12}$ steps. Ordinary
[mass scaling](./massscaling.md) fixes the scaled wave
speed from the boundary velocity, $c\,v_{bc}$. That keeps loading
quasi-static, but a fault slipping $10^9$ times faster than the boundary
then moves faster than the scaled waves, and inertia dominates the event.

Global velocity scaling (GVS) ties the mass scaling to the fastest motion
in the model at every step. `control.use_global_velocity_scaling = yes`
enables it, and DES3D turns it on for any RSF rheology.

### Scaled wave speed and density

At each step DES3D finds the largest speed $v_{\max}$ (nodal or boundary)
and sets

$$
c_f = \min\!\left(c\,v_{\max},\ \sqrt{M/\rho}\right),
\qquad
\rho_f = \frac{K}{c_f^{2}},
$$

where $c$ is `control.inertial_scaling`, $K$ the bulk modulus, $\rho$ the
physical density and $M$ the modulus chosen by
`control.mass_scaling_reference_speed` (`shear`: $G$, the default;
`bulk`: $K$). The nodal masses are rebuilt from $\rho_f$ every step.

While $c\,v_{\max}$ is below the cap, the scaled waves always travel $c$
times faster than the fastest material point. Stress therefore spreads
through the model ahead of the motion, and the model is as close to
quasi-static during accelerating slip as during loading. When $c\,v_{\max}$
reaches the cap, the wave speed is the physical shear or bulk wave speed.
With the `bulk` ceiling the density is then the physical density. With the
default `shear` ceiling it is $\rho K/G$, still larger than $\rho$.

### Time step

The elastic step follows the same speed:

$$
\Delta t = \frac{0.5\,l_{\min}}{c\,v_{\max}},
\qquad
\Delta t \ge \frac{0.2\,l_{\min}}{\sqrt{M/\rho}},
$$

where $l_{\min}$ is the smallest element size. The fastest point therefore
moves at most $0.5\,l_{\min}/c$ per step, a fixed fraction of an element,
whatever its speed. The lower bound is the stable step at the capped wave speed.
Other limits (Maxwell relaxation, heat and fluid diffusion, the state limit
below) still apply, and `control.dt_fraction` scales the result.

For example, with $l_{\min}=100$ m, $c=10^5$, $G=30$ GPa and
$\rho=2700$ kg/m³ (shear speed 3.3 km/s):

| Stage | $v_{\max}$ | $c_f$ | $\Delta t$ |
| --- | --- | --- | --- |
| Interseismic loading | $10^{-9}$ m/s | $10^{-4}$ m/s | $5\times10^{5}$ s (6 days) |
| Rupture | 1 m/s | 3.3 km/s (cap) | $6\times10^{-3}$ s |

The step changes by eight orders of magnitude within one cycle and returns
to long steps after the event, without user intervention.

### Damping

Force damping (`control.damping_option`, default `1` with
`control.damping_factor = 0.8`) acts in every step, including during events.
Ruptures in DES3D are therefore damped, as in the quasi-dynamic
simulations of [Tong and Lavier (2018)](https://doi.org/10.1038/s41467-018-06390-z).
`control.damping_option = 0` removes the damping.

### Output during events

With GVS, regular output follows `sim.output_time_interval_in_yr` or
`sim.output_step_interval` as usual, and events add frames every
`sim.earthquake_output_step_interval` steps (see
[earthquake output](#earthquake-output)). A long cycle model therefore saves
sparse interseismic frames and dense coseismic frames.

### Limiting the state change per step

The explicit state update is accurate only if the slip in one step is small
compared with $D_c$. GVS limits the slip per step to $0.5\,l_{\min}/c$,
which is set by the element size, not by $D_c$. For the aging law, the
update is stable only if $\Delta t\,V/D_c<2$. When $0.5\,l_{\min}/c$ is
not small compared with $D_c$, set `control.rsf_dtheta_max` $=f$. It adds
two bounds over all elements:

$$
\Delta t \le f\,\frac{D_c}{V},
\qquad
\Delta t \le f\,\theta .
$$

The first limits the slip per step to $fD_c$. The second limits the
fractional healing per step to $f$. $f$ must lie in $[0,2)$; `0` (default)
disables the bounds. The bounds require the aging law
(`mat.state_var_model = 1`), slip-rate option 1, adaptive stepping
(`control.fixed_dt = 0`), and no PT solver, body-force adjustment or
isostasy adjustment.

## Resolving a velocity-weakening fault

A velocity-weakening fault is unstable only if it is softer than a critical
stiffness. For a spring-slider of stiffness $k$ under effective normal
stress $\sigma$, steady sliding is unstable when

$$
k < k_c = \frac{(b-a)\,\sigma}{D_c}
$$

([Ruina, 1983](https://doi.org/10.1029/JB088iB12p10359)). A fault in an
elastic medium has stiffness of order $G'/L$ over a slipping length $L$, so
instability needs a patch larger than a nucleation length. For the aging law
two length scales are useful
([Rubin and Ampuero, 2005](https://doi.org/10.1029/2005JB003686)):

$$
L_b = \frac{G' D_c}{b\,\sigma},
\qquad
L_\infty = \frac{1}{\pi}\left(\frac{b}{b-a}\right)^2 L_b
\quad (0.5 \lesssim a/b < 1),
$$

with $G'=G$ for antiplane and $G'=G/(1-\nu)$ for in-plane slip.
$L_b$ is close to the size of the cohesive zone at a rupture tip and sets
the element size. Cycle simulations need several elements across $L_b$
([Lapusta et al., 2000](https://doi.org/10.1029/2000JB900250)). A
velocity-weakening patch shorter than $L_\infty$ creeps or slips slowly
instead of rupturing. In DES3D the slip of an element is spread over its
width $w$, so element size controls both the length scales above and the
width of the shear zone.

## Earthquake output

DES3D detects events in RSF models from the largest speed $v_{\max}$ and
plastic activity:

- an event starts when $v_{\max}$ exceeds `sim.earthquake_start_factor`
  (default 5) times the largest boundary speed, but at least $10^{-6}$ m/s,
  while plastic strain is growing;
- it ends when $v_{\max}$ falls below `sim.earthquake_end_factor`
  (default 2) times the boundary speed, but at least $5\times10^{-7}$ m/s,
  or when plastic strain stops growing.

During an event, fields are written every
`sim.earthquake_output_step_interval` steps (default 50) in addition to the
regular output. With `sim.seismic_moment_calculate_output = yes` DES3D
writes each event's start and end times to `seismic_moment_magnitude.txt`,
together with a size measure $\sum G\,\Omega_e\,|\bar v_e|\,\Delta t$
accumulated over elements (shear modulus $G$, element volume $\Omega_e$,
mean element speed $\bar v_e$) and a magnitude
$M_w = \tfrac23(\log_{10}M_0 - 9.1)$ from it
([Hanks and Kanamori, 1979](https://doi.org/10.1029/JB084iB05p02348)).
The size measure uses element speed rather than slip across the shear zone.
Use it to compare events within one model, not as a seismic moment in N·m.

The point monitor can record the friction coefficient and state at chosen
points with `monitor.output_dynamic_friction` and
`monitor.output_state_variable`.

## Parameters

| Parameter | Default | Meaning |
| --- | --- | --- |
| `mat.rheology_type` | – | `elasto-plastic-rsf` or `elasto-visco-plastic-rsf` |
| `mat.direct_a` | `[0.020]` | $a$ per material |
| `mat.evolution_b` | `[0.025]` | $b$ per material |
| `mat.characteristic_velocity` | `[1e-6]` | $V_0$ per material (m/s), must be positive |
| `mat.characteristic_distance` | `[4e-3]` | $D_c$ per material (m) |
| `mat.state_var_model` | `0` | `0` steady state, `1` aging law, `2` slip law |
| `mat.friction_angle0`, `mat.friction_angle1` | `[30]`, `[5]` | reference friction angle $\phi_0$ (degrees) before and after plastic weakening |
| `control.rsf_slip_rate_projection_option` | `0` | `0` velocity projection, `1` strain-rate invariant |
| `control.rsf_dtheta_max` | `0` | state-change limit $f$ on the time step, in $[0,2)$ |
| `control.use_global_velocity_scaling` | `no` | Global velocity scaling; forced on for RSF |
| `control.inertial_scaling` | `1e5` | $c$: scaled wave speed over the fastest speed |
| `control.mass_scaling_reference_speed` | `shear` | Wave-speed cap: `shear` ($G$) or `bulk` ($K$) |
| `control.damping_option`, `control.damping_factor` | `1`, `0.8` | Force damping |
| `sim.earthquake_start_factor`, `sim.earthquake_end_factor` | `5`, `2` | event thresholds relative to the boundary speed |
| `sim.earthquake_output_step_interval` | `50` | output interval during an event (steps) |
| `sim.seismic_moment_calculate_output` | `no` | write event times and size to `seismic_moment_magnitude.txt` |

## References

- Dieterich, J. H. (1979). Modeling of rock friction: 1. Experimental
  results and constitutive equations. *Journal of Geophysical Research*,
  84(B5), 2161–2168. https://doi.org/10.1029/JB084iB05p02161
- Hanks, T. C., and Kanamori, H. (1979). A moment magnitude scale.
  *Journal of Geophysical Research*, 84(B5), 2348–2350.
  https://doi.org/10.1029/JB084iB05p02348
- Herrendörfer, R., Gerya, T., and van Dinther, Y. (2018). An invariant
  rate- and state-dependent friction formulation for viscoeastoplastic
  earthquake cycle simulations. *Journal of Geophysical Research: Solid
  Earth*, 123, 5018–5051. https://doi.org/10.1029/2017JB015225
- Lapusta, N., Rice, J. R., Ben-Zion, Y., and Zheng, G. (2000).
  Elastodynamic analysis for slow tectonic loading with spontaneous rupture
  episodes on faults with rate- and state-dependent friction. *Journal of
  Geophysical Research*, 105(B10), 23765–23789.
  https://doi.org/10.1029/2000JB900250
- Marone, C. (1998). Laboratory-derived friction laws and their application
  to seismic faulting. *Annual Review of Earth and Planetary Sciences*, 26,
  643–696. https://doi.org/10.1146/annurev.earth.26.1.643
- Rubin, A. M., and Ampuero, J.-P. (2005). Earthquake nucleation on (aging)
  rate and state faults. *Journal of Geophysical Research*, 110, B11312.
  https://doi.org/10.1029/2005JB003686
- Ruina, A. (1983). Slip instability and state variable friction laws.
  *Journal of Geophysical Research*, 88(B12), 10359–10370.
  https://doi.org/10.1029/JB088iB12p10359
- Scholz, C. H. (1998). Earthquakes and friction laws. *Nature*, 391,
  37–42. https://doi.org/10.1038/34097
- Tong, X., and Lavier, L. L. (2018). Simulation of slip transients and
  earthquakes in finite thickness shear zones with a plastic formulation.
  *Nature Communications*, 9, 3893.
  https://doi.org/10.1038/s41467-018-06390-z
