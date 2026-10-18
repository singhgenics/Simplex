"""Bar equipment only, for the kitchen fabricator: the machines and the stainless pieces, with W × D × H in metres.
Everything else in the bar (counter, back bar, shelves, glass rack, stools, TV, neon, POS nook, lighting, services) stays in the full bar list (tools/boq_bar.py).
Sizes come from boq_bar.py, which takes them from the Simplex model. Usage: python3 tools/boq_bar_equipment.py -> boq-bar-equipment.html, plans/bar-equipment.xlsx, plans/bar-equipment.csv (PDF: print the page, A4 portrait)."""
import os, sys, csv, html
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import boq_bar as B
import kitchen_sheets as K
from kitchen_sheets import KZ, INK, MUT, RED, BLU, GRN

DATA = {k: (item, where, size, spec, unit, qty) for _s, _t, _n, _c, rows in B.SECTIONS for (k, item, where, size, spec, unit, qty) in rows}

# (letter, title, note, [(key, size override, note override)])  W × D × H in metres; '' size means the model has no size
GROUPS = [
 ('1', 'Bar equipment (machines)', 'To be supplied by the equipment vendor. Sizes are the space available in the bar: do not quote a wider unit.', [
  ('chiller', None, None), ('gw', None, None), ('cooler', None, None), ('ice', None, None),
  ('brewer', 'on the 0.80 × 0.50 counter', 'State the make, model and size'), ('waterdisp', 'on the 0.80 × 0.50 counter', 'State the make, model and size'), ('milk', 'on the 0.80 × 0.50 counter', 'State the make, model and size'),
 ]),
 ('2', 'Stainless pieces the fabricator can also make', 'Stainless steel 304 fabrication, the same as the kitchen work. Drawn in the model; the fabricator measures on site.', [
  ('workunit', None, None), ('sink', None, None), ('speedrail', '1.06 long (depth and height to suit the unit)', None),
 ]),
 ('3', 'Draught gear (usually supplied by the brewery; list for fitting space only)', 'Do not price these unless the brewery asks you to; the fabricator needs the sizes to leave room.', [
  ('font', '0.09 × 0.09 × 0.42', None), ('keg', None, None), ('co2', None, 'Cylinder with regulator; the gas supplier fills it'),
 ]),
]

def rows():
    n = 0
    for letter, title, note, items in GROUPS:
        out = []
        for key, size, note2 in items:
            item, where, sz, spec, unit, qty = DATA[key]; n += 1
            if key == 'keg': sz = '0.24 × 0.24 × 0.42'
            if key == 'co2': sz = '0.15 × 0.15 × 0.67'
            out.append((n, item, where, size or sz, note2 or spec, unit, qty))
        yield letter, title, note, out

def fmt(q): return f'{q:g}' if isinstance(q, float) else str(q)

def write_csv(path):
    with open(path, 'w', newline='') as f:
        w = csv.writer(f); w.writerow(['No.', 'Item', 'Where it goes', 'Size W × D × H (m)', 'Notes', 'Unit', 'Qty', 'Rate (INR)', 'Amount (INR)', 'Make / model'])
        for letter, title, note, out in rows():
            w.writerow(['', f'{letter}. {title}', '', '', note, '', '', '', '', ''])
            for r in out: w.writerow([r[0], r[1], r[2], r[3], r[4], r[5], fmt(r[6]), '', '', ''])

