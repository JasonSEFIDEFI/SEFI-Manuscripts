"""Manuscript-specific schematics replacing inconsistent Designer illustrations."""
from pathlib import Path
common=Path(__file__).with_name('build_unified_figure2.py').read_text(encoding='utf-8').split("text(120,140,")[0]
exec(compile(common,__file__,'exec'))
OUT=ROOT/'output/jmp_video_clips_verified/supplemental_figures';OUT.mkdir(parents=True,exist_ok=True)
base=parts.copy()
records=[]
def begin(title,subtitle):
    global parts
    parts=base.copy();text(120,140,title,76,weight='bold');text(120,218,subtitle,43,css='muted');line(120,263,2880,263)
def card(x,y,w,h,color='#176779'):
    parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="18" fill="{color}" fill-opacity="0.045" stroke="{color}" stroke-width="4"/>')
def save(name,caption,note):
    line(120,1650,2880,1650);text(120,1720,note,36,css='muted');parts.append('</svg>');svg='\n'.join(parts)
    (OUT/(name+'.svg')).write_text(svg,encoding='utf-8')
    png=resvg_py.svg_to_bytes(svg_string=svg,width=3000,height=1800)
    im=Image.open(io.BytesIO(png)).convert('RGB');im.save(OUT/(name+'.png'),dpi=(300,300));im.save(OUT/(name+'.jpg'),quality=100,subsampling=0,dpi=(300,300))
    records.append(dict(filename=name+'.png',caption=caption,scope=note))

begin('Proposed identity-space coordinates','Four internal model coordinates, with the metric stated in the manuscript')
for x,letter,label,color in [(120,'O','Origin','#2a6d94'),(835,'A','Authorship','#b45b23'),(1550,'S','Sovereignty','#176779'),(2265,'W','Warp Expression','#638348')]:
    card(x,430,615,380,color);text(x+307,555,'I'+sub(letter),96,'middle',css='math');text(x+307,710,label,52,'middle',weight='bold')
text(1500,1010,'I = (I'+sub('O')+', I'+sub('A')+', I'+sub('S')+', I'+sub('W')+') ∈ ℐ = ℝ'+sup('4'),76,'middle',css='math')
text(1500,1195,'g'+sub('I')+' = diag(α, β, γ, δ) ;  α, β, γ, δ &gt; 0',62,'middle',css='math')
text(1500,1400,'Displacement components: (d'+sub('O')+', d'+sub('A')+', d'+sub('S')+', d'+sub('W')+')',62,'middle',css='math')
save('Supplement_S1_Identity_Space','Four proposed identity coordinates and the positive diagonal identity metric specified for the manuscript Hilbert-space construction. The cards label coordinates without asserting a measurable orthonormal embedding.','Internal coordinates of the proposed model; no experimental coordinate measurements are shown.')

begin('Proposed unified operator','Differential terms and potentials exactly as specified in the manuscript')
text(1500,470,'T = −g'+sup('μν')+'∇'+sub('μ')+'∇'+sub('ν')+' + g'+sub('I')+sup('ab')+'∇'+sub('a')+'∇'+sub('b'),78,'middle',css='math')
text(1500,610,'+ V'+sub('geom')+' + V'+sub('ident')+' + V'+sub('dyn'),78,'middle',css='math')
for y in [760,1030,1300]:card(120,y,2760,210)
text(1500,889,'V'+sub('geom')+' = λ'+sub('1')+'κ'+sup('2')+' + λ'+sub('2')+'τ'+sub('g')+sup('2'),68,'middle',css='math')
text(1500,1159,'V'+sub('ident')+' = αI'+sub('O')+sup('2')+' + βI'+sub('A')+sup('2')+' + γI'+sub('S')+sup('2')+' + δI'+sub('W')+sup('2'),68,'middle',css='math')
text(1500,1429,'V'+sub('dyn')+' = η'+sub('1')+'‖dI/dτ‖'+sub('I')+sup('2')+' + η'+sub('2')+'‖d'+sup('2')+'I/dτ'+sup('2')+'‖'+sub('I')+sup('2'),65,'middle',css='math')
save('Supplement_S2_Unified_Operator','The proposed differential operator and its three potentials, reproducing the manuscript definitions. No claim about self-adjointness, spectrum or physical identification follows from this expression alone.','A defined operator expression; its properties require a specified domain, metrics and boundary conditions.')

