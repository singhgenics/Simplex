"""Bar vendor list (BOQ) taken from the Simplex model and floor plan: the bar on the left wall (back bar, counter, keg cabinet, built-in glasswasher and cooler, ice, POS)
plus the server station beside it. Sizes in mm. One A3 portrait PDF: the 1:25 bar plan on top (every item numbered and named), the list below.
Positions come from tools/plan.py (the mirrored, final bar); sizes from the model code and the side panel in index.html. Rates are left blank for suppliers.
Usage: python3 tools/boq_bar.py  ->  boq-bar.html, plans/bar-boq.xlsx, plans/bar-boq.csv   (PDF: print boq-bar.html from Chrome, A3 portrait, no header/footer)
"""
import sys, os, csv, html
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kitchen_sheets as K
from kitchen_sheets import X1, T, KZ, INK, MUT, RED, BLU, GRN, STEEL

# (key, item / type, size W × D × H mm, capacity / specification, unit, qty, trade)   position of each item is in POS below
SECTIONS = [
('A', 'Bar carpentry and fabrication', 'Contractor and carpenter. Marble tops, black bases and brass details as in the 3D model (singhgenics.github.io/Simplex). Sizes are the space available: the fabricator measures on site.', [
 ('counter', 'Bar counter', '2,200 × 750 × 1,040', 'Marble top, square end facing the door; onyx front edge-lit by an LED panel behind black mesh; black base; brass foot rail; houses the keg cabinet (next line)', 'nos', 1),
 ('kegcab', 'Keg cabinet inside the counter, door end', '1,100 × 630 × 900', 'Two louvred timber doors (the flash chiller needs air), roll-out base for 3 kegs', 'nos', 1),
 ('sinkunit', 'Bar sink unit with ice well and speed rail', '500 long × 850 high', 'Stainless, bartender side, with a speed rail for bottles', 'nos', 1),
 ('backbar', 'Back bar run', '2,650 × 400 × 960', 'Olive-wood doors, marble top; onyx panel from 960 to 2,380 mm and sage panel above, along the left wall', 'm', 2.65),
 ('builtin', 'Built-in section of the back bar (holds the glasswasher and the cooler)', '1,270 long × 550 deep × 960', 'Deeper stretch opposite the bar sink; bartender aisle here is about 700 mm', 'nos', 1),
 ('display', 'Back bar display shelves with LED and onyx glow panel', '1,000 × 250', 'Two brass-edged timber tiers at 1,300 and 1,740 mm for whisky, gin and vodka bottles; backlit onyx panel behind', 'set', 1),
 ('infusion', 'Infusion jars with glass shelf, door end', '600 long × 220', 'Glass shelf at 960 mm with 3 jars; the CO₂ cylinder stands in the cabinet below', 'set', 1),
 ('soju', 'Soju display riser and ON TAP board, pillar end', '', 'Size by the contractor', 'set', 1),
 ('rack', 'Floating glass rack over the counter', '740 × 2,000', 'Brass frame hung from the slab on 4 black rods; lower tier at 2,300 mm (stemware upside down on brass rails), upper tier at 2,580 mm (glass shelf for pints and highballs); warm LED strips and 4 downlights', 'nos', 1),
 ('pos', 'POS nook recessed into the back bar, door end', '480 long × 400 deep × 960 to 1,350', 'Timber frame; space for tablet, card machine and receipt printer', 'nos', 1),
 ('drawer', 'Cash drawer with small safe, under the POS nook', '400 × 240', 'Lockable', 'nos', 1),
 ('stool', 'Bar stool, velvet high-back', '', '4 stools, 600 mm apart; seat height to suit the 1,040 mm counter', 'nos', 4),
 ('tv', 'Wall TV with bracket', '1,140 × 620', 'On the wall above the back bar at the door end', 'nos', 1),
 ('neon', 'Neon sign "settle up here"', '900 × 200', 'Over the POS nook; plus 2 red vertical neon tubes on the back bar wall', 'set', 1),
]),
('B', 'Bar equipment (branded)', 'State make and model, kW or litres, and who services it in Goa. Sizes are the space available: do not quote a wider unit.', [
 ('font', 'Beer font, brass, 3 taps on one font', 'Ø 90 × 420 high', 'Taps for 3 craft beers; tap handles to the brand; the brewery may lend this (get it in writing)', 'nos', 1),
 ('chiller', 'Flash chiller, under-counter, self-contained', '500 × 420 × 570', 'No outdoor unit; rated for room-temperature kegs in the tropics; chills the beer on its way to the taps', 'nos', 1),
 ('keg', 'Keg 20 L on tap, with coupler', 'Ø 240 × 420', '3 on tap (one per tap), on the roll-out base; supplied by the brewery', 'nos', 3),
 ('beerline', 'Beer line, insulated, chiller to font', '', 'About 2 m with fittings', 'lot', 1),
 ('co2', 'CO₂ cylinder 6 kg with regulator and chain', 'Ø 150 × 670', 'In the back-bar cabinet under the infusion jars, with a low vent grille', 'nos', 1),
 ('co2alarm', 'Low-mounted CO₂ alarm', '', 'CO₂ is heavier than air', 'nos', 1),
 ('gw', 'Under-counter glasswasher, drop-down door', '450 × 500 × 820', 'Built into the back bar; hot and cold water and a drain', 'nos', 1),
 ('cooler', 'Glass-door cooler for mixers, water and soft drinks', '700 × 520 × 860', 'Built into the back bar; lit, with shelves; state litres', 'nos', 1),
 ('ice', 'Ice machine, under-counter', '500 × 550 × 800', 'About 50 kg a day; water filter and a drain', 'nos', 1),
 ('filter', 'Water filter cartridge for the ice machine and the glasswasher', '', '', 'set', 1),
 ('smallware', 'Bar smallware', '', 'To the bar consultant\'s list: shakers, jiggers, strainers, muddlers, bar mats, speed-rail bottles', 'lot', 1),
 ('glass', 'Glassware per the drinks menu', '', 'Pint, gose, whisky, highball, coupe, shot; see the crockery list (breweries often give branded pint glasses)', 'lot', 1),
]),
('C', 'Server station (next to the bar)', 'Left wall, just past the back bar, two steps from the kitchen door.', [
 ('station', 'Server station counter', '800 × 500 × 940', 'Black base, olive-wood doors, marble top', 'nos', 1),
 ('stshelf', 'Wall shelf over the station', '800 × 300', 'At 1,600 mm and 1,950 mm, for glasses and cutlery', 'nos', 2),
 ('brewer', 'Commercial filter-coffee batch brewer with 2 jugs and warming plates', '', 'About 12 cups a batch; state make and model', 'nos', 1),
 ('waterdisp', 'Water dispenser', '', 'Chilled and ambient', 'nos', 1),
 ('milk', 'Milk warmer', '', 'Small', 'nos', 1),
]),
('D', 'Bar services', 'Licensed electrician and plumber. Bar and kitchen drains go to the grey-water line (never the biodigester).', [
 ('power', 'Power points, bar and station', '', 'Ice machine, glasswasher, cooler, flash chiller, POS, TV, neon and LED strips, coffee brewer, water dispenser; the chillers and POS are on the power backup', 'nos', 10),
 ('water', 'Water points with isolation valves', '', 'Bar sink (hot and cold), glasswasher (hot and cold), ice machine (cold, filtered), coffee brewer (cold)', 'nos', 4),
 ('drain', 'Drain points to the grey-water line', '', 'Bar sink, glasswasher, ice machine, ice well', 'nos', 4),
 ('led', 'Warm LED strips (2,200 K) under both long sides of the counter, and 4 warm downlights over the marble', '', '', 'lot', 1),
]),
]

