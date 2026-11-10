#!/usr/bin/env python3
"""Plot saved consolidation refinement or mechanical-method error histories.

Usage: plot_studies.py {refinement,methods} STUDY
Only recorded CSV/JSON metrics are read; no reference is evaluated.
"""
from des import ROOT
from pathlib import Path
import argparse
import json
import numpy as np
import prepare_figures as pf
import diagram_style as ds


def refinement(study):
    report = json.loads((study/'summary.json').read_text())
    with pf.plt.rc_context(ds.FIGURE_RC):
        fig, axes = pf.plt.subplots(2, 2, figsize=(10, 8), constrained_layout=True)
        for dim in report['settings']['dimensions']:
            records = [r for r in report['runs'] if r['dimension'] == dim]
            spatial = sorted((r for r in records if 'spatial' in r['roles']), key=lambda r:-r['spacing_m'])
            changes = report['dimensions'][str(dim)]['temporal_changes']
            for ax, x, y in (
                (axes[0, 0], [r['spacing_m'] for r in spatial], [r['max_pressure_error_over_load'] for r in spatial]),
                (axes[0, 1], [r['spacing_m'] for r in spatial], [r['max_settlement_error_over_drained'] for r in spatial]),
                (axes[1, 0], [r['dt_s'] for r in changes], [r['pressure'] for r in changes]),
                (axes[1, 1], [r['dt_s'] for r in changes], [r['settlement'] for r in changes])):
                ax.loglog(x, y, 'o-', mfc='white', label=f'{dim}D')
        for ax, letter, title, xlabel in (
            (axes[0, 0], 'a', 'Pressure error by mesh', 'spacing (m)'),
            (axes[0, 1], 'b', 'Settlement error by mesh', 'spacing (m)'),
            (axes[1, 0], 'c', 'Pressure difference by step', 'physical step (s)'),
            (axes[1, 1], 'd', 'Settlement difference by step', 'physical step (s)')):
            ds.panel(ax, letter, title, xlabel=xlabel, ylabel='normalised error')
        pf.save_figure(fig, study, 'terzaghi_refinement')


def methods(study):
    report = json.loads((study/'summary.json').read_text())
    settings = report['settings']
    provenance = json.loads((study/'provenance.json').read_text())
    speeds = settings['initial_speeds_m_s']
    scales = settings.get('scalings', [1e4, 1e5, 1e6])
    with pf.plt.rc_context(ds.FIGURE_RC):
        fig, axes = pf.plt.subplots(len(speeds), 2, squeeze=False,
                                    figsize=(11, 3.5*len(speeds)), constrained_layout=True)
        for row, speed in enumerate(speeds):
            for name, result in report['cases'].items():
                if result['status'] != 'complete':
                    continue
                control = provenance['cases'][name]['control']
                if name.startswith('pt'):
                    color, linestyle = ds.INK, ':' if name == 'pt0' else '-'
                    label = name.upper()
                else:
                    if float(control['characteristic_speed']) != speed:
                        continue
                    scaling = float(control['inertial_scaling'])
                    color = ds.SERIES[scales.index(scaling) % len(ds.SERIES)]
                    method = name.split('-S')[0]
                    linestyle = {'explicit':':', 'gvs-shear':'--', 'gvs-bulk':'-'}[method]
                    label = f'{method}, S={scaling:g}'
                history = np.loadtxt(study/name/f"terzaghi-{settings['dimension']}d-history.csv",
                                     delimiter=',', skiprows=1)
                active = history[:, 0] > 0
                for col, field in enumerate((5, 6)):
                    axes[row, col].semilogy(history[active, 0], history[active, field],
                                            color=color, ls=linestyle, label=label)
            for col, ylabel in enumerate(('pressure error / load', 'settlement error / drained')):
                ds.panel(axes[row, col], '', f'Initial velocity scale {speed:g} m/s',
                         xlabel='physical time (s)', ylabel=ylabel)
        pf.save_figure(fig, study, 'mechanical-methods')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('kind', choices=('refinement', 'methods'))
    parser.add_argument('study', type=Path)
    args = parser.parse_args()
    dict(refinement=refinement, methods=methods)[args.kind](args.study)
