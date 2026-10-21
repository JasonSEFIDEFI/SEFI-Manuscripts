"""Source-grounded displacement schematic; all drawing geometry is illustrative."""
from pathlib import Path
common=Path(__file__).with_name('build_unified_figure2.py').read_text(encoding='utf-8').split("text(120,140,")[0]
exec(compile(common,__file__,'exec'))

text(120,140,'Error displacement from the stability manifold',76,weight='bold')
text(120,218,'Local displacement and its spacetime and identity-space components',43,css='muted')
line(120,263,2880,263)
text(120,350,'A   Local coordinate schematic',43,weight='bold')
text(1840,350,'B   Displacement definitions',43,weight='bold')
line(1740,330,1740,1530)

# Illustrative manifold segment and coordinate decomposition. The diagonal arrow
# points OUT from the projected point, distinguishing error from correction.
xs=np.linspace(290,1430,300)
ys=1120+(350/470)*(xs-850)+.00012*(xs-850)**2
parts.append('<polyline points="'+' '.join(f'{x:.2f},{y:.2f}' for x,y in zip(xs,ys))+'" fill="none" stroke="#176779" stroke-width="10" stroke-linecap="round"/>')
text(320,610,'Stability manifold Σ',49,css='math',color='#176779')
line(490,637,530,ys[np.argmin(abs(xs-530))]-16,color='#176779',width=2)
p=np.array([850.,1120.]);q=np.array([1200.,650.]);corner=np.array([1200.,1120.])
line(*p,*corner,color='#b45b23',width=6,marker='normal')
line(*corner,*q,color='#638348',width=6,marker='binormal')
line(*p,*q,color='#2a6d94',width=8,marker='tangent')
for loc in [p,q]:parts.append(f'<circle cx="{loc[0]}" cy="{loc[1]}" r="16" fill="#162332" stroke="white" stroke-width="4"/>')
parts.append(f'<circle cx="{corner[0]}" cy="{corner[1]}" r="8" fill="white" stroke="#53616b" stroke-width="3"/>')
text(1215,595,'(x, I)',60,css='math')
text(940,855,'D',64,css='math',color='#2a6d94')
text(1050,1190,'D'+sub('M'),59,css='math',color='#b45b23')
text(1260,920,'D'+sub('I'),59,css='math',color='#638348')
text(180,1290,'Π'+sub('Σ')+'(x, I) = (x'+sub('Σ')+', I'+sub('Σ')+')',48,css='math')
line(660,1240,831,1143,width=2)
text(210,1510,'D points from the projected point to the displaced state.',34,css='muted')

text(1840,464,'Product-space displacement',39,weight='bold')
text(1840,536,'D(x, I) = (x, I) − Π'+sub('Σ')+'(x, I)',49,css='math')
text(1840,612,'D = D'+sub('M')+' + D'+sub('I'),54,css='math')
line(1840,662,2880,662)
text(1840,740,'Spacetime component',39,weight='bold')
text(1840,810,'D'+sub('M')+' = x − x'+sub('Σ'),54,css='math')
text(1840,881,'d'+sub('M')+' = d'+sub('T')+'T + d'+sub('N')+'N + d'+sub('B')+'B',51,css='math')
text(1840,939,'T, N, B: tangent, normal and binormal',33,css='muted')
line(1840,988,2880,988)
text(1840,1066,'Identity-space component',39,weight='bold')
text(1840,1138,'D'+sub('I')+' = I − I'+sub('Σ'),54,css='math')
text(1840,1209,'Components: d'+sub('O')+', d'+sub('A')+', d'+sub('S')+', d'+sub('W'),48,css='math')
text(1840,1267,'Origin, Authorship, Sovereignty, Warp Expression',32,css='muted')
line(1840,1318,2880,1318)
text(1840,1396,'Geometric invariant deviations',39,weight='bold')
text(1840,1468,'Δκ = κ − κ'+sub('Σ')+' ;  Δτ'+sub('g')+' = τ'+sub('g')+' − τ'+sub('Σ'),50,css='math')
line(120,1650,2880,1650)
text(120,1720,'Local coordinate illustration; projection is assumed where defined and unique. No displacement magnitudes are calculated.',33,css='muted')
parts.append('</svg>')
svg='\n'.join(parts)
(OUT/'Fig3_Error_Displacement.svg').write_text(svg,encoding='utf-8')
png=resvg_py.svg_to_bytes(svg_string=svg,width=3000,height=1800)
Image.open(io.BytesIO(png)).convert('RGB').save(OUT/'Fig3_Error_Displacement.jpg',quality=100,subsampling=0,dpi=(300,300))
(OUT/'Fig3_Error_Displacement_notes.txt').write_text(
 'Source: unifiying.tex, Error Displacement Geometry section. Coordinate subtraction and projection reproduce stated manuscript definitions in a local schematic, not an asserted global manifold construction.\n'
 'The blue displacement arrow points from the projected state to the off-manifold state; it is not the correction arrow. Orange and green arrows illustrate spacetime and identity coordinate components without assigning scales or a physical spacetime metric.\n'
 'Alt text: A curved teal line represents Sigma. A projected point on Sigma is joined to an off-manifold state by a blue displacement arrow. Orange and green coordinate-component arrows form a schematic decomposition. The companion panel lists product-space displacement, spacetime frame decomposition, identity-layer components, and curvature and torsion differences.\n',encoding='utf-8')
print(OUT/'Fig3_Error_Displacement.jpg')