def write_xlsx(path):
    from openpyxl import Workbook
    from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
    wb = Workbook(); ws = wb.active; ws.title = 'Bar equipment'
    thin = Side(style='thin', color='BBBBBB'); box = Border(left=thin, right=thin, top=thin, bottom=thin)
    head = PatternFill('solid', fgColor='2A2420'); band = PatternFill('solid', fgColor='EFE6D3'); inp = PatternFill('solid', fgColor='FFF9E0'); NC = 10
    ws['A1'] = 'Bar equipment · Betalbatim pub'; ws['A1'].font = Font(bold=True, size=14)
    ws['A2'] = 'Shop 4, Tulip Residency, Gandaulim, Salcete, South Goa. Equipment and stainless pieces only; the rest of the bar is in the full bar list. Sizes W × D × H in metres, the space available. Fill the yellow cells; amounts and totals calculate; rates ex-GST.'
    ws.merge_cells('A2:J2'); ws['A2'].alignment = Alignment(wrap_text=True, vertical='top'); ws.row_dimensions[2].height = 34
    for i, h in enumerate(['No.', 'Item', 'Where it goes', 'Size W × D × H (m)', 'Notes', 'Unit', 'Qty', 'Rate (₹)', 'Amount (₹)', 'Make / model'], 1):
        c = ws.cell(4, i, h); c.font = Font(bold=True, color='FFFFFF'); c.fill = head; c.border = box; c.alignment = Alignment(wrap_text=True, vertical='center')
    r = 5; subs = []
    for letter, title, note, out in rows():
        ws.cell(r, 1, letter); ws.cell(r, 2, title); ws.cell(r, 5, note)
        for i in range(1, NC + 1): c = ws.cell(r, i); c.fill = band; c.font = Font(bold=True); c.border = box; c.alignment = Alignment(wrap_text=True, vertical='top')
        ws.row_dimensions[r].height = 36; r += 1; first = r
        for row in out:
            for i, v in enumerate([row[0], row[1], row[2], row[3], row[4], row[5], row[6], None, f'=IF(H{r}="","",G{r}*H{r})', None], 1):
                c = ws.cell(r, i, v); c.border = box; c.alignment = Alignment(wrap_text=True, vertical='top')
            for i in (8, 10): ws.cell(r, i).fill = inp
            ws.cell(r, 8).number_format = '#,##0.00'; ws.cell(r, 9).number_format = '#,##0.00'
            r += 1
        ws.cell(r, 2, f'Subtotal, group {letter}'); ws.cell(r, 9, f'=SUM(I{first}:I{r-1})'); subs.append(r)
        for i in range(1, NC + 1): c = ws.cell(r, i); c.font = Font(bold=True); c.border = box
        ws.cell(r, 9).number_format = '#,##0.00'; r += 2
    ws.cell(r, 2, 'Total (ex-GST)'); ws.cell(r, 9, '=' + '+'.join(f'I{x}' for x in subs)); tot = r; r += 1
    ws.cell(r, 2, 'Freight and unloading'); ws.cell(r, 9).fill = inp; fr = r; r += 1
    ws.cell(r, 2, 'Installation and connections'); ws.cell(r, 9).fill = inp; ins = r; r += 1
    ws.cell(r, 2, 'GST rate (%)'); ws.cell(r, 9, 18).fill = inp; gr = r; r += 1
    ws.cell(r, 2, 'GST'); ws.cell(r, 9, f'=ROUND((I{tot}+I{fr}+I{ins})*I{gr}/100,2)'); gs = r; r += 1
    ws.cell(r, 2, 'Grand total including GST'); ws.cell(r, 9, f'=I{tot}+I{fr}+I{ins}+I{gs}')
    for x in range(tot, r + 1): ws.cell(x, 2).font = Font(bold=True); ws.cell(x, 9).number_format = '#,##0.00'; ws.cell(x, 9).font = Font(bold=True)
    for c, w in zip('ABCDEFGHIJ', (6, 36, 34, 24, 44, 6, 6, 12, 14, 24)): ws.column_dimensions[c].width = w
    ws.freeze_panes = 'C5'; ws.page_setup.orientation = 'landscape'; ws.page_setup.paperSize = ws.PAPERSIZE_A4; ws.page_setup.fitToWidth = 1; ws.page_setup.fitToHeight = 0
    ws.sheet_properties.pageSetUpPr.fitToPage = True
    wb.save(path)

GCOL = {'1': '#2f6f9f', '2': '#3f6a3a', '3': '#a8741a'}
# where each equipment item sits on the plan (x, z in metres, from tools/plan.py); the number tag goes here
AT = {'chiller': (0.92, 3.72), 'gw': (2.17, 4.8), 'cooler': (2.17, 4.17), 'ice': (0.85, 4.9), 'brewer': (2.3, 5.8), 'waterdisp': (2.05, 5.8), 'milk': (2.05, 5.6),
      'workunit': (1.1, 4.3), 'sink': (1.1, 4.75), 'speedrail': (1.1, 5.1), 'font': (0.86, 3.42), 'keg': (0.77, 3.21), 'co2': (2.38, 3.6)}

