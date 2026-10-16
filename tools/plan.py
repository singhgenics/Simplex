import sys,re
X0,X1,D,T,KZ=-2.45,2.45,8.8,0.2,6.3
XS=X0-T
S=120; z0,z1=-3.0,D+2.5
ox=50+0.9*S; oy=150
W=int(ox+(X1-(-6.6))*S)+380; Hh=int((z1-z0)*S)+300
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
rect(XS-3.3,XS-0.5,-0.1,D+T,'#e3ddd4','none'); line(XS-0.5,-0.1,XS-0.5,D+T,'#ffffff',2,'8 6'); text(XS-2.0,6.45,'CAR PATHWAY',11,'#6a5d4e',weight=700)
rect(XS-0.5,XS,-0.1,D+T,'#ece6db','none')
for z in (0.3,1.2,2.1,3.0,3.85,4.7): circ(XS-0.52,z,0.065,'#e0b030','#2a2420',1)
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
rect(X0,X1,-0.06,0,'#9fb4c2','#4a6070',1); rect(-X1-T,X1+T,-0.2,-0.12,'#6d7276','#4a4038',0.8); text(0,-0.37,'glazed shopfront · doors open outward · slot drain + 15 mm bevelled sill · garden falls 1 in 60 to the road',9,'#4a6070')
for z,n in ((4.8,'P1'),(6.8,'P2')): rect(X0,X0+0.23,z-0.15,z+0.15,WALL,WALL,1)
for xa,xb,za,zb in ((1.335,1.565,0,D),(X0,X1,4.675,4.925),(X0,1.335,6.675,6.925),(0.325,0.475,4.925,6.675)): rect(xa,xb,za,zb,'none','#8a7a62',1,'6 4')
# ---- RIGHT: window tables, two tables for 4, 0.45 m apart, cane chairs on both sides
rect(-2.02,-1.28,0.15,1.35,'#c69c6d'); text(-1.65,0.75,'1.2×0.74',10,rot=90)
rect(-2.02,-1.28,1.8,3.0,'#c69c6d'); text(-1.65,2.4,'1.2×0.74',10,rot=90)
for z in (0.45,1.05,2.1,2.7):
    for x in (-2.2,-1.12): rect(x-0.22,x+0.22,z-0.22,z+0.22,'#efe2c8')
text(-0.62,1.2,'WINDOW TABLES · 4 + 4',10,weight=700,rot=90); vdim(-1.9,1.35,1.8,'0.45',0); vdim(-1.9,3.0,3.6,'0.60',0)
# ---- RIGHT: hand-wash alcove (one basin) + washroom (drain straight out through the right wall)
rect(X0,-1.45,3.6,3.7,'#d8c6ac','#d8c6ac',1); rect(X0,-1.45,3.7,4.7,'#e9efe4','#8a9a7a',1); rect(-1.55,-1.45,3.7,4.7,'none','#8a9a7a',1,'4 3')
def tri(x0,z0,l,k,fill,stroke):
    a,b=P(x0,z0);c,d=P(x0+l,z0);e,f=P(x0+l*k,z0+l*k);g,h=P(x0,z0+l)
    out.append(f'<path d="M{a:.1f} {b:.1f} L{c:.1f} {d:.1f} Q{e:.1f} {f:.1f} {g:.1f} {h:.1f} Z" fill="{fill}" stroke="{stroke}" stroke-width="1.2"/>')
