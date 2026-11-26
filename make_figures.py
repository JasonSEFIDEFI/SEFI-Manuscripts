"""Compatibility entry point: regenerate all eight current manuscript figures."""
from pathlib import Path
import subprocess,sys
root=Path(__file__).resolve().parent
for name in ['make_recovery_figures.py','make_field_figures.py']:
    subprocess.run([sys.executable,name],cwd=root,check=True)
