# docs/tutorial/img/tectonics/subduction-geometry.svg -- initial geometry of poly-subduction.poly
# with region materials colored, node numbers, and the 3 km virtual-topology grid over the slab.
# Full domain 400 x 160 km shown at true aspect in an inset; main panel zooms on the trench.
import os
nodes = {0:(0,0),1:(0,-2),2:(0,-9),3:(0,-160),4:(400,-160),5:(400,-9),6:(400,-2),7:(400,0),
 8:(125,-9),9:(139,-9),10:(178.69,-40),11:(182.19,-33.938),12:(104.996,-9),13:(158.996,-9),
 14:(182.350,-53.660),15:(195.850,-30.278)}
C = {'crust':'#2F6FB0','crust_f':'#CFE0F0','sed':'#E8C547','sed_f':'#F6E7B0','mantle':'#7A9A7E','mantle_f':'#E3EDE4',
     'halo_f':'#CFE0D2','grid':'#B5651D','txt':'#374151','grey':'#6B7280'}
# main panel: x 90..230 km, z 0..-70 km ; px scale 5 px/km both ways
X0,Z0 = 90,0
def X(x): return 60 + (x-X0)*5.6
def Y(z): return 110 - z*5.6
def P(i): x,z=nodes[i]; return f"{X(x):.1f},{Y(z):.1f}"
def pts(ids): return " ".join(P(i) for i in ids)
s=[]
a=s.append
a('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 960 560" width="960" height="560" role="img" aria-label="Initial geometry of the subduction example: a 2 km sediment layer over 7 km oceanic crust across the domain, a 7 km slab of oceanic crust dipping 30 degrees from the trench at 125-139 km to 40 km depth, a 10 km halo of refined mantle around it, and the 3 km virtual-topology grid over the slab">')
a('<style>text{font-family:system-ui,-apple-system,"Segoe UI",Roboto,Arial,sans-serif}</style>')
a('<rect width="960" height="560" rx="16" fill="#F7F6F2"/>')
a('<text x="480" y="36" text-anchor="middle" font-size="22" font-weight="700" fill="#374151">poly-subduction.poly: initial geometry around the trench</text>')
# clip to main panel
a('<defs><clipPath id="main"><rect x="60" y="110" width="784" height="392"/></clipPath></defs>')
a('<g clip-path="url(#main)">')
# coarse mantle background (region 4) over whole panel
a(f'<rect x="60" y="{Y(-9):.1f}" width="784" height="400" fill="{C["mantle_f"]}"/>')
# halo (region 3): polygon 12-8-10-14 (below) and 9-13-15-11 (above) -> draw as one polygon 12,8,9,13,15,11,10,14
a(f'<polygon points="{pts([12,8,9,13,15,11,10,14])}" fill="{C["halo_f"]}" stroke="{C["mantle"]}" stroke-width="1.5" stroke-dasharray="5 4"/>')
# slab (region 2): 8,9,11,10
a(f'<polygon points="{pts([8,9,11,10])}" fill="{C["crust_f"]}" stroke="{C["crust"]}" stroke-width="2"/>')
# crust layer (region 1): z -2..-9 across panel
a(f'<rect x="60" y="{Y(-2):.1f}" width="784" height="{(Y(-9)-Y(-2)):.1f}" fill="{C["crust_f"]}" stroke="{C["crust"]}" stroke-width="1.5"/>')
# sediment (region 0): z 0..-2
a(f'<rect x="60" y="{Y(0):.1f}" width="784" height="{(Y(-2)-Y(0)):.1f}" fill="{C["sed_f"]}" stroke="{C["sed"]}" stroke-width="1.5"/>')
# virtual-topology grid: 3 km cells over x 120..200, z -9..-60 (drawn light, over halo+slab)
gx0,gx1,gz0,gz1 = 120,201,-9,-60
x=gx0
while x<=gx1:
    a(f'<line x1="{X(x):.1f}" y1="{Y(gz0):.1f}" x2="{X(x):.1f}" y2="{Y(gz1):.1f}" stroke="{C["grid"]}" stroke-opacity="0.35" stroke-width="1"/>'); x+=3
z=gz0
while z>=gz1:
    a(f'<line x1="{X(gx0):.1f}" y1="{Y(z):.1f}" x2="{X(gx1):.1f}" y2="{Y(z):.1f}" stroke="{C["grid"]}" stroke-opacity="0.35" stroke-width="1"/>'); z-=3
# highlight the serpentinizing cells: one cell row above the slab top (approximate band along 9->11)
import math
dip=math.radians(30)
for t in [i/14 for i in range(15)]:
    sx = 139 + (182.19-139)*t; sz = -9 + (-33.938+9)*t
    # cell containing point 1.5 km above slab top (normal direction)
    nx, nz = -math.sin(dip), math.cos(dip)
    cx = sx + 1.5*nx; cz = sz + 1.5*nz
    gx = gx0 + math.floor((cx-gx0)/3)*3; gz = gz0 - math.floor((gz0-cz)/3)*3
    a(f'<rect x="{X(gx):.1f}" y="{Y(gz):.1f}" width="{3*5.6:.1f}" height="{3*5.6:.1f}" fill="#9b59d0" fill-opacity="0.35"/>')
