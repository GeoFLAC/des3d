---
sidebar_position: 2
slug: /user-guide/initial-stress
title: Initial stress
---

# Initial stress

By default (`initial_stress_option = 0`) the historical initialization is used.
For zero-gravity models, set `initial_stress_option = 1` in the `[ic]` section
to prescribe a homogeneous absolute stress tensor with `initial_stress`:

```cfg
[ic]
initial_stress_option = 1
# 2-D: [sxx, szz, sxz]    3-D: [sxx, syy, szz, sxy, sxz, syz]
initial_stress = [sxx, szz, sxz]   # replace with your values (Pa)
```
