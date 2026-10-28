from pathlib import Path
import argparse, subprocess, shutil, json, math
import numpy as np
from PIL import Image, ImageDraw, ImageFont

p=argparse.ArgumentParser();p.add_argument('--output',required=True);p.add_argument('--figures',required=True);a=p.parse_args()
out=Path(a.output);out.mkdir(parents=True,exist_ok=True);figures=Path(a.figures)
W,H=1280,720;FPS=15;DURATION=100
fontpath='C:/Windows/Fonts/arial.ttf';boldpath='C:/Windows/Fonts/arialbd.ttf'
def font(size,bold=False):return ImageFont.truetype(boldpath if bold else fontpath,size)
scenes=[
 (0,14,'A geometric view of photonic errors','Proposed research framework', 'figure_01_stability_manifold.png',
 'My research explores a geometric interpretation of how photonic systems depart from an intended configuration, and how a mathematical model can describe their return.',
 'Conceptual model • not an experimental result'),
 (14,32,'Identity, geometry, and dynamics','Three proposed roles in one framework','figure_08_proposed_workflow.png',
 'The Single Entity Field Interpretation describes proposed identity constraints. The Geometric Worldline Field Model describes trajectory geometry. Dynamic Entity Field Integration proposes a connection between those constraints and their evolution.',
 'Identity constraints → trajectory geometry → proposed coupled dynamics'),
 (32,48,'Represent a deviation','Reference trajectory and perturbed trajectory','figure_05_projection_mapping.png',
 'In the illustrated example, a reference trajectory lies on a saddle shaped surface. A deliberately introduced vertical perturbation moves the trajectory away from that surface.',
 'Σ: z = 0.25x² − 0.25y²     |     γ(t) = γΣ(t) + (0, 0, 0.15 cos t)'),
 (48,66,'Apply the prescribed projection','A mathematical consistency demonstration','figure_10_validation_projection.png',
 'A prescribed vertical projection then returns the trajectory to the surface. The residual becomes zero by construction. This verifies the chosen mathematical operation, rather than demonstrating physical quantum error correction.',
 'Πᵥ(x, y, z) = (x, y, 0.25x² − 0.25y²)     |     rafter = 0'),
 (66,84,'Connect the model to physics','The next step requires measurable predictions','figure_04_vertical_displacement.png',
 'The next step is to connect these geometric quantities to measurable optical behavior, specify a physically allowed recovery operation, and test predictions against established methods and experimental evidence.',
 'Physical mapping → allowed recovery operation → independent comparison'),
 (84,100,'Make the work reviewable','Source code, figures, and numerical data','figure_09_validation_surface.png',
 'The deliverables include reproducible calculations, diagrams, numerical data, and research manuscripts. Together, they present a proposed direction for investigation, with assumptions and limitations stated openly.',
 'Jason Duran Dutton • Independent research • Candidate graphical abstract')]

def wrap(draw,text,ft,width):
    lines=[];line=''
    for word in text.split():
        trial=(line+' '+word).strip()
        if draw.textlength(trial,font=ft)>width and line:lines.append(line);line=word
        else:line=trial
    if line:lines.append(line)
    return lines
def stamp(seconds):
    return f'{int(seconds)//3600:02}:{int(seconds)//60%60:02}:{int(seconds)%60:02},000'

