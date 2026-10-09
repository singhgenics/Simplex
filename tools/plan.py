import sys,re
X0,X1,D,T,KZ=-2.45,2.45,8.8,0.2,6.3
XS=X0-T
S=120; z0,z1=-3.0,D+2.5
ox=50+0.9*S; oy=150
W=int(ox+(X1-(-5.2))*S)+380; Hh=int((z1-z0)*S)+300
out=[]
def P(x,z): return (ox+(X1-x)*S, oy+(z1-z)*S)
def rect(xa,xb,za,zb,fill='none',stroke='#3a3128',sw=1.4,dash=None):
    (a,b),(c,d)=P(max(xa,xb),max(za,zb)),P(min(xa,xb),min(za,zb))
    out.append(f'<rect x="{a:.1f}" y="{b:.1f}" width="{c-a:.1f}" height="{d-b:.1f}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"'+(f' stroke-dasharray="{dash}"' if dash else '')+'/>')
def circ(x,z,r,fill='none',stroke='#3a3128',sw=1.4):
    a,b=P(x,z);out.append(f'<circle cx="{a:.1f}" cy="{b:.1f}" r="{r*S:.1f}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')
def line(xa,za,xb,zb,stroke='#3a3128',sw=1.4,dash=None):
    a,b=P(xa,za);c,d=P(xb,zb);out.append(f'<line x1="{a:.1f}" y1="{b:.1f}" x2="{c:.1f}" y2="{d:.1f}" stroke="{stroke}" stroke-width="{sw}"'+(f' stroke-dasharray="{dash}"' if dash else '')+'/>')
def text(x,z,t,size=11,fill='#2a2420',anchor='middle',weight=500,rot=0):
    a,b=P(x,z);tr=f' transform="rotate({rot} {a:.1f} {b:.1f})"' if rot else ''
    out.append(f'<text x="{a:.1f}" y="{b+size*0.35:.1f}" font-size="{size}" fill="{fill}" text-anchor="{anchor}" font-weight="{weight}"{tr}>{t}</text>')
def hdim(xa,xb,z,t):
    a,b=P(xa,z);c,_=P(xb,z)
    out.append(f'<g stroke="#c4442a" stroke-width="1.2"><line x1="{a}" y1="{b}" x2="{c}" y2="{b}"/><line x1="{a}" y1="{b-6}" x2="{a}" y2="{b+6}"/><line x1="{c}" y1="{b-6}" x2="{c}" y2="{b+6}"/></g>')
    out.append(f'<text x="{(a+c)/2}" y="{b-5}" font-size="12" fill="#b23a1e" text-anchor="middle" font-weight="600">{t}</text>')
def vdim(x,za,zb,t,off=0):
    a,b=P(x,za);_,d=P(x,zb);a+=off
    out.append(f'<g stroke="#c4442a" stroke-width="1.2"><line x1="{a}" y1="{b}" x2="{a}" y2="{d}"/><line x1="{a-6}" y1="{b}" x2="{a+6}" y2="{b}"/><line x1="{a-6}" y1="{d}" x2="{a+6}" y2="{d}"/></g>')
    out.append(f'<text x="{a-6}" y="{(b+d)/2}" font-size="12" fill="#b23a1e" text-anchor="middle" font-weight="600" transform="rotate(-90 {a-6} {(b+d)/2})">{t}</text>')
