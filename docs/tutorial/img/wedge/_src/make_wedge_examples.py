"""Generate ../wedge-examples.png: shaded-relief maps of two active convergent wedges, Taiwan (a
strong decollement) and the Fars arc of the Zagros (Hormuz salt), each with a swath profile of
topography across it at the same scale, and the mean surface slope fitted to the profile.

Topography and bathymetry: GMRT (Ryan et al. 2009, doi:10.1029/2008GC002332), CC BY 4.0,
downloaded from www.gmrt.org on first run and cached in the system temporary directory.
Run: python3 make_wedge_examples.py  (needs numpy and matplotlib)
"""
import os
import tempfile
import urllib.request
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import LightSource

HERE = os.path.dirname(os.path.abspath(__file__))
R = 6371.0   # km

# Profiles run from the foreland toward the hinterland; fit = the stretch (km along the profile,
# from where the topography starts to rise to the crest) the mean surface slope is fitted over.
REGIONS = {
    'taiwan': dict(box=(119.3, 122.3, 21.7, 25.5), res='low', title='Taiwan',
                   start=(120.0, 24.05), az=110.0, length=200.0, half=10.0, fit=(65, 122),
                   ends=('A', "A'"), xlim=(119.3, 122.3), ylim=(22.0, 25.4),
                   notes=[(15, 1.2, 'Taiwan Strait\n(foreland)'), (125, 3.95, 'Central Range'),
                          (205, 2.3, 'Philippine Sea plate\n(backstop)')]),
    'zagros': dict(box=(50.0, 58.0, 25.5, 31.5), res='low', title='Zagros, Fars arc',
                   start=(52.0, 27.0), az=28.0, length=440.0, half=15.0, fit=(80, 300),
                   ends=('B', "B'"), xlim=(50.0, 58.0), ylim=(25.5, 31.5),
                   notes=[(30, 1.2, 'Persian Gulf\n(foreland)'), (190, 3.6, 'folds over the Hormuz salt')]),
}


def load(name, box, res):
    f = os.path.join(tempfile.gettempdir(), f'gmrt-{name}.asc')
    if not os.path.exists(f):
        w, e, s, n = box
        url = ('https://www.gmrt.org/services/GridServer?'
               f'north={n}&west={w}&east={e}&south={s}&layer=topo&format=esriascii&resolution={res}')
        print('downloading', url)
        urllib.request.urlretrieve(url, f)
    h = {}
    with open(f) as fh:
        for _ in range(6):
            k, v = fh.readline().split()
            h[k] = float(v)
    z = np.loadtxt(f, skiprows=6)
    z[z == h['nodata_value']] = np.nan
    nr, nc = z.shape
    c = h['cellsize']
    lon = h['xllcorner'] + c * (np.arange(nc) + 0.5)
    lat = h['yllcorner'] + c * (np.arange(nr)[::-1] + 0.5)
    return lon, lat, z / 1e3                      # km


def offset(lon0, lat0, az, d):
    """Point d km from (lon0, lat0) along azimuth az (deg), on a sphere."""
    p1, l1, b, dr = map(np.radians, (lat0, lon0, az, 0.0))
    dr = d / R
    p2 = np.arcsin(np.sin(p1) * np.cos(dr) + np.cos(p1) * np.sin(dr) * np.cos(b))
    l2 = l1 + np.arctan2(np.sin(b) * np.sin(dr) * np.cos(p1), np.cos(dr) - np.sin(p1) * np.sin(p2))
    return np.degrees(l2), np.degrees(p2)


def swath(lon, lat, z, start, az, length, half):
    """Mean, minimum and maximum elevation in a swath 2*half km wide, every km along the line."""
    ds = np.arange(0.0, length + 0.5, 1.0)
    offs = np.arange(-half, half + 0.5, 1.0)
    c = lon[1] - lon[0]
    out = np.full((len(ds), len(offs)), np.nan)
    for i, d in enumerate(ds):
        lo, la = offset(*start, az, d)
        for j, o in enumerate(offs):
            lo2, la2 = offset(lo, la, az + 90.0, o)
            ix = int(round((lo2 - lon[0]) / c)); iy = int(round((lat[0] - la2) / c))
            if 0 <= ix < len(lon) and 0 <= iy < len(lat):
                out[i, j] = z[iy, ix]
    return ds, np.nanmean(out, 1), np.nanmin(out, 1), np.nanmax(out, 1)


