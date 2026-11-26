"""Independent finite checks for the author draft. No experimental data.
Run with Python and NumPy. The mathematical proofs are in main.tex.
"""
from pathlib import Path
import itertools,json,math,platform
import numpy as np
root=Path(__file__).resolve().parent
rng=np.random.default_rng(20261123);records=[]
def check(name,error,tolerance):
    error=float(error);assert error<=tolerance,(name,error,tolerance)
    records.append(dict(name=name,error=error,tolerance=tolerance,passed=True))
def unitary(n):
    z=rng.normal(size=(n,n))+1j*rng.normal(size=(n,n));return np.linalg.qr(z)[0]
# Real-linear conjugate embedding, energy and the two currents.
psi=rng.normal(size=40)+1j*rng.normal(size=40)
der=rng.normal(size=40)+1j*rng.normal(size=40)
pair=np.stack([psi,psi.conj()],axis=-1)/np.sqrt(2)
dpair=np.stack([der,der.conj()],axis=-1)/np.sqrt(2)
check('conjugate embedding amplitude identity',np.max(abs(np.sum(abs(pair)**2,axis=1)-abs(psi)**2)),1e-13)
check('conjugate embedding derivative norm',np.max(abs(np.sum(abs(dpair)**2,axis=1)-abs(der)**2)),1e-13)
j=lambda z,d:1j*(z.conj()*d-d.conj()*z)
check('common-phase current vanishes',np.max(abs(np.sum(j(pair,dpair),axis=1))),1e-13)
check('orientation current equals scalar current',np.max(abs(j(pair[:,0],dpair[:,0])-j(pair[:,1],dpair[:,1])-j(psi,der))),1e-13)
check('complex superposition leaves the real constraint',np.linalg.norm((1j*pair)[:,::-1].conj()+1j*pair),1e-13)
# History amplitudes: three sites, three layers, every path allowed.
m=3;U=[unitary(m) for _ in range(3)];c=rng.normal(size=m)+1j*rng.normal(size=m);c/=np.linalg.norm(c)
direct=U[2]@U[1]@U[0]@c;history=np.zeros(m,dtype=complex)
for path in itertools.product(range(m),repeat=4):
    value=c[path[0]]
    for k in range(3):value*=U[k][path[k+1],path[k]]
    history[path[-1]]+=value
check('finite history expansion',np.max(abs(direct-history)),1e-13)
R=[np.diag(np.exp(1j*rng.normal(size=m))) for _ in range(4)]
changed=[R[k+1]@U[k]@R[k].conj().T for k in range(3)]
check('basis rephasing readout invariance',np.max(abs(abs(changed[2]@changed[1]@changed[0]@R[0]@c)**2-abs(direct)**2)),1e-13)
# Positive internal matrix, Schur coefficient and Fourier-band bound.
worst=0
for _ in range(150):
    a,b=rng.uniform(-.5,.5,2);r=np.hypot(a,b);K=np.array([[1,0,0,0],[0,1,a,b],[0,a,1,0],[0,b,0,1.]])
    checkerr=max(abs(np.linalg.eigvalsh(K)-np.sort([1,1,1-r,1+r])))
    assert checkerr<1e-13
    h=rng.normal(size=4);mu=1.7;G=h@np.linalg.solve(mu*mu*K,h)
    closed=(h[0]**2+h[2]**2+h[3]**2+(h[1]-a*h[2]-b*h[3])**2/(1-r*r))/(mu*mu)
    worst=max(worst,abs(G-closed))
    q=rng.uniform(-.4,.4)*mu*mu*(1-r);delta=abs(q)/(mu*mu*(1-r));Gq=h@np.linalg.solve(mu*mu*K+q*np.eye(4),h)
    assert abs(Gq-G)<=delta/(1-delta)*G+1e-12
