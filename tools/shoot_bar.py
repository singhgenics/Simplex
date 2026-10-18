#!/usr/bin/env python3
"""Renders the bar-section views (exact model and photo-textured model) from fixed cameras with headless Chrome, from interior-3d.html.
Needs playwright (the gflow-cli Python has it) and the page served over http: python3 -m http.server 8765 from the Simplex folder.
usage: python3 tools/shoot_bar.py [id ...] -> renders/bar/<id>-model.jpg, <id>-tex.jpg and tools/bar-refs/<id>.jpg"""
import json, os, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.join(HERE, '..')
from playwright.sync_api import sync_playwright
# id: (camera position, target) in model coordinates (x from the right wall -2.45 to the left wall +2.45, z from the shopfront 0 to the back wall 8.8)
VIEWS = {
 'guest':   ([-1.0, 1.75, 0.8], [1.5, 1.45, 4.6]),
 'aisle':   ([1.55, 1.55, 2.55], [1.75, 0.95, 5.0]),
 'equip':   ([1.25, 1.3, 2.95], [2.45, 0.6, 4.25]),
 'kegs':    ([1.75, 1.35, 4.87], [1.15, 0.45, 3.52]),
 'ice':     ([1.75, 1.35, 5.75], [1.0, 0.65, 4.75]),
 'top':     ([1.25, 6.6, 4.15], [1.25, 0, 4.15]),
}
ids = sys.argv[1:] or list(VIEWS)
def shot(pg, view, photo, path):
    (p, t) = VIEWS[view]
    pg.evaluate(f"(()=>{{const k=__k;k.camera.position.set({p[0]},{p[1]},{p[2]});k.controls.target.set({t[0]},{t[1]},{t[2]});k.controls.update();k.state.photo={'true' if photo else 'false'};k.setPhoto(k.state.photo);k.setDirty();}})()")
    pg.wait_for_timeout(3500); pg.screenshot(path='/tmp/_bshot.png')
    subprocess.run(['sips', '-s', 'format', 'jpeg', '-s', 'formatOptions', '88', '/tmp/_bshot.png', '--out', path], capture_output=True)
with sync_playwright() as p:
    b = p.chromium.launch(channel='chrome', args=['--use-gl=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'])
    pg = b.new_page(viewport={'width': 1600, 'height': 1200}); errs = []
    pg.on('pageerror', lambda e: errs.append(str(e)))
    pg.goto('http://127.0.0.1:8765/interior-3d.html'); pg.wait_for_timeout(9000)
    pg.add_style_tag(content='.panel,.toolbar,.hint,.card,.labels,.htag,.cmp{display:none!important}.app{display:block!important;height:1200px!important;min-height:0!important}.stage{width:1600px!important;height:1200px!important}')
    pg.evaluate("window.dispatchEvent(new Event('resize'))"); pg.wait_for_timeout(1000)
    print('page errors', errs[:3])
    for i in ids:
        shot(pg, i, False, os.path.join(ROOT, 'renders', 'bar', f'{i}-model.jpg'))
        shot(pg, i, True, os.path.join(ROOT, 'renders', 'bar', f'{i}-tex.jpg'))
        subprocess.run(['sips', '-Z', '1200', '-s', 'format', 'jpeg', '-s', 'formatOptions', '86', os.path.join(ROOT, 'renders', 'bar', f'{i}-tex.jpg'), '--out', os.path.join(HERE, 'bar-refs', f'{i}.jpg')], capture_output=True)
        print('shot', i)
    b.close()
