from pathlib import Path
import os,sys,json,argparse,random
ROOT=Path(__file__).resolve().parents[2]
TASK=Path(__file__).resolve().parent
MODEL=ROOT/'models/Seed-VC'
os.environ['CUDA_VISIBLE_DEVICES']='1'
os.environ['SEED_VC_RMVPE_PATH']=str(MODEL/'rmvpe/rmvpe.pt')
os.environ['SEED_VC_CAMPPLUS_PATH']=str(MODEL/'campplus/campplus_cn_common.bin')
os.environ['SEED_VC_BIGVGAN_DIR']=str(MODEL/'bigvgan')
os.environ['SEED_VC_WHISPER_DIR']=str(MODEL/'whisper-small')
os.environ['HF_HUB_OFFLINE']='1'
sys.path.append(str(MODEL/'venv/lib/python3.10/site-packages'))
sys.path.insert(0,str(MODEL/'source/seed-vc-main'))
os.chdir(MODEL/'source/seed-vc-main')
import torch,numpy as np,librosa
import inference as vc
torch.set_num_threads(4)
a=argparse.Namespace(source=str(TASK/'work/赵本山-副歌人声.wav'),target=str(ROOT/'reference_audio/贾队长-单人长参考音频.wav'),output=str(TASK/'work/原调转换'),diffusion_steps=20,length_adjust=1.0,inference_cfg_rate=0.8,f0_condition=True,auto_f0_adjust=False,semi_tone_shift=0,checkpoint=str(MODEL/'core/DiT_seed_v2_uvit_whisper_base_f0_44k_bigvgan_pruned_ft_ema_v2.pth'),config=str(MODEL/'core/config_dit_mel_seed_uvit_whisper_base_f0_44k.yml'),fp16=True)
models=vc.load_models(a)
vc.load_models=lambda _:models
pitch={}
for name,p in [('贾队长参考',a.target),('赵本山副歌',a.source),('隐形的翅膀',next((ROOT/'generated_audio/贾队长-隐形的翅膀/converted').glob('*.wav')))]:
 y=librosa.load(str(p),sr=16000)[0]
 f=models[2](torch.tensor(y,device='cuda'),thred=0.03)
 v=f[f>65]
 pitch[name]={'median_hz':float(np.median(v)),'p10':float(np.percentile(v,10)),'p90':float(np.percentile(v,90))}
print('PITCH',json.dumps(pitch,ensure_ascii=False),flush=True)
(TASK/'work/音高分析.json').write_text(json.dumps(pitch,ensure_ascii=False,indent=2))
for name,shift in [('原调转换',0),('角色声区转换',round(12*np.log2(pitch['隐形的翅膀']['median_hz']/pitch['赵本山副歌']['median_hz'])))]:
 shift=max(-5,min(5,shift))
 if name=='角色声区转换' and shift==0:continue
 a.output=str(TASK/'work'/name);a.semi_tone_shift=shift
 Path(a.output).mkdir(exist_ok=True)
 random.seed(20261118);np.random.seed(20261118);torch.manual_seed(20261118);torch.cuda.manual_seed_all(20261118)
 print('GENERATING',name,'pitch_shift',shift,flush=True)
 vc.main(a)
(TASK/'work/生成参数.json').write_text(json.dumps({'source_start':63.8,'duration':31.8,'reference':a.target,'steps':20,'cfg':0.8,'f0':True,'auto_f0_adjust':False,'variants':{'原调转换':0,'角色声区转换':a.semi_tone_shift},'seed':20261118},ensure_ascii=False,indent=2))
