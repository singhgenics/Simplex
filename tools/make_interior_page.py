#!/usr/bin/env python3
"""Builds interior-3d.html from index.html (the pub's exact 3D model): the same scene and coordinates, plus a "Photo textures" switch that wraps real
photographs on the model (the furniture comes from the Furnishings images in the Menu repo), a scrolling page layout, and a section comparing
exact model / textured model / photoreal Flow image from the same camera. Re-run after changing index.html or the textures:
    python3 tools/make_interior_page.py
Textures: tools/make_interior_textures.py. Photoreal views: tools/gen-interior-renders.sh (prompts in tools/interior_render_jobs.py)."""
import json, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.join(HERE, '..')
src = open(os.path.join(ROOT, 'index.html')).read()
try: info = json.load(open(os.path.join(ROOT, 'renders', 'tex', 'interior.json')))
except Exception: info = {}
def sub1(a, b, s):
    assert s.count(a) == 1, (s.count(a), a[:70]); return s.replace(a, b)
s = src
# ---- head / layout: scrolling page, aside replaced, compare section added ----
s = re.sub(r'<title>.*?</title>', '<title>Interiors in 3D · photo-textured</title>', s, count=1, flags=re.S)
s = re.sub(r'<meta name="description"[^>]*>', '<meta name="description" content="The Simplex pub interior as an exact 3D model with real photographs wrapped on it, built from the Furnishings pieces, next to photoreal views from the same cameras.">', s, count=1)
s = sub1("html,body{height:100%}", "html,body{height:auto}", s)
s = sub1(".app{display:grid;grid-template-columns:minmax(0,1fr) 400px;height:100%}", ".app{display:grid;grid-template-columns:minmax(0,1fr) 400px;height:100vh;min-height:560px}", s)
css = """
.cmp{max-width:1240px;margin:0 auto;padding:30px 16px 60px}
.cmp h2{font:700 28px/1.15 var(--display);margin:0 0 6px;letter-spacing:-.01em}
.cmp .sub{color:var(--muted);max-width:75ch;margin:0 0 18px}
.pairs{display:grid;grid-template-columns:repeat(auto-fill,minmax(min(100%,380px),1fr));gap:18px}
.pair{border:1px solid var(--line);border-radius:14px;overflow:hidden;background:var(--raise)}
.pair .ph{position:relative;aspect-ratio:4/3;background:#222;cursor:pointer}
.pair .ph img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;transition:opacity .25s}
.pair .ph img.b,.pair .ph img.t{opacity:0}.pair.show-m .ph img.b{opacity:1}.pair.show-t .ph img.t{opacity:1}
.pair .tg{position:absolute;left:8px;bottom:8px;display:flex;flex-wrap:wrap;gap:4px;right:8px}
.pair .tg button{appearance:none;border:1.5px solid rgba(255,255,255,.7);background:rgba(20,15,12,.7);color:#fff;font:600 10.5px/1 var(--mono);letter-spacing:.06em;text-transform:uppercase;padding:7px 10px;border-radius:999px;cursor:pointer}
.pair .tg button[aria-pressed=true]{background:#e9b54a;color:#1b120a;border-color:#e9b54a}
.pair .bd{padding:12px 14px 14px}.pair h3{font:700 16px/1.25 var(--body);margin:0 0 4px}.pair p{margin:0;font-size:13px;color:var(--muted)}
.pair .key{font:500 11.5px/1.55 var(--mono);color:var(--amber);margin-top:8px}
.cmp .note{font-size:13px;color:var(--muted);border-left:3px solid var(--ox);padding-left:10px;max-width:75ch;margin-top:22px}
.photo-aside{padding:22px 22px 30px}.photo-aside h1{font:700 30px/1.05 var(--display);margin:0 0 10px}.photo-aside p{color:var(--muted);margin:0 0 12px}
.photo-aside ul{margin:0 0 14px;padding-left:18px;color:var(--muted)}.photo-aside li{margin:0 0 6px}.photo-aside a{color:var(--amber)}
"""
s = sub1("</style>", css + "</style>", s)
aside = """<aside class="panel photo-aside">
    <p class="eyebrow">Concept 27 · 4.9 × 8.8 m · exact model with real photographs</p>
    <h1>The interior, photo-textured</h1>
    <p>This is the same 3D model as the pub page, at the same sizes and positions, with real photographs wrapped on it. Switch <b>Photo textures</b> (top, second row) to compare with the plain model.</p>
    <ul>
      <li><b>Furniture from the Furnishings section:</b> the S1 cane chair back, the S2 velvet bar stool (brass legs), the T1 acacia table tops and the bar front (back-lit onyx under brass mesh) use crops of the generated furniture images.</li>
      <li><b>Surfaces:</b> real brick, black-and-white porcelain checker, reclaimed wood, emerald glass mosaic, white marble, lime-wash plaster, concrete, brushed stainless and 75 mm white tile.</li>
      <li>Click a zone for its sizes; use the view buttons, the lighting control and the Cutaway switch as on the pub page.</li>
    </ul>
    <p><a href="index.html">Pub model (plain)</a> · <a href="kitchen-3d.html">Kitchen in 3D</a> · <a href="https://singhgenics.github.io/Menu/#furnishings">Furnishings schedule and gallery</a> · <a href="plan.html">Floor plan</a></p>
    <p style="font-size:12px">Photo textures need the page served over http(s); opened from disk, browsers block them and the plain model shows.</p>
  </aside>"""