# plan position of each item (x, z) in metres, from tools/plan.py; used for the leader lines on the drawing
POS = {'counter': (0.8, 3.1), 'kegcab': (0.85, 3.5), 'sinkunit': (1.1, 4.4), 'backbar': (2.3, 5.25), 'builtin': (1.95, 4.4), 'display': (2.3, 3.95), 'infusion': (2.3, 3.4), 'soju': (2.3, 5.2),
       'rack': (0.5, 5.0), 'pos': (2.25, 3.0), 'drawer': (2.2, 2.9), 'stool': (0.13, 4.47), 'tv': (2.4, 3.1), 'neon': (2.4, 2.85), 'font': (0.85, 3.4), 'chiller': (0.92, 3.87), 'keg': (1.05, 3.21),
       'beerline': (0.95, 3.7), 'co2': (2.25, 3.55), 'co2alarm': (2.45, 3.45), 'gw': (2.15, 4.8), 'cooler': (2.15, 4.17), 'ice': (0.95, 4.9), 'filter': (1.0, 4.7), 'smallware': (0.6, 4.3), 'glass': (0.45, 5.0),
       'station': (2.2, 5.85), 'stshelf': (2.4, 5.6), 'brewer': (2.2, 5.7), 'waterdisp': (2.2, 6.0), 'milk': (2.15, 5.95)}

