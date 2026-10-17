#!/usr/bin/env python3
"""Renders the interior-3d.html views (exact model and photo-textured model) from fixed cameras with headless Chrome.
Needs playwright (the gflow-cli Python has it; macOS sips converts the images) and the page served over http: python3 -m http.server 8765 from the Simplex folder.
usage: python3 tools/shoot_interior.py [id ...]   -> renders/interior3d-<id>-model.jpg, -tex.jpg and tools/interior-refs/<id>.jpg"""
import json, os, sys
import subprocess
from playwright.sync_api import sync_playwright
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.join(HERE, '..')
KEY = {'washwc': 'niche'}
ids = sys.argv[1:] or [p[0] for p in json.load(open(os.path.join(HERE, 'interior_views.json')))]
def shot(pg, key, photo, path):
    pg.evaluate(f"(()=>{{const k=__k;k.goView(true?{json.dumps(key)}:'',true);k.state.photo={'true' if photo else 'false'};k.setPhoto(k.state.photo);k.setDirty();}})()")
    pg.wait_for_timeout(3500)
    pg.screenshot(path='/tmp/_shot.png')
    subprocess.run(['sips', '-s', 'format', 'jpeg', '-s', 'formatOptions', '88', '/tmp/_shot.png', '--out', path], capture_output=True)
with sync_playwright() as p:
    b = p.chromium.launch(channel='chrome', args=['--use-gl=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'])
    pg = b.new_page(viewport={'width': 1600, 'height': 1200}); errs = []
    pg.on('pageerror', lambda e: errs.append(str(e)))
    pg.goto('http://127.0.0.1:8765/interior-3d.html'); pg.wait_for_timeout(9000)
    pg.add_style_tag(content='.panel,.toolbar,.hint,.card,.labels,.htag,.cmp{display:none!important}.app{display:block!important;height:1200px!important;min-height:0!important}.stage{width:1600px!important;height:1200px!important}')
    pg.evaluate("window.dispatchEvent(new Event('resize'))"); pg.wait_for_timeout(1000)
    print('page errors', errs[:3])
    for i in ids:
        key = KEY.get(i, i)
        shot(pg, key, False, os.path.join(ROOT, 'renders', f'interior3d-{i}-model.jpg'))
        shot(pg, key, True, os.path.join(ROOT, 'renders', f'interior3d-{i}-tex.jpg'))
        subprocess.run(['sips', '-Z', '1200', '-s', 'format', 'jpeg', '-s', 'formatOptions', '86', os.path.join(ROOT, 'renders', f'interior3d-{i}-tex.jpg'), '--out', os.path.join(HERE, 'interior-refs', f'{i}.jpg')], capture_output=True)
        print('shot', i)
    b.close()
