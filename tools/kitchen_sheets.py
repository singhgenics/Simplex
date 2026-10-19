"""Two A3 kitchen sheets for vendors, drawn in real millimetres (viewBox 420 x 297) so the printed scales are exact.
Sheet 1: equipment layout, plan at 1:25 (40 mm per metre), every item named and sized on the drawing, equipment list.
Sheet 2: services and exhaust, plan at 1:25 with exhaust, gas, water, drains and power; hot-line elevation at 1:40 (25 mm per metre).
Model coordinates: x from the right wall (X0 = -2.45) to the left wall (X1 = 2.45) as you walk in; z from the shopfront to the back wall (D = 8.8).
Usage: python3 tools/kitchen_sheets.py build [--page]  ->  build/kitchen-sheet-1.svg, build/kitchen-sheet-2.svg (and kitchen.html with --page).\nPDFs: print the SVGs from Chrome headless with IBM Plex embedded, @page 420 x 297 mm, margin 0.
"""
import sys, os
X0, X1, D, T, KZ, KC, H = -2.45, 2.45, 8.8, 0.2, 6.3, 2.7, 4.5
XS = X0 - T
INK, MUT, RED, BLU, GAS, GRN, PWR = '#2a2420', '#6a5d4e', '#b23a1e', '#2f6f9f', '#a8741a', '#3f6a3a', '#6b3fa0'
WALL, STEEL, HOT, PAPER = '#4a4038', '#c9cdd1', '#9aa0a5', '#fbf7ef'
FT, FS, FB = 2.6, 2.5, 3.0          # text sizes in mm: ~7.4 pt, ~7.1 pt (minimum), ~8.5 pt


class Sheet:
    def __init__(s, ox, oy, xl, zt, k=40.0):
        s.o, s.ox, s.oy, s.xl, s.zt, s.k = [], ox, oy, xl, zt, k
    def P(s, x, z): return (s.ox + (s.xl - x) * s.k, s.oy + (s.zt - z) * s.k)
    def add(s, t): s.o.append(t)
    def rect(s, xa, xb, za, zb, fill='none', stroke=INK, sw=0.3, dash=None):
        (a, b), (c, d) = s.P(max(xa, xb), max(za, zb)), s.P(min(xa, xb), min(za, zb))
        s.add(f'<rect x="{a:.2f}" y="{b:.2f}" width="{c-a:.2f}" height="{d-b:.2f}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"' + (f' stroke-dasharray="{dash}"' if dash else '') + '/>')
    def line(s, xa, za, xb, zb, stroke=INK, sw=0.3, dash=None):
        a, b = s.P(xa, za); c, d = s.P(xb, zb)
        s.add(f'<line x1="{a:.2f}" y1="{b:.2f}" x2="{c:.2f}" y2="{d:.2f}" stroke="{stroke}" stroke-width="{sw}"' + (f' stroke-dasharray="{dash}"' if dash else '') + '/>')
    def circ(s, x, z, r, fill='none', stroke=INK, sw=0.3, dash=None):
        a, b = s.P(x, z); s.add(f'<circle cx="{a:.2f}" cy="{b:.2f}" r="{r*s.k:.2f}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"' + (f' stroke-dasharray="{dash}"' if dash else '') + '/>')
    def text(s, x, z, t, size=FT, fill=INK, anchor='middle', weight=500, rot=0):
        a, b = s.P(x, z); tr = f' transform="rotate({rot} {a:.2f} {b:.2f})"' if rot else ''
        s.add(f'<text x="{a:.2f}" y="{b+size*0.35:.2f}" font-size="{size}" fill="{fill}" text-anchor="{anchor}" font-weight="{weight}"{tr}>{t}</text>')
    def lines(s, x, z, ls, size=FT, fill=INK, gap=1.25):
        n = len(ls)
        for i, (t, w) in enumerate(ls):
            a, b = s.P(x, z); y = b + (i - (n - 1) / 2) * size * gap
            s.add(f'<text x="{a:.2f}" y="{y+size*0.35:.2f}" font-size="{size}" fill="{fill}" text-anchor="middle" font-weight="{w}">{t}</text>')
    def hdim(s, xa, xb, z, t, col=RED, size=FS):
        a, b = s.P(xa, z); c, _ = s.P(xb, z)
        s.add(f'<g stroke="{col}" stroke-width="0.25"><line x1="{a:.2f}" y1="{b:.2f}" x2="{c:.2f}" y2="{b:.2f}"/><line x1="{a:.2f}" y1="{b-1.2:.2f}" x2="{a:.2f}" y2="{b+1.2:.2f}"/><line x1="{c:.2f}" y1="{b-1.2:.2f}" x2="{c:.2f}" y2="{b+1.2:.2f}"/></g>')
        s.add(f'<text x="{(a+c)/2:.2f}" y="{b-0.9:.2f}" font-size="{size}" fill="{col}" text-anchor="middle" font-weight="600">{t}</text>')
    def vdim(s, x, za, zb, t, col=RED, size=FS):
        a, b = s.P(x, za); _, d = s.P(x, zb)
        s.add(f'<g stroke="{col}" stroke-width="0.25"><line x1="{a:.2f}" y1="{b:.2f}" x2="{a:.2f}" y2="{d:.2f}"/><line x1="{a-1.2:.2f}" y1="{b:.2f}" x2="{a+1.2:.2f}" y2="{b:.2f}"/><line x1="{a-1.2:.2f}" y1="{d:.2f}" x2="{a+1.2:.2f}" y2="{d:.2f}"/></g>')
        s.add(f'<text x="{a-1.0:.2f}" y="{(b+d)/2:.2f}" font-size="{size}" fill="{col}" text-anchor="middle" font-weight="600" transform="rotate(-90 {a-1.0:.2f} {(b+d)/2:.2f})">{t}</text>')
    def call(s, x, z, px, py, t, col=INK, anchor='start'):
        """leader from a point on the drawing to text placed at paper position (px, py) in mm"""
        a, b = s.P(x, z)
        s.add(f'<circle cx="{a:.2f}" cy="{b:.2f}" r="0.6" fill="{col}"/><polyline points="{a:.2f},{b:.2f} {px-(1.2 if anchor=="start" else -1.2):.2f},{py-0.9:.2f} {px-(0.2 if anchor=="start" else -0.2):.2f},{py-0.9:.2f}" fill="none" stroke="{col}" stroke-width="0.2"/>')
        s.add(f'<text x="{px:.2f}" y="{py:.2f}" font-size="{FS}" fill="{col}" text-anchor="{anchor}" font-weight="500">{t}</text>')
    def arc(s, cx, cz, r, x0, z0, x1, z1, sweep, col=INK):
        a, b = s.P(x0, z0); c, d = s.P(x1, z1)
        s.add(f'<path d="M{a:.2f} {b:.2f} A{r*s.k:.2f} {r*s.k:.2f} 0 0 {sweep} {c:.2f} {d:.2f}" fill="none" stroke="{col}" stroke-width="0.2" stroke-dasharray="1 0.8"/>')
        s.line(cx, cz, x1, z1, col, 0.45)

    # ---- shared shell of the kitchen
    def shell(s, outside_strip=False):
        s.rect(X0, X1, KZ + 0.1, D, '#eef0ec', 'none')
        s.rect(XS, X0, KZ - 0.35, D + T, WALL, WALL, 0.2); s.rect(X1, X1 + T, KZ - 0.35, D + T, WALL, WALL, 0.2)
        s.rect(X0, 0.95, D, D + T, WALL, WALL, 0.2); s.rect(1.75, X1, D, D + T, WALL, WALL, 0.2)
        for xa, xb in ((X0, -0.6), (0.05, 0.1), (0.9, X1)): s.rect(xa, xb, KZ, KZ + 0.1, '#d8c6ac', '#a8987c', 0.2)
        s.rect(-0.6, 0.05, KZ, KZ + 0.1, '#cfe3ea', '#7a9aaa', 0.2)
        s.rect(X0, X0 + 0.23, 6.65, 6.95, WALL, WALL, 0.2); s.text(X0 + 0.115, 6.8, 'P2', FS, '#fff', weight=700)
        s.arc(0.1, KZ + 0.1, 0.8, 0.9, KZ + 0.1, 0.1, KZ + 0.9, 1)                        # kitchen door: double-acting (shown swung into the kitchen; it also swings into the dining room)

        s.arc(1.75, D + T, 0.8, 0.95, D + T, 1.75, D + T + 0.8, 0)                        # rear exit, opens out
        for hz, sg in ((6.45, 1), (7.4, -1)):                                             # fridge door swings
            a, b = s.P(1.7, hz); c, d = s.P(1.23, hz); r = 0.47 * s.k
            s.add(f'<path d="M{c:.2f} {d:.2f} A{r:.2f} {r:.2f} 0 0 {0 if sg>0 else 1} {a:.2f} {b-sg*r:.2f}" fill="none" stroke="{BLU}" stroke-width="0.2" stroke-dasharray="1 0.8"/>')

    def scalebar(s, px, py, label):
        k = s.k
        s.add(f'<g transform="translate({px:.2f},{py:.2f})"><rect width="{k}" height="1.6" fill="{INK}"/><rect x="{k}" width="{k}" height="1.6" fill="none" stroke="{INK}" stroke-width="0.2"/>'
              f'<text y="5" font-size="{FS}" fill="{INK}">0</text><text x="{k}" y="5" font-size="{FS}" text-anchor="middle" fill="{INK}">1 m</text><text x="{2*k}" y="5" font-size="{FS}" text-anchor="middle" fill="{INK}">2 m</text>'
              f'<text x="{2*k+6}" y="1.8" font-size="{FT}" font-weight="700" fill="{INK}">{label}</text></g>')


