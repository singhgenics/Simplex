#!/usr/bin/env python3
"""Interior textures for interior-3d.html. Two sources: (1) the furniture images generated for the Furnishings section of the Menu repo
(tools/furnishing-refs/: the cane chair, velvet bar stool, acacia table and the glowing bar front) are cropped to give the cane back, velvet,
table top and onyx-mesh bar front textures, so the model uses the designed pieces; (2) raw Flow textures in renders/tex-raw/int-*.png (brick, checker,
mosaic, reclaimed wood, marble, lime-wash, concrete) are cropped to whole tiles / made tileable. Writes renders/tex/*.jpg and renders/tex/interior.json."""
import os, json
import numpy as np
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.join(HERE, '..')
RAW, OUT, REF = os.path.join(ROOT, 'renders', 'tex-raw'), os.path.join(ROOT, 'renders', 'tex'), os.path.join(HERE, 'furnishing-refs')
os.makedirs(OUT, exist_ok=True)
info = {}
def save(im, name, size=512):
    im = im.convert('RGB').resize((size, size) if size else im.size, Image.LANCZOS); im.save(os.path.join(OUT, name + '.jpg'), 'JPEG', quality=88, optimize=True); print('wrote', name)
def raw(i):
    p = os.path.join(RAW, i + '.png'); return Image.open(p).convert('RGB') if os.path.exists(p) else None
def seamless(im, size=512):
    im = im.resize((size, size), Image.LANCZOS); a = np.asarray(im, float)
    w = np.hanning(size); m = np.outer(w, w)[..., None] ** 0.5
    r = np.roll(np.roll(a, size // 2, 0), size // 2, 1)
    return Image.fromarray(np.clip(a * m + r * (1 - m), 0, 255).astype('uint8'))
def period(prof, lo=10):
    p = prof - prof.mean(); ac = np.correlate(p, p, 'full')[len(p) - 1:]; return lo + int(np.argmax(ac[lo:len(p) // 2]))
def grid(im, even=False):
    a = np.asarray(im.convert('L'), float); W, H = im.size
    p = (period(a.mean(axis=0)) + period(a.mean(axis=1))) / 2
    cx = int(np.argmin(a.mean(axis=0)[:int(p)])); cy = int(np.argmin(a.mean(axis=1)[:int(p)]))
    n = max(2, min(int((W - cx) // p), int((H - cy) // p)))
    if even and n % 2: n -= 1
    return im.crop((cx, cy, int(cx + n * p), int(cy + n * p))).resize((512, 512), Image.LANCZOS), n
def crop(name, box):
    return Image.open(os.path.join(REF, name + '.jpg')).convert('RGB').crop(box)
def main():
    # (1) the Furnishings furniture, cropped
    save(crop('chair', (352, 132, 488, 238)), 'int-cane')           # cane back of the S1 chair
    save(crop('stool', (470, 140, 590, 230)), 'int-velvet')         # sand velvet of the S2 bar stool
    save(crop('table', (200, 200, 420, 250)), 'int-acacia')         # acacia plank top of the T1 table
    save(crop('barfront', (318, 258, 565, 590)), 'int-onyx')        # back-lit onyx under the brass mesh, B3 bar front
    # (2) raw Flow textures
    im = raw('int-brick')
    if im: save(im, 'int-brick'); info['brick'] = [4, 8]
    im = raw('int-checker')
    if im: save(im, 'int-checker'); info['checker'] = 6      # prompt asks for exactly 6 x 6 squares; the autocorrelation grid finder is unreliable on a 2-colour checker
    im = raw('int-mosaic')
    if im: t, n = grid(im); t.save(os.path.join(OUT, 'int-mosaic.jpg'), 'JPEG', quality=88); info['mosaic'] = n; print('mosaic tiles', n)
    for i in ('int-reclaim', 'int-marble', 'int-limewash', 'int-concrete'):
        im = raw(i)
        if im: save(seamless(im), i)
    json.dump(info, open(os.path.join(OUT, 'interior.json'), 'w')); print(info)
if __name__ == '__main__': main()
