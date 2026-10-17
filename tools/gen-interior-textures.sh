#!/bin/bash
# usage: tools/gen-kitchen-textures.sh [<id>...]  Raw Flow interior textures -> renders/tex-raw/<id>.png (then run tools/make_interior_textures.py). Free Flow images, one at a time.
set -u
export GFLOW_CLI_UPDATE_CHECK=0 GFLOW_CLI_LEASE_WAIT_SECONDS=600
cd "$(dirname "$0")/.."
PROJECT=5657dbf4-d0a4-414b-9fda-48d501728c40
OUT=${FLOW_OUT:-/tmp/flow-itex}; mkdir -p "$OUT" renders/tex-raw
ids=("$@"); [ ${#ids[@]} -eq 0 ] && ids=($(python3 -c "import runpy;print(' '.join(runpy.run_path('tools/interior_texture_jobs.py')['JOBS']))"))
for id in "${ids[@]}"; do
  [ -f "renders/tex-raw/$id.png" ] && { echo "skip $id"; continue; }
  read -r ASPECT < <(python3 -c "import runpy,sys;print(runpy.run_path('tools/interior_texture_jobs.py')['JOBS'][sys.argv[1]][0])" "$id")
  PROMPT=$(python3 -c "import runpy,sys;print(runpy.run_path('tools/interior_texture_jobs.py')['JOBS'][sys.argv[1]][1])" "$id")
  d="$OUT/$id"; rm -rf "$d"; mkdir -p "$d"; ok=0
  for try in 1 2 3; do
    gflow image t2i "$PROMPT" --model nano2 --aspect "$ASPECT" -n 1 --project "$PROJECT" --out "$d" >"$d/log.txt" 2>&1 && f=$(ls "$d"/*.png "$d"/*.jpg "$d"/*.jpeg "$d"/*.webp 2>/dev/null | head -1) && [ -n "$f" ] && { ok=1; break; }
    echo "retry $id ($try)"; sleep 8
  done
  if [ $ok = 1 ]; then python3 -c "
from PIL import Image
Image.open('$f').convert('RGB').save('renders/tex-raw/$id.png')"; echo "done $id"; else echo "FAILED $id"; tail -3 "$d/log.txt"; fi
done
