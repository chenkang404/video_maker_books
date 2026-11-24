"""Decode every frame; detect unintended full-frame flashes outside authored cuts."""
import argparse,json,subprocess
from pathlib import Path
import numpy as np
p=argparse.ArgumentParser();p.add_argument('video');p.add_argument('--output');args=p.parse_args()
raw=subprocess.check_output(['ffmpeg','-v','error','-i',args.video,'-vf','scale=108:192','-pix_fmt','rgb24','-f','rawvideo','-'])
a=np.frombuffer(raw,np.uint8).reshape(-1,192,108,3)
d=np.abs(np.diff(a.astype(float),axis=0)).mean(axis=(1,2,3))
t=np.arange(1,len(a))/24
cuts=[4.5,12.28,19.76,27.18]
allowed=np.zeros(len(d),bool)
for cut in cuts: allowed|=np.abs(t-cut)<2/24
bad=np.flatnonzero((d>15)&~allowed)
# A nearly uniform full-width stripe indicates missing browser paint tiles.
row_std=a.astype(float).std(axis=2).mean(axis=2)
uniform_rows=(row_std<1.5).sum(axis=1)
blank=np.flatnonzero(uniform_rows>80)
report={'file':str(Path(args.video).resolve()),'frames':len(a),'adjacent_difference_mean':float(d.mean()),'unintended_large_jumps':len(bad),'large_jump_times':t[bad].round(4).tolist(),'blank_or_partial_frames':len(blank),'blank_frame_times':(blank/24).round(4).tolist(),'passed':len(bad)==0 and len(blank)==0}
if args.output:Path(args.output).write_text(json.dumps(report,ensure_ascii=False,indent=2))
print(json.dumps({k:v for k,v in report.items() if not k.endswith('times')},ensure_ascii=False,indent=2))
raise SystemExit(0 if report['passed'] else 1)