def drawing_svg():
    """1:25 plan of the bar: the equipment numbered (same numbers as the list below), everything else drawn plain and unnumbered, in metres."""
    s = K.Sheet(14, 14, 2.65, 6.45)
    def R(xa, xb, za, zb, fill='none', stroke='#9aa0a5', sw=0.3, dash=None): s.rect(xa, xb, za, zb, fill, stroke, sw, dash)
    R(2.45, 2.65, 2.2, 6.45, '#4a4038', '#4a4038', 0.2)
    R(-0.1, 2.45, KZ, KZ + 0.1, '#d8c6ac', '#a8987c', 0.2); s.text(0.5, KZ + 0.05, 'kitchen wall (door to the kitchen)', 2.5, MUT)
    # the rest of the bar, plain grey (labelled in words, no numbers)
    R(2.05, 2.45, 2.72, 5.37, '#ecebe6'); s.text(2.25, 5.0, 'back bar', 2.5, MUT, rot=90)
    R(0.35, 1.2, 2.94, 5.22, '#f1ede4'); s.text(0.4, 5.3, 'bar counter', 2.5, MUT, anchor='start') if False else s.text(0.78, 2.78, 'bar counter', 2.5, MUT)
    for z in (3.27, 3.87, 4.47, 5.07): s.circ(0.13, z, 0.21, '#f1ede4', '#9aa0a5', 0.3)
    s.text(0.13, 5.4, 'stools', 2.5, MUT)
    R(0.35, 1.1, 3.12, 5.12, 'none', '#9aa0a5', 0.3, '1.4 0.8'); s.text(0.7, 3.0, 'glass rack above', 2.5, MUT)
    R(2.05, 2.45, 2.78, 3.26, '#f6f1e6'); s.text(2.25, 2.98, 'POS', 2.5, MUT)
    R(1.95, 2.45, 5.45, 6.25, '#ecebe6'); s.text(2.2, 6.1, 'server station', 2.5, MUT)
    # equipment outlines, coloured by group
    G = {k: g for g, _t, _n, items in GROUPS for (k, _a, _b) in items}
    for k, (xa, xb, za, zb) in {'chiller': (0.67, 1.17, 3.66, 4.08), 'cooler': (1.9, 2.45, 3.82, 4.52), 'gw': (1.9, 2.45, 4.57, 5.02), 'ice': (0.67, 1.22, 4.64, 5.14), 'workunit': (1.0, 1.2, 4.16, 5.22),
                                'brewer': (2.15, 2.45, 5.45, 5.7)}.items():
        R(xa, xb, za, zb, 'none', GCOL[G[k]], 0.9, '1.6 0.8' if k in ('ice',) else None)
    R(0.59, 1.22, 3.04, 4.14, 'none', '#9aa0a5', 0.3); s.text(1.0, 4.1, 'keg cabinet', 2.5, MUT) if False else None
    for x, z in ((1.05, 3.21), (0.77, 3.21), (1.05, 3.49)): s.circ(x, z, 0.11, 'none', GCOL['3'], 0.9)
    R(0.85, 0.87, 3.2, 3.6, GCOL['3'], GCOL['3'], 0.2)
    NUMS = {}
    n = 0
    for _g, _t, _n, items in GROUPS:
        for (k, _a, _b) in items: n += 1; NUMS[k] = n
    for k, (x, z) in AT.items():
        a, b = s.P(x, z); c = GCOL[G[k]]
        s.add(f'<circle cx="{a:.2f}" cy="{b:.2f}" r="2.4" fill="#fff" stroke="{c}" stroke-width="0.5"/><text x="{a:.2f}" y="{b+0.9:.2f}" font-size="2.6" font-weight="700" fill="{c}" text-anchor="middle">{NUMS[k]}</text>')
    s.vdim(2.84, 2.72, 5.37, 'back bar 2.65', RED); s.vdim(-0.3, 2.94, 5.22, 'counter 2.28 incl. front', RED); s.hdim(1.2, 1.9, 5.5, 'bartender aisle 0.85', RED)
    s.text(1.0, 2.3, 'toward the shopfront and the entry', 2.5, MUT)
    # key on the right: number, name and W × D × H for every numbered item
    col_x, ty = 138.0, 22.0
    for letter, title, note, items in GROUPS:
        c = GCOL[letter]
        s.add(f'<rect x="{col_x-1}" y="{ty-3.2:.1f}" width="152" height="4.4" fill="{c}" fill-opacity="0.16"/><rect x="{col_x-1}" y="{ty-3.2:.1f}" width="1.2" height="4.4" fill="{c}"/><text x="{col_x+1.5}" y="{ty:.1f}" font-size="3" font-weight="700" fill="{c}">{html.escape(title.upper())}</text>'); ty += 5.2
        for (k, size, _n2) in items:
            item, where, sz, spec, unit, qty = DATA[k]
            sz = size or sz
            if k == 'keg': sz = '0.24 × 0.24 × 0.42'
            if k == 'co2': sz = '0.15 × 0.15 × 0.67'
            if k == 'font': sz = '0.09 × 0.09 × 0.42'
            sfx = '' if sz.startswith(('on ', 'fits', '1.06 long')) else ' m'
            s.add(f'<text x="{col_x+1.5}" y="{ty:.1f}" font-size="2.6" fill="{INK}"><tspan font-weight="700">{NUMS[k]}</tspan>   {html.escape(item)}</text><text x="{col_x+1.5}" y="{ty+3.3:.1f}" font-size="2.4" fill="{MUT}">{html.escape(sz + sfx)}</text>'); ty += 8.2
        ty += 2
    bx_, by_ = 22.0, 208.0
    s.add(f'<rect x="{bx_}" y="{by_}" width="40" height="1.6" fill="{INK}"/><rect x="{bx_+40}" y="{by_}" width="40" height="1.6" fill="none" stroke="{INK}" stroke-width="0.2"/>'
          f'<text x="{bx_}" y="{by_+5}" font-size="2.5" fill="{INK}">0</text><text x="{bx_+40}" y="{by_+5}" font-size="2.5" text-anchor="middle" fill="{INK}">1 m</text><text x="{bx_+80}" y="{by_+5}" font-size="2.5" text-anchor="middle" fill="{INK}">2 m</text>'
          f'<text x="{bx_+86}" y="{by_+1.8}" font-size="2.9" font-weight="700" fill="{INK}">PLAN 1:25 on A3, dimensions in metres</text>')
    s.add(f'<text x="22" y="219" font-size="2.5" fill="{MUT}">Each numbered circle is one item in the list below. Grey, unnumbered shapes are the rest of the bar (counter, back bar, stools, POS, server station); they are not part of this list. Left wall at the left of the plan.</text>')
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="291mm" height="208mm" viewBox="0 12 291 224" font-family="\'IBM Plex Sans\', Helvetica, Arial, sans-serif"><rect x="0" y="12" width="291" height="224" fill="#fbf7ef"/>{"".join(s.o)}</svg>'

