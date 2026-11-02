"""Generate ../wedge-anatomy.svg: a schematic convergent wedge (backstop, wedge, decollement,
forethrusts, a backthrust and pop-up, the deformation front, the taper angles alpha and beta),
and below it two sketches contrasting a wedge over a strong decollement (narrow, steep,
forward-verging thrusts) with one over salt (wide, low, symmetric folds of both vergences),
after Davis & Engelder (1985) and Dahlen (1990). Schematic, vertically exaggerated.
Run: python3 make_wedge_anatomy.py
"""
import math
import os

W, H = 1000, 700
C = dict(bg='#F7F6F2', txt='#374151', grey='#6B7280', back='#9CA3AF', back_e='#4B5563',
         wedge='#E9D9B8', wedge_e='#9A7B3F', fore='#F3EAD7', base='#D6D3D1', dec='#2F6FB0',
         salt='#F2B8C6', salt_e='#BE185D', fault='#B91C1C', push='#C2410C')

s = []
a = s.append
a(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" '
  'aria-label="Schematic convergent wedge: a backstop on the left pushes a wedge of sedimentary rock over '
  'a weak decollement; forethrusts and a backthrust cut the wedge, the surface slopes at alpha and the '
  'decollement dips at beta toward the backstop; below, a narrow steep wedge over a strong decollement '
  'beside a wide low wedge over salt">')
a('<style>text{font-family:system-ui,-apple-system,"Segoe UI",Roboto,Arial,sans-serif}</style>')
a('<defs>'
  f'<marker id="ap" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto"><path d="M0 0L10 5L0 10z" fill="{C["push"]}"/></marker>'
  f'<marker id="ag" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="4" markerHeight="4" orient="auto"><path d="M0 0L10 5L0 10z" fill="{C["grey"]}"/></marker>'
  '</defs>')
a(f'<rect width="{W}" height="{H}" rx="16" fill="{C["bg"]}"/>')
a(f'<text x="{W/2}" y="36" text-anchor="middle" font-size="21" font-weight="700" fill="{C["txt"]}">'
  'Anatomy of a convergent wedge (schematic, vertically exaggerated)</text>')

# ---------------------------------------------------------------- top panel: anatomy
X0, X1 = 270, 930           # wedge rear (against the backstop) and right edge of the foreland
XF = 760                    # deformation front
def ydec(x):                # decollement, dipping toward the backstop at beta
    return 330 - 0.05 * (x - X0)
def ysurf(x):               # wedge surface, sloping toward the foreland at alpha; flat foreland
    return 140 + (262 - 140) * (x - X0) / (XF - X0) if x <= XF else 262
DT = 9                      # decollement layer thickness, px

