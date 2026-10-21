from pathlib import Path
import hashlib,json,subprocess,shutil,re
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'output/jmp_video_clips_verified'
DEST=Path('V:/V Drive and GitHub Content/Journal Submissions/Defining SEFI/jmp_video_clips')
FF='C:/ffmpeg/ffmpeg-9.0.1-essentials_build/bin/ffmpeg.exe'
PROBE='C:/ffmpeg/ffmpeg-9.0.1-essentials_build/bin/ffprobe.exe'
qa=OUT/'quality_review';qa.mkdir(exist_ok=True)
def run(args,log):
    with (qa/log).open('w',encoding='utf-8') as f:subprocess.run(args,check=True,stdout=f,stderr=subprocess.STDOUT)
movies=['JMP_Graphical_Abstract_Clean_1080p.mp4','JMP_Graphical_Abstract_Captioned_1080p.mp4','JMP_Graphical_Abstract_Upload.mp4']
for name in movies:
    run([FF,'-hide_banner','-v','error','-threads','2','-i',str(OUT/name),'-f','null','-'],name+'.decode.log')
    assert not (qa/(name+'.decode.log')).read_text().strip(),name
for i,t in enumerate([3,14,26,38,52,66,79,95,104,118,132,144]):
    run([FF,'-hide_banner','-loglevel','error','-y','-ss',str(t),'-i',str(OUT/movies[1]),'-frames:v','1','-q:v','2',str(qa/f'chapter_{i+1:02d}.jpg')],f'extract_{i+1:02d}.log')
shots=sorted(qa.glob('chapter_*.jpg'));sheet=Image.new('RGB',(1440,1200),'#e4e9ed');d=ImageDraw.Draw(sheet)
for i,p in enumerate(shots):
    sheet.paste(Image.open(p).resize((480,270)),((i%3)*480,(i//3)*300));d.text(((i%3)*480+12,(i//3)*300+275),p.stem,fill='black')
sheet.save(qa/'Encoded_Video_Contact_Sheet.jpg')
shutil.copy2(qa/'chapter_01.jpg',OUT/'Representative_Still.jpg')
story=json.loads((OUT/'Storyboard.json').read_text());assert all('Uploaded_' not in r['asset'] and 'reference_only' not in r['asset'] for r in story)
assert len({r['asset'] for r in story})==11
for asset in {r['asset'] for r in story}:assert (OUT/asset).exists()
captions=(OUT/'Graphical_Abstract_Captions.srt').read_text(encoding='utf-8')
def seconds(s):
    h,m,rest=s.split(':');return int(h)*3600+int(m)*60+float(rest.replace(',','.'))
times=[(seconds(a),seconds(b)) for a,b in re.findall(r'(\d\d:\d\d:\d\d,\d\d\d) --> (\d\d:\d\d:\d\d,\d\d\d)',captions)]
assert times and all(0<=a<b<=150.001 for a,b in times)
assert all(times[i][1]<=times[i+1][0]+.001 for i in range(len(times)-1))
records=json.loads((OUT/'Asset_Manifest.json').read_text())
for r in records:assert hashlib.sha256((OUT/r['saved_as']).read_bytes()).hexdigest()==r['sha256']
report=json.loads((OUT/'VIDEO_VERIFICATION.json').read_text())
words=len((OUT/'Voiceover_Transcript.txt').read_text(encoding='utf-8').split());assert words==report['script_word_count']
assert report['JMP_Graphical_Abstract_Upload.mp4']['bytes']<10_000_000
source=Path('V:/V Drive and GitHub Content/Journal Submissions/Defining SEFI/unifiying.tex')
result=dict(duration_seconds=150,chapters=12,views=len(story),checked_video_assets=11,original_designer_assets_used=0,
    original_uploads_preserved=8,script_word_count=words,caption_timing_checked=True,full_decode_passed=movies,
    manuscript_source=str(source),manuscript_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
    recorded_author_audio_present=False,editorial_scope='Illustrations of the manuscript proposal; no computed spectrum or experimental validation implied.',
    visual_review='Awaiting review of encoded contact sheet and representative full-size frames before final delivery.')
(OUT/'FINAL_QA.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
print(json.dumps(result,indent=2),flush=True)
# Copy is performed separately after visual review.
