"""Graphical summary of the manuscript's proposed mathematical structure."""
from pathlib import Path
common=Path(__file__).with_name('build_unified_figure2.py').read_text(encoding='utf-8').split("text(120,140,")[0]
exec(compile(common,__file__,'exec'))
text(120,140,'Unified geometric field framework',76,weight='bold')
text(120,218,'Worldline geometry + identity space + dynamical invariants',43,css='muted')
line(120,263,2880,263)

def card(x,y,w,h,color):
    parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="18" fill="{color}" fill-opacity="0.055" stroke="{color}" stroke-width="4"/>')
for x,color in [(120,'#2a6d94'),(1080,'#b45b23'),(2040,'#638348')]:card(x,340,840,400,color)
text(540,412,'Worldline geometry',44,'middle',weight='bold')
text(540,465,'GWFM',34,'middle',css='muted')
pts=[(260+560*u,555+48*math.sin(2*math.pi*u)) for u in np.linspace(0,1,200)]
parts.append('<polyline points="'+' '.join(f'{x:.2f},{y:.2f}' for x,y in pts)+'" fill="none" stroke="#2a6d94" stroke-width="7"/>')
text(540,676,'Curvature κ; torsion τ'+sub('g'),45,'middle',css='math')

text(1500,412,'Identity space',44,'middle',weight='bold')
text(1500,465,'SEFI',34,'middle',css='muted')
for x,label in [(1230,'O'),(1410,'A'),(1590,'S'),(1770,'W')]:
    parts.append(f'<circle cx="{x}" cy="555" r="43" fill="white" stroke="#b45b23" stroke-width="4"/>')
    text(x,571,label,43,'middle',css='math')
text(1500,676,'I = (I'+sub('O')+', I'+sub('A')+', I'+sub('S')+', I'+sub('W')+')',45,'middle',css='math')

text(2460,412,'Dynamical invariants',44,'middle',weight='bold')
text(2460,465,'DEFI',34,'middle',css='muted')
text(2460,550,'Ideal evolution preserves',36,'middle',css='muted')
text(2460,615,'κ, τ'+sub('g')+', dI/dτ, d'+sup('2')+'I/dτ'+sup('2'),47,'middle',css='math')
text(2460,681,'D/dτ (invariants) = 0',40,'middle',css='math')

for x in [540,1500,2460]:line(x,755,x,831,color='#2a6d94',width=6,marker='tangent')
card(120,850,2760,340,'#176779')
text(1500,921,'Proposed unified operator acting on Ψ(x, I)',45,'middle',weight='bold')
text(1500,1015,'T = T'+sub('M')+' + T'+sub('I')+' + V'+sub('geom')+' + V'+sub('ident')+' + V'+sub('dyn'),68,'middle',css='math')
text(1500,1111,'T'+sub('M')+' = −g'+sup('μν')+'∇'+sub('μ')+'∇'+sub('ν')+' ;  T'+sub('I')+' = g'+sub('I')+sup('ab')+'∇'+sub('a')+'∇'+sub('b'),52,'middle',css='math')
for x in [540,1500,2460]:line(x,1205,x,1280,color='#2a6d94',width=6,marker='tangent')

for x,color in [(120,'#2a6d94'),(1080,'#176779'),(2040,'#638348')]:card(x,1300,840,270,color)
text(540,1374,'Candidate modes',43,'middle',weight='bold')
text(540,1450,'TΨ'+sub('n')+' = λ'+sub('n')+'Ψ'+sub('n'),54,'middle',css='math')
text(540,1523,'Physical identification requires testing',32,'middle',css='muted')
text(1500,1374,'Stability and projection',43,'middle',weight='bold')
text(1500,1450,'Σ;  C = Π'+sub('Σ'),54,'middle',css='math')
text(1500,1523,'Geometric and identity constraints',32,'middle',css='muted')
text(2460,1374,'Photonic application',43,'middle',weight='bold')
text(2460,1450,'S'+sub('ph')+' = (Δκ, Δτ'+sub('g')+', Δω, Δθ'+sub('pol')+')',43,'middle',css='math')
text(2460,1523,'Proposed syndrome framework',32,'middle',css='muted')
line(120,1650,2880,1650)
text(120,1720,'Conceptual summary of the manuscript; arrows show mathematical organization, not experimental validation.',34,css='muted')
parts.append('</svg>')
svg='\n'.join(parts);(OUT/'Highlight.svg').write_text(svg,encoding='utf-8')
png=resvg_py.svg_to_bytes(svg_string=svg,width=3000,height=1800)
Image.open(io.BytesIO(png)).convert('RGB').save(OUT/'Highlight.jpg',quality=100,subsampling=0,dpi=(300,300))
(OUT/'Highlight_notes.txt').write_text(
 'Graphical summary for Highlight.jpg referenced in unifiying.tex. Source: Unified Transformation Operator, Stability Manifolds, Correction Mapping and Photonic Implementation sections. T_M and T_I are labelled abbreviations for the two differential terms in the manuscript operator.\n'
 'The curve icon and identity nodes are schematic. No spectrum, physical particle identification, verified correction performance or empirical unification is asserted.\n'
 'Alt text: Three upper panels summarize GWFM worldline curvature and torsion, SEFI identity coordinates, and DEFI dynamical invariants. Arrows connect these to the proposed unified operator, with its two differential terms defined. Lower panels show the candidate eigenmode equation, stability and projection structures, and the proposed photonic syndrome framework.\n',encoding='utf-8')
print(OUT/'Highlight.jpg')
