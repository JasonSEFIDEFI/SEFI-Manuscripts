"""Check a conditional quantum realization of the source's forced oscillator.

This does not quantize the complete higher-derivative worldline theory.
Assumptions: fixed independent logical labels, constant oscillator parameters,
controlled branch-dependent force, canonical oscillator quantization, and an
available inverse encoding operation. No optical realization is asserted.
"""
from pathlib import Path
import numpy as np
import json,math

def unitary(H,t):
    e,v=np.linalg.eigh(H)
    return (v*np.exp(-1j*t*e))@v.conj().T

rows=[]
for cutoff in (20,40,60):
    a=np.diag(np.sqrt(np.arange(1,cutoff)),1)
    Q=(a+a.T)/np.sqrt(2);P=(a-a.T)/(1j*np.sqrt(2))
    H0=np.diag(np.arange(cutoff,dtype=float)) # zero-point energy removed
    parity=np.diag((-1.)**np.arange(cutoff))
    g=np.zeros(cutoff,dtype=complex);g[0]=1/np.sqrt(2);g[2]=1j/np.sqrt(2)
    forces=(-.8,.3,1.1);enc=[];formula_errors=[]
    for J in forces:
        U=unitary(H0+J*Q,math.pi)
        expected=np.exp(1j*math.pi*J*J/2)*unitary(P,-2*J)@parity
        formula_errors.append(float(np.linalg.norm((U-expected)@g)))
        enc.append(U)
    d=.4;noise=unitary(P,d)
    residuals=[U.conj().T@noise@U@g for U in enc]
    target=unitary(P,-d)@g
    residual_error=max(float(np.linalg.norm(v-target)) for v in residuals)
    n=len(enc)
    bell_fidelity=float(sum(np.vdot(v,w).real for v in residuals for w in residuals)/(n*n))
    rows.append({'fock_cutoff':cutoff,'half_period_formula_max_state_error':max(formula_errors),
                 'common_shift_recovery_max_state_error':residual_error,
                 'three_label_bell_fidelity':bell_fidelity})
assert rows[-1]['half_period_formula_max_state_error']<1e-11
assert rows[-1]['common_shift_recovery_max_state_error']<1e-11
assert abs(rows[-1]['three_label_bell_fidelity']-1)<1e-11
result={'status':'new conditional quantum extension of prescribed-geometry oscillator; not full proposed model quantization',
        'units':'hbar=mass=frequency=1, zero-point energy removed',
        'forces':list(forces),'common_height_shift':d,'rows':rows,'all_checks_passed':True}
(Path(__file__).parent/'forced_oscillator_bridge_checks.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print(json.dumps(result,indent=2))
