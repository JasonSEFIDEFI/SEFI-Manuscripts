"""Checks for declared sandbox geometry; not a SEFI propulsion simulation."""
from pathlib import Path
import math,json,hashlib

def geometry(L,R,d):
    assert L>=2*R and R>0 and d>0
    c=L-2*R
    volume=lambda r:math.pi*r*r*c+4*math.pi*r**3/3
    return dict(body_m3=volume(R),shell_m3=volume(R+d)-volume(R),area_m2=2*math.pi*R*c+4*math.pi*R*R)
def taper(u):return 1-10*u**3+15*u**4-6*u**5
def derivative(u):return -30*u*u+60*u**3-30*u**4

assert taper(0)==1 and taper(1)==0
assert derivative(0)==derivative(1)==0
assert abs(derivative(.5))==15/8
assert all(-1e-12<=taper(i/1000)<=1+1e-12 for i in range(1001))
assert max(abs(derivative(i/1000)) for i in range(1001))==15/8
for A,d in [(0,1),(.1,1),(.5,1),(.1,.5)]:
    G=15*abs(A)/(8*d)
    if G<1:
        # 1D normal-coordinate slice; analytic proof gives the stated general
        # sufficient bound under the workbook's global Lipschitz assumptions.
        xs=[-1+3*i/500 for i in range(501)]
        def shift(x):return A*(1 if x<0 else (0 if x>d else taper(x/d)))
        ys=[x+shift(x) for x in xs]
        assert min((ys[i+1]-ys[i])/(xs[i+1]-xs[i]) for i in range(500))>=1-G-1e-10
ref=geometry(14,2,1)
paths=[Path('V:/V Drive and GitHub Content/Journal Submissions/Warp/Warp.tex'),Path('V:/V Drive and GitHub Content/Journal Submissions/The New Warp/warp.tex')]
manifest=[dict(path=str(p),sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for p in paths]
out=Path(__file__).parent
(out/'source-manifest.json').write_text(json.dumps(manifest,indent=2))
results=dict(reference=ref,example_gradient_bound=.1875,example_separation_lower_factor=.8125,
             emitter_force_at_1000W_N=1000/299792458,
             checks='taper endpoints, derivative maximum, monotonic slices, geometry',
             physical_propulsion_tested=False)
(out/'checks.json').write_text(json.dumps(results,indent=2))
print(json.dumps(results,indent=2))
