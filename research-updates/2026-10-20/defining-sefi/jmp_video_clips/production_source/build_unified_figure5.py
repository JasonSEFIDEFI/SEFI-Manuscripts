"""Conceptual photonic workflow grounded in the manuscript's Section VI."""
from pathlib import Path
common=Path(__file__).with_name('build_unified_figure2.py').read_text(encoding='utf-8').split("text(120,140,")[0]
exec(compile(common,__file__,'exec'))
text(120,140,'Proposed photonic implementation',76,weight='bold')
text(120,218,'Optical propagation, selected observables and geometric syndrome representation',43,css='muted')
line(120,263,2880,263)
text(120,350,'A   Conceptual optical-to-syndrome workflow',43,weight='bold')

def box(x,title,lines,color):
    parts.append(f'<rect x="{x}" y="455" width="615" height="365" rx="18" fill="{color}" fill-opacity="0.06" stroke="{color}" stroke-width="4"/>')
    text(x+307.5,528,title,36,'middle',weight='bold')
    for j,s in enumerate(lines):text(x+307.5,607+58*j,s,33,'middle',css='muted')
box(120,'Prepared photonic mode',['Optical input / encoding','SPDC is one source','discussed in the manuscript'],'#2a6d94')
box(835,'Propagation and errors',['Loss; dephasing','Mode mixing','Spectral drift'],'#b45b23')
box(1550,'Selected observables',['Geometric / spectral /','polarization deviations','Weak or QND sampling proposed'],'#638348')
box(2265,'Syndrome representation',['Deviation vector S'+sub('ph'),'Mathematical description','for the proposed framework'],'#2a6d94')
for start,end in [(745,820),(1460,1535),(2175,2250)]:line(start,638,end,638,color='#2a6d94',width=6,marker='tangent')
text(120,901,'Boxes indicate proposed functions, not a specified or experimentally validated optical circuit.',34,css='muted')
line(120,959,2880,959)
line(1660,1010,1660,1530)
text(120,1050,'B   Syndrome components',43,weight='bold')
text(1770,1050,'C   Geometric correction target',43,weight='bold')
text(120,1147,'S'+sub('ph')+' = (Δκ'+sub('ph')+', Δτ'+sub('g,ph')+', Δω, Δθ'+sub('pol')+')',54,css='math')
text(120,1236,'Δκ'+sub('ph')+': curvature deviation',40,css='math')
text(120,1303,'Δτ'+sub('g,ph')+': torsion deviation',40,css='math')
text(120,1370,'Δω: frequency deviation',40,css='math')
text(120,1437,'Δθ'+sub('pol')+': polarization-angle deviation',40,css='math')

text(1770,1147,'C = Π'+sub('Σph'),59,css='math')
text(1770,1236,'κ'+sub('ph')+' = κ'+sub('Σ')+' ;  τ'+sub('g,ph')+' = τ'+sub('Σ'),51,css='math')
text(1770,1311,'I'+sup('a')+' = I'+sup('a')+sub('Σ')+' ;  a ∈ {O, A, S, W}',46,css='math')
text(1770,1386,'dI'+sup('a')+'/dτ = 0 ;  d'+sup('2')+'I'+sup('a')+'/dτ'+sup('2')+' = 0',46,css='math')
text(1770,1471,'Target conditions stated for Σ'+sub('ph'),35,css='muted')
line(120,1650,2880,1650)
text(120,1720,'Conceptual proposal; no syndrome-to-actuator implementation, loss recovery or correction performance is demonstrated here.',33,css='muted')
parts.append('</svg>')
svg='\n'.join(parts);(OUT/'Fig5_Photonic_Implementation.svg').write_text(svg,encoding='utf-8')
png=resvg_py.svg_to_bytes(svg_string=svg,width=3000,height=1800)
Image.open(io.BytesIO(png)).convert('RGB').save(OUT/'Fig5_Photonic_Implementation.jpg',quality=100,subsampling=0,dpi=(300,300))
(OUT/'Fig5_Photonic_Implementation_notes.txt').write_text(
 'Source: unifiying.tex, Photonic Implementation section. Functional boxes summarize the manuscript proposal and are not an apparatus design. No components, quantum channels, encoders, detector models, syndrome inversion or feedback actuators have been invented. No implication that geometric projection restores a lost photon is made.\n'
 'The listed syndrome and target conditions reproduce manuscript statements; their optical measurability and implementation are not established by this diagram.\n'
 'Alt text: Four proposed functional stages connect a prepared photonic mode, propagation and errors, selected observables with proposed weak or QND sampling, and a mathematical syndrome representation. Lower panels list the four syndrome components and the proposed geometric correction target and invariant conditions.\n',encoding='utf-8')
print(OUT/'Fig5_Photonic_Implementation.jpg')