if __name__ == '__main__':
    plt.rcParams.update({'font.size': 9})
    fig = plt.figure(figsize=(12, 9.4))
    gs = fig.add_gridspec(3, 2, height_ratios=[2.6, 1, 1], hspace=0.38, wspace=0.12)
    ls = LightSource(azdeg=315, altdeg=40)
    cmap = plt.get_cmap('gist_earth')
    VE = 25
    for k, (name, r) in enumerate(REGIONS.items()):
        lon, lat, z = load(name, r['box'], r['res'])
        ds, zm, zmin, zmax = swath(lon, lat, z, r['start'], r['az'], r['length'], r['half'])
        # map
        ax = fig.add_subplot(gs[0, k])
        dx = (lon[1] - lon[0]) * 111.2 * np.cos(np.radians(lat.mean()))
        rgb = ls.shade(np.nan_to_num(z, nan=0.0), cmap=cmap, vert_exag=0.05, dx=dx, dy=(lon[1] - lon[0]) * 111.2,
                       blend_mode='soft', vmin=-4, vmax=4)
        ax.imshow(rgb, extent=(lon[0], lon[-1], lat[-1], lat[0]), origin='upper')
        ax.set_aspect(1 / np.cos(np.radians(lat.mean())))
        ax.set_xlim(*r['xlim']); ax.set_ylim(*r['ylim'])
        p0 = r['start']; p1 = offset(*p0, r['az'], r['length'])
        for o in (-r['half'], r['half']):                       # swath outline
            q0 = offset(*p0, r['az'] + 90, o); q1 = offset(*p1, r['az'] + 90, o)
            ax.plot([q0[0], q1[0]], [q0[1], q1[1]], color='w', lw=0.8, ls='--')
        ax.plot([p0[0], p1[0]], [p0[1], p1[1]], color='#C2410C', lw=2)
        for (x, y), t in zip((p0, p1), r['ends']):
            ax.text(x, y, t, color='w', fontweight='bold', fontsize=12, ha='center', va='center',
                    bbox=dict(boxstyle='circle,pad=0.2', fc='#C2410C', ec='none'))
        ax.set_title(r['title'], fontweight='bold', loc='left')
        ax.set_xlabel('longitude (°E)')
        if k == 0:
            ax.set_ylabel('latitude (°N)')
        # profile, hinterland on the left as in the model and the sketch above
        axp = fig.add_subplot(gs[1 + k, :])
        i0, i1 = r['fit']
        x = ds - i0                     # 0 where the topography starts to rise, + toward the hinterland
        axp.fill_between(x, zmin, zmax, color='0.8', lw=0, label='swath minimum to maximum')
        axp.plot(x, zm, color='k', lw=1.2, label='swath mean')
        axp.axhline(0, color='#2F6FB0', lw=0.6)
        c = np.polyfit(ds[i0:i1 + 1], zm[i0:i1 + 1], 1)
        alpha = np.degrees(np.arctan(c[0]))
        axp.plot(x[i0:i1 + 1], np.polyval(c, ds[i0:i1 + 1]), color='#C2410C', lw=2.2,
                 label='mean surface slope α, fitted')
        for d, y, t in r['notes']:
            axp.text(d - i0, y, t, ha='center', va='top', fontsize=8.5, color='0.25')
        axp.text(x[0], -0.9, r['ends'][0], fontweight='bold', ha='center', color='#C2410C', fontsize=11)
        axp.text(x[-1], -0.9, r['ends'][1], fontweight='bold', ha='center', color='#C2410C', fontsize=11)
        axp.axvline(0, color='#C2410C', lw=0.8, ls=':')
        axp.set_xlim(375, -95); axp.set_ylim(-1.2, 4.0)
        axp.set_aspect(VE)
        axp.set_ylabel('elevation (km)')
        axp.set_title('%s: profile %s–%s, swath %d km wide, vertical exaggeration %d×'
                      % (r['title'], r['ends'][1], r['ends'][0], 2 * r['half'], VE), loc='left', fontsize=9)
        axp.text(0.985, 0.9, 'α = %.1f°' % alpha, transform=axp.transAxes, ha='right', va='top', fontsize=11,
                 fontweight='bold', color='#C2410C')
        print('%s: alpha = %.2f deg over %d-%d km' % (name, alpha, i0, i1))
    axp.set_xlabel('distance toward the hinterland from where the topography starts to rise (km); same scale in both profiles')
    fig.legend(*axp.get_legend_handles_labels(), loc='lower center', ncol=3, frameon=False,
               bbox_to_anchor=(0.5, 0.0))
    fig.text(0.99, 0.005, 'Topography: GMRT (Ryan et al. 2009), CC BY 4.0', ha='right', fontsize=7, color='0.4')
    fig.savefig(os.path.join(HERE, '..', 'wedge-examples.png'), dpi=130, bbox_inches='tight')
