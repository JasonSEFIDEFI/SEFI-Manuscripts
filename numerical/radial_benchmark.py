"""Radial single-complex-scalar numerical benchmark using an established Q-ball potential.

U(rho)=rho-rho**2+rho**3/3. This is an additional trial action, not a
derived shared-field law. All coordinates and coefficients are dimensionless.
"""
from pathlib import Path
import math,json,numpy as np

def force(f,omega):return (1-omega*omega)*f-2*f**3+f**5

def shoot(f0,omega,h=.01,limit=50.):
    f=f0+h*h*force(f0,omega)/6;p=h*force(f0,omega)/3;r=h
    rs=[0.,r];fs=[f0,f]
    def rhs(r,f,p):return p,force(f,omega)-2*p/r
    while r<limit:
        if f<0:return -1,np.array(rs),np.array(fs)
        if p>0 and r>.1:return 1,np.array(rs),np.array(fs)
        if f<1e-6 and p<0:return 0,np.array(rs),np.array(fs)
        a,b=rhs(r,f,p);c,d=rhs(r+h/2,f+h*a/2,p+h*b/2);e,g=rhs(r+h/2,f+h*c/2,p+h*d/2);u,v=rhs(r+h,f+h*e,p+h*g)
        f+=h*(a+2*c+2*e+u)/6;p+=h*(b+2*d+2*g+v)/6;r+=h
        rs.append(r);fs.append(f)
        if abs(f)>10:return 1,np.array(rs),np.array(fs)
    return 1,np.array(rs),np.array(fs)

def seed(omega):
    lo=math.sqrt(1-omega)+1e-7;hi=math.sqrt(1+omega)-1e-7
    sl,*_=shoot(lo,omega);sh,*_=shoot(hi,omega)
    if sl==sh:raise ValueError(('No overshoot/undershoot bracket',omega,sl,sh))
    best=None
    for _ in range(60):
        mid=(lo+hi)/2;sign,r,f=shoot(mid,omega)
        if best is None or f[-1]<best[2][-1]:best=(mid,r,f)
        if sign==0:return mid,r,f
        if sign==sl:lo=mid
        else:hi=mid
    return best

def tridiagonal(lower,diag,upper,rhs):
    d=diag.copy();b=rhs.copy();n=len(d)
    for i in range(1,n):
        factor=lower[i-1]/d[i-1];d[i]-=factor*upper[i-1];b[i]-=factor*b[i-1]
    x=np.zeros(n);x[-1]=b[-1]/d[-1]
    for i in range(n-2,-1,-1):x[i]=(b[i]-upper[i]*x[i+1])/d[i]
    return x

def solve(omega=.8,h=.025,R=30.,initial=None):
    n=round(R/h);r=np.arange(n+1)*h
    if initial is None:
        f0,rs,fs=seed(omega);fs=np.maximum(fs,1e-12);f=np.interp(r,rs,fs)
        tail=r>rs[-1];f[tail]=fs[-1]*rs[-1]/r[tail]*np.exp(-math.sqrt(1-omega*omega)*(r[tail]-rs[-1]))
    else:f=np.interp(r,initial[0],initial[1])
    f[-1]=0
    lower=np.full(n-1,1/h**2)-1/(r[1:n]*h)
    # Upper[i] connects row i to i+1, so its interior coordinates start at r[1].
    upper=np.r_[6/h**2,1/h**2+1/(r[1:n-1]*h)]
    diag=np.full(n,-2/h**2);diag[0]=-6/h**2
    def residual(f):
        z=diag*f[:-1];z[1:]+=lower*f[:-2];z[:-1]+=upper*f[1:-1]
        return z-force(f[:-1],omega)
    history=[]
    for _ in range(60):
        F=residual(f);err=float(abs(F).max());history.append(err)
        if err<2e-9:break
        J=diag-(1-omega*omega)+6*f[:-1]**2-5*f[:-1]**4
        delta=tridiagonal(lower,J,upper,-F);step=1.
        while step>1e-7:
            trial=f.copy();trial[:-1]+=step*delta
            if np.linalg.norm(residual(trial))<np.linalg.norm(F) and trial.min()>-1e-8:break
            step*=.5
        if step<=1e-7:break
        f=trial
    err=float(abs(residual(f)).max())
    if err>2e-7 or f.max()<.3 or np.any(f<-1e-8):raise RuntimeError(('Profile solve failed',omega,h,R,err,float(f.max()),history))
    fp=np.gradient(f,h,edge_order=2);fp[0]=0
    integ=lambda a:float(4*np.pi*np.trapezoid(r*r*a,r))
    rho=f*f;I=integ(rho);K=integ(fp*fp);U=integ(rho-rho*rho+rho**3/3);Q=2*omega*I;E=omega*omega*I+K+U
    virial=K+3*U-3*omega*omega*I
    return r,f,dict(omega=omega,h=h,R=R,residual=err,peak=float(f[0]),I=I,gradient_energy=K,potential_energy=U,energy=E,orientation_charge=Q,energy_per_orientation_charge=E/Q,virial=virial,relative_virial=abs(virial)/(K+3*U+3*omega*omega*I),iterations=len(history),history=history)

if __name__=='__main__':
    root=Path(__file__).resolve().parent;runs=[];last=None
    for h in [.1,.05,.025]:
        r,f,data=solve(.8,h,30.,last);last=(r,f);runs.append(data);print(json.dumps(data),flush=True)
        np.savez(root/f'localized_w080_h{h:g}.npz',r=r,f=f)
        if h==.025:np.savez(root/'radial-profile.npz',r=r,f=f)
    r,f,data=solve(.8,.025,40.,last);runs.append(data);np.savez(root/'localized_w080_R40.npz',r=r,f=f);print('Domain check',json.dumps(data),flush=True)
    branches=[]
    for w in [.78,.8,.82]:
        r,f,data=solve(w,.05,30.);branches.append(data);print('Branch',json.dumps(data),flush=True)
    report=dict(trial_potential='U(rho)=rho-rho^2+rho^3/3',scope='Numerical stationary local scalar benchmark; no experimental measurements or common microscopic derivation asserted.',analytic_frequency_window=[.5,1.],runs=runs,branch=branches,branch_charge_slope=(branches[2]['orientation_charge']-branches[0]['orientation_charge'])/.04,warning='The existence of a finite-domain profile, its E/Q ratio, or a charge-slope diagnostic does not by itself establish full nonlinear stability.')
    (root/'radial-results.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
