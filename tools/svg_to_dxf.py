"""Convert the two A3 kitchen sheets (plans/kitchen-sheet-*.svg) into AutoCAD DXF files.

The SVGs are drawn in paper millimetres (viewBox 420 x 297), so each DXF is the A3 sheet at paper size, 1 drawing unit = 1 mm.
The plans on the sheets are at 1:25 and the elevation at 1:40: scale a plan up by 25 (or the elevation by 40) to get real-world size,
or read the dimension labels. Colours become layers so a CAD user can switch them on and off.

Usage, from the repo root:  python3 tools/svg_to_dxf.py          (needs: pip install ezdxf)
Writes plans/kitchen-sheet-1-equipment.dxf and plans/kitchen-sheet-2-services.dxf
"""
import math, re, sys
import xml.etree.ElementTree as ET
import ezdxf
import ezdxf.zoom
from ezdxf import colors
from ezdxf.enums import TextEntityAlignment as TA

H = 297.0                      # sheet height in mm, used to flip SVG's downward y axis
NS = '{http://www.w3.org/2000/svg}'
LAYER_NAMES = {'#2a2420': 'INK', '#6a5d4e': 'MUTED', '#b23a1e': 'EXHAUST-RED', '#2f6f9f': 'WATER-BLUE', '#a8741a': 'GAS',
               '#3f6a3a': 'AIR-GREEN', '#6b3fa0': 'POWER', '#4a4038': 'WALLS', '#c9cdd1': 'STEEL', '#9aa0a5': 'HOT-LINE',
               '#fbf7ef': 'PAPER', '#fff': 'WHITE', '#ffffff': 'WHITE'}
LINEWEIGHTS = [0, 5, 9, 13, 15, 18, 20, 25, 30, 35, 40, 50, 53, 60, 70, 80, 90, 100, 106, 120, 140, 158, 200, 211]
FONT_CAP = 0.72                # SVG font-size is the em height; DXF text height is the cap height


def norm(c):
    c = c.strip().lower()
    if len(c) == 4 and c[0] == '#': c = '#' + ''.join(ch * 2 for ch in c[1:])
    return c


def layer_for(c, suffix=''):
    c = norm(c)
    base = LAYER_NAMES.get(c) or LAYER_NAMES.get(c[:4]) or 'COLOR-' + c.lstrip('#').upper()
    return base + suffix


def rgb(c):
    c = norm(c)
    return colors.rgb2int((int(c[1:3], 16), int(c[3:5], 16), int(c[5:7], 16)))


def lineweight(sw):
    v = float(sw) * 100
    return min(LINEWEIGHTS, key=lambda w: abs(w - v))


