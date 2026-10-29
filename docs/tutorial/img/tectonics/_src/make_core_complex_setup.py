"""Generate ../core-complex-setup.svg: the initial geometry and mesh of examples/core-complex.cfg with the
parameters that set them annotated (no material properties: those are in the config walkthrough). 100 x 10 km box at 2x vertical exaggeration; the refined zone, the planar weak-zone seed
(|x - x0 + z / tan(inclination)| < halfwidth, within the depth range), the wall velocities, the free
surface and the Winkler bottom. Run: python3 make_core_complex_setup.py
"""
import math
import os

SX, SZ = 8.0, 16.0                         # px per km, horizontal and vertical (2x exaggeration)
X0, Y0 = 80, 120                           # px of (x = 0, z = 0)
def X(x): return X0 + SX * x
def Y(z): return Y0 - SZ * z
C = dict(bg='#F7F6F2', rock='#CFE0F0', rock_e='#2F6FB0', fine='#E3ECF6', weak='#E8A33D', weak_e='#B5651D',
         grey='#6B7280', txt='#374151', arrow='#6B7280')

# weak zone: plane through (50, 0), inclination -60 deg -> x = 50 + z / tan(-60) = 50 - 0.577 z... (ic.cxx Planar_zone)
incl = 1 / math.tan(math.radians(-60)); hw = 1.2
def xw(z): return 50 + incl * (z - 0) * (-1)      # ic.cxx: |(x - x0) + incl (z - z0)| < hw  ->  x = x0 - incl (z - z0)
zt, zb = -5, -10                                   # weakzone_depth_min/max = 0.5, 1.0 of zlength
band = [(xw(zt) - hw, zt), (xw(zt) + hw, zt), (xw(zb) + hw, zb), (xw(zb) - hw, zb)]

s = []
a = s.append
a('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 960 372" width="960" height="372" role="img" aria-label="Initial setup of core-complex.cfg: a 100 by 10 km elasto-plastic layer pulled apart at 3.15 cm/yr per wall, with a refined mesh zone between 30 and 70 km and a planar weak-zone seed dipping 60 degrees in the lower half of the layer under x = 50 km; free surface with hillslope diffusion on top, Winkler foundation below">')
a('<style>text{font-family:system-ui,-apple-system,"Segoe UI",Roboto,Arial,sans-serif}</style>')
a('<defs>')
a('<marker id="ab" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto"><path d="M0 0L10 5L0 10z" fill="#6B7280"/></marker>')
a('</defs>')
a(f'<rect width="960" height="372" rx="16" fill="{C["bg"]}"/>')
a(f'<text x="480" y="34" text-anchor="middle" font-size="22" font-weight="700" fill="{C["txt"]}">core-complex.cfg: initial geometry and mesh</text>')
# layer with coarse pattern, refined zone with fine pattern
a(f'<rect x="{X(0)}" y="{Y(0)}" width="{X(100)-X(0)}" height="{Y(-10)-Y(0)}" fill="{C["rock"]}"/>')
a(f'<rect x="{X(30)}" y="{Y(0)}" width="{X(70)-X(30)}" height="{Y(-10)-Y(0)}" fill="{C["fine"]}"/>')
# one representative element per zone: an equilateral triangle of edge 1 km inside, and of the coarse
# zone's size outside (largest_size = 10 x the area -> edge sqrt(10) ~ 3.2 km), drawn to scale
def tri(xc, zc, edge, col):
    h = edge * math.sqrt(3) / 2
    pts = [(xc - edge / 2, zc - h / 3), (xc + edge / 2, zc - h / 3), (xc, zc + 2 * h / 3)]
    a(f'<polygon points="{" ".join(f"{X(x):.1f},{Y(z):.1f}" for x, z in pts)}" fill="white" fill-opacity="0.9" stroke="{col}" stroke-width="1.6"/>')
