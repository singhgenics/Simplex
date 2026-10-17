"""One A3 portrait PDF for the kitchen equipment and exhaust: the 1:25 plan on top (every size in mm) and the BOQ below it (sizes in mm only).
The plan is cropped from sheet 1 (plans/kitchen-sheet-1-equipment.svg), so rebuild the sheets first; every metre label is converted to mm here.
The BOQ lines are the 44 equipment and exhaust lines of the Goa BOQ (tools/boq_goa.py), with the metric wording from tools/boq.py.
Usage: python3 tools/boq_drawing.py  ->  boq-drawing.html   (PDF: print it from Chrome headless on A3 portrait, see tools/README.md)
"""
import re, html, boq, boq_goa

def mm_text(m):
    """Inside one <text>: 0.60 -> 600, 1.45 m -> 1,450 mm. Integers (already mm) are left alone."""
    def f(x):
        v = round(float(x.group(1)) * 1000)
        return f'{v:,}' + ('mm' if x.group(2) else '') if False else f'{v:,}' + (' mm' if x.group(2) else '')
    return m.group(1) + re.sub(r'(\d+\.\d+)( m\b)?', f, m.group(2)) + m.group(3)

import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kitchen_sheets as K
from kitchen_sheets import X0, X1, D, T, KZ, XS, INK, MUT, RED, BLU, GAS, GRN, STEEL, HOT, FS, FT, FB

