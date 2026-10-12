"""Kitchen layout sheet for commercial kitchen vendors: plan (1:25 at A3), hot-line elevation, exhaust run and equipment schedule.
Coordinates are the 3D model's: x runs from the right wall (X0 = -2.45) to the left wall (X1 = 2.45) as you walk in; z runs from the shopfront
to the back wall (D = 8.8). The kitchen is z 6.4 to 8.8. Usage: python3 tools/kitchen_plan.py build  ->  build/kitchen-plan.svg
"""
import sys, os
X0, X1, D, T, KZ, KC, H = -2.45, 2.45, 8.8, 0.2, 6.3, 2.7, 4.5
XS = X0 - T
W, HH = 2480, 1754                    # A3 landscape proportions
out = []
INK, MUT, RED, BLU, GAS, GRN, BRN = '#2a2420', '#6a5d4e', '#b23a1e', '#2f6f9f', '#b8862a', '#3f6a3a', '#7a3f1d'

# ---------------- plan mapping (1:25 on A3 when printed: 190 px per metre)
S = 190; XL, ZT = X1 + T + 0.2, D + T + 0.95; POX, POY = 60, 150
def P(x, z): return (POX + (XL - x) * S, POY + (ZT - z) * S)
def rect(xa, xb, za, zb, fill='none', stroke=INK, sw=1.4, dash=None):
    (a, b), (c, d) = P(max(xa, xb), max(za, zb)), P(min(xa, xb), min(za, zb))
    out.append(f'<rect x="{a:.1f}" y="{b:.1f}" width="{c-a:.1f}" height="{d-b:.1f}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"' + (f' stroke-dasharray="{dash}"' if dash else '') + '/>')
def line(xa, za, xb, zb, stroke=INK, sw=1.4, dash=None):
    a, b = P(xa, za); c, d = P(xb, zb)
    out.append(f'<line x1="{a:.1f}" y1="{b:.1f}" x2="{c:.1f}" y2="{d:.1f}" stroke="{stroke}" stroke-width="{sw}"' + (f' stroke-dasharray="{dash}"' if dash else '') + '/>')
def circ(x, z, r, fill='none', stroke=INK, sw=1.4, dash=None):
    a, b = P(x, z); out.append(f'<circle cx="{a:.1f}" cy="{b:.1f}" r="{r*S:.1f}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"' + (f' stroke-dasharray="{dash}"' if dash else '') + '/>')
def text(x, z, t, size=13, fill=INK, anchor='middle', weight=500, rot=0):
    a, b = P(x, z); tr = f' transform="rotate({rot} {a:.1f} {b:.1f})"' if rot else ''
    out.append(f'<text x="{a:.1f}" y="{b+size*0.35:.1f}" font-size="{size}" fill="{fill}" text-anchor="{anchor}" font-weight="{weight}"{tr}>{t}</text>')
def tagc(x, z, n, col=INK):
    a, b = P(x, z); out.append(f'<g><circle cx="{a:.1f}" cy="{b:.1f}" r="13" fill="#fff" stroke="{col}" stroke-width="1.6"/><text x="{a:.1f}" y="{b+4.6:.1f}" font-size="12.5" font-weight="700" fill="{col}" text-anchor="middle">{n}</text></g>')
def arc(cx, cz, r, x0, z0, x1, z1, sweep, stroke=INK):
    a, b = P(x0, z0); c, d = P(x1, z1)
    out.append(f'<path d="M{a:.1f} {b:.1f} A{r*S:.1f} {r*S:.1f} 0 0 {sweep} {c:.1f} {d:.1f}" fill="none" stroke="{stroke}" stroke-width="1" stroke-dasharray="4 3"/>')
    line(cx, cz, x1, z1, stroke, 1.6)
def hdim(xa, xb, z, t, col=RED, size=12.5, tick=6):
    a, b = P(xa, z); c, _ = P(xb, z)
    out.append(f'<g stroke="{col}" stroke-width="1.1"><line x1="{a:.1f}" y1="{b:.1f}" x2="{c:.1f}" y2="{b:.1f}"/><line x1="{a:.1f}" y1="{b-tick}" x2="{a:.1f}" y2="{b+tick}"/><line x1="{c:.1f}" y1="{b-tick}" x2="{c:.1f}" y2="{b+tick}"/></g>')
    out.append(f'<text x="{(a+c)/2:.1f}" y="{b-5:.1f}" font-size="{size}" fill="{col}" text-anchor="middle" font-weight="600">{t}</text>')
