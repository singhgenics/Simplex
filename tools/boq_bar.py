"""Bar vendor list (BOQ) taken from the Simplex model and floor plan: the bar on the left wall (back bar, counter, keg cabinet, built-in glasswasher and cooler, ice, POS)
plus the server station beside it. Sizes in mm. One A3 portrait PDF: the 1:25 bar plan on top (every item numbered and named), the list below.
Positions come from tools/plan.py (the mirrored, final bar); sizes from the model code and the side panel in index.html. Rates are left blank for suppliers.
Usage: python3 tools/boq_bar.py  ->  boq-bar.html, plans/bar-boq.xlsx, plans/bar-boq.csv   (PDF: print boq-bar.html from Chrome, A3 portrait, no header/footer)
"""
import sys, os, csv, html
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kitchen_sheets as K
from kitchen_sheets import X1, T, KZ, INK, MUT, RED, BLU, GRN, STEEL

# Sections follow the bar's physical areas, so each one is a place you can point at on the plan.
# (key, item, where it is, size W × D × H mm, specification, unit, qty)
SECTIONS = [
('A', 'Customer side of the bar', 'What guests see and sit at: the counter, the stools and the glass rack hanging above it.', '#b98f3a', [
 ('counter', 'Bar counter', 'The long island in the middle of the bar', '2,200 × 750 × 1,040', 'Marble top, square end facing the door; onyx front edge-lit by an LED panel behind black mesh; black base; brass foot rail', 'nos', 1),
 ('stool', 'Bar stool, velvet high-back', 'In front of the counter, 600 mm apart', '', 'Seat height to suit the 1,040 mm counter', 'nos', 4),
 ('rack', 'Floating glass rack', 'Hangs from the slab above the counter', '740 × 2,000', 'Brass frame on 4 black rods; lower tier at 2,300 mm for stemware hung upside down, upper tier at 2,580 mm for pints and highballs; warm LED strips', 'nos', 1),
]),
('B', 'Draught beer (taps, kegs and chiller)', 'Everything for the 3 craft taps. The taps are on top of the counter; the kegs and chiller are inside the counter at the door end, behind two louvred doors.', '#2f6f9f', [
 ('font', 'Beer font with 3 taps', 'On top of the counter, door end', 'Ø 90 × 420 high', 'One brass font, 3 taps; tap handles to the brewery brand. The brewery may lend this (get it in writing)', 'nos', 1),
 ('kegcab', 'Keg cabinet', 'Inside the counter, door end (bartender side)', '1,100 × 630 × 900', 'Two louvred timber doors, because the chiller needs air; roll-out base for the kegs', 'nos', 1),
 ('keg', 'Keg 20 L with coupler', 'On the roll-out base in the keg cabinet', 'Ø 240 × 420', '3 on tap, one per tap; supplied by the brewery', 'nos', 3),
 ('chiller', 'Flash chiller', 'In the keg cabinet, beside the kegs', '500 × 420 × 570', 'Self-contained, no outdoor unit, rated for room-temperature kegs in the tropics; chills the beer on its way to the taps', 'nos', 1),
 ('beerline', 'Beer line, insulated', 'From the chiller up to the font', '', 'About 2 m with fittings', 'lot', 1),
 ('co2', 'CO₂ cylinder with regulator and chain', 'In the back-bar cabinet under the infusion jars (a different place from the kegs)', 'Ø 150 × 670', '6 kg, chained upright, with a low vent grille', 'nos', 1),
 ('co2alarm', 'Low CO₂ alarm', 'Low on the back-bar cabinet', '', 'CO₂ is heavier than air, so it sits near the floor', 'nos', 1),
]),
('C', 'Bartender work area (sink and ice basin, speed rail, ice machine)', 'The stainless area behind the counter at the far end, where the bartender washes and scoops ice from the basin and keeps the speed-rail bottles.', '#3f6a3a', [
 ('workunit', 'Stainless work unit', 'Behind the counter, bartender side, far end', '1,060 × 200 × 850', 'Holds the sink basin and the speed rail below; one continuous stainless unit', 'nos', 1),
 ('sink', 'Bar sink / ice well basin', 'Set into the top of the work unit', '380 × 160 × 160', 'One basin used for washing and as the ice well; hot and cold tap, drains to the grey-water line. The vendor may propose a deeper basin (then the unit depth changes)', 'nos', 1),
 ('speedrail', 'Speed rail', 'Along the front of the work unit', '1,060 long', 'Holds the everyday spirit bottles within reach', 'nos', 1),
 ('ice', 'Ice machine, under-counter', 'Under the counter beside the work unit', '500 × 550 × 800', 'About 50 kg a day; filtered cold water and a drain', 'nos', 1),
 ('filter', 'Water filter for the ice machine and the glasswasher', 'Inside the cabinet next to the ice machine', '', 'Cartridge type; replace on schedule', 'set', 1),
]),
('D', 'Back bar (the wall behind the bartender)', 'The long unit along the left wall: cabinets below, display shelves and an onyx panel above.', '#8a3a1a', [
 ('backbar', 'Back bar run', 'Along the left wall, 2,650 mm long', '2,650 × 400 × 960', 'Olive-wood doors and marble top; onyx panel from 960 to 2,380 mm with a sage panel above', 'm', 2.65),
 ('display', 'Display shelves for whisky, gin and vodka', 'On the wall above the back bar', '1,000 × 250', 'Two brass-edged tiers at 1,300 and 1,740 mm; backlit onyx panel behind', 'set', 1),
 ('infusion', 'Infusion jars with a glass shelf', 'Door end of the back bar', '600 long × 220', 'Glass shelf at 960 mm with 3 jars', 'set', 1),
 ('soju', 'Soju display and ON TAP board', 'Far end of the back bar, by the pillar', '', 'Size by the contractor; not drawn in the model', 'set', 1),
 ('tv', 'Wall TV with bracket', 'On the wall above the back bar, door end', '1,140 × 620', '', 'nos', 1),
 ('neon', 'Neon sign "settle up here" and two red neon tubes', 'Over the POS nook; tubes on the back bar wall', '900 × 200', '', 'set', 1),
]),
('E', 'Built-in section (glasswasher and drinks cooler)', 'A deeper stretch of the back bar opposite the bartender work area. The glasswasher and the cooler sit side by side in it.', '#5a6a7a', [
 ('builtin', 'Built-in cabinet for the glasswasher and cooler', 'Part of the back bar, 550 mm deep here', '1,270 × 550 × 960', 'Bartender aisle is about 700 mm at this point', 'nos', 1),
 ('gw', 'Under-counter glasswasher', 'In the built-in cabinet, toward the far end', '450 × 500 × 820', 'Drop-down door; hot and cold water and a drain', 'nos', 1),
 ('cooler', 'Glass-door drinks cooler', 'In the built-in cabinet, toward the door', '700 × 520 × 860', 'Lit; for mixers, water and soft drinks; state litres', 'nos', 1),
]),
('F', 'Cash and POS', 'At the door end of the back bar, where bills are settled.', '#6b3fa0', [
 ('pos', 'POS nook', 'Recessed into the back bar, door end', '480 × 400 × 960 to 1,350', 'Timber frame; room for tablet, card machine and receipt printer', 'nos', 1),
 ('drawer', 'Cash drawer with small safe', 'Under the POS nook', '400 × 240', 'Lockable', 'nos', 1),
]),
('G', 'Server station', 'On the left wall just past the back bar, two steps from the kitchen door.', '#a8741a', [
 ('station', 'Server station counter', 'Left wall, past the back bar', '800 × 500 × 940', 'Black base, olive-wood doors, marble top', 'nos', 1),
 ('stshelf', 'Wall shelf over the station', 'Above the counter', '800 × 300', 'At 1,600 and 1,950 mm, for glasses and cutlery', 'nos', 2),
 ('brewer', 'Coffee batch brewer with 2 jugs', 'On the station counter', '', 'About 12 cups a batch; state make and model', 'nos', 1),
 ('waterdisp', 'Water dispenser', 'On the station counter', '', 'Chilled and ambient', 'nos', 1),
 ('milk', 'Milk warmer', 'On the station counter', '', 'Small', 'nos', 1),
]),
('H', 'Services and loose items', 'Not a place on the plan: the power, water and drains the bar needs, the lighting, and things the bartender brings.', '#6a5d4e', [
 ('power', 'Power points', 'Across the bar and the station', '', 'Ice machine, glasswasher, cooler, flash chiller, POS, TV, neon, LED strips, coffee brewer, water dispenser; the chillers and POS on the power backup', 'nos', 10),
 ('water', 'Water points with isolation valves', 'Bar sink, glasswasher, ice machine, coffee brewer', '', 'Hot and cold at the sink and glasswasher; filtered cold at the ice machine', 'nos', 4),
 ('drain', 'Drain points to the grey-water line', 'Bar sink and ice basin, glasswasher, ice machine', '', 'Never to the biodigester', 'nos', 4),
 ('led', 'Warm LED strips and downlights', 'Under both long sides of the counter; 4 over the marble', '', '2,200 K', 'lot', 1),
 ('smallware', 'Bar smallware', 'Bartender brings or buys', '', 'To the bar consultant\'s list: shakers, jiggers, strainers, muddlers, bar mats', 'lot', 1),
 ('glass', 'Glassware', 'Per the drinks menu', '', 'Pint, gose, whisky, highball, coupe, shot; see the crockery list (breweries often give branded pint glasses)', 'lot', 1),
]),
]

