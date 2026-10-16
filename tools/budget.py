"""Setup budget for the pub, in two phases, and the budget page.
Phase 1 = bought before opening. Phase 2 = bought after opening, from the first months' takings.
Figures are rough Goa ranges in rupees lakh (floor = second-hand / hard bargaining on every line; likely = ordinary new quotes).
They are the owner's planning figures, not quotes. Usage: python3 tools/budget.py  ->  budget.html (and prints the totals)
"""
import html, sys
BUDGET_LOW, BUDGET_HIGH = 12.0, 13.0      # whole project, including the backup
FIXED = 1.11                              # monthly fixed costs (rent 40k + chef 25k + helper 13k + server 12k + utilities etc.), 5 Oct scenario
RESERVE_MONTHS = 3

P1 = [
 ('Kitchen: services', [
  ('Gas: 4 × 19 kg cage, copper, solenoid valve, valves, leak detector', 0.45, 0.65, 'Licensed gas contractor; fire NOC'),
  ('Hood, exhaust fan, ducting, fresh-air fan, ESP + carbon filter', 1.00, 1.40, 'The side exhaust needs the ESP to be approvable'),
  ('Plumbing: drains, grease trap, hand-wash basins, veg sink (existing water supply)', 0.40, 0.65, 'No sump or softener yet'),
  ('35 L water heater', 0.08, 0.12, ''),
  ('Electrical board and kitchen + bar power points', 0.60, 0.90, ''),
  ('Dining AC: one 2 TR split + ceiling fans', 0.55, 0.75, 'Second split is phase 2'),
  ('Cement-board ceiling, double-acting door, rear door closer', 0.20, 0.35, ''),
 ]),
 ('Kitchen: equipment', [
  ('Steel benches, dish table, sinks, shelving, pass', 0.80, 1.20, 'Local fabricator; free layout drawing'),
  ('Wok range (2 burners), steamer, stock range', 0.65, 1.00, 'Second-hand or Chinese-made'),
  ('Twin-tank fryer', 0.20, 0.35, 'Second-hand'),
  ('Cold: one 2-door reach-in + the under-counter freezer in the veg bench', 0.55, 0.90, 'Second-hand reach-ins are common at season end'),
  ('Woks, pans, steamer baskets, food pans, knives, boards, rice cookers, mortar', 0.35, 0.55, 'The chef writes the list'),
  ('Hood fire suppression with gas cut-off, Class K extinguisher, blanket, heat detector', 0.30, 0.50, 'Needed for the fire NOC'),
 ]),
 ('Bar', [
  ('Bar counter, back bar, POS nook (timber, no onyx front)', 0.90, 1.40, ''),
  ('3 taps and keg cabinet with flash chiller (brewery lends the draught gear)', 0.25, 0.60, 'Get the loan in writing'),
  ('Back bar bottle chiller', 0.20, 0.35, 'Second-hand'),
  ('Shakers, jiggers, speed rail, mats', 0.12, 0.20, ''),
  ('Cocktail recipes and bartender training', 0.10, 0.30, 'One-off; cap the fee'),
 ]),
 ('Crockery, cutlery, glassware', [
  ('Plates and bowls, 2 sets per seat', 0.35, 0.60, ''),
  ('Bamboo steamers, soup spoons, dip bowls, chopsticks', 0.15, 0.25, ''),
  ('Cutlery', 0.12, 0.20, ''),
  ('Glassware (brewery pint glasses are often free)', 0.30, 0.50, ''),
 ]),
 ('Opening and the rest', [
  ('Opening stock and the trial service', 0.50, 0.80, ''),
  ('Tables, chairs, benches, lighting, signage (my assumption: not priced before)', 0.90, 1.60, 'Second-hand tables and local carpenter at the low end'),
  ('Licence fees and agent (FSSAI, trade, fire NOC fees; excise fee not included)', 0.15, 0.30, 'Confirm with the licence agent'),
 ]),
]
P2 = [
 ('Dishwasher, under-counter (second-hand at the low end)', 0.60, 1.20),
 ('Dual-temperature reach-in upgrade and the pass under-counter fridge', 0.70, 1.20),
 ('Ice machine, 50–70 kg a day', 1.00, 1.80),
 ('200 kg goods hoist and deck racking', 0.40, 0.70),
 ('Water: 1,000 L sump, pump, filter and softener cabinet', 0.80, 1.40),
 ('Kitchen make-up-air cooling coil and its condenser', 0.50, 0.90),
 ('Second dining AC split (front right)', 0.45, 0.60),
 ('Fifth (spare) LPG cylinder and deposit', 0.10, 0.15),
 ('Mixer-grinder, kitchen torch, hand-wash heaters', 0.15, 0.25),
 ('Onyx bar front and the finishing upgrades', 0.60, 1.20),
 ('Third crockery set per seat', 0.40, 0.70),
]

