"""Generate ../core-complex-rolling-hinge.svg: animated setup and rolling hinge for core-complex.cfg.

Four keyframes in km are morphed by SMIL <animate> on path "d" attributes, so every
keyframe path must keep the same point count. Run: python3 make_core_complex_rolling_hinge.py
"""
import os

X = lambda x: 110 + 7.5 * x      # km -> px, 7.5 px/km
Y = lambda z: 200 - 16 * z       # km -> px, 16 px/km (2x vertical exaggeration); z < 0 is depth


def P(pt):
    return f"{X(pt[0]):.1f} {Y(pt[1]):.1f}"


# xl/xr: wall positions; B bottom of fault; H hinge; S surface trace; Bp basin; C crest; F flank;
# T top of the drawn fault; Cf exhumed end of the fault on the footwall
K = [
    dict(xl=0.0, xr=100.0, B=(47.1, -10), H=(50.0, -5.0), S=(52.9, 0.0), Bp=(47.0, 0.0), C=(56.0, 0.0), F=(70, 0.0), T=(50.0, -5.0), Cf=(50.0, -5.0)),
    dict(xl=-0.8, xr=100.8, B=(46.3, -10), H=(49.2, -5.0), S=(52.1, 0.2), Bp=(46.0, -0.5), C=(55.5, 0.7), F=(68, 0.2), T=(52.1, 0.2), Cf=(53.0, 0.4)),
    dict(xl=-1.9, xr=101.9, B=(44.0, -10), H=(48.0, -5.2), S=(52.0, 0.4), Bp=(46.5, -1.1), C=(56.0, 1.5), F=(68, 0.5), T=(52.0, 0.4), Cf=(55.5, 1.4)),
    dict(xl=-3.2, xr=103.2, B=(41.5, -10), H=(46.5, -5.6), S=(52.0, 0.3), Bp=(47.0, -1.5), C=(56.5, 2.1), F=(69, 0.6), T=(52.0, 0.3), Cf=(56.0, 2.0)),
]
K = [K[0]] + K + [K[-1]]  # hold the first and last frames
KT = "0;0.12;0.32;0.58;0.86;1"
DUR = "14s"


def hw(k):
    return f"M{P((k['xl'], 0))} L{P(k['Bp'])} L{P(k['S'])} L{P(k['H'])} L{P(k['B'])} L{P((k['xl'], -10))} Z"


def fw(k):
    return f"M{P(k['S'])} L{P(k['C'])} L{P(k['F'])} L{P((k['xr'], 0))} L{P((k['xr'], -10))} L{P(k['B'])} L{P(k['H'])} Z"


def fault(k):
    return f"M{P(k['B'])} L{P(k['H'])} L{P(k['T'])} L{P(k['Cf'])}"


def anim(attr, fn):
    vals = ";".join(fn(k) for k in K)
    return f'<animate attributeName="{attr}" values="{vals}" keyTimes="{KT}" dur="{DUR}" repeatCount="indefinite"/>'


def opac(i):  # visible during segment i (6 keyTimes, 5 segments)
    v = ["0"] * 6
    v[i] = "1"
    if i == 4:
        v[5] = "1"
    return ";".join(v)


captions = [
    "t = 0: a pre-softened seed sits in the lower half of the layer",
    "the fault cuts to the surface; the hanging wall drops, the footwall rises",
    "the footwall keeps rising and the fault starts to rotate",
    "rolling hinge: the fault flattens as the footwall is exhumed",
    "rolling hinge: the fault flattens as the footwall is exhumed",
]
times = ["0 kyr", "0 → 25 kyr", "25 → 60 kyr", "60 → 100 kyr", "100 kyr"]

s = []
a = s.append
a('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 960 460" width="960" height="460" role="img" aria-label="Core-complex setup and rolling hinge: a 100 by 10 km brittle layer is pulled apart at both walls; a pre-softened seed fault dipping 60 degrees cuts to the surface, the hanging wall drops into a basin, the footwall rises and the fault rotates to a gentle dip as it is exhumed">')
a('<style>text{font-family:system-ui,-apple-system,"Segoe UI",Roboto,Arial,sans-serif}</style>')
a('<defs><marker id="ab" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto"><path d="M0 0L10 5L0 10z" fill="#6B7280"/></marker></defs>')
a('<rect width="960" height="460" rx="16" fill="#F7F6F2"/>')
a('<text x="480" y="36" text-anchor="middle" font-size="22" font-weight="700" fill="#374151">core-complex.cfg: setup and rolling hinge</text>')
for i in range(5):
    a(f'<text x="80" y="70" font-size="16" fill="#374151" opacity="0">{captions[i]}<animate attributeName="opacity" values="{opac(i)}" keyTimes="{KT}" calcMode="discrete" dur="{DUR}" repeatCount="indefinite"/></text>')
