"""Build a source-grounded, narration-ready graphical abstract package."""
from pathlib import Path
import subprocess,json,hashlib,shutil,textwrap,csv,sys
from PIL import Image,ImageDraw,ImageFont,ImageOps

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'output/jmp_video_clips';OUT.mkdir(parents=True,exist_ok=True)
FRAMES=OUT/'storyboard_frames';FRAMES.mkdir(exist_ok=True)
CLIPS=OUT/'scene_clips';CLIPS.mkdir(exist_ok=True)
FFMPEG='C:/ffmpeg/ffmpeg-9.0.1-essentials_build/bin/ffmpeg.exe'
FFPROBE='C:/ffmpeg/ffmpeg-9.0.1-essentials_build/bin/ffprobe.exe'
SOURCES=[
 ('Designer (3).png','Uploaded_Unified_Operator_Architecture.png'),
 ('Designer (4).png','Uploaded_Stability_Manifold.png'),
 ('Designer (5).png','Uploaded_Frenet_Serret_Error_Geometry.png'),
 ('Designer (6).png','Uploaded_Identity_Space_Structure.png'),
 ('Designer (7).png','Uploaded_Unified_Error_Vector.png'),
 ('Designer (8).png','Uploaded_Unified_Operator_Spectrum.png'),
 ('Designer (9).png','Uploaded_Photonic_Stability_Surface.png'),
 ('Designer (10).png','Uploaded_FRW_Cosmological_Extension.png')]
manifest=[]
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
for old,new in SOURCES:
    src=Path('C:/Users/jason/Downloads')/old;dst=OUT/new
    shutil.copy2(src,dst)
    manifest.append(dict(source=str(src),saved_as=new,sha256=digest(dst),original_preserved=True))
for name in ['Fig1_Stability_Surface','Fig2_Worldline_Geometry','Fig3_Error_Displacement','Fig4_Correction_Mapping','Fig5_Photonic_Implementation','Highlight']:
    src=ROOT/'output/unified-manuscript-figures'/(name+'.jpg');shutil.copy2(src,OUT/src.name)
    manifest.append(dict(source=str(src),saved_as=src.name,sha256=digest(src),original_preserved=True))