ITEMS = [(k, i, sz, sp, u, q, sec) for sec, _t, _n, rows in SECTIONS for (k, i, sz, sp, u, q) in rows]
NUM = {r[0]: n for n, r in enumerate(ITEMS, 1)}


def numbered():
    for sec, title, note, rows in SECTIONS:
        yield ('sec', sec, title, note)
        for (k, item, size, spec, unit, qty) in rows: yield ('item', NUM[k], item, size, spec, unit, qty)

def fmt(q): return f'{q:g}' if isinstance(q, float) else str(q)

def write_csv(path):
    with open(path, 'w', newline='') as f:
        w = csv.writer(f); w.writerow(['No.', 'Item / type', 'Size W × D × H (mm)', 'Capacity, rating, specification', 'Unit', 'Qty', 'Rate (INR)', 'Amount (INR)', 'Make / model / remarks'])
        for r in numbered():
            if r[0] == 'sec': w.writerow(['', r[2], '', r[3], '', '', '', '', ''])
            else: w.writerow([r[1], r[2], r[3], r[4], r[5], fmt(r[6]), '', '', ''])

def write_xlsx(path):
    from openpyxl import Workbook
    from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
    wb = Workbook(); ws = wb.active; ws.title = 'Bar BOQ'
    thin = Side(style='thin', color='BBBBBB'); box = Border(left=thin, right=thin, top=thin, bottom=thin)
    head = PatternFill('solid', fgColor='2A2420'); band = PatternFill('solid', fgColor='EFE6D3'); inp = PatternFill('solid', fgColor='FFF9E0'); NC = 9
    ws['A1'] = 'Bill of quantities · bar and server station · Betalbatim pub'; ws['A1'].font = Font(bold=True, size=14)
    ws['A2'] = 'Shop 4, Tulip Residency, Gandaulim, Salcete, South Goa. Bar on the left wall as in the Simplex model. Sizes in mm (width × depth × height), the space available; measure on site. Item numbers match the A3 drawing.'
    ws['A3'] = 'Fill the yellow cells (rate, make/model, remarks). Amounts and totals calculate. Rates ex-GST; freight, installation and the GST rate go in the lines at the bottom.'
    for r in (2, 3): ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=NC); ws.cell(r, 1).alignment = Alignment(wrap_text=True, vertical='top'); ws.row_dimensions[r].height = 30
    for i, h in enumerate(['No.', 'Item / type', 'Size W × D × H (mm)', 'Capacity, rating, specification', 'Unit', 'Qty', 'Rate (₹)', 'Amount (₹)', 'Make / model / remarks'], 1):
        c = ws.cell(5, i, h); c.font = Font(bold=True, color='FFFFFF'); c.fill = head; c.alignment = Alignment(vertical='center', wrap_text=True); c.border = box
    r = 6; subs = []
    for sec, title, note, rows in SECTIONS:
        ws.cell(r, 2, title); ws.cell(r, 4, note)
        for i in range(1, NC + 1): c = ws.cell(r, i); c.fill = band; c.font = Font(bold=True); c.border = box; c.alignment = Alignment(wrap_text=True, vertical='top')
        ws.row_dimensions[r].height = 44; r += 1; first = r
        for (k, item, size, spec, unit, qty) in rows:
            for i, v in enumerate([NUM[k], item, size, spec, unit, qty, None, f'=IF(G{r}="","",F{r}*G{r})', None], 1):
                c = ws.cell(r, i, v); c.border = box; c.alignment = Alignment(wrap_text=True, vertical='top')
            for i in (7, 9): ws.cell(r, i).fill = inp
            ws.cell(r, 7).number_format = '#,##0.00'; ws.cell(r, 8).number_format = '#,##0.00'; ws.cell(r, 6).number_format = '0.0#'
            r += 1
        ws.cell(r, 2, f'Subtotal, section {sec}'); ws.cell(r, 8, f'=SUM(H{first}:H{r-1})'); subs.append(r)
        for i in range(1, NC + 1): c = ws.cell(r, i); c.font = Font(bold=True); c.border = box
        ws.cell(r, 8).number_format = '#,##0.00'; r += 2
    ws.cell(r, 2, 'Total of all sections (ex-GST)'); ws.cell(r, 8, '=' + '+'.join(f'H{x}' for x in subs)); tot = r; r += 1
    ws.cell(r, 2, 'Freight and unloading to Betalbatim'); ws.cell(r, 8).fill = inp; fr = r; r += 1
    ws.cell(r, 2, 'Installation and connections not included above'); ws.cell(r, 8).fill = inp; ins = r; r += 1
    ws.cell(r, 2, 'GST rate (%)'); ws.cell(r, 8, 18).fill = inp; gr = r; r += 1
    ws.cell(r, 2, 'GST'); ws.cell(r, 8, f'=ROUND((H{tot}+H{fr}+H{ins})*H{gr}/100,2)'); gs = r; r += 1
    ws.cell(r, 2, 'Grand total including GST'); ws.cell(r, 8, f'=H{tot}+H{fr}+H{ins}+H{gs}'); gt = r
    for x in range(tot, r + 1):
        ws.cell(x, 2).font = Font(bold=True); ws.cell(x, 8).number_format = '#,##0.00'; ws.cell(x, 8).font = Font(bold=True)
    ws.cell(gt, 2).fill = band; ws.cell(gt, 8).fill = band
    for c, w in zip('ABCDEFGHI', (6, 44, 24, 58, 6, 7, 12, 14, 28)): ws.column_dimensions[c].width = w
    ws.freeze_panes = 'C6'; ws.page_setup.orientation = 'landscape'; ws.page_setup.paperSize = ws.PAPERSIZE_A4; ws.page_setup.fitToWidth = 1; ws.page_setup.fitToHeight = 0
    ws.sheet_properties.pageSetUpPr.fitToPage = True; ws.print_title_rows = '5:5'
    wb.save(path)