WALL='#4a4038'
# ---- surroundings: parking behind, side passage on the right
rect(-4.5,X1+T+0.5,D+T,D+2.3,'#e3ddd4','none');
for x in (-3.6,-1.0,1.6): line(x,D+0.9,x,D+2.3,'#ffffff',3)
text(-0.6,D+1.9,'PARKING BEHIND · nothing stored here · rear door is the kitchen fire exit',12,'#6a5d4e',weight=600)
rect(XS-2.2,XS-0.8,-0.1,D+T,'#e3ddd4','none'); line(XS-0.8,-0.1,XS-0.8,D+T,'#ffffff',2,'8 6'); text(XS-1.5,2.2,'CAR PATHWAY',11,'#6a5d4e',weight=700,rot=90)
rect(XS-0.8,XS,-0.1,D+T,'#ece6db','none'); text(XS-0.4,6.6,'usable strip 0.8 m',9,'#6a5d4e',rot=90)
for z in (0.35,1.25,2.15,3.0,3.9,4.85): circ(XS-0.82,z,0.065,'#e0b030','#2a2420',1)
# ---- beer garden 5.3 × 2.0
GW=X1+T
rect(-GW,GW,-2.0,-0.06,'#efe6d2','#b9a989',1)
for x in (-(GW-0.1),GW-0.1): rect(x-0.08,x+0.08,-2.0,-1.84,'#8f5634','#8f5634',1)
rect(-GW,GW,-0.26,-0.1,'none','#8f5634',1,'4 3'); rect(-GW,GW,-2.0,-1.84,'none','#8f5634',1,'4 3')
for tx in (-1.5,1.5):
    rect(tx-0.38,tx+0.38,-1.68,-0.48,'#e8d3b0'); text(tx,-1.08,'1.2×0.76',10,rot=90)
    for s2 in (-1,1):
        rect(tx+s2*0.62-0.18,tx+s2*0.62+0.18,-1.68,-0.48,'#f3e8d6'); rect(tx+s2*0.79-0.02,tx+s2*0.79+0.02,-1.68,-0.48,'#8f5634','#8f5634',1)