import re
def _m(n): return f'{float(n.replace(",", "")) / 1000:.2f}'
def to_m_size(t):      # every number in a size string is millimetres -> metres
    return re.sub(r'\d[\d,]*', lambda m: _m(m.group(0)), t)
def to_m_text(t):      # only numbers followed by "mm" (also lists like "1,600 and 1,950 mm" or "960 to 2,380 mm")
    def lst(m): return re.sub(r'\d[\d,]*', lambda x: _m(x.group(0)), m.group(1)) + ' m'
    return re.sub(r'((?:\d[\d,]*\s+(?:and|to)\s+)*\d[\d,]*)\s*mm\b', lst, t)
SECTIONS = [(sec, title, to_m_text(note), col, [(k, item, to_m_text(wh), to_m_size(sz), to_m_text(sp), u, q) for (k, item, wh, sz, sp, u, q) in rows]) for sec, title, note, col, rows in SECTIONS]

ITEMS = [(k, i, sz, sp, u, q, sec) for sec, _t, _n, _c, rows in SECTIONS for (k, i, wh, sz, sp, u, q) in rows]
NUM = {r[0]: n for n, r in enumerate(ITEMS, 1)}
WHERE = {k: wh for _s, _t, _n, _c, rows in SECTIONS for (k, i, wh, sz, sp, u, q) in rows}