# Each chapter specifies the visible crop of each original. Originals stay intact.
scenes=[
 dict(duration=8,title='One proposed geometric framework',subtitle='Unified Geometric Field Theory from Worldline and Identity-Space Invariants',
      points=['Jason Duran Dutton','Worldline geometry','Identity-space invariants'],
      images=[('Highlight.jpg',None)],
      narration="I am Jason Duran Dutton. This manuscript proposes a framework connecting worldline geometry, identity-space structure, and dynamical invariants."),
 dict(duration=12,title='Three connected ingredients',subtitle='GWFM, SEFI and DEFI',
      points=['Geometry of a worldline','Four identity coordinates','Preservation along ideal evolution'],
      images=[('Uploaded_Unified_Operator_Architecture.png',None)],
      narration="The starting point is a proposed single continuous entity. The model combines its spacetime geometry with four identity coordinates and invariants preserved during ideal evolution."),
 dict(duration=12,title='Worldline geometry',subtitle='Tangent, normal and binormal directions',
      points=['Curvature and torsion','Local geometric frame','Projection shown schematically'],
      images=[('Fig2_Worldline_Geometry.jpg',(210,430,1680,1570)),('Uploaded_Frenet_Serret_Error_Geometry.png',(25,120,1080,780))],
      narration="A local geometric frame describes worldline curvature and torsion. These diagrams show conceptual relationships, not calculated particle trajectories or experimentally measured paths."),
 dict(duration=12,title='Identity-space structure',subtitle='Origin, Authorship, Sovereignty and Warp Expression',
      points=['Four model coordinates','Internal identity space','Geometric displacement components'],
      images=[('Uploaded_Identity_Space_Structure.png',(30,120,1030,940))],
      narration="Origin, Authorship, Sovereignty, and Warp Expression form the proposed identity coordinates. Their physical interpretation and measurement require further specification. The diagram projects a four-dimensional construction."),
 dict(duration=16,title='The proposed unified operator',subtitle='Spacetime term + identity-space term + three potentials',
      points=['Geometric potential','Identity potential','Dynamical potential'],
      images=[('Uploaded_Unified_Operator_Architecture.png',(555,100,1020,830)),('Highlight.jpg',(110,845,2890,1195))],
      narration="The unified operator combines spacetime and identity-space derivatives with three potentials. Its mathematical properties depend on the metrics, coefficients, domain, and boundary conditions. The expression defines a proposed model; physical validity requires further tests."),
 dict(duration=12,title='Candidate modes, not identified particles',subtitle='The eigenvalue problem organizes possible model excitations',
      points=['Eigenmode equation','Spectrum depends on assumptions','Mass, charge and spin require comparison'],
      images=[('Uploaded_Unified_Operator_Spectrum.png',(205,115,1310,465))],
      narration="The eigenvalue problem describes candidate excitations. These mode sketches are illustrative. Identifying a mode with an observed particle requires comparison with measured properties."),
 dict(duration=14,title='The proposed stability manifold',subtitle='A common locus of geometric and identity constraints',
      points=['Constant geometric invariants','Specified identity values','Ideal dynamical conditions'],
      images=[('Fig1_Stability_Surface.jpg',(170,350,1700,1635)),('Uploaded_Stability_Manifold.png',(30,430,1135,945))],
      narration="A proposed stability manifold collects ideal geometric, identity, and dynamical conditions. Preserving these conditions organizes the framework. This schematic does not prove that nearby disturbances decay."),
 dict(duration=12,title='Describe departures explicitly',subtitle='Geometric, identity and dynamical error components',
      points=['Displacement from the reference locus','Normal and binormal components','Identity-coordinate deviations'],
      images=[('Fig3_Error_Displacement.jpg',(165,420,1660,1590)),('Uploaded_Unified_Error_Vector.png',(20,120,1115,475))],
      narration="The error description combines geometric, identity, and dynamical departures. Displacement points away from a projected reference state, separating the definition of an error from its correction."),
 dict(duration=12,title='Correction as a proposed projection',subtitle='A mathematical target, not a demonstrated control device',
      points=['Map back to the proposed locus','Projection needs suitable assumptions','A physical recovery mechanism is separate'],
      images=[('Fig4_Correction_Mapping.jpg',(165,420,1660,1590))],
      narration="Correction is proposed as projection onto the stability manifold, where that projection is well defined. It specifies a target; a physical recovery process must be established separately."),
 dict(duration=16,title='Photonic application',subtitle='Selected deviations form a proposed syndrome vector',
      points=['Geometric and spectral deviations','Polarization-angle deviation','Measurement and correction need validation'],
      images=[('Uploaded_Photonic_Stability_Surface.png',(240,130,1500,755)),('Fig5_Photonic_Implementation.jpg',(100,1010,1610,1460))],
      narration="For photons, the proposed syndrome uses curvature, torsion, frequency, and polarization deviations. Weak or quantum-nondemolition sampling is discussed conceptually. No detector, decoder, lost-photon recovery, or error-correction advantage is demonstrated by these figures."),
 dict(duration=12,title='A cosmological extension',subtitle='Exploration in a Friedmann-Robertson-Walker background',
      points=['Cosmic scale factor','Time-dependent background','Additional spectral assumptions required'],
      images=[('Uploaded_FRW_Cosmological_Extension.png',(30,245,1140,755))],
      narration="An expanding cosmological background extends the framework. These slices are schematic. Scaling of spatial derivative terms alone does not establish the full spectrum or explain inflation."),
 dict(duration=12,title='A proposal for mathematical evaluation',subtitle='From defined structures to independently testable predictions',
      points=['Specify domains and dynamics','Calculate discriminating predictions','Compare with established theory and data'],
      images=[('Highlight.jpg',None)],
      narration="The contribution is a proposed mathematical organization. Precise operator analysis, specified dynamics, and discriminating predictions are essential next tests. Identification with observed matter and experimental advantages remain open.")
]
assert sum(s['duration'] for s in scenes)==150
W,H=1920,1080;INK='#162332';TEAL='#176779';MUTED='#475766'
def font(size,bold=False):return ImageFont.truetype('C:/Windows/Fonts/'+('arialbd.ttf' if bold else 'arial.ttf'),size)
def wrap_pixels(draw,text,f,maxwidth):
    lines=[];row=''
    for word in text.split():
        candidate=(row+' '+word).strip()
        if row and draw.textlength(candidate,font=f)>maxwidth:lines.append(row);row=word
        else:row=candidate
    if row:lines.append(row)
    return lines