s = re.sub(r'<aside class="panel">.*?</aside>', lambda m: aside, s, count=1, flags=re.S)
cmp = """<section class="cmp" id="compare">
  <h2>Exact model, textured model and photoreal view</h2>
  <p class="sub">Each view has three states from the same camera. <b>Exact model</b>: the plain model. <b>Textured model</b>: the same model with real photographs wrapped on it. <b>Photoreal</b>: a Google Flow image made from the textured model plus the Furnishings product images (chair, stool, table, bench, lights), so the furniture is the designed furniture. Tap an image to cycle. Flow is close but not exact: the model and the sheets govern sizes.</p>
  <div class="pairs" id="pairs"></div>
  <p class="note">Sizes and positions come from the shop drawing and the plan (see the Floor plan page). Generated images show the intent, not a supplier's product, and differ from the model in small details.</p>
</section>
"""
s = sub1('<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>', cmp + '<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>', s)

# ---- the photo layer, right after the materials ----
n = info
photo = r"""
// ---------- PHOTO TEXTURES: real photographs wrapped on the same exact model (tools/make_interior_textures.py) ----------
M.chairBack=S({color:'#d1ab72',roughness:0.85}); M.chairSeat=S({color:'#d1ab72',roughness:0.85}); M.chairLeg=S({color:'#8f5634',roughness:0.7}); M.stoolLeg=S({color:'#1a1a1a',roughness:0.6});
const TEXN=__TEXN__;
const ldr=new THREE.TextureLoader();
function ltex(id,rx,ry){const t=ldr.load('renders/tex/'+id+'.jpg',()=>{dirty=true});t.encoding=THREE.sRGBEncoding;t.anisotropy=aniso;t.wrapS=t.wrapT=THREE.RepeatWrapping;t.repeat.set(rx,ry);return t;}
const SWP=[];
function swp(key,id,o){o=o||{};const m=M[key];if(!m)return;const old=m.map,rx=(old?old.repeat.x:1)*(o.sx||1),ry=(old?old.repeat.y:1)*(o.sy||1);
  SWP.push({m,clay:{map:old,color:m.color.getHex(),rough:m.roughness,metal:m.metalness,em:m.emissiveMap||null},photo:ltex(id,rx,ry),o});}
const nM=TEXN.mosaic||8,nC=TEXN.checker||6,nT=7;
swp('brick','int-brick',{}); swp('floor','int-checker',{sx:2/nC,sy:2/nC}); swp('reclaim','int-reclaim',{}); swp('timber','int-acacia',{});
swp('marble','int-marble',{}); swp('sage','int-mosaic',{sx:8/nM,sy:8/nM}); swp('whiteTile','tile-75',{sx:4/nT,sy:4/nT}); swp('plaster','int-limewash',{});
swp('conc','int-concrete',{}); swp('epoxy','floor-epoxy',{sx:0.5,sy:0.5});
swp('ss','ss-brushed',{color:0xffffff,metal:0.5,rough:0.45}); swp('ssDark','ss-brushed',{color:0xa9adb2,metal:0.5,rough:0.5});
swp('chairBack','int-cane',{color:0xffffff}); swp('velvetSand','int-velvet',{color:0xffffff,rough:0.95});
swp('onyxGlow','int-onyx',{emissive:true});
const NOWHITE=['brick','plaster'];
function setPhoto(on){SWP.forEach(k=>{const m=k.m,o=k.o;
    m.map=on?k.photo:k.clay.map;m.color.setHex(on&&o.color!==undefined?o.color:k.clay.color);
    if(o.metal!==undefined)m.metalness=on?o.metal:k.clay.metal;if(o.rough!==undefined)m.roughness=on?o.rough:k.clay.rough;
    if(o.emissive)m.emissiveMap=on?k.photo:k.clay.em;m.needsUpdate=true;});
  // the designed furniture: S1 cane chair (walnut legs, tan leatherette seat), S2 stool (brass legs)
  M.chairLeg.color.set(on?'#5a3a24':'#8f5634'); M.chairSeat.color.set(on?'#b98a5a':'#d1ab72'); M.stoolLeg.color.set(on?'#c9993f':'#1a1a1a'); M.stoolLeg.metalness=on?0.9:0; M.stoolLeg.roughness=on?0.3:0.6;
  dirty=true;}
"""
photo = photo.replace('__TEXN__', json.dumps(n))
s = sub1("const cush=['#7b8452'", photo + "const cush=['#7b8452'", s)
# ---- furniture: the S1 chair and S2 stool use the new materials (identical look until Photo textures is on) ----
s = sub1("bx(-0.22,0.22,0.43,0.49,-0.22,0.22,M.cane,g);bx(-0.22,0.22,0.49,0.92,0.18,0.23,M.cane,g);", "bx(-0.22,0.22,0.43,0.49,-0.22,0.22,M.chairSeat,g);bx(-0.22,0.22,0.49,0.92,0.18,0.23,M.chairBack,g);", s)
s = sub1("[[-.2,-.2],[.2,-.2],[-.2,.2],[.2,.2]].forEach(([a,b])=>cyl(0.015,0.015,0.43,a,0,b,M.timberDark,g,6));", "[[-.2,-.2],[.2,-.2],[-.2,.2],[.2,.2]].forEach(([a,b])=>cyl(0.015,0.015,0.43,a,0,b,M.chairLeg,g,6));", s)
s = sub1("rod(V(x+a*1.1,0,z+b*1.1),V(x+a*0.8,0.68,z+b*0.8),0.011,M.black,parent));", "rod(V(x+a*1.1,0,z+b*1.1),V(x+a*0.8,0.68,z+b*0.8),0.011,M.stoolLeg,parent));", s)
# ---- state, toggle, handle for screenshots and the compare section ----
s = sub1("const state={cut:true,labels:false,night:true,loft:false,focus:null};", "const state={cut:true,labels:false,night:true,loft:false,focus:null,photo:location.protocol!=='file:'};", s)
s = sub1("function goView(k,instant){", "window.__k={get goView(){return goView},state,VIEWS,camera,controls,setPhoto,setDirty:()=>{dirty=true}};\nfunction goView(k,instant){", s)
s = sub1('<button id="t-plans" aria-pressed="false">Floor plans</button>', '<button id="t-plans" aria-pressed="false">Floor plans</button>\n        <button id="t-photo" aria-pressed="true">Photo textures</button>', s)
tog = """
{const pb=document.getElementById('t-photo');
 if(location.protocol==='file:'){pb.disabled=true;pb.setAttribute('aria-pressed','false');pb.title='Photo textures need the page served over http(s)';}
 const apply=()=>{pb.setAttribute('aria-pressed',String(state.photo));setPhoto(state.photo);};
 pb.addEventListener('click',()=>{state.photo=!state.photo;apply();});apply();}
"""
s = sub1("const viewBtns=[...document.querySelectorAll('[data-view]')];", tog + "const viewBtns=[...document.querySelectorAll('[data-view]')];", s)
# ---- compare section ----
PAIRS = json.load(open(os.path.join(HERE, 'interior_views.json')))
cmpjs = """
<script>
(function(){const PAIRS=__PAIRS__;const pairs=document.getElementById('pairs');
PAIRS.forEach(([id,t,p,key])=>{const el=document.createElement('div');el.className='pair';
 el.innerHTML=`<div class="ph"><img class="a" src="renders/interior3d-${id}-photo.jpg" alt="${t}, photoreal" loading="lazy"><img class="t" src="renders/interior3d-${id}-tex.jpg" alt="${t}, photo-textured model" loading="lazy"><img class="b" src="renders/interior3d-${id}-model.jpg" alt="${t}, exact model" loading="lazy"><div class="tg"><button type="button" data-m="0" aria-pressed="true">Photoreal</button><button type="button" data-m="1" aria-pressed="false">Textured model</button><button type="button" data-m="2" aria-pressed="false">Exact model</button></div></div><div class="bd"><h3>${t}</h3><p>${p}</p><div class="key">${key}</div></div>`;
 let cur=0;const flip=m=>{cur=m;el.classList.toggle('show-t',m===1);el.classList.toggle('show-m',m===2);el.querySelectorAll('.tg button').forEach(b=>b.setAttribute('aria-pressed',String(+b.dataset.m===m)));};
 el.querySelector('.tg').addEventListener('click',e=>{e.stopPropagation();const b=e.target.closest('[data-m]');if(b)flip(+b.dataset.m);});
 el.querySelector('.ph').addEventListener('click',()=>flip((cur+1)%3));pairs.appendChild(el);});})();
</script>
"""
s = sub1("</body>", cmpjs.replace('__PAIRS__', json.dumps(PAIRS, ensure_ascii=False)) + "</body>", s)
open(os.path.join(ROOT, 'interior-3d.html'), 'w').write(s)
print('wrote interior-3d.html', len(s), 'bytes; texture counts', n)
