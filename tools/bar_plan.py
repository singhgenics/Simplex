#!/usr/bin/env python3
"""Draws the bar-section plan (renders/bar/bar-plan.svg) from the same coordinates as plan.py / the 3D model.
x runs from the right wall (-2.45) to the left wall (+2.45), z from the shopfront (0) to the back wall (8.8); the bar is on the left wall.
Drawn with the left wall at the left and the door end (low z) at the bottom, like the Simplex plan. Scale 1:20 when printed at 100% on A3."""
import os
X1 = 2.45
S = 230                      # px per metre
XL, XR = -0.45, 2.75         # drawn x range (stools to just past the left wall)
ZB, ZT = 2.35, 6.45          # drawn z range (door end to just past the kitchen front wall)
LEFT, TOP = 60, 110
def P(x, z): return (LEFT + (XR - x) * S, TOP + (ZT - z) * S)
W = int((XR - XL) * S) + LEFT + 560; H = int((ZT - ZB) * S) + TOP + 90
o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" font-family="IBM Plex Sans, Helvetica, Arial, sans-serif">', f'<rect width="{W}" height="{H}" fill="#FBF7EF"/>']
INK, MUT, RED, BLU, WALL = '#2a2420', '#6a5d4e', '#b23a1e', '#2a6f8f', '#4a4038'
def rect(xa, xb, za, zb, fill='none', stroke=INK, sw=1.4, dash=None):
    (a, b), (c, d) = P(max(xa, xb), max(za, zb)), P(min(xa, xb), min(za, zb))
    o.append(f'<rect x="{a:.1f}" y="{b:.1f}" width="{c-a:.1f}" height="{d-b:.1f}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"' + (f' stroke-dasharray="{dash}"' if dash else '') + '/>')
def circ(x, z, r, fill='none', stroke=INK, sw=1.4):
    a, b = P(x, z); o.append(f'<circle cx="{a:.1f}" cy="{b:.1f}" r="{r*S:.1f}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')
def line(xa, za, xb, zb, stroke=INK, sw=1.2, dash=None):
    a, b = P(xa, za); c, d = P(xb, zb); o.append(f'<line x1="{a:.1f}" y1="{b:.1f}" x2="{c:.1f}" y2="{d:.1f}" stroke="{stroke}" stroke-width="{sw}"' + (f' stroke-dasharray="{dash}"' if dash else '') + '/>')
def text(x, z, t, size=12, fill=INK, anchor='middle', weight=500, rot=0):
    a, b = P(x, z); tr = f' transform="rotate({rot} {a:.1f} {b:.1f})"' if rot else ''
    o.append(f'<text x="{a:.1f}" y="{b+size*0.35:.1f}" font-size="{size}" fill="{fill}" text-anchor="{anchor}" font-weight="{weight}"{tr}>{t}</text>')
def num(x, z, n, fill='#B5321C'):
    a, b = P(x, z); w = 8.4 * len(str(n)) + 10
    o.append(f'<rect x="{a-w/2:.1f}" y="{b-10:.1f}" width="{w:.1f}" height="20" rx="10" fill="{fill}"/><text x="{a:.1f}" y="{b+4.5:.1f}" font-size="12.5" fill="#fff" text-anchor="middle" font-weight="700">{n}</text>')
def hdim(xa, xb, z, t, off=0):
    a, b = P(xa, z); c, _ = P(xb, z); b += off
    o.append(f'<g stroke="{RED}" stroke-width="1.2"><line x1="{a:.1f}" y1="{b:.1f}" x2="{c:.1f}" y2="{b:.1f}"/><line x1="{a:.1f}" y1="{b-6:.1f}" x2="{a:.1f}" y2="{b+6:.1f}"/><line x1="{c:.1f}" y1="{b-6:.1f}" x2="{c:.1f}" y2="{b+6:.1f}"/></g><text x="{(a+c)/2:.1f}" y="{b-6:.1f}" font-size="12" fill="{RED}" text-anchor="middle" font-weight="600">{t}</text>')
