"""Independent full-state checks of the integrated channel and timing assumptions."""
from pathlib import Path
import json,math
import numpy as np
rng=np.random.default_rng(20261125)
records=[]
def check(name,error,tolerance):
    error=float(error);assert error<=tolerance,(name,error,tolerance)
    records.append(dict(name=name,error=error,tolerance=tolerance))
def unitary(n):
    q,r=np.linalg.qr(rng.normal(size=(n,n))+1j*rng.normal(size=(n,n)))
    return q@np.diag(np.diag(r)/abs(np.diag(r)))
def packet(n):
    v=rng.normal(size=n)+1j*rng.normal(size=n);return v/np.linalg.norm(v)
def density(v):return np.outer(v,v.conj())
def tr_aux(rho,d,n):return np.trace(rho.reshape(d,n,d,n),axis1=1,axis2=3)
d,n,k=3,5,4
E=[unitary(n) for _ in range(d)];W=[[unitary(n) for _ in range(d)] for _ in range(k)]
weights=np.array([.1,.2,.3,.4]);g=packet(n)
controlled=lambda ops:sum(np.kron(np.diag(np.eye(d)[b]),ops[b]) for b in range(d))
enc=controlled(E)
decoded=[];res=[]
for j in range(k):
    U=enc.conj().T@controlled(W[j])@enc;decoded.append(U)
    res.append([e.conj().T@w@e@g for e,w in zip(E,W[j])])
gram=sum(w*np.array([[np.vdot(states[c],states[b]) for c in range(d)] for b in range(d)]) for w,states in zip(weights,res))
rho=density(packet(d));full=sum(w*(U@np.kron(rho,density(g))@U.conj().T) for w,U in zip(weights,decoded))
check('explicit encoded-noisy-decoded density versus residual Gram channel',np.max(abs(tr_aux(full,d,n)-rho*gram)),2e-14)
# An independent full reference x logical x auxiliary simulation.
bell=np.eye(d).reshape(-1)/np.sqrt(d);rho_ref=np.kron(density(bell),density(g))
final=sum(w*(np.kron(np.eye(d),U)@rho_ref@np.kron(np.eye(d),U.conj().T)) for w,U in zip(weights,decoded))
reduced=tr_aux(final,d*d,n);fe=float(np.vdot(bell,reduced@bell).real)
disp=sum(w*sum(np.linalg.norm(v-z)**2 for v in states for z in states)/(2*d*d) for w,states in zip(weights,res))
check('full reference-state fidelity versus Gram trace',abs(fe-np.sum(gram).real/d**2),2e-14)
check('full reference-state fidelity deficit versus residual dispersion',abs(1-fe-disp),2e-14)
check('reduced reference-state trace',abs(np.trace(reduced)-1),2e-14)
assert np.linalg.eigvalsh(reduced).min()>-2e-14
# Same auxiliary density matrices do not imply the identity if their vectors differ in phase.
theta=.7;states=[g,np.exp(1j*theta)*g]
check('phase-only residual density equality',np.max(abs(density(states[0])-density(states[1]))),2e-14)
phase_fe=float(sum(np.vdot(v,z).real for v in states for z in states)/4)
check('phase-only logical fidelity',abs(phase_fe-(1+np.cos(theta))/2),2e-14)
assert phase_fe<.9
# Nonzero-mean, rank-one Gaussian displacement: quadrature and characteristic function.
omega=np.array([1.,2.]);forcegap=np.array([.7,-.2]);t=.63
ell=forcegap*np.sin(omega*t)/omega
mean=np.array([.2,-.1]);direction=np.array([.3,.15]);cov=np.outer(direction,direction)
xs,ws=np.polynomial.hermite.hermgauss(24)
quadrature=sum(w*np.exp(1j*(mean+np.sqrt(2)*x*direction)@ell) for x,w in zip(xs,ws))/np.sqrt(np.pi)
exact=np.exp(1j*mean@ell-.5*ell@cov@ell)
check('singular Gaussian covariance and nonzero mean',abs(quadrature-exact),2e-14)
check('known mean-phase compensation',abs(quadrature*np.exp(-1j*mean@ell)-np.exp(-.5*ell@cov@ell)),2e-14)
# Matched inverse timing law cannot be assigned to a nominal forward-phase decoder.
N=40;a=np.diag(np.sqrt(np.arange(1,N)),1);Q=(a+a.T)/np.sqrt(2)
g0=np.zeros(N,dtype=complex);g0[0]=1/np.sqrt(2);g0[2]=1j/np.sqrt(2)
forces=[-.35,.45]
def evolution(J,time):
    e,v=np.linalg.eigh(np.diag(np.arange(N))+J*Q)
    return (v*np.exp(-1j*time*e))@v.conj().T
timing_controls=[]
for delta in [0.,.12]:
    t=math.pi+delta;ops=[evolution(J,t) for J in forces]
    matched=[U.conj().T@U@g0 for U in ops]
    nominal=[np.exp(-1j*math.pi*J*J)*U@U@g0 for J,U in zip(forces,ops)]
    fidelity=lambda s:float(sum(np.vdot(v,z).real for v in s for z in s)/4)
    fm,fn=fidelity(matched),fidelity(nominal)
    check('matched inverse with zero noise at offset '+str(delta),abs(fm-1),2e-13)
    if delta==0:check('forward-phase synthesis at nominal half-period',abs(fn-1),2e-13)
    else:assert fn<1-1e-5
    timing_controls.append(dict(delta=delta,matched_inverse_fidelity=fm,nominal_forward_phase_fidelity=fn))
out=dict(all_passed=True,check_count=len(records),checks=records,timing_decoder_controls=timing_controls,scope='Deterministic full-state and quadrature checks; no experimental measurements.')
(Path(__file__).parent/'integrated_recovery_checks.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
print(json.dumps(out,indent=2))
