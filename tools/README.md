# Floor-plan tools

`plan.py` draws the dimensioned ground-floor plan as SVG from the same coordinates as the 3D model (`index.html`). `render_plan.py` turns it into the high-resolution PNG (2.5×, rendered in two tiles because Chrome caps screenshot height).

Regenerate after any layout change, from the repo root:

```sh
python3 tools/plan.py build
python3 tools/render_plan.py build
cp build/plan_noloft.svg plans/ground-floor-plan-noloft.svg
cp build/plans/ground-floor-plan-noloft.png plans/
```

Then paste the new SVG into `plan.html` (replace the `<svg id="plan" …>` element). Needs Python 3, Google Chrome (macOS path in `render_plan.py`) and ImageMagick (`magick`).

Coordinates: x runs from the right wall (−2.45) to the left wall (2.45) as you walk in from the road; z runs from the shopfront (0) to the back wall (8.8).

`boq.py` writes the kitchen bill of quantities (`boq.html`, `plans/kitchen-boq.xlsx`, `.csv`); print `boq.html` from Chrome headless (A4 landscape, no header or footer) for `plans/kitchen-boq.pdf`. `kitchen_sheets.py` draws the two A3 kitchen sheets and `kitchen.html`.

`boq_goa.py` writes the separate kitchen equipment and exhaust BOQ in feet and inches, SWG, CFM and TR (`boq-goa.html`, `plans/kitchen-boq-goa.xlsx`, `.csv`; PDF from Chrome headless, A4 landscape). It reads the item list from `boq.py`, so the two stay in step.

`boq_drawing.py` writes `boq-drawing.html`: the 1:25 kitchen and exhaust plan with numbered balloons (every size in mm) above the equipment and exhaust BOQ in mm only. Print it from Chrome headless on A3 portrait (`--print-to-pdf=plans/kitchen-drawing-boq-mm.pdf`, no header or footer). Its Sl numbers are the 1.xx, 2.xx, 3.xx lines of `boq_goa.py`.