def frame(index,scene,asset,crop):
    im=Image.new('RGB',(W,H),'white');d=ImageDraw.Draw(im)
    d.rectangle((0,0,W,12),fill=TEAL)
    d.text((64,42),'GRAPHICAL ABSTRACT | PROPOSED GEOMETRIC FRAMEWORK',font=font(22,True),fill=TEAL)
    d.text((1750,42),f'{index+1:02d} / 12',font=font(22),fill=MUTED)
    y=95
    for row in wrap_pixels(d,scene['title'],font(48,True),1760):d.text((64,y),row,font=font(48,True),fill=INK);y+=57
    for row in wrap_pixels(d,scene['subtitle'],font(26),1760):d.text((64,y+7),row,font=font(26),fill=MUTED);y+=32
    d.line((64,220,1856,220),fill='#c6d0d8',width=2)
    box=(64,248,1230,894);d.rounded_rectangle(box,radius=10,fill='#fafcfd',outline='#dce4e9',width=2)
    art=Image.open(OUT/asset).convert('RGB')
    if crop:art=art.crop(crop)
    art=ImageOps.contain(art,(1122,606),Image.Resampling.LANCZOS)
    im.paste(art,(647-art.width//2,571-art.height//2))
    yy=300
    for k,point in enumerate(scene['points']):
        d.rounded_rectangle((1295,yy+8,1305,yy+36),radius=4,fill=['#2a6d94','#b45b23','#638348'][k])
        for row in wrap_pixels(d,point,font(34,True),485):d.text((1330,yy),row,font=font(34,True),fill=INK);yy+=43
        yy+=57
    d.text((1295,820),'JASON DURAN DUTTON',font=font(22,True),fill=TEAL)
    d.text((64,915),'Schematics illustrate the manuscript proposal; they are not experimental results.',font=font(22),fill=MUTED)
    d.line((64,948,1856,948),fill='#c6d0d8',width=2)
    return im

def stamp(t,sep=','):
    ms=round(t*1000);h=ms//3600000;ms%=3600000;m=ms//60000;ms%=60000;s=ms//1000;ms%=1000
    return f'{h:02}:{m:02}:{s:02}{sep}{ms:03}'
def assstamp(t):
    cs=round(t*100);h=cs//360000;cs%=360000;m=cs//6000;cs%=6000;s=cs//100;cs%=100
    return f'{h}:{m:02}:{s:02}.{cs:02}'
story=[];srt=[];ass=[];transcript=[];cues=[];subnum=0;start=0
for i,s in enumerate(scenes):
    end=start+s['duration'];transcript.append(s['narration'])
    cues.append(f"{stamp(start,'.')} - {stamp(end,'.')} | {s['title']}\n{s['narration']}\n")
    words=s['narration'].split();groups=[words[j:j+15] for j in range(0,len(words),15)]
    consumed=0
    for group in groups:
        a=start+s['duration']*consumed/len(words);consumed+=len(group);b=start+s['duration']*consumed/len(words)
        subnum+=1;caption=' '.join(group);wrapped='\n'.join(textwrap.wrap(caption,96))
        srt.append(f'{subnum}\n{stamp(a)} --> {stamp(b)}\n{wrapped}\n')
        ass.append('Dialogue: 0,'+assstamp(a)+','+assstamp(b)+',Default,,0,0,0,,'+wrapped.replace('\n','\\N'))
    for j,(asset,crop) in enumerate(s['images']):
        duration=s['duration']/len(s['images']);name=f'{i+1:02d}_{j+1:02d}'
        frame(i,s,asset,crop).save(FRAMES/(name+'.png'))
        story.append(dict(chapter=i+1,title=s['title'],start=start+j*duration,duration=duration,frame=f'storyboard_frames/{name}.png',clip=f'scene_clips/{name}.mp4',asset=asset,crop=crop,narration=s['narration']))
    start=end

(OUT/'Voiceover_Script_Timed.txt').write_text('AUTHOR VOICE-OVER | 150 seconds\n\nSpeak naturally, approximately 125-135 words per minute, allowing the chapter pauses. Follow the timestamps; do not read headings aloud. Record in a quiet room with a consistent microphone distance. The supplied video has no recorded narration. Do not read equations symbol by symbol; follow this spoken explanation.\n\n'+'\n'.join(cues),encoding='utf-8')
(OUT/'Voiceover_Transcript.txt').write_text('\n\n'.join(transcript)+'\n',encoding='utf-8')
(OUT/'Graphical_Abstract_Captions.srt').write_text('\n'.join(srt),encoding='utf-8')
assheader='''[Script Info]
ScriptType: v4.00+
PlayResX: 1920
PlayResY: 1080
WrapStyle: 0
[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Arial,30,&H00322316,&H00322316,&H00FFFFFF,&H00FFFFFF,0,0,0,0,100,100,0,0,3,1,0,2,75,75,36,1
[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
'''
(OUT/'Graphical_Abstract_Captions.ass').write_text(assheader+'\n'.join(ass)+'\n',encoding='utf-8')
(OUT/'Storyboard.json').write_text(json.dumps(story,indent=2)+'\n',encoding='utf-8')
(OUT/'Asset_Manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
with (OUT/'Storyboard.csv').open('w',newline='',encoding='utf-8') as f:
    w=csv.DictWriter(f,fieldnames=['chapter','title','start','duration','asset','crop']);w.writeheader();w.writerows({k:r[k] for k in w.fieldnames} for r in story)

if '--prepare-only' in sys.argv:
    print('Prepared script, captions, assets and frames; words:',sum(len(s['narration'].split()) for s in scenes),flush=True)
    sys.exit(0)

def run(cmd,logname):
    with (OUT/logname).open('w',encoding='utf-8') as log:
        subprocess.run(cmd,stdout=log,stderr=subprocess.STDOUT,check=True,cwd=OUT)

for n,r in enumerate(story):
    duration=r['duration'];vf=f'fade=t=in:st=0:d=0.3:color=white,fade=t=out:st={duration-.3}:d=0.3:color=white'
    run([FFMPEG,'-hide_banner','-y','-loop','1','-framerate','30','-i',r['frame'],'-t',str(duration),'-vf',vf,'-c:v','libx264','-preset','fast','-crf','20','-threads','2','-pix_fmt','yuv420p','-an',r['clip']],f'encode_scene_{n+1:02d}.log')
    print(f"Encoded {n+1}/{len(story)}: {r['title']}",flush=True)
(OUT/'concat.txt').write_text(''.join("file '"+r['clip']+"'\n" for r in story),encoding='utf-8')
run([FFMPEG,'-hide_banner','-y','-f','concat','-safe','0','-i','concat.txt','-c','copy','-movflags','+faststart','JMP_Graphical_Abstract_Clean_1080p.mp4'],'encode_clean.log')
run([FFMPEG,'-hide_banner','-y','-i','JMP_Graphical_Abstract_Clean_1080p.mp4','-vf','ass=Graphical_Abstract_Captions.ass','-c:v','libx264','-preset','slow','-crf','20','-threads','2','-pix_fmt','yuv420p','-an','-movflags','+faststart','JMP_Graphical_Abstract_Captioned_1080p.mp4'],'encode_captioned.log')
# Rate-controlled upload derivative reserves room for the user's later AAC voice track.
run([FFMPEG,'-hide_banner','-y','-i','JMP_Graphical_Abstract_Captioned_1080p.mp4','-c:v','libx264','-preset','slow','-b:v','330k','-maxrate','360k','-bufsize','720k','-threads','2','-pix_fmt','yuv420p','-an','-movflags','+faststart','JMP_Graphical_Abstract_Upload.mp4'],'encode_upload.log')
shutil.copy2(FRAMES/'01_01.png',OUT/'Representative_Still.png')
report={}
for name in ['JMP_Graphical_Abstract_Clean_1080p.mp4','JMP_Graphical_Abstract_Captioned_1080p.mp4','JMP_Graphical_Abstract_Upload.mp4']:
    data=json.loads(subprocess.check_output([FFPROBE,'-v','error','-show_streams','-show_format','-of','json',str(OUT/name)],text=True));v=next(s for s in data['streams'] if s['codec_type']=='video')
    assert v['codec_name']=='h264' and v['pix_fmt']=='yuv420p' and v['width']==1920 and v['height']==1080
    assert abs(float(data['format']['duration'])-150)<.1
    report[name]=dict(bytes=(OUT/name).stat().st_size,duration=float(data['format']['duration']),codec=v['codec_name'],pixel_format=v['pix_fmt'],width=v['width'],height=v['height'],frame_rate=v['r_frame_rate'],has_recorded_narration=False)
assert report['JMP_Graphical_Abstract_Upload.mp4']['bytes']<10_000_000
report['script_word_count']=sum(len(s['narration'].split()) for s in scenes)
report['narration_words_per_minute']=report['script_word_count']/2.5
report['original_images_sha256_checked']=True
(OUT/'VIDEO_VERIFICATION.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print(json.dumps(report,indent=2),flush=True)
