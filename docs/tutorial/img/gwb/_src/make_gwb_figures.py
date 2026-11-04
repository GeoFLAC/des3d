"""Generate the figures of the Geodynamic World Builder tutorial from DES runs of the
DynEarthSol examples (build with usegwb=1; set DES_DIR to the DynEarthSol directory):

    gwb-subduction.png     examples/gwb-subduction.cfg, frame 0
    gwb-core-complex.png   examples/core-complex.cfg and gwb-core-complex.cfg, frame 0
    gwb-slab-3d.png        examples/gwb-slab-3d.cfg, frame 0

Run: python3 make_gwb_figures.py SUBDUCTION_DIR CORE_COMPLEX_DIR SLAB3D_DIR
where each directory holds the output of the run(s) named above.
"""
import os
import sys
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.tri as mtri
from matplotlib.colors import ListedColormap
from mpl_toolkits.axes_grid1 import make_axes_locatable

sys.path.insert(0, os.environ.get('DES_DIR', '.'))
from Dynearthsol import Dynearthsol

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
MATS = ListedColormap(['#2F6FB0', '#C2410C', '#E8E2D0'])
MAT_NAMES = ['oceanic crust', 'continental crust', 'mantle']
plt.rcParams.update({'font.size': 9})


def cbar_axes(ax):
    """A colorbar slot beside ax, so stacked panels keep the same width."""
    return make_axes_locatable(ax).append_axes('right', size='1.5%', pad=0.08)


def weak_outline(ax, tri, pls, color='#16A34A'):
    """Draw the edges of the weak elements (plastic strain > 0)."""
    w = pls > 0
    if w.any():
        ax.triplot(mtri.Triangulation(tri.x, tri.y, tri.triangles[w]), color=color, lw=0.9)


def subduction(d):
    xy = d.read_field(0, 'coordinate') / 1e3
    conn = d.read_field(0, 'connectivity')
    tri = mtri.Triangulation(xy[:, 0], xy[:, 1], conn)
    T = d.read_field(0, 'temperature')
    pls = d.read_field(0, 'plastic strain')
    mk = d.read_markers(0, 'markerset')
    p, mt = mk['markerset.coord'] / 1e3, mk['markerset.mattype']
    fig, ax = plt.subplots(3, 1, figsize=(11, 9.5), sharex=True)
    for a in ax:
        a.set_aspect('equal')
    im = ax[0].tripcolor(tri, T, shading='gouraud', cmap='inferno')
    ax[0].tricontour(tri, T, levels=np.arange(473, 1573, 200), colors='w', linewidths=0.6)
    fig.colorbar(im, cax=cbar_axes(ax[0]), label='temperature (K)')
    ax[0].set_title('temperature_option = 936: temperature at every node (contours every 200 K)',
                    loc='left')
    sc = ax[1].scatter(p[:, 0], p[:, 1], c=mt, cmap=MATS, vmin=-0.5, vmax=2.5, s=1.0, linewidths=0)
    cb = fig.colorbar(sc, cax=cbar_axes(ax[1]), ticks=[0, 1, 2])
    cb.ax.set_yticklabels(MAT_NAMES)
    ax[1].set_title('mattype_option = 936: GWB composition i is mattype i, on each marker',
                    loc='left')
    ax[2].triplot(tri, color='0.7', lw=0.3)
    weak_outline(ax[2], tri, pls)
    ax[2].set_title('weakzone_option = 936: weakzone_plstrain (green) in the elements of the '
                    'plate-interface fault; %d elements' % len(conn), loc='left')
    cbar_axes(ax[2]).axis('off')
    for a in ax:
        a.set_ylabel('z (km)')
        a.set_xlim(0, 600)
        a.set_ylim(-200, 5)
    ax[2].set_xlabel('x (km)')
    fig.savefig(os.path.join(OUT, 'gwb-subduction.png'), dpi=130, bbox_inches='tight')