def numbered():
    for sec, title, note, col, rows in SECTIONS:
        yield ('sec', sec, title, note)
        for (k, item, where, size, spec, unit, qty) in rows: yield ('item', NUM[k], item, where, size, spec, unit, qty)

def fmt(q): return f'{q:g}' if isinstance(q, float) else str(q)

def write_csv(path):
    with open(path, 'w', newline='') as f:
        w = csv.writer(f); w.writerow(['No.', 'Item', 'Where it is', 'Size W × D × H (m)', 'What it is / specification', 'Unit', 'Qty', 'Rate (INR)', 'Amount (INR)', 'Make / model / remarks'])
        for r in numbered():
            if r[0] == 'sec': w.writerow([r[1], r[2], '', '', r[3], '', '', '', '', ''])
            else: w.writerow([r[1], r[2], r[3], r[4], r[5], r[6], fmt(r[7]), '', '', ''])

def write_xlsx(path):
    from openpyxl import Workbook
    from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
    wb = Workbook(); ws = wb.active; ws.title = 'Bar BOQ'
    thin = Side(style='thin', color='BBBBBB'); box = Border(left=thin, right=thin, top=thin, bottom=thin)
    head = PatternFill('solid', fgColor='2A2420'); band = PatternFill('solid', fgColor='EFE6D3'); inp = PatternFill('solid', fgColor='FFF9E0'); NC = 10
    ws['A1'] = 'Vendor list · bar and server station · Betalbatim pub'; ws['A1'].font = Font(bold=True, size=14)
    ws['A2'] = 'Shop 4, Tulip Residency, Gandaulim, Salcete, South Goa. Bar on the left wall as in the Simplex model. Grouped by area of the bar (A to H); the same letters and item numbers are on the A3 drawing. Sizes in metres (width × depth × height), the space available; measure on site.'
    ws['A3'] = 'Fill the yellow cells (rate, make/model, remarks). Amounts and totals calculate. Rates ex-GST; freight, installation and the GST rate go in the lines at the bottom.'
    for r in (2, 3): ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=NC); ws.cell(r, 1).alignment = Alignment(wrap_text=True, vertical='top'); ws.row_dimensions[r].height = 32
    for i, h in enumerate(['No.', 'Item', 'Where it is', 'Size W × D × H (m)', 'What it is / specification', 'Unit', 'Qty', 'Rate (₹)', 'Amount (₹)', 'Make / model / remarks'], 1):
        c = ws.cell(5, i, h); c.font = Font(bold=True, color='FFFFFF'); c.fill = head; c.alignment = Alignment(vertical='center', wrap_text=True); c.border = box
    r = 6; subs = []
    for sec, title, note, col, rows in SECTIONS:
        ws.cell(r, 1, sec); ws.cell(r, 2, title); ws.cell(r, 5, note)
        for i in range(1, NC + 1): c = ws.cell(r, i); c.fill = band; c.font = Font(bold=True); c.border = box; c.alignment = Alignment(wrap_text=True, vertical='top')
        ws.row_dimensions[r].height = 46; r += 1; first = r
        for (k, item, where, size, spec, unit, qty) in rows:
            for i, v in enumerate([NUM[k], item, where, size, spec, unit, qty, None, f'=IF(H{r}="","",G{r}*H{r})', None], 1):
                c = ws.cell(r, i, v); c.border = box; c.alignment = Alignment(wrap_text=True, vertical='top')
            for i in (8, 10): ws.cell(r, i).fill = inp
            ws.cell(r, 8).number_format = '#,##0.00'; ws.cell(r, 9).number_format = '#,##0.00'; ws.cell(r, 7).number_format = '0.0#'
            r += 1
        ws.cell(r, 2, f'Subtotal, section {sec}'); ws.cell(r, 9, f'=SUM(I{first}:I{r-1})'); subs.append(r)
        for i in range(1, NC + 1): c = ws.cell(r, i); c.font = Font(bold=True); c.border = box
        ws.cell(r, 9).number_format = '#,##0.00'; r += 2
    ws.cell(r, 2, 'Total of all sections (ex-GST)'); ws.cell(r, 9, '=' + '+'.join(f'I{x}' for x in subs)); tot = r; r += 1
    ws.cell(r, 2, 'Freight and unloading to Betalbatim'); ws.cell(r, 9).fill = inp; fr = r; r += 1
    ws.cell(r, 2, 'Installation and connections not included above'); ws.cell(r, 9).fill = inp; ins = r; r += 1
    ws.cell(r, 2, 'GST rate (%)'); ws.cell(r, 9, 18).fill = inp; gr = r; r += 1
    ws.cell(r, 2, 'GST'); ws.cell(r, 9, f'=ROUND((I{tot}+I{fr}+I{ins})*I{gr}/100,2)'); gs = r; r += 1
    ws.cell(r, 2, 'Grand total including GST'); ws.cell(r, 9, f'=I{tot}+I{fr}+I{ins}+I{gs}'); gt = r
    for x in range(tot, r + 1):
        ws.cell(x, 2).font = Font(bold=True); ws.cell(x, 9).number_format = '#,##0.00'; ws.cell(x, 9).font = Font(bold=True)
    ws.cell(gt, 2).fill = band; ws.cell(gt, 9).fill = band
    for c, w in zip('ABCDEFGHIJ', (6, 38, 34, 22, 52, 6, 7, 12, 14, 26)): ws.column_dimensions[c].width = w
    ws.freeze_panes = 'C6'; ws.page_setup.orientation = 'landscape'; ws.page_setup.paperSize = ws.PAPERSIZE_A4; ws.page_setup.fitToWidth = 1; ws.page_setup.fitToHeight = 0
    ws.sheet_properties.pageSetUpPr.fitToPage = True; ws.print_title_rows = '5:5'
    wb.save(path)