rect(-GW,-0.6,-2.2,-2.02,'#c97a5a','#8f4a32',1); rect(0.6,GW,-2.2,-2.02,'#c97a5a','#8f4a32',1)
hdim(-0.69,0.69,-1.95,'path 1.38'); vdim(GW+0.3,-2.0,-0.06,'2.00',0)
text(0,-2.45,'BEER GARDEN · 5.3 × 2.0 m · 8 covers · pergola on 2 posts + facade ledger · PVC curtains on 3 sides',12,'#6a5d4e')
hdim(-GW,GW,-2.75,'5.30 (in line with the side walls)')
# ---- shell
rect(XS,X0,0,D+T,WALL,WALL,1); rect(X1,X1+T,0,D+T,WALL,WALL,1); rect(X0,0.95,D,D+T,WALL,WALL,1); rect(1.75,X1,D,D+T,WALL,WALL,1)
line(1.75,D+T,1.75-0.62,D+T+0.5,'#2a2420',1,'3 3'); text(1.35,D+0.45,'rear exit',10,'#6a5d4e')
rect(X0,X1,-0.06,0,'#9fb4c2','#4a6070',1); text(0,-0.37,'glazed shopfront · doors open outward',10,'#4a6070')
for z,n in ((4.8,'P1'),(6.8,'P2')): rect(X0,X0+0.23,z-0.15,z+0.15,WALL,WALL,1)
for xa,xb,za,zb in ((1.335,1.565,0,D),(X0,X1,4.675,4.925),(X0,1.335,6.675,6.925),(0.325,0.475,4.925,6.675)): rect(xa,xb,za,zb,'none','#8a7a62',1,'6 4')
# ---- right window tables
rect(X0,-1.95,0.15,2.25,'#d8c2a2'); text(-2.2,1.2,'banquette 2.1×0.5',9.5,rot=90)
rect(-1.95,-1.25,0.15,1.35,'#c69c6d'); text(-1.6,0.75,'1.2×0.7',10,rot=90)
rect(-1.95,-1.25,1.65,2.25,'#c69c6d'); text(-1.6,1.95,'0.6×0.7',10,rot=90)
for z in (0.45,1.05,1.95): rect(-1.14,-0.7,z-0.22,z+0.22,'#efe2c8')
text(-1.45,2.33,'WINDOW TABLES · 4 + 2',10,weight=700)
# ---- left booth + bench
rect(1.95,X1,0.15,2.25,'#d8c2a2'); text(2.2,1.2,'banquette 2.1×0.5',9.5,rot=90)
rect(0.9,1.35,0.15,2.25,'#d8c2a2'); rect(0.9,0.98,0.15,2.25,'#8f6a4a','#8f6a4a',1)
rect(1.28,2.02,0.15,1.35,'#c69c6d'); text(1.65,0.75,'1.2×0.74',10,rot=90)
rect(1.28,2.02,1.65,2.25,'#c69c6d'); text(1.65,1.95,'0.6×0.74',10,rot=90)
text(1.25,2.33,'BOOTH · 4 + 2',10,weight=700)
hdim(-0.7,0.9,1.5,'entry 1.60 clear')
rect(2.0,X1,2.4,3.55,'#d8c2a2'); rect(1.5,2.05,2.45,3.5,'#c69c6d'); text(1.78,2.97,'1.05×0.55',9.5,rot=90)
for z in (2.7,3.25): circ(2.22,z,0.12,'#efe2c8','#8f6a4a',1)
text(1.3,2.97,'BENCH · 2',11,weight=700,rot=90)
# ---- niche + washroom
rect(1.25,X1,3.6,3.68,'#d8c6ac','#d8c6ac',1); rect(1.35,X1,3.68,4.43,'#e9efe4','#8a9a7a',1); circ(2.15,4.055,0.25,'#ffffff'); text(1.7,4.055,'HAND-WASH',9,weight=700)
rect(1.25,X1,4.43,4.53,'#d8c6ac','#d8c6ac',1); rect(1.25,1.35,4.53,4.85,'#d8c6ac','#d8c6ac',1); rect(1.25,1.35,5.55,KZ,'#d8c6ac','#d8c6ac',1)
rect(1.35,X1,4.53,KZ,'#e9efe4','#8a9a7a',1); text(1.85,5.25,'WC 1.1×1.77',10,weight=700)
rect(X1-0.24,X1,4.7,5.0,'#ffffff'); rect(1.9,X1,5.2,5.23,'#8f5634','#8f5634',1); rect(1.89,2.21,5.7,6.27,'#ffffff')
line(1.3,4.85,1.3-0.62,5.35,'#2a2420',1,'3 3')
rect(1.1,1.25,5.75,6.17,'#6d7276'); text(0.75,5.96,'DB + fire panel',9,'#4a4038')
for x in (1.45,1.65): circ(x,3.52,0.07,'#c8231b','#c8231b',1)
# ---- bar
BBF,BDX=X0+0.4,X0+0.55
rect(X0,BBF,2.3,4.95,'#cfd7b2'); rect(BBF,BDX,3.35,4.62,'#cfd7b2','#4a4038',1)
rect(X0,BDX,4.15,4.6,'#9aa0a5','#4a4038',1.2); text(-2.12,4.38,'GW',8.5,'#fff',weight=700)
rect(X0,BDX,3.4,4.1,'#dff0f6','#2a6f8f',1.2); text(-2.12,3.75,'mixers',8.5,'#2a6f8f',weight=700,rot=90)
rect(X0,BBF,2.36,2.84,'#e6d6bc'); text(-2.25,2.6,'POS',8.5,weight=700)
rect(X0,BBF,2.95,3.3,'#e6d6bc','#8f6a4a',1); text(-2.25,3.12,'CO₂',8.5,weight=700)
rect(-1.1,-0.35,2.6,4.8,'#efe7da'); text(-0.6,4.3,'bar 2.2×0.75',10,rot=90)
rect(-1.22,-0.59,2.62,3.72,'#dff0f6','#2a6f8f',1.2)
for x in (-1.05,-0.77):
    for z in (2.76,3.03,3.3,3.57): circ(x,z,0.11,'none','#2a6f8f',1)