def tot(rows, i): return sum(r[i] for r in rows)
def p1_totals():
    lo = sum(r[1] for _, rows in P1 for r in rows); hi = sum(r[2] for _, rows in P1 for r in rows); return lo, hi
def numbers():
    lo, hi = p1_totals(); res = FIXED * RESERVE_MONTHS
    return dict(p1_lo=lo, p1_hi=hi, reserve=res, all_lo=lo + res, all_hi=hi + res,
                p2_lo=tot(P2, 1), p2_hi=tot(P2, 2), months_left_at_floor=(BUDGET_HIGH - lo) / FIXED, setup_room=BUDGET_HIGH - res)

def L(x): return f'₹{x:.2f} L'

def page():
    n = numbers()
    def phase_rows(groups):
        o = []
        for g, rows in groups:
            o.append(f'<tr class="grp"><th colspan="4">{html.escape(g)} <span>{L(sum(r[1] for r in rows))} – {L(sum(r[2] for r in rows))}</span></th></tr>')
            for t, a, b, note in rows:
                o.append(f'<tr><td>{html.escape(t)}</td><td class="n">{a:.2f}</td><td class="n">{b:.2f}</td><td class="note">{html.escape(note)}</td></tr>')
        return ''.join(o)
    p2 = ''.join(f'<tr><td>{html.escape(t)}</td><td class="n">{a:.2f}</td><td class="n">{b:.2f}</td></tr>' for t, a, b in P2)
    over = n['all_lo'] - BUDGET_HIGH
    verdict = (f'At floor prices on every line the total is <b>{L(n["all_lo"])}</b>, which is <b>{L(over)} over</b> the ₹13 L ceiling.'
               if over > 0 else f'At floor prices on every line the total is {L(n["all_lo"])}, inside the ceiling.')
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"><title>Setup Budget · Betalbatim Pub</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,600;12..96,700&family=IBM+Plex+Sans:wght@400;500;600;700&family=IBM+Plex+Mono:wght@500&display=swap">
<style>
/* Layout: one reading column on drafting paper; tables scroll sideways on a phone */
:root{{--paper:#fbf7ef;--ink:#2a2420;--muted:#6a5d4e;--rule:#d9cbb3;--accent:#b23a1e;--chip:#fffdf8;--ok:#2f6f3a;
  --display:'Bricolage Grotesque','Avenir Next','Segoe UI',sans-serif;--body:'IBM Plex Sans','Helvetica Neue',Arial,sans-serif;--mono:'IBM Plex Mono',ui-monospace,Menlo,monospace;color-scheme:light}}
