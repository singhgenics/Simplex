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
