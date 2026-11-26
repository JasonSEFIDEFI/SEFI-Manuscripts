from pathlib import Path
import subprocess,shutil,re
p=Path(__file__).resolve().parent
compiler=shutil.which('pdflatex') or str(Path.home()/'AppData/Local/Programs/MiKTeX/miktex/bin/x64/pdflatex.exe')
for name in ['Conjugate_Phase_Geometry_AIP_Advances','Cover_Letter_AIP_Advances']:
 source='cover_letter.tex' if name.startswith('Cover_') else name+'.tex'
 for iteration in range(3):
  r=subprocess.run([compiler,'-interaction=batchmode','-halt-on-error','-disable-installer','-jobname='+name,source],cwd=p,capture_output=True,text=True)
  if r.returncode:raise SystemExit(r.stdout+r.stderr)
  log=(p/(name+'.log')).read_text(errors='replace')
  if iteration>0 and not re.search(r'undefined|Rerun to get|Label\(s\) may have changed',log,re.I):break
 else:raise SystemExit('Unresolved cross-references: '+name)
 if 'Overfull' in log:raise SystemExit('Overfull box: '+name)
 print(name+' compiled and checked.')
