"""Generate ../wedge-ramp-setup.svg: the three two-decollement geometries of the ramp-*.poly files,
a 40 x 5 km box with a lower decollement along the base from the pushing wall to x = xa and an
upper one at 1.5-2.5 km depth from x = xb to the right wall, drawn to scale at 2x vertical
exaggeration. Run: python3 make_ramp_setup.py
"""
import os

CASES = [('gap8', 12, 20, 'Gap of 8 km (xa = 12, xb = 20)'),
         ('ov2', 16, 14, 'Overlap of 2 km (xa = 16, xb = 14)'),
         ('ov14', 26, 12, 'Overlap of 14 km (xa = 26, xb = 12)')]
SX, SZ = 19.0, 38.0                       # px per km (2x vertical exaggeration)
X0 = 110
W, H = 1000, 130 + 262 * len(CASES)
C = dict(bg='#F7F6F2', rock='#E9D9B8', rock_e='#9A7B3F', dec='#BFD3E6', dec_e='#2F6FB0',
         txt='#374151', grey='#6B7280', push='#C2410C')

s = []
a = s.append
a(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" '
  'aria-label="Three model geometries with two decollements: a lower one along the base from the pushing '
  'wall to xa and an upper one at 1.5 to 2.5 km depth from xb to the right wall; an 8 km gap, a 2 km '
  'overlap and a 14 km overlap">')
a('<style>text{font-family:system-ui,-apple-system,"Segoe UI",Roboto,Arial,sans-serif}</style>')
a(f'<defs><marker id="ap" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto">'
  f'<path d="M0 0L10 5L0 10z" fill="{C["push"]}"/></marker>'
  f'<marker id="ag" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="4" markerHeight="4" orient="auto-start-reverse">'
  f'<path d="M0 0L10 5L0 10z" fill="{C["grey"]}"/></marker></defs>')
a(f'<rect width="{W}" height="{H}" rx="16" fill="{C["bg"]}"/>')
a(f'<text x="{W/2}" y="38" text-anchor="middle" font-size="21" font-weight="700" fill="{C["txt"]}">'
  'ramp-*.poly: two decollements, three arrangements</text>')
a(f'<text x="{W/2}" y="64" text-anchor="middle" font-size="14" fill="{C["grey"]}">'
  '40 × 5 km, vertical exaggeration 2×; both decollements 1 km thick, friction 1°; pushed from the left as before</text>')

for k, (name, xa, xb, title) in enumerate(CASES):
    y0 = 120 + 262 * k
    X = lambda x: X0 + SX * x
    Y = lambda z: y0 + SZ * (-z)
    a(f'<text x="{X0}" y="{y0 - 14}" font-size="16" font-weight="700" fill="{C["txt"]}">{title}</text>')
    a(f'<rect x="{X(0)}" y="{Y(0)}" width="{SX*40}" height="{SZ*5}" fill="{C["rock"]}" stroke="{C["rock_e"]}"/>')
    a(f'<rect x="{X(0)}" y="{Y(-4)}" width="{SX*xa}" height="{SZ}" fill="{C["dec"]}" stroke="{C["dec_e"]}" stroke-width="1.5"/>')
    a(f'<rect x="{X(xb)}" y="{Y(-1.5)}" width="{SX*(40-xb)}" height="{SZ}" fill="{C["dec"]}" stroke="{C["dec_e"]}" stroke-width="1.5"/>')
    a(f'<text x="{X(xa/2)}" y="{Y(-4.5)+5}" text-anchor="middle" font-size="13" fill="{C["dec_e"]}">lower decollement</text>')
    a(f'<text x="{X((xb+40)/2)}" y="{Y(-2)+5}" text-anchor="middle" font-size="13" fill="{C["dec_e"]}">upper decollement</text>')
    for x, lab, z in ((xa, 'xa', -5), (xb, 'xb', -1.5)):
        y1 = Y(z) + (20 if z == -5 else -20)
        a(f'<line x1="{X(x)}" y1="{Y(z)}" x2="{X(x)}" y2="{y1}" stroke="{C["grey"]}" stroke-dasharray="3 3"/>')
        a(f'<text x="{X(x)}" y="{y1 + (14 if z == -5 else -4)}" text-anchor="middle" font-size="13" '
          f'font-weight="600" fill="{C["grey"]}">{lab} = {x} km</text>')
    a(f'<line x1="{X(0)-60}" y1="{Y(-2.5)}" x2="{X(0)-6}" y2="{Y(-2.5)}" stroke="{C["push"]}" stroke-width="3" marker-end="url(#ap)"/>')
    a(f'<line x1="{X(0)}" y1="{Y(0)}" x2="{X(0)}" y2="{Y(-5)}" stroke="{C["push"]}" stroke-width="3"/>')
    if k == 0:
        for z0, z1, t in ((0, -1.5, '1.5'), (-1.5, -2.5, '1'), (-2.5, -4, '1.5'), (-4, -5, '1')):
            xd = X(40) + 22
            a(f'<line x1="{xd}" y1="{Y(z0)}" x2="{xd}" y2="{Y(z1)}" stroke="{C["grey"]}" marker-start="url(#ag)" marker-end="url(#ag)"/>')
            a(f'<text x="{xd + 6}" y="{(Y(z0)+Y(z1))/2 + 5}" font-size="12" fill="{C["grey"]}">{t} km</text>')

a('</svg>')
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'wedge-ramp-setup.svg')
with open(out, 'w') as f:
    f.write('\n'.join(s) + '\n')
print('wrote', out)