tri(X0+0.02,3.72,0.42,0.62,'#ffffff','#3a3128'); tri(X0+0.06,3.76,0.32,0.6,'#e6ecef','#8a9a7a'); circ(X0+0.1,3.8,0.022,'#2a2420','#2a2420',1)
text(-1.72,3.85,'HAND-WASH',8.5,weight=700); text(-1.72,4.0,'LOBBY 1.0 × 1.0',7.5,'#4a4038'); text(-1.72,4.14,'corner basin 0.42',7.5,'#4a4038')
rect(X0,-2.05,4.7,4.8,'#d8c6ac','#d8c6ac',1); rect(-1.35,-1.2,4.7,4.8,'#d8c6ac','#d8c6ac',1); rect(-1.3,-1.2,4.8,KZ,'#d8c6ac','#d8c6ac',1)
rect(X0,-1.3,4.8,KZ,'#e9efe4','#8a9a7a',1); text(-1.55,6.1,'WC room',8.5,weight=700); text(-1.55,6.23,'1.15×1.50',7.5,'#4a4038')
rect(X0,X0+0.15,5.59,5.91,'#ffffff'); rect(X0+0.15,-1.83,5.5,6.0,'#ffffff'); text(-2.05,5.75,'WC',7.5,'#4a4038')
rect(-2.08,-1.69,4.62,4.65,'#c69c6d','#3a3128',1); rect(-1.72,-1.33,4.58,4.61,'#c69c6d','#3a3128',1) # sliding panels, closed
rect(-2.44,-2.05,4.52,4.56,'none','#2a2420',0.8,'3 2') # stacked when open
line(-2.41,4.5,-1.6,4.5,'#2a2420',0.8,'3 2'); text(-1.72,4.4,'WC sliding door · 0.70 clear',7,'#4a4038')
rect(X0,X0+0.25,4.97,5.3,'#ffffff'); text(X0+0.125,5.135,'basin',6,'#4a4038',rot=90)
rect(1.0,1.42,KZ-0.15,KZ,'#6d7276'); text(1.21,5.98,'DB + fire panel',8.5,'#4a4038')
for x in (X1-0.1,X1-0.3): circ(x,2.56,0.07,'#c8231b','#c8231b',1)
# ---- LEFT: window table for 4
rect(1.25,1.95,0.15,1.35,'#c69c6d'); text(1.6,0.75,'1.2×0.7',10,rot=90)
rect(1.25,1.95,1.8,2.4,'#c69c6d'); text(1.6,2.1,'0.6×0.7',10,rot=90); vdim(1.4,1.35,1.8,'0.45',0)
for z in (0.45,1.05,2.1):
    for x in (0.92,2.2): rect(x-0.22,x+0.22,z-0.22,z+0.22,'#efe2c8')