body{{background:var(--paper);color:var(--ink);font-family:var(--body);margin:0;line-height:1.55}}
.wrap{{max-width:980px;margin:0 auto;padding:22px 16px 56px;display:flex;flex-direction:column;gap:22px}}
.eyebrow{{font:500 11px/1.4 var(--mono);letter-spacing:.08em;text-transform:uppercase;color:var(--accent);margin:0}}
h1{{font:700 clamp(26px,4vw,38px)/1.05 var(--display);margin:4px 0 6px;text-wrap:balance}}
h2{{font:700 22px/1.2 var(--display);margin:0 0 8px}}
.lede{{margin:0;max-width:72ch;color:var(--muted)}}
.stats{{display:grid;grid-template-columns:repeat(auto-fit,minmax(190px,1fr));gap:10px}}
.stat{{background:var(--chip);border:1px solid var(--rule);border-radius:8px;padding:12px 14px}}
.stat b{{display:block;font:500 20px var(--mono)}} .stat span{{font-size:13px;color:var(--muted)}}
.stat.bad b{{color:var(--accent)}} .stat.good b{{color:var(--ok)}}
.verdict{{background:#f8e7da;border-left:3px solid var(--accent);border-radius:4px;padding:12px 16px}}
.verdict p{{margin:0 0 6px}} .verdict p:last-child{{margin:0}}
.tw{{overflow-x:auto;border:1px solid var(--rule);border-radius:8px;background:var(--chip)}}
table{{border-collapse:collapse;width:100%;min-width:640px;font-size:14px}}
th,td{{text-align:left;padding:7px 12px;border-top:1px solid var(--rule);vertical-align:top}}
thead th{{background:var(--ink);color:var(--paper);font:600 12px var(--mono);border-top:0;white-space:nowrap}}
tr.grp th{{background:#efe6d3;font:700 14px var(--body)}} tr.grp th span{{float:right;font:500 12px var(--mono);color:var(--muted)}}
td.n{{text-align:right;font-family:var(--mono);white-space:nowrap}} td.note{{color:var(--muted);font-size:13px}}
tfoot td{{font-weight:700;background:#efe6d3}}
ul{{margin:0;padding-left:20px}} li{{margin:4px 0}}
.nav{{display:flex;flex-wrap:wrap;gap:8px}} .nav a{{font:600 13px var(--body);color:var(--ink);background:var(--chip);border:1px solid var(--rule);border-radius:8px;padding:9px 12px;text-decoration:none}}
</style></head><body><div class="wrap">
<header><p class="eyebrow">Simplex · Betalbatim pub · budget</p><h1>Setup budget: phase 1 before opening, phase 2 after</h1>
<p class="lede">The whole project, including a {RESERVE_MONTHS}-month backup, has to stay within ₹{BUDGET_LOW:.0f}–{BUDGET_HIGH:.0f} lakh. Phase 1 builds what the kitchen and bar cannot open without, and leaves room, wiring and drains ready for phase 2. In the 3D model the “Phase 2 items” button shows what is added later. These are planning ranges in rupees lakh, not quotes: <b>floor</b> = second-hand or hard bargaining on every line, <b>likely</b> = ordinary new quotes.</p></header>
<div class="stats">
<div class="stat"><span>Phase 1, floor – likely</span><b>{n['p1_lo']:.1f} – {n['p1_hi']:.1f} L</b></div>
<div class="stat"><span>Backup, {RESERVE_MONTHS} months × ₹{FIXED:.2f} L</span><b>{n['reserve']:.1f} L</b></div>
<div class="stat {'bad' if over>0 else 'good'}"><span>Total at floor prices</span><b>{n['all_lo']:.1f} L</b></div>
<div class="stat"><span>Ceiling</span><b>₹{BUDGET_HIGH:.0f} L</b></div>
</div>
<div class="verdict"><p>{verdict} At likely prices it is {L(n['all_hi'])}.</p>
<p>So the plan only fits if nearly every line lands at its floor, and even then there is no contingency. Ways to close the gap, in order of how little they hurt: a licence agent and the brewery's loan terms confirmed in writing before anything is bought; second-hand tables and a local carpenter for the counter; and a backup of 2½ months instead of 3 (₹{FIXED*0.5:.2f} L), which is a risk to weigh against the slow first months. Real quotes will replace these figures.</p></div>
<section><h2>Phase 1: before opening</h2><div class="tw"><table><thead><tr><th>Item</th><th>Floor ₹ L</th><th>Likely ₹ L</th><th>Note</th></tr></thead><tbody>{phase_rows(P1)}</tbody>
<tfoot><tr><td>Phase 1 total</td><td class="n">{n['p1_lo']:.2f}</td><td class="n">{n['p1_hi']:.2f}</td><td></td></tr></tfoot></table></div></section>
<section><h2>Phase 2: after opening, from the takings</h2><div class="tw"><table><thead><tr><th>Item</th><th>Floor ₹ L</th><th>Likely ₹ L</th></tr></thead><tbody>{p2}</tbody>
<tfoot><tr><td>Phase 2 total</td><td class="n">{n['p2_lo']:.2f}</td><td class="n">{n['p2_hi']:.2f}</td></tr></tfoot></table></div>
<p class="lede" style="margin-top:8px">Buy these one at a time as takings allow. The layout already reserves their space, power and drains. The dishwasher and the ice machine come first, then the reach-in upgrade and the second AC split.</p></section>
<section><h2>What is not in these numbers</h2><ul>
<li>The rent deposit and any advance rent, and the Goa excise licence fee, which is still unconfirmed.</li>
<li>Any change to the shop shell or a structural fix the society or architect asks for.</li>
<li>The hood and gas work depend on the fabricator's burner ratings; a vaporiser or a bigger fan would add to it.</li>
<li>Furniture, lighting and signage are my assumption (₹0.9–1.6 L), because the earlier checklist did not price them.</li></ul></section>
<nav class="nav"><a href="kitchen.html">Kitchen sheets</a><a href="plan.html">Floor plan</a><a href="./">3D model</a><a href="licences.html">Licences</a></nav>
</div></body></html>
'''

if __name__ == '__main__':
    n = numbers()
    for k, v in n.items(): print(f'{k:22s} {v:.2f}')
    open('budget.html', 'w').write(page()); print('budget.html written')
