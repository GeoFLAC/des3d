"""Figures for the saved thermal cell study."""
from des import ROOT
from thermal_cell import RATE, STOP, BETA, STORAGE, T0, FLUID
import thermal_cell as thermal
import numpy as np
from Dynearthsol import Dynearthsol, scan_frames

def plot_result(output, target, controls=True):
    import diagram_style as ds
    import prepare_figures as pf
    closed = np.loadtxt(output/'explicit-fixed/history.csv', delimiter=',', skiprows=1)
    sampled = closed[::4]
    with pf.plt.rc_context(ds.FIGURE_RC):
        fig, axes = ds.result_figure(2)
        rise = np.linspace(0, RATE*STOP, 201)
        ds.analytical(axes[0], rise, BETA*rise/STORAGE/1000)
        ds.des(axes[0], sampled[:, 1]-T0, sampled[:, 2]/1000)
        ds.panel(axes[0], 'a', 'Sealed thermal pressurization', xlabel='temperature rise (K)', ylabel='pressure (kPa)')
        ds.analytical(axes[1], closed[:, 0], closed[:, 8]/1e6, label='supplied heat')
        ds.des(axes[1], sampled[:, 0], sampled[:, 7]/1e6, label='stored heat')
        ds.panel(axes[1], 'b', 'Closed heat balance', xlabel='time (s)', ylabel='heat (MJ per unit cell)')
        pf.save_figure(fig, target, 'result')
        if not controls:
            return
        fig, axes = ds.result_figure(2)
        pt = np.loadtxt(output/'pt-fixed/history.csv', delimiter=',', skiprows=1)
        ds.analytical(axes[0], closed[:, 0], closed[:, 3]/1000, label='physical fixed-strain reference')
        ds.des(axes[0], pt[::4, 0], pt[::4, 2]/1000, label='PT, 0.01 s step')
        ds.panel(axes[0], 'a', 'PT pending-increment control', xlabel='time (s)', ylabel='pressure (kPa)')
        drained = np.loadtxt(output/'explicit-drained/history.csv', delimiter=',', skiprows=1)
        ds.analytical(axes[1], drained[:, 0], -.5*FLUID*BETA*(drained[:, 1]-T0)**2/1000,
                      label='missing-capacity prediction')
        ds.des(axes[1], drained[::4, 0], drained[::4, 10]/1000, label='retained-fluid ledger')
        axes[1].axhline(0, color=ds.MUTED, lw=.7)
        ds.panel(axes[1], 'b', 'Open energy remains unqualified', xlabel='time (s)', ylabel='enthalpy residual (kJ per unit cell)')
        pf.save_figure(fig, target, 'controls')