begin('Candidate eigenmode relation','A mathematical problem to solve, without invented eigenfunctions or spectral values')
card(120,420,830,780,'#2a6d94');card(1085,420,1795,780)
text(535,545,'Specify the problem',51,'middle',weight='bold')
for y,label in [(700,'Metrics and potentials'),(855,'Operator domain'),(1010,'Boundary conditions')]:text(535,y,label,49,'middle')
line(967,810,1063,810,color='#2a6d94',width=7,marker='tangent')
text(1982,600,'Candidate mode equation',56,'middle',weight='bold')
text(1982,805,'TΨ'+sub('n')+' = λ'+sub('n')+'Ψ'+sub('n'),110,'middle',css='math')
text(1982,1010,'Modes and spectral values must be calculated.',48,'middle',css='muted')
text(1500,1390,'Particle identification requires masses, charges, spins and couplings.',55,'middle')
save('Supplement_S3_Candidate_Modes','Schematic organization of the eigenmode problem. The figure contains no computed eigenfunctions, invented level spacing, assumed one-dimensional eigenspaces or asserted identification with particles.','No eigenfunctions or spectral values are calculated in this diagram.')

begin('Unified error description','Geometric, identity-space and dynamical deviations listed in the manuscript')
for x,title,lineset,color in [
    (120,'Geometric sector',[('d'+sub('N')+', d'+sub('B'),76),('Δκ, Δτ'+sub('g'),76)],'#2a6d94'),
    (1080,'Identity sector',[('d'+sub('O')+', d'+sub('A'),76),('d'+sub('S')+', d'+sub('W'),76)],'#b45b23'),
    (2040,'Dynamical sector',[('Δ(dI'+sup('a')+'/dτ)',70),('Δ(d'+sup('2')+'I'+sup('a')+'/dτ'+sup('2')+')',70)],'#638348')]:
    card(x,420,840,640,color);text(x+420,535,title,53,'middle',weight='bold')
    for j,(s,size) in enumerate(lineset):text(x+420,735+170*j,s,size,'middle',css='math')
    line(x+420,1085,x+420,1190,color='#2a6d94',width=7,marker='tangent')
card(120,1220,2760,310)
text(1500,1340,'E(τ) = (geometric, identity, dynamical components)',65,'middle',css='math')
text(1500,1450,'Velocity and acceleration deviations are not renamed as inertial or interaction coordinates.',43,'middle',css='muted')
save('Supplement_S4_Unified_Error','Grouping of the error-vector components defined in the manuscript. The dynamical entries denote deviations of identity-space velocity and acceleration, without introducing new inertial or interaction variables.','Component labels follow the manuscript; the diagram does not supply a measured error model.')

begin('FRW background extension','An illustrative sequence of spatial slices; no fitted cosmic history or full spectrum')
for cx,size,label in [(350,170,'t'+sub('0')),(1040,250,'t'+sub('1')),(1800,340,'t'+sub('2')),(2600,440,'t'+sub('3'))]:
    x=cx-size/2;y=820-size/2
    parts.append(f'<rect x="{x}" y="{y}" width="{size}" height="{size}" fill="#eef5f7" stroke="#176779" stroke-width="4"/>')
    for frac in [.25,.5,.75]:line(x+size*frac,y,x+size*frac,y+size,color='#a6bec6',width=2);line(x,y+size*frac,x+size,y+size*frac,color='#a6bec6',width=2)
    text(cx,1160,label,58,'middle',css='math')
line(230,1210,2780,1210,color='#2a6d94',width=5,marker='tangent')
text(1500,1390,'H(t) = (da/dt) / a(t)',76,'middle',css='math')
text(1500,1515,'The spatial derivative term scales as a(t)'+sup('−2')+'; the full operator requires separate analysis.',48,'middle')
save('Supplement_S5_FRW_Background','Schematic expanding grid patches at successive times and the standard definition of the Hubble parameter. Patch sizes are illustrative; they do not specify a cosmological solution, spatial curvature, inflation mechanism or full operator spectrum.','Schematic grid patches only; no expansion data, inflation result or spectral prediction is plotted.')

import json
(OUT/'Supplemental_Figure_Captions.json').write_text(json.dumps(records,indent=2)+'\n',encoding='utf-8')
print('Created',len(records),'checked supplemental schematics',flush=True)
