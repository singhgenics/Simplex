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
rect(X0,X1,-0.06,0,'#9fb4c2','#4a6070',1); text(0,-0.37,'glazed shopfront · doors open outward',10,'#4a6070')
for z,n in ((4.8,'P1'),(6.8,'P2')): rect(X0,X0+0.23,z-0.15,z+0.15,WALL,WALL,1)
for xa,xb,za,zb in ((1.335,1.565,0,D),(X0,X1,4.675,4.925),(X0,1.335,6.675,6.925),(0.325,0.475,4.925,6.675)): rect(xa,xb,za,zb,'none','#8a7a62',1,'6 4')
# ---- RIGHT: window tables, two tables for 4, 0.45 m apart, cane chairs on both sides
rect(-2.02,-1.28,0.15,1.35,'#c69c6d'); text(-1.65,0.75,'1.2×0.74',10,rot=90)
rect(-2.02,-1.28,1.8,3.0,'#c69c6d'); text(-1.65,2.4,'1.2×0.74',10,rot=90)
for z in (0.45,1.05,2.1,2.7):
    for x in (-2.2,-1.12): rect(x-0.22,x+0.22,z-0.22,z+0.22,'#efe2c8')
text(-0.62,1.2,'WINDOW TABLES · 4 + 4',10,weight=700,rot=90); vdim(-1.9,1.35,1.8,'0.45',0); vdim(-1.9,3.0,3.45,'0.45',0)
# ---- RIGHT: hand-wash alcove (one basin) + washroom (drain straight out through the right wall)
rect(X0,-1.2,3.45,3.55,'#d8c6ac','#d8c6ac',1); rect(X0,-1.2,3.55,4.7,'#e9efe4','#8a9a7a',1); rect(-1.3,-1.2,3.55,4.7,'none','#8a9a7a',1,'4 3')
circ(X0+0.3,4.12,0.25,'#ffffff'); circ(X0+0.3,4.12,0.18,'#e6ecef','#8a9a7a',1); circ(X0+0.07,4.12,0.03,'#2a2420','#2a2420',1)
text(-1.62,3.85,'HAND-WASH',9.5,weight=700); text(-1.62,4.05,'1.25 × 1.15',8,'#4a4038'); text(-1.62,4.22,'1 basin Ø 0.50',8,'#4a4038')
rect(X0,-1.2,4.7,4.8,'#d8c6ac','#d8c6ac',1); rect(-1.3,-1.2,4.8,5.0,'#d8c6ac','#d8c6ac',1); rect(-1.3,-1.2,5.7,KZ,'#d8c6ac','#d8c6ac',1)
rect(X0,-1.3,4.8,KZ,'#e9efe4','#8a9a7a',1); text(-1.75,5.05,'WC 1.15×1.50',9.5,weight=700)
rect(-2.16,-1.84,5.64,6.27,'#ffffff'); line(-1.25,5.0,-1.8,5.43,'#2a2420',1,'3 3'); text(-1.62,5.25,'door 0.70',8,'#4a4038')
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
rect(0.59,1.22,3.04,4.14,'#dff0f6','#2a6f8f',1.2)
for x in (1.05,0.77):
    for z in (3.18,3.45,3.72,3.99): circ(x,z,0.11,'none','#2a6f8f',1)
