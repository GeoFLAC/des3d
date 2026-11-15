"""Plot a saved averaged-aquifer slab comparison."""
from des import ROOT
from pumping_slab import compare, BAND, Q
import numpy as np
import matplotlib.pyplot as plt

def figure(aq, rows, output):
    blue, orange, ink, ink2 = '#2a78d6', '#eb6834', '#0b0b0b', '#52514e'
    plt.rcParams.update({'font.size': 9, 'axes.spines.top': False, 'axes.spines.right': False,
                         'axes.grid': True, 'grid.color': '#e6e5e1', 'grid.linewidth': 0.6,
                         'legend.frameon': False, 'axes.titlelocation': 'left'})
    fig, axes = plt.subplots(1, 2, figsize=(10, 3.8), gridspec_kw=dict(wspace=0.25))
    r = np.geomspace(BAND[0], BAND[1], 200)
    last = rows[-1]
    for k, row in enumerate((rows[0], last)):
        ref = aq.line_well(r, row['time_s'], Q)
        shade = '#86b6ef' if k == 0 else '#1c5cab'
        axes[0].plot(r, -ref['pressure'] / 1e3, color=ink, linewidth=1.6)
        axes[0].plot(row['plot']['r_node'], -row['plot']['p'] / 1e3, 'o', markersize=2.5,
                     color=shade, alpha=0.6, label=f"DES, t = {row['time_s']:.0f} s")
    axes[0].plot([], [], color=ink, label='Reference (plane stress)')
    axes[0].set(xscale='log', xlabel='Radius (m)', ylabel='Pressure drop (kPa)',
                title='(a) Pore pressure across the slab')
    axes[0].legend()
    ref = aq.line_well(r, last['time_s'], Q)
    axes[1].plot(r, -ref['areal_strain'] * 1e6, color=ink, linewidth=1.6,
                 label='Reference: areal = vertical')
    axes[1].plot(last['plot']['r_elem'], -last['plot']['areal'] * 1e6, 'o', markersize=2.5,
                 color=blue, alpha=0.6, label='DES areal strain')
    axes[1].plot(last['plot']['r_elem'], -last['plot']['vertical'] * 1e6, 's', markersize=2.5,
                 color=orange, alpha=0.6, label='DES vertical strain')
    axes[1].set(xscale='log', xlabel='Radius (m)', ylabel='Contraction (microstrain)',
                title=f"(b) Strain split at t = {last['time_s']:.0f} s")
    axes[1].legend()
    fig.suptitle('Thin 3D DES slab vs the averaged-aquifer reference', x=0.06, ha='left',
                 fontsize=11, fontweight='semibold', y=1.02)
    for suffix in ('png',):
        fig.savefig(output / f'pumping_slab.{suffix}', dpi=180, bbox_inches='tight')
    plt.close(fig)


if __name__ == "__main__":
    import argparse
    from pathlib import Path
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("study", type=Path)
    a = p.parse_args()
    figure(*compare(a.study/"slab-3d"), a.study)