def vdim(x, za, zb, t, col=RED, size=12.5, tick=6):
    a, b = P(x, za); _, d = P(x, zb)
    out.append(f'<g stroke="{col}" stroke-width="1.1"><line x1="{a:.1f}" y1="{b:.1f}" x2="{a:.1f}" y2="{d:.1f}"/><line x1="{a-tick}" y1="{b:.1f}" x2="{a+tick}" y2="{b:.1f}"/><line x1="{a-tick}" y1="{d:.1f}" x2="{a+tick}" y2="{d:.1f}"/></g>')
    out.append(f'<text x="{a-6:.1f}" y="{(b+d)/2:.1f}" font-size="{size}" fill="{col}" text-anchor="middle" font-weight="600" transform="rotate(-90 {a-6:.1f} {(b+d)/2:.1f})">{t}</text>')

WALL = '#4a4038'; STEEL = '#c3c8cc'; HOT = '#9aa0a5'
# outside: right-side strip and back (parking)
rect(XS - 0.5, XS, 6.0, D + T, '#ece6db', 'none'); rect(XL, XS - 0.8, D + T, ZT, '#e8e3da', 'none')
text(XS - 0.25, 6.15, 'side strip', 10, MUT, rot=-90); text(-0.2, D + T + 0.8, 'OUTSIDE · BACK (parking: nothing stored here)', 12, MUT, weight=600)
# floor, walls, dining side of the front wall
rect(X0, X1, KZ + 0.1, D, '#eef0ec', 'none'); rect(X0, X1, 5.9, KZ, '#fbf7ef', 'none'); text(1.7, 6.05, 'DINING ROOM SIDE', 11, MUT, weight=600)
rect(XS, X0, 5.9, D + T, WALL, WALL); rect(X1, X1 + T, 5.9, D + T, WALL, WALL)
rect(X0, 0.95, D, D + T, WALL, WALL); rect(1.75, X1, D, D + T, WALL, WALL)
rect(X0, -0.6, KZ, KZ + 0.1, '#d8c6ac', '#a8987c', 1); rect(0.05, 0.1, KZ, KZ + 0.1, '#d8c6ac', '#a8987c', 1); rect(0.8, X1, KZ, KZ + 0.1, '#d8c6ac', '#a8987c', 1)
rect(-0.6, 0.05, KZ, KZ + 0.1, '#cfe3ea', '#7a9aaa', 1)
rect(X0, X0 + 0.23, 6.65, 6.95, WALL, WALL); text(X0 + 0.115, 6.8, 'P2', 10, '#fff', weight=700)
# HOT LINE (back wall) under the hood
for xa, xb, n, t in ((X0, -1.25, 1, 'wok range'), (-1.2, -0.6, 2, 'steamer'), (-0.55, 0.05, 3, 'fryer'), (0.1, 0.7, 4, 'stock range')):
    rect(xa, xb, 8.1, D, HOT); text((xa + xb) / 2, 8.6, t, 13, '#fff', weight=700); tagc((xa + xb) / 2, 8.3, n)
