from pathlib import Path
import numpy as np
import json,csv

ROOT=Path(__file__).resolve().parent
def rk4_step(fun,t,y,h):
    k1=fun(t,y);k2=fun(t+h/2,y+h*k1/2);k3=fun(t+h/2,y+h*k2/2);k4=fun(t+h,y+h*k3)
    return y+h*(k1+2*k2+2*k3+k4)/6
def monodromy(omega,n):
    period=2*np.pi/omega;h=period/n;y=np.eye(2)
    def fun(t,Y): return np.array([[0.,1.],[-(.5-.1*np.cos(omega*t)),0.]])@Y
    for i in range(n):y=rk4_step(fun,i*h,y,h)
    return y
res={}
for omega in [np.sqrt(2),2.2]:
    mats=[monodromy(omega,n) for n in [128,256,512,1024]]
    diffs=[float(np.max(np.abs(mats[j+1]-mats[j]))) for j in range(3)]
    eig=np.linalg.eigvals(mats[-1]);rho=max(abs(eig));period=2*np.pi/omega
    res[str(omega)]={'steps':[128,256,512,1024],'monodromy':mats[-1].tolist(),'multipliers':[[float(z.real),float(z.imag)] for z in eig],'spectral_radius':float(rho),'growth_rate':float(np.log(rho)/period),'determinant':float(np.linalg.det(mats[-1])),'successive_matrix_differences':diffs,'observed_orders':[float(np.log2(diffs[i]/diffs[i+1])) for i in range(2)]}
    assert abs(np.linalg.det(mats[-1])-1)<1e-10
assert res[str(np.sqrt(2))]['spectral_radius']>1.1
assert abs(res[str(2.2)]['spectral_radius']-1)<1e-10

# Select the unstable Floquet eigenvector, normalized to a unit initial state.
omega=np.sqrt(2);M=monodromy(omega,1024);vals,vecs=np.linalg.eig(M)
y0=vecs[:,np.argmax(abs(vals))].real;y0/=np.linalg.norm(y0)
if y0[0]<0:y0=-y0
res['resonant_initial_state']=y0.tolist()
dt=.01;count=12000;ys={str(o):y0.copy() for o in [omega,2.2]}
rows=[]
for i in range(count+1):
    t=i*dt
    if i%10==0: rows.append([t,.5+.1*np.cos(omega*t),ys[str(omega)][0],ys[str(omega)][1],ys[str(2.2)][0],ys[str(2.2)][1]])
    for o in [omega,2.2]:
        fun=lambda tt,y,oo=o:np.array([y[1],-(.5-.1*np.cos(oo*tt))*y[0]])
        ys[str(o)]=rk4_step(fun,t,ys[str(o)],dt)
with (ROOT/'Parametric_Response_Data.csv').open('w',newline='') as f:
    w=csv.writer(f);w.writerow(['tau','resonant_r','resonant_eta','resonant_velocity','off_resonant_eta','off_resonant_velocity']);w.writerows(rows)

# Independent algebraic check: arbitrary nonlinear equilibrium Hessian and Schur complement.
rng=np.random.default_rng(72);maxerr=0
for i in range(1000):
    d,a,b=rng.uniform(-2,2,3);B=np.array([[d,a,b],[a,1,0],[b,0,1]])
    exact=np.sort([1,(d+1-np.sqrt((d-1)**2+4*(a*a+b*b)))/2,(d+1+np.sqrt((d-1)**2+4*(a*a+b*b)))/2])
    maxerr=max(maxerr,float(np.max(abs(np.linalg.eigvalsh(B)-exact))))
    if abs(d-a*a-b*b)>1e-8:assert (min(exact)>0)==(d>a*a+b*b)
res['nonlinear_hessian_max_eigenvalue_error']=maxerr
res['instantaneous_r_bounds']=[.4,.6]
(ROOT/'Extended_Numerical_Validation.json').write_text(json.dumps(res,indent=2))
print(json.dumps(res,indent=2))
