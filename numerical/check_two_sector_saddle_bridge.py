"""Conditional two-sector construction using the existing S/W coupling form.

The quadratic curvature/torsion profiles and equal oscillator parameters are
design assumptions, not predictions of the full coupled field equations.
Both auxiliary sectors are retained and coherently decoded.
"""
from pathlib import Path
import math,json
import numpy as np

J0=.1;alpha=.25;beta=.15;k=1.;mu=nu=1.
locations=[(x,y) for x in (-1.,0.,1.) for y in (-1.,0.,1.)]
forces=[(J0+k*alpha*x*x/math.sqrt(2),J0+k*beta*y*y/math.sqrt(2)) for x,y in locations]
def unitary(H,t):
    vals,vecs=np.linalg.eigh(H)
    return (vecs*np.exp(-1j*t*vals))@vecs.conj().T

rows=[]
for cutoff in (18,30,42):
    a=np.diag(np.sqrt(np.arange(1,cutoff)),1)
    Q=(a+a.T)/math.sqrt(2);P=(a-a.T)/(1j*math.sqrt(2))
    H0=np.diag(np.arange(cutoff,dtype=float))
    g=np.zeros(cutoff,dtype=complex);g[0]=1
    Us=[unitary(H0+js*Q,math.pi) for js,jw in forces]
    Uw=[unitary(H0+jw*Q,math.pi) for js,jw in forces]
    height_error=0.;b_error=0.
    for (x,y),(js,jw),u,w in zip(locations,forces,Us,Uw):
        vs=u@g;vw=w@g
        mean_s=float(np.vdot(vs,Q@vs).real);mean_w=float(np.vdot(vw,Q@vw).real)
        mean_z=(mean_w-mean_s)/math.sqrt(2)
        mean_b=(mean_w+mean_s)/math.sqrt(2)
        height_error=max(height_error,abs(mean_z-(alpha*x*x-beta*y*y)))
        b_error=max(b_error,abs(mean_b-(-2*math.sqrt(2)*J0-alpha*x*x-beta*y*y)))
    # A common Z shift and B shift are a common pair of S/W translations.
    dz,db=.4,-.2
    ds=(db-dz)/math.sqrt(2);dw=(db+dz)/math.sqrt(2)
    Ts,Tw=unitary(P,ds),unitary(P,dw)
    residual_s=[u.conj().T@Ts@u@g for u in Us]
    residual_w=[w.conj().T@Tw@w@g for w in Uw]
    target_s=unitary(P,-ds)@g;target_w=unitary(P,-dw)@g
    state_error=max(np.linalg.norm(s-target_s)+np.linalg.norm(w-target_w) for s,w in zip(residual_s,residual_w))
    # Reuse the forward encoder and remove its known branch-dependent phase.
    forward_s=[np.exp(-1j*math.pi*js*js)*u@Ts@u@g for (js,jw),u in zip(forces,Us)]
    forward_w=[np.exp(-1j*math.pi*jw*jw)*w@Tw@w@g for (js,jw),w in zip(forces,Uw)]
    forward_decoder_error=max(np.linalg.norm(s-target_s)+np.linalg.norm(w-target_w) for s,w in zip(forward_s,forward_w))
    # Fe for a maximally entangled 9-level reference uses all 81 coherences.
    fe=sum((np.vdot(residual_s[j],residual_s[i])*np.vdot(residual_w[j],residual_w[i])).real
           for i in range(9) for j in range(9))/81
    rows.append({'cutoff':cutoff,'saddle_height_mean_max_error':height_error,
                 'companion_height_mean_max_error':b_error,
                 'full_two_sector_recovery_max_state_error':float(state_error),
                 'forward_half_period_plus_phase_decoder_max_state_error':float(forward_decoder_error),
                 'nine_label_bell_fidelity':float(fe)})
assert max(rows[-1][s] for s in ('saddle_height_mean_max_error','companion_height_mean_max_error','full_two_sector_recovery_max_state_error'))<1e-11
assert abs(rows[-1]['nine_label_bell_fidelity']-1)<1e-11
assert rows[-1]['forward_half_period_plus_phase_decoder_max_state_error']<1e-11

# Explicit constant-invariant timelike Frenet families exist kinematically.
# This check does not establish their stationarity under the full coupled action.
eta=np.diag([-1.,1.,1.]);frenet_error=0.
for js,jw in forces:
    curvature=math.sqrt(js/mu);torsion=math.sqrt(jw/nu)
    A=np.array([[0.,curvature,0.],[curvature,0.,-torsion],[0.,torsion,0.]])
    frenet_error=max(frenet_error,float(np.max(np.abs(A.T@eta+eta@A))))
assert frenet_error<1e-14

result={'status':'new conditional design; no photonic or full-field derivation claimed',
        'parameters':{'J0':J0,'alpha':alpha,'beta':beta,'k':k,'mu':mu,'nu':nu},
        'labels':locations,'rows':rows,'frenet_metric_preservation_error':frenet_error,
        'discarding_companion_control':{'alpha':.5,'beta':.5,'locations':[[0,0],[1,1]],
           'same_saddle_height':0,'companion_height_gap':1,'gaussian_position_sd':1/math.sqrt(2),
           'bell_fidelity_after_correcting_Z_but_discarding_uncorrected_B':(1+math.exp(-.25))/2},
        'all_checks_passed':True}
(Path(__file__).parent/'two_sector_saddle_bridge_checks.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print(json.dumps(result,indent=2))
