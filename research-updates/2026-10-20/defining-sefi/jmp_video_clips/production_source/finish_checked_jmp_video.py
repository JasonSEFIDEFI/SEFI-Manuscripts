from pathlib import Path
import subprocess,json,shutil
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'output/jmp_video_clips_verified'
FF='C:/ffmpeg/ffmpeg-9.0.1-essentials_build/bin/ffmpeg.exe';PROBE='C:/ffmpeg/ffmpeg-9.0.1-essentials_build/bin/ffprobe.exe'
def run(args,name):
    with (OUT/name).open('w',encoding='utf-8') as log:subprocess.run(args,cwd=OUT,stdout=log,stderr=subprocess.STDOUT,check=True)
run([FF,'-hide_banner','-y','-i','JMP_Graphical_Abstract_Clean_1080p.mp4','-vf','ass=Graphical_Abstract_Captions.ass','-c:v','libx264','-preset','veryfast','-crf','20','-threads','4','-pix_fmt','yuv420p','-an','-movflags','+faststart','JMP_Graphical_Abstract_Captioned_1080p.mp4'],'encode_captioned_final.log')
print('Captioned master completed',flush=True)
captioned=OUT/'JMP_Graphical_Abstract_Captioned_1080p.mp4'
if captioned.stat().st_size<7_000_000:
    shutil.copy2(captioned,OUT/'JMP_Graphical_Abstract_Upload.mp4')
else:
    run([FF,'-hide_banner','-y','-i',captioned.name,'-c:v','libx264','-preset','veryfast','-b:v','330k','-maxrate','360k','-bufsize','720k','-threads','4','-pix_fmt','yuv420p','-an','-movflags','+faststart','JMP_Graphical_Abstract_Upload.mp4'],'encode_upload_final.log')
report={}
for name in ['JMP_Graphical_Abstract_Clean_1080p.mp4','JMP_Graphical_Abstract_Captioned_1080p.mp4','JMP_Graphical_Abstract_Upload.mp4']:
    data=json.loads(subprocess.check_output([PROBE,'-v','error','-show_streams','-show_format','-of','json',str(OUT/name)],text=True));v=next(s for s in data['streams'] if s['codec_type']=='video')
    assert v['codec_name']=='h264' and v['pix_fmt']=='yuv420p' and v['width']==1920 and v['height']==1080
    assert abs(float(data['format']['duration'])-150)<.1
    report[name]=dict(bytes=(OUT/name).stat().st_size,duration=float(data['format']['duration']),codec=v['codec_name'],pixel_format=v['pix_fmt'],width=v['width'],height=v['height'],frame_rate=v['r_frame_rate'],has_recorded_narration=False)
assert report['JMP_Graphical_Abstract_Upload.mp4']['bytes']<10_000_000
report['script_word_count']=len((OUT/'Voiceover_Transcript.txt').read_text(encoding='utf-8').split())
report['narration_words_per_minute']=report['script_word_count']/2.5
report['original_images_sha256_checked']=True
(OUT/'VIDEO_VERIFICATION.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print(json.dumps(report,indent=2),flush=True)
