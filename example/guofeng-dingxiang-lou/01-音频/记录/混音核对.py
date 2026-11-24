from pathlib import Path
import json,subprocess,sys
import numpy as np,soundfile as sf,torch,torchaudio
ROOT=Path(__file__).resolve().parents[2];TASK=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'models/Seed-VC/source/seed-vc-main'))
from modules.campplus.DTDNN import CAMPPlus
torch.set_num_threads(4)
m=CAMPPlus(feat_dim=80,embedding_size=192);m.load_state_dict(torch.load(ROOT/'models/Seed-VC/campplus/campplus_cn_common.bin',map_location='cpu'));m.eval()
@torch.inference_mode()
def emb(p):
 w,s=torchaudio.load(str(p));w=torchaudio.functional.resample(w.mean(0,keepdim=True),s,16000)
 f=torchaudio.compliance.kaldi.fbank(w,num_mel_bins=80,dither=0,sample_frequency=16000);f-=f.mean(0,keepdim=True)
 return torch.nn.functional.normalize(m(f[None]).squeeze(),dim=0)
refs={'贾队长长参考':emb(ROOT/'reference_audio/贾队长-单人长参考音频.wav'),'隐形的翅膀':emb(next((ROOT/'generated_audio/贾队长-隐形的翅膀/converted').glob('*.wav'))),'赵本山原人声':emb(TASK/'work/赵本山-副歌人声.wav')}
params=json.loads((TASK/'work/生成参数.json').read_text())
report={};outputs=[]
for variant,shift in params['variants'].items():
 files=list((TASK/'work'/variant).glob('vc_*.wav'))
 if not files:continue
 src=files[0];label='原调版' if variant=='原调转换' else '角色声区版'
 vocal=TASK/f'贾队长-慌啥子嘛-赵本山底版-{label}-清唱.wav'
 subprocess.run(['ffmpeg','-v','error','-y','-i',str(src),'-af','apad,atrim=duration=31.8,highpass=f=70,afade=t=in:d=0.03,afade=t=out:st=31.55:d=0.25,loudnorm=I=-17:TP=-2:LRA=9','-ar','44100','-ac','1',str(vocal)],check=True)
 accomp=TASK/'work/赵本山-副歌伴奏.wav'
 if shift:
  out=TASK/'work'/f'伴奏{shift:+d}半音.wav'
  subprocess.run(['ffmpeg','-v','error','-y','-i',str(accomp),'-af',f'rubberband=pitch={2**(shift/12):.9f}',str(out)],check=True);accomp=out
 mix=TASK/f'贾队长-慌啥子嘛-赵本山底版-{label}-伴奏版.wav'
 subprocess.run(['ffmpeg','-v','error','-y','-i',str(vocal),'-i',str(accomp),'-filter_complex','[1:a]volume=0.72[b];[0:a][b]amix=inputs=2:duration=first:normalize=0,loudnorm=I=-16:TP=-1.5:LRA=9,afade=t=out:st=31.55:d=0.25[out]','-map','[out]','-ar','44100',str(mix)],check=True)
 subprocess.run(['ffmpeg','-v','error','-y','-i',str(mix),'-codec:a','libmp3lame','-b:a','192k',str(mix.with_suffix('.mp3'))],check=True)
 e=emb(vocal);report[label]={'semitones':shift,'similarity':{k:round(torch.dot(e,v).item(),4) for k,v in refs.items()}}
 for p in [vocal,mix]:
  w,s=sf.read(p);assert np.isfinite(w).all();assert len(w)/s>=31.79;assert np.max(abs(w))<1
  report[label][p.stem]={'duration':len(w)/s,'peak':float(np.max(abs(w))),'rms':float(np.sqrt(np.mean(w*w)))}
 outputs.append((label,vocal))
# Short comparison uses the same opening lyric in each new variant.
clips=[]
old=ROOT/'generated_audio/贾队长-慌啥子嘛-音色加强/贾队长-慌啥子嘛-重唱清唱.wav'
for p in [old]+[p for _,p in outputs]:
 w,s=sf.read(p);w=w[:s*8]
 w=w*(0.12/max(1e-6,np.sqrt(np.mean(w*w))));w=np.clip(w,-.98,.98)
 clips.extend([w,np.zeros(int(s*.65))])
sf.write(TASK/'清唱对比-旧加强版-新原调-新角色声区.wav',np.concatenate(clips),s)
(TASK/'work/核对结果.json').write_text(json.dumps(report,ensure_ascii=False,indent=2));print(json.dumps(report,ensure_ascii=False,indent=2))
