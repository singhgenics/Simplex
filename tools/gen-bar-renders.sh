#!/bin/bash
# usage: tools/gen-bar-renders.sh products|views|[<kind>:<id> ...]   Bar equipment shots and bar-section views via Google Flow (free images), one at a time. Skips files that exist.
#   products -> renders/bar/product-<id>.jpg (text-to-image, 1200x900)
#   views    -> renders/bar/<id>-photo.jpg  (reference 1 = tools/bar-refs/<id>.jpg, reference 2 = sheet of the product shots for that view)
set -u
export GFLOW_CLI_UPDATE_CHECK=0 GFLOW_CLI_LEASE_WAIT_SECONDS=600
cd "$(dirname "$0")/.."
PROJECT=5657dbf4-d0a4-414b-9fda-48d501728c40
OUT=${FLOW_OUT:-/tmp/flow-bar}; mkdir -p "$OUT" renders/bar
run() { # $1 id  $2 prompt  $3 outfile  $4 W  $5 H  rest: gflow args
  local id=$1 prompt=$2 outf=$3 W=$4 H=$5; shift 5; local d="$OUT/$id" ok=0 f
  rm -rf "$d"; mkdir -p "$d"
  for try in 1 2 3; do
    gflow image "$@" "$prompt" --model nano2 --aspect 4:3 -n 1 --project "$PROJECT" --out "$d" >"$d/log.txt" 2>&1 && f=$(ls "$d"/*.png "$d"/*.jpg "$d"/*.jpeg "$d"/*.webp 2>/dev/null | head -1) && [ -n "$f" ] && { ok=1; break; }
    echo "retry $id ($try)"; sleep 8
  done
  if [ $ok = 1 ]; then python3 -c "
from PIL import Image
im=Image.open('$f').convert('RGB').resize(($W,$H),Image.LANCZOS); im.save('$outf','JPEG',quality=86,optimize=True)"; echo "done $id"; else echo "FAILED $id"; tail -3 "$d/log.txt"; fi
}
pids() { python3 -c "import runpy;print(' '.join(runpy.run_path('tools/bar_render_jobs.py')['$1']))"; }
what=${1:-all}
if [ "$what" = products ] || [ "$what" = all ]; then
  for id in $(pids PRODUCTS); do
    [ -f "renders/bar/product-$id.jpg" ] && { echo "skip product $id"; continue; }
    P=$(python3 -c "import runpy,sys;print(runpy.run_path('tools/bar_render_jobs.py')['PRODUCTS'][sys.argv[1]])" "$id")
    run "p-$id" "$P" "renders/bar/product-$id.jpg" 1200 900 t2i
  done
fi
if [ "$what" = views ] || [ "$what" = all ]; then
  for id in $(pids VIEWS); do
    [ -f "renders/bar/$id-photo.jpg" ] && { echo "skip view $id"; continue; }
    python3 - "$id" "$OUT" <<'PY'
import sys,runpy,math
from PIL import Image
i,out=sys.argv[1:3]; refs,_=runpy.run_path('tools/bar_render_jobs.py')['VIEWS'][i]
n=len(refs); cols=3 if n>4 else 2 if n>1 else 1; rows=math.ceil(n/cols); W,H=600,450
sheet=Image.new('RGB',(W*cols,H*rows),'white')
for k,r in enumerate(refs): sheet.paste(Image.open('renders/bar/product-%s.jpg'%r).convert('RGB').resize((W,H)),((k%cols)*W,(k//cols)*H))
sheet.save('%s/%s-sheet.jpg'%(out,i),quality=88)
PY
    P=$(python3 -c "import runpy,sys;print(runpy.run_path('tools/bar_render_jobs.py')['VIEWS'][sys.argv[1]][1])" "$id")
    run "v-$id" "$P" "renders/bar/$id-photo.jpg" 1600 1200 i2i --ref "tools/bar-refs/$id.jpg" --ref "$OUT/$id-sheet.jpg"
  done
fi