a('</g>')
# node numbers
for i,(x,z) in nodes.items():
    if X0<=x<=230 and z>=-70:
        a(f'<circle cx="{X(x):.1f}" cy="{Y(z):.1f}" r="4" fill="{C["txt"]}"/>')
        dx,dy = (8,-6)
        if i in (8,12): dx,dy=(-6,18)
        if i in (9,13): dx,dy=(6,18)
        if i==10: dx,dy=(-22,14)
        if i==14: dx,dy=(-26,16)
        a(f'<text x="{X(x)+dx:.1f}" y="{Y(z)+dy:.1f}" font-size="13" fill="{C["txt"]}">{i}</text>')
# labels
a(f'<text x="{X(100):.0f}" y="{Y(-1)+4:.0f}" font-size="13" fill="#8a6d1d">region 0: sediment (3), 0 to −2 km</text>')
a(f'<text x="{X(100):.0f}" y="{Y(-5.5)+4:.0f}" font-size="13" fill="{C["crust"]}">region 1: oceanic crust (0), −2 to −9 km</text>')
a(f'<text x="{X(150):.0f}" y="{Y(-24):.0f}" font-size="13" font-weight="700" fill="{C["crust"]}" transform="rotate(30 {X(150):.0f} {Y(-24):.0f})">region 2: slab, 7 km, 30° dip</text>')
a(f'<text x="{X(120):.0f}" y="{Y(-42):.0f}" font-size="13" fill="{C["mantle"]}">region 3: refined mantle halo, 10 km</text>')
a(f'<text x="{X(92):.0f}" y="{Y(-64):.0f}" font-size="13" fill="{C["mantle"]}">region 4: mantle (2), coarse</text>')
a(f'<text x="{X(163):.0f}" y="{Y(-14):.0f}" font-size="13" fill="#7a3fa8">cells above the slab top turn mantle into serpentinite</text>')
a(f'<text x="{X(163):.0f}" y="{Y(-17):.0f}" font-size="12" fill="{C["grid"]}">virtual-topology grid: 3 km cells (resolution × vt_size)</text>')
a(f'<text x="{X(132):.0f}" y="{Y(2.5):.0f}" text-anchor="middle" font-size="13" fill="{C["txt"]}">trench: slab enters the mantle at x = 125–139 km</text>')
# axes ticks
for xk in (100,125,150,175,200,225):
    a(f'<line x1="{X(xk):.1f}" y1="502" x2="{X(xk):.1f}" y2="510" stroke="{C["grey"]}" stroke-width="2"/>')
    a(f'<text x="{X(xk):.1f}" y="526" text-anchor="middle" font-size="12" fill="{C["txt"]}">{xk} km</text>')
for zk in (0,-20,-40,-60):
    a(f'<line x1="52" y1="{Y(zk):.1f}" x2="60" y2="{Y(zk):.1f}" stroke="{C["grey"]}" stroke-width="2"/>')
    a(f'<text x="46" y="{Y(zk)+4:.1f}" text-anchor="end" font-size="12" fill="{C["txt"]}">{zk}</text>')
a(f'<text x="24" y="300" text-anchor="middle" font-size="12" fill="{C["txt"]}" transform="rotate(-90 24 300)">z (km)</text>')
a(f'<rect x="60" y="110" width="784" height="392" fill="none" stroke="{C["grey"]}" stroke-width="1.5"/>')
# inset: full domain 400 x 160 at true aspect (scale 0.55 px/km): 220 x 88 px
ix,iy,sc = 612,396,0.55
def IX(x): return ix + x*sc
def IY(z): return iy - z*sc
a(f'<rect x="{ix}" y="{iy}" width="{400*sc}" height="{160*sc}" fill="{C["mantle_f"]}" stroke="{C["grey"]}" stroke-width="1"/>')
a(f'<rect x="{ix}" y="{iy}" width="{400*sc}" height="{9*sc}" fill="{C["crust_f"]}"/>')
a(f'<polygon points="{IX(125):.1f},{IY(-9):.1f} {IX(139):.1f},{IY(-9):.1f} {IX(182.19):.1f},{IY(-33.9):.1f} {IX(178.69):.1f},{IY(-40):.1f}" fill="{C["crust"]}"/>')
a(f'<rect x="{IX(90):.1f}" y="{IY(0):.1f}" width="{140*sc:.1f}" height="{70*sc:.1f}" fill="none" stroke="{C["grid"]}" stroke-width="1.5"/>')
a(f'<text x="{ix+400*sc/2:.0f}" y="{iy-8:.0f}" text-anchor="middle" font-size="12" fill="{C["txt"]}">full domain 400 × 160 km; box = main panel</text>')
a(f'<text x="{ix+400*sc/2:.0f}" y="{iy+160*sc+14:.0f}" text-anchor="middle" font-size="11" fill="{C["grey"]}">left plate → 3.15 cm/yr, right wall fixed</text>')
a('</svg>')
out=__import__('os').path.join(__import__('os').path.dirname(os.path.abspath(__file__)), '..', 'subduction-geometry.svg')
open(out,"w").write("\n".join(s)+"\n"); print(out, len("\n".join(s)))