pts = lambda P: ' '.join(f'{x:.1f},{y:.1f}' for x, y in P)
xs = [X0 + i * 5 for i in range((X1 - X0) // 5 + 1)]
# basement, decollement layer, foreland strata and wedge
a(f'<polygon points="{pts([(X0 - 40, ydec(X0 - 40) + DT)] + [(x, ydec(x) + DT) for x in xs] + [(X1, 372), (X0 - 40, 372)])}" fill="{C["base"]}"/>')
a(f'<polygon points="{pts([(x, ydec(x)) for x in xs] + [(x, ydec(x) + DT) for x in xs[::-1]])}" fill="{C["dec"]}" fill-opacity="0.85"/>')
a(f'<polygon points="{pts([(XF, ysurf(XF)), (X1, 262), (X1, ydec(X1)), (XF, ydec(XF))])}" fill="{C["fore"]}" stroke="{C["wedge_e"]}" stroke-width="1"/>')
for k in (1, 2):            # undeformed foreland layering
    y0 = 262 + k * (ydec(XF) - 262) / 3
    a(f'<line x1="{XF}" y1="{y0:.1f}" x2="{X1}" y2="{y0 + (ydec(X1) - ydec(XF)) * k / 3:.1f}" stroke="{C["wedge_e"]}" stroke-width="0.8" stroke-dasharray="5 3"/>')
wx = [x for x in xs if x <= XF]
a(f'<polygon points="{pts([(x, ysurf(x)) for x in wx] + [(x, ydec(x)) for x in wx[::-1]])}" fill="{C["wedge"]}" stroke="{C["wedge_e"]}" stroke-width="1.2"/>')
# backstop
a(f'<polygon points="{pts([(40, 120), (X0 - 30, 120), (X0, 140), (X0 + 20, ydec(X0 + 20)), (X0 - 40, 372), (40, 372)])}" fill="{C["back"]}" stroke="{C["back_e"]}" stroke-width="1.5"/>')
a(f'<text x="140" y="215" text-anchor="middle" font-size="17" font-weight="700" fill="white">BACKSTOP</text>')
a(f'<text x="140" y="238" text-anchor="middle" font-size="13" fill="white">stronger rock: island arc,</text>')
a(f'<text x="140" y="256" text-anchor="middle" font-size="13" fill="white">crystalline basement or</text>')
a(f'<text x="140" y="274" text-anchor="middle" font-size="13" fill="white">older, accreted wedge</text>')
a(f'<line x1="44" y1="300" x2="150" y2="300" stroke="{C["push"]}" stroke-width="4" marker-end="url(#ap)"/>')
a(f'<text x="98" y="325" text-anchor="middle" font-size="13" fill="white">convergence</text>')

# thrusts: forethrusts step up toward the foreland, one backthrust makes the frontal pop-up
def thrust(xb, run, back=False):
    xt = xb - run if back else xb + run
    a(f'<line x1="{xb}" y1="{ydec(xb):.1f}" x2="{xt}" y2="{ysurf(xt):.1f}" stroke="{C["fault"]}" stroke-width="2.4"/>')
    return xt
for xb in (300, 390, 480, 570):
    thrust(xb, 75)
thrust(680, 80)                       # frontal forethrust, reaches the surface at the front
thrust(680, 70, back=True)            # its conjugate backthrust: a pop-up between them

# labels
def label(x, y, t, anchor='middle', size=14, col=None, bold=False):
    a(f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-size="{size}"{" font-weight=\"600\"" if bold else ""} fill="{col or C["txt"]}">{t}</text>')
a('<rect x="372" y="236" width="196" height="46" rx="6" fill="white" fill-opacity="0.85"/>')
label(470, 256, 'WEDGE', size=17, bold=True)
label(470, 275, 'deformed sedimentary rock', size=13)
a('<rect x="768" y="271" width="156" height="18" rx="4" fill="white" fill-opacity="0.8"/>')
label(846, 284, 'undeformed foreland strata', size=12)
label(560, 395, 'DECOLLEMENT: weak layer (shale with high pore pressure, or salt)', size=14, col=C['dec'], bold=True)
a(f'<line x1="560" y1="381" x2="560" y2="{ydec(560) + DT + 1:.1f}" stroke="{C["dec"]}" stroke-width="1.2" marker-end="url(#ag)"/>')
label(820, 362, 'basement', size=13, col=C['grey'])
label(520, 150, 'forethrusts', size=13, col=C['fault'], bold=True)
a(f'<line x1="520" y1="156" x2="537" y2="{ysurf(537) - 4:.1f}" stroke="{C["fault"]}" stroke-width="1" marker-end="url(#ag)"/>')
label(612, 168, 'backthrust', size=13, col=C['fault'], bold=True)
a(f'<line x1="612" y1="174" x2="{612 + 8}" y2="{ysurf(620) - 4:.1f}" stroke="{C["fault"]}" stroke-width="1" marker-end="url(#ag)"/>')
label(682, 278, 'pop-up', size=12, col=C['fault'], bold=True)
label(XF + 10, 228, 'deformation front', anchor='start', size=13)
a(f'<line x1="{XF + 40}" y1="234" x2="{XF + 3}" y2="258" stroke="{C["grey"]}" stroke-width="1" marker-end="url(#ag)"/>')
label(X0 + 5, 110, 'hinterland', anchor='start', size=13, col=C['grey'])
label(X1, 245, 'foreland', anchor='end', size=13, col=C['grey'])
# taper angles
a(f'<line x1="{X0 + 10}" y1="{ysurf(X0 + 10):.1f}" x2="{X0 + 150}" y2="{ysurf(X0 + 10):.1f}" stroke="{C["grey"]}" stroke-width="1" stroke-dasharray="4 3"/>')
label(X0 + 128, ysurf(X0 + 10) + 16, 'α', size=17, col=C['txt'], bold=True)
a(f'<line x1="{XF - 140}" y1="{ydec(XF - 140):.1f}" x2="{XF - 140 + 120}" y2="{ydec(XF - 140):.1f}" stroke="{C["grey"]}" stroke-width="1" stroke-dasharray="4 3"/>')
label(XF - 32, ydec(XF - 140) - 6, 'β', size=17, col=C['txt'], bold=True)
label(W / 2, 425, 'Critical taper α + β: set by the strength of the wedge against the friction on the decollement',
      size=14, col=C['grey'])

# ---------------------------------------------------------------- bottom: strong vs salt base
a(f'<line x1="40" y1="445" x2="{W - 40}" y2="445" stroke="{C["grey"]}" stroke-width="0.8"/>')
def sketch(x0, width, height, title, sub, salt):
    yb = 640
    a(f'<text x="{x0 + width / 2 + 30}" y="474" text-anchor="middle" font-size="15" font-weight="700" fill="{C["txt"]}">{title}</text>')
    a(f'<text x="{x0 + width / 2 + 30}" y="493" text-anchor="middle" font-size="13" fill="{C["grey"]}">{sub}</text>')
    a(f'<rect x="{x0 - 30}" y="{yb - height - 30}" width="40" height="{height + 30}" fill="{C["back"]}" stroke="{C["back_e"]}"/>')
    top = lambda x: yb - 40 - height * max(0.0, 1 - (x - x0 - 10) / width) if x <= x0 + 10 + width else yb - 40
    xr = x0 + width + 70
    xx = [x0 + 10 + i * 2 for i in range(int((xr - x0 - 10) / 2) + 1)]
    a(f'<polygon points="{pts([(x, top(x)) for x in xx] + [(xr, yb), (x0 + 10, yb)])}" fill="{C["wedge"]}" stroke="{C["wedge_e"]}"/>')
    a(f'<rect x="{x0 + 10}" y="{yb}" width="{xr - x0 - 10}" height="7" fill="{C["salt"] if salt else C["dec"]}"/>')
    if salt:
        for k in range(5):                       # symmetric folds above salt, both vergences
            path = []
            for x in xx:
                yk = yb - 6 - k * 7
                if x <= x0 + 10 + width:
                    yk -= 9 * math.sin((x - x0 - 10) / 26.0 * math.pi) ** 2
                path.append((x, max(yk, top(x) + 2)))
            a(f'<polyline points="{pts(path)}" fill="none" stroke="{C["wedge_e"]}" stroke-width="1.1"/>')
        for xc in [x0 + 10 + 26 * (j + 0.5) for j in range(int(width / 26))]:
            a(f'<path d="M{xc - 5},{yb} Q{xc},{yb - 24} {xc + 5},{yb} Z" fill="{C["salt"]}" stroke="{C["salt_e"]}" stroke-width="0.8"/>')
    else:
        for k in range(5):                       # forward-verging imbricate thrusts
            xb = x0 + 25 + k * width / 5.5
            a(f'<line x1="{xb:.1f}" y1="{yb}" x2="{xb + 32:.1f}" y2="{top(xb + 32) + 1:.1f}" stroke="{C["fault"]}" stroke-width="2"/>')
sketch(80, 190, 95, 'Strong decollement: narrow, steep', 'e.g. Taiwan, α + β ≈ 9°; mostly forethrusts', False)
sketch(560, 370, 26, 'Salt decollement: wide, low', 'e.g. Zagros (Fars), α + β ≈ 1°; folds of both vergences', True)

a('</svg>')
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'wedge-anatomy.svg')
with open(out, 'w') as f:
    f.write('\n'.join(s) + '\n')
print('wrote', out)