script=['# Graphical abstract recording script','','Title: Geometric Photonic Quantum Error Correction via the Single Entity Field Interpretation, the Geometric Worldline Field Model, and Dynamic Entity Field Integration','','Duration: one minute and forty seconds. The video is silent so you can record your own narration. Read only the prose under each recording passage; timing notes are production directions. All framework names are expanded. No mathematical notation is included in the spoken text.','']
srt=[]
for i,(start,end,title,subtitle,img,narration,caption) in enumerate(scenes,1):
    script.extend([f'## Recording passage {i}: {start}–{end} seconds','',narration,''])
    # Keep subtitle chunks short and synchronized to the recording passages.
    words=narration.split();chunks=[' '.join(words[j:j+12]) for j in range(0,len(words),12)]
    for j,chunk in enumerate(chunks):
        s=start+(end-start)*j/len(chunks);e=start+(end-start)*(j+1)/len(chunks)
        def ts(v):
            ms=round(v*1000);return f'{ms//3600000:02}:{ms//60000%60:02}:{ms//1000%60:02},{ms%1000:03}'
        srt.extend([str(len(srt)//4+1),f'{ts(s)} --> {ts(e)}',chunk,''])
(out/'recording_script.md').write_text('\n'.join(script),encoding='utf-8')
(out/'recording_script.txt').write_text('\n\n'.join(s[5] for s in scenes),encoding='utf-8')
(out/'narration_subtitles.srt').write_text('\n'.join(srt),encoding='utf-8')
(out/'storyboard.json').write_text(json.dumps([{'start':s[0],'end':s[1],'title':s[2],'narration':s[5],'caption':s[6]} for s in scenes],indent=2),encoding='utf-8')
spoken=' '.join(s[5] for s in scenes)
assert not any(x in spoken for x in ['SEFI','GWFM','DEFI','QEC','CSV','AIU','Π','Σ'])

images=[]
for s in scenes:
    im=Image.open(figures/s[4]).convert('RGB');im.thumbnail((1140,420),Image.Resampling.LANCZOS);images.append(im)

def render(t):
    idx=next((i for i,s in enumerate(scenes) if s[0]<=t<s[1]),len(scenes)-1)
    start,end,title,subtitle,img,narration,caption=scenes[idx];progress=(t-start)/(end-start)
    frame=Image.new('RGB',(W,H),'#f5f8fb');d=ImageDraw.Draw(frame)
    d.rectangle((0,0,W,132),fill='#102b43')
    d.text((42,21),title,font=font(34,True),fill='white')
    d.text((44,77),subtitle,font=font(22),fill='#b9d9ed')
    # Center source figure inside a white panel, with a small scene-entry fade.
    d.rounded_rectangle((30,146,1250,586),radius=14,fill='white',outline='#dce4ec',width=1)
    im=images[idx];x=(W-im.width)//2;y=154+(420-im.height)//2
    fade=min(1,max(0,(t-start)/.6))
    if fade<1:im=Image.blend(Image.new('RGB',im.size,'white'),im,fade)
    frame.paste(im,(x,y));d=ImageDraw.Draw(frame)
    # Animated progression beneath the artwork, independent of the plotted data.
    d.rounded_rectangle((48,601,1232,608),radius=3,fill='#dce4ec')
    d.rounded_rectangle((48,601,48+max(3,int(1184*progress)),608),radius=3,fill='#0072b2')
    lines=wrap(d,caption,font(20),1180)
    for j,line in enumerate(lines):d.text(((W-d.textlength(line,font=font(20)))/2,620+j*25),line,font=font(20),fill='#233c52')
    d.text((42,688),f'PROPOSED RESEARCH  •  {idx+1} / {len(scenes)}',font=font(13,True),fill='#526779')
    d.text((1060,688),f'{int(t)//60:02}:{int(t)%60:02} / 01:40',font=font(13),fill='#526779')
    # Whole-video progress line.
    d.rectangle((0,716,int(W*t/DURATION),719),fill='#009e73')
    return frame

ff=shutil.which('ffmpeg');assert ff
cmd=[ff,'-y','-loglevel','error','-f','rawvideo','-vcodec','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-','-an','-c:v','libx264','-preset','fast','-crf','20','-pix_fmt','yuv420p','-movflags','+faststart',str(out/'graphical_abstract_recording_video.mp4')]
proc=subprocess.Popen(cmd,stdin=subprocess.PIPE)
for frame_no in range(DURATION*FPS):proc.stdin.write(render(frame_no/FPS).tobytes())
proc.stdin.close();assert proc.wait()==0
render(5).save(out/'video_poster.png')
thumb=Image.new('RGB',(1280,1080),'white')
for i,s in enumerate(scenes):
    frame=render(s[0]+3);frame.thumbnail((640,360));thumb.paste(frame,((i%2)*640,(i//2)*360))
thumb.save(out/'video_storyboard.png')
(out/'README.md').write_text('# Graphical abstract video and recording package\n\nThe video is silent, 1280 by 720 pixels, fifteen frames per second, and one hundred seconds long. Record your narration using recording_script.txt or the timed Markdown version. The separate subtitle file follows the planned pacing; adjust its timing to your actual recording. Mathematics appear only in on-screen captions.\n\nThis is a candidate presentation of proposed research, based on the replacement figures. It uses illustrative parameters and does not establish physical quantum error correction. Figure eight remains a conceptual workflow pending a software audit. Confirm the submitted manuscript, captions, and journal video requirements before submission.\n\nThe source script reproduces the video using Pillow, NumPy, and a local installation of the video encoder. No synthetic narration or background music is included.\n',encoding='utf-8')
print(json.dumps({'video':str(out/'graphical_abstract_recording_video.mp4'),'duration':DURATION,'spoken_words':len(spoken.split()),'script_abbreviation_check':'passed'}))
