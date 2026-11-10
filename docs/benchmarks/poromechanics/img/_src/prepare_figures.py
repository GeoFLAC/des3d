#!/usr/bin/env python3
"""Plot saved DES columns; simulation and acceptance checks live in DES_DIR."""
from des import ROOT
from pathlib import Path
import configparser
import hashlib
import html
import json
import math
import textwrap
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from consolidation import load_study, load_case, make_config, reference_from_config
from Dynearthsol import Dynearthsol, YEAR2SEC, scan_frames
from theis_reference import drawdown, scheduled_drawdown

COLORS = ['#0072B2', '#D55E00', '#009E73', '#CC79A7']

def save_figure(fig, output, name):
    # Keep keys below all panels and colour bars at the same height.
    keys = []
    for ax in fig.axes:
        ax.set_title('\n'.join(textwrap.wrap(html.unescape(ax.get_title()), 38)), pad=10)
        legend = ax.get_legend()
        if legend is not None:
            keys.append((ax, legend.legend_handles, [t.get_text() for t in legend.texts]))
            legend.remove()
    # Keep dense fields compact in SVG/PDF while preserving vector labels.
    for ax in fig.axes:
        for artist in ax.collections:
            values = artist.get_array()
            if values is not None and values.size > 1000:
                artist.set_rasterized(True)
    fig.canvas.draw()
    renderer = fig.canvas.get_renderer()
    bottom = min(ax.get_tightbbox(renderer).y0 for ax in fig.axes)/fig.bbox.height-.04
    outside = []
    columns = {}
    for ax, handles, labels in keys:
        centre = ax.get_position().x0+ax.get_position().width/2
        column = round(centre, 1)
        if column not in columns:
            columns[column] = (centre, [], [])
        _, merged_handles, merged_labels = columns[column]
        for handle, label in zip(handles, labels):
            if label not in merged_labels:
                merged_handles.append(handle); merged_labels.append(label)
    for centre, handles, labels in columns.values():
        labels = ['\n'.join(textwrap.wrap(t, 32, break_long_words=False, break_on_hyphens=False))
                  if '$' not in t else t for t in labels]
        legend = fig.legend(handles, labels, loc='upper center', fontsize=11,
                            bbox_to_anchor=(centre, bottom),
                            bbox_transform=fig.transFigure, frameon=False, ncol=1)
        outside.append(legend)
    for suffix in ('png', 'svg', 'pdf'):
        fig.savefig(output / f'{name}.{suffix}', dpi=180, bbox_inches='tight',
                    bbox_extra_artists=outside or None)
    plt.close(fig)


def theis_figures(output):
    trans, storage, rate = 1e-3, 1e-3, 0.01
    radius = np.geomspace(1, 500, 300)
    time = np.geomspace(1, 14400, 400)
    fig, axes = plt.subplots(2, 2, figsize=(11, 8), constrained_layout=True)
    for t, color in zip((60, 600, 3600, 14400), COLORS):
        axes[0, 0].semilogx(radius, -drawdown(radius, t, rate, trans, storage),
                           color=color, label=f'{t / 60:g} min')
    for r, color in zip((10, 25, 50, 100), COLORS):
        axes[0, 1].semilogx(time / 60, -drawdown(r, time, rate, trans, storage),
                           color=color, label=f'r = {r} m')
    schedule = [(0.0, rate), (3600.0, 0.0), (7200.0, -rate), (10800.0, 0.0)]
    axes[1, 0].step([t / 60 for t, _ in schedule] + [240],
                    [q * 3600 for _, q in schedule] + [schedule[-1][1] * 3600],
                    where='post', color=COLORS[0], linewidth=2)
    axes[1, 0].axhline(0, color='0.5', linewidth=0.7)
    axes[1, 0].set(xlabel='Time (min)', ylabel='Extraction rate (m³/h)', title='Pumping → shut-in → injection → shut-in')
    scheduled_time = np.unique(np.r_[np.linspace(0, 14400, 1500), [x[0] for x in schedule]])
    histories = []
    for r, color in zip((10, 25, 50, 100), COLORS):
        head = -scheduled_drawdown(r, scheduled_time, schedule, trans, storage)
        histories.append(head)
        axes[1, 1].plot(scheduled_time / 60, head, color=color, label=f'r = {r} m')
    axes[1, 1].axhline(0, color='0.5', linewidth=0.7)
    axes[0, 0].set(xlabel='Radius from well (m)', ylabel='Head change (m)', title='Constant pumping: radial profiles')
    axes[0, 1].set(xlabel='Time (min)', ylabel='Head change (m)', title='Constant pumping: observation wells')
    axes[1, 1].set(xlabel='Time (min)', ylabel='Head change (m)', title='Response to the scheduled rates')
    for ax in axes.flat:
        ax.grid(alpha=0.22)
    for ax in (axes[0, 0], axes[0, 1], axes[1, 1]):
        ax.legend(fontsize=8)
    fig.suptitle('Theis analytical reference — DES well simulation pending\n'
                 'T = 0.001 m²/s · S = 0.001 · |Q| = 0.01 m³/s · constant properties', fontsize=13)
    save_figure(fig, output, 'theis_reference')
    np.savetxt(output / 'theis-scheduled-head.csv', np.column_stack([scheduled_time] + histories),
               delimiter=',', header='time_s,head_change_r10_m,head_change_r25_m,head_change_r50_m,head_change_r100_m', comments='')
    return dict(transmissivity_m2_s=trans, storativity=storage,
                schedule_seconds_rate_m3_s=schedule, simulation_status='analytical reference only')


