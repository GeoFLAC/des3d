---
sidebar_position: 0
slug: /benchmarks/poromechanics
title: Overview
---

# Poromechanics benchmarks

Benchmarks of coupled fluid flow, heat and deformation in DES. Each page sets up one problem, gives the input file and the commands to run it, says which output to look at, and compares the result with an analytical or independent reference solution, with the limits of that comparison.

The applications built on these checks, slides, rapid drawdown, embankment stability and land subsidence, are in the [Groundwater and slopes](../../tutorial/groundwater-slopes/embankment.md) tutorials.

Every example ships its input file and any mesh or restart files it needs, so it runs as is with DES built from this source. See [Running the examples](./running.md).

Terms: DES is DynEarthSol. PT is its pseudo-transient solver, which iterates each time step to mechanical equilibrium by dynamic relaxation; a physical step is one model time step, as opposed to a PT iteration. The explicit form is ordinary explicit mechanics with inertial (mass) scaling, and GVS is that form with global velocity scaling. Pressure feedback means that deformation changes the pore pressure, so flow and mechanics are coupled both ways. EP is elasto-plastic Mohr–Coulomb plasticity, and EP-RSF the same with rate-and-state friction.

Pressure is compression-positive; stress and volumetric strain are tension/expansion-positive.

These examples need DynEarthSol built from the poromechanics source.