rect(-1.2,-1.0,3.74,4.8,'#c3c8cc'); rect(-1.22,-0.67,4.22,4.72,'none','#2a6f8f',1,'4 3'); text(-0.95,4.47,'ice',9,'#2a6f8f',weight=700)
for z in (2.85,3.45,4.05,4.65): circ(-0.13,z,0.21,'#efe2c8')
text(-1.5,3.17,'KEG COOLER · 8 kegs',9,'#2a6f8f',weight=700,rot=90)
hdim(BBF,-1.2,2.5,'0.85'); text(0.3,3.3,'4 stools · 0.6 apart',10,'#6a5d4e',rot=90)
hdim(0.1,1.25,4.25,'aisle 1.15')
# ---- table for 2 by the pass + server station
rect(X0,-1.95,5.0,6.25,'#d8c2a2'); rect(-1.98,-1.46,5.05,6.2,'#c69c6d'); text(-1.72,5.62,'1.15×0.52',9.5,rot=90)
for z in (5.35,5.9): circ(-2.2,z,0.12,'#efe2c8','#8f6a4a',1)
text(-1.2,5.3,'TABLE · 2',10,weight=700,rot=90)
rect(-1.55,-0.65,5.8,6.3,'#cfd7b2'); text(-1.1,6.05,'server station',9,weight=700)
# ---- kitchen
rect(X0,X1,KZ,KZ+0.1,'#d8c6ac','#d8c6ac',1); rect(-0.6,0.05,KZ,KZ+0.1,'#cfe3ea','#7a9aaa',1); rect(0.1,0.8,KZ,KZ+0.1,'#fbf7ef','#fbf7ef',1)
text(-0.28,KZ-0.15,'pass',9,'#4a6070'); text(0.45,KZ-0.15,'door',9,'#6a5d4e')
rect(-2.2,-1.4,KZ+0.1,7.05,'#c3c8cc'); text(-1.8,6.72,'non-veg prep',9)
rect(-1.4,-0.6,KZ+0.1,7.05,'#c3c8cc'); text(-1.08,6.62,'veg / dumpling',8.5); text(-1.08,6.85,'+ u/c freezer',8,'#4a4038'); circ(-0.75,6.75,0.12,'#e9e9e9','#6d7276',1)
rect(-0.6,0.05,KZ+0.1,7.05,'#c3c8cc'); text(-0.28,6.72,'pass',9)
rect(0.85,1.18,KZ+0.1,6.8,'#c3c8cc'); text(1.015,6.6,'HW',8.5,weight=700)
# fridge door swings (two 0.47 m doors) and the kitchen door swing, dashed
for hz,sg in ((6.45,1),(7.4,-1)):
    a,b=P(1.7,hz);r=0.47*S;ex,ey=P(1.23,hz)
    out.append(f'<path d="M{ex:.1f} {ey:.1f} A{r:.1f} {r:.1f} 0 0 {0 if sg>0 else 1} {a:.1f} {b-sg*r:.1f}" fill="none" stroke="#2a6f8f" stroke-width="1" stroke-dasharray="3 3"/>')
    line(1.7,hz,1.23,hz,'#2a6f8f',1,'3 3')
line(0.8,KZ+0.1,0.8,KZ+0.8,'#6a5d4e',1,'3 3')
rect(X0,X0+0.3,7.15,8.05,'none','#6d7276',1,'4 3'); text(-1.75,7.6,'wok cook',9,'#6a5d4e',weight=700); text(-1.75,7.42,'clear space',8.5,'#6a5d4e'); text(-2.3,7.6,'sauce shelf',8,'#6a5d4e',rot=90)
for xa,xb,t in ((X0,-1.25,'wok ×2'),(-1.2,-0.6,'steamer'),(-0.55,0.05,'fryer ×2'),(0.1,0.7,'stock ×2')):
    rect(xa,xb,8.1,D,'#9aa0a5'); text((xa+xb)/2,8.45,t,9.5,'#fff',weight=700)
