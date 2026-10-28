from pathlib import Path
import argparse,subprocess,shutil,json,math
import numpy as np
from PIL import Image,ImageDraw,ImageFont

p=argparse.ArgumentParser();p.add_argument('--output',required=True);p.add_argument('--figures',required=True);p.add_argument('--audio',required=True);p.add_argument('--transcript',required=True);a=p.parse_args()
out=Path(a.output);out.mkdir(parents=True,exist_ok=True);figures=Path(a.figures)
# Reuse the reviewed visual renderer, without running its encoder.
source=(Path(__file__).parent/'create_graphical_abstract_video.py').read_text(encoding='utf8')
exec(source[source.index('W,H='):source.index("ff=shutil.which")],globals())
original_scenes=list(scenes)
audio_root=Path(a.audio);transcripts=json.loads(Path(a.transcript).read_text(encoding='utf8'))
rate=48000;gap=.18;intro=.6;outro=1.0
parts=[np.zeros(round(rate*intro),dtype=np.float32)];cursor=intro;clips=[];mapping=[0,1,1,2,2,3,3,4,5,5]
for i in range(1,11):
    raw=subprocess.check_output(['ffmpeg','-v','error','-i',str(audio_root/f'{i}.wav'),'-ar',str(rate),'-ac','1','-f','f32le','-'])
    samples=np.frombuffer(raw,dtype=np.float32).copy();entry=transcripts[i-1]
    # Retain all leading audio; remove only trailing material beyond the last
    # recognized word plus a generous half-second margin. Never alter speech speed.
    last=max((s['end'] for s in entry['segments']),default=len(samples)/rate)
    kept_end=min(len(samples)/rate,last+.5);samples=samples[:math.ceil(kept_end*rate)]
    fade=min(480,len(samples)//2);samples[:fade]*=np.linspace(0,1,fade);samples[-fade:]*=np.linspace(1,0,fade)
    duration=len(samples)/rate
    clips.append({'file':f'{i}.wav','scene':mapping[i-1]+1,'start':cursor,'end':cursor+duration,'original_duration':len(raw)/4/rate,'retained_duration':duration,'trim_start':0})
    parts.append(samples);cursor+=duration
    if i<10:parts.append(np.zeros(round(rate*gap),dtype=np.float32));cursor+=gap
parts.append(np.zeros(round(rate*outro),dtype=np.float32));cursor+=outro
audio=np.concatenate(parts);peak=float(np.max(np.abs(audio)));target=10**(-1/20);gain=min(1,target/max(peak,1e-12));audio*=gain
master=out/'narration_master.wav'
subprocess.run(['ffmpeg','-y','-v','error','-f','f32le','-ar',str(rate),'-ac','1','-i','-','-c:a','pcm_s24le',str(master)],input=audio.tobytes(),check=True)
scenes=[]
for idx,old in enumerate(original_scenes):
    matching=[c for c in clips if c['scene']==idx+1]
    start=0 if idx==0 else matching[0]['start']-.09
    end=cursor if idx==5 else [c for c in clips if c['scene']==idx+2][0]['start']-.09
    scenes.append((start,end,*old[2:]))
DURATION=cursor;FPS=15
# Speech-aligned soft subtitles, split into brief phrases using word timestamps.
def stamp(v):
    ms=max(0,round(v*1000));return f'{ms//3600000:02}:{ms//60000%60:02}:{ms//1000%60:02},{ms%1000:03}'
subs=[];n=0
for clip,entry in zip(clips,transcripts):
    words=[w for s in entry['segments'] for w in s['words']]
    for j in range(0,len(words),9):
        chunk=words[j:j+9];n+=1
        text=''.join(w['word'] for w in chunk).strip()
        subs.extend([str(n),f"{stamp(clip['start']+chunk[0]['start'])} --> {stamp(min(clip['end'],clip['start']+chunk[-1]['end']+.08))}",text,''])
srt=out/'narration_subtitles.srt';srt.write_text('\n'.join(subs),encoding='utf8')
(out/'edit_timeline.json').write_text(json.dumps({'duration':cursor,'sample_rate':rate,'gain_db':20*math.log10(gain),'source_peak_dbfs':20*math.log10(max(peak,1e-12)),'clips':clips,'scenes':[{'start':s[0],'end':s[1],'title':s[2]} for s in scenes]},indent=2),encoding='utf8')
shutil.copy2(a.transcript,out/'automatic_transcript.json')
# Correct the original renderer's fixed duration display to this edit's runtime.
old_render=render
def render(t):
    frame=old_render(t);d=ImageDraw.Draw(frame);d.rectangle((1035,681,1280,714),fill='#f5f8fb')
    total=math.ceil(DURATION);d.text((1052,688),f'{int(t)//60:02}:{int(t)%60:02} / {total//60:02}:{total%60:02}',font=font(13),fill='#526779');return frame
temp=out/'visual_track.mp4'
ff=shutil.which('ffmpeg')
proc=subprocess.Popen([ff,'-y','-v','error','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-','-an','-c:v','libx264','-preset','fast','-crf','20','-pix_fmt','yuv420p',str(temp)],stdin=subprocess.PIPE)
for i in range(math.ceil(DURATION*FPS)):proc.stdin.write(render(i/FPS).tobytes())
proc.stdin.close();assert proc.wait()==0
final=out/'graphical_abstract_narrated.mp4'
subprocess.run([ff,'-y','-v','error','-i',str(temp),'-i',str(master),'-i',str(srt),'-map','0:v:0','-map','1:a:0','-map','2:s:0','-c:v','copy','-c:a','aac','-b:a','256k','-c:s','mov_text','-metadata:s:s:0','language=eng','-t',str(DURATION),'-movflags','+faststart',str(final)],check=True)
thumb=Image.new('RGB',(1280,1080),'white')
for idx,s in enumerate(scenes):
    im=render(s[0]+min(2,(s[1]-s[0])/2));im.thumbnail((640,360));thumb.paste(im,((idx%2)*640,(idx//2)*360))
thumb.save(out/'narrated_storyboard.png');render(3).save(out/'video_poster.png')
temp.unlink()
(out/'README.md').write_text(f'# Narrated graphical abstract\n\nFinal duration: {DURATION:.3f} seconds. All ten supplied recordings are used once in numeric order. Speech is not time-stretched. Processing: ten millisecond boundary fades, at most trailing silence trimming after the recognized speech plus half a second, short pauses between clips, and a single overall gain adjustment of {20*math.log10(gain):.2f} decibels to retain one decibel of peak headroom. No equalization, noise reduction, music, or dynamic compression was applied.\n\nThe master is a twenty-four-bit mono wave file at forty-eight thousand samples per second. The video contains compressed narration and optional English subtitles. Subtitles use automatic speech alignment and should be checked against the recording. Original studio files remain unchanged in the sibling audio folder and are not republished in this package.\n\nThe mathematical figures remain candidate illustrations with proposed parameters, not experimental validation. The original silent video is retained separately.\n',encoding='utf8')
print(json.dumps({'file':str(final),'duration':DURATION,'clips':len(clips),'gain_db':20*math.log10(gain)}),flush=True)