W_MM, H_MM = 291, 226                     # drawing size on the page, mm, at 1:25 (40 mm per metre)
def drawing_svg():
    """The 1:25 plan: kitchen with every BOQ line numbered by a balloon, names on or beside the parts, and the exhaust run outside. All sizes in mm."""
    s = K.Sheet(0, 0, 3.15, 10.35)        # left wall outside face at x = 20 mm; page y = (10.35 - z) * 40
    s.shell()
    def bub(sl, bx, by, ix=None, iz=None, col=INK):
        """Number balloon matching the Sl column of the BOQ. (bx, by) is the balloon centre on the page in mm; (ix, iz) is the item's model position, joined by a leader."""
        if ix is not None:
            a, b = s.P(ix, iz); s.add(f'<line x1="{a:.2f}" y1="{b:.2f}" x2="{bx:.2f}" y2="{by:.2f}" stroke="{col}" stroke-width="0.2"/><circle cx="{a:.2f}" cy="{b:.2f}" r="0.55" fill="{col}"/>')
        s.add(f'<rect x="{bx-3.9:.2f}" y="{by-1.9:.2f}" width="7.8" height="3.8" rx="1.9" fill="#fff" stroke="{col}" stroke-width="0.3"/><text x="{bx:.2f}" y="{by+0.9:.2f}" font-size="2.5" font-weight="700" fill="{col}" text-anchor="middle">{sl}</text>')
    def box(xa, xb, za, zb, lines_, fill=STEEL, tc=INK, dz=0.0):
        s.rect(xa, xb, za, zb, fill, INK, 0.3)
        s.lines((xa + xb) / 2, (za + zb) / 2 + dz, lines_, 2.5, tc)
    # ---- hot line (back wall), floor channel
    s.rect(-2.4, 0.75, 7.92, 8.0, '#b9c0c5', '#6d7276', 0.15)
    for sl, xa, xb, z0, name, size in (('2.01', X0, -1.25, 8.0, 'Wok range', '1,200 × 800 × 800'), ('2.02', -1.2, -0.6, 8.1, 'Steamer', '600 × 700 × 800'), ('2.03', -0.55, 0.05, 8.1, 'Fryer', '600 × 700 × 900'), ('2.04', 0.1, 0.7, 8.1, 'Stock range', '600 × 700 × 850')):
        box(xa, xb, z0, D, [(name, 700), (size, 500)], HOT, '#fff', dz=-0.05)
        a, b = s.P((xa + xb) / 2, D); bub(sl, a, b + 4)
    s.text(-0.85, 7.96, '1.15  floor channel drain 3,150 × 80', 2.5, INK, weight=600)
    # ---- front-wall benches, pass, hand-wash (names; balloons below)
    box(-2.2, -1.4, KZ + 0.115, 7.05, [('Non-veg prep', 700), ('800 × 650 × 900', 500)], dz=0.22); a, b = s.P(-1.8, 7.05); bub('1.01', a - 8, b - 4)
    box(-1.4, -0.6, KZ + 0.115, 7.05, [], dz=0); a, b = s.P(-1.0, 7.05); bub('1.02', a + 4, b - 4)
    box(-0.6, 0.05, KZ + 0.115, 7.05, [], dz=0); a, b = s.P(-0.275, 7.05); bub('1.03', a - 8, b - 4)
    s.rect(0.92, 1.2, KZ + 0.115, 6.8, STEEL, INK, 0.3); s.text(1.06, 6.62, 'HW', 2.5, weight=700)
    s.rect(X0, X0 + 0.25, KZ + 0.115, 6.65, STEEL, INK, 0.3); s.text(X0 + 0.125, 6.52, 'HW', 2.5, weight=700)
    # ---- left wall: reach-in, dish line
    box(1.7, X1, 6.45, 7.4, [('Reach-in', 700), ('950 × 750 × 2,000', 500)]); bub('2.05', 43, s.P(0, 7.3)[1])
    box(1.8, X1, 7.4, 8.0, [('Dishwasher', 700)])
    box(1.8, X1, 8.0, D, [('Dish sink', 700), ('800 × 650 × 900', 500)]); bub('1.04', 36, 68)
    bub('2.12', 52, 68)                                # 35 L heater on the wall above the sink
    bub('2.08', 35, 97); bub('3.09', 51, 97)           # dishwasher; fan + ESP control panel on the wall above it
    bub('2.18', 36, 114); bub('1.05', 50, 114)         # bamboo stacks and the shelves over the dish line
    s.rect(2.1, X1, 7.4, D, 'none', MUT, 0.2, '1 0.8')
    # ---- right wall: veg sink, rails, pillar
    box(X0, X0 + 0.45, 7.12, 7.6, []); bub('1.06', 213, 114)
    s.rect(X0, X0 + 0.23, 6.65, 6.95, K.WALL, K.WALL, 0.2); s.text(X0 + 0.115, 6.8, 'P2', 2.5, '#fff', weight=700)
    s.rect(X0, X0 + 0.22, 7.62, 8.06, '#e6ecef', BLU, 0.3)
    s.line(X0 + 0.05, 8.13, X0 + 0.05, 8.6, BLU, 0.9, '1.4 0.5')
    s.rect(X0, X0 + 0.3, 7.15, 8.05, 'none', MUT, 0.2, '1 0.8')
    bub('1.09', 212, 88, X0 + 0.05, 8.45); bub('1.08', 208, 101, X0 + 0.11, 7.84); bub('1.07', 199, 107, X0 + 0.2, 7.3)
    # ---- small kit on the benches and walls (balloons in a row below the pass wall)
    for z in (6.56, 6.9): s.circ(-0.75, z, 0.13, '#e9e9e9', '#6d7276', 0.25)
    s.rect(-2.18, -1.42, 6.42, 6.68, '#dff0f6', BLU, 0.3); s.rect(-0.6, 0.05, 6.93, 7.05, '#e6ecef', BLU, 0.25)
    s.rect(-2.12, -1.84, 6.5, 6.76, 'none', '#8f6a4a', 0.25, '0.8 0.6')
    for xa, xb in ((-1.84, -1.44), (-1.35, -0.95)): s.line(xa, KZ + 0.13, xb, KZ + 0.13, INK, 0.8)
    s.circ(-2.27, 7.27, 0.085, '#cfe0bf', GRN, 0.3, '0.8 0.6'); s.circ(0.83, 8.62, 0.1, '#d6e2ef', BLU, 0.3); s.circ(0.83, 8.71, 0.07, '#c8231b', '#c8231b', 0.2)
    s.circ(2.27, 8.62, 0.16, 'none', BLU, 0.3, '1.2 0.8')
    s.rect(1.0, 1.6, 7.45, 8.25, 'none', BLU, 0.3, '1.6 0.9')
    s.lines(-1.12, 6.78, [('Veg prep', 700), ('800×650×900', 500)], 2.5, INK)
    s.lines(-0.275, 6.62, [('Pass', 700), ('650×650×900', 500)], 2.5, INK)
    row = 184.0
    for sl, px, ix, iz in (('2.13', 74, 1.06, 6.5), ('2.14', 92, 0.5, KZ + 0.05), ('2.06', 124, -0.2, 6.55), ('2.15', 133, -0.28, 6.45), ('1.12', 142, -0.3, KZ + 0.05), ('1.11', 151, -0.3, 6.99),
                           ('2.11', 160, -0.72, 6.5), ('2.09', 169, -0.75, 6.73), ('2.10', 178, -1.0, 6.6), ('2.07', 187, -1.15, 6.95), ('1.13', 196, -1.64, KZ + 0.13), ('1.10', 205, -1.8, 6.55), ('1.14', 214, -2.0, 6.7)):
        bub(sl, px, row, ix, iz)
    bub('2.16', 74, 91); s.text(1.3, 7.95, 'Hatch 600 × 800', 2.5, BLU, weight=600); bub('1.17', 74, 109)
    # ---- hood, make-up air
    s.rect(X0, 0.9, 7.85, D - 0.02, 'none', RED, 0.45, '2.2 1.2')
    s.lines(0.5, 7.5, [('Canopy hood above', 600), ('3,350 × 950 × 550', 500)], 2.5, RED)
    a, b = s.P(0.5, 7.85); bub('3.01', a, b + 4, col=RED)
    s.rect(-2.4, -1.8, 7.0, 7.5, 'none', GRN, 0.35, '1 0.6'); s.rect(-0.95, -0.35, 7.1, 7.6, 'none', GRN, 0.35, '1 0.6')
    s.lines(-0.65, 7.38, [('Make-up air', 600), ('diffuser 600 × 500', 500)], 2.5, GRN)
    bub('3.07', 204, 128, col=GRN); a, b = s.P(-0.65, 7.6); bub('3.07', a, b + 3, col=GRN)
    # ---- exhaust run outside (duct at 2,350 to 2,750 mm high)
    EX = '#c4442a'
    s.rect(-1.6, -1.1, 8.4, D, 'none', RED, 0.35, '1.4 0.8')
    for xa, xb, za, zb in ((-1.6, -1.1, D, D + T), (XS - 0.45, -1.1, D + T, D + T + 0.4), (XS - 0.45, XS - 0.05, D - 0.35, D + T + 0.4)): s.rect(xa, xb, za, zb, '#f3e0dc', EX, 0.3, '1.4 0.8')
    s.text(-2.0, D + T + 0.2, 'Exhaust duct 400 × 400 at 2,350 to 2,750', 2.5, RED, weight=600); bub('3.02', 244, 65, col=RED)
    s.rect(XS - 0.5, XS + 0.02, D - 1.35, D - 0.35, '#e8c9c2', RED, 0.4); s.text(XS - 0.24, D - 0.85, 'ESP + carbon filter', 2.5, RED, weight=600, rot=-90)
    bub('3.04', 266, 96, XS - 0.5, D - 0.85, RED)
    s.circ(XS - 0.25, D - 1.55, 0.18, '#f3e0dc', EX, 0.3); s.text(XS - 0.25, D - 1.55, 'Fan', 2.5, RED, weight=600)
    bub('3.05', 266, 124, XS - 0.43, D - 1.55, RED)
    s.rect(XS - 0.5, XS - 0.05, D - 1.95, D - 1.75, '#f3e0dc', EX, 0.3, '1.4 0.8')
    a, b = s.P(XS - 0.5, D - 1.85); s.add(f'<path d="M{a:.2f} {b:.2f} l6 0 m0 0 l-1.8 -1.2 m1.8 1.2 l-1.8 1.2" stroke="{RED}" stroke-width="0.45" fill="none"/>')
    bub('3.03', 275, b + 1, XS - 0.5, D - 1.85, RED); s.lines(a + 22, b + 8, [('Discharge', 600), ('400 × 400', 500), ('at 2,600', 500)], 2.5, RED)
    s.rect(1.9, 2.4, D + T, D + T + 0.3, '#e1eadc', GRN, 0.3); s.lines(2.15, D + T + 0.15, [('Fresh-air fan', 600), ('500 × 480', 500)], 2.5, GRN); bub('3.06', 40, 36, col=GRN)
    # ---- dimensions in mm
    for xa, xb, t in ((X0, -1.25, '1,200'), (-1.2, -0.6, '600'), (-0.55, 0.05, '600'), (0.1, 0.7, '600'), (0.95, 1.75, 'rear exit 800')): s.hdim(xa, xb, D + T + 0.58, t)
    s.hdim(X1, X0, D + T + 0.82, '4,900 inside')
    for xa, xb, t in ((0.1, 0.9, 'door 800'), (0.92, 1.2, '280')): s.hdim(xa, xb, KZ - 0.18, t)
    s.vdim(X1 + T + 0.3, KZ + 0.1, D, '2,400 inside')
    for za, zb, t in ((6.45, 7.4, '950'), (7.4, 8.0, '600'), (8.0, D, '800')): s.vdim(X1 + T + 0.12, za, zb, t)
    s.vdim(-0.3, 7.05, 8.1, "cooks' aisle 1,050"); s.vdim(-1.3, 7.05, 8.0, '950 at the wok range')
    # ---- key to the small items, scale bar
    ky = 198.0
    key = [('1.05', 'Dish-line wall shelves, one slatted'), ('1.06', 'Veg and herb wash sink 450 × 500'), ('1.07', 'Sauce and oil wall shelf'), ('1.08', 'Wok seasoning rail'), ('1.09', 'Wok tool rail'), ('1.10', 'Mise-en-place rail'), ('1.11', 'Dip and garnish rail'),
           ('1.12', 'Ticket rail over the pass'), ('1.13', 'Knife strips (2)'), ('1.14', 'Cutting-board rack'), ('1.17', 'Ceiling hatch and ladder'), ('2.06', 'Pass under-counter fridge'), ('2.07', 'Under-counter freezer (veg bench)'),
           ('2.09', 'Rice cookers (2)'), ('2.10', 'Mixer-grinder, on the shelf'), ('2.11', 'Kitchen torch'), ('2.12', '35 L water heater, on the wall'), ('2.13', 'Hand-wash heaters 6 L (2)'), ('2.14', 'Insect killer'),
           ('2.15', 'Heat lamps over the pass (2)'), ('2.16', 'Goods hoist 200 kg'), ('2.18', 'Bamboo steamer stacks'), ('3.01', 'Canopy hood'), ('3.02', 'Exhaust duct'), ('3.03', 'Discharge elbow'),
           ('3.04', 'ESP + carbon filter'), ('3.05', 'Exhaust fan'), ('3.06', 'Fresh-air intake fan'), ('3.07', 'Make-up air diffusers (2)'), ('3.09', 'Fan + ESP control panel')]
    s.add(f'<text x="12" y="{ky-2:.1f}" font-size="2.9" font-weight="700" fill="{INK}">KEY · the numbers are the Sl column of the BOQ below · 1.xx steel fabrication · 2.xx equipment · 3.xx hood and exhaust · big items are named on the plan</text>')
    cols = 3; per = (len(key) + cols - 1) // cols
    for i, (n_, t) in enumerate(key):
        cx = 12 + (i // per) * 92; cy = ky + 2.4 + (i % per) * 3.5
        s.add(f'<text x="{cx:.1f}" y="{cy:.1f}" font-size="2.5" font-weight="700" fill="{INK}">{n_}</text><text x="{cx+8:.1f}" y="{cy:.1f}" font-size="2.5" fill="{INK}">{t}</text>')
    ny = ky + 2.4 + per * 3.5 + 2.2
    s.add(f'<text x="12" y="{ny:.1f}" font-size="2.5" fill="{MUT}">Not drawn: 1.16 storage-deck racking, 2.17 smallware (chef\'s list), 3.08 the cooling-coil condenser (on the right outside wall at about 3,000 mm high, nearer the shopfront, sheet 2),</text>')
    s.add(f'<text x="12" y="{ny+3.2:.1f}" font-size="2.5" fill="{MUT}">1.xx rails and shelves are on the walls at the heights in the BOQ. Dashed lines: hood, duct, make-up air diffusers and ceiling hatch are above the floor.</text>')
    bx_, by_ = 12.0, ny + 8.5
    s.add(f'<rect x="{bx_}" y="{by_}" width="40" height="1.6" fill="{INK}"/><rect x="{bx_+40}" y="{by_}" width="40" height="1.6" fill="none" stroke="{INK}" stroke-width="0.2"/>'
          f'<text x="{bx_}" y="{by_+5}" font-size="2.5" fill="{INK}">0</text><text x="{bx_+40}" y="{by_+5}" font-size="2.5" text-anchor="middle" fill="{INK}">1000</text><text x="{bx_+80}" y="{by_+5}" font-size="2.5" text-anchor="middle" fill="{INK}">2000</text>'
          f'<text x="{bx_+86}" y="{by_+1.8}" font-size="2.9" font-weight="700" fill="{INK}">PLAN 1:25 on A3, all dimensions in mm</text>')
    H = by_ + 8
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{W_MM}mm" height="{H-14:.1f}mm" viewBox="0 14 {W_MM} {H-14:.1f}" font-family="\'IBM Plex Sans\', Helvetica, Arial, sans-serif"><rect x="0" y="14" width="{W_MM}" height="{H-14:.1f}" fill="#fbf7ef"/>{"".join(s.o)}</svg>'

def metres_to_mm(t):
    """'at 2.35 to 2.75 m' -> 'at 2,350 to 2,750 mm'; '1.45 m' -> '1,450 mm'. Thickness already in mm ('1.2 mm') is left alone."""
    t = re.sub(r'(\d+\.\d+) to (\d+\.\d+) m\b(?!m)', lambda m: f'{round(float(m.group(1))*1000):,} to {round(float(m.group(2))*1000):,} mm', t)
    return re.sub(r'(\d+\.\d+) m\b(?!m)', lambda m: f'{round(float(m.group(1))*1000):,} mm', t)

def lines():
    by = {i[0]: i for sec in boq.S for i in sec[3]}
    for sl, title, note, items in boq_goa.GOA:
        yield ('sec', sl, title, note)
        for k, r in enumerate(items, 1):
            no, item, size, spec, unit, qty, ref = by[r['no']]
            item = r['item'] if r['no'] in ('A.16', 'A.17', 'B.16', 'B.17', 'B.18', 'B.19', 'B.20', 'E.03') else item
            yield ('item', f'{sl}.{k:02d}', item, size, spec, unit, qty, no)

def page():
    esc = html.escape; body = []; n = 0
    for r in lines():
        if r[0] == 'sec':
            note = r[3].replace('Exhaust about 2,400 to 3,000 CFM (4,000 to 5,000 m³/h)', 'Exhaust 4,000 to 5,000 m³/h').replace('Vendor states the static pressure the fan is selected for.', 'Vendor states the static pressure the fan is selected for.')
            note = metres_to_mm(note)
            note = re.sub(r"Worktops 18 SWG \(1\.2 mm\), bodies and shelves 19 SWG \(1\.0 mm\), legs 1½\" \(38 mm\) tube", 'Worktops 1.2 mm or thicker, bodies and shelves 1.0 mm, legs 38 mm tube', note)
            body.append(f'<tr class="sec"><th>{r[1]}</th><th colspan="9">{esc(r[2])}<small>{esc(note)}</small></th></tr>')
        else:
            _, sl, item, size, spec, unit, qty, ref = r; n += 1
            spec = metres_to_mm(re.sub(r'\s*\(about \d+ sq ft with bends\)', '', spec))
            if unit == 'm': unit, qty = 'mm', round(qty * 1000)
            q = f'{qty:,}' if isinstance(qty, int) else f'{qty:g}'
            body.append(f'<tr><td class="no">{sl}</td><td><b>{esc(item)}</b></td><td class="sz">{esc(size)}</td><td>{esc(spec)}</td><td>{unit}</td><td class="n">{q}</td><td class="blank"></td><td class="blank"></td><td class="blank"></td><td class="ref">{ref}</td></tr>')
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><title>Kitchen drawing and BOQ in mm · Betalbatim Pub</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,700&family=IBM+Plex+Sans:wght@400;500;600;700&family=IBM+Plex+Mono:wght@500&display=swap">
<style>
/* Layout: A3 portrait. The 1:25 plan fills the top of page 1 at true scale; the BOQ table starts below it and continues on page 2 */
@page{{size:297mm 420mm;margin:0}}
:root{{--paper:#fbf7ef;--ink:#2a2420;--muted:#6a5d4e;--rule:#d9cbb3;--accent:#b23a1e;--mono:'IBM Plex Mono',ui-monospace,Menlo,monospace;--body:'IBM Plex Sans','Helvetica Neue',Arial,sans-serif;--display:'Bricolage Grotesque','Segoe UI',sans-serif}}
html,body{{margin:0;background:var(--paper);color:var(--ink);font-family:var(--body)}}
.sheet{{width:291mm;margin:0 auto;padding:4mm 0 6mm}}
.hd{{display:flex;justify-content:space-between;align-items:flex-end;height:18mm;border-bottom:.35mm solid var(--ink);margin-bottom:1mm}}
.hd h1{{font:700 7mm/1 var(--display);margin:0}} .hd p{{margin:1mm 0 0;font-size:2.6mm;color:var(--muted)}} .hd .r{{text-align:right;font-size:2.6mm;color:var(--muted)}}
svg{{display:block}}
h2{{font:700 4.4mm/1.2 var(--display);margin:3mm 0 1.5mm}}
table{{border-collapse:collapse;width:100%;font-size:2.7mm;line-height:1.3}}
th,td{{padding:.9mm 1.4mm;border-top:.2mm solid var(--rule);vertical-align:top;text-align:left}}
thead th{{background:var(--ink);color:var(--paper);font:600 2.5mm var(--mono);border-top:0;white-space:nowrap}}
tr.sec th{{background:#efe6d3;font:700 2.9mm var(--body)}} tr.sec small{{display:block;font:400 2.4mm var(--body);color:var(--muted)}}
td.no{{font:600 2.5mm var(--mono);white-space:nowrap}} td.sz{{font:500 2.5mm var(--mono)}} td.n{{text-align:right;font-family:var(--mono)}} td.ref{{color:var(--muted);font-size:2.4mm}}
td.blank{{background:#fffdf0;width:11mm}} thead{{display:table-header-group}} tr{{break-inside:avoid}}
.foot{{font-size:2.6mm;color:var(--muted);margin-top:2mm}}
@media screen{{html{{background:#eee}} .sheet{{background:var(--paper);padding:4mm 3mm 6mm;width:297mm;margin:4mm auto;box-shadow:0 1px 8px rgba(0,0,0,.2)}}}}
</style></head><body><div class="sheet">
<div class="hd"><div><h1>Kitchen equipment and exhaust</h1><p>Drawing at 1:25 on A3 (print at 100%), then the BOQ. All sizes in mm. For kitchen equipment and exhaust vendors · Shop 4, Tulip Residency, Gandaulim, South Goa</p></div><div class="r">Betalbatim pub · Simplex · Concept 27<br>singhgenics.github.io/Simplex/boq-drawing.html</div></div>
{drawing_svg()}
<h2>BOQ: kitchen equipment and exhaust ({n} lines)</h2>
<table><thead><tr><th>Sl</th><th>Item / type</th><th>Size W × D × H (mm)</th><th>Capacity, rating, specification</th><th>Unit</th><th>Qty</th><th>Rate ₹</th><th>Amount ₹</th><th>Make / model</th><th>Main BOQ</th></tr></thead><tbody>{''.join(body)}</tbody></table>
<p class="foot">Quantities and sizes are the space available, from the model; the vendor measures on site and states the make, model, kW or litres, steel grade and thickness, price ex-GST, delivery, installation, lead time, warranty and who services it in Goa. Duct length is an estimate. Gas, plumbing, electrical, civil and fire work are in the main BOQ (boq.html). Concept drawings for briefing suppliers, not construction drawings.</p>
</div></body></html>
'''

if __name__ == '__main__':
    open('boq-drawing.html', 'w').write(page()); print('boq-drawing.html written')