def vdim(x, za, zb, t, off=0):
    a, b = P(x, za); _, d = P(x, zb); a += off
    o.append(f'<g stroke="{RED}" stroke-width="1.2"><line x1="{a:.1f}" y1="{b:.1f}" x2="{a:.1f}" y2="{d:.1f}"/><line x1="{a-6:.1f}" y1="{b:.1f}" x2="{a+6:.1f}" y2="{b:.1f}"/><line x1="{a-6:.1f}" y1="{d:.1f}" x2="{a+6:.1f}" y2="{d:.1f}"/></g><text x="{a-8:.1f}" y="{(b+d)/2:.1f}" font-size="12" fill="{RED}" text-anchor="middle" font-weight="600" transform="rotate(-90 {a-8:.1f} {(b+d)/2:.1f})">{t}</text>')
o.append(f'<text x="{LEFT}" y="40" font-size="26" font-weight="700" fill="#1B1714">Bar section · plan and equipment</text>')
o.append(f'<text x="{LEFT}" y="64" font-size="13" fill="{MUT}">Cabin East · Simplex concept 27 · metres · left wall on the left, door end at the bottom · numbers match the equipment list · scale 1:20 on A3 at 100%</text>')
# ---- shell: left wall, kitchen front wall ----
rect(X1, X1 + 0.2, ZB - 0.2, ZT + 0.1, WALL, WALL, 1)
rect(-0.4, X1, 6.3, 6.4, '#d8c6ac', '#d8c6ac', 1)
text(0.9, 6.35, 'kitchen front wall · door and pass', 11, MUT, weight=600)
# ---- back bar (left wall): 0.40 deep strip, 0.55 deep stretch for the built-ins ----
rect(2.05, X1, 2.72, 5.37, '#cfd7b2', INK, 1.4)
rect(1.90, 2.05, 3.77, 5.04, '#cfd7b2', INK, 1.4)
rect(2.05, X1, 2.78, 3.26, '#e6d6bc', '#8f6a4a', 1.2); num(2.25, 3.02, 10)                    # POS nook
rect(2.05, X1, 3.37, 3.72, '#e6d6bc', '#8f6a4a', 1.2); circ(2.2, 3.545, 0.075, '#9aa0a5', INK, 1.2); num(2.38, 3.545, 5)   # CO2 cabinet + 6 kg cylinder
rect(1.90, X1, 3.82, 4.52, '#dff0f6', BLU, 1.6); num(2.17, 4.17, 8)                            # mixer cooler 0.70 x 0.55
rect(1.90, X1, 4.57, 5.02, '#9aa0a5', INK, 1.6); num(2.17, 4.795, 9)                           # glasswasher 0.45 x 0.55
text(2.37, 5.2, 'back bar', 10, MUT, rot=-90)
rect(1.95, X1, 5.45, 6.25, '#cfd7b2', INK, 1.4); num(2.2, 5.85, 12)                            # server station
# ---- counter, kegs, chiller, ice, sink, font, stools ----
rect(0.35, 1.2, 2.94, 5.22, '#efe7da', INK, 2.0); num(0.47, 4.45, 1)
rect(0.59, 1.22, 3.04, 4.14, 'none', BLU, 1.6, '6 4'); num(0.69, 3.2, 3)                       # keg cabinet 1.10 x 0.63
for x, z in ((1.05, 3.21), (0.77, 3.21), (1.05, 3.49)): circ(x, z, 0.11, '#e4e8ea', BLU, 1.3)
text(0.9, 3.35, '', 8)
rect(0.67, 1.17, 3.66, 4.08, '#dff0f6', BLU, 1.6); num(0.92, 3.87, 4)                          # chiller 0.50 x 0.42
rect(1.0, 1.2, 4.16, 5.22, '#c3c8cc', INK, 1.2); num(1.1, 4.45, 6)                             # sink + ice well + speed rail
rect(0.67, 1.22, 4.64, 5.14, 'none', BLU, 1.6, '6 4'); num(0.82, 4.9, 7)                       # ice machine 0.55 x 0.50 under the counter
circ(0.85, 3.62, 0.045, '#d6a84a', '#8a6420', 1.6); num(0.62, 3.62, 2)                          # brass 3-tap font
line(0.3, 3.0, 0.3, 5.16, '#b8862a', 3)                                                         # brass foot rail
for z in (3.27, 3.87, 4.47, 5.07): circ(0.13, z, 0.21, '#efe2c8', '#8f6a4a', 1.3)
num(0.13, 3.27, 13, '#2F7A5B')
num(2.25, 5.2, 11, '#8a6420')
# ---- dimensions ----
hdim(1.2, 2.05, 5.48, '0.85 aisle', 0)
hdim(1.2, 1.90, 5.12, '0.68 at the built-ins', 0)
vdim(2.62, 2.72, 5.37, 'back bar 2.65', 0)
vdim(-0.28, 2.94, 5.22, 'counter 2.28 incl. square end and rail', 0)
vdim(1.9, 3.82, 4.52, '0.70', 0) if False else None
hdim(1.22, 0.59, 2.80, 'keg cabinet 0.63')
vdim(1.28, 3.04, 4.14, 'keg cabinet 1.10')
vdim(0.58, 3.66, 4.08, '0.42')
vdim(2.5, 4.57, 5.02, '0.45') if False else None
line(0.13, 5.35, 0.13, 5.35)
text(0.0, 5.45, 'stools 0.6 m apart', 11, MUT)
text(1.55, 2.5, 'door end of the bar', 11, MUT)
text(1.55, 6.12, 'bartender way in and out', 11, MUT, weight=600)
text(0.0, 2.55, 'to the window tables, 0.62 m', 10, MUT)
# ---- equipment list ----
rows = [
 (1, 'Bar counter', '2.20 L × 0.75 D × 1.04 H · square end · marble top, back-lit onyx and brass-mesh front, brass foot rail'),
 (2, 'Brass tap font, 3 taps', '≈ 0.42 H on the counter, over the keg cabinet · drip tray'),
 (3, 'Keg cabinet under the counter', '1.10 × 0.63 × 0.90 · 3 × 20 L kegs on a roll-out base · louvred timber doors'),
 (4, 'Beer flash chiller', '≈ 0.50 × 0.42 × 0.57 · self-contained, no outdoor unit, for room-temperature kegs'),
 (5, 'CO₂ cabinet', '0.35 wide in the back bar · 6 kg cylinder, chained · low vent · low CO₂ alarm'),
 (6, 'Bar sink, ice well, speed rail', '0.50 · on the bartender side of the counter, next to the ice machine'),
 (7, 'Ice machine, under the counter', '0.55 D × 0.50 W · about 50 kg a day · self-contained'),
 (8, 'Mixer cooler (glass door)', '0.70 W × 0.55 D · built into the back bar · mixers, water, soft drinks'),
 (9, 'Glasswasher, under the back bar', '0.45 W × 0.55 D · opposite the bar sink'),
 (10, 'POS nook', '0.48 W recessed in the back bar · cash drawer and safe below'),
 (11, 'Back bar', '2.65 L × 0.40 D × 0.96 H · 0.55 deep at the built-ins · 2.72 to 5.37 m from the front'),
 (12, 'Server station', '0.80 L × 0.50 D × 0.94 H · coffee, water, glasses, cutlery'),
 (13, 'Bar stools ×4', 'Ø 0.42 seat · seat 0.76 H · 0.6 m apart'),
]
lx = LEFT + int((XR - XL) * S) + 40
o.append(f'<text x="{lx}" y="{TOP-22}" font-size="15" font-weight="700" fill="#1B1714">Equipment (sizes W × D × H in metres)</text>')
import textwrap
y = TOP + 8
for n, name, spec in rows:
    w = 8.4 * len(str(n)) + 10
    o.append(f'<rect x="{lx}" y="{y-11}" width="{w:.1f}" height="20" rx="10" fill="{"#2F7A5B" if n == 13 else "#8a6420" if n in (11,) else "#B5321C"}"/><text x="{lx+w/2:.1f}" y="{y+3.5}" font-size="12.5" fill="#fff" text-anchor="middle" font-weight="700">{n}</text>')
    o.append(f'<text x="{lx+34}" y="{y+4}" font-size="13" font-weight="700" fill="{INK}">{name}</text>')
    y += 20
    for ln in textwrap.wrap(spec, 62):
        o.append(f'<text x="{lx+34}" y="{y+3}" font-size="11.5" fill="{MUT}">{ln}</text>'); y += 15
    y += 12
o.append(f'<text x="{LEFT}" y="{H-30}" font-size="11.5" fill="{MUT}">Counter 0.35 to 1.20 m, back bar 2.05 to 2.45 m from the right wall, as on the pub plan. Equipment heights are to fit under the 1.04 m counter and the 0.96 m back-bar top: the vendor confirms. Concept drawing, not for construction.</text>')
o.append('</svg>')
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'renders', 'bar', 'bar-plan.svg')
os.makedirs(os.path.dirname(out), exist_ok=True)
open(out, 'w').write('\n'.join(o)); print('wrote', out)
