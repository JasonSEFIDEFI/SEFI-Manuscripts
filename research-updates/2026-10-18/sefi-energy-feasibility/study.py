"""Deterministic SI-unit engineering model; no new physical interaction.
Run with Python 3. No third-party dependencies. Outputs describe simulations.
"""
from pathlib import Path
import math,json,csv

M=.02; CM=.01; CE=.02; K0=M*(2*math.pi*10)**2
KMIN=M*(2*math.pi*5)**2; KMAX=M*(2*math.pi*15)**2
T=30.; SAMPLE=.05; XMAX=.003; ETA=.8
CONTROL_W=10e-6; SWITCH_J=.1e-6

def source(t,case):
    if case=='steady': f=10.
    elif case=='steps':f=5. if t<10 else (15. if t<20 else 8.)
    else:f=5.+10.*t/T
    amp=.0004 if case=='weak_chirp' else .002
    return f,amp

def run(case,mode,dt=.001,fixed_hz=10.):
    k=M*(2*math.pi*fixed_hz)**2 if mode=='fixed' else K0
    ce=CE; x=v=phase=0.; es=ee=em=wt=release=0.; tuning=0.; switches=0
    lastf=0.;lastcross=None; estimate=10.;maxx=0.;violations=0
    sample_steps=round(SAMPLE/dt)
    for n in range(round(T/dt)):
        t=n*dt; hz,amp=source(t,case)
        force=amp*math.sin(phase)
        # Same directly observed source-force signal for all adaptive policies.
        if lastf<=0<force:
            crossing=t-dt+dt*(-lastf)/(force-lastf)
            if lastcross is not None:
                period=crossing-lastcross
                if period>0: estimate=max(5.,min(15.,1./period))
            lastcross=crossing
        lastf=force
        if mode!='fixed' and n%sample_steps==0:
            target=max(KMIN,min(KMAX,M*(2*math.pi*estimate)**2))
            # The SEFI-labeled policy and matched conventional ablation are
            # mathematically identical. Provenance labels do not alter physics.
            threshold=.01 if mode=='adaptive' else .05
            if abs(target-k)/k>threshold:
                knew=k+max(-5.,min(5.,target-k))
                work=.5*(knew-k)*x*x
                wt+=max(0.,work);release+=max(0.,-work)
                tuning+=max(0.,work)/ETA+SWITCH_J
                k=knew;switches+=1
            ce=.08 if math.hypot(x,v/math.sqrt(k/M))>XMAX else CE
        # Classical RK4, integrating source work and both damping losses.
        def deriv(xx,vv,pp,tt):
            ff,aa=source(tt,case); drive=aa*math.sin(pp)
            return (vv,(drive-(CM+ce)*vv-k*xx)/M,2*math.pi*ff,
                    drive*vv,ce*vv*vv,CM*vv*vv)
        a=deriv(x,v,phase,t)
        b=deriv(x+dt*a[0]/2,v+dt*a[1]/2,phase+dt*a[2]/2,t+dt/2)
        c=deriv(x+dt*b[0]/2,v+dt*b[1]/2,phase+dt*b[2]/2,t+dt/2)
        d=deriv(x+dt*c[0],v+dt*c[1],phase+dt*c[2],t+dt)
        z=[dt*(a[j]+2*b[j]+2*c[j]+d[j])/6 for j in range(6)]
        x+=z[0];v+=z[1];phase+=z[2];es+=z[3];ee+=z[4];em+=z[5]
        maxx=max(maxx,abs(x));violations+=abs(x)>XMAX
    stored=.5*M*v*v+.5*k*x*x
    residual=es+wt-release-ee-em-stored
    standby=0. if mode=='fixed' else CONTROL_W*T
    return dict(case=case,mode=mode,dt_s=dt,fixed_hz=fixed_hz,
        electric_J=ee,source_work_J=es,positive_tuning_work_J=wt,
        released_tuning_energy_J=release,tuning_supply_J=tuning,
        controller_J=standby,net_J=ee-tuning-standby,
        mechanical_loss_J=em,final_stored_J=stored,ledger_residual_J=residual,
        max_displacement_m=maxx,travel_violation_samples=violations,switches=switches)

def main():
    out=Path(__file__).parent
    rows=[]; checks=[]
    for case in ['steady','steps','chirp','weak_chirp']:
        candidates=[run(case,'fixed',fixed_hz=f) for f in [5,7.5,10,12.5,15]]
        fixed=max(candidates,key=lambda r:r['net_J'])
        rows.append(fixed)
        for mode in ['adaptive','event_conventional','sefi_candidate']:
            rows.append(run(case,mode))
        assert rows[-1]['net_J']==rows[-2]['net_J']
        for r in rows[-4:]:
            assert abs(r['ledger_residual_J'])<1e-7
            refined=run(case,r['mode'],dt=.0005,fixed_hz=r['fixed_hz'])
            checks.append(dict(case=case,mode=r['mode'],net_J=r['net_J'],
                refined_net_J=refined['net_J'],absolute_difference_J=abs(r['net_J']-refined['net_J']),
                ledger_residual_J=refined['ledger_residual_J']))
    (out/'results.json').write_text(json.dumps(rows,indent=2))
    (out/'convergence.json').write_text(json.dumps(checks,indent=2))
    with (out/'results.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=rows[0].keys());w.writeheader();w.writerows(rows)
    for r in rows:print(r['case'],r['mode'],'net uJ',round(r['net_J']*1e6,2),'max mm',round(r['max_displacement_m']*1000,3),'ledger J',r['ledger_residual_J'])
    print('max refinement difference uJ',max(c['absolute_difference_J'] for c in checks)*1e6)

if __name__=='__main__':main()