check('Schur response and 150 spectral-band samples',worst,1e-12)
# An arbitrary controlled encoder gives the residual-state Gram channel.
d=3;n=7;E=[unitary(n) for _ in range(d)];W=unitary(n);g=rng.normal(size=n)+1j*rng.normal(size=n);g/=np.linalg.norm(g)
chi=[e.conj().T@W@e@g for e in E]
gram=np.array([[np.vdot(chi[c],chi[b]) for c in range(d)] for b in range(d)])
fe=np.sum(gram).real/d**2
disp=sum(np.linalg.norm(chi[b]-chi[c])**2 for b in range(d) for c in range(d))/(2*d*d)
check('exact residual-state dispersion identity',abs(1-fe-disp),1e-13)
assert np.linalg.eigvalsh(gram).min()>-1e-12
# Exact finite cyclic common-translation recovery, including off-diagonals.
bins=11;labels=list(itertools.product([-1,0,1],repeat=2));heights=[(x*x-y*y)%bins for x,y in labels]
for shift in range(bins):
    residual=[((h+shift)%bins-h)%bins for h in heights]
    for b in range(9):
        for c in range(9):assert residual[b]==residual[c]
check('891 finite matrix-unit common-shift identities',0,0)
# Direct matrix-exponential timing check, no state-space translation formula assumed.
def hermitian_exp(H,t):
    e,v=np.linalg.eigh(H);return (v*np.exp(-1j*t*e))@v.conj().T
def oscillator(N):
    a=np.diag(np.sqrt(np.arange(1,N)),1);Q=(a+a.T)/np.sqrt(2);P=(a-a.T)/(1j*np.sqrt(2));return np.diag(np.arange(N)),Q,P
N,Q,P=oscillator(50);g=np.zeros(50,dtype=complex);g[0]=1/np.sqrt(2);g[2]=1j/np.sqrt(2)
forces=[-.35,.45];noise_sd=.3;xs,ws=np.polynomial.hermite.hermgauss(14);xs=np.sqrt(2)*noise_sd*xs;ws=ws/np.sqrt(np.pi)
translations=[hermitian_exp(P,float(x)) for x in xs]
timing=[]
for t in [math.pi,math.pi+.03,math.pi+.12,math.pi+.3]:
    operators=[hermitian_exp(N+J*Q,t) for J in forces]
    overlap=0j
    for x,w,T in zip(xs,ws,translations):
        states=[E.conj().T@T@E@g for E in operators];overlap+=w*np.vdot(states[1],states[0])
    variance=(forces[0]-forces[1])**2*np.sin(t)**2*noise_sd**2
    exact=np.exp(-variance/2);check('forced evolution timing kernel at t='+format(t,'.5f'),abs(overlap-exact),3e-12)
    timing.append(dict(time=t,delta=t-math.pi,variance=variance,kernel=float(exact),entanglement_fidelity=float((1+exact)/2),direct_kernel_real=float(overlap.real)))
# Unequal frequencies: full-rank Gaussian noise is corrected at common turning times.
omega=np.array([1.,2.]);times=[math.pi,.5*math.pi]
deltaJ=np.array([.6,.4]);cov=np.diag([.09,.16])
for t in times:
    ell=deltaJ*np.sin(omega*t)/omega;variance=ell@cov@ell
    assert (variance<1e-25) if t==math.pi else variance>.001
check('commensurate unequal-frequency turning criterion',0,0)
# Explicit ordinary invariants and positive representation benchmark.
Nlist=[1,2,4,8,16];quad=[]
for n in Nlist:
    x=(np.arange(160000)+.5)/160000;centers=(np.arange(n)+.5)/n
    distances=abs(x[:,None]-centers[None,:]);distances=np.minimum(distances,1-distances)
    value=np.min(distances,axis=1).mean();quad.append(dict(N=n,quadrature=float(value),exact=1/(4*n)))
    assert abs(value-1/(4*n))<1e-10
check('uniform-circle spatial quantization quadrature',max(abs(q['quadrature']-q['exact']) for q in quad),1e-10)
R=10.5;pitch=34;b=pitch/(2*math.pi);kappa=R/(R*R+b*b);tau=b/(R*R+b*b)
check('helix invariant ratio',abs(kappa/tau-2*math.pi*R/pitch),1e-14)
for t in [.5,1,2,5]:
    mass=1.3;energy=2*mass*mass/t**2+1/t**4;pressure=1/t**4;der=-4*mass*mass/t**3-4/t**5
    assert abs(der+2/t*(energy+pressure))<1e-10
check('prescribed expansion energy continuity',0,0)
report=dict(seed=20261123,python=platform.python_version(),numpy=np.__version__,checks=records,check_count=len(records),all_passed=True,timing=timing,quantization=quad,scope='Deterministic checks of explicit mathematical examples; no experimental data or particle identification.')
(root/'model-verification.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps({'all_passed':True,'check_count':len(records),'timing':timing},indent=2))
