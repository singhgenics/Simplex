# Real-photo textures for the kitchen model (kitchen-3d.html "Photo textures"): id -> (aspect for Flow, prompt). Processed by tools/make_textures.py.
FLAT = "Perfectly flat front-on orthographic photograph, no perspective, even soft lighting, no shadows, no vignette, fills the whole frame edge to edge, no background, no text, no logos. "
FRONT = FLAT + "The front face of a commercial stainless steel 304 kitchen unit, photographed straight on so it fills the frame; panel seams and gaps only; NO handles and NO knobs (they are modelled separately). "
JOBS = {
 "ss-brushed": ("1:1", FLAT + "Close texture photograph of brushed stainless steel sheet with fine horizontal grain and very subtle wear, uniform across the frame, no dents, no edges."),
 "tile-75": ("1:1", FLAT + "A wall of white glazed square ceramic tiles with thin mid-grey grout, exactly 8 columns by 8 rows of tiles, perfectly aligned grid, slight gloss, filling the frame."),
 "floor-epoxy": ("1:1", FLAT + "Macro photograph of smooth light-grey polished concrete, a seamless material swatch with subtle tonal variation."),
 "ceiling-board": ("1:1", FLAT + "Close texture photograph of a white-painted cement board ceiling with faint flush joints, matt, uniform."),
 "front-wok": ("4:3", FRONT + "A wok range cabinet front: a stainless fascia strip across the top and two plain flat stainless doors below, filling the frame."),
 "front-steamer": ("3:4", FRONT + "A dim sum steamer cabinet front: stainless control fascia on top and a plain flat stainless door below."),
 "front-fryer": ("3:4", FRONT + "A twin-tank fryer cabinet front: stainless control fascia on top and a plain flat stainless door below with a small drain-valve slot."),
 "front-stock": ("3:4", FRONT + "A stock pot range cabinet front: stainless control fascia on top and a plain flat stainless door below."),
 "front-reachin": ("9:16", FRONT + "Two tall stainless refrigerator doors side by side with a thin central gap, rubber gasket lines visible, a small digital temperature display on the upper right door."),
 "front-dishwasher": ("1:1", FRONT + "An under-counter dishwasher front door in stainless with a small control strip at the top edge."),
 "front-sink": ("4:3", FRONT + "A stainless sink cabinet front with two plain flat doors."),
 "bench-door": ("3:4", FRONT + "A single plain flat stainless cabinet door for an under-counter fridge, with a subtle seam around it."),
 "kitchen-door": ("9:16", FRONT + "A pair of stainless double-acting kitchen swing doors, each with a rectangular glass vision panel at head height and a kick plate at the bottom, no push plates."),
 "rear-door": ("9:16", FLAT + "A flat painted steel fire-exit door in dull grey-green with a small wire-glass window at head height, a kick plate at the bottom, no handle."),
}
