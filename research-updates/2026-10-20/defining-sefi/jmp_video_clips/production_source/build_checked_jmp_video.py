"""Corrected production cut: no Designer upload is used as a video asset."""
from pathlib import Path
src=Path(__file__).with_name('build_jmp_video_package.py').read_text(encoding='utf-8')
src=src.replace("ROOT/'output/jmp_video_clips'","ROOT/'output/jmp_video_clips_verified'")
src=src.replace("src=Path('C:/Users/jason/Downloads')/old;dst=OUT/new", "src=Path('C:/Users/jason/Downloads')/old;dst=OUT/'reference_only_original_uploads'/new;dst.parent.mkdir(exist_ok=True)")
src=src.replace("saved_as=new,sha256=digest(dst),original_preserved=True", "saved_as='reference_only_original_uploads/'+new,sha256=digest(dst),original_preserved=True,used_in_video=False")
replacements={
 "images=[('Uploaded_Unified_Operator_Architecture.png',None)]":"images=[('supplemental_figures/Supplement_S2_Unified_Operator.png',None)]",
 "images=[('Fig2_Worldline_Geometry.jpg',(210,430,1680,1570)),('Uploaded_Frenet_Serret_Error_Geometry.png',(25,120,1080,780))]":"images=[('Fig2_Worldline_Geometry.jpg',(210,430,1680,1570))]",
 "images=[('Uploaded_Identity_Space_Structure.png',(30,120,1030,940))]":"images=[('supplemental_figures/Supplement_S1_Identity_Space.png',None)]",
 "images=[('Uploaded_Unified_Operator_Architecture.png',(555,100,1020,830)),('Highlight.jpg',(110,845,2890,1195))]":"images=[('supplemental_figures/Supplement_S2_Unified_Operator.png',None)]",
 "images=[('Uploaded_Unified_Operator_Spectrum.png',(205,115,1310,465))]":"images=[('supplemental_figures/Supplement_S3_Candidate_Modes.png',None)]",
 "images=[('Fig1_Stability_Surface.jpg',(170,350,1700,1635)),('Uploaded_Stability_Manifold.png',(30,430,1135,945))]":"images=[('Fig1_Stability_Surface.jpg',(170,350,1700,1635))]",
 "images=[('Fig3_Error_Displacement.jpg',(165,420,1660,1590)),('Uploaded_Unified_Error_Vector.png',(20,120,1115,475))]":"images=[('Fig3_Error_Displacement.jpg',(165,420,1660,1590)),('supplemental_figures/Supplement_S4_Unified_Error.png',None)]",
 "images=[('Uploaded_Photonic_Stability_Surface.png',(240,130,1500,755)),('Fig5_Photonic_Implementation.jpg',(100,1010,1610,1460))]":"images=[('Fig5_Photonic_Implementation.jpg',None)]",
 "images=[('Uploaded_FRW_Cosmological_Extension.png',(30,245,1140,755))]":"images=[('supplemental_figures/Supplement_S5_FRW_Background.png',None)]",
 'The eigenvalue problem describes candidate excitations. These mode sketches are illustrative. Identifying a mode with an observed particle requires comparison with measured properties.':'The eigenvalue problem describes candidate excitations. Its modes and spectral values must be calculated. Identifying a mode with an observed particle requires comparison with measured properties.',
 "vf=f'fade=t=in:st=0:d=0.3:color=white,fade=t=out:st={duration-.3}:d=0.3:color=white'":"vf=f'fps=24,fade=t=in:st=0:d=0.3:color=white,fade=t=out:st={duration-.3}:d=0.3:color=white'",
 "'-framerate','30'":"'-framerate','1'",
 "'-preset','fast'":"'-preset','veryfast'",
 "'-preset','slow'":"'-preset','veryfast'"
}
for a,b in replacements.items():
    if a not in src:raise ValueError('Missing expected production replacement: '+a[:100])
    src=src.replace(a,b)
src=src.replace("print(f\"Encoded {n+1}/{len(story)}: {r['title']}\",flush=True)","print(f\"Encoded checked scene {n+1}/{len(story)}: {r['title']}\",flush=True)")
exec(compile(src,__file__,'exec'))
