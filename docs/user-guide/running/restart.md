---
sidebar_position: 1
slug: /user-guide/restart
title: Checkpointing and restart
---

# Checkpointing and restart

DES3D writes checkpoint files at regular intervals so that a simulation
can be resumed after interruption. With unchanged controls, the restart
tests compare saved physical state with uninterrupted runs. Use one OpenMP
thread for byte-exact PT continuation; multi-thread ADR reductions can
change the last bits. The following state is persisted in the checkpoint:

- `dt` and `dt_PT` (time step)
- `max_global_vel_mag`
- `reference_frame_time`
- `info_display_next_step`
- `dhacc` (surface marker correction)
- `strain_rate`, `viscosity`, `volume_old`
- `plastic strain-rate` (`delta_plstrain`), so a restarted run's diagnostic
  output matches a continuous one

Copy the original config and edit its existing `[sim]` section to select
a checkpoint explicitly, giving the restart a distinct output name:

```cfg
[sim]
modelname = result-r
is_restarting = yes
restarting_from_modelname = result
restarting_from_frame = 10
```

Replace `result` and `10` with your original model prefix and an output
frame that has both save and checkpoint files, then run the executable
with that edited config. Checkpoint frame numbers are output-frame indices,
not necessarily physical step numbers. Retain the original physical
controls and set the stopping step/time to permit continuation. DES3D
requires both restart-selection parameters; rerunning an unchanged fresh
config does not automatically find a checkpoint.

PT restores saved velocity, next-step dt and velocity scale, and does not
repeat completed initial equilibration. Its optional running scale requires
the stored history; old checkpoints without it cannot silently start a new
history. Hydraulic checkpoints also require the pending signed pressure
increment for the next mechanical step. Dry checkpoints do not require that
hydraulic record. See [PT restart and limits](../numerical-controls/solver.md#failure-restart-and-limits).

:::danger Checkpoint/output format revision 4
The checkpoint and frame file format was bumped from revision 3 to 4.
A revision (or dimensionality) mismatch between the file and the running
binary is now a **hard error** with a diagnostic naming the expected and
actual values, previously it was accepted silently and could be misread.
This means **checkpoint and frame files written before this change cannot
be restarted or read by a newer DES3D binary.** Finish or discard runs on
the old binary before upgrading.
:::

:::danger Conservative MMG remeshing adds new checkpoint records
Checkpoints now also carry `nremesh`, `plstrain_remesh`, and, in MMG builds,
`surface dh` and `refined_elem_size_n` (plus, with `remeshing_option = 13`,
`side_prof_*`). A checkpoint written before this change does not have these
records, and restarting from it is a restart-mismatch error (`21`/`22`).
Finish or discard runs on the old binary before upgrading. See
[Conservative remeshing](../numerical-controls/mmg.md#conservative-remeshing-freeze--required-policy)
for what changed in MMG remeshing itself.
:::

Frame files (HDF5 and plain binary) now also embed the full `.info` row
(steps, time, dt, walltime, node/element/segment counts). If a run's
`.info` file is lost, `utils/recreate_info.py` rebuilds it from the frame
files alone; `restart()` also falls back to this embedded metadata
automatically when `.info` is missing.
