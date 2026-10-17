#!/bin/bash
# usage: tools/gen-kitchen-renders.sh [<id>...]   Photoreal kitchen views from the exact 3D model renders, via Google Flow (free images).
# Writes renders/kitchen3d-<id>-photo.jpg (1600x1200). Runs one at a time (the gflow profile allows one process). Skips ids that exist.
set -u
export GFLOW_CLI_UPDATE_CHECK=0 GFLOW_CLI_LEASE_WAIT_SECONDS=600
cd "$(dirname "$0")/.."
PROJECT=5657dbf4-d0a4-414b-9fda-48d501728c40
OUT=${FLOW_OUT:-/tmp/flow-kitchen}; mkdir -p "$OUT" renders
ids=("$@"); [ ${#ids[@]} -eq 0 ] && ids=($(python3 -c "import runpy;print(' '.join(runpy.run_path('tools/kitchen_render_jobs.py')['JOBS']))"))
for id in "${ids[@]}"; do
  [ -f "renders/kitchen3d-$id-photo.jpg" ] && { echo "skip $id"; continue; }
  PROMPT=$(python3 -c "import runpy,sys;print(runpy.run_path('tools/kitchen_render_jobs.py')['JOBS'][sys.argv[1]])" "$id")
  d="$OUT/$id"; rm -rf "$d"; mkdir -p "$d"; ok=0
  for try in 1 2 3; do
    gflow image i2i "$PROMPT" --ref "tools/kitchen-refs/$id.jpg" --model nano2 --aspect 4:3 -n 1 --project "$PROJECT" --out "$d" >"$d/log.txt" 2>&1 && f=$(ls "$d"/*.png "$d"/*.jpg "$d"/*.jpeg "$d"/*.webp 2>/dev/null | head -1) && [ -n "$f" ] && { ok=1; break; }
    echo "retry $id ($try)"; sleep 8
  done
  if [ $ok = 1 ]; then python3 -c "
from PIL import Image
im=Image.open('$f').convert('RGB'); im=im.resize((1600,1200),Image.LANCZOS); im.save('renders/kitchen3d-$id-photo.jpg','JPEG',quality=86,optimize=True)"; echo "done $id"; else echo "FAILED $id"; tail -3 "$d/log.txt"; fi
done