text(0.45,1.2,'WINDOW TABLES · 4 + 2',10,weight=700,rot=90)
hdim(-0.9,0.7,2.1,'entry 1.60 clear')
# ---- LEFT: bar, mirrored from Concept 25 and moved 0.42 m back
BBF,BDX=X1-0.4,X1-0.55
rect(BBF,X1,2.72,5.37,'#cfd7b2'); rect(BDX,BBF,3.77,5.04,'#cfd7b2','#4a4038',1)
rect(BDX,X1,4.57,5.02,'#9aa0a5','#4a4038',1.2); text(2.12,4.8,'GW',8.5,'#fff',weight=700)
rect(BDX,X1,3.82,4.52,'#dff0f6','#2a6f8f',1.2); text(2.12,4.17,'mixers',8.5,'#2a6f8f',weight=700,rot=90)
rect(BBF,X1,2.78,3.26,'#e6d6bc'); text(2.25,3.02,'POS',8.5,weight=700)
rect(BBF,X1,3.37,3.72,'#e6d6bc','#8f6a4a',1); text(2.25,3.54,'CO₂',8.5,weight=700)
rect(0.35,1.2,2.94,5.22,'#efe7da'); text(0.6,4.72,'bar 2.2×0.75',10,rot=90)
rect(0.59,1.22,3.04,4.14,'#efe7da','#2a6f8f',1.2)
for x,z in ((1.05,3.21),(0.77,3.21),(1.05,3.49)): circ(x,z,0.11,'none','#2a6f8f',1)
rect(0.67,1.17,3.66,4.08,'#dff0f6','#2a6f8f',1); text(0.92,3.87,'chiller',7.5,'#2a6f8f',weight=700)
rect(1.0,1.2,4.16,5.22,'#c3c8cc'); rect(0.67,1.22,4.64,5.14,'none','#2a6f8f',1,'4 3'); text(0.95,4.89,'ice',9,'#2a6f8f',weight=700)
for z in (3.27,3.87,4.47,5.07): circ(0.13,z,0.21,'#efe2c8')
text(1.5,3.59,'3 KEGS + CHILLER · LOUVRED',9,'#2a6f8f',weight=700,rot=90)
hdim(1.22,BBF,5.3,'0.85'); text(-0.3,4.17,'4 stools · 0.6 apart',10,'#6a5d4e',rot=90)
vdim(0.95,2.32,2.94,'0.62',0)
hdim(-1.2,0.35,4.77,'1.55 to the bar edge')
# ---- LEFT: server station + landing at the kitchen door
rect(X1-0.5,X1,5.45,6.25,'#cfd7b2'); text(2.12,5.85,'server stn',8.5,weight=700,rot=90); text(2.32,5.85,'0.80 × 0.50',7.5,'#4a4038',rot=90)
vdim(0.45,5.22,KZ,'1.08',0)
# ---- kitchen
rect(X0,X1,KZ,KZ+0.1,'#d8c6ac','#d8c6ac',1); rect(-0.6,0.05,KZ,KZ+0.1,'#cfe3ea','#7a9aaa',1); rect(0.1,0.9,KZ,KZ+0.1,'#fbf7ef','#fbf7ef',1)
text(-0.28,KZ-0.15,'pass',9,'#4a6070'); text(0.5,KZ-0.15,'door',9,'#6a5d4e')
rect(-2.2,-1.4,KZ+0.1,7.05,'#c3c8cc'); text(-1.8,6.62,'non-veg prep',8.5,weight=600); text(-1.8,6.84,'0.80 × 0.65 · h 0.90',7.5,'#4a4038')
rect(-1.4,-0.6,KZ+0.1,7.05,'#c3c8cc'); text(-1.12,6.55,'veg prep',8.5,weight=600); text(-1.12,6.74,'+ u/c freezer',7.5,'#4a4038'); text(-1.12,6.92,'0.80 × 0.65',7.5,'#4a4038'); circ(-0.72,6.56,0.1,'#e9e9e9','#6d7276',1); circ(-0.72,6.9,0.1,'#e9e9e9','#6d7276',1) # two rice cookers
rect(-0.6,0.05,KZ+0.1,7.05,'#c3c8cc'); text(-0.28,6.56,'pass + lamps',8.5,weight=600); text(-0.28,6.72,'+ u/c fridge',7.5,'#4a4038'); text(-0.28,6.88,'0.65 × 0.65',7.5,'#4a4038')
rect(0.92,1.2,KZ+0.1,6.8,'#c3c8cc'); text(1.06,6.52,'HW',8,weight=700); text(1.06,6.68,'0.28×0.40',6.5,'#4a4038')
rect(X0,X0+0.25,KZ+0.1,6.65,'#c3c8cc'); text(X0+0.125,6.52,'HW',6.5,weight=700) # second hand-wash at the prep corner, apron rail above
rect(X0,X0+0.45,7.12,7.6,'#c3c8cc'); text(X0+0.225,7.2,'veg sink',6.5,weight=600) # veg + herb wash sink, wet bin under it
# fridge door swings (two 0.47 m doors) and the kitchen door swing, dashed
for hz,sg in ((6.45,1),(7.4,-1)):
    a,b=P(1.7,hz);r=0.47*S;ex,ey=P(1.23,hz)
    out.append(f'<path d="M{ex:.1f} {ey:.1f} A{r:.1f} {r:.1f} 0 0 {0 if sg>0 else 1} {a:.1f} {b-sg*r:.1f}" fill="none" stroke="#2a6f8f" stroke-width="1" stroke-dasharray="3 3"/>')
    line(1.7,hz,1.23,hz,'#2a6f8f',1,'3 3')
