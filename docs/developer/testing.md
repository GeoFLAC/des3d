---
sidebar_position: 2
slug: /developer/testing
title: Testing a change
description: How to check that a change to DynEarthSol builds in both dimensions and does not alter results unintentionally.
---

# Testing a change

Compiling is not verification. Before a change is reported as done:

1. **Build both dimensions.**

   ```console
   make ndims=2
   make ndims=3
   ```

2. **Compare results with the parent revision** whenever the change could
   alter them. In `benchmarks-cores/`, store a reference with the executable
   built from the parent commit, then rebuild with the change and compare:

   ```console
   cd benchmarks-cores
   make set NDIMS=2 CASE=<case>.cfg      # with the parent's dynearthsol2d
   # rebuild the root executables with your change, then
   make cmp NDIMS=2 CASE=<case>.cfg
   ```

   `compare.py` prints the relative difference of each field and fails above
   $10^{-8}$. A change that is meant to alter results should say so, with
   the case and the size of the difference, in the commit message and the
   pull request. `make fresh-restart-cmp` checks that a restart reproduces an
   uninterrupted run. `test-tiny.cfg` is a one-second smoke test.

3. **Run the tests that cover the area you changed**, for example the
   functional tests under `tests/functional/`, the component checks under
   `tests/residual-assembly-test/`, or a benchmark under `benchmarks/`. See
   [Benchmarks](../benchmarks/index.md) for the list.

Pull requests run the same build matrix and functional tests in continuous
integration, but CI cannot tell whether a change should have altered results;
the pull-request template asks you to report the comparison.