for x in (-2.1, -1.6): circ(x, 8.45, 0.2, 'none', '#fff', 1.2)
for x in (-1.05, -0.75): circ(x, 8.45, 0.13, 'none', '#fff', 1.2)
for x in (0.25, 0.55): circ(x, 8.45, 0.11, 'none', '#fff', 1.2)
rect(X0 + 0.02, 0.8, 7.85, D - 0.02, 'none', RED, 2, '10 5'); text(-0.8, 7.95, 'canopy hood over the whole line · bottom at 2.05 m', 11.5, RED, weight=600); tagc(0.62, 7.95, 5, RED)
rect(-1.6, -1.1, 8.4, D, '#f3e0dc', RED, 1.2, '5 3')
rect(-2.4, 0.75, 7.92, 8.0, '#b9c0c5', '#6d7276', 0.8); tagc(-2.27, 7.82, 23, '#6d7276')
# right wall: sauce shelf, seasoning rail, extinguishers, first aid, fire blanket
rect(X0, X0 + 0.3, 7.15, 8.05, 'none', MUT, 1, '4 3'); rect(X0, X0 + 0.22, 7.62, 8.06, '#e6ecef', BLU, 1.2)
tagc(X0 + 0.4, 7.9, 14, BLU); tagc(X0 + 0.4, 7.35, 15, MUT)
for z in (7.25, 7.5): circ(X0 + 0.1, z, 0.075, '#c8231b', '#c8231b', 1)
rect(-2.1, -1.86, KZ + 0.1, KZ + 0.16, '#d9261c', '#d9261c', 1)
# FRONT WALL inside: non-veg bench, veg/dumpling bench, pass
rect(-2.2, -1.4, KZ + 0.115, 7.05, STEEL); text(-1.8, 6.95, 'non-veg prep', 12, weight=700); tagc(-1.55, 6.62, 6)
rect(-2.18, -1.42, 6.42, 6.68, '#dff0f6', BLU, 1.2, '4 2'); tagc(-2.05, 6.8, 16, BLU)
rect(-2.12, -1.84, 6.5, 6.92, 'none', '#8f6a4a', 1, '2 2'); tagc(-1.97, 6.55, 18, '#8f6a4a')
rect(-1.4, -0.6, KZ + 0.115, 7.05, STEEL); text(-1.0, 6.95, 'veg / dumpling', 12, weight=700); text(-1.0, 6.78, '+ u/c freezer', 10.5, MUT); tagc(-1.25, 6.55, 7)
circ(-0.78, 6.62, 0.15, '#e9e9e9', '#6d7276', 1); tagc(-0.78, 6.62, 19, '#6d7276')
rect(-0.6, 0.05, KZ + 0.115, 7.05, STEEL); text(-0.28, 6.95, 'pass', 12, weight=700); tagc(-0.28, 6.62, 8)
rect(-0.6, 0.05, 6.93, 7.05, '#e6ecef', BLU, 1); tagc(-0.03, 6.62, 17, BLU)
# door, hand-wash, insect killer, apron hooks
arc(0.8, KZ + 0.1, 0.7, 0.1, KZ + 0.1, 0.8, KZ + 0.8, 1); tagc(0.6, 6.95, 21, MUT)
rect(0.85, 1.18, KZ + 0.115, 6.8, STEEL); tagc(1.015, 6.62, 9); tagc(0.45, 6.5, 22, MUT)
# LEFT WALL: reach-in, dishwasher, sink, shelves over; fridge door swings
rect(1.7, X1, 6.45, 7.4, STEEL); text(2.08, 6.92, '2-door reach-in', 12, weight=700, rot=90); tagc(1.95, 6.62, 10)
for hz, sg in ((6.45, 1), (7.4, -1)):
    a, b = P(1.7, hz); c, d = P(1.23, hz); r = 0.47 * S
    out.append(f'<path d="M{c:.1f} {d:.1f} A{r:.1f} {r:.1f} 0 0 {0 if sg>0 else 1} {a:.1f} {b-sg*r:.1f}" fill="none" stroke="{BLU}" stroke-width="1" stroke-dasharray="4 3"/>')
