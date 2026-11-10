"""Figures for the saved fluid content study."""
from des import ROOT
from fluid_content import INFLOW, REF, reference
import fluid_content as water
import numpy as np
from Dynearthsol import Dynearthsol, scan_frames

def plot_result(folder, target, inflow=INFLOW):
    import diagram_style as ds
    import prepare_figures as pf
    model = Dynearthsol(str(folder/'column'))
    rows = scan_frames(str(folder/'column'))
    x = model.read_field(0, 'coordinate')
    history = np.loadtxt(folder/'history.csv', delimiter=',', skiprows=1)
    width = float(np.ptp(x[:, 0]))
    depth = np.linspace(0, REF.height, 301)
    with pf.plt.rc_context(ds.FIGURE_RC):
        fig, axes = ds.result_figure(2)
        for t, color in zip((.1, .5, 1., 4.), ds.SERIES):
            row = min(rows, key=lambda r: abs(r['time']-t))
            pressure = model.read_field(row['frame'], 'pore pressure')
            ds.analytical(axes[0], reference(depth, row['time'], inflow=inflow)[0][0], depth,
                          color=color, label=f"$t={row['time']:g}$ s")
            line = np.isclose(x[:, 0], width/2)
            ds.des(axes[0], pressure[line], -x[line, -1], color=color, label='_nolegend_')
        axes[0].invert_yaxis()
        ds.panel(axes[0], 'a', 'Pressure while the column fills', xlabel='pressure (Pa)', ylabel='depth (m)')
        ds.key(axes[0], loc='upper right')
        sampled = history[::max(1, len(history)//24)]
        for exact, discrete, label, color in ((5, 1, 'stored fluid', ds.WATER), (8, 6, 'drain outflow', ds.HOT)):
            ds.analytical(axes[1], history[:, 0], history[:, exact]/width*1e6, color=color, label=label)
            ds.des(axes[1], sampled[:, 0], sampled[:, discrete]/width*1e6, color=color, label='_nolegend_')
        ds.panel(axes[1], 'b', 'Independent water balance', xlabel='time (s)', ylabel=r'volume / area ($\mu$m)')
        ds.key(axes[1])
        pf.save_figure(fig, target, 'result')
