---
sidebar_position: 1
title: "Running the examples"
---
# Running the examples

## Build DES

From the DES source folder:

```bash
make ndims=2      # dynearthsol2d
make ndims=3      # dynearthsol3d
```

Put the executables on your `PATH`, or call them with their full path.
For the Python reader and ParaView converter, set the source-folder path:

```bash
export DES_SOURCE=/path/to/DynEarthSol
export PYTHONPATH="$DES_SOURCE${PYTHONPATH:+:$PYTHONPATH}"
```

## Run an example

Each example's files come in one zip, linked in its *At a glance* box: `input.cfg`,
and any mesh (`.poly`) or restart frames (`.save`, `.chkpt`, `.info`) it starts from.
Unpack it somewhere writable and run the commands given in the
example's "Input and how to run" section, for instance

```bash
mkdir -p ~/runs && cd ~/runs
unzip theis.zip
cd theis
export OMP_NUM_THREADS=1
dynearthsol3d input.cfg
```

`dynearthsol2d -h` lists every input option with its default and meaning.
Each page lists the settings that define its example.

## Look at the output

DES names its output after `sim.modelname`: `<model>.info` lists the saved
frames (frame, step, time in seconds), `<model>.save.NNNNNN` holds the
fields of each frame and `<model>.chkpt.NNNNNN` the restart checkpoints.

```python
import sys; sys.path.append('/path/to/DynEarthSol')
from Dynearthsol import Dynearthsol
model = Dynearthsol('theis')
p = model.read_field(model.frames[-1], 'pore pressure')
```

`python3 "$DES_SOURCE/2vtk.py" <model>` converts the frames for ParaView; add `-g` for a
run that restarted from another, to include the frames before the restart.

## Reproduce a figure

Each page names the script that ran the whole study behind its figure (all
meshes and time steps). The scripts are in `benchmarks/hydromechanics/` and
`tests/functional/hydromechanics/`. Each page's *At a glance* box records the
source revision its published figures were made with. For an exact
reproduction, use that revision; a newer solver can contain corrections absent from the archived run.