rect(1.8, X1, 7.4, 8.0, STEEL); text(2.12, 7.7, 'u/c dishwasher', 11.5, weight=700, rot=90); tagc(1.95, 7.5, 11)
rect(1.8, X1, 8.0, D, STEEL); text(2.12, 8.4, '2-bowl sink', 11.5, weight=700, rot=90); tagc(1.95, 8.1, 12)
rect(2.1, X1, 7.4, D, 'none', MUT, 1, '3 3'); tagc(2.32, 7.82, 13, MUT)
# bins, hatch, make-up grille, heat detector, rear exit, suppression pull
circ(-2.32, 6.52, 0.1, '#cfe0bf', GRN, 1.2); circ(0.83, 8.62, 0.1, '#d6e2ef', BLU, 1.2); tagc(0.83, 8.3, 20, MUT)
rect(0.35, 0.95, 7.15, 7.95, 'none', BLU, 1.4, '6 3'); text(0.65, 7.55, 'hatch to deck', 11, BLU, weight=600); tagc(0.65, 7.35, 27, BLU)
rect(-0.6, -0.05, 7.42, 7.8, 'none', GRN, 1.3, '3 3'); text(-0.325, 7.6, 'make-up air', 10.5, GRN, weight=600); tagc(-0.15, 7.32, 24, GRN)
circ(-0.6, 7.6, 0.05, '#fff', RED, 1.2)
arc(1.75, D + T, 0.8, 0.95, D + T, 1.75, D + T + 0.8, 0, INK); text(1.35, D + T + 0.12, 'rear exit', 11, MUT)
rect(0.76, 0.92, D - 0.06, D, '#c8231b', '#c8231b', 1); tagc(0.84, 8.95, 26, RED)
tagc(-2.05, 7.38, 25, RED)
# KITCHEN label
text(1.35, 7.62, 'KITCHEN', 14, INK, weight=700)
# GAS: LPG cage on the side strip, copper line along the outside wall at 1.3 m, in behind the wok range
rect(XS - 0.4, XS - 0.05, 6.0, 6.25, '#f3d6cf', RED, 1, '3 2'); text(XS - 0.22, 6.12, 'LPG', 9, RED, weight=700)
line(XS - 0.06, 6.25, XS - 0.06, 8.45, GAS, 2.4); line(XS - 0.06, 8.45, X0 + 0.05, 8.45, GAS, 2.4); line(X0 + 0.05, 8.45, X0 + 0.05, 8.7, GAS, 2.4); line(X0 + 0.05, 8.7, 0.62, 8.7, GAS, 1.6, '7 3')
text(XS - 0.12, 7.0, 'gas line in (G1)', 10.5, GAS, 'end', 600, rot=-90)
# GREASE TRAP and drain out
rect(XS - 0.45, XS - 0.05, 8.15, 8.6, '#e6ecef', BLU, 1.2); text(XS - 0.25, 8.375, 'GT', 10, BLU, weight=700)
line(X1 - 0.3, 8.4, X1 - 0.3, D - 0.05, BLU, 1, '5 3'); line(X1 - 0.3, D - 0.05, X0 + 0.1, D - 0.05, BLU, 1, '5 3')
# EXHAUST: through the back wall, along it, round the corner, ESP, fan, side discharge
EX = '#c4442a'
rect(-1.6, -1.1, D, D + T, '#f3e0dc', EX, 1.4, '6 3')
rect(XS - 0.45, -1.1, D + T, D + T + 0.4, '#f3e0dc', EX, 1.4, '6 3')
rect(XS - 0.45, XS - 0.05, D - 0.35, D + T + 0.4, '#f3e0dc', EX, 1.4, '6 3')
rect(XS - 0.5, XS + 0.02, D - 1.35, D - 0.35, '#e8c9c2', RED, 1.6); text(XS - 0.24, D - 0.85, 'ESP', 11, RED, weight=700, rot=-90)
circ(XS - 0.25, D - 1.55, 0.18, '#f3e0dc', EX, 1.4); text(XS - 0.25, D - 1.55, 'fan', 9, RED, weight=700)
rect(XS - 0.5, XS - 0.05, D - 1.95, D - 1.75, '#f3e0dc', EX, 1.4, '6 3')
a, b = P(XS - 0.5, D - 1.85); out.append(f'<path d="M{a:.1f} {b:.1f} l-34 0 m0 0 l10 -7 m-10 7 l10 7" stroke="{RED}" stroke-width="2.2" fill="none"/>')
for n, x, z in (('E1', -1.35, D + 0.1), ('E2', -2.3, D + T + 0.2), ('E3', XS - 0.85, D - 0.85), ('E4', XS - 0.85, D - 1.55), ('E5', XS - 0.85, D - 1.85)): tagc(x, z, n, RED)
rect(1.9, 2.4, D + T, D + T + 0.3, '#e1eadc', GRN, 1.3); tagc(2.15, D + T + 0.55, 'F1', GRN)
tagc(XS - 0.85, 8.45, 'G1', GAS)
# DIMENSIONS
for xa, xb, t in ((X0, -1.25, '1.20'), (-1.2, -0.6, '0.60'), (-0.55, 0.05, '0.60'), (0.1, 0.7, '0.60'), (0.95, 1.75, 'rear exit 0.80')):
    hdim(xa, xb, 8.03, t, RED, 11)
hdim(X1, X0, KZ - 0.25, '4.90 kitchen, inside', RED, 13)
for xa, xb, t in ((-2.2, -1.4, '0.80'), (-1.4, -0.6, '0.80'), (-0.6, 0.05, 'pass 0.65'), (0.1, 0.8, 'door 0.70'), (0.85, 1.18, '0.33')):
    hdim(xa, xb, KZ - 0.06, t, RED, 11)