line(0.1,KZ+0.1,0.1,KZ+0.9,'#6a5d4e',1,'3 3')
ax,ay=P(0.1,KZ+0.9); bx_,by_=P(0.9,KZ+0.1); r=0.8*S; out.append(f'<path d="M{ax:.1f} {ay:.1f} A{r:.1f} {r:.1f} 0 0 0 {bx_:.1f} {by_:.1f}" fill="none" stroke="#6a5d4e" stroke-width="1" stroke-dasharray="3 3"/>') # double-acting door, into the kitchen
ax,ay=P(0.1,KZ-0.8); bx_,by_=P(0.9,KZ); out.append(f'<path d="M{ax:.1f} {ay:.1f} A{r:.1f} {r:.1f} 0 0 1 {bx_:.1f} {by_:.1f}" fill="none" stroke="#6a5d4e" stroke-width="1" stroke-dasharray="3 3"/>') # ... and into the dining room
rect(X0,X0+0.3,7.15,8.05,'none','#6d7276',1,'4 3');
# working kit: seasoning rail, chilled mise-en-place rail, pass dip rail, board rack, pedal bins, apron hooks
rect(X0,X0+0.22,7.62,8.06,'#e6ecef','#2a6f8f',1.1); text(X0+0.11,7.84,'seasoning',6.5,'#2a6f8f',rot=-90)
rect(-2.18,-1.42,6.42,6.68,'none','#2a6f8f',1.1,'4 2'); rect(-0.6,0.05,6.93,7.05,'#e6ecef','#2a6f8f',1); rect(-2.12,-1.84,6.5,6.92,'none','#8f6a4a',0.8,'2 2')
circ(-2.27,7.36,0.1,'#cfe0bf','#3f6a3a',1.2); circ(0.83,8.62,0.1,'#d6e2ef','#2f5f9a',1.2); circ(0.83,8.7,0.07,'#c8231b','#c8231b',1); text(0.83,8.7,'K',5.5,'#fff',weight=700)
text(-1.82,7.82,'wok cook',9,'#6a5d4e',weight=700); text(-1.82,7.66,'clear space',8.5,'#6a5d4e')
for xa,xb,za,zb in ((-2.4,-1.8,7.0,7.5),(-0.95,-0.35,7.1,7.6)): rect(xa,xb,za,zb,'none','#3f6a3a',1.1,'3 2')
text(-0.65,7.35,'make-up air',6.5,'#3f6a3a',weight=600)
for xa,xb,t,dim,z0 in ((X0,-1.25,'wok range ×2','1.20 × 0.80 · h 0.80',8.0),(-1.2,-0.6,'steamer','0.60 × 0.70',8.1),(-0.55,0.05,'fryer ×2','0.60 × 0.70',8.1),(0.1,0.7,'stock ×2','0.60 × 0.70',8.1)):
    rect(xa,xb,z0,D,'#9aa0a5'); text((xa+xb)/2,8.36,t,9,'#fff',weight=700); text((xa+xb)/2,8.58,dim,7.5,'#fff')
