"""Independent checks of final driven-response and DNA energy calculations."""
from pathlib import Path
import json, math
import numpy as np
R=Path(__file__).resolve().parent
def step(t,y,h,omega):
    def f(t,y):return np.array([y[1],-(.5-.1*np.cos(omega*t))*y[0]])
    a=f(t,y);b=f(t+h/2,y+h*a/2);c=f(t+h/2,y+h*b/2);d=f(t+h,y+h*c)
    return y+h*(a+2*b+2*c+d)/6
V=json.loads((R/'Extended_Numerical_Validation.json').read_text())
y0=np.array(V['resonant_initial_state']);omega=np.sqrt(2);period=2*np.pi/omega
M=np.array(V[str(omega)]['monodromy']);vals=np.linalg.eigvals(M);rho=vals[np.argmax(abs(vals))]
y=y0.copy();error=0.
for n in range(1,28):
    h=period/1024
    for j in range(1024):y=step(((n-1)*1024+j)*h,y,h,omega)
    exact=rho**n*y0;error=max(error,float(np.linalg.norm(y-exact)/np.linalg.norm(exact)))
maxerr=0.
for drive in [omega,2.2]:
    coarse=y0.copy();fine=y0.copy()
    for i in range(12000):
        t=i*.01;coarse=step(t,coarse,.01,drive)
        fine=step(t,fine,.005,drive);fine=step(t+.005,fine,.005,drive)
        if (i+1)%10==0:maxerr=max(maxerr,float(np.linalg.norm(coarse-fine)/max(1,np.linalg.norm(fine))))
assert error<1e-10 and maxerr<1e-8
# Finite differences independently check constant DNA mismatch: old energy varies,
# whereas the modified oscillator energy is conserved.
alpha=1.7;lam=.4;delta=.3;freq=np.sqrt(1+2*lam*delta**2);t=.71;h=1e-5
def state(t):return np.cos(freq*t),-freq*np.sin(freq*t)
def energy(t,modified):
    x,v=state(t);return alpha/2*(v*v+(freq**2 if modified else 1)*x*x)
x,v=state(t);old_derivative=(energy(t+h,False)-energy(t-h,False))/(2*h)
predicted=-2*alpha*lam*delta**2*x*v
new_derivative=(energy(t+h,True)-energy(t-h,True))/(2*h)
assert abs(old_derivative-predicted)<1e-9 and abs(new_derivative)<1e-9
result={'floquet_27_period_relative_error':error,'step_halving_relative_error':maxerr,
        'dna_old_energy_derivative_error':abs(old_derivative-predicted),
        'dna_modified_energy_derivative':new_derivative,'passed':True}
(R/'Independent_Final_Checks.json').write_text(json.dumps(result,indent=2))
print(json.dumps(result,indent=2))
