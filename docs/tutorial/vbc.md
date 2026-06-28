---
sidebar_position: 4
title: Velocity boundary conditions (3D)
---

# Velocity boundary conditions (3D)

Each lateral face of a 3D model (`x0`, `x1`, `y0`, `y1`) can be assigned
an independent velocity boundary condition (VBC) case. The case number is
set via `bc.vbc_x0`, `bc.vbc_x1`, `bc.vbc_y0`, `bc.vbc_y1`.

| Case | Normal component | Lateral-shear component | Vertical |
|------|-----------------|------------------------|---------|
| 0 | Free | Free | Free |
| 1 | Fixed (`vbc_val_*`) | Free | Free |
| 2 | Free | Fixed (0) | Free |
| 3 | Fixed | Fixed (0) | Free |
| 4 | Free | Free | Fixed (0) |
| 5 | Fixed | Fixed | Free |
| **6** | **Fixed (`vbc_val_*`)** | **Fixed (`vbc_val_*_l`)** | **Free** |

## Case 6 — independent normal and lateral-shear velocities

Case 6 (added in 2026) allows setting both the normal and lateral-shear
velocities on a face to independent non-zero values, with the vertical
component free. It is useful for transtensional or transpressional
boundary conditions.

```cfg
bc.vbc_x0 = 6
bc.vbc_val_x0   = -0.01   # normal velocity (m/yr)
bc.vbc_val_x0_l =  0.005  # lateral-shear velocity (m/yr)

bc.vbc_x1 = 6
bc.vbc_val_x1   =  0.01
bc.vbc_val_x1_l = -0.005
```

See `examples/oblique-rift-3d.cfg` for a complete transtensional rifting
example using case 6.