line(X0+0.05,8.13,X0+0.05,8.6,'#2a6f8f',3,'5 2'); text(X0+0.14,8.36,'tools',6.5,'#fff',rot=-90) # wok tool rail on the wall, at 1.4 m
rect(X0,0.9,7.85,D-0.02,'none','#c4442a',1.3,'8 4'); text(-0.25,7.95,'hood 3.35 × 0.95 × 0.55 · bottom 2.05 m',8.5,'#b23a1e'); circ(0.4,8.74,0.04,'#2f6f9f','#2f6f9f',1) # pot filler
rect(1.7,X1,6.45,7.4,'#c3c8cc'); text(2.0,6.92,'dual-temp reach-in',8.5,weight=600,rot=90); text(2.2,6.92,'0.95 × 0.75 · h 2.0',7.5,'#4a4038',rot=90)
rect(1.8,X1,7.4,8.0,'#c3c8cc'); text(2.03,7.7,'u/c dishwasher',8,weight=600,rot=90); text(2.23,7.7,'0.60 × 0.65',7.5,'#4a4038',rot=90)
rect(1.8,X1,8.0,D,'#c3c8cc'); text(2.0,8.22,'2-bowl sink',8,weight=600,rot=90); text(2.17,8.22,'0.80 × 0.65',7.5,'#4a4038',rot=90); circ(2.27,8.62,0.16,'none','#b8862a',1.4); text(2.27,8.62,'35 L',6,'#8a6420',weight=700) # water heater above
rect(1.0,1.6,7.45,8.25,'none','#2a6f8f',1.3,'5 3'); text(1.3,7.78,'hatch + hoist',8.5,'#2a6f8f',weight=700); text(1.3,7.96,'0.6 × 0.8',7.5,'#2a6f8f')
text(0.47,7.6,'KITCHEN 4.9 × 2.4',11,weight=700); text(0.47,7.42,'ceiling 2.7 · deck above',8.5,'#2a6f8f')
# ---- right side: 0.5 m service strip, every fit-out dimensioned (D = depth from the wall, L = length along the wall, H = height)
rect(XS-0.35,XS,0.35,1.15,'#d6dde2','#3a4a56',1.3); text(XS-0.17,0.75,'UPS',8,'#2a3a46',weight=700,rot=90)
rect(XS-0.45,XS,1.2,2.0,'#d6e2ef','#2f6f9f',1.3); text(XS-0.22,1.6,'water',8,'#2f6f9f',weight=700,rot=90)
rect(XS-0.45,XS,2.05,2.95,'#d9c7a8','#8f5634'); text(XS-0.22,2.5,'bins',8.5,rot=90)
rect(XS-0.4,XS-0.05,3.0,4.7,'#f3d6cf','#b23a1e',1.2); text(XS-0.22,3.85,'LPG',8.5,'#b23a1e',weight=700,rot=90)
for z in (3.17,3.51,3.85,4.19,4.53): circ(XS-0.22,z,0.15,'none','#b23a1e',1)
line(XS-0.06,4.7,XS-0.06,8.7,'#b8862a',2); line(XS-0.06,8.7,X0,8.7,'#b8862a',2); rect(XS-0.13,XS-0.01,8.46,8.6,'#e8b81a','#8a6420',1) # solenoid valve on the entry
for z in (1.0,2.0,3.0): rect(XS-0.3,XS,z-0.4,z+0.4,'none','#6a5d4e',1,'3 2')
BW,GY='#7a3f1d','#2f6f9f' # toilet (black water) and grey water lines, buried, drawn dashed
line(X0,5.95,XS-0.3,5.95,BW,2,'6 3'); line(XS-0.3,5.75,XS-0.3,-0.2,BW,2,'6 3'); line(XS-0.3,-0.6,XS-0.3,-1.2,BW,2,'6 3'); line(XS-0.3,-1.2,-2.15,-1.2,BW,2,'6 3')
for za,zb,t in ((5.75,6.15,'IC1'),(-0.6,-0.2,'IC2')): rect(XS-0.45,XS-0.05,za,zb,'#f3e6dc',BW,1.4); text(XS-0.25,za+0.1 if t=='IC1' else (za+zb)/2,t,7,BW,weight=700)
rect(XS-0.45,XS-0.05,8.15,8.6,'#e6ecef',GY,1.2); text(XS-0.25,8.37,'GT',8,GY,weight=700)
line(XS-0.12,8.15,XS-0.12,-0.75,GY,1.4,'5 3'); line(XS,3.85,XS-0.12,3.85,GY,1.4,'5 3'); line(XS,5.13,XS-0.12,5.13,GY,1,'5 3'); line(1.1,4.45,X0,4.45,GY,1,'5 3')
line(X1-0.3,8.4,X1-0.3,D-0.05,GY,1,'5 3'); line(X1-0.3,D-0.05,X0+0.1,D-0.05,GY,1,'5 3'); line(XS-0.25,8.6,XS-0.25,D+T,GY,1,'5 3')
circ(XS-0.16,6.06,0.05,'#ffffff',BW,1.2)
rect(0.05,1.35,-1.7,-0.7,'none','#2f6f9f',2,'7 4'); text(0.7,-1.12,'water sump',7.5,'#2f6f9f',weight=700); text(0.7,-1.3,'1,000 L',7.5,'#2f6f9f',weight=700); circ(0.33,-1.2,0.2,'none','#2f6f9f',1.2)
WT='#3b8fd0'; line(0.7,-0.7,0.7,-0.06,WT,1.6); line(0.7,-0.06,XS-0.2,-0.06,WT,1.6); line(XS-0.2,-0.06,XS-0.2,1.2,WT,1.6); line(XS-0.2,2.0,XS-0.2,8.55,WT,1.6); line(XS-0.2,8.55,X0,8.55,WT,1.6) # water: sump to the cabinet, then buried along the strip to the kitchen
rect(-2.15,-0.05,-1.75,-0.65,'none','#2c8a66',2,'7 4'); line(-2.15,-1.5,XS-0.9,-1.5,'#2c8a66',0.8); text(XS-0.94,-1.5,'Biodigester 2,000 L · 2.1 × 1.1 × 1.2 m · buried, top 0.3 m down · 2 lids by the path',9.5,'#2c8a66','start',600)
for z in (-0.95,-1.45): circ(-0.33,z,0.2,'none','#2c8a66',1.2)
rect(X0,X0+0.06,0.45,1.11,'#c9993f','#8a6420',1.2); text(X0+0.12,0.32,'meter behind hinged portrait',8,'#8a6420','end')
# exhaust (at 2.35–2.75 m, drawn dashed)
for xa,xb,za,zb in ((-1.6,-1.1,D,D+T),(XS-0.45,-1.1,D+T,D+T+0.4),(XS-0.45,XS-0.05,D-0.35,D+T+0.4)): rect(xa,xb,za,zb,'#f3e0dc','#c4442a',1.3,'6 3')
rect(XS-0.5,XS+0.02,D-1.35,D-0.35,'#e8c9c2','#b23a1e',1.4); text(XS-0.25,D-0.85,'ESP',8.5,'#b23a1e',weight=700,rot=90)
circ(XS-0.25,D-1.55,0.18,'#f3e0dc','#c4442a',1.3)
rect(XS-0.5,XS-0.05,D-1.95,D-1.75,'#f3e0dc','#c4442a',1.3,'6 3')
a,b=P(XS-0.5,D-1.85);out.append(f'<path d="M{a} {b} l-22 0 m0 0 l8 -6 m-8 6 l8 6" stroke="#b23a1e" stroke-width="2" fill="none"/>')
text(-0.6,D+0.75,'kitchen exhaust: out the back, right along the wall, round the corner',9.5,'#b23a1e')
# callouts with sizes, on the car pathway side
def call(z,t,col='#2a2420',zi=None):
    zi=z if zi is None else zi
    line(XS-0.5,zi,XS-0.9,z,'#8a7a62',0.8); text(XS-0.94,z,t,9.5,col,'start',600)
