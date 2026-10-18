"""Independent algebra/numerical checks, not experimental validation."""
import math, json, hashlib
from pathlib import Path
p=Path(__file__).resolve().parent
eta=[-1,1,1,1]
q=[.7,1.1,-.4,.8]; alpha=.3; beta=.6; W=.2
q2=sum(eta[i]*q[i]**2 for i in range(4))
def ricci(h):
    trace=sum(eta[i]*h[i][i] for i in range(4))
    return [[.5*(-sum(eta[r]*q[r]*q[a]*h[r][b] for r in range(4))
                     -sum(eta[r]*q[r]*q[b]*h[r][a] for r in range(4))
                     +q2*h[a][b]+q[a]*q[b]*trace) for b in range(4)] for a in range(4)]
hbeta=[[-beta*q[a]*q[b]*W for b in range(4)] for a in range(4)]
halpha=[[alpha*W*eta[a] if a==b else 0 for b in range(4)] for a in range(4)]
rb=ricci(hbeta); ra=ricci(halpha)
beta_riemann=max(abs(.5*(-q[c]*q[b]*hbeta[a][d]-q[d]*q[a]*hbeta[b][c]
    +q[d]*q[b]*hbeta[a][c]+q[c]*q[a]*hbeta[b][d]))
    for a in range(4) for b in range(4) for c in range(4) for d in range(4))
alpha_err=max(abs(ra[a][b]-(alpha*q[a]*q[b]*W+
     (.5*alpha*eta[a]*q2*W if a==b else 0))) for a in range(4) for b in range(4))
Z=2.; mu=.4; gs=1.2; gt=.8; r=1.7; step=1e-5
def V(r): return -gs*gt*math.exp(-mu*r)/(4*math.pi*Z*r)
F=-gs*gt*math.exp(-mu*r)*(1+mu*r)/(4*math.pi*Z*r*r)
Fn=-(V(r+step)-V(r-step))/(2*step)
v=[.2,-.1,.3]; gamma=1/math.sqrt(1-sum(x*x for x in v)); u=[gamma]+[gamma*x for x in v]
grad=[.7,-.2,.4,.9]
force=[-sum(((eta[a] if a==b else 0)+u[a]*u[b])*grad[b] for b in range(4)) for a in range(4)]
orth=sum(eta[a]*u[a]*force[a] for a in range(4))
ell=1.3; rad=.8
def field(x): return math.exp(-x*x/(2*ell*ell))
lap_num=(field(rad+step)-2*field(rad)+field(rad-step))/step**2+2/rad*(field(rad+step)-field(rad-step))/(2*step)
lap_exact=(rad**2/ell**4-3/ell**2)*field(rad)
c=299792458.; G=6.67430e-11
results={
 'meaning':'Mathematical consistency checks only; no force measurements or engine simulation.',
 'beta_linearized_riemann_max_abs':beta_riemann,
 'beta_linearized_ricci_max_abs':max(abs(x) for row in rb for x in row),
 'alpha_linearized_ricci_max_abs_error':alpha_err,
 'yukawa_force_relative_finite_difference_error':abs(F-Fn)/abs(F),
 'four_force_orthogonality_abs_error':abs(orth),
 'gaussian_laplacian_abs_error':abs(lap_num-lap_exact),
 'conditional_GR_example':{'a_coordinate_m_s2':1.,'k_per_m':1.,
    'energy_density_amplitude_J_m3':c*c/(4*math.pi*G),
    'equivalent_mass_density_kg_m3':1/(4*math.pi*G)},
 'candidate_gaussian_source_sign_change_r_over_ell':math.sqrt(3+(mu*ell)**2),
}
assert beta_riemann<1e-14 and alpha_err<1e-14 and abs(orth)<1e-14
assert abs(F-Fn)/abs(F)<1e-7 and abs(lap_num-lap_exact)<1e-4
(p/'results.json').write_text(json.dumps(results,indent=2))
manifest=json.loads((p.parent.parent/'tmp/charge-audit/manifest.json').read_text())
for f in [Path('V:/V Drive and GitHub Content/Journal Submissions/DEFI/DEFI_Formal_Construction.tex'),
          Path('V:/V Drive and GitHub Content/Journal Submissions/Warp/Warp.tex'),
          Path('V:/V Drive and GitHub Content/Journal Submissions/The New Warp/warp.tex')]:
    manifest.append({'path':str(f),'sha256':hashlib.sha256(f.read_bytes()).hexdigest()})
(p/'source-manifest.json').write_text(json.dumps(manifest,indent=2))
print(json.dumps(results,indent=2))