vdim(X1 + T + 0.12, KZ + 0.1, D, '2.40', RED, 13)
vdim(-1.0, 7.05, 8.1, "cooks' aisle 1.05")
vdim(-2.0, KZ + 0.115, 7.05, '0.65', RED, 11); vdim(-0.95 + 0.6, 8.1, D, '0.70', RED, 11)
vdim(X1 + 0.07, 6.45, 7.4, '0.95', RED, 11); vdim(X1 + 0.07, 7.4, 8.0, '0.60', RED, 11); vdim(X1 + 0.07, 8.0, D, '0.80', RED, 11)
hdim(1.23, 1.7, 7.0, 'door swing 0.47', BLU, 10.5)
# north / orientation note and scale bar
sx, sy = POX + 10, POY + (ZT - 5.9) * S + 40
out.append(f'<g transform="translate({sx},{sy})"><rect width="{S}" height="9" fill="{INK}"/><rect x="{S}" width="{S}" height="9" fill="none" stroke="{INK}"/><text y="27" font-size="12.5" fill="{INK}">0</text><text x="{S}" y="27" font-size="12.5" text-anchor="middle" fill="{INK}">1 m</text><text x="{2*S}" y="27" font-size="12.5" text-anchor="middle" fill="{INK}">2 m</text><text x="{2*S+30}" y="9" font-size="12.5" fill="{MUT}">PLAN · 1:25 at A3 · back wall at the top, dining room at the bottom; left and right as you walk in from the road</text></g>')

# ---------------- hot-line elevation (back wall seen from inside the kitchen)
E = 120; EOX, EOY = 60, 1075
def Q(x, y): return (EOX + (X1 - x) * E, EOY + (H - y) * E)
def erect(xa, xb, ya, yb, fill='none', stroke=INK, sw=1.3, dash=None):
    (a, b), (c, d) = Q(max(xa, xb), max(ya, yb)), Q(min(xa, xb), min(ya, yb))
    out.append(f'<rect x="{a:.1f}" y="{b:.1f}" width="{c-a:.1f}" height="{d-b:.1f}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"' + (f' stroke-dasharray="{dash}"' if dash else '') + '/>')
def etext(x, y, t, size=12, fill=INK, anchor='middle', weight=500):
    a, b = Q(x, y); out.append(f'<text x="{a:.1f}" y="{b+size*0.35:.1f}" font-size="{size}" fill="{fill}" text-anchor="{anchor}" font-weight="{weight}">{t}</text>')
def eline(xa, ya, xb, yb, stroke=INK, sw=1.3, dash=None):
    a, b = Q(xa, ya); c, d = Q(xb, yb)
    out.append(f'<line x1="{a:.1f}" y1="{b:.1f}" x2="{c:.1f}" y2="{d:.1f}" stroke="{stroke}" stroke-width="{sw}"' + (f' stroke-dasharray="{dash}"' if dash else '') + '/>')
def eydim(x, ya, yb, t, col=RED):
    a, b = Q(x, ya); _, d = Q(x, yb)
    out.append(f'<g stroke="{col}" stroke-width="1.1"><line x1="{a:.1f}" y1="{b:.1f}" x2="{a:.1f}" y2="{d:.1f}"/><line x1="{a-5}" y1="{b:.1f}" x2="{a+5}" y2="{b:.1f}"/><line x1="{a-5}" y1="{d:.1f}" x2="{a+5}" y2="{d:.1f}"/></g>')
    out.append(f'<text x="{a+8:.1f}" y="{(b+d)/2+4:.1f}" font-size="11.5" fill="{col}" font-weight="600">{t}</text>')
out.append(f'<text x="{EOX}" y="{EOY-28}" font-size="20" font-weight="700" fill="{INK}">Hot line elevation · back wall seen from inside the kitchen · 1:40</text>')
erect(X0, X1, KC + 0.08, H, '#f4efe6', 'none'); etext(0.0, 3.65, 'STORAGE DECK above the kitchen ceiling · 1.7 m clear', 12, MUT, weight=600)
erect(X0, X1, 0, KC, '#ffffff', 'none'); erect(X0, X1, 0, 2.1, '#f2f4f2', 'none'); etext(1.35, 2.25, 'white tiles to 2.10 m', 10.5, MUT)
erect(X0, X1, KC, KC + 0.08, '#cdbfa8', 'none'); eline(X0, 0, X1, 0, INK, 2.2); eline(X0, H, X1, H, INK, 2.2)
erect(X0 - 0.05, X0, 0, H, WALL, WALL); erect(X1, X1 + 0.05, 0, H, WALL, WALL)
for xa, xb, h, t in ((X0, -1.25, 0.8, 'wok range'), (-1.2, -0.6, 0.8, 'steamer'), (-0.55, 0.05, 0.9, 'fryer'), (0.1, 0.7, 0.85, 'stock')):
    erect(xa, xb, 0, h, HOT); etext((xa + xb) / 2, h - 0.17, t, 11.5, '#fff', weight=700)
