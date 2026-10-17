# Real-photo textures for the interior model (interior-3d.html "Photo textures"): id -> (Flow aspect, prompt). Processed by tools/make_interior_textures.py.
FLAT = "Perfectly flat orthographic photograph, no perspective, even soft lighting, no shadows, no vignette, fills the whole frame edge to edge, no objects, no people, no text. "
# int-acacia, int-cane, int-velvet and int-onyx come from the Furnishings images in the Menu repo (the chair, bar stool, table and bar front), see make_interior_textures.py
JOBS = {
 "int-brick": ("1:1", FLAT + "A wall of burnt-red clay bricks in running bond with off-white lime mortar, exactly 4 bricks across and 8 courses high, slightly irregular, matt."),
 "int-checker": ("1:1", FLAT + "Top-down view of a black and white porcelain checkerboard floor, exactly 6 by 6 squares, matt, crisp grout lines."),
 "int-reclaim": ("1:1", FLAT + "A wall of reclaimed weathered teak and mixed-wood planks laid horizontally, varied warm browns, old nail holes and grain."),
 "int-marble": ("1:1", FLAT + "A honed white Makrana marble slab with soft grey veining."),
 "int-mosaic": ("1:1", FLAT + "An emerald green glass mosaic tile wall, exactly 8 columns by 8 rows of small square tiles with grey grout."),
 "int-limewash": ("1:1", FLAT + "A cream lime-wash plaster wall with a soft mottled hand-trowelled texture."),
 "int-concrete": ("1:1", FLAT + "Raw grey board-marked concrete surface with subtle horizontal formwork lines."),
}
