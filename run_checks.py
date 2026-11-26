from pathlib import Path
import subprocess,sys,json,hashlib,platform
root=Path(__file__).resolve().parent
names=['verify_model.py','radial_benchmark.py','check_surface_extension.py','check_coherent_surface_bridge.py','check_forced_oscillator_bridge.py','check_two_sector_saddle_bridge.py','check_phase_loss_boundary.py','check_integrated_recovery.py']
records=[];logs=[]
for name in names:
    print('Checking '+name,flush=True)
    result=subprocess.run([sys.executable,'-B','-X','utf8',name],cwd=root/'numerical',capture_output=True,text=True,encoding='utf-8')
    logs.append(name+'\n'+result.stdout+result.stderr)
    (root/'verification_transcript.txt').write_text('\n\n'.join(logs),encoding='utf-8')
    if result.returncode:raise RuntimeError(name+' failed\n'+logs[-1])
    records.append(dict(script=name,returncode=result.returncode,sha256=hashlib.sha256((root/'numerical'/name).read_bytes()).hexdigest()))
radial=json.loads((root/'numerical/radial-results.json').read_text());runs=radial['runs']
assert max(r['residual'] for r in runs)<1e-8
assert all(runs[i+1]['relative_virial']/runs[i]['relative_virial']<.3 for i in [0,1])
assert abs(runs[2]['energy']-runs[3]['energy'])<1e-7
(root/'verification.json').write_text(json.dumps(dict(all_passed=True,date='2026-11-25',python=sys.version,platform=platform.platform(),scripts=records,radial_grid_domain_checks=True),indent=2),encoding='utf-8')
print('All eight scripts and radial refinement/domain checks passed.',flush=True)