rect(1.0,1.2,4.16,5.22,'#c3c8cc'); rect(0.67,1.22,4.64,5.14,'none','#2a6f8f',1,'4 3'); text(0.95,4.89,'ice',9,'#2a6f8f',weight=700)
for z in (3.27,3.87,4.47,5.07): circ(0.13,z,0.21,'#efe2c8')
text(1.5,3.59,'KEG COOLER · 8 kegs',9,'#2a6f8f',weight=700,rot=90)
hdim(1.22,BBF,5.3,'0.85'); text(-0.3,4.17,'4 stools · 0.6 apart',10,'#6a5d4e',rot=90)
vdim(0.95,2.32,2.94,'0.62',0)
hdim(-1.2,0.35,4.77,'1.55 to the bar edge')
# ---- LEFT: server station + landing at the kitchen door
rect(X1-0.5,X1,5.45,6.25,'#cfd7b2'); text(2.12,5.85,'server stn',8.5,weight=700,rot=90); text(2.32,5.85,'0.80 × 0.50',7.5,'#4a4038',rot=90)
vdim(0.45,5.22,KZ,'1.08',0)
# ---- kitchen
rect(X0,X1,KZ,KZ+0.1,'#d8c6ac','#d8c6ac',1); rect(-0.6,0.05,KZ,KZ+0.1,'#cfe3ea','#7a9aaa',1); rect(0.1,0.8,KZ,KZ+0.1,'#fbf7ef','#fbf7ef',1)
text(-0.28,KZ-0.15,'pass',9,'#4a6070'); text(0.45,KZ-0.15,'door',9,'#6a5d4e')
rect(-2.2,-1.4,KZ+0.1,7.05,'#c3c8cc'); text(-1.8,6.62,'non-veg prep',8.5,weight=600); text(-1.8,6.84,'0.80 × 0.65 · h 0.90',7.5,'#4a4038')
rect(-1.4,-0.6,KZ+0.1,7.05,'#c3c8cc'); text(-1.08,6.55,'veg / dumpling',8.5,weight=600); text(-1.08,6.74,'+ u/c freezer',7.5,'#4a4038'); text(-1.08,6.92,'0.80 × 0.65',7.5,'#4a4038'); circ(-0.75,6.62,0.1,'#e9e9e9','#6d7276',1)
rect(-0.6,0.05,KZ+0.1,7.05,'#c3c8cc'); text(-0.28,6.62,'pass + lamps',8.5,weight=600); text(-0.28,6.84,'0.65 × 0.65',7.5,'#4a4038')
rect(0.85,1.18,KZ+0.1,6.8,'#c3c8cc'); text(1.015,6.52,'HW',8,weight=700); text(1.015,6.68,'0.33×0.40',6.5,'#4a4038')
# fridge door swings (two 0.47 m doors) and the kitchen door swing, dashed
for hz,sg in ((6.45,1),(7.4,-1)):
    a,b=P(1.7,hz);r=0.47*S;ex,ey=P(1.23,hz)
    out.append(f'<path d="M{ex:.1f} {ey:.1f} A{r:.1f} {r:.1f} 0 0 {0 if sg>0 else 1} {a:.1f} {b-sg*r:.1f}" fill="none" stroke="#2a6f8f" stroke-width="1" stroke-dasharray="3 3"/>')
    line(1.7,hz,1.23,hz,'#2a6f8f',1,'3 3')
line(0.8,KZ+0.1,0.8,KZ+0.8,'#6a5d4e',1,'3 3')
rect(X0,X0+0.3,7.15,8.05,'none','#6d7276',1,'4 3'); text(-1.75,7.6,'wok cook',9,'#6a5d4e',weight=700); text(-1.75,7.42,'clear space',8.5,'#6a5d4e'); text(-2.3,7.6,'sauce shelf 0.9 × 0.3',7.5,'#6a5d4e',rot=90)
for xa,xb,t,dim in ((X0,-1.25,'wok range ×2','1.20 × 0.70 · h 0.80'),(-1.2,-0.6,'steamer','0.60 × 0.70'),(-0.55,0.05,'fryer ×2','0.60 × 0.70'),(0.1,0.7,'stock ×2','0.60 × 0.70')):
    rect(xa,xb,8.1,D,'#9aa0a5'); text((xa+xb)/2,8.36,t,9,'#fff',weight=700); text((xa+xb)/2,8.58,dim,7.5,'#fff')