for x in (-2.1, -1.6): erect(x - 0.24, x + 0.24, 0.8, 0.95, '#3a3a3a')
for x in (-1.05, -0.75): erect(x - 0.13, x + 0.13, 0.8, 1.07, '#d8c49c')
erect(0.4, 0.7, 0.85, 1.19, '#c3c8cc')
eline(-1.85, 0.8, -1.85, 1.15, BLU, 2); eline(-1.85, 1.15, -1.85 + 0.0, 1.15, BLU, 2); etext(-1.85, 1.28, 'swan-neck tap', 10, BLU)
erect(X0 + 0.02, 0.8, 2.05, 2.6, '#e6e3de', RED, 1.6); etext(-0.8, 2.22, 'CANOPY HOOD 3.25 × 0.95 × 0.55 (tag 5)', 11.5, RED, weight=600)
erect(-1.6, -1.1, 2.35, 2.75, '#f3e0dc', RED, 1.3, '5 3'); etext(-1.35, 2.86, 'duct out through the wall', 10.5, RED, weight=600)
eline(X0 + 0.05, 0.4, 0.62, 0.4, GAS, 2.2, '7 3')
erect(0.95, 1.75, 0, 2.1, '#fbf7ef', INK, 1.2); etext(1.35, 1.05, 'rear exit', 11, MUT); etext(1.35, 0.88, '0.80 × 2.10', 10, MUT); eline(1.05, 1.0, 1.65, 1.0, INK, 2)
erect(0.76, 0.92, 1.3, 1.5, '#c8231b', '#c8231b'); etext(0.84, 1.62, 'pull + gas cut-off', 9.5, RED)
erect(0.73, 0.93, 0, 0.6, '#d6e2ef', BLU, 1); etext(0.83, 0.3, 'bin', 9, BLU)
erect(1.8, X1, 0, 0.9, STEEL); etext(2.12, 0.45, 'sink', 11, weight=700)
for y in (1.45, 1.85): erect(2.1, X1, y, y + 0.03, STEEL)
erect(1.9, 2.4, 3.3, 3.78, '#e1eadc', GRN, 1.2, '4 2'); etext(2.42, 3.93, 'fresh-air fan F1 (outside, 3.3 m)', 10, GRN, 'start')
erect(X0, X0 + 0.3, 1.45, 1.48, STEEL); erect(X0, X0 + 0.22, 0.97, 1.04, '#e6ecef', BLU)
eydim(X0 - 0.12, 0, 0.8, '0.80'); eydim(X0 - 0.42, 0, 2.05, '2.05'); eydim(X0 - 0.72, 0, KC, '2.70'); eydim(X0 - 1.02, 0, H, '4.50')
eydim(-1.0, 2.35, 2.75, '2.35–2.75')
a, b = Q(X1, -0.25); out.append(f'<text x="{a:.1f}" y="{b+12:.1f}" font-size="11.5" fill="{MUT}">left wall (dish line)</text>')
a, b = Q(X0, -0.25); out.append(f'<text x="{a:.1f}" y="{b+12:.1f}" font-size="11.5" fill="{MUT}" text-anchor="end">right wall (wok side)</text>')
a, b = Q(X1, -0.25); out.append(f'<text x="{a:.1f}" y="{b+32:.1f}" font-size="11.5" fill="{GAS}">Dashed gold line: gas manifold behind the hot line at 0.40 m, solenoid valve where the line enters</text>')

