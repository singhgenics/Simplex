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
        return f'{v:,}' + (' mm' if x.group(2) else '')
    return m.group(1) + re.sub(r'(\d+\.\d+)( m\b)?', f, m.group(2)) + m.group(3)

import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kitchen_sheets as K
from kitchen_sheets import X0, X1, D, T, KZ, XS, INK, MUT, RED, BLU, GAS, GRN, STEEL, HOT, FS, FT, FB

W_MM, H_MM = 291, 226                     # drawing size on the page, mm, at 1:25 (40 mm per metre)
def drawing_svg():
    """The 1:25 plan: kitchen and the exhaust run outside. Every item is named on the drawing itself (inside the box, or on a leader to a label). All sizes in mm."""
    s = K.Sheet(0, 0, 3.15, 10.35)        # left wall outside face at x = 20 mm; page y = (10.35 - z) * 40
    s.shell()
    N = {r[7]: r[1] for r in lines() if r[0] == 'item'}      # running BOQ number (1 to 44) of each item
    def box(xa, xb, za, zb, lines_, fill=STEEL, tc=INK, dz=0.0):
        s.rect(xa, xb, za, zb, fill, INK, 0.3)
        if lines_: s.lines((xa + xb) / 2, (za + zb) / 2 + dz, lines_, 2.5, tc)
    # ---- hot line (back wall) and floor channel
    s.rect(-2.4, 0.75, 7.92, 8.0, '#b9c0c5', '#6d7276', 0.15)
    for xa, xb, z0, name, size in ((X0, -1.25, 8.0, f"{N['B.01']}|Wok range", '1,200 × 800 × 800'), (-1.2, -0.6, 8.1, f"{N['B.02']}|Dim sum|steamer", '600 × 700 × 800'), (-0.55, 0.05, 8.1, f"{N['B.03']}|Fryer", '600 × 700 × 900'), (0.1, 0.7, 8.1, f"{N['B.04']}|Stock range", '600 × 700 × 850')):
        parts = name.split('|'); box(xa, xb, z0, D, [(parts[0], 800)] + [(n_, 700) for n_ in parts[1:]] + [(size, 500)], HOT, '#fff', dz=0.0)
    s.text(-0.85, 7.96, f"{N['A.15']}  Floor channel drain 3,150 × 80", 2.5, INK, weight=600)
    # ---- front-wall benches, pass, hand-wash
    box(-2.2, -1.4, KZ + 0.115, 7.05, [])
    box(-1.4, -0.6, KZ + 0.115, 7.05, [])
    box(-0.6, 0.05, KZ + 0.115, 7.05, [])
    s.rect(0.92, 1.2, KZ + 0.115, 6.8, STEEL, INK, 0.3); s.rect(X0, X0 + 0.25, KZ + 0.115, 6.65, STEEL, INK, 0.3)
    # ---- left wall: reach-in, dish line (what is in and above each box is written inside it)
    box(1.7, X1, 6.45, 7.4, [(N['B.05'], 800), ('Reach-in', 700), ('950 × 750 × 2,000', 500)])
    box(1.8, X1, 7.4, 8.0, [(N['B.08'], 800), ('Dishwasher', 700), ('600×650×900', 500), (f"Above: panel {N['E.03']},", 400), (f"baskets {N['B.23']}", 400)])
    box(1.8, X1, 8.0, D, [(N['A.04'], 800), ('Dish sink', 700), ('800×650×900', 500), (f"Above: shelves {N['A.05']},", 400), (f"heater {N['B.12']}", 400)])
    s.rect(2.1, X1, 7.4, D, 'none', MUT, 0.2, '1 0.8')
    # ---- right wall: veg sink, rails, pillar
    box(X0, X0 + 0.45, 7.12, 7.6, []); s.lines(X0 + 0.23, 7.5, [(N['A.06'], 800), ('Veg sink', 700)], 2.5, INK)
    s.rect(X0, X0 + 0.23, 6.65, 6.95, K.WALL, K.WALL, 0.2); s.text(X0 + 0.115, 6.8, 'P2', 2.5, '#fff', weight=700)
    s.rect(X0, X0 + 0.22, 7.62, 8.06, '#e6ecef', BLU, 0.3)
    s.line(X0 + 0.05, 8.13, X0 + 0.05, 8.6, BLU, 0.9, '1.4 0.5')
    s.rect(X0, X0 + 0.3, 7.15, 8.05, 'none', MUT, 0.2, '1 0.8')
    s.text(X0 + 0.1, 8.1, f"{N['A.09']}  Wok tool rail", 2.5, BLU, anchor='end', weight=600); s.text(X0 + 0.28, 7.78, f"{N['A.08']}  Seasoning rail", 2.5, BLU, anchor='end', weight=600); s.text(X0 + 0.34, 7.68, f"{N['A.07']}  Sauce + oil shelf", 2.5, BLU, anchor='end', weight=600)
    # ---- small kit on the benches and walls
    for z in (6.56, 6.9): s.circ(-0.75, z, 0.13, '#e9e9e9', '#6d7276', 0.25)
    s.rect(-2.18, -1.42, 6.42, 6.68, '#dff0f6', BLU, 0.3); s.rect(-0.6, 0.05, 6.93, 7.05, '#e6ecef', BLU, 0.25)
    s.rect(-2.12, -1.84, 6.5, 6.76, 'none', '#8f6a4a', 0.25, '0.8 0.6')
    for xa, xb in ((-1.84, -1.44), (-1.35, -0.95)): s.line(xa, KZ + 0.13, xb, KZ + 0.13, INK, 0.8)
    s.circ(-2.27, 7.27, 0.085, '#cfe0bf', GRN, 0.3, '0.8 0.6'); s.circ(0.83, 8.62, 0.1, '#d6e2ef', BLU, 0.3); s.circ(0.83, 8.71, 0.07, '#c8231b', '#c8231b', 0.2)
    s.circ(2.27, 8.62, 0.16, 'none', BLU, 0.3, '1.2 0.8')
    s.rect(1.0, 1.6, 7.45, 8.25, 'none', BLU, 0.3, '1.6 0.9'); s.lines(1.3, 7.85, [(N['A.20'], 800), ('Ceiling hatch', 600), ('600 × 800', 500), ('with ladder', 500), (N['B.21'], 800), ('Goods hoist', 600), ('200 kg', 500)], 2.5, BLU)
    # bench names, written after the kit so nothing covers them
    s.lines(-1.8, 6.86, [(N['A.01'], 800), ('Non-veg prep', 700), ('800 × 650 × 900', 500)], 2.5, INK)
    s.lines(-1.12, 6.78, [(N['A.02'], 800), ('Veg prep', 700), ('800×650×900', 500)], 2.5, INK)
    s.lines(-0.275, 6.62, [(N['A.03'], 800), ('Pass', 700), ('650×650×900', 500)], 2.5, INK)
    # ---- hood, make-up air
    s.rect(X0, 0.9, 7.85, D - 0.02, 'none', RED, 0.45, '2.2 1.2')
    s.lines(0.5, 7.5, [(N['A.16'], 800), ('Canopy hood above', 600), ('3,350 × 950 × 550', 500)], 2.5, RED)
    s.rect(-2.4, -1.8, 7.0, 7.5, 'none', GRN, 0.35, '1 0.6'); s.rect(-0.95, -0.35, 7.1, 7.6, 'none', GRN, 0.35, '1 0.6')
    s.lines(-0.65, 7.35, [(N['B.19'], 800), ('Make-up air', 600), ('diffuser 600 × 500', 500)], 2.5, GRN)
    s.lines(-1.5, 7.25, [(N['B.19'], 800), ('Make-up air', 600), ('diffuser 600×500', 500)], 2.5, GRN)
    # ---- exhaust run outside (duct at 2,350 to 2,750 mm high)
    EX = '#c4442a'
    s.rect(-1.6, -1.1, 8.4, D, 'none', RED, 0.35, '1.4 0.8')
    for xa, xb, za, zb in ((-1.6, -1.1, D, D + T), (XS - 0.45, -1.1, D + T, D + T + 0.4), (XS - 0.45, XS - 0.05, D - 0.35, D + T + 0.4)): s.rect(xa, xb, za, zb, '#f3e0dc', EX, 0.3, '1.4 0.8')
    s.text(-2.0, D + T + 0.2, f"{N['A.17']}  Exhaust duct 400 × 400, at 2,350 to 2,750 high", 2.5, RED, weight=600)
    s.rect(XS - 0.5, XS + 0.02, D - 1.35, D - 0.35, '#e8c9c2', RED, 0.4); s.text(XS - 0.24, D - 0.85, f"{N['B.16']}  ESP + carbon filter 500 × 1,000", 2.5, RED, weight=600, rot=-90)
    s.circ(XS - 0.25, D - 1.55, 0.18, '#f3e0dc', EX, 0.3); s.lines(XS - 0.25, D - 1.55, [(N['B.17'], 800), ('Exhaust', 600), ('fan Ø440', 500)], 2.5, RED)
    s.text(XS - 0.25, D - 1.2, '', 2.5)
    s.rect(XS - 0.5, XS - 0.05, D - 1.95, D - 1.75, '#f3e0dc', EX, 0.3, '1.4 0.8')
    a, b = s.P(XS - 0.5, D - 1.85); s.add(f'<path d="M{a:.2f} {b:.2f} l6 0 m0 0 l-1.8 -1.2 m1.8 1.2 l-1.8 1.2" stroke="{RED}" stroke-width="0.45" fill="none"/>')
    s.lines(XS - 1.2, D - 1.85, [(N['A.18'], 800), ('Discharge', 600), ('400×400', 500), ('at 2,600', 500)], 2.5, RED)
    s.rect(1.9, 2.4, D + T, D + T + 0.3, '#e1eadc', GRN, 0.3); s.lines(2.15, D + T + 0.15, [(N['B.18'], 800), ('Fresh-air fan', 600), ('500 × 480', 500)], 2.5, GRN)
    # ---- dimensions in mm
    for xa, xb, t in ((X0, -1.25, '1,200'), (-1.2, -0.6, '600'), (-0.55, 0.05, '600'), (0.1, 0.7, '600'), (0.95, 1.75, 'rear exit 800')): s.hdim(xa, xb, D + T + 0.58, t)
    s.hdim(X1, X0, D + T + 0.82, '4,900 inside')
    for xa, xb, t in ((0.1, 0.9, 'door 800'),): s.hdim(xa, xb, KZ - 0.18, t)
    s.vdim(X1 + T + 0.3, KZ + 0.1, D, '2,400 inside')
    for za, zb, t in ((6.45, 7.4, '950'), (7.4, 8.0, '600'), (8.0, D, '800')): s.vdim(X1 + T + 0.12, za, zb, t)
    s.vdim(-0.3, 7.05, 8.1, "cooks' aisle 1,050")
    # ---- labels on leaders below the pass wall (rightmost item on the top row, so no leader crosses a label)
    items = [('Hand-wash basin 250 × 250, prep corner, heater ' + N['B.13'], -2.33, 6.5), (N['A.14'] + '  Cutting-board rack', -2.0, 6.7), (N['A.10'] + '  Mise-en-place rail on the bench', -1.8, 6.55), (N['A.13'] + '  Knife strips on the wall (2)', -1.64, KZ + 0.13),
             (N['B.07'] + '  Under-counter freezer, in the veg bench', -1.15, 6.95), (N['B.10'] + '  Mixer-grinder, on the shelf over the bench', -1.0, 6.6), (N['B.09'] + '  Rice cookers (2)', -0.8, 6.73), (N['B.11'] + '  Kitchen torch, on the shelf', -0.72, 6.5),
             (N['B.15'] + '  Heat lamps over the pass (2)', -0.42, 6.62), (N['A.11'] + '  Dip and garnish rail on the pass', -0.3, 6.99), (N['B.06'] + '  Under-counter fridge, in the pass', -0.2, 6.55), (N['A.12'] + '  Ticket rail over the pass hatch', -0.05, KZ + 0.03),
             (N['B.14'] + '  Insect killer over the door', 0.4, KZ + 0.05), ('Hand-wash basin 280 × 400, at the door, heater ' + N['B.13'], 1.12, 6.5)]
    y0 = 182.0
    for i, (name, ix, iz) in enumerate(items):
        a, b = s.P(ix, iz); ty = y0 + i * 4.4
        s.add(f'<circle cx="{a:.2f}" cy="{b:.2f}" r="0.55" fill="{INK}"/><polyline points="{a:.2f},{b:.2f} {a:.2f},{ty-0.9:.2f} {a+1.5:.2f},{ty-0.9:.2f}" fill="none" stroke="{INK}" stroke-width="0.2"/><text x="{a+2:.2f}" y="{ty:.2f}" font-size="2.5" fill="{INK}">{name}</text>')
    ny = y0 + len(items) * 4.4 + 4
    s.add(f'<text x="12" y="{ny:.1f}" font-size="2.5" fill="{MUT}">The number on each item is its number in the BOQ table below (1 to 44). Not drawn: 16 storage-deck racking, 34 smallware (chef\'s list), 43 the cooling-coil condenser (right outside wall at about 3,000 high, nearer the shopfront, sheet 2).</text>')
    s.add(f'<text x="12" y="{ny+3.2:.1f}" font-size="2.5" fill="{MUT}">Dashed lines are above the floor: hood, duct, make-up air diffusers, ceiling hatch. Rails and shelves are on the walls at the heights given in the BOQ. Cooks\' aisle 1,050, and 950 at the wok range.</text>')
    bx_, by_ = 12.0, ny + 9
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
    import itertools; cnt = itertools.count(1)
    by = {i[0]: i for sec in boq.S for i in sec[3]}
    for sl, title, note, items in boq_goa.GOA:
        yield ('sec', sl, title, note)
        for k, r in enumerate(items, 1):
            no, item, size, spec, unit, qty, ref = by[r['no']]
            item = r['item'] if r['no'] in ('A.16', 'A.17', 'B.16', 'B.17', 'B.18', 'B.19', 'B.20', 'E.03') else item
            yield ('item', str(next(cnt)), item, size, spec, unit, qty, no)

