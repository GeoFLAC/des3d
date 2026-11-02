"""Generate ../wedge-setup.svg: the initial geometry and boundary conditions of wedge-phi1.cfg and
wedge-phi5.cfg. A 40 x 4 km box at 3x vertical exaggeration: a 3 km brittle layer over a 1 km
decollement, the left wall pushing at 5 cm/yr with the push tapered to 0 across the decollement
(vbc_x0 = 3, bottom_shear_zone_thickness), a free-slip right wall, a no-slip base and a free surface
with hillslope diffusion. Run: python3 make_wedge_setup.py
"""
import os

SX, SZ = 16.5, 49.5                        # px per km, horizontal and vertical (3x exaggeration)
X0, Y0 = 200, 120                          # px of (x = 0, z = 0)
def X(x): return X0 + SX * x
def Y(z): return Y0 - SZ * z
C = dict(bg='#F7F6F2', rock='#E9D9B8', rock_e='#9A7B3F', dec='#BFD3E6', dec_e='#2F6FB0',
         grey='#6B7280', txt='#374151', push='#C2410C')
W, H = 1000, 500

s = []
a = s.append
a(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" '
  'aria-label="Initial setup of the wedge models: a 40 by 4 km box, a 3 km brittle layer over a 1 km '
  'decollement, pushed from the left wall at 5 cm/yr with the push tapering to zero across the '
  'decollement, a free-slip right wall, a no-slip base and a free surface with hillslope diffusion">')
a('<style>text{font-family:system-ui,-apple-system,"Segoe UI",Roboto,Arial,sans-serif}</style>')
a('<defs>')
a(f'<marker id="ap" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto"><path d="M0 0L10 5L0 10z" fill="{C["push"]}"/></marker>')
a(f'<marker id="ag" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="{C["grey"]}"/></marker>')
a(f'<pattern id="hatch" width="8" height="8" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><line x1="0" y1="0" x2="0" y2="8" stroke="{C["grey"]}" stroke-width="1.5"/></pattern>')
a('</defs>')
a(f'<rect width="{W}" height="{H}" rx="16" fill="{C["bg"]}"/>')
a(f'<text x="{W/2}" y="40" text-anchor="middle" font-size="22" font-weight="700" fill="{C["txt"]}">'
  'wedge-phi1.cfg / wedge-phi5.cfg: initial geometry and boundary conditions</text>')

# layers
a(f'<rect x="{X(0)}" y="{Y(0)}" width="{X(40)-X(0)}" height="{Y(-3)-Y(0)}" fill="{C["rock"]}" stroke="{C["rock_e"]}" stroke-width="1.2"/>')
a(f'<rect x="{X(0)}" y="{Y(-3)}" width="{X(40)-X(0)}" height="{Y(-4)-Y(-3)}" fill="{C["dec"]}" stroke="{C["dec_e"]}" stroke-width="1.2"/>')
a(f'<text x="{X(22)}" y="{Y(-1.25)}" text-anchor="middle" font-size="17" font-weight="600" fill="{C["txt"]}">brittle layer, material 0</text>')
a(f'<text x="{X(22)}" y="{Y(-1.25)+24}" text-anchor="middle" font-size="15" fill="{C["txt"]}">'
  'friction 30° → 15°, cohesion 4 → 0.4 MPa over plastic strain 0 → 0.1</text>')
a(f'<text x="{X(22)}" y="{Y(-3.5)+6}" text-anchor="middle" font-size="15" font-weight="600" fill="{C["dec_e"]}">'
  'decollement, material 1: friction 1° (phi1) or 5° (phi5), same cohesion</text>')

# free surface
a(f'<text x="{X(40)}" y="{Y(0)-12}" text-anchor="end" font-size="14" fill="{C["grey"]}">'
  'free surface, hillslope diffusion (surface_diffusivity = 1e-6 m²/s)</text>')

# base: no slip
a(f'<rect x="{X(0)}" y="{Y(-4)}" width="{X(40)-X(0)}" height="12" fill="url(#hatch)"/>')
a(f'<text x="{X(20)}" y="{Y(-4)+34}" text-anchor="middle" font-size="14" fill="{C["grey"]}">'
  'no-slip base: vx = vz = 0 (vbc_z0 = 3)</text>')