class Conv:
    def __init__(self, doc):
        self.doc, self.msp, self.n = doc, doc.modelspace(), {}
        self.layers = set()

    def layer(self, name, color):
        if name not in self.layers:
            self.doc.layers.add(name, true_color=rgb(color))
            self.layers.add(name)
        return name

    def count(self, k): self.n[k] = self.n.get(k, 0) + 1

    def attrs(self, el, inh):
        a = dict(inh)
        for k in ('fill', 'stroke', 'stroke-width', 'stroke-dasharray', 'font-size', 'font-weight', 'text-anchor'):
            if el.get(k) is not None: a[k] = el.get(k)
        return a

    def pt(self, x, y, off): return (float(x) + off[0], H - (float(y) + off[1]))

    def stroke_attribs(self, a):
        s = a.get('stroke', 'none')
        if s == 'none': return None
        d = {'layer': self.layer(layer_for(s), s), 'true_color': rgb(s), 'lineweight': lineweight(a.get('stroke-width', '0.25'))}
        if a.get('stroke-dasharray'): d['linetype'] = 'DASHED'
        return d

    def fill(self, pts, a):
        f = a.get('fill', 'black')
        if f == 'none': return
        h = self.msp.add_hatch(dxfattribs={'layer': self.layer('FILL-' + layer_for(f), f), 'true_color': rgb(f)})
        h.set_solid_fill(color=7, style=0, rgb=colors.int2rgb(rgb(f)))
        h.paths.add_polyline_path(pts, is_closed=True)
        self.count('hatch')

    def poly_path(self, ch, a, off):
        """straight-segment paths: M/m/L/l moves and lines, z closes (arrowheads and small symbols)"""
        subs, cur, pos = [], None, (0.0, 0.0)
        for cmd, args in re.findall(r'([MmLlZz])([^MmLlZz]*)', ch.get('d')):
            v = [float(n) for n in args.replace(',', ' ').split()]
            if cmd in 'Zz':
                if cur: cur[1] = True
                continue
            for i in range(0, len(v), 2):
                pos = (v[i], v[i + 1]) if cmd in 'ML' else (pos[0] + v[i], pos[1] + v[i + 1])
                if cmd in 'Mm' and i == 0: cur = [[pos], False]; subs.append(cur)
                else: cur[0].append(pos)
        sa = self.stroke_attribs(a)
        for pts, closed in subs:
            xy = [self.pt(x, y, off) for x, y in pts]
            if closed and ch.get('fill', 'none') != 'none': self.fill(xy, {'fill': ch.get('fill')})
            if sa and len(xy) > 1: self.msp.add_lwpolyline(xy, close=closed, dxfattribs=sa); self.count('polyline')

    def walk(self, el, inh, off):
        for ch in el:
            tag = ch.tag.replace(NS, '')
            a = self.attrs(ch, inh)
            if tag == 'g':
                o = off
                m = re.match(r'translate\(([-\d.]+)[ ,]+([-\d.]+)\)', ch.get('transform', ''))
                if m: o = (off[0] + float(m.group(1)), off[1] + float(m.group(2)))
                # a group's own stroke applies to its children, its fill does not
                self.walk(ch, a, o)
            elif tag == 'rect':
                x, y, w, h = (float(ch.get(k, 0)) for k in 'x y width height'.split())
                pts = [self.pt(x, y, off), self.pt(x + w, y, off), self.pt(x + w, y + h, off), self.pt(x, y + h, off)]
                self.fill(pts, {'fill': ch.get('fill', 'black')})
                sa = self.stroke_attribs({'stroke': ch.get('stroke', 'none'), 'stroke-width': ch.get('stroke-width', '0.25'), 'stroke-dasharray': ch.get('stroke-dasharray')})
                if sa: self.msp.add_lwpolyline(pts, close=True, dxfattribs=sa); self.count('rect')
            elif tag == 'line':
                sa = self.stroke_attribs(a)
                if sa:
                    self.msp.add_line(self.pt(ch.get('x1'), ch.get('y1'), off), self.pt(ch.get('x2'), ch.get('y2'), off), dxfattribs=sa); self.count('line')
            elif tag == 'polyline':
                sa = self.stroke_attribs(a)
                pts = [self.pt(*p.split(','), off) for p in ch.get('points').split()]
                if sa: self.msp.add_lwpolyline(pts, dxfattribs=sa); self.count('polyline')
            elif tag == 'circle':
                c = self.pt(ch.get('cx'), ch.get('cy'), off); r = float(ch.get('r'))
                f = ch.get('fill', 'black')
                if f != 'none':
                    h = self.msp.add_hatch(dxfattribs={'layer': self.layer('FILL-' + layer_for(f), f), 'true_color': rgb(f)})
                    h.set_solid_fill(color=7, style=0, rgb=colors.int2rgb(rgb(f)))
                    h.paths.add_edge_path().add_arc(c, r, 0, 360, ccw=True); self.count('hatch')
                sa = self.stroke_attribs({'stroke': ch.get('stroke', 'none'), 'stroke-width': ch.get('stroke-width', '0.25'), 'stroke-dasharray': ch.get('stroke-dasharray')})
                if sa: self.msp.add_circle(c, r, dxfattribs=sa); self.count('circle')
            elif tag == 'path':
                m = re.match(r'M([-\d.]+) ([-\d.]+) A([-\d.]+) ([-\d.]+) 0 0 ([01]) ([-\d.]+) ([-\d.]+)$', ch.get('d').strip())
                if not m:
                    self.poly_path(ch, a, off); continue
                x1, y1, r, _, sweep, x2, y2 = (float(v) for v in m.groups())
                p1, p2 = self.pt(x1, y1, off), self.pt(x2, y2, off)
                mx, my, dx, dy = (p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2, p2[0] - p1[0], p2[1] - p1[1]
                d = math.hypot(dx, dy); hgt = math.sqrt(max(r * r - d * d / 4, 0))
                # small-arc centre lies to one side of the chord; pick the side that matches the sweep after the y flip
                nx, ny = -dy / d, dx / d
                sgn = 1 if int(sweep) == 1 else -1                # SVG sweep 1 = clockwise on screen
                c = (mx + sgn * nx * hgt * -1, my + sgn * ny * hgt * -1)
                a1 = math.degrees(math.atan2(p1[1] - c[1], p1[0] - c[0])); a2 = math.degrees(math.atan2(p2[1] - c[1], p2[0] - c[0]))
                start, end = (a2, a1) if int(sweep) == 1 else (a1, a2)   # DXF arcs run counter-clockwise
                sa = self.stroke_attribs(a)
                if sa: self.msp.add_arc(c, r, start, end, dxfattribs=sa); self.count('arc')
            elif tag == 'text':
                t = ''.join(ch.itertext()).strip()
                if not t: continue
                size = float(ch.get('font-size', a.get('font-size', 2.5)))
                fill = a.get('fill', '#2a2420'); anchor = ch.get('text-anchor', 'start')
                x, y = self.pt(ch.get('x', 0), ch.get('y', 0), off)
                rot = 0.0
                m = re.match(r'rotate\(([-\d.]+)', ch.get('transform', ''))
                if m: rot = -float(m.group(1))
                al = {'start': TA.BOTTOM_LEFT, 'middle': TA.BOTTOM_CENTER, 'end': TA.BOTTOM_RIGHT}[anchor]
                e = self.msp.add_text(t, height=size * FONT_CAP, rotation=rot, dxfattribs={'layer': self.layer(layer_for(fill, '-TEXT'), fill), 'true_color': rgb(fill), 'style': 'KITCHEN'})
                e.set_placement((x, y), align=al); self.count('text')


def convert(svg_path, dxf_path):
    doc = ezdxf.new('R2010', setup=True)
    doc.units = ezdxf.units.MM
    doc.styles.add('KITCHEN', font='arial.ttf')
    root = ET.parse(svg_path).getroot()
    c = Conv(doc)
    # paper-coloured sheet underneath, so dark text stays readable on AutoCAD's black model-space background
    bg = [ch for ch in root if ch.tag.replace(NS, '') == 'rect' and ch.get('x') is None][0]
    c.fill([(0, 0), (420, 0), (420, H), (0, H)], {'fill': bg.get('fill')})
    root.remove(bg)
    c.walk(root, {'fill': '#2a2420', 'stroke': 'none', 'stroke-width': '0.25'}, (0, 0))
    ezdxf.zoom.extents(c.msp)
    # ezdxf leaves the header extents unset (1e20); some viewers, LibreOffice included, then mis-scale the drawing
    doc.header['$EXTMIN'], doc.header['$EXTMAX'] = (0, 0, 0), (420, H, 0)
    doc.header['$LIMMIN'], doc.header['$LIMMAX'] = (0, 0), (420, H)
    doc.saveas(dxf_path)
    return c.n


if __name__ == '__main__':
    for src, dst in (('plans/kitchen-sheet-1-equipment.svg', 'plans/kitchen-sheet-1-equipment.dxf'),
                     ('plans/kitchen-sheet-2-services.svg', 'plans/kitchen-sheet-2-services.dxf')):
        print(dst, convert(src, dst))