rect(X0+0.02,0.8,7.85,D-0.02,'none','#c4442a',1.3,'8 4'); text(-0.25,7.95,'hood 3.25 × 0.95 × 0.55 · bottom 2.05 m',8.5,'#b23a1e')
rect(1.7,X1,6.45,7.4,'#c3c8cc'); text(2.0,6.92,'2-door reach-in',8.5,weight=600,rot=90); text(2.2,6.92,'1.0 × 0.75 · h 2.0',7.5,'#4a4038',rot=90)
rect(1.8,X1,7.4,8.0,'#c3c8cc'); text(2.03,7.7,'u/c dishwasher',8,weight=600,rot=90); text(2.23,7.7,'0.60 × 0.65',7.5,'#4a4038',rot=90)
rect(1.8,X1,8.0,D,'#c3c8cc'); text(2.03,8.4,'2-bowl sink',8,weight=600,rot=90); text(2.23,8.4,'0.80 × 0.65',7.5,'#4a4038',rot=90)
rect(0.35,0.95,7.15,7.95,'none','#2a6f8f',1.3,'5 3'); text(0.65,7.5,'hatch',9,'#2a6f8f',weight=700); text(0.65,7.68,'0.6 × 0.8',7.5,'#2a6f8f')
text(0.0,7.35,'KITCHEN 4.9 × 2.4 · ceiling 2.7',11,weight=700); text(-0.45,7.17,'deck above (+2.7 m)',9,'#2a6f8f')
# ---- right side: 0.5 m service strip, every fit-out dimensioned (D = depth from the wall, L = length along the wall, H = height)
rect(XS-0.35,XS,0.35,1.15,'#d6dde2','#3a4a56',1.3); text(XS-0.17,0.75,'UPS',8,'#2a3a46',weight=700,rot=90)
rect(XS-0.45,XS,1.55,2.15,'#e9e9e9'); text(XS-0.22,1.85,'kegs',8,rot=90)
rect(XS-0.45,XS,2.25,3.15,'#d9c7a8','#8f5634'); text(XS-0.22,2.7,'bins',8.5,rot=90)
rect(XS-0.4,XS-0.05,3.3,4.7,'#f3d6cf','#b23a1e',1.2); text(XS-0.22,4.0,'LPG',8.5,'#b23a1e',weight=700,rot=90)
for z in (3.47,3.81,4.15,4.49): circ(XS-0.22,z,0.15,'none','#b23a1e',1)
line(XS-0.06,4.7,XS-0.06,8.45,'#b8862a',2); line(XS-0.06,8.45,X0,8.45,'#b8862a',2)
for z in (1.0,2.0): rect(XS-0.3,XS,z-0.4,z+0.4,'none','#6a5d4e',1,'3 2')
rect(XS-0.33,XS,2.225,2.675,'none','#6a5d4e',1,'2 2')
rect(XS-0.45,XS-0.05,6.75,7.2,'#e6ecef','#4a6070',1.2); text(XS-0.25,6.97,'IC',8,'#4a6070',weight=700)
rect(XS-0.45,XS-0.05,8.15,8.6,'#e6ecef','#4a6070',1.2); text(XS-0.25,8.37,'GT',8,'#4a6070',weight=700)
line(XS-0.3,4.12,XS-0.3,6.75,'#4a6070',1.2,'5 3'); line(XS,4.12,XS-0.3,4.12,'#4a6070',1.2,'5 3'); line(XS,6.0,XS-0.3,6.0,'#4a6070',1.2,'5 3'); line(XS-0.3,7.2,XS-0.3,8.15,'#4a6070',1.2,'5 3'); line(XS-0.3,8.6,XS-0.3,D+T+0.7,'#4a6070',1.2,'5 3')
line(X1-0.3,8.4,X1-0.3,D-0.05,'#4a6070',1,'5 3'); line(X1-0.3,D-0.05,X0+0.1,D-0.05,'#4a6070',1,'5 3')
circ(XS-0.16,6.05,0.055,'#ffffff','#4a6070',1.2)
text(XS-0.25,D+T+0.85,'drain line on to the treatment tank (under the pathway or parking, with consent)',9.5,'#4a6070','start',600)
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
call(0.15,'AC outdoor units (2) · 0.30 D × 0.80 L × 0.55 H · high, at 3.0 m','#6a5d4e',1.0)
call(0.75,'Power backup cabinet · 0.35 D × 0.80 L × 1.60 H · wall-mounted, changeover inside','#2a3a46')
call(1.85,'Empty-keg cage · 0.45 D × 0.60 L × 1.20 H · 2 kegs')
call(2.3,'Keg-cooler compressor · 0.33 D × 0.45 L × 0.45 H · high, at 2.25 m','#6a5d4e',2.45)
call(2.75,'Bin store · 0.45 D × 0.90 L × 1.00 H · 3 × 60 L bins')
call(4.0,'LPG cage · 0.35 D × 1.40 L × 1.60 H · 4 × 19 kg in one row','#b23a1e')
call(5.15,'Steel bollards · Ø 0.13 × 0.90 H · 6 no., on the strip edge','#8a6420',4.7)
call(5.75,'Copper gas line along the wall at 1.3 m, into the kitchen','#8a6420')
call(6.3,'Soil vent pipe Ø 0.11 up the wall · washroom exhaust fan at 2.3 m','#4a6070',6.05)
call(6.6,'Sealed inspection chamber 0.45 × 0.45 · 2.0 m past the gas','#4a6070',6.97)
call(8.25,'Grease trap 0.45 × 0.45 · kitchen + bar grey water','#4a6070',8.37)
call(6.9,'Discharge · 0.40 × 0.40 at 2.4–2.8 m · ends inside the strip','#b23a1e',D-1.85)
call(7.25,'Inline exhaust fan · Ø 0.44','#b23a1e',D-1.55)
call(7.95,'ESP + carbon filter · 0.50 D × 1.00 L × 0.90 H · at 2.05–2.95 m','#b23a1e',D-0.85)
call(8.55,'Exhaust duct · 0.40 × 0.40 · at 2.35–2.75 m','#b23a1e',D-0.1)
# chain of positions along the strip + strip width + gas-to-outlet distance
for za,zb,t in ((0.35,1.15,'0.80'),(1.55,2.15,'0.60'),(2.25,3.15,'0.90'),(3.3,4.7,'1.40'),(D-1.35,D-0.35,'1.00')): vdim(XS-0.68,za,zb,t,0)
vdim(XS-0.68,4.7,D-1.95,'2.15 gas to outlet',0)
hdim(XS-0.5,XS,6.35,'0.50')
text(2.15,D+0.55,'Fresh-air intake · 0.50 × 0.48 · high, at 3.3 m',9,'#6a5d4e',weight=600)
vdim(-1.45,7.05,8.1,'aisle 1.05',0); hdim(0.95,1.75,D-0.15,'rear door 0.80'); hdim(0.1,0.8,KZ+0.25,'door 0.70')
# ---- dimensions
hdim(X1,X0,D+0.2,'4.90 (inside)')
vdim(X1+T,0,D,'8.80 (inside)',-46)
vdim(XS-3.45,0.15,3.0,'tables 2.85',0); vdim(XS-3.45,3.55,4.7,'hand-wash 1.15',0); vdim(XS-3.45,4.8,KZ,'WC 1.50',0); vdim(XS-3.45,KZ+0.1,D,'kitchen 2.40',0)
vdim(X1+T,0.15,2.4,'2.25 tables',-18); vdim(X1+T,2.72,5.37,'back bar 2.65',-18); vdim(X1+T,5.45,6.25,'0.80',-18)
title='Ground floor plan · 4.9 × 8.8 m'
sub='Betalbatim pub · Concept 27 (mirrored: washroom right, bar left; 0.45 m min between tables) · from the shop drawing (47 m² super built-up) · 18 covers inside + 8 in the garden · 26 in all'
rows=[('Bar stools','4'),('Window tables, left (4 + 2)','6'),('Window tables, right (4 + 4)','8'),('Beer garden, 5.3 × 2.0 m','8'),('Total','26')]
lx=W-330; ly=170
NOTES=['One double-height room, no loft.','Mirrored: washroom + hand-wash on the','right wall drain straight out; bar on the left.','At least 0.45 m between any two tables.','1.6 m entry, 0.62 m window table to bar,','1.1 m at the kitchen door, 1.55 m from','the bar edge to the washroom block.','Kitchen sized to the 22-dish menu.','Power backup cabinet (changeover inside);','meter stays inside behind a portrait.','Gas, bins, AC, exhaust and drains in a','0.5 m strip on the right, behind bollards;','car pathway beyond, parking behind.','Exhaust and drains shown dashed.']
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