def page():
    esc = html.escape; body = []; n = 0
    for r in lines():
        if r[0] == 'sec':
            note = r[3].replace('Exhaust about 2,400 to 3,000 CFM (4,000 to 5,000 m³/h)', 'Exhaust 4,000 to 5,000 m³/h').replace('Vendor states the static pressure the fan is selected for.', 'Vendor states the static pressure the fan is selected for.')
            note = metres_to_mm(note)
            note = re.sub(r"Worktops 18 SWG \(1\.2 mm\), bodies and shelves 19 SWG \(1\.0 mm\), legs 1½\" \(38 mm\) tube", 'Worktops 1.2 mm or thicker, bodies and shelves 1.0 mm, legs 38 mm tube', note)
            body.append(f'<tr class="sec"><th>{r[1]}</th><th colspan="8">{esc(r[2])}<small>{esc(note)}</small></th></tr>')
        else:
            _, sl, item, size, spec, unit, qty, ref = r; n += 1
            spec = metres_to_mm(re.sub(r'\s*\(about \d+ sq ft with bends\)', '', spec))
            spec = spec.replace('under-counter freezer (B.07)', 'under-counter freezer').replace('goes on the hoist (B.21)', 'goes on the goods hoist').replace('its own baskets, B.02', 'its own baskets').replace('steamer comes', 'dim sum steamer comes')
            if unit == 'm': unit, qty = 'mm', round(qty * 1000)
            q = f'{qty:,}' if isinstance(qty, int) else f'{qty:g}'
            body.append(f'<tr><td class="no">{sl}</td><td><b>{esc(item)}</b></td><td class="sz">{esc(size)}</td><td>{esc(spec)}</td><td>{unit}</td><td class="n">{q}</td><td class="blank"></td><td class="blank"></td><td class="blank"></td></tr>')
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><title>Kitchen drawing and BOQ in mm · Cabin East</title>
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
<div class="hd"><div><h1>Kitchen equipment and exhaust</h1><p>Drawing at 1:25 on A3 (print at 100%), then the BOQ. Every item is named on the drawing. All sizes in mm. For kitchen equipment and exhaust vendors · Shop 4, Tulip Residency, Gandaulim, South Goa</p></div><div class="r">Cabin East · Wok | Steam | Draught · Concept 27<br>singhgenics.github.io/Simplex/boq-drawing.html</div></div>
{drawing_svg()}
<h2>BOQ: kitchen equipment and exhaust ({n} lines)</h2>
<table><thead><tr><th>No.</th><th>Item / type</th><th>Size W × D × H (mm)</th><th>Capacity, rating, specification</th><th>Unit</th><th>Qty</th><th>Rate ₹</th><th>Amount ₹</th><th>Make / model</th></tr></thead><tbody>{''.join(body)}</tbody></table>
<p class="foot">Quantities and sizes are the space available, from the model; the vendor measures on site and states the make, model, kW or litres, steel grade and thickness, price ex-GST, delivery, installation, lead time, warranty and who services it in Goa. Duct length is an estimate. Gas, plumbing, electrical, civil and fire work are in the main BOQ (boq.html). Concept drawings for briefing suppliers, not construction drawings.</p>
</div></body></html>
'''

if __name__ == '__main__':
    open('boq-drawing.html', 'w').write(page()); print('boq-drawing.html written')