for i in range(5):
    a(f'<text x="880" y="70" text-anchor="end" font-size="16" font-weight="700" fill="#374151" opacity="0">t = {times[i]}<animate attributeName="opacity" values="{opac(i)}" keyTimes="{KT}" calcMode="discrete" dur="{DUR}" repeatCount="indefinite"/></text>')
a(f'<path fill="#CFE0F0" stroke="#2F6FB0" stroke-width="2" stroke-linejoin="round" d="{hw(K[0])}">{anim("d", hw)}</path>')
a(f'<path fill="#CFE0F0" stroke="#2F6FB0" stroke-width="2" stroke-linejoin="round" d="{fw(K[0])}">{anim("d", fw)}</path>')
a(f'<path fill="none" stroke="#E8A33D" stroke-opacity="0.45" stroke-linecap="round" stroke-linejoin="round" stroke-width="0" d="{fault(K[0])}">{anim("d", fault)}<animate attributeName="stroke-width" values="0;0;6;11;15;15" keyTimes="{KT}" dur="{DUR}" repeatCount="indefinite"/></path>')
a(f'<path fill="none" stroke="#B5651D" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round" d="{fault(K[0])}">{anim("d", fault)}</path>')
a(f'<text x="{X(50)+14:.0f}" y="{Y(-7.5)+5:.0f}" font-size="14" fill="#B5651D" opacity="0">weak-zone seed, 60° dip<animate attributeName="opacity" values="1;0;0;0;0;0" keyTimes="{KT}" calcMode="discrete" dur="{DUR}" repeatCount="indefinite"/></text>')
a(f'<text x="{X(22):.0f}" y="{Y(-5)+5:.0f}" text-anchor="middle" font-size="16" fill="#2F6FB0">hanging wall</text>')
a(f'<text x="{X(80):.0f}" y="{Y(-5)+5:.0f}" text-anchor="middle" font-size="16" fill="#2F6FB0">footwall</text>')
a(f'<text x="{X(14):.0f}" y="{Y(0)-10:.0f}" font-size="14" fill="#6B7280">free surface, hillslope diffusion</text>')
a(f'<text x="480" y="{Y(-10)+52:.0f}" text-anchor="middle" font-size="14" fill="#6B7280">Winkler foundation: lithostatic support, free to move vertically; remeshing restores it to 10 km depth</text>')
a(f'<path d="M62 {Y(-2.5):.0f} L14 {Y(-2.5):.0f}" stroke="#6B7280" stroke-width="3" marker-end="url(#ab)" fill="none"/>')
a(f'<path d="M898 {Y(-2.5):.0f} L946 {Y(-2.5):.0f}" stroke="#6B7280" stroke-width="3" marker-end="url(#ab)" fill="none"/>')
a(f'<text x="38" y="{Y(-2.5)+26:.0f}" text-anchor="middle" font-size="13" fill="#374151">3.15 cm/yr</text>')
a(f'<text x="922" y="{Y(-2.5)+26:.0f}" text-anchor="middle" font-size="13" fill="#374151">3.15 cm/yr</text>')
a(f'<text x="38" y="{Y(-2.5)+44:.0f}" text-anchor="middle" font-size="12" fill="#6B7280">vbc_val_x0</text>')
a(f'<text x="922" y="{Y(-2.5)+44:.0f}" text-anchor="middle" font-size="12" fill="#6B7280">vbc_val_x1</text>')
for xk, lab in [(0, "0"), (50, "50 km"), (100, "100 km")]:
    a(f'<path d="M{X(xk):.0f} {Y(-10)+4:.0f} L{X(xk):.0f} {Y(-10)+12:.0f}" stroke="#6B7280" stroke-width="2"/>')
    a(f'<text x="{X(xk):.0f}" y="{Y(-10)+28:.0f}" text-anchor="middle" font-size="13" fill="#374151">{lab}</text>')
a('<text x="480" y="446" text-anchor="middle" font-size="13" fill="#6B7280">10 km brittle layer, vertical exaggeration 2×, elasto-plastic with cohesion softening (see the previous figure)</text>')
a('</svg>')
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'core-complex-rolling-hinge.svg')
open(out, "w").write("\n".join(s) + "\n")
print(out)