def frame(title, sub, sheet_no, body):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="420mm" height="297mm" viewBox="0 0 420 297" font-family="IBM Plex Sans, Helvetica, Arial, sans-serif">
<rect width="420" height="297" fill="{PAPER}"/>
<rect x="5" y="5" width="410" height="287" fill="none" stroke="{INK}" stroke-width="0.35"/>
<text x="12" y="16" font-size="7" font-weight="700" fill="{INK}">{title}</text>
<text x="12" y="22.5" font-size="{FT}" fill="{MUT}">{sub}</text>
<text x="408" y="13" font-size="{FT}" fill="{MUT}" text-anchor="end">Cabin East · Wok | Steam | Draught · Concept 27</text>
<text x="408" y="18" font-size="{FB}" font-weight="700" fill="{INK}" text-anchor="end">Sheet {sheet_no} of 2 · A3</text>
<text x="408" y="22.5" font-size="{FS}" fill="{MUT}" text-anchor="end">singhgenics.github.io/Simplex/kitchen.html</text>
<line x1="5" y1="26" x2="415" y2="26" stroke="{INK}" stroke-width="0.25"/>
{body}
</svg>'''


def table(rows, x, y, cols, head, rowh=4.2, size=FS, zebra='#f3efe6', width=None):
    o = []; width = width or (cols[-1] - x + 30)
    o.append(f'<rect x="{x-1.5}" y="{y-3.3}" width="{width}" height="4.6" fill="{INK}"/>')
    for c, t in zip(cols, head): o.append(f'<text x="{c}" y="{y}" font-size="{size}" font-weight="700" fill="#fff">{t}</text>')
    y += rowh + 0.6
    for i, r in enumerate(rows):
        if i % 2 == 0: o.append(f'<rect x="{x-1.5}" y="{y-3.1}" width="{width}" height="{rowh}" fill="{zebra}"/>')
        for j, (c, t) in enumerate(zip(cols, r)):
            col, w = (r[-1] if isinstance(r[-1], str) and r[-1].startswith('#') and j == 0 else INK), (700 if j == 0 else 500)
            if isinstance(t, str) and t.startswith('#'): continue
            o.append(f'<text x="{c}" y="{y}" font-size="{size}" fill="{col}" font-weight="{w}">{t}</text>')
        y += rowh
    return ''.join(o), y


def notes_block(blocks, x, y, width_chars=None, size=FS, lead=3.4):
    o = []
    for h, ls in blocks:
        o.append(f'<text x="{x}" y="{y}" font-size="{size}" font-weight="700" fill="{RED}" letter-spacing="0.15">{h.upper()}</text>'); y += lead + 0.3
        for l in ls: o.append(f'<text x="{x}" y="{y}" font-size="{size}" fill="{INK}">{l}</text>'); y += lead
        y += 1.6
    return ''.join(o), y


# ======================================================================= SHEET 1: equipment layout
s = Sheet(12, 30, X1 + T + 0.3, D + T + 1.05)
s.shell()
s.add(f'<text x="12" y="{s.P(0, KZ-0.6)[1]:.2f}" font-size="{FS}" fill="{MUT}">DINING ROOM SIDE</text>')
import boq_goa
NUM = {k: str(v) for k, v in boq_goa.NUM.items()}   # plain BOQ numbers 1 to 44, the same on every drawing and in every list
def nm(ref): return NUM[ref]
# hot line
for xa, xb, ls in ((X0, -1.25, [(nm('B.01'), 800), ('Wok range', 700), ('2 burners', 500), ('1.20 × 0.80 × 0.80', 500)]),
                   (-1.2, -0.6, [(nm('B.02'), 800), ('Dim sum', 700), ('steamer', 700), ('0.60 × 0.70', 500), ('h 0.80', 500)]),
                   (-0.55, 0.05, [(nm('B.03'), 800), ('Twin-tank', 700), ('fryer', 700), ('0.60 × 0.70', 500), ('h 0.90', 500)]),
                   (0.1, 0.7, [(nm('B.04'), 800), ('Stock', 700), ('range', 700), ('0.60 × 0.70', 500), ('h 0.85', 500)])):
    s.rect(xa, xb, 8.0 if xa == X0 else 8.1, D, HOT, INK, 0.3); s.lines((xa + xb) / 2, 8.45, ls, FT, '#fff')
s.rect(X0, 0.9, 7.85, D - 0.02, 'none', RED, 0.45, '2.2 1.2')
s.rect(-2.4, 0.75, 7.92, 8.0, '#b9c0c5', '#6d7276', 0.15)
# front-wall benches
s.rect(-2.2, -1.4, KZ + 0.115, 7.05, STEEL, INK, 0.3); s.lines(-1.8, 6.86, [(nm('A.01'), 800), ('Non-veg prep', 700), ('0.80 × 0.65 · h 0.90', 500)])
s.rect(-2.18, -1.42, 6.42, 6.68, '#dff0f6', BLU, 0.3)
s.rect(-1.4, -0.6, KZ + 0.115, 7.05, STEEL, INK, 0.3); s.lines(-1.15, 6.8, [(nm('A.02'), 800), ('Veg / dumpling', 700), ('0.80 × 0.65', 500), ('freezer under', 500)], 2.5)
[s.circ(-0.75, z, 0.13, '#e9e9e9', '#6d7276', 0.25) for z in (6.56, 6.9)]   # two 5 L rice cookers
s.rect(-0.6, 0.05, KZ + 0.115, 7.05, STEEL, INK, 0.3); s.lines(-0.275, 6.7, [(nm('A.03'), 800), ('Pass', 700), ('0.65 × 0.65', 500), ('u/c fridge ' + nm('B.06'), 500)])
s.rect(-0.6, 0.05, 6.93, 7.05, '#e6ecef', BLU, 0.25)
s.rect(0.92, 1.2, KZ + 0.115, 6.8, STEEL, INK, 0.3); s.text(1.06, 6.6, 'HW', FS, weight=700)
s.rect(X0, X0 + 0.25, KZ + 0.115, 6.65, STEEL, INK, 0.3); s.text(X0 + 0.125, 6.53, 'HW', 2.5, weight=700)   # second hand-wash at the prep corner
s.rect(X0, X0 + 0.45, 7.12, 7.6, STEEL, INK, 0.3); s.lines(X0 + 0.225, 7.5, [(nm('A.06'), 800), ('Veg sink', 700), ('0.45 × 0.50', 500)], 2.5)
# left wall
s.rect(1.7, X1, 6.45, 7.4, STEEL, INK, 0.3); s.lines(2.08, 6.92, [(nm('B.05'), 800), ('Dual-temp', 700), ('reach-in', 700), ('fridge + freezer', 500), ('0.95 × 0.75', 500), ('h 2.00', 500)], 2.5)
s.rect(1.8, X1, 7.4, 8.0, STEEL, INK, 0.3); s.lines(2.12, 7.7, [(nm('B.08'), 800), ('Dish-', 700), ('washer', 700), ('0.60 × 0.65', 500)])
s.rect(1.8, X1, 8.0, D, STEEL, INK, 0.3); s.lines(2.12, 8.22, [(nm('A.04'), 800), ('2-bowl', 700), ('sink', 700), ('0.80 × 0.65', 500)], 2.5)
s.circ(2.27, 8.62, 0.16, 'none', BLU, 0.3, '1.2 0.8')   # water heater above
# right wall + small kit
s.rect(X0, X0 + 0.3, 7.15, 8.05, 'none', MUT, 0.2, '1 0.8'); s.rect(X0, X0 + 0.22, 7.62, 8.06, '#e6ecef', BLU, 0.3)
s.rect(-2.1, -1.86, KZ + 0.1, KZ + 0.16, '#d9261c', '#d9261c', 0.2)
s.circ(-2.27, 7.27, 0.085, '#cfe0bf', GRN, 0.3, '0.8 0.6'); s.circ(0.83, 8.62, 0.1, '#d6e2ef', BLU, 0.3); s.circ(0.83, 8.71, 0.07, '#c8231b', '#c8231b', 0.2); s.circ(0.4, 8.74, 0.04, BLU, BLU, 0.2)
s.rect(-2.12, -1.84, 6.5, 6.76, 'none', '#8f6a4a', 0.25, '0.8 0.6')
for xa, xb in ((-1.84, -1.44), (-1.35, -0.95)): s.line(xa, KZ + 0.13, xb, KZ + 0.13, INK, 0.8)
s.rect(1.0, 1.6, 7.45, 8.25, 'none', BLU, 0.3, '1.6 0.9'); s.lines(1.3, 7.85, [(nm('A.20'), 800), ('Ceiling hatch', 600), ('0.60 × 0.80', 500), (nm('B.21'), 800), ('+ goods hoist', 600)], 2.5, BLU)
for xa, xb, za, zb in ((-2.4, -1.8, 7.0, 7.5), (-0.95, -0.35, 7.1, 7.6)):
    s.rect(xa, xb, za, zb, 'none', GRN, 0.3, '1 0.6')
    if xa > -1.5: s.lines((xa + xb) / 2, (za + zb) / 2, [(nm('B.19'), 800), ('Make-up air', 600), ('0.60 × 0.50', 500)], 2.5, GRN)
s.text(0.62, 7.62, 'KITCHEN', FB, INK, weight=700); s.text(0.62, 7.48, '4.90 × 2.40 m', FS, INK, weight=600); s.text(0.62, 7.36, 'ceiling 2.70 m', FS, MUT)
s.text(-1.05, 7.96, nm('A.15') + '  floor channel drain 3.15 × 0.08', 2.5, INK, weight=600)
# dimensions
for xa, xb, t in ((X0, -1.25, '1.20'), (-1.2, -0.6, '0.60'), (-0.55, 0.05, '0.60'), (0.1, 0.7, '0.60'), (0.95, 1.75, 'rear exit 0.80')): s.hdim(xa, xb, D + T + 0.12, t)
s.hdim(X1, X0, D + T + 0.45, '4.90 inside')
for xa, xb, t in ((-2.2, -1.4, '0.80'), (-1.4, -0.6, '0.80'), (-0.6, 0.05, '0.65'), (0.1, 0.9, 'door 0.80'), (0.92, 1.2, '0.28')): s.hdim(xa, xb, KZ - 0.08, t)
s.vdim(X1 + T + 0.24, KZ + 0.1, D, '2.40 inside')
s.vdim(-0.3, 7.05, 8.1, "cooks' aisle 1.05"); s.vdim(-1.3, 7.05, 8.0, '0.95 at the wok range')
for za, zb, t in ((6.45, 7.4, '0.95'), (7.4, 8.0, '0.60'), (8.0, D, '0.80')): s.vdim(X1 + T + 0.1, za, zb, t)
# callouts. Right margin: items on the right wall, horizontal leaders at the item's own depth.
R = s.P(XS, 0)[0] + 5
s.line(X0 + 0.05, 8.13, X0 + 0.05, 8.6, BLU, 0.9, '1.4 0.5')   # wok tool rail on the wall at 1.4 m, over the range
for x, z, zt, t in ((X0 + 0.05, 8.36, 8.3, nm('A.09') + '  Wok tool rail at 1.4 m · 4 tools'), (X0 + 0.25, 8.0, 8.03, nm('A.07') + '  Sauce + oil shelf above, at 1.45 m'), (X0 + 0.11, 7.84, 7.8, nm('A.08') + '  Wok seasoning rail at 1.0 m · 0.44 × 0.22'),
                    (X0 + 0.2, 7.36, 7.36, nm('A.06') + '  Veg + herb sink 0.45 × 0.50 · wet bin under'), (X0 + 0.03, 6.72, 6.8, 'Pillar P2: measure on site'),
                    (X0 + 0.12, 6.52, 6.52, 'Second hand-wash 0.25 · 3 apron hooks')):
    s.call(x, z, R, s.P(0, zt)[1] + 0.9, t)
# top: dry bin, straight up past the back wall
for (x, z, row, t) in ((2.27, 8.62, 0, nm('B.12') + '  Water heater 35 L, 3 kW, high on the left wall over the dish sink'), (0.88, 8.74, 1, 'Class K extinguisher on the wall, above the dry bin · suppression pull above it'),
                       (0.78, 8.62, 2, 'Dry bin (pedal) Ø 0.20 · keeps the rear exit clear'), (0.4, 8.74, 3, 'Pot filler over the stock range · cold, swing arm')):
    a, b = s.P(x, z); ty = s.P(0, D + T + 0.78)[1] - (2 - row) * 4.3
    s.add(f'<circle cx="{a:.2f}" cy="{b:.2f}" r="0.6" fill="{INK}"/><polyline points="{a:.2f},{b:.2f} {a:.2f},{ty-0.9:.2f} {a+1.5:.2f},{ty-0.9:.2f}" fill="none" stroke="{INK}" stroke-width="0.2"/><text x="{a+2:.2f}" y="{ty:.2f}" font-size="{FS}" fill="{INK}">{t}</text>')
s.add(f'<text x="12" y="{s.P(0, D+T+0.35)[1]+13:.2f}" font-size="{FS}" fill="{MUT}">OUTSIDE (parking)</text>')
# bottom: front-wall items. Stair-stepped rows, rightmost item on the top row, so no leader crosses any text.
bot = [(-2.05, 6.63, nm('A.14') + '  Colour-coded board rack in slots under the bench (4 boards)'), (-1.9, KZ + 0.13, 'Fire blanket on the wall'),
       (-1.6, 6.55, nm('A.10') + '  Chilled mise-en-place rail on the bench · 0.76 × 0.26'), (-1.3, 6.62, 'Shelf over the veg bench: mixer-grinder ' + nm('B.10') + ', kitchen torch ' + nm('B.11')), (-1.2, KZ + 0.13, nm('A.13') + '  Magnetic knife strips on the wall over both benches · 0.40 each'),
       (-0.75, 6.56, nm('B.09') + '  Two 5 L rice cookers (jasmine, sticky) · Ø 0.26'), (-0.55, 6.99, nm('A.11') + '  Dip + garnish rail on the pass · ' + nm('A.12') + '  ticket rail above the hatch'),
       (0.5, KZ + 0.1, 'Double-acting door 0.80 with vision panel · insect killer ' + nm('B.14') + ' above'), (1.06, 6.6, 'Hand-wash at the door 0.28 × 0.40 · hands-free tap · 6 L heater')]
y0 = s.P(0, KZ - 0.42)[1]
for i, (x, z, t) in enumerate(bot):
    a, b = s.P(x, z); ty = y0 + i * 4.3
    s.add(f'<circle cx="{a:.2f}" cy="{b:.2f}" r="0.6" fill="{INK}"/><polyline points="{a:.2f},{b:.2f} {a:.2f},{ty-0.9:.2f} {a+1.5:.2f},{ty-0.9:.2f}" fill="none" stroke="{INK}" stroke-width="0.2"/><text x="{a+2:.2f}" y="{ty:.2f}" font-size="{FS}" fill="{INK}">{t}</text>')
s.scalebar(12, 252, 'PLAN 1:25 on A3 · dimensions in metres')
s.add(f'<text x="12" y="263" font-size="{FS}" fill="{MUT}">Back wall at the top, dining room at the bottom; left and right as you walk in from the road. Dashed red: canopy hood above (3.35 × 0.95, bottom 2.05 m).</text>')
s.add(f'<text x="12" y="267.5" font-size="{FS}" fill="{MUT}">Dashed blue: hatch and fridge doors. Dashed green: make-up air diffusers above (2). Dashed grey: shelves above. Heights and services: sheet 2.</text>')
import boq
eq = []
by = {i[0]: i for sec in boq.S for i in sec[3]}
for sl, title, _note, items in boq_goa.GOA:
    eq.append(('', title.upper(), '', ''))
    for r in items:
        no, item, size, spec, unit, qty, ref = by[r['no']]
        item = r['item'] if r['no'] in ('A.16', 'A.17', 'B.16', 'B.17', 'B.18', 'B.19', 'B.20', 'E.03') else item
        q = f'{qty:g}' if isinstance(qty, float) else str(qty)
        sz = size.replace(' section', ''); sz = '3 sizes, see BOQ' if len(sz) > 26 else sz
        eq.append((NUM[r['no']], item, sz, f'{q} {unit}'))
eq.append(('', 'Gas, plumbing, electrical, civil, fire: main BOQ', '', ''))
CX = 300
t, y = table(eq, CX, 36, (CX, CX + 9, CX + 63, CX + 100), ('NO', 'EQUIPMENT / TYPE', 'SIZE W × D × H (mm)', 'QTY'), 3.75, FS, width=111)
s.add(f'<text x="{CX-1.5}" y="31.5" font-size="{FB}" font-weight="700" fill="{INK}">Equipment list: the same numbers 1 to 44 as the BOQ</text>' + t)
nb, y = notes_block([('Notes', ['Stainless steel 304 benches, 0.90 m high; hot line 0.70 deep,', "wok range 0.80. Cooks' aisle 1.05 m (0.95 m at the wok range).", 'Cement-board ceiling at 2.70 m; storage deck above, hoist at the hatch.',
                                'Pan-Asian menu: about 23 recipes, 40 choices; one chef + one helper.', 'The numbers 1 to 44 on the items are the BOQ numbers (boq.html).', 'Positions are from the 3D model: check walls and pillar P2 on site.'])], CX - 1.5, y + 4)
s.add(nb)
sheet1 = frame('Kitchen equipment layout', 'For commercial kitchen equipment vendors · plan at 1:25 on A3 · every item named and sized on the drawing', 1, ''.join(s.o))

# ======================================================================= SHEET 2: services + exhaust
s = Sheet(12, 30, X1 + T + 0.3, D + T + 0.8)
s.shell()
s.rect(XS - 0.5, XS, KZ - 0.35, D + T, '#ece6db', 'none')
s.add(f'<text x="12" y="{s.P(0, D+T+0.62)[1]:.2f}" font-size="{FS}" fill="{MUT}">OUTSIDE · back (parking)</text>')
# equipment as light outlines with names
for xa, xb, za, zb, t in ((X0, -1.25, 8.0, D, nm('B.01') + '|Wok range|1,200 × 800 × 800'), (-1.2, -0.6, 8.1, D, nm('B.02') + '|Dim sum|steamer|600 × 700 × 800'), (-0.55, 0.05, 8.1, D, nm('B.03') + '|Fryer|600 × 700 × 900'), (0.1, 0.7, 8.1, D, nm('B.04') + '|Stock range|600 × 700 × 850'),
                          (-2.2, -1.4, KZ + 0.115, 7.05, nm('A.01') + '|Non-veg prep|800 × 650 × 900'), (-1.4, -0.6, KZ + 0.115, 7.05, nm('A.02') + '|Veg prep|800 × 650 × 900'), (-0.6, 0.05, KZ + 0.115, 7.05, nm('A.03') + '|Pass|650 × 650 × 900'),
                          (0.92, 1.2, KZ + 0.115, 6.8, ''), (X0, X0 + 0.25, KZ + 0.115, 6.65, ''), (X0, X0 + 0.45, 7.12, 7.6, ''), (1.7, X1, 6.45, 7.4, nm('B.05') + '|Reach-in|950×750×2,000'), (1.8, X1, 7.4, 8.0, nm('B.08') + '|Dishwasher|600×650×900'), (1.8, X1, 8.0, D, nm('A.04') + '|Dish sink|800×650×900')):
    s.rect(xa, xb, za, zb, '#f4f4f2', '#9aa0a5', 0.25)
    if t:
        ls = [(w, 800 if i == 0 else (700 if '×' not in w else 500)) for i, w in enumerate(t.split('|'))]
        if xa > 1.6: ls = [(w.replace('|', ''), wt) for w, wt in ls]; s.lines(xa + 0.2, (za + zb) / 2, ls, FS, '#5d666c')
        elif za >= 8: s.lines((xa + xb) / 2, 8.22 if xb - xa < 0.7 else 8.2, ls, FS, '#5d666c')
        else: s.lines((xa + xb) / 2, (za + zb) / 2 + 0.1, ls, FS, '#5d666c')
# EXHAUST (red)
s.rect(X0, 0.9, 7.85, D - 0.02, 'none', RED, 0.45, '2.2 1.2'); s.text(-1.6, 7.72, 'canopy hood above · bottom 2.05 m', FS, RED, weight=600)
s.rect(-1.6, -1.1, 8.4, D, 'none', RED, 0.35, '1.4 0.8')
EX = '#c4442a'
for xa, xb, za, zb in ((-1.6, -1.1, D, D + T), (XS - 0.45, -1.1, D + T, D + T + 0.4), (XS - 0.45, XS - 0.05, D - 0.35, D + T + 0.4)): s.rect(xa, xb, za, zb, '#f3e0dc', EX, 0.3, '1.4 0.8')
s.rect(XS - 0.5, XS + 0.02, D - 1.35, D - 0.35, '#e8c9c2', RED, 0.4); s.text(XS - 0.24, D - 1.05, 'E3 ESP', FS, RED, weight=700, rot=-90)
s.circ(XS - 0.25, D - 1.55, 0.18, '#f3e0dc', EX, 0.3); s.text(XS - 0.25, D - 1.55, 'E4', FS, RED, weight=700)
s.rect(XS - 0.5, XS - 0.05, D - 1.95, D - 1.75, '#f3e0dc', EX, 0.3, '1.4 0.8')
a, b = s.P(XS - 0.5, D - 1.85); s.add(f'<path d="M{a:.2f} {b:.2f} l6 0 m0 0 l-1.8 -1.2 m1.8 1.2 l-1.8 1.2" stroke="{RED}" stroke-width="0.45" fill="none"/><text x="{a+7.5:.2f}" y="{b+0.9:.2f}" font-size="{FS}" font-weight="700" fill="{RED}">E5 out</text>')
s.text(-1.35, 8.47, 'E1', FS, RED, weight=700); s.text(-2.0, D + T + 0.2, 'E2 duct outside, 0.40 × 0.40 at 2.35–2.75 m', FS, RED, weight=700)
for xa, xb, za, zb in ((-2.4, -1.8, 7.0, 7.5), (-0.95, -0.35, 7.1, 7.6)): s.rect(xa, xb, za, zb, 'none', GRN, 0.35, '1 0.6'); s.text((xa + xb) / 2, (za + zb) / 2, 'MA', FS, GRN, weight=700)
s.rect(1.9, 2.4, D + T, D + T + 0.3, '#e1eadc', GRN, 0.3); s.text(2.15, D + T + 0.15, 'F1', FS, GRN, weight=700)
# GAS (gold): from the cage on the side strip, along the outside wall at 1.3 m, in behind the wok, manifold along the back
s.line(XS - 0.06, KZ - 0.3, XS - 0.06, 8.7, GAS, 0.7); s.line(XS - 0.06, 8.7, X0 + 0.06, 8.7, GAS, 0.7)
s.line(X0 + 0.06, 8.7, X0 + 0.06, 8.74, GAS, 0.7); s.line(X0 + 0.06, 8.74, 0.62, 8.74, GAS, 0.55, '1.6 0.8')
for x in (-2.1, -1.6, -0.9, -0.25, 0.25, 0.55): s.circ(x, 8.74, 0.035, GAS, GAS, 0.2)
s.circ(X0 + 0.12, 7.72, 0.075, '#fff', GAS, 0.3); s.text(X0 + 0.12, 7.72, 'L', FS, GAS, weight=700)
a, b = s.P(XS - 0.06, KZ - 0.3); s.add(f'<path d="M{a:.2f} {b+3:.2f} l0 -3 m0 0 l-1.1 1.6 m1.1 -1.6 l1.1 1.6" stroke="{GAS}" stroke-width="0.5" fill="none"/>')
# WATER (blue points) and DRAINS (blue dashed)
for x, z, t in ((2.38, 8.2, 'HC'), (2.38, 7.7, 'HC'), (1.06, 6.45, 'HC'), (X0 + 0.12, 6.45, 'HC'), (X0 + 0.2, 7.36, 'C'), (-1.85, 8.55, 'C'), (-0.9, 8.55, 'C'), (0.4, 8.55, 'C')):
    s.circ(x, z, 0.075, '#fff', BLU, 0.35); s.text(x, z, t, FS, BLU, weight=700)
HWC = '#c2571a'
s.circ(2.27, 8.62, 0.16, '#fbe9dc', HWC, 0.4); s.text(2.27, 8.62, 'W', FS, HWC, weight=700); s.line(2.42, 8.5, 2.42, 7.7, HWC, 0.5, '1.4 0.8')   # 35 L heater and its hot line to the sink + dishwasher
s.line(XS - 0.2, 8.5, X0 + 0.05, 8.5, '#3b8fd0', 0.6); s.text(XS - 0.2, 8.28, 'WM', FS, '#3b8fd0', weight=700, rot=-90)   # cold water main in through the right wall
s.rect(-2.4, 0.75, 7.92, 8.0, '#cfe0ea', BLU, 0.25)
DZ = D - 0.16
for (xa, za, xb, zb) in ((2.2, 7.6, X1 - 0.07, 7.6), (X1 - 0.07, 7.6, X1 - 0.07, DZ), (X1 - 0.07, DZ, XS - 0.25, DZ), (XS - 0.25, DZ, XS - 0.25, 8.6),
                         (-2.4, 7.96, XS - 0.25, 7.96), (XS - 0.25, 7.96, XS - 0.25, 8.15)): s.line(xa, za, xb, zb, BLU, 0.4, '1.2 0.7')
s.rect(XS - 0.45, XS - 0.05, 8.15, 8.6, '#e6ecef', BLU, 0.35); s.text(XS - 0.25, 8.25, 'GT', FS, BLU, weight=700)
s.rect(XS - 0.13, XS + 0.01, 8.55, 8.69, '#fff', GAS, 0.35); s.text(XS - 0.06, 8.62, 'S', FS, GAS, weight=700)   # solenoid valve outside, on the entry
for x, z in ((2.38, 8.4), (2.38, 7.6), (1.06, 6.62), (X0 + 0.2, 7.2), (-0.9, 8.4), (-1.85, 8.4)):
    a, b = s.P(x, z); s.add(f'<path d="M{a-1:.2f} {b-0.8:.2f} l2 0 l-1 1.7 z" fill="{BLU}"/>')
# POWER (purple squares)
pw = [('1', 2.0, 6.62), ('2', -1.0, 6.55), ('3', -0.72, 6.5), ('10', -0.02, 6.5), ('11', -1.2, 6.5), ('4', -1.6, 6.5), ('5', -0.28, 6.55), ('6', 2.05, 7.42), ('7', 0.45, 6.5), ('8', 2.36, 7.5), ('9', 2.36, 7.92), ('12', 2.0, 8.05), ('13', 1.14, 6.66), ('13', X0 + 0.2, 6.66), ('14', 1.3, 7.62)]
for n, x, z in pw:
    a, b = s.P(x, z); s.add(f'<rect x="{a-3.4:.2f}" y="{b-2.2:.2f}" width="6.8" height="4.4" fill="#fff" stroke="{PWR}" stroke-width="0.35"/><text x="{a:.2f}" y="{b+0.9:.2f}" font-size="{FS}" font-weight="700" fill="{PWR}" text-anchor="middle">P{n}</text>')
# fire: suppression pull + gas cut-off, heat detector
s.rect(0.76, 0.92, D - 0.07, D, '#c8231b', '#c8231b', 0.2); s.text(1.05, 8.45, 'SP', FS, RED, weight=700); s.circ(0.83, 8.6, 0.08, '#c8231b', '#c8231b', 0.2); s.text(0.83, 8.6, 'K', 2.5, '#fff', weight=700); s.circ(-0.2, 7.55, 0.075, '#fff', RED, 0.3); s.text(-0.2, 7.55, 'H', FS, RED, weight=700)
s.text(XS - 0.27, 6.4, 'G gas line at 1.3 m', FS, GAS, weight=700, rot=-90)
s.scalebar(110, 187, 'PLAN 1:25 on A3 · metres')
a, b = s.P(XS - 0.06, KZ - 0.3); s.add(f'<text x="{a+2:.2f}" y="{b+2:.2f}" font-size="{FS}" fill="{GAS}" font-weight="600">from the LPG cage (5 × 19 kg)</text>')
# ---- hot-line elevation at 1:40
E = 25.0; EOX, EOY = 40, 276     # EOY = floor line
def Q(x, y): return (EOX + (X1 - x) * E, EOY - y * E)
def er(xa, xb, ya, yb, fill='none', stroke=INK, sw=0.3, dash=None):
    (a, b), (c, d) = Q(max(xa, xb), max(ya, yb)), Q(min(xa, xb), min(ya, yb))
    return f'<rect x="{a:.2f}" y="{b:.2f}" width="{c-a:.2f}" height="{d-b:.2f}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"' + (f' stroke-dasharray="{dash}"' if dash else '') + '/>'
def et(x, y, t, size=FS, fill=INK, anchor='middle', weight=500):
    a, b = Q(x, y); return f'<text x="{a:.2f}" y="{b+size*0.35:.2f}" font-size="{size}" fill="{fill}" text-anchor="{anchor}" font-weight="{weight}">{t}</text>'
def el(xa, ya, xb, yb, stroke=INK, sw=0.3, dash=None):
    a, b = Q(xa, ya); c, d = Q(xb, yb); return f'<line x1="{a:.2f}" y1="{b:.2f}" x2="{c:.2f}" y2="{d:.2f}" stroke="{stroke}" stroke-width="{sw}"' + (f' stroke-dasharray="{dash}"' if dash else '') + '/>'
def edim(x, ya, yb, t):
    a, b = Q(x, ya); _, d = Q(x, yb)
    return (f'<g stroke="{RED}" stroke-width="0.25"><line x1="{a:.2f}" y1="{b:.2f}" x2="{a:.2f}" y2="{d:.2f}"/><line x1="{a-1:.2f}" y1="{b:.2f}" x2="{a+1:.2f}" y2="{b:.2f}"/><line x1="{a-1:.2f}" y1="{d:.2f}" x2="{a+1:.2f}" y2="{d:.2f}"/></g>'
            f'<text x="{a-1.2:.2f}" y="{(b+d)/2+0.8:.2f}" font-size="{FS}" fill="{RED}" font-weight="600" text-anchor="end">{t}</text>')
ev = [f'<text x="{EOX}" y="{EOY - 3.0*E - 4:.2f}" font-size="{FB}" font-weight="700" fill="{INK}">Hot line elevation · back wall seen from inside · 1:40 on A3</text>',
      er(X0, X1, 0, KC, '#ffffff', 'none'), er(X0, X1, 0, 2.1, '#f2f4f2', 'none'), er(X0, X1, KC, 2.78, '#cdbfa8', 'none'), er(X0, X1, 2.78, 3.0, '#f4efe6', 'none'),
      et(1.6, 2.89, 'storage deck above', 2.5, MUT), el(X0, 0, X1, 0, INK, 0.6), er(X0 - 0.04, X0, 0, 3.0, WALL, WALL, 0.1), er(X1, X1 + 0.04, 0, 3.0, WALL, WALL, 0.1)]
for xa, xb, h, t in ((X0, -1.25, 0.8, 'wok range'), (-1.2, -0.6, 0.8, 'steamer'), (-0.55, 0.05, 0.9, 'fryer'), (0.1, 0.7, 0.85, 'stock')):
    ev += [er(xa, xb, 0, h, HOT, INK, 0.3), et((xa + xb) / 2, h - 0.2, t, FS, '#fff', weight=700)]
ev += [er(X0, 0.9, 2.05, 2.6, '#e6e3de', RED, 0.45), et(-0.8, 2.25, 'canopy hood 3.35 × 0.95 × 0.55', FS, RED, weight=600),
       er(-1.6, -1.1, 2.35, 2.75, '#f3e0dc', RED, 0.3, '1.2 0.6'), et(-1.68, 2.89, 'E1 duct out 0.40 × 0.40 at 2.35–2.75 m', 2.5, RED, 'end', 600),
       el(X0 + 0.05, 0.4, 0.62, 0.4, GAS, 0.5, '1.6 0.8'),
       el(-1.85, 0.8, -1.85, 1.12, BLU, 0.4), et(-1.85, 1.24, 'wok tap', FS, BLU), el(-0.9, 0.8, -0.9, 1.12, BLU, 0.4), et(-0.9, 1.24, 'steamer feed', FS, BLU),
       el(X0 + 0.06, 0.4, X0 + 0.06, 1.3, GAS, 0.6), et(X0 + 0.05, 1.72, 'gas in at 1.3 m', FS, GAS, 'end'),
       er(0.95, 1.75, 0, 2.1, '#fbf7ef', INK, 0.3), et(1.35, 1.1, 'rear exit', FS, MUT), et(1.35, 0.9, '0.80 × 2.10', FS, MUT), el(1.05, 1.0, 1.65, 1.0, INK, 0.5),
       er(0.76, 0.92, 1.3, 1.5, '#c8231b', '#c8231b', 0.1), er(0.73, 0.93, 0, 0.6, '#d6e2ef', BLU, 0.25), er(0.745, 0.915, 0.65, 1.2, '#e8a090', '#c8231b', 0.25), et(0.83, 1.28, '', FS),
       er(1.0, 1.6, KC, 2.78, '#ffffff', INK, 0.25), el(1.3, KC, 1.3, 1.25, INK, 0.3), et(1.34, 2.42, 'hoist hook', FS, MUT, 'start'),
       er(2.11, 2.43, 2.14, 2.64, '#fbe9dc', HWC, 0.3), et(2.27, 2.4, 'W', FS, HWC, weight=700), el(0.4, 1.3, 0.4, 1.2, BLU, 0.5), et(0.4, 1.42, 'pot filler', FS, BLU),
       er(1.8, X1, 0, 0.9, STEEL, INK, 0.3), et(2.12, 0.45, 'sink', FS, weight=700), er(2.1, X1, 1.45, 1.48, STEEL, INK, 0.2), er(2.1, X1, 1.85, 1.88, STEEL, INK, 0.2),
       er(X0, X0 + 0.3, 1.45, 1.48, STEEL, INK, 0.2), er(X0, X0 + 0.22, 0.97, 1.04, '#e6ecef', BLU, 0.25),
       edim(X1 + 0.3, 0, 0.8, '0.80'), edim(X1 + 0.62, 0, 2.05, '2.05'), edim(X1 + 0.94, 0, KC, '2.70'), et(0.84, 1.62, 'SP', FS, RED, weight=700)]
a, b = Q(X1, -0.25); ev.append(f'<text x="{a:.2f}" y="{b+1.5:.2f}" font-size="{FS}" fill="{MUT}">left wall</text>')
a, b = Q(X0, -0.25); ev.append(f'<text x="{a:.2f}" y="{b+1.5:.2f}" font-size="{FS}" fill="{MUT}" text-anchor="end">right wall (wok side)</text>')
s.add(''.join(ev))
# ---- legend
LX, LY = 168, 198
leg = [f'<text x="{LX}" y="{LY}" font-size="{FB}" font-weight="700" fill="{INK}">Legend: every symbol and letter on this sheet</text>']
items = [('line', RED, '2.2 1.2', 'canopy hood outline (above)'), ('line', EX, '1.4 0.8', 'exhaust duct, outside, 2.35–2.75 m'), ('line', GAS, None, 'gas line, copper'),
         ('line', GAS, '1.6 0.8', 'gas manifold at 0.40 m (dot = valve)'), ('box', GAS, 'S', 'S  solenoid shut-off valve'), ('circ', GAS, 'L', 'L  gas leak detector'),
         ('circ', BLU, 'HC', 'HC  water point, hot + cold'), ('circ', BLU, 'C', 'C  water point, cold only'), ('tri', BLU, None, 'drain point'),
         ('line', BLU, '1.2 0.7', 'drain line to the grease trap'), ('line', HWC, '1.4 0.8', 'hot water pipe from heater W'), ('line', '#3b8fd0', None, 'cold water main in (WM)'),
         ('boxf', BLU, 'GT', 'GT  grease trap (outside, back corner)'), ('circ', HWC, 'W', 'W  35 L storage water heater'),
         ('box', PWR, 'P1', 'P1 to P14  power point (services list); plain numbers 1 to 44 are BOQ items'), ('line', GRN, '1 0.6', 'MA  make-up air diffusers, ceiling'),
         ('circ', RED, 'H', 'H  heat detector'), ('circf', '#c8231b', 'K', 'K  Class K extinguisher (wok and fryer fires)'), ('sq', RED, None, 'SP  hood suppression pull + gas cut-off'),
         ('dark', INK, 'P', 'P1, P2  structural pillars on the right wall'), ('none', INK, None, 'E, F, CC, G, WC, SU, PF: services list')]
half = 11
for i, (kind, col, d, t) in enumerate(items):
    cx0 = LX + (i // half) * 66; y = LY + 6 + (i % half) * 5.6
    if kind == 'line': leg.append(f'<line x1="{cx0}" y1="{y-0.9}" x2="{cx0+9}" y2="{y-0.9}" stroke="{col}" stroke-width="0.6"' + (f' stroke-dasharray="{d}"' if d else '') + '/>')
    elif kind in ('box', 'boxf'): leg.append(f'<rect x="{cx0+2.3}" y="{y-3.1}" width="4.4" height="4.4" fill="{"#e6ecef" if kind == "boxf" else "#fff"}" stroke="{col}" stroke-width="0.35"/><text x="{cx0+4.5}" y="{y}" font-size="{FS if len(d) < 2 else 2.3}" font-weight="700" fill="{col}" text-anchor="middle">{d}</text>')
    elif kind in ('circ', 'circf'): leg.append(f'<circle cx="{cx0+4.5}" cy="{y-0.9}" r="3" fill="{"#c8231b" if kind == "circf" else "#fff"}" stroke="{col}" stroke-width="0.35"/><text x="{cx0+4.5}" y="{y}" font-size="{FS}" font-weight="700" fill="{"#fff" if kind == "circf" else col}" text-anchor="middle">{d}</text>')
    elif kind == 'sq': leg.append(f'<rect x="{cx0+3.5}" y="{y-2.3}" width="2" height="2.6" fill="{col}"/>')
    elif kind == 'dark': leg.append(f'<rect x="{cx0+2.5}" y="{y-3.0}" width="4" height="4" fill="#4a4038"/>')
    elif kind == 'tri': leg.append(f'<path d="M{cx0+3.5} {y-1.8} l2 0 l-1 1.7 z" fill="{col}"/>')
    leg.append(f'<text x="{cx0+12}" y="{y}" font-size="{FS}" fill="{INK}">{t}</text>')
s.add(''.join(leg))
# ---- services schedule (right column)
CX = 300
sv = [('E1', 'Duct through the back wall', '0.40 × 0.40 at 2.35–2.75 m', RED), ('E2', 'Duct along the wall, round the corner', '0.40 × 0.40, outside', RED),
      ('E3', 'ESP + carbon odour filter', '0.50 × 1.00 × 0.90, 2.05–2.95 m', RED), ('E4', 'Inline exhaust fan', 'Ø 0.44 · on backup', RED),
      ('E5', 'Side discharge, mesh + rain cowl', '0.40 × 0.40 at ~2.6 m', RED), ('F1', 'Fresh-air intake fan, back wall', '0.50 × 0.48 at 3.3 m', GRN),
      ('MA', 'Make-up air diffusers ×2, ceiling', '0.60 × 0.50 each · ~2.4 m/s', GRN), ('CC', 'Cooling coil in the make-up duct', '1.5 TR · 3rd condenser on the wall', GRN), ('G', 'LPG line, copper, from the cage', 'at 1.3 m, in at the back corner', GAS),
      ('S', 'Solenoid valve on the entry, outside', 'interlocked: fan + suppression', GAS), ('SP', 'Hood suppression pull + gas cut-off', 'at the rear exit, 1.3–1.5 m', RED), ('GT', 'Grease trap, outside back corner', '0.45 × 0.45', BLU), ('W', 'Storage water heater, 3 kW', '35 L · left wall over the sink', BLU), ('PF', 'Pot filler, cold, swing arm', 'over the stock range', BLU),
      ('WC', 'Water cabinet: pump, filter, softener', 'outside, 1.2–2.0 m · on backup', BLU), ('SU', 'Water sump, buried', '1,000 L · 1.3 × 1.0 × 0.8 · garden', BLU),
      ('P1', 'Reach-in fridge', '1-ph socket · on backup', PWR), ('P2', 'Under-counter freezer', '1-ph socket · on backup', PWR), ('P3', 'Two rice cookers', 'twin 1-ph socket', PWR),
      ('P4', 'Chilled mise-en-place rail', '1-ph socket · on backup', PWR), ('P5', 'Heat lamps over the pass', '1-ph, switched', PWR), ('P6', 'Dishwasher', '1-ph or 3-ph: confirm model', PWR),
      ('P7', 'Insect killer', '1-ph', PWR), ('P8', 'Hood-light switch', 'left wall, by panel P9', PWR), ('P9', 'Exhaust fan + ESP control panel', 'left wall over the DW · on backup', PWR),
      ('P10', 'Pass under-counter fridge', '1-ph socket · on backup', PWR), ('P11', 'Mixer-grinder', '1-ph socket, 16 A', PWR), ('P12', 'Water heater isolator', 'own 3 kW MCB', PWR), ('P13', 'Hand-wash heaters ×2', '1 kW each, 6 L', PWR), ('P14', 'Goods hoist over the hatch', '200 kg · 0.4 kW', PWR)]
rows = [(a, b, c, col) for a, b, c, col in sv]
o = [f'<text x="{CX-1.5}" y="31.5" font-size="{FB}" font-weight="700" fill="{INK}">Services list</text>', f'<rect x="{CX-1.5}" y="32.7" width="111" height="4.6" fill="{INK}"/>']
for c, t in zip((CX, CX + 9, CX + 64), ('TAG', 'ITEM', 'SIZE / NOTE')): o.append(f'<text x="{c}" y="36" font-size="{FS}" font-weight="700" fill="#fff">{t}</text>')
y = 40.6
for i, (tg, it, sz, col) in enumerate(rows):
    if i % 2 == 0: o.append(f'<rect x="{CX-1.5}" y="{y-3.1}" width="111" height="4.15" fill="#f3efe6"/>')
    o.append(f'<text x="{CX}" y="{y}" font-size="{FS}" font-weight="700" fill="{col}">{tg}</text><text x="{CX+9}" y="{y}" font-size="{FS}" fill="{INK}">{it}</text><text x="{CX+64}" y="{y}" font-size="{FS}" fill="{MUT}">{sz}</text>')
    y += 4.15
s.add(''.join(o))
nb, y2 = notes_block([('Exhaust + air', ['Allow about 4,000–5,000 m³/h for the whole hood (vendor to size);', 'about 8 m/s in the 0.40 × 0.40 duct. ESP + carbon filter before', 'the fan. No roof stack: apartment above, parking behind.', 'Hood overhang 0.20 m at the open end, 0.15 m over the wok range.', 'Make-up air about 80% of the exhaust through two low-velocity', 'diffusers (~2.4 m/s), cooled by a 1.5 TR coil, interlocked.']),
                      ('Gas', ['5 × 19 kg LPG (4 on the manifold + 1 full spare = 95 kg) in a', 'locked cage on the right strip. Typical load: wok 2 × 18, stock', '2 × 8, fryer 18, steamer 11 kW = about 80 kW connected, 55 kW', 'at once; 4 cylinders give about 60–75 kW in Goa: vendor to', 'confirm the burner ratings, add a vaporiser if they are higher.', 'A valve per appliance; solenoid shuts off with the fan or the', 'suppression; leak detector low on the right wall.']),
                      ('Water + drains', ['Cold: 1,000 L buried sump → pump, filter, softener cabinet', '(on backup) → kitchen. Hot: 35 L heater for the sink and pre-', 'rinse, 6 L heaters under both hand-wash basins, dishwasher', 'with its own booster. All kitchen drains to the grease trap,', 'then the grey-water line (never the biodigester).']),
                      ('Power', ['Shop supply: three-phase, about 15–20 kW. Backup 7.5 kVA', 'covers the fridges, rails, fan, ESP, lights and the water pump.', 'Not the ACs.'])], CX - 1.5, y + 4)
s.add(nb)
sheet2 = frame('Kitchen services and exhaust', 'For kitchen equipment, exhaust, gas, plumbing and electrical vendors · plan at 1:25 and elevation at 1:40 on A3', 2, ''.join(s.o))

PAGE = """<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"><title>Kitchen Sheets · Cabin East</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,600;12..96,700&family=IBM+Plex+Sans:wght@400;500;600;700&family=IBM+Plex+Mono:wght@500&display=swap">
<style>
/* Layout: two drafting-paper sheets, each with its own downloads and zoom; paper look in both themes (drawings for vendors) */
:root{--paper:#fbf7ef;--ink:#2a2420;--muted:#6a5d4e;--rule:#d9cbb3;--accent:#b23a1e;--chip:#fffdf8;
  --display:'Bricolage Grotesque','Avenir Next','Segoe UI',sans-serif;--body:'IBM Plex Sans','Helvetica Neue',Arial,sans-serif;--mono:'IBM Plex Mono',ui-monospace,Menlo,monospace;color-scheme:light}
body{background:var(--paper);color:var(--ink);font-family:var(--body);margin:0}
.wrap{max-width:1280px;margin:0 auto;padding-inline:16px;padding-block:22px 40px;display:flex;flex-direction:column;gap:16px}
.eyebrow{font:500 11px/1.4 var(--mono);letter-spacing:.08em;text-transform:uppercase;color:var(--accent);margin:0}
h1{font:700 clamp(26px,4vw,38px)/1.05 var(--display);margin:4px 0 6px;text-wrap:balance}
h2{font:700 clamp(19px,2.6vw,24px)/1.15 var(--display);margin:18px 0 2px}
.lede,.sub{margin:0;max-width:78ch;color:var(--muted);line-height:1.55}
.bar{display:flex;flex-wrap:wrap;gap:8px;align-items:center}
.bar button,.bar a{appearance:none;font:600 13px/1 var(--body);color:var(--ink);background:var(--chip);border:1px solid var(--rule);border-radius:8px;padding:9px 12px;cursor:pointer;text-decoration:none}
.bar a.pri{background:var(--ink);color:var(--paper);border-color:var(--ink)}
.bar button[aria-pressed="true"]{background:var(--accent);color:#fff;border-color:var(--accent)}
.bar button:focus-visible,.bar a:focus-visible{outline:2px solid var(--accent);outline-offset:2px}
.sheet{overflow:auto;border:1px solid var(--rule);background:var(--paper);max-height:84vh}
.sheet svg{display:block;width:100%;height:auto}
.sheet[data-z="2"] svg{width:200%}.sheet[data-z="3"] svg{width:300%}
</style></head><body>
<div class="wrap">
<header>
<p class="eyebrow">Cabin East · Betalbatim · for kitchen vendors</p>
<h1>Kitchen drawings: equipment, services and exhaust</h1>
<p class="lede">Two A3 sheets drawn to true scale: print at 100% (no “fit to page”) and the plans measure 1:25, the elevation 1:40. Sheet 1 is for the equipment fabricator; sheet 2 is for the exhaust, gas, plumbing and electrical vendors. Prices are asked against the <a href="boq.html">bill of quantities (BOQ)</a>, which numbers every line and gives its unit and quantity.</p>
</header>
<div class="bar"><a class="pri" href="plans/kitchen-sheets-A3.pdf" target="_blank" rel="noopener">Both sheets · 2-page PDF (A3, vector)</a><a href="boq.html">BOQ (Excel, PDF)</a><a href="boq-goa.html">Equipment and exhaust BOQ (feet, SWG, CFM)</a><a href="boq-drawing.html">Drawing + BOQ in mm (A3 PDF)</a><a href="plan.html">Whole floor plan</a><a href="kitchen-3d.html">Kitchen in 3D, exact sizes</a><a href="./">3D model</a></div>
@@SHEETS@@
</div>
<script>
document.querySelectorAll('.sheet').forEach(sh=>{const bs=[...document.querySelectorAll('button[data-for="'+sh.id+'"]')];
bs.forEach(b=>b.addEventListener('click',()=>{sh.dataset.z=b.dataset.z;bs.forEach(x=>x.setAttribute('aria-pressed',String(x===b)));}));});
</script>
</body></html>
"""
def page_block(n, slug, title, sub, svg):
    z = ''.join(f'<button data-for="s{n}" data-z="{k}" aria-pressed="{str(k == 1).lower()}">{l}</button>' for k, l in ((1, 'Fit'), (2, '2×'), (3, '3×')))
    return (f'<section><h2>Sheet {n} · {title}</h2><p class="sub">{sub}</p>'
            f'<div class="bar" role="group" aria-label="Sheet {n} zoom and downloads">{z}<a class="pri" href="plans/kitchen-sheet-{slug}.pdf" target="_blank" rel="noopener">PDF</a>'
            f'<a href="plans/kitchen-sheet-{slug}.png" target="_blank" rel="noopener">PNG 300 dpi</a></div>'
            f'<div class="sheet" id="s{n}" data-z="1">{svg}</div></section>')

def main():
    d = sys.argv[1]; os.makedirs(d, exist_ok=True)
    open(d + '/kitchen-sheet-1.svg', 'w').write(sheet1); open(d + '/kitchen-sheet-2.svg', 'w').write(sheet2)
    print('sheet 1 notes end', round(y, 1), '| sheet 2 notes end', round(y2, 1))
    if '--page' in sys.argv:
        blocks = page_block(1, '1-equipment', 'Equipment layout', 'Plan 1:25 with every item named and sized, the key dimensions and the equipment list.', sheet1) + \
                 page_block(2, '2-services', 'Services and exhaust', 'Plan 1:25 with the exhaust run, gas, water, drains and power points; hot-line elevation 1:40; legend, services list and vendor notes.', sheet2)
        open('kitchen.html', 'w').write(PAGE.replace('@@SHEETS@@', blocks)); print('kitchen.html written')

if __name__ == '__main__':
    main()
