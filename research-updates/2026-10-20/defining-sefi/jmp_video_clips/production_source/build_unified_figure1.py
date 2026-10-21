from pathlib import Path
import html

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'output/unified-manuscript-figures';OUT.mkdir(parents=True,exist_ok=True)
W,H=3000,1800
parts=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
 '<rect width="3000" height="1800" fill="white"/>',
 '<style>text{font-family:Arial,sans-serif;fill:#162332}.math{font-family:Cambria,"Times New Roman",serif}.muted{fill:#475766}</style>']
def text(x,y,s,size=44,anchor='start',css='',weight='normal'):
    parts.append(f'<text x="{x}" y="{y}" font-size="{size}" text-anchor="{anchor}" class="{css}" font-weight="{weight}">{s}</text>')
def sub(s):return '<tspan baseline-shift="sub" font-size="68%">'+s+'</tspan>'
def sup(s):return '<tspan baseline-shift="super" font-size="68%">'+s+'</tspan>'
def line(x1,y1,x2,y2,color='#c6d0d8',width=3):parts.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="{width}"/>')
text(120,140,'Proposed stability manifold',76,weight='bold')
text(120,218,'Worldline geometry, identity-space constraints and invariant preservation',43,css='muted')
line(120,263,2880,263)
text(120,350,'A   Constraint intersection',43,weight='bold')
text(1840,350,'B   Conditions stated on Σ',43,weight='bold')
line(1740,330,1740,1530)

# Set-membership schematic only: circle geometry is not a physical metric or phase map.
circles=[('geometry',650,815,'#2a6d94'),('identity',1090,815,'#b45b23'),('sovereignty',870,1130,'#638348')]
parts.append('<defs>')
for name,cx,cy,color in circles:parts.append(f'<clipPath id="{name}"><circle cx="{cx}" cy="{cy}" r="360"/></clipPath>')
parts.append('</defs>')
for name,cx,cy,color in circles:parts.append(f'<circle cx="{cx}" cy="{cy}" r="360" fill="{color}" fill-opacity="0.08" stroke="{color}" stroke-width="5"/>')
parts.append('<g clip-path="url(#geometry)"><g clip-path="url(#identity)"><circle cx="870" cy="1130" r="360" fill="#176779" fill-opacity="0.3"/></g></g>')
text(410,405,'Geometric constraints',39,'middle',weight='bold')
text(410,458,'Σ'+sub('geom'),55,'middle',css='math')
text(1310,405,'Identity constraints',39,'middle',weight='bold')
text(1310,458,'Σ'+sub('ident'),55,'middle',css='math')
text(870,1530,'Sovereignty constraints, Σ'+sub('S'),39,'middle',weight='bold')
text(870,935,'Σ',86,'middle',css='math')
text(870,991,'common locus',31,'middle')
text(870,1605,'Σ = Σ'+sub('geom')+' ∩ Σ'+sub('ident')+' ∩ Σ'+sub('S'),44,'middle',css='math')

text(1840,466,'Worldline geometry',39,weight='bold')
text(1840,539,'κ = κ'+sub('Σ')+' ;  τ'+sub('g')+' = τ'+sub('Σ'),57,css='math')
text(1840,600,'Constant curvature and torsion',35,css='muted')
line(1840,652,2880,652)
text(1840,732,'Identity and sovereignty',39,weight='bold')
text(1840,807,'I'+sup('a')+' = I'+sup('a')+sub('Σ')+' ;  a ∈ {O, A, S, W}',53,css='math')
text(1840,875,'O: Origin;  A: Authorship',35,css='muted')
text(1840,929,'S: Sovereignty;  W: Warp Expression',35,css='muted')
line(1840,983,2880,983)
text(1840,1065,'Identity-space dynamics',39,weight='bold')
text(1840,1142,'dI'+sup('a')+'/dτ = 0 ;  d'+sup('2')+'I'+sup('a')+'/dτ'+sup('2')+' = 0',53,css='math')
text(1840,1203,'No identity-coordinate drift on Σ',35,css='muted')
line(1840,1257,2880,1257)
text(1840,1339,'Associated field condition',39,weight='bold')
text(1840,1416,'TΨ = λΨ ;  Ψ|'+sub('Σ')+' ≠ 0',57,css='math')
line(120,1650,2880,1650)
text(120,1720,'Schematic set intersection; no metric scale, computed boundary or experimental phase diagram is implied.',34,css='muted')
parts.append('</svg>')
(OUT/'Fig1_Stability_Surface.svg').write_text('\n'.join(parts),encoding='utf-8')
(OUT/'Fig1_Stability_Surface_notes.txt').write_text(
 'Replacement for Fig1_Stability_Surface.jpg in unifiying.tex.\n'
 'Source: Section Stability Manifolds, including geometric, identity, sovereignty and dynamical conditions.\n'
 'Set circles are symbolic and are not calculated stability boundaries. The eigenfield condition is reproduced as a stated manuscript condition, not newly proved.\n'
 'Alt text: Three overlapping sets represent geometric, identity and sovereignty constraints. Their common intersection is labelled Sigma. A companion panel lists constant curvature and torsion, fixed identity coordinates for Origin, Authorship, Sovereignty and Warp Expression, zero identity velocity and acceleration, and the associated stated eigenfield condition.\n',encoding='utf-8')
print(OUT/'Fig1_Stability_Surface.svg')