def consolidation_figures(output, cases):
    fig, axes = plt.subplots(2, 2, figsize=(11, 8), constrained_layout=True)
    ref = cases[2]['reference']
    smooth = np.linspace(0.1, max(c['times'][-1] for c in cases.values()), 600)
    axes[0, 0].plot(smooth, ref.pressure([ref.height], smooth)[:, 0] / 1000, color='0.15', label='Biot analytical')
    axes[0, 1].plot(smooth, ref.settlement(smooth) * 1000, color='0.15', label='Biot analytical')
    for dim, color, marker in ((2, COLORS[0], 'o'), (3, COLORS[1], '^')):
        case = cases[dim]
        times, pressure = case['times'], case['pressure']
        bottom = np.isclose(case['depth'], ref.height)
        active = times > 0
        axes[0, 0].plot(times[active][::4], pressure[active][:, bottom].mean(axis=1)[::4] / 1000,
                       marker, color=color, markersize=4, fillstyle='none', label=f'DES {dim}D')
        axes[0, 1].plot(times[active][::4], case['settlement'][active][::4] * 1000,
                       marker, color=color, markersize=4, fillstyle='none', label=f'DES {dim}D')
        axes[1, 1].semilogy(times[active], case['pressure_error'][active] * 100,
                          color=color, label=f'{dim}D pressure / load')
        axes[1, 1].semilogy(times[active], case['settlement_error'][active] * 100,
                          '--', color=color, label=f'{dim}D settlement / drained')
    case = cases[2]
    for target, color in zip((100, 1000, 5000), COLORS):
        i = np.argmin(np.abs(case['times'] - target))
        depths, inverse = np.unique(case['depth'].round(10), return_inverse=True)
        averaged = np.bincount(inverse, weights=case['pressure'][i]) / np.bincount(inverse)
        axes[1, 0].plot(averaged / 1000, depths, 'o', color=color, markersize=4, fillstyle='none')
        exact_depth = np.linspace(0, ref.height, 200)
        axes[1, 0].plot(ref.pressure(exact_depth, case['times'][i])[0] / 1000, exact_depth,
                       color=color, label=f'{case["times"][i]:.0f} s')
    axes[0, 0].set(xlabel='Time (s)', ylabel='Bottom excess pressure (kPa)', title='Pressure dissipation')
    axes[0, 1].set(xlabel='Time (s)', ylabel='Top settlement (mm)', title='Settlement integrated from axial strain')
    axes[1, 0].set(xlabel='Excess pressure (kPa)', ylabel='Depth below drained top (m)', title='2D profiles: symbols DES, lines analytical')
    axes[1, 0].invert_yaxis()
    axes[1, 1].set(xlabel='Time (s)', ylabel='Normalized absolute error (%)', title='All saved post-load frames; all pressure nodes')
    for ax in axes.flat:
        ax.grid(alpha=0.22)
        ax.legend(fontsize=8)
    fig.suptitle('Actual DES baseline vs classical Terzaghi consolidation\n'
                 'PT option 1 · absolute tolerance 10⁻⁶ · fixed mesh · frame 0 is pre-load', fontsize=13)
    save_figure(fig, output, 'terzaghi_comparison')

    fig, axes = plt.subplots(1, 3, figsize=(9, 6), constrained_layout=True)
    for ax, target in zip(axes, (100, 1000, 5000)):
        i = np.argmin(np.abs(case['times'] - target))
        image = ax.tripcolor(case['coordinate'][:, 0], -case['coordinate'][:, -1],
                             case['connectivity'], case['pressure'][i] / 1000,
                             shading='gouraud', cmap='viridis', vmin=0, vmax=ref.load / 1000)
        ax.set(xlabel='Horizontal position (m)', ylabel='Depth (m)',
               title=f't = {case["times"][i]:.0f} s')
        ax.invert_yaxis()
    fig.colorbar(image, ax=axes, label='Excess pore pressure (kPa)', shrink=0.8)
    fig.suptitle('Actual DES 2D pressure field\nTop drained · bottom and sides sealed · 100 kPa traction load', fontsize=13)
    save_figure(fig, output, 'terzaghi_pressure_fields')


if __name__ == '__main__':
    import argparse
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('study', type=Path)
    a = p.parse_args()
    cases = {d: load_case(a.study, d) for d in (2, 3)}
    consolidation_figures(a.study, cases)
    theis_figures(a.study)
