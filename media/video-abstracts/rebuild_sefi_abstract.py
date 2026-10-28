from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import subprocess,shutil,math
src=Path('V:/V Drive and GitHub Content/CV-/Defining SEFI')
out=Path('C:/Users/jason/Documents/Codex/2026-10-27/i-need/outputs/video-publication');out.mkdir(parents=True,exist_ok=True)
scenes=[('Fig5_Photonic_Implementation.jpg','FROM PHOTONIC INTUITION','Stable patterns can be explored geometrically.'),('Fig2_Worldline_Geometry.jpg','ONE CONTINUOUS ENTITY','A proposed worldline interpretation.'),('Fig1_Stability_Surface.jpg','TWO ORIENTATIONS, ONE ENTITY','Opposite orientations in the proposed model.'),('Highlight.jpg','OBSERVER GEOMETRY','A conceptual connection between entity and observer.')]
font=lambda n:ImageFont.truetype('C:/Windows/Fonts/arial.ttf',n)
frames=[]
for name,title,caption in scenes:
 im=Image.open(src/name).convert('RGB');im.thumbnail((1280,550),Image.Resampling.LANCZOS)
 bg=Image.new('RGB',(1280,720),'#10232e');bg.paste(im,((1280-im.width)//2,125+(550-im.height)//2))
 d=ImageDraw.Draw(bg);d.rectangle((0,0,1280,124),fill='#10232e');d.text((38,22),title,font=font(37),fill='white');d.text((40,78),caption,font=font(23),fill='#c4d7e3')
 d.rectangle((0,676,1280,720),fill='#10232e');d.text((38,689),'Jason Duran Dutton | Independent research proposal | Conceptual illustration',font=font(19),fill='#c4d7e3');frames.append(bg)
video=out/'Graphical_Abstract_SEFI_rebuilt.mp4'
p=subprocess.Popen([shutil.which('ffmpeg'),'-y','-v','error','-f','rawvideo','-pix_fmt','rgb24','-s','1280x720','-r','15','-i','-','-an','-c:v','libx264','-preset','fast','-crf','20','-pix_fmt','yuv420p','-movflags','+faststart',str(video)],stdin=subprocess.PIPE)
for k in range(300):
 scene=min(k//75,3);im=frames[scene];local=k%75
 if scene>0 and local<8:im=Image.blend(frames[scene-1],im,local/8)
 p.stdin.write(im.tobytes())
p.stdin.close();assert p.wait()==0
frames[0].save(out/'sefi_poster.png')
shutil.copy2(src/'JMP_Video_Abstract_Unified_Geometric_Field_Theory.mp4',out/'JMP_Video_Abstract_Unified_Geometric_Field_Theory.mp4')
shutil.copy2('C:/Users/jason/Documents/Codex/2026-10-27/i-need/outputs/photonics-narrated/graphical_abstract_narrated.mp4',out/'graphical_abstract_narrated.mp4')
dest=Path('V:/V Drive and GitHub Content/Journal Submissions/Video Publication');dest.mkdir(exist_ok=True)
for path in out.iterdir():shutil.copy2(path,dest/path.name)
print(video)