call(0.15,'AC outdoor units (3) · 0.30 D × 0.80 L × 0.55 H · high, at 3.0 m · third = kitchen air coil','#6a5d4e',1.0)
call(0.75,'Power backup cabinet · 0.35 D × 0.80 L × 1.60 H · wall-mounted, changeover inside','#2a3a46')
call(1.62,'Water cabinet · 0.45 × 0.80 × 1.50 H · pump, filter, softener','#2f6f9f')
call(2.62,'Bin store · 0.45 D × 0.90 L × 1.00 H · 3 × 60 L bins')
call(3.85,'LPG cage · 0.35 D × 1.70 L × 1.60 H · 5 × 19 kg in one row (4 + 1 spare)','#b23a1e')
call(5.15,'Steel bollards · Ø 0.13 × 0.90 H · 6 no., on the strip edge','#8a6420',4.7)
call(5.75,'Copper gas line along the wall at 1.3 m, solenoid valve, into the kitchen','#8a6420')
call(6.3,'Soil vent pipe Ø 0.11 up the wall (WC exhaust now ducted to the back wall, high)','#7a3f1d',5.95)
call(6.6,'Inspection chamber 1 · 0.40 × 0.40 · sealed, gas-tight · WC pipe leaves the wall','#7a3f1d',5.95)
call(-0.45,'Inspection chamber 2 · toilet pipe turns in to the biodigester','#7a3f1d',-0.4)
call(-0.95,'Grey water (hand-wash, bar, kitchen) skips the tank · both go on to a soak pit or other outlet','#2f6f9f',-0.75)
call(8.25,'Grease trap 0.45 × 0.45 · kitchen grey water','#2f6f9f',8.37)
call(6.9,'Discharge · 0.40 × 0.40 at 2.4–2.8 m · ends inside the strip','#b23a1e',D-1.85)
call(7.25,'Inline exhaust fan · Ø 0.44','#b23a1e',D-1.55)
call(7.95,'ESP + carbon filter · 0.50 D × 1.00 L × 0.90 H · at 2.05–2.95 m','#b23a1e',D-0.85)
call(8.55,'Exhaust duct · 0.40 × 0.40 · at 2.35–2.75 m','#b23a1e',D-0.1)
# chain of positions along the strip + strip width + gas-to-outlet distance
for za,zb,t in ((0.35,1.15,'0.80'),(1.2,2.0,'0.80'),(2.05,2.95,'0.90'),(3.0,4.7,'1.70'),(D-1.35,D-0.35,'1.00')): vdim(XS-0.68,za,zb,t,0)
vdim(XS-0.68,4.7,D-1.95,'2.15 gas to outlet',0)
hdim(XS-0.5,XS,6.35,'0.50')
text(2.15,D+0.55,'Fresh-air intake · 0.50 × 0.48 · high, at 3.3 m',9,'#6a5d4e',weight=600)
vdim(-1.45,7.05,8.1,'aisle 1.05',0); hdim(0.95,1.75,D-0.15,'rear door 0.80'); hdim(0.1,0.9,KZ+0.25,'door 0.80')
# ---- dimensions
hdim(X1,X0,D+0.2,'4.90 (inside)')
vdim(X1+T,0,D,'8.80 (inside)',-46)
vdim(XS-3.45,0.15,3.0,'tables 2.85',0); vdim(XS-3.45,3.55,4.7,'hand-wash 1.00',0); vdim(XS-3.45,4.8,KZ,'WC 1.50',0); vdim(XS-3.45,KZ+0.1,D,'kitchen 2.40',0)
vdim(X1+T,0.15,2.4,'2.25 tables',-18); vdim(X1+T,2.72,5.37,'back bar 2.65',-18); vdim(X1+T,5.45,6.25,'0.80',-18)
title='Ground floor plan · 4.9 × 8.8 m'
sub='Betalbatim pub · Concept 27 (mirrored: washroom right, bar left; 0.45 m min between tables) · from the shop drawing (47 m² super built-up) · 18 covers inside + 8 in the garden · 26 in all'
rows=[('Bar stools','4'),('Window tables, left (4 + 2)','6'),('Window tables, right (4 + 4)','8'),('Beer garden, 5.3 × 2.0 m','8'),('Total','26')]
lx=W-330; ly=170
NOTES=['One double-height room, no loft.','Mirrored: washroom + hand-wash on the','right wall drain straight out; bar on the left.','At least 0.45 m between any two tables.','1.6 m entry, 0.62 m window table to bar,','1.1 m at the kitchen door, 1.55 m from','the bar edge to the washroom block.','Kitchen sized to the Pan-Asian menu.','Power backup cabinet (changeover inside);','meter stays inside behind a portrait.','Gas, bins, AC, exhaust, water and drains in a','0.5 m strip on the right, behind bollards;','car pathway beyond, parking behind.','WC drains along the strip to a 2,000 L','biodigester under the garden (dashed).','Kitchen: veg sink and two hand-washes (aprons','at the prep corner), 0.8 m double-acting door,','dual-temp reach-in, 35 L water heater, pot','filler, make-up air, cement-board ceiling,','goods hoist at the hatch, seasoning rail,','mise-en-place rail, pass fridge, rice cookers,','gas solenoid + leak detector, Class K at the','end of the hot line.','Water: 1,000 L sump under the left garden →','pump, filter, softener on the strip → kitchen.','Exhaust and drains shown dashed.']
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