# right wall: free slip (rollers)
for z in (-0.5, -1.5, -2.5, -3.5):
    a(f'<circle cx="{X(40)+7}" cy="{Y(z)}" r="6" fill="none" stroke="{C["grey"]}" stroke-width="1.5"/>')
a(f'<line x1="{X(40)+14}" y1="{Y(0)}" x2="{X(40)+14}" y2="{Y(-4)}" stroke="{C["grey"]}" stroke-width="2"/>')
a(f'<text x="{X(40)+24}" y="{Y(-1.6)}" font-size="14" fill="{C["grey"]}">free slip</text>')
a(f'<text x="{X(40)+24}" y="{Y(-1.6)+18}" font-size="14" fill="{C["grey"]}">vx = 0</text>')
a(f'<text x="{X(40)+24}" y="{Y(-1.6)+36}" font-size="13" fill="{C["grey"]}">(vbc_x1 = 1)</text>')

# left wall: push, tapered across the decollement
a(f'<line x1="{X(0)}" y1="{Y(0)}" x2="{X(0)}" y2="{Y(-4)}" stroke="{C["push"]}" stroke-width="3"/>')
L = 70.0  # px for 5 cm/yr
for z in (-0.25, -1.0, -1.75, -2.5, -3.0, -3.33, -3.67):
    f = min(1.0, (z + 4) / 1.0)
    if f <= 0:
        continue
    a(f'<line x1="{X(0)-L*f-6:.1f}" y1="{Y(z):.1f}" x2="{X(0)-4:.1f}" y2="{Y(z):.1f}" stroke="{C["push"]}" stroke-width="2.4" marker-end="url(#ap)"/>')
# velocity profile envelope
a(f'<polyline points="{X(0)-L-6:.1f},{Y(0):.1f} {X(0)-L-6:.1f},{Y(-3):.1f} {X(0)-6:.1f},{Y(-4):.1f}" fill="none" stroke="{C["push"]}" stroke-width="1.2" stroke-dasharray="4 3"/>')
a(f'<text x="{X(0)-L/2-6}" y="{Y(0)-30}" text-anchor="middle" font-size="15" font-weight="600" fill="{C["push"]}">5 cm/yr</text>')
a(f'<text x="{X(0)-L/2-6}" y="{Y(0)-12}" text-anchor="middle" font-size="13" fill="{C["push"]}">vz = 0 on the wall</text>')

# dimensions
yd = Y(-4) + 64
a(f'<line x1="{X(0)}" y1="{yd}" x2="{X(40)}" y2="{yd}" stroke="{C["grey"]}" stroke-width="1.2" marker-start="url(#ag)" marker-end="url(#ag)"/>')
a(f'<text x="{X(20)}" y="{yd-6}" text-anchor="middle" font-size="14" fill="{C["grey"]}">xlength = 40 km</text>')
xd = X(0) - 120
a(f'<line x1="{xd}" y1="{Y(0)}" x2="{xd}" y2="{Y(-3)}" stroke="{C["grey"]}" stroke-width="1.2" marker-start="url(#ag)" marker-end="url(#ag)"/>')
a(f'<text x="{xd-6}" y="{Y(-1.5)+5}" text-anchor="end" font-size="14" fill="{C["grey"]}">3 km</text>')
a(f'<line x1="{xd}" y1="{Y(-3)}" x2="{xd}" y2="{Y(-4)}" stroke="{C["grey"]}" stroke-width="1.2" marker-start="url(#ag)" marker-end="url(#ag)"/>')
a(f'<text x="{xd-6}" y="{Y(-3.5)+5}" text-anchor="end" font-size="14" fill="{C["grey"]}">1 km</text>')

# legend of the taper and remeshing note
yn = yd + 40
notes = [
    'The push tapers linearly to 0 over the lowest bottom_shear_zone_thickness = 1 km, so the wall meets the',
    'fixed base without a velocity jump. The wall foot then lags its top; remeshing_option = 12 makes the wall',
    'vertical again at every remesh. Vertical exaggeration 3×; uniform mesh, resolution = 250 m.',
]
for i, t in enumerate(notes):
    a(f'<text x="{W/2}" text-anchor="middle" y="{yn + 22*i}" font-size="14" fill="{C["txt"]}">{t}</text>')

a('</svg>')
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'wedge-setup.svg')
with open(out, 'w') as f:
    f.write('\n'.join(s) + '\n')
print('wrote', out)
