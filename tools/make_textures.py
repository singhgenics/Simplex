#!/usr/bin/env python3
"""Turns the raw Flow textures in renders/tex-raw/ into the textures used by kitchen-3d.html (renders/tex/): crops each front to the exact face
aspect of the BOQ item, splits the paired doors, finds the tile grid so the wall texture repeats on a true 75 mm pitch, and makes the grain
textures tileable. Writes the tile count into kitchen-3d.html (TILE_N)."""
import os, re, sys
import numpy as np
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.join(HERE, '..')
RAW, OUT = os.path.join(ROOT, 'renders', 'tex-raw'), os.path.join(ROOT, 'renders', 'tex'); os.makedirs(OUT, exist_ok=True)
def load(i):
    p = os.path.join(RAW, i + '.png'); return Image.open(p).convert('RGB') if os.path.exists(p) else None
def crop_aspect(im, ar, cx=0.5):          # crop to width/height = ar, centred
    w, h = im.size
    if w / h > ar: nw = int(h * ar); x = int((w - nw) * cx); return im.crop((x, 0, x + nw, h))
    nh = int(w / ar); y = (h - nh) // 2; return im.crop((0, y, w, y + nh))
def save(im, name, maxs=1024):
    im = im.copy(); im.thumbnail((maxs, maxs), Image.LANCZOS); im.save(os.path.join(OUT, name + '.jpg'), 'JPEG', quality=86, optimize=True); print('wrote', name, im.size)
def seamless(im, size=512):
    im = im.resize((size, size), Image.LANCZOS); a = np.asarray(im, float)
    w = np.hanning(size); m = np.outer(w, w)[..., None] ** 0.5          # 1 in the middle, 0 at the borders
    r = np.roll(np.roll(a, size // 2, 0), size // 2, 1)
    return Image.fromarray(np.clip(a * m + r * (1 - m), 0, 255).astype('uint8'))
def period(prof):
    p = prof - prof.mean(); ac = np.correlate(p, p, 'full')[len(p) - 1:]
    lo = 12; hi = len(p) // 2; return lo + int(np.argmax(ac[lo:hi]))
def tile_grid(im):
    a = np.asarray(im.convert('L'), float); W, H = im.size
    pc, pr = period(a.mean(axis=0)), period(a.mean(axis=1)); p = (pc + pr) / 2
    cx = int(np.argmin(a.mean(axis=0)[:int(p)])); cy = int(np.argmin(a.mean(axis=1)[:int(p)]))
    n = max(2, min(int((W - cx) // p), int((H - cy) // p)))
    c = im.crop((cx, cy, int(cx + n * p), int(cy + n * p))); return c.resize((512, 512), Image.LANCZOS), n, round(p, 1)
def main():
    for i in ('ss-brushed', 'floor-epoxy', 'ceiling-board'):
        im = load(i)
        if im: save(seamless(im), i, 512)
    im = load('tile-75')
    if im:
        t, n, p = tile_grid(im); save(t, 'tile-75'); print('tile grid: period', p, 'px,', n, 'tiles per side')
        f = os.path.join(ROOT, 'kitchen-3d.html'); s = open(f).read(); s2 = re.sub(r'const TILE_N=\d+;/\*tile-n\*/', f'const TILE_N={n};/*tile-n*/', s)
        if s2 != s: open(f, 'w').write(s2)
    # fronts: exact face aspect (width / height) of the BOQ item
    for i, ar in (('front-wok', 1.2 / 0.8), ('front-steamer', 0.6 / 0.8), ('front-fryer', 0.6 / 0.9), ('front-stock', 0.6 / 0.85), ('front-dishwasher', 0.6 / 0.7), ('front-sink', 0.8 / 0.9), ('bench-door', 0.4 / 0.69)):
        im = load(i)
        if im: save(crop_aspect(im, ar), i)
    im = load('front-reachin')                       # two doors in one picture: left and right halves, each 0.475 wide x 1.72 high
    if im:
        w, h = im.size
        for k, nm in enumerate(('front-reachin-l', 'front-reachin-r')): save(crop_aspect(im.crop((k * w // 2, 0, (k + 1) * w // 2, h)), 0.475 / 1.72), nm)
    im = load('kitchen-door')                        # pair of leaves, each 0.40 x 2.05
    if im:
        w, h = im.size
        for k, nm in enumerate(('kitchen-door-l', 'kitchen-door-r')): save(crop_aspect(im.crop((k * w // 2, 0, (k + 1) * w // 2, h)), 0.4 / 2.05), nm)
    im = load('rear-door')
    if im: save(crop_aspect(im, 0.8 / 2.1), 'rear-door')
if __name__ == '__main__': main()
