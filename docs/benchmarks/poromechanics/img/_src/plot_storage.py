"""Plot saved before/after Biot storage comparisons."""
from des import ROOT
import prepare_figures as pf
import numpy as np
import json

def plot(output, biot):
    cases = {label: {dim: pf.load_case(output / label, dim) for dim in (2, 3)}
             for label in ('before', 'after')}
    fig, axes = pf.plt.subplots(3, 2, figsize=(11, 11), constrained_layout=True)
    summary = {}
    for col, dim in enumerate((2, 3)):
        ref = cases['after'][dim]['reference']
        time = np.linspace(0, max(cases[label][dim]['times'][-1] for label in cases), 800)
        axes[0, col].plot(time, ref.pressure([ref.height], time)[:, 0] / 1000,
                          color='0.15', label='Biot analytical')
        axes[1, col].plot(time, ref.settlement(time) * 1000, color='0.15', label='Biot analytical')
        for label, color, marker in (('before', '#D55E00', 'x'), ('after', '#0072B2', 'o')):
            c = cases[label][dim]
            active = c['times'] > 0
            t = c['times'][active]
            p = c['pressure'][active][:, np.isclose(c['depth'], ref.height)].mean(axis=1)
            axes[0, col].plot(t[::3], p[::3] / 1000, marker, color=color,
                              markersize=4, fillstyle='none', label=label.capitalize())
            axes[1, col].plot(t[::3], c['settlement'][active][::3] * 1000, marker,
                              color=color, markersize=4, fillstyle='none', label=label.capitalize())
            axes[2, col].semilogy(t, c['pressure_error'][active] * 100, color=color,
                                  label=f'{label}: pressure / load')
            axes[2, col].semilogy(t, c['settlement_error'][active] * 100, '--', color=color,
                                  label=f'{label}: settlement / drained')
            summary.setdefault(label, {})[str(dim)] = c['metrics']
        axes[0, col].set(title=f'{dim}D: pressure dissipation', ylabel='Bottom excess pressure (kPa)')
        axes[1, col].set(title=f'{dim}D: settlement', ylabel='Settlement (mm)')
        axes[2, col].set(title='All post-load frames and pressure nodes',
                         ylabel='Normalized absolute error (%)')
    for ax in axes.flat:
        ax.set_xlabel('Time (s)')
        ax.grid(alpha=0.22)
        ax.legend(fontsize=8)
    fig.suptitle(f'Actual DES before/after Biot storage correction — α = {biot:g}\n'
                 'Same mesh, inputs and PT tolerances · each frame compared at its actual time', fontsize=13)
    pf.save_figure(fig, output, 'biot_storage_comparison')
    summary['biot'] = biot
    summary['provenance'] = json.loads((output / 'provenance.json').read_text())
    summary['notes'] = ['Frame zero is pre-load and excluded from analytical error metrics.',
                        'This is a coarse-column regression, not a mesh/time convergence claim.',
                        'Pressure error is normalized by applied load; settlement by drained settlement.']
    (output / 'summary.json').write_text(json.dumps(summary, indent=2) + '\n')

if __name__ == '__main__':
    import argparse
    from pathlib import Path
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('study', type=Path)
    a = p.parse_args()
    plot(a.study, json.loads((a.study/'settings.json').read_text())['biot'])