rect(X0+0.02,0.8,7.85,D-0.02,'none','#c4442a',1.3,'8 4'); text(-0.8,7.75,'canopy hood 3.25×0.95 (bottom 2.05 m)',9.5,'#b23a1e')
rect(1.7,X1,6.45,7.4,'#c3c8cc'); text(2.07,6.92,'2-door reach-in 1.0',8.5,rot=90)
rect(1.8,X1,7.4,8.0,'#c3c8cc'); text(2.12,7.7,'dishwasher',8.5,rot=90)
rect(1.8,X1,8.0,D,'#c3c8cc'); text(2.12,8.4,'2-bowl sink',8.5,rot=90)
rect(0.35,0.95,7.15,7.95,'none','#2a6f8f',1.3,'5 3'); text(0.65,7.55,'hatch',9,'#2a6f8f',weight=700)
text(0.0,7.35,'KITCHEN 4.9 × 2.4 · ceiling 2.7',11,weight=700); text(-0.45,7.17,'deck above (+2.7 m)',9,'#2a6f8f')
# ---- right side: services
rect(XS-0.6,XS,2.15,2.75,'#e9e9e9'); text(XS-0.3,2.45,'empties',8.5)
rect(XS-0.7,XS,2.95,3.85,'#d9c7a8','#8f5634'); text(XS-0.35,3.4,'bins',9)
rect(XS-0.75,XS-0.05,3.95,4.75,'#f3d6cf','#b23a1e',1.2); text(XS-0.4,4.35,'LPG 4×19 kg',8.5,'#b23a1e',weight=700,rot=90)
line(XS-0.06,4.7,XS-0.06,8.45,'#b8862a',2); line(XS-0.06,8.45,X0,8.45,'#b8862a',2); text(XS-0.25,6.0,'gas line',8.5,'#8a6420',rot=90)
rect(XS-0.62,XS,0.35,1.25,'#d6dde2','#3a4a56',1.3); text(XS-0.31,0.8,'power backup',8.5,'#2a3a46',weight=700,rot=90)
rect(XS-0.15,XS,1.4,1.75,'#6d7276','#2a3a46',1)
rect(X0,X0+0.06,0.45,1.11,'#c9993f','#8a6420',1.2); text(X0+0.12,0.32,'meter behind hinged portrait',8,'#8a6420','end')
for z in (1.0,2.0): rect(XS-0.3,XS,z-0.4,z+0.4,'none','#6a5d4e',1,'3 2')
text(XS-0.55,2.0,'AC above',8,'#6a5d4e',rot=90)
# exhaust (at 2.35–2.75 m, drawn dashed)
for xa,xb,za,zb in ((-1.6,-1.1,D,D+T),(XS-0.45,-1.1,D+T,D+T+0.4),(XS-0.45,XS-0.05,D-0.35,D+T+0.4)): rect(xa,xb,za,zb,'#f3e0dc','#c4442a',1.3,'6 3')
rect(XS-0.6,XS+0.02,D-1.35,D-0.35,'#e8c9c2','#b23a1e',1.4); text(XS-0.3,D-0.85,'ESP',9,'#b23a1e',weight=700)
circ(XS-0.25,D-1.55,0.18,'#f3e0dc','#c4442a',1.3); text(XS-0.25,D-1.55,'fan',8,'#b23a1e')
rect(XS-0.75,XS-0.05,D-1.95,D-1.75,'#f3e0dc','#c4442a',1.3,'6 3')
a,b=P(XS-0.75,D-1.85);out.append(f'<path d="M{a} {b} l-26 0 m0 0 l9 -7 m-9 7 l9 7" stroke="#b23a1e" stroke-width="2" fill="none"/>')
text(XS-0.9,D-2.3,'smoke out at 2.6 m',9,'#b23a1e','end',700)
text(-0.6,D+0.75,'kitchen exhaust: out the back, right along the wall, round the corner',9.5,'#b23a1e')
# ---- dimensions
hdim(X1,X0,D+0.2,'4.90 (inside)')
vdim(X1+T,0,D,'8.80 (inside)',-46)
vdim(XS-2.35,0,2.25,'2.25',0); vdim(XS-2.35,2.3,4.95,'bar 2.65',0); vdim(XS-2.35,KZ+0.1,D,'kitchen 2.40',0)
vdim(X1+T,0.15,2.25,'2.10',-18); vdim(X1+T,2.4,3.55,'1.15',-18); vdim(X1+T,3.68,4.43,'0.75',-18); vdim(X1+T,4.53,KZ,'WC 1.77',-18)
title='Ground floor plan · 4.9 × 8.8 m'
sub='Betalbatim pub · Concept 25 · from the shop drawing (47 m² super built-up) · 20 covers inside + 8 in the garden · 28 covers in all'
rows=[('Bar stools','4'),('Window tables, right','6'),('Window booth, left','6'),('Bench facing the bar','2'),('Table by the pass','2'),('Beer garden, 5.3 × 2.0 m','8'),('Total','28')]
lx=W-330; ly=170
NOTES=['One double-height room, no loft.','Kitchen sized to the 22-dish menu;','fridge by the door, wok side kept clear.','Power backup on the right side, front end;','meter stays inside behind a portrait.','Kegs under the bar; glasswasher and','mixer cooler built into the back bar.','Gas, bins, AC and the kitchen exhaust in','a 0.8 m strip on the right, behind bollards;','car pathway beyond, parking behind.','Exhaust shown dashed (at 2.35–2.75 m).']
leg=[f'<rect x="{lx-18}" y="{ly-34}" width="310" height="{len(rows)*30+60+len(NOTES)*19}" fill="#fffdf8" stroke="#d9cbb3"/>',f'<text x="{lx}" y="{ly-8}" font-size="15" font-weight="700" fill="#2a2420">COVERS</text>']
for k,(a2,b2) in enumerate(rows):
    y=ly+22+k*30; bold=' font-weight="700"' if a2=='Total' else ''
    if a2=='Total': leg.append(f'<line x1="{lx}" y1="{y-20}" x2="{lx+274}" y2="{y-20}" stroke="#2a2420"/>')
    leg.append(f'<text x="{lx}" y="{y}" font-size="14" fill="#2a2420"{bold}>{a2}</text><text x="{lx+274}" y="{y}" font-size="14" text-anchor="end" fill="#2a2420"{bold}>{b2}</text>')
