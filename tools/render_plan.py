import subprocess,sys,re,os,time
d=os.path.abspath(sys.argv[1])  # folder holding plan_noloft_render.html; writes plans/ground-floor-plan-noloft.png
src=open(f'{d}/plan_noloft_render.html').read()
W,H=map(int,re.search(r'width="(\d+)" height="(\d+)"',src).groups())
CH="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
n=2; th=(H+n-1)//n; tiles=[]
os.makedirs(f'{d}/plans',exist_ok=True)
for i in range(n):
    off=i*th; h=min(th,H-off)
    html=src.replace('<style>html,body{margin:0;background:#fbf7ef}</style>',f'<style>html,body{{margin:0;background:#fbf7ef;overflow:hidden}}svg{{display:block;margin-top:-{off}px}}</style>')
    assert f'margin-top:-{off}px' in html
    f=f'{d}/tile{i}.html'; open(f,'w').write(html); png=f'{d}/tile{i}.png'
    for attempt in range(5):
        if os.path.exists(png): os.remove(png)
        subprocess.run([CH,'--headless','--hide-scrollbars','--force-device-scale-factor=2.5',f'--window-size={W},{h}',f'--screenshot={png}','file://'+f],capture_output=True)
        m=re.search(r'pixelHeight: (\d+)',subprocess.run(['sips','-g','pixelHeight',png],capture_output=True,text=True).stdout) if os.path.exists(png) else None
        got=int(m.group(1)) if m else 0
        if abs(got-round(h*2.5))<=3: break
        time.sleep(1)
    else: sys.exit(f'tile {i} failed: {got} vs {h*2.5}')
    tiles.append(png)
subprocess.run(['magick',*tiles,'-append',f'{d}/plans/ground-floor-plan-noloft.png'],check=True)
print(subprocess.run(['sips','-g','pixelWidth','-g','pixelHeight',f'{d}/plans/ground-floor-plan-noloft.png'],capture_output=True,text=True).stdout.strip())
