"""Noise audit of the candidate optical mapping; no apparatus data are used."""
from pathlib import Path
import json,math
import numpy as np

def unitary(H,t):
    e,v=np.linalg.eigh(H)
    return (v*np.exp(-1j*t*e))@v.conj().T

cutoff=50
a=np.diag(np.sqrt(np.arange(1,cutoff)),1)
Q=(a+a.T)/math.sqrt(2);P=(a-a.T)/(1j*math.sqrt(2))
N=np.diag(np.arange(cutoff,dtype=float))
g=np.zeros(cutoff,dtype=complex);g[0]=1/math.sqrt(2);g[2]=1j/math.sqrt(2)
alpha,beta,J0=.25,.15,.1
labels=[(1.,0.),(0.,1.)]
forces=np.array([(J0+alpha*x*x/math.sqrt(2),J0+beta*y*y/math.sqrt(2)) for x,y in labels])
heights=-2*forces
delta=heights[0]-heights[1]
U=[[unitary(N+forces[b,axis]*Q,math.pi) for axis in range(2)] for b in range(2)]
mom=np.array([.17,-.23]);shift=np.array([.3,-.2])
res=[]
for b in range(2):
    res.append([U[b][axis].conj().T@unitary(P,shift[axis])@unitary(Q,-mom[axis])@U[b][axis]@g for axis in range(2)])
coherence=np.vdot(res[1][0],res[0][0])*np.vdot(res[1][1],res[0][1])
expected=np.exp(1j*float(mom@delta))
operator_error=float(abs(coherence-expected))
assert operator_error<1e-11

# Zero-mean joint Gaussian path phase theta and tilt k, with physical covariances
# specified as INPUTS. Independent and correlated cases remain labeled separately.
C=np.eye(2)*.04;phase_variance=.01
v_added=float(delta@C@delta)
score=lambda eta,v:eta*(1+math.exp(-v/2))/2
independent={'theta_variance':phase_variance,'tilt_added_variance':v_added,
             'equal_transmission':.95,
             'flat_fidelity_equal_transmission':score(.95,phase_variance),
             'saddle_fidelity_equal_transmission':score(.95,phase_variance+v_added),
             'saddle_fidelity_with_transmission_0_90':score(.90,phase_variance+v_added)}

# Numerical Gaussian integration cross-check of exp[-Var(theta+k.Delta)/2].
nodes,weights=np.polynomial.hermite.hermgauss(16)
avg=0.
for i,x in enumerate(nodes):
    for j,y in enumerate(nodes):
        for ell,z in enumerate(nodes):
            theta=math.sqrt(2*phase_variance)*x
            kk=np.sqrt(.08)*np.array([y,z])
            avg+=weights[i]*weights[j]*weights[ell]*math.cos(theta+float(kk@delta))/(math.pi**1.5)
quadrature_error=abs(avg-math.exp(-(phase_variance+v_added)/2))
assert quadrature_error<1e-12

# A counterexample to a broader no-advantage claim: an assumed anti-correlation
# can make encoding compensate a phase. This covariance is not derived or measured.
# theta=-k.Delta+epsilon, epsilon independent with variance .01.
correlated={'status':'illustrative assumed correlation; not a prediction',
            'theta_variance':phase_variance+v_added,
            'cov_theta_tilt':list(-C@delta),
            'residual_variance_saddle':phase_variance,
            'flat_conditional_fidelity':score(1,phase_variance+v_added),
            'saddle_conditional_fidelity':score(1,phase_variance),
            'minimum_encoded_to_flat_transmission_ratio_for_benefit':score(1,phase_variance+v_added)/score(1,phase_variance)}

# Uniform erasure channel: verify trace-preservation and Bell overlap on an
# explicit reference-qubit x (qubit + vacuum) output density matrix.
eta=.91;v=.13;kappa=math.exp(-v/2)
rho=np.zeros((6,6),dtype=complex)
# ordering ref*3+out, with out 2 denoting vacuum
rho[0,0]=rho[4,4]=eta/2
rho[0,4]=rho[4,0]=eta*kappa/2
rho[2,2]=rho[5,5]=(1-eta)/2
bell=np.zeros(6);bell[0]=bell[4]=1/math.sqrt(2)
overlap=bell@rho@bell
assert abs(overlap.imag)<1e-14
erasure_error=abs(float(overlap.real)-score(eta,v))
assert abs(np.trace(rho)-1)<1e-12 and np.linalg.eigvalsh(rho).min()>-1e-12 and erasure_error<1e-12

result={'status':'conditional noise calculation; normalized synthetic parameters, not laboratory measurements',
        'operator_coherence_error':operator_error,'gaussian_quadrature_error':quadrature_error,
        'explicit_erasure_channel_formula_error':erasure_error,
        'delta_heights_SW':list(delta),'independent_noise_example':independent,
        'correlated_control':correlated,'all_checks_passed':True}
(Path(__file__).parent/'phase_loss_boundary_checks.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print(json.dumps(result,indent=2))
