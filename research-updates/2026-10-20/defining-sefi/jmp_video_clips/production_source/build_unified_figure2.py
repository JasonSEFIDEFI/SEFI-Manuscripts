from pathlib import Path
import math,sys,io
import numpy as np
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tmp/figure-render-deps'))
import resvg_py
OUT=ROOT/'output/unified-manuscript-figures';OUT.mkdir(parents=True,exist_ok=True)
parts=['<svg xmlns="http://www.w3.org/2000/svg" width="3000" height="1800" viewBox="0 0 3000 1800">',
 '<rect width="3000" height="1800" fill="white"/>',
 '<style>text{font-family:Arial,sans-serif;fill:#162332}.math{font-family:Cambria,"Times New Roman",serif}.muted{fill:#475766}</style>',
 '<defs>']
for name,color in [('curve','#2a6d94'),('tangent','#2a6d94'),('normal','#b45b23'),('binormal','#638348')]:
    parts.append(f'<marker id="{name}" viewBox="0 0 12 12" refX="10" refY="6" markerWidth="8" markerHeight="8" orient="auto-start-reverse"><path d="M0,0 L12,6 L0,12 Z" fill="{color}"/></marker>')
parts.append('</defs>')
def sub(s):return '<tspan dy="12" font-size="68%">'+s+'</tspan><tspan dy="-12">&#8203;</tspan>'
def sup(s):return '<tspan dy="-20" font-size="68%">'+s+'</tspan><tspan dy="20">&#8203;</tspan>'
def text(x,y,s,size=44,anchor='start',css='',weight='normal',color=None):
    style=f' style="fill:{color}"' if color else ''
    parts.append(f'<text x="{x}" y="{y}" font-size="{size}" text-anchor="{anchor}" class="{css}" font-weight="{weight}"{style}>{s}</text>')
def line(x1,y1,x2,y2,color='#c6d0d8',width=3,marker=None):
    tail=f' marker-end="url(#{marker})"' if marker else ''
    parts.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="{width}"{tail}/>')
text(120,140,'Worldline geometry',76,weight='bold')
text(120,218,'Curve, local frame and geometric invariants in the proposed construction',43,css='muted')
line(120,263,2880,263)
text(120,350,'A   Schematic worldline projection',43,weight='bold')
text(1840,350,'B   Manuscript definitions',43,weight='bold')
line(1740,330,1740,1530)

# Illustrative Euclidean helix used only to lay out a 2D projected curve/frame.
# It is not a solved relativistic trajectory and has no assigned metric or units.
def point(u):return np.array([math.cos(u),math.sin(u),.55*u])
def project(q):return np.array([870+300*(q[0]-.6*q[1]),1370-160*(.35*q[0]+.45*q[1]+.85*q[2])])
us=np.linspace(0,3.5*math.pi,501);xy=np.array([project(point(u)) for u in us])
parts.append('<polyline points="'+' '.join(f'{x:.3f},{y:.3f}' for x,y in xy)+'" fill="none" stroke="#2a6d94" stroke-width="8" stroke-linejoin="round"/>')
for a,b in [(140,151),(365,376)]:line(*xy[a],*xy[b],color='#2a6d94',width=6,marker='curve')
u=5.2;q=point(u);p=project(q)
T=np.array([-math.sin(u),math.cos(u),.55]);T/=np.linalg.norm(T)
N=np.array([-math.cos(u),-math.sin(u),0.]);B=np.cross(T,N)
parts.append(f'<circle cx="{p[0]}" cy="{p[1]}" r="14" fill="#162332" stroke="white" stroke-width="4"/>')
for vector,name,color,scale,offset in [(T,'tangent','#2a6d94',1.12,(22,-6)),(N,'normal','#b45b23',.9,(-52,18)),(B,'binormal','#638348',1.6,(-36,-20))]:
    end=project(q+scale*vector)
    line(*p,*end,color=color,width=7,marker=name)
    label={'tangent':'T','normal':'N','binormal':'B'}[name]
    text(end[0]+offset[0],end[1]+offset[1],label,64,css='math',color=color)
text(1280,1112,'x'+sup('μ')+'(τ'+sub('0')+')',53,css='math')
line(p[0]+16,p[1]+16,1260,1080,width=2)
text(320,540,'x'+sup('μ')+'(τ)',64,css='math',color='#2a6d94')
text(250,1475,'Arrows along the curve indicate parameter order.',35,css='muted')
text(250,1533,'The local frame is shown at one selected point.',35,css='muted')

text(1840,468,'Local Frenet-Serret frame',39,weight='bold')
text(1840,542,'T: tangent;  N: normal;  B: binormal',44,css='math')
text(1840,607,'τ parametrizes the worldline.',35,css='muted')
line(1840,661,2880,661)
text(1840,743,'Worldline curvature',39,weight='bold')
text(1840,819,'κ(τ) = ‖DT'+sup('μ')+'/dτ‖',58,css='math')
text(1840,885,'Covariant change of the tangent',35,css='muted')
line(1840,939,2880,939)
text(1840,1021,'Worldline torsion',39,weight='bold')
text(1840,1097,'τ'+sub('g')+'(τ) = B'+sub('μ')+' DN'+sup('μ')+'/dτ',58,css='math')
text(1840,1163,'Binormal component of the normal derivative',35,css='muted')
line(1840,1217,2880,1217)
text(1840,1299,'Geometric operator contribution',39,weight='bold')
text(1840,1375,'V'+sub('geom')+' = λ'+sub('1')+'κ'+sup('2')+' + λ'+sub('2')+'τ'+sub('g')+sup('2'),58,css='math')
text(1840,1441,'As specified in the unified operator',35,css='muted')
line(120,1650,2880,1650)
text(120,1720,'Illustrative projection only; no metric scale, causal character or calculated particle trajectory is implied.',34,css='muted')
parts.append('</svg>')
svg='\n'.join(parts);(OUT/'Fig2_Worldline_Geometry.svg').write_text(svg,encoding='utf-8')
png=resvg_py.svg_to_bytes(svg_string=svg,width=3000,height=1800)
im=Image.open(io.BytesIO(png)).convert('RGB')
im.save(OUT/'Fig2_Worldline_Geometry.jpg',quality=100,subsampling=0,dpi=(300,300))
(OUT/'Fig2_Worldline_Geometry_notes.txt').write_text(
 'Source: unifiying.tex, covariant derivatives and unified operator subsections.\n'
 'The projected helix is an illustrative layout, not a solution or a causal/spacetime metric diagram. T, N and B denote the manuscript frame. Curvature, torsion and V_geom formulas reproduce the manuscript definitions without claiming a new derivation.\n'
 'Alt text: A blue curved worldline is shown in schematic projection, with arrows indicating parameter order. At a selected point, blue tangent, orange normal and green binormal arrows illustrate the local frame. A companion panel lists the manuscript definitions of curvature, torsion and the geometric contribution to the unified operator.\n',encoding='utf-8')
print(OUT/'Fig2_Worldline_Geometry.jpg')