def page():
    esc = html.escape; body = []
    for letter, title, note, out in rows():
        body.append(f'<tr class="sec"><th>{letter}</th><th colspan="6">{esc(title)}<small>{esc(note)}</small></th></tr>')
        for r in out:
            body.append(f'<tr><td class="no">{r[0]}</td><td><b>{esc(r[1])}</b><small>{esc(r[2])}</small></td><td class="sz">{esc(r[3])}</td><td>{esc(r[4])}</td><td class="n">{fmt(r[6])}</td><td class="blank"></td><td class="blank"></td></tr>')
    css = """
/* Layout: one A4 portrait page when printed; a scrolling page on screen */
@page{size:297mm 420mm;margin:0}
:root{--paper:#fbf7ef;--ink:#2a2420;--muted:#6a5d4e;--rule:#d9cbb3;--accent:#b23a1e;--chip:#fffdf8;--display:'Bricolage Grotesque','Segoe UI',sans-serif;--body:'IBM Plex Sans','Helvetica Neue',Arial,sans-serif;--mono:'IBM Plex Mono',ui-monospace,Menlo,monospace}
body{background:var(--paper);color:var(--ink);font-family:var(--body);margin:0;line-height:1.4}
.wrap{max-width:297mm;margin:0 auto;padding:4mm 3mm 6mm} svg{display:block;width:100%;height:auto}
h1{font:700 28px/1.05 var(--display);margin:0 0 6px} .lede{margin:0 0 10px;color:var(--muted);font-size:14px}
.bar{display:flex;flex-wrap:wrap;gap:8px;margin:10px 0} .bar a{font:600 13px var(--body);color:var(--ink);background:var(--chip);border:1px solid var(--rule);border-radius:8px;padding:9px 12px;text-decoration:none} .bar a.pri{background:var(--ink);color:var(--paper);border-color:var(--ink)}
.tw{overflow-x:auto;border:1px solid var(--rule);border-radius:8px;background:var(--chip)}
table{border-collapse:collapse;width:100%;min-width:700px;font-size:13px}
th,td{padding:6px 9px;border-top:1px solid var(--rule);vertical-align:top;text-align:left}
tr.sec th{background:#efe6d3;font:700 14px var(--body)} tr.sec small,td small{display:block;font:400 12px var(--body);color:var(--muted);margin-top:2px}
td.no{font:600 12px var(--mono)} td.sz{font:500 13px var(--mono)} td.n{text-align:right;font-family:var(--mono)} td.blank{background:#fffdf0;min-width:70px} th:nth-child(2){width:26%} th:nth-child(3){width:16%} th:nth-child(4){width:34%}
thead th{background:var(--ink);color:var(--paper);font:600 11.5px var(--mono);white-space:nowrap}
@media print{.bar{display:none} body{background:var(--paper)} .wrap{padding:4mm 3mm} .tw{border:0;overflow:visible} table{min-width:0;font-size:10pt} td.blank{min-width:0;width:9%} th,td{padding:5px 8px} tr{break-inside:avoid}}
"""
    return ('<!doctype html>\n<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"><title>Bar equipment · Betalbatim Pub</title>\n'
            '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,700&family=IBM+Plex+Sans:wght@400;500;600;700&family=IBM+Plex+Mono:wght@500&display=swap">\n'
            f'<style>{css}</style></head><body><div class="wrap">\n<h1>Bar equipment: layout and list</h1>\n'
            '<p class="lede">Equipment and stainless pieces for the bar, for the fabricator. Sizes are W × D × H in metres, the space available in the bar, from the Simplex model. The rest of the bar (counter, back bar, shelves, glass rack, stools, POS nook, lighting, services) is in the <a href="boq-bar.html">full bar list</a>. Shop 4, Tulip Residency, Gandaulim, South Goa.</p>\n'
            '<div class="bar"><a class="pri" href="plans/bar-equipment.pdf" target="_blank" rel="noopener">A3 PDF: layout + list</a><a href="plans/bar-equipment.xlsx">Excel (rates and totals calculate)</a><a href="plans/bar-equipment.csv">CSV</a><a href="boq-bar.html">Full bar list</a></div>\n'
            f'{drawing_svg()}\n<div class="tw"><table><thead><tr><th>No.</th><th>Item and where it goes</th><th>Size W × D × H (m)</th><th>Notes</th><th>Qty</th><th>Rate ₹</th><th>Make / model</th></tr></thead>'
            f'<tbody>{"".join(body)}</tbody></table></div>\n'
            '<p class="lede" style="margin-top:10px">Concept sizes for pricing, not construction drawings. State the make, model, kW or litres, price ex-GST, delivery, installation, lead time, warranty and who services it in Goa. The Goa excise licence comes before any draught installation.</p>\n</div></body></html>\n')

if __name__ == '__main__':
    write_csv('plans/bar-equipment.csv'); write_xlsx('plans/bar-equipment.xlsx')
    open('boq-bar-equipment.html', 'w').write(page()); print('boq-bar-equipment.html, plans/bar-equipment.xlsx, .csv written')