def drawing_svg():
    """1:25 plan of the bar and the server station: items numbered and named, sizes in mm. Leaders run to a label column on the right."""
    s = K.Sheet(14, 14, 2.65, 6.45)           # left wall inside face at x = 2.45 -> page 22 mm; page y = 14 + (6.45 - z) * 40
    def R(xa, xb, za, zb, fill='none', stroke=INK, sw=0.3, dash=None): s.rect(xa, xb, za, zb, fill, stroke, sw, dash)
    R(2.45, 2.65, 2.2, 6.45, '#4a4038', '#4a4038', 0.2)                                    # left wall
    R(-0.1, 2.45, KZ, KZ + 0.1, '#d8c6ac', '#a8987c', 0.2); s.text(0.5, KZ + 0.05, 'kitchen wall (door to the kitchen)', 2.5, MUT)
    for z in (0.0,): pass
    # back bar and the built-in section
    R(2.05, 2.45, 2.72, 5.37, '#cfd7b2'); R(1.9, 2.05, 3.77, 5.04, '#cfd7b2', INK, 0.3)
    R(1.9, 2.45, 4.57, 5.02, '#9aa0a5', INK, 0.4); R(1.9, 2.45, 3.82, 4.52, '#dff0f6', BLU, 0.4)
    R(2.05, 2.45, 2.78, 3.26, '#e6d6bc'); R(2.05, 2.45, 3.37, 3.72, '#e6d6bc', '#8f6a4a', 0.4)
    # counter, keg cabinet, chiller, kegs, sink, ice
    R(0.35, 1.2, 2.94, 5.22, '#efe7da'); R(0.59, 1.22, 3.04, 4.14, '#efe7da', BLU, 0.4); R(0.67, 1.17, 3.66, 4.08, '#dff0f6', BLU, 0.3)
    for x, z in ((1.05, 3.21), (0.77, 3.21), (1.05, 3.49)): s.circ(x, z, 0.11, 'none', BLU, 0.3)
    R(1.0, 1.2, 4.16, 5.22, '#c3c8cc'); R(0.67, 1.22, 4.64, 5.14, 'none', BLU, 0.3, '1.4 0.8')
    for z in (3.27, 3.87, 4.47, 5.07): s.circ(0.13, z, 0.21, '#efe2c8', INK, 0.3)
    R(0.35, 1.1, 3.12, 5.12, 'none', MUT, 0.3, '1.4 0.8')                                 # floating glass rack above
    R(0.85, 0.87, 3.2, 3.6, '#a8741a', '#a8741a', 0.2)                                      # beer font on the counter
    # server station
    R(1.95, 2.45, 5.45, 6.25, '#cfd7b2')
    # the item number on each item (small circle); lot items without a place on the plan are listed under the key
    def tag(k, x, z, col=INK):
        a, b = s.P(x, z); s.add(f'<circle cx="{a:.2f}" cy="{b:.2f}" r="2.3" fill="#fff" stroke="{col}" stroke-width="0.3"/><text x="{a:.2f}" y="{b+0.9:.2f}" font-size="2.4" font-weight="700" fill="{col}" text-anchor="middle">{NUM[k]}</text>')
    placed = {'counter': (0.5, 3.0), 'kegcab': (0.85, 3.95), 'chiller': (0.92, 3.72), 'keg': (0.77, 3.21), 'font': (0.86, 3.42), 'beerline': (0.72, 3.62), 'sinkunit': (1.1, 4.45), 'ice': (0.85, 4.9), 'rack': (0.7, 5.1), 'stool': (0.13, 3.87),
              'backbar': (2.25, 5.25), 'soju': (2.55, 5.1), 'display': (2.55, 4.3), 'builtin': (1.97, 3.9), 'gw': (2.17, 4.8), 'cooler': (2.17, 4.17), 'pos': (2.35, 3.05), 'drawer': (2.15, 2.9), 'infusion': (2.15, 3.5), 'co2': (2.38, 3.6),
              'co2alarm': (2.55, 3.65), 'tv': (2.55, 3.4), 'neon': (2.55, 3.0), 'station': (2.2, 6.1), 'stshelf': (2.55, 5.85), 'brewer': (2.3, 5.8), 'waterdisp': (2.05, 5.8), 'milk': (2.05, 5.6)}
    for k, (x, z) in placed.items(): tag(k, x, z)
    # key: every numbered item, on the right of the plan, in list order
    col_x, ty = 138.0, 24.0
    for sec, title, _n, rows in SECTIONS:
        s.add(f'<text x="{col_x}" y="{ty:.1f}" font-size="2.9" font-weight="700" fill="{RED}">{html.escape(sec + ". " + title.upper())}</text>'); ty += 4.4
        for (k, item, size, spec, unit, qty) in rows:
            sz = f'  {size}' if size else ''
            s.add(f'<text x="{col_x}" y="{ty:.1f}" font-size="2.5" fill="{INK}"><tspan font-weight="700">{NUM[k]}</tspan>   {html.escape(item)}{html.escape(sz)}</text>'); ty += 3.9
        ty += 2.2
    missing = [NUM[k] for k, *_ in ITEMS if k not in placed]
    s.add(f'<text x="{col_x}" y="{ty:.1f}" font-size="2.5" fill="{MUT}">No tag on the plan (lots, services and loose items): {", ".join(map(str, missing))}.</text>')
    # dimensions
    s.vdim(2.95, 2.72, 5.37, 'back bar 2,650', RED); s.vdim(-0.3, 2.94, 5.22, 'counter 2,280 incl. front', RED)
    s.hdim(1.2, 1.9, 5.5, 'bartender aisle 850', RED); s.hdim(0.35, 1.2, 2.82, '850', RED)
    s.text(0.22, 6.2, 'Window tables are in front of the bar (left, toward the shopfront); the entry is at the bottom of the plan.', 2.5, MUT, anchor='start') if False else None
    s.text(1.0, 2.3, 'toward the shopfront and the entry', 2.5, MUT)
    bx_, by_ = 22.0, 208.0
    s.add(f'<rect x="{bx_}" y="{by_}" width="40" height="1.6" fill="{INK}"/><rect x="{bx_+40}" y="{by_}" width="40" height="1.6" fill="none" stroke="{INK}" stroke-width="0.2"/>'
          f'<text x="{bx_}" y="{by_+5}" font-size="2.5" fill="{INK}">0</text><text x="{bx_+40}" y="{by_+5}" font-size="2.5" text-anchor="middle" fill="{INK}">1000</text><text x="{bx_+80}" y="{by_+5}" font-size="2.5" text-anchor="middle" fill="{INK}">2000</text>'
          f'<text x="{bx_+86}" y="{by_+1.8}" font-size="2.9" font-weight="700" fill="{INK}">PLAN 1:25 on A3, dimensions in mm</text>')
    s.add(f'<text x="22" y="219" font-size="2.5" fill="{MUT}">Left wall at the left of the plan, the bar island to its right. Dashed: floating glass rack above, and the ice machine zone. The numbers are the item numbers in the key and in the list below and the Excel.</text>')
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="291mm" height="208mm" viewBox="0 12 291 224" font-family="\'IBM Plex Sans\', Helvetica, Arial, sans-serif"><rect x="0" y="12" width="291" height="224" fill="#fbf7ef"/>{"".join(s.o)}</svg>'