def drawing_svg():
    """1:25 plan of the bar and the server station: items numbered and named, sizes in m. Leaders run to a label column on the right."""
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
    COL = {sec: col for sec, _t, _n, col, _r in SECTIONS}
    R(0.85, 0.87, 3.2, 3.6, '#a8741a', '#a8741a', 0.2)                                      # beer font on the counter
    # server station
    R(1.95, 2.45, 5.45, 6.25, '#cfd7b2')
    def zone(sec, xa, xb, za, zb, tabx, tabz):
        R(xa, xb, za, zb, 'none', COL[sec], 0.9)
        a, b = s.P(tabx, tabz); s.add(f'<rect x="{a-3.3:.2f}" y="{b-3.3:.2f}" width="6.6" height="6.6" rx="1.2" fill="{COL[sec]}"/><text x="{a:.2f}" y="{b+1.4:.2f}" font-size="4.2" font-weight="700" fill="#fff" text-anchor="middle">{sec}</text>')
    zone('A', 0.3, 1.25, 2.9, 5.27, 0.78, 5.5); zone('B', 0.57, 1.24, 3.02, 4.16, 1.45, 3.6); zone('C', 0.65, 1.24, 4.18, 5.2, 1.45, 4.75)
    zone('D', 2.03, 2.47, 4.78, 5.4, 2.85, 5.15); zone('E', 1.88, 2.47, 3.8, 4.55, 1.62, 4.18); zone('F', 2.03, 2.47, 2.76, 3.28, 2.85, 3.02); zone('G', 1.93, 2.47, 5.43, 6.27, 2.85, 5.85)
    def tag(k, x, z, col=INK):
        a, b = s.P(x, z); s.add(f'<circle cx="{a:.2f}" cy="{b:.2f}" r="2.3" fill="#fff" stroke="{col}" stroke-width="0.3"/><text x="{a:.2f}" y="{b+0.9:.2f}" font-size="2.4" font-weight="700" fill="{col}" text-anchor="middle">{NUM[k]}</text>')
    placed = {'counter': (0.5, 3.0), 'stool': (0.13, 3.87), 'rack': (0.7, 5.1),
              'font': (0.86, 3.42), 'kegcab': (0.85, 3.95), 'keg': (0.77, 3.21), 'chiller': (0.92, 3.72), 'beerline': (0.72, 3.62), 'co2': (2.38, 3.6), 'co2alarm': (2.55, 3.65),
              'workunit': (1.1, 4.3), 'sink': (1.1, 4.75), 'speedrail': (1.1, 5.1), 'ice': (0.85, 4.9),
              'backbar': (2.25, 5.25), 'display': (2.55, 4.3), 'infusion': (2.15, 3.5), 'soju': (2.55, 5.1), 'tv': (2.55, 3.4), 'neon': (2.55, 3.0),
              'builtin': (1.97, 3.9), 'gw': (2.17, 4.8), 'cooler': (2.17, 4.17), 'pos': (2.35, 3.05), 'drawer': (2.15, 2.9),
              'station': (2.2, 6.1), 'stshelf': (2.55, 5.85), 'brewer': (2.3, 5.8), 'waterdisp': (2.05, 5.8), 'milk': (2.05, 5.6)}
    SEC = {it[0]: it[6] for it in ITEMS}
    for k, (x, z) in placed.items(): tag(k, x, z, COL[SEC[k]])
    col_x, ty = 138.0, 22.0
    for sec, title, note, col, rows in SECTIONS:
        s.add(f'<rect x="{col_x-1}" y="{ty-3.2:.1f}" width="152" height="4.4" fill="{col}" fill-opacity="0.16"/><rect x="{col_x-1}" y="{ty-3.2:.1f}" width="1.2" height="4.4" fill="{col}"/>'
              f'<text x="{col_x+1.5}" y="{ty:.1f}" font-size="3" font-weight="700" fill="{col}">{sec}   {html.escape(title.upper())}</text>'); ty += 3.6
        for line in wrap(note, 96):
            s.add(f'<text x="{col_x+1.5}" y="{ty+1:.1f}" font-size="2.4" fill="{MUT}">{html.escape(line)}</text>'); ty += 3.1
        ty += 0.6
        for (k, item, where, size, spec, unit, qty) in rows:
            sz = f' · {size}' if size else ''
            s.add(f'<text x="{col_x+1.5}" y="{ty+0.9:.1f}" font-size="2.5" fill="{INK}"><tspan font-weight="700">{NUM[k]}</tspan>   {html.escape(item)}<tspan fill="{MUT}">{html.escape(sz)}</tspan></text>'); ty += 3.6
        ty += 2.8
    missing = [NUM[k] for k, *_ in ITEMS if k not in placed]
    s.add(f'<text x="{col_x}" y="{ty:.1f}" font-size="2.5" fill="{MUT}">No tag on the plan: {", ".join(map(str, missing))} (services, lighting and loose items, area H).</text>')
    s.vdim(2.84, 2.72, 5.37, 'back bar 2.65', RED); s.vdim(-0.3, 2.94, 5.22, 'counter 2.28 incl. front', RED)
    s.hdim(1.2, 1.9, 5.5, 'bartender aisle 0.85', RED); s.hdim(0.35, 1.2, 2.82, '0.85', RED)
    s.text(0.22, 6.2, 'Window tables are in front of the bar (left, toward the shopfront); the entry is at the bottom of the plan.', 2.5, MUT, anchor='start') if False else None
    s.text(1.0, 2.3, 'toward the shopfront and the entry', 2.5, MUT)
    by_ = max(208.0, ty + 4)                                            # scale bar and reading note go below whichever is lower, the plan or the key
    bx_ = 22.0
    s.add(f'<rect x="{bx_}" y="{by_}" width="40" height="1.6" fill="{INK}"/><rect x="{bx_+40}" y="{by_}" width="40" height="1.6" fill="none" stroke="{INK}" stroke-width="0.2"/>'
          f'<text x="{bx_}" y="{by_+5}" font-size="2.5" fill="{INK}">0</text><text x="{bx_+40}" y="{by_+5}" font-size="2.5" text-anchor="middle" fill="{INK}">1 m</text><text x="{bx_+80}" y="{by_+5}" font-size="2.5" text-anchor="middle" fill="{INK}">2 m</text>'
          f'<text x="{bx_+86}" y="{by_+1.8}" font-size="2.9" font-weight="700" fill="{INK}">PLAN 1:25 on A3, dimensions in metres</text>')
    note = 'How to read it: the coloured letter tabs A to G are the areas of the bar; the numbered circles are the items in the list. The left wall is at the left of the plan, the bar island to its right. Dashed: the glass rack above and the ice machine.'
    for i, line in enumerate(wrap(note, 150)): s.add(f'<text x="22" y="{by_+10+i*3.2:.1f}" font-size="2.5" fill="{MUT}">{html.escape(line)}</text>')
    H = by_ + 10 + 3.2 * 2 + 4
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="291mm" height="{H-12:.1f}mm" viewBox="0 12 291 {H-12:.1f}" font-family="\'IBM Plex Sans\', Helvetica, Arial, sans-serif"><rect x="0" y="12" width="291" height="{H-12:.1f}" fill="#fbf7ef"/>{"".join(s.o)}</svg>'