y=ly+22+len(rows)*30+8
for t in NOTES:
    leg.append(f'<text x="{lx}" y="{y}" font-size="12.5" fill="#6a5d4e">{t}</text>'); y+=19
svg=f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{Hh}" viewBox="0 0 {W} {Hh}" font-family="IBM Plex Sans, Helvetica, Arial, sans-serif">
<rect width="100%" height="100%" fill="#fbf7ef"/>
<text x="40" y="52" font-size="30" font-weight="700" fill="#2a2420">{title}</text>
<text x="40" y="84" font-size="15" fill="#6a5d4e">{sub}</text>
{''.join(out)}{''.join(leg)}
<g transform="translate(40,{Hh-60})"><rect width="{S}" height="10" fill="#2a2420"/><rect x="{S}" width="{S}" height="10" fill="none" stroke="#2a2420"/><text y="30" font-size="13" fill="#2a2420">0</text><text x="{S}" y="30" font-size="13" text-anchor="middle" fill="#2a2420">1 m</text><text x="{2*S}" y="30" font-size="13" text-anchor="middle" fill="#2a2420">2 m</text>
<text x="{2*S+60}" y="10" font-size="13" fill="#6a5d4e">All dimensions in metres. Left/right as you walk in from the road (road at the bottom). Dashed = overhead beams, hood, hatch and exhaust duct.</text></g>
</svg>'''
d=sys.argv[1]
import os; os.makedirs(d,exist_ok=True)
open(d+'/plan_noloft.svg','w').write(svg)
open(d+'/plan_noloft_render.html','w').write('<!doctype html><html><head><meta charset="utf-8"><style>html,body{margin:0;background:#fbf7ef}</style></head><body>'+svg+'</body></html>')
print(W,Hh)
