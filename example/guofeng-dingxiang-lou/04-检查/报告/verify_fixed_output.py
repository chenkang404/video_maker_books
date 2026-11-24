from pathlib import Path
import subprocess,json,numpy as np
p=Path(__file__).resolve().parent
v=p.parent/'贾队长-慌啥子嘛-国风鼎香楼-修复闪烁版.mp4'
subprocess.run(['ffmpeg','-v','error','-i',str(v),'-f','null','-'],check=True)
probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(v)]))
vid=next(s for s in probe['streams'] if s['codec_type']=='video')
assert (vid['width'],vid['height'],vid['r_frame_rate'])==(1080,1920,'24/1')
def samples(path):
 b=subprocess.check_output(['ffmpeg','-v','error','-i',str(path),'-f','f32le','-ac','2','-ar','44100','-'])
 return np.frombuffer(b,np.float32)
x=samples(v);y=samples(p/'assets/song.wav');n=min(len(x),len(y));corr=float(np.corrcoef(x[:n],y[:n])[0,1]);assert corr>.99
pause=float(np.sqrt(np.mean(x[int(4.05*88200):int(4.4*88200)]**2)));assert pause<.0001
result={'full_decode':'passed','width':vid['width'],'height':vid['height'],'fps':vid['r_frame_rate'],'duration':float(probe['format']['duration']),'audio_correlation_with_source':corr,'pause_rms':pause}
(p/'fixed-output-verification.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