def page():
    esc = html.escape; body = []
    for r in numbered():
        if r[0] == 'sec': body.append(f'<tr class="sec"><th></th><th colspan="8">{esc(r[1])}. {esc(r[2])}<small>{esc(r[3])}</small></th></tr>')
        else: body.append(f'<tr><td class="no">{r[1]}</td><td><b>{esc(r[2])}</b></td><td class="sz">{esc(r[3])}</td><td>{esc(r[4])}</td><td>{r[5]}</td><td class="n">{fmt(r[6])}</td><td class="blank"></td><td class="blank"></td><td class="blank"></td></tr>')
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"><title>Bar BOQ and drawing · Betalbatim Pub</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,700&family=IBM+Plex+Sans:wght@400;500;600;700&family=IBM+Plex+Mono:wght@500&display=swap">
<style>
/* Layout: A3 portrait when printed (plan on top at 1:25, list below); a scrolling page on screen */
@page{{size:297mm 420mm;margin:0}}
:root{{--paper:#fbf7ef;--ink:#2a2420;--muted:#6a5d4e;--rule:#d9cbb3;--accent:#b23a1e;--chip:#fffdf8;--display:'Bricolage Grotesque','Segoe UI',sans-serif;--body:'IBM Plex Sans','Helvetica Neue',Arial,sans-serif;--mono:'IBM Plex Mono',ui-monospace,Menlo,monospace}}
html,body{{margin:0;background:var(--paper);color:var(--ink);font-family:var(--body)}}
.sheet{{max-width:297mm;margin:0 auto;padding:4mm 3mm 6mm}}
.hd{{display:flex;justify-content:space-between;align-items:flex-end;gap:12px;border-bottom:.35mm solid var(--ink);padding-bottom:2mm}}
.hd h1{{font:700 7mm/1 var(--display);margin:0}} .hd p{{margin:1mm 0 0;font-size:2.6mm;color:var(--muted)}} .hd .r{{text-align:right;font-size:2.6mm;color:var(--muted)}}
svg{{display:block;width:100%;height:auto}}
.bar{{display:flex;flex-wrap:wrap;gap:8px;margin:8px 0}} .bar a{{font:600 13px var(--body);color:var(--ink);background:var(--chip);border:1px solid var(--rule);border-radius:8px;padding:9px 12px;text-decoration:none}} .bar a.pri{{background:var(--ink);color:var(--paper);border-color:var(--ink)}}
h2{{font:700 4.4mm/1.2 var(--display);margin:3mm 0 1.5mm}}
.tw{{overflow-x:auto}}
table{{border-collapse:collapse;width:100%;min-width:900px;font-size:2.7mm;line-height:1.3}}
th,td{{padding:.9mm 1.4mm;border-top:.2mm solid var(--rule);vertical-align:top;text-align:left}}
thead th{{background:var(--ink);color:var(--paper);font:600 2.5mm var(--mono);border-top:0;white-space:nowrap}}
tr.sec th{{background:#efe6d3;font:700 2.9mm var(--body)}} tr.sec small{{display:block;font:400 2.4mm var(--body);color:var(--muted)}}
td.no{{font:600 2.5mm var(--mono)}} td.sz{{font:500 2.5mm var(--mono)}} td.n{{text-align:right;font-family:var(--mono)}} td.blank{{background:#fffdf0;width:11mm}}
thead{{display:table-header-group}} tr{{break-inside:avoid}} .foot{{font-size:2.6mm;color:var(--muted);margin-top:2mm}}
@media print{{.bar{{display:none}} .sheet{{padding:4mm 3mm}} table{{min-width:0}}}}
@media (max-width:700px){{.hd{{flex-direction:column;align-items:flex-start}} .hd h1{{font-size:26px}} .hd p,.hd .r{{font-size:12px}} table{{font-size:13px}} th,td{{padding:6px 8px}} h2{{font-size:20px}}}}
</style></head><body><div class="sheet">
<div class="hd"><div><h1>Bar and server station</h1><p>Vendor list and drawing for the bar equipment, taken from the Simplex model. Plan at 1:25 on A3 (print at 100%), sizes in mm. Shop 4, Tulip Residency, Gandaulim, South Goa</p></div><div class="r">Betalbatim pub · Simplex · Concept 27<br>singhgenics.github.io/Simplex/boq-bar.html</div></div>
<div class="bar"><a class="pri" href="plans/bar-drawing-boq-mm.pdf" target="_blank" rel="noopener">A3 PDF: drawing + list</a><a href="plans/bar-boq.xlsx">Excel (rates and totals calculate)</a><a href="plans/bar-boq.csv">CSV</a><a href="boq.html">Kitchen BOQ</a><a href="./">3D model</a></div>
{drawing_svg()}
<h2>Bar vendor list ({len(ITEMS)} lines)</h2>
<div class="tw"><table><thead><tr><th>No.</th><th>Item / type</th><th>Size W × D × H (mm)</th><th>Capacity, rating, specification</th><th>Unit</th><th>Qty</th><th>Rate ₹</th><th>Amount ₹</th><th>Make / model</th></tr></thead><tbody>{''.join(body)}</tbody></table></div>
<p class="foot">Quantities and sizes are the space available, from the model; the vendor measures on site and states make, model, kW or litres, price ex-GST, delivery, installation, lead time, warranty and who services it in Goa. The Goa excise licence and fire NOC come before any draught installation. Concept drawings for briefing suppliers, not construction drawings.</p>
</div></body></html>
'''

if __name__ == '__main__':
    write_csv('plans/bar-boq.csv'); write_xlsx('plans/bar-boq.xlsx')
    open('boq-bar.html', 'w').write(page()); print(len(ITEMS), 'lines; boq-bar.html, plans/bar-boq.xlsx, .csv written')