tri(50, -2.3, 1.0, C['rock_e']); tri(20, -2.6, math.sqrt(10), C['grey']); tri(93, -2.6, math.sqrt(10), C['grey'])
a(f'<text x="{X(50):.0f}" y="{Y(-3.6):.0f}" text-anchor="middle" font-size="11" fill="{C["rock_e"]}">1 km element</text>')
a(f'<text x="{X(20):.0f}" y="{Y(-5.0):.0f}" text-anchor="middle" font-size="11" fill="{C["grey"]}">up to ~3.2 km</text>')
a(f'<text x="{X(93):.0f}" y="{Y(-5.0):.0f}" text-anchor="middle" font-size="11" fill="{C["grey"]}">up to ~3.2 km</text>')
a(f'<rect x="{X(0)}" y="{Y(0)}" width="{X(100)-X(0)}" height="{Y(-10)-Y(0)}" fill="none" stroke="{C["rock_e"]}" stroke-width="2"/>')
a(f'<line x1="{X(30)}" y1="{Y(0)}" x2="{X(30)}" y2="{Y(-10)}" stroke="{C["rock_e"]}" stroke-width="1" stroke-dasharray="4 3"/>')
a(f'<line x1="{X(70)}" y1="{Y(0)}" x2="{X(70)}" y2="{Y(-10)}" stroke="{C["rock_e"]}" stroke-width="1" stroke-dasharray="4 3"/>')
# weak zone band and its plane
pts = ' '.join(f'{X(x):.1f},{Y(z):.1f}' for x, z in band)
a(f'<polygon points="{pts}" fill="{C["weak"]}" fill-opacity="0.85" stroke="{C["weak_e"]}" stroke-width="1.5"/>')
a(f'<line x1="{X(xw(0)):.1f}" y1="{Y(0):.1f}" x2="{X(xw(zt)):.1f}" y2="{Y(zt):.1f}" stroke="{C["weak_e"]}" stroke-width="1.2" stroke-dasharray="5 4"/>')
a(f'<circle cx="{X(50):.1f}" cy="{Y(0):.1f}" r="4" fill="{C["weak_e"]}"/>')
# labels: refined zone
a(f'<text x="{X(50):.0f}" y="{Y(0)-34:.0f}" text-anchor="middle" font-size="13" fill="{C["rock_e"]}">refined zone, refined_zonex = [0.3, 0.7]: resolution = 1 km</text>')
a(f'<text x="{X(15):.0f}" y="{Y(0)-34:.0f}" text-anchor="middle" font-size="12" fill="{C["grey"]}">outside: coarser, up to</text>')
a(f'<text x="{X(15):.0f}" y="{Y(0)-19:.0f}" text-anchor="middle" font-size="12" fill="{C["grey"]}">largest_size = 10× the area</text>')
# free surface and bottom
a(f'<text x="{X(85):.0f}" y="{Y(0)-19:.0f}" text-anchor="middle" font-size="12" fill="{C["grey"]}">free surface, hillslope diffusion</text>')
a(f'<text x="{X(85):.0f}" y="{Y(0)-34:.0f}" text-anchor="middle" font-size="12" fill="{C["grey"]}">surface_diffusivity = 1e-7 m²/s</text>')
a(f'<text x="480" y="{Y(-10)+40:.0f}" text-anchor="middle" font-size="13" fill="{C["grey"]}">Winkler foundation: lithostatic support, free to move vertically; remeshing_option = 11 restores it to 10 km</text>')
# wall velocities
a(f'<path d="M{X(0)-14} {Y(-5)} L{X(0)-62} {Y(-5)}" stroke="{C["arrow"]}" stroke-width="3" marker-end="url(#ab)" fill="none"/>')
a(f'<path d="M{X(100)+14} {Y(-5)} L{X(100)+62} {Y(-5)}" stroke="{C["arrow"]}" stroke-width="3" marker-end="url(#ab)" fill="none"/>')
a(f'<text x="{X(0)-38:.0f}" y="{Y(-5)+26:.0f}" text-anchor="middle" font-size="13" fill="{C["txt"]}">3.15 cm/yr</text>')
a(f'<text x="4" y="{Y(-5)+42:.0f}" text-anchor="start" font-size="11" fill="{C["grey"]}">vbc_val_x0 = −1e-9</text>')
a(f'<text x="{X(100)+38:.0f}" y="{Y(-5)+26:.0f}" text-anchor="middle" font-size="13" fill="{C["txt"]}">3.15 cm/yr</text>')
a(f'<text x="956" y="{Y(-5)+42:.0f}" text-anchor="end" font-size="11" fill="{C["grey"]}">vbc_val_x1 = +1e-9</text>')
# weak zone callout (right of the band, inside the layer)
cx = X(56); cy = Y(-5.6)
a(f'<rect x="{cx-6:.0f}" y="{cy-14:.0f}" width="258" height="66" rx="4" fill="white" fill-opacity="0.8"/>')
a(f'<path d="M{X(xw(-7.0)+hw)+2:.1f} {Y(-7.0):.1f} L{cx-6:.0f} {cy+20:.0f}" stroke="{C["weak_e"]}" stroke-width="1.2" fill="none"/>')
a(f'<text x="{cx:.0f}" y="{cy:.0f}" font-size="13" font-weight="700" fill="{C["weak_e"]}">weak-zone seed (weakzone_option = 1)</text>')
a(f'<text x="{cx:.0f}" y="{cy+16:.0f}" font-size="12" fill="{C["weak_e"]}">plane through (50 km, 0), inclination −60°</text>')
a(f'<text x="{cx:.0f}" y="{cy+31:.0f}" font-size="12" fill="{C["weak_e"]}">halfwidth 1.2 km, depth 0.5–1.0 (lower 5 km)</text>')
a(f'<text x="{cx:.0f}" y="{cy+46:.0f}" font-size="12" fill="{C["weak_e"]}">plstrain 0.5 = pls1: already fully softened</text>')
# axes ticks
for xk in (0, 30, 50, 70, 100):
    a(f'<line x1="{X(xk)}" y1="{Y(-10)+3}" x2="{X(xk)}" y2="{Y(-10)+10}" stroke="{C["grey"]}" stroke-width="2"/>')
    a(f'<text x="{X(xk)}" y="{Y(-10)+24}" text-anchor="middle" font-size="12" fill="{C["txt"]}">{xk} km</text>')
for zk in (0, -5, -10):
    a(f'<line x1="{X(0)-8}" y1="{Y(zk)}" x2="{X(0)-1}" y2="{Y(zk)}" stroke="{C["grey"]}" stroke-width="2"/>')
    a(f'<text x="{X(0)-12}" y="{Y(zk)+4}" text-anchor="end" font-size="12" fill="{C["txt"]}">{zk}</text>')
a(f'<text x="480" y="356" text-anchor="middle" font-size="12" fill="{C["grey"]}">100 × 10 km box (xlength, zlength), meshing_option = 2; vertical exaggeration 2×</text>')
a('</svg>')
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'core-complex-setup.svg')
open(out, 'w').write('\n'.join(s) + '\n'); print(out)