# ---------------- schedule + notes (right column)
CX = 1330; CW = 1090
rows = [('1', 'Chinese wok range, 2 burners', '1.20 × 0.70 × 0.80', 'gas (2 burners) · water (swan-neck tap) · drain'),
        ('2', 'Dim sum steamer, 2 holes', '0.60 × 0.70 × 0.80', 'gas · water auto-fill · drain'),
        ('3', 'Twin-tank fryer (veg / non-veg oil)', '0.60 × 0.70 × 0.90', 'gas'),
        ('4', 'Stock range, 2 burners', '0.60 × 0.70 × 0.85', 'gas'),
        ('5', 'Canopy hood, baffle filters, lights', '3.25 × 0.95 × 0.55, bottom 2.05', 'exhaust · wet-chemical suppression · 1-ph'),
        ('6', 'Non-veg prep bench, open undershelf, shelf over', '0.80 × 0.65 × 0.90', '1-ph socket'),
        ('7', 'Veg / dumpling bench + u/c freezer, 2 shelves over', '0.80 × 0.65 × 0.90', '1-ph (freezer) · socket'),
        ('8', 'Pass bench, 2 heat lamps, hatch 0.65 × 0.60', '0.65 × 0.65 × 0.90', '1-ph (lamps)'),
        ('9', 'Hand-wash sink at the door, hands-free tap', '0.33 × 0.40', 'hot + cold · drain'),
        ('10', 'Slim 2-door reach-in fridge', '0.95 × 0.75 × 2.00', '1-ph · on backup'),
        ('11', 'Under-counter dishwasher + drainboard', '0.60 × 0.65 × 0.90', 'cold · drain · 1-ph / 3-ph (confirm)'),
        ('12', '2-bowl sink + pre-rinse spray', '0.80 × 0.65 × 0.90', 'hot + cold · drain to grease trap'),
        ('13', 'Clean-plate shelves over the dish line (2)', '1.40 × 0.35 at 1.45 / 1.85', '—'),
        ('14', 'Wok seasoning rail: 8 pots + 8 squeeze bottles', '0.44 × 0.22 at 1.00', '—'),
        ('15', 'Back-up sauce + oil shelf', '0.90 × 0.30 at 1.45', '—'),
        ('16', 'Chilled mise-en-place rail, 5 pans (counter-top)', '0.76 × 0.26 × 0.22', '1-ph'),
        ('17', 'Dip + garnish rail at the pass · ticket rail', '0.65 × 0.12', '—'),
        ('18', 'Knife strips (2) · colour-coded board rack', '0.40 long · rack under bench 6', '—'),
        ('19', '10 L rice cooker', 'Ø 0.30', '1-ph'),
        ('20', 'Foot-pedal bins: wet, dry', 'Ø 0.20 × 0.60 each', '—'),
        ('21', 'Kitchen door with 3 apron hooks (inside)', '0.70 × 2.05, opens in', '—'),
        ('22', 'Insect killer over the door', '0.50 × 0.18', '1-ph'),
        ('23', 'Floor channel drain in front of the hot line', '3.15 × 0.08', 'to grease trap'),
        ('24', 'Make-up (fresh) air ceiling grille', '0.55 × 0.38', 'from fan F1 · interlocked'),
        ('25', 'Class K + CO₂ extinguishers, fire blanket, heat detector', 'wall brackets', '—'),
        ('26', 'Hood suppression manual pull + gas cut-off', 'by the rear exit', 'interlocked with gas + fan'),
        ('27', 'Hatch + fold-down ladder to the storage deck', '0.60 × 0.80 opening', '—'),
        ('E1', 'Duct through the back wall (hood collar 0.50 × 0.25)', '0.40 × 0.40 at 2.35–2.75', 'exhaust'),
        ('E2', 'Duct along the back wall, round the corner, forward', '0.40 × 0.40, outside', 'exhaust'),
        ('E3', 'ESP + carbon odour filter', '0.50 × 1.00 × 0.90 at 2.05–2.95', '1-ph · on backup'),
        ('E4', 'Inline exhaust fan', 'Ø 0.44', '1-ph / 3-ph · on backup'),
        ('E5', 'Side discharge away from the building, mesh + cowl', '0.40 × 0.40 at 2.4–2.8', '—'),
        ('F1', 'Fresh-air intake fan, back wall', '0.50 × 0.48 at 3.3', '1-ph · interlocked'),
        ('G1', 'LPG copper line in from the cage (4 × 19 kg)', 'along the outside wall at 1.3', 'solenoid + leak detector'),
        ('GT', 'Grease trap, outside back corner', '0.45 × 0.45', 'all kitchen drains')]