def core_complex(planar, gwb):
    fig, ax = plt.subplots(2, 1, figsize=(11, 4.6), sharex=True)
    for a, d, t in ((ax[0], planar, 'core-complex.cfg: weakzone_option = 1, a planar zone'),
                    (ax[1], gwb, 'gwb-core-complex.cfg: weakzone_option = 936, a GWB fault feature')):
        xy = d.read_field(0, 'coordinate') / 1e3
        tri = mtri.Triangulation(xy[:, 0], xy[:, 1], d.read_field(0, 'connectivity'))
        pls = d.read_field(0, 'plastic strain')
        a.triplot(tri, color='0.7', lw=0.3)
        weak_outline(a, tri, pls)
        a.set_title('%s: %d weak elements' % (t, (pls > 0).sum()), loc='left')
        # the fault plane through (50 km, 0) dipping 60 degrees toward -x, 5 to 10 km deep
        z = np.array([-5.0, -10.0])
        a.plot(50 + z / np.tan(np.radians(60)), z, color='k', lw=1, ls='--')
        a.set_xlim(30, 70)
        a.set_aspect('equal')
        a.set_ylabel('z (km)')
    ax[1].set_xlabel('x (km); dashed: the plane of the seed fault, 5 to 10 km deep')
    fig.savefig(os.path.join(OUT, 'gwb-core-complex.png'), dpi=130, bbox_inches='tight')


def slab3d(d, y0=50.0, half=4.0):
    xyz = d.read_field(0, 'coordinate') / 1e3
    T = d.read_field(0, 'temperature')
    mk = d.read_markers(0, 'markerset')
    p, mt = mk['markerset.coord'] / 1e3, mk['markerset.mattype']
    conn = d.read_field(0, 'connectivity')
    pls = d.read_field(0, 'plastic strain')
    cen = xyz[conn].mean(axis=1)
    fig, ax = plt.subplots(2, 1, figsize=(10, 6.6), sharex=True)
    for a in ax:
        a.set_aspect('equal')
    n = np.abs(xyz[:, 1] - y0) < 1.5 * half
    tn = mtri.Triangulation(xyz[n, 0], xyz[n, 2])
    im = ax[0].tripcolor(tn, T[n], shading='gouraud', cmap='inferno')
    ax[0].tricontour(tn, T[n], levels=np.arange(473, 1573, 200), colors='w', linewidths=0.6)
    fig.colorbar(im, cax=cbar_axes(ax[0]), label='temperature (K)')
    ax[0].set_title('temperature at the nodes within %g km of y = %g km (contours every 200 K)'
                    % (1.5 * half, y0), loc='left')
    m = np.abs(p[:, 1] - y0) < half
    sc = ax[1].scatter(p[m, 0], p[m, 2], c=mt[m], cmap=MATS, vmin=-0.5, vmax=2.5, s=2, linewidths=0)
    e = (np.abs(cen[:, 1] - y0) < half) & (pls > 0)
    ax[1].scatter(cen[e, 0], cen[e, 2], s=14, facecolors='none', edgecolors='#16A34A', linewidths=0.9)
    cb = fig.colorbar(sc, cax=cbar_axes(ax[1]), ticks=[0, 1, 2])
    cb.ax.set_yticklabels(MAT_NAMES)
    ax[1].set_title('markers within %g km of y = %g km by material; green circles: weak elements '
                    'of the fault' % (half, y0), loc='left')
    for a in ax:
        a.set_ylabel('z (km)')
        a.set_xlim(0, 200)
        a.set_ylim(-100, 2)
    ax[1].set_xlabel('x (km)')
    fig.savefig(os.path.join(OUT, 'gwb-slab-3d.png'), dpi=130, bbox_inches='tight')


if __name__ == '__main__':
    sub_dir, cc_dir, s3_dir = sys.argv[1:4]
    subduction(Dynearthsol(os.path.join(sub_dir, 'gwb-subduction')))
    core_complex(Dynearthsol(os.path.join(cc_dir, 'result3')),
                 Dynearthsol(os.path.join(cc_dir, 'gwb-core-complex')))
    slab3d(Dynearthsol(os.path.join(s3_dir, 'gwb-slab-3d')))
