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

## Kitchen sheets as AutoCAD files

`svg_to_dxf.py` converts `plans/kitchen-sheet-1-equipment.svg` and `plans/kitchen-sheet-2-services.svg` into DXF (`pip install ezdxf`, then `python3 tools/svg_to_dxf.py` from the repo root). Each DXF is the A3 sheet at paper size, 1 unit = 1 mm, with colours as layers. The plans are drawn at 1:25 and the elevation at 1:40, so scale a plan by 25 (the elevation by 40) for real-world size. Rerun it after `kitchen_sheets.py` changes the SVGs.
