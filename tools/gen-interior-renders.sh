#!/bin/bash
# usage: tools/gen-interior-renders.sh [<id>...]  Photoreal interior views via Google Flow (free images), one at a time. Skips ids that exist.
# Reference 1 = tools/interior-refs/<id>.jpg (the photo-textured model); reference 2 = a sheet of the Furnishings product images (tools/furnishing-refs/) for that view. Writes renders/interior3d-<id>-photo.jpg.
set -u
export GFLOW_CLI_UPDATE_CHECK=0 GFLOW_CLI_LEASE_WAIT_SECONDS=600
cd "$(dirname "$0")/.."
PROJECT=5657dbf4-d0a4-414b-9fda-48d501728c40
OUT=${FLOW_OUT:-/tmp/flow-interior}; mkdir -p "$OUT" renders
ids=("$@"); [ ${#ids[@]} -eq 0 ] && ids=($(python3 -c "import runpy;print(' '.join(runpy.run_path('tools/interior_render_jobs.py')['JOBS']))"))
for id in "${ids[@]}"; do
  [ -f "renders/interior3d-$id-photo.jpg" ] && { echo "skip $id"; continue; }
  # gflow handles two references reliably, so the Furnishings product images are combined into one reference sheet
  python3 - "$id" "$OUT" <<'PY'
import sys,runpy,math
from PIL import Image
i,out=sys.argv[1:3]; refs,_=runpy.run_path('tools/interior_render_jobs.py')['JOBS'][i]
n=len(refs); cols=2 if n>1 else 1; rows=math.ceil(n/cols); W,H=800,600
sheet=Image.new('RGB',(W*cols,H*rows),'white')
for k,r in enumerate(refs): sheet.paste(Image.open('tools/furnishing-refs/%s.jpg'%r).convert('RGB').resize((W,H)),((k%cols)*W,(k//cols)*H))
sheet.save('%s/%s-sheet.jpg'%(out,i),quality=88)
PY
  REFARGS=(--ref "tools/interior-refs/$id.jpg" --ref "$OUT/$id-sheet.jpg")
  PROMPT=$(python3 -c "import runpy,sys;print(runpy.run_path('tools/interior_render_jobs.py')['JOBS'][sys.argv[1]][1])" "$id")
  d="$OUT/$id"; rm -rf "$d"; mkdir -p "$d"; ok=0
  for try in 1 2 3; do
    gflow image i2i "$PROMPT" "${REFARGS[@]}" --model nano2 --aspect 4:3 -n 1 --project "$PROJECT" --out "$d" >"$d/log.txt" 2>&1 && f=$(ls "$d"/*.png "$d"/*.jpg "$d"/*.jpeg "$d"/*.webp 2>/dev/null | head -1) && [ -n "$f" ] && { ok=1; break; }
    echo "retry $id ($try)"; sleep 8
  done
  if [ $ok = 1 ]; then python3 -c "
from PIL import Image
im=Image.open('$f').convert('RGB'); im=im.resize((1600,1200),Image.LANCZOS); im.save('renders/interior3d-$id-photo.jpg','JPEG',quality=86,optimize=True)"; echo "done $id"; else echo "FAILED $id"; tail -3 "$d/log.txt"; fi
done