y = POY - 8
out.append(f'<text x="{CX}" y="{y}" font-size="20" font-weight="700" fill="{INK}">Equipment schedule</text>')
y += 26; cols = (CX, CX + 46, CX + 430, CX + 800)
out.append(f'<rect x="{CX-6}" y="{y-17}" width="{CW+6}" height="25" fill="#2a2420"/>')
for c, t in zip(cols, ('TAG', 'ITEM', 'SIZE W × D × H (m)', 'SERVICES')): out.append(f'<text x="{c}" y="{y}" font-size="12" font-weight="700" fill="#fff" letter-spacing=".04em">{t}</text>')
y += 25
for i, (tg, it, sz, ut) in enumerate(rows):
    if i % 2 == 0: out.append(f'<rect x="{CX-6}" y="{y-17}" width="{CW+6}" height="24.5" fill="#f3efe6"/>')
    col = RED if tg.startswith('E') else GRN if tg == 'F1' else GAS if tg == 'G1' else BLU if tg == 'GT' else INK
    out.append(f'<text x="{cols[0]}" y="{y}" font-size="13" font-weight="700" fill="{col}">{tg}</text><text x="{cols[1]}" y="{y}" font-size="13" fill="{INK}">{it}</text>'
               f'<text x="{cols[2]}" y="{y}" font-size="12.5" fill="{INK}" font-family="IBM Plex Mono, Menlo, monospace">{sz}</text><text x="{cols[3]}" y="{y}" font-size="12.5" fill="{MUT}">{ut}</text>')
    y += 24.5
y += 22
notes = [('Basis', ['22-dish menu: Tangra Indo-Chinese wok dishes, dim sum, bao, Korean bar food;', 'about 60–80 covers a day in season. One wok cook, one prep cook, one dishwasher.']),
         ('Exhaust', ['One canopy hood over all four appliances. Allow about 4,000–5,000 m³/h (vendor to size)', 'with ~8 m/s in the 0.40 × 0.40 duct. ESP + carbon filter before the fan; side discharge at', '~2.6 m: there is an apartment above (no roof stack) and parking behind. Make-up air about', '80% of the exhaust through ceiling grille 24 from fan F1, interlocked. Fan, ESP on backup power.']),
         ('Gas', ['LPG 4 × 19 kg in a locked, ventilated cage on the right side strip; copper line G1 along the', 'outside wall at 1.3 m, in behind the wok range; manifold with a valve per appliance; solenoid', 'shut-off interlocked with the exhaust fan and the hood suppression; leak detector.']),
         ('Water + drains', ['Hot + cold to the sink, pre-rinse and hand-wash; cold to the dishwasher, wok tap and steamer.', 'All kitchen drains and the channel drain go to grease trap GT, then the grey-water line', '(never the biodigester). Epoxy floor laid to fall to the channel drain.']),
         ('Power + finishes', ['1-ph points as listed; confirm the dishwasher and fan supply. The shop needs a 3-phase', 'connection of about 15–20 kW. Fridge, freezer, chilled rail, fan and ESP on the 7.5 kVA backup.', 'Benches SS 304 at 0.90 m; white wall tiles to 2.10 m; PVC ceiling at 2.70 m.']),
         ('Check on site', ['Pillar P2 (right wall) and the beams are estimates: measure before fabrication.', 'Kitchen door 0.70 opens in; rear exit 0.80 opens out with a panic bar; keep it clear.'])]
for h, ls in notes:
    out.append(f'<text x="{CX}" y="{y}" font-size="12.5" font-weight="700" fill="{RED}" letter-spacing=".06em">{h.upper()}</text>'); y += 19
    for l in ls: out.append(f'<text x="{CX}" y="{y}" font-size="13" fill="{INK}">{l}</text>'); y += 18.5
    y += 7
title = 'Kitchen layout · Betalbatim pub'
sub = 'For commercial kitchen equipment vendors · kitchen 4.90 × 2.40 m inside, ceiling 2.70 m · all dimensions in metres · tags match the equipment schedule'
svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{HH}" viewBox="0 0 {W} {HH}" font-family="IBM Plex Sans, Helvetica, Arial, sans-serif">
<rect width="100%" height="100%" fill="#fbf7ef"/>
<text x="60" y="70" font-size="34" font-weight="700" fill="{INK}">{title}</text>
<text x="60" y="104" font-size="16" fill="{MUT}">{sub}</text>
<text x="{W-60}" y="70" font-size="13" fill="{MUT}" text-anchor="end">Simplex · Concept 27 · singhgenics.github.io/Simplex/kitchen.html</text>
{''.join(out)}
</svg>'''
d = sys.argv[1]; os.makedirs(d, exist_ok=True)
open(d + '/kitchen-plan.svg', 'w').write(svg)
print(W, HH, 'rows', len(rows), 'notes end y', round(y))