def wrap(t, n):
    out, cur = [], ''
    for w in t.split():
        if len(cur) + len(w) + 1 > n: out.append(cur); cur = w
        else: cur = (cur + ' ' + w).strip()
    return out + ([cur] if cur else [])

def page():
    esc = html.escape; body = []
    COL = {sec: col for sec, _t, _n, col, _r in SECTIONS}
    for r in numbered():
        if r[0] == 'sec': body.append(f'<tr class="sec" style="--c:{COL[r[1]]}"><th class="L">{r[1]}</th><th colspan="8">{esc(r[2])}<small>{esc(r[3])}</small></th></tr>')
        else: body.append(f'<tr><td class="no">{r[1]}</td><td><b>{esc(r[2])}</b><small>{esc(r[3])}</small></td><td class="sz">{esc(r[4])}</td><td>{esc(r[5])}</td><td>{r[6]}</td><td class="n">{fmt(r[7])}</td><td class="blank"></td><td class="blank"></td><td class="blank"></td></tr>')
    css = """
/* Layout: A3 portrait when printed (plan on top at 1:25, list below); a scrolling page on screen. Each area of the bar has its own colour band */
@page{size:297mm 420mm;margin:0}
:root{--paper:#fbf7ef;--ink:#2a2420;--muted:#6a5d4e;--rule:#d9cbb3;--accent:#b23a1e;--chip:#fffdf8;--display:'Bricolage Grotesque','Segoe UI',sans-serif;--body:'IBM Plex Sans','Helvetica Neue',Arial,sans-serif;--mono:'IBM Plex Mono',ui-monospace,Menlo,monospace}
html,body{margin:0;background:var(--paper);color:var(--ink);font-family:var(--body)}
.sheet{max-width:297mm;margin:0 auto;padding:4mm 3mm 6mm}
.hd{display:flex;justify-content:space-between;align-items:flex-end;gap:12px;border-bottom:.35mm solid var(--ink);padding-bottom:2mm}
.hd h1{font:700 7mm/1 var(--display);margin:0} .hd p{margin:1mm 0 0;font-size:2.6mm;color:var(--muted)} .hd .r{text-align:right;font-size:2.6mm;color:var(--muted)}
svg{display:block;width:100%;height:auto}
.bar{display:flex;flex-wrap:wrap;gap:8px;margin:8px 0} .bar a{font:600 13px var(--body);color:var(--ink);background:var(--chip);border:1px solid var(--rule);border-radius:8px;padding:9px 12px;text-decoration:none} .bar a.pri{background:var(--ink);color:var(--paper);border-color:var(--ink)}
h2{font:700 4.4mm/1.2 var(--display);margin:3mm 0 1.5mm}
.tw{overflow-x:auto}
table{border-collapse:collapse;width:100%;min-width:980px;font-size:2.7mm;line-height:1.3}
th,td{padding:.9mm 1.4mm;border-top:.2mm solid var(--rule);vertical-align:top;text-align:left}
thead th{background:var(--ink);color:var(--paper);font:600 2.5mm var(--mono);border-top:0;white-space:nowrap}
tr.sec th{background:color-mix(in srgb,var(--c) 14%,#fbf7ef);font:700 3mm var(--body);border-top:.5mm solid var(--c)} tr.sec th.L{background:var(--c);color:#fff;text-align:center;font-size:4mm}
tr.sec small{display:block;font:400 2.5mm var(--body);color:var(--muted)} td small{display:block;color:var(--muted);font-size:2.4mm;margin-top:.3mm}
td.no{font:600 2.5mm var(--mono)} td.sz{font:500 2.5mm var(--mono)} td.n{text-align:right;font-family:var(--mono)} td.blank{background:#fffdf0;width:11mm}
thead{display:table-header-group} tr{break-inside:avoid} .foot{font-size:2.6mm;color:var(--muted);margin-top:2mm}
@media print{.bar{display:none} .sheet{padding:4mm 3mm} table{min-width:0}}
@media (max-width:700px){.hd{flex-direction:column;align-items:flex-start} .hd h1{font-size:26px} .hd p,.hd .r{font-size:12px} table{font-size:13px} th,td{padding:6px 8px} h2{font-size:20px} td small,tr.sec small{font-size:12px}}
"""
    return ('<!doctype html>\n<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"><title>Bar vendor list · Betalbatim Pub</title>\n'
            '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,700&family=IBM+Plex+Sans:wght@400;500;600;700&family=IBM+Plex+Mono:wght@500&display=swap">\n'
            f'<style>{css}</style></head><body><div class="sheet">\n'
            '<div class="hd"><div><h1>Bar and server station: vendor list</h1><p>Grouped by area of the bar, A to H. Plan at 1:25 on A3 (print at 100%), sizes in metres. From the Simplex model. Shop 4, Tulip Residency, Gandaulim, South Goa</p></div><div class="r">Betalbatim pub · Simplex · Concept 27<br>singhgenics.github.io/Simplex/boq-bar.html</div></div>\n'
            '<div class="bar"><a class="pri" href="plans/bar-drawing-boq.pdf" target="_blank" rel="noopener">A3 PDF: drawing + list</a><a href="plans/bar-boq.xlsx">Excel (rates and totals calculate)</a><a href="plans/bar-boq.csv">CSV</a><a href="boq.html">Kitchen BOQ</a><a href="./">3D model</a></div>\n'
            f'{drawing_svg()}\n<h2>Vendor list ({len(ITEMS)} lines in {len(SECTIONS)} areas)</h2>\n'
            '<div class="tw"><table><thead><tr><th>Area</th><th>Item and where it is</th><th>Size W × D × H (m)</th><th>What it is / specification</th><th>Unit</th><th>Qty</th><th>Rate ₹</th><th>Amount ₹</th><th>Make / model</th></tr></thead>'
            f'<tbody>{"".join(body)}</tbody></table></div>\n'
            '<p class="foot">Quantities and sizes are the space available, from the model; the vendor measures on site and states make, model, kW or litres, price ex-GST, delivery, installation, lead time, warranty and who services it in Goa. The Goa excise licence and fire NOC come before any draught installation. Concept drawings for briefing suppliers, not construction drawings.</p>\n</div></body></html>\n')

if __name__ == '__main__':
    write_csv('plans/bar-boq.csv'); write_xlsx('plans/bar-boq.xlsx')
    open('boq-bar.html', 'w').write(page()); print(len(ITEMS), 'lines; boq-bar.html, plans/bar-boq.xlsx, .csv written')
