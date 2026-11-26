from pathlib import Path
import json,math
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch,FancyArrowPatch
root=Path(__file__).resolve().parent
out=root/'figures';out.mkdir(exist_ok=True)
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':9,'axes.spines.top':False,'axes.spines.right':False,'axes.grid':True,'grid.alpha':.15,'pdf.fonttype':42,'savefig.bbox':'tight'})
blue,orange,green,gray='#2463A6','#C36C25','#167566','#667085'
def save(fig,name):
    fig.savefig(out/(name+'.pdf'))
    fig.savefig(out/(name+'.png'),dpi=240)
    plt.close(fig)

# 1: the logical path and two auxiliary coordinates are different registers.
fig,ax=plt.subplots(figsize=(7,2.75));ax.set_xlim(0,12.1);ax.set_ylim(-.65,2.8);ax.axis('off')
ys=[2.15,1.2,.25]
for y,label,color in zip(ys,[r'$L$: unknown $\rho$',r'$S$: auxiliary',r'$W$: auxiliary'],[blue,orange,green]):
    ax.text(.02,y+.2,label,color=color,fontsize=8.5)
    ax.plot([.1,11.6],[y,y],color=color,lw=1.4)
for x,w,label,face in [(2.15,1.7,'Coherent\nencoding $E$','#edf4fc'),(4.7,2.0,'Unknown common\ntranslations $N_d$','#f7f8fa'),(7.5,1.7,'Coherent\ndecoding $E^\\dagger$','#edf4fc')]:
    ax.add_patch(FancyBboxPatch((x,-.02),w,2.5,boxstyle='round,pad=0.08',edgecolor=gray,facecolor=face,zorder=3))
    ax.text(x+w/2,1.2,label,ha='center',va='center',fontsize=8.5,zorder=4)
ax.text(11.7,2.15,r'$\rho$',ha='left',va='center',fontsize=12,color=blue)
ax.add_patch(FancyBboxPatch((10.0,-.02),1.5,1.5,boxstyle='round,pad=0.06',edgecolor=gray,facecolor='white',zorder=3))
ax.text(10.75,.7,'Trace out\nS and W',ha='center',va='center',fontsize=8,zorder=4)
ax.text(6,-.52,'The reference system is untouched throughout; no logical label is measured.',ha='center',fontsize=8)
fig.tight_layout();save(fig,'figure_1_registers')

# 2: two generated surfaces, never silently discard the companion coordinate.
x=np.linspace(-1,1,45);X,Y=np.meshgrid(x,x);alpha,beta,J0=.25,.15,.1
Z=alpha*X**2-beta*Y**2;B=-2*np.sqrt(2)*J0-alpha*X**2-beta*Y**2
fig=plt.figure(figsize=(7,3.0))
for i,(V,label) in enumerate([(Z,r'(a) Difference: $h_Z=\alpha x^2-\beta y^2$'),(B,r'(b) Companion: $h_B=-2\sqrt{2}j_0-\alpha x^2-\beta y^2$')]):
    ax=fig.add_subplot(1,2,i+1,projection='3d');ax.plot_surface(X,Y,V,cmap='viridis',alpha=.8,linewidth=0,rstride=2,cstride=2)
    xx,yy=np.meshgrid([-1,0,1],[-1,0,1]);vv=alpha*xx**2-beta*yy**2 if i==0 else -2*np.sqrt(2)*J0-alpha*xx**2-beta*yy**2
    ax.scatter(xx,yy,vv,c='black',s=12,label='Nine tested labels',depthshade=False)
    ax.set(xlabel='Design label x',ylabel='Design label y',zlabel='Displacement');ax.set_title(label,fontsize=8,pad=8);ax.view_init(23,-55);ax.legend(loc='upper left',fontsize=6,frameon=False)
fig.subplots_adjust(left=.0,right=.99,bottom=.03,top=.85,wspace=.18);save(fig,'figure_2_surfaces')

# 3: direct Hamiltonian evolution; all markers and the reference line are keyed.
result=json.loads((root/'numerical'/'forced_oscillator_bridge_checks.json').read_text())
fig,axes=plt.subplots(1,2,figsize=(7,3.0))
t=np.linspace(0,2*np.pi,400)
for J,color in [(-.8,blue),(.3,green),(1.1,orange)]:axes[0].plot(t/np.pi,-J*(1-np.cos(t)),c=color,label=f'J = {J:g}')
axes[0].axvline(1,c=gray,ls=':',label='Half-period')
axes[0].set(xlabel=r'Normalized evolution $t/\pi$',ylabel='Packet mean Q',title='(a) Exact forced-oscillator motion');axes[0].legend(fontsize=7,frameon=False)
rows=result['rows'];ns=[r['fock_cutoff'] for r in rows]
axes[1].semilogy(ns,[r['half_period_formula_max_state_error'] for r in rows],'-o',c=blue,label='Circle: evolution formula')
axes[1].semilogy(ns,[r['common_shift_recovery_max_state_error'] for r in rows],'--s',c=orange,label='Square: decoded state')
axes[1].set(xlabel='Fock basis dimension',ylabel='Maximum state-vector discrepancy',title='(b) Direct matrix checks');axes[1].set_xticks(ns);axes[1].legend(fontsize=7,frameon=False)
for ax in axes:ax.title.set_fontsize(9)
fig.tight_layout();save(fig,'figure_3_dynamics')

# 4: controls are analytic channel values, with explicit labels and no error bars.
fig,axes=plt.subplots(1,2,figsize=(7,3.2))
vals=[1,1,1,.5];labels=['Full two-mode\nrecovery','Same-operation\nconventional','Matched\nflat','Measure logical\nlabel first']
axes[0].bar(range(4),vals,color=[blue,green,gray,orange],width=.63)
axes[0].set_xticks(range(4),labels,rotation=20,ha='right',fontsize=7)
for i,v in enumerate(vals):axes[0].text(i,v+.025,f'{v:g}',ha='center',fontsize=9)
axes[0].set_title('(a) Common-translation channel',loc='left',fontsize=9)
vals=[1,(1+math.exp(-.25))/2,0];labels=['Decode both\nauxiliary modes','Discard uncorrected\ncompanion mode','Uncorrected\nlogical phase pi']
axes[1].bar(range(3),vals,color=[blue,orange,orange],width=.63)
axes[1].scatter([2],[0],color=orange,s=15)
axes[1].set_xticks(range(3),labels,rotation=20,ha='right',fontsize=7)
for i,v in enumerate(vals):axes[1].text(i,v+.025,f'{v:.4f}' if v not in (0,1) else f'{v:g}',ha='center',fontsize=9)
axes[1].set_title('(b) Separate stated controls',loc='left',fontsize=9)
for ax in axes:ax.set_ylim(-.02,1.12);ax.set_ylabel('Bell entanglement fidelity')
fig.tight_layout();save(fig,'figure_4_controls')

# 5: exact error/loss laws. Distinct line styles are labeled, all curves deterministic.
fig,axes=plt.subplots(1,2,figsize=(7,3.0))
gap=np.linspace(0,6,400);axes[0].plot(gap,(1+np.exp(-gap**2/8))/2,c=blue,label='Gaussian residual overlap')
axes[0].set(xlabel=r'Differential gap $|\delta|/\sigma$',ylabel='Bell entanglement fidelity',title='(a) Differential displacement');axes[0].legend(frameon=False,fontsize=7);axes[0].set_ylim(.48,1.02)
sd=np.linspace(0,2,400)
for eta,color,style in [(1,blue,'-'),(.95,green,'--'),(.9,orange,':')]:axes[1].plot(sd,eta*(1+np.exp(-sd*sd/2))/2,color=color,ls=style,label=fr'Transmission $\eta={eta:g}$')
axes[1].set(xlabel=r'Residual phase standard deviation (rad)',ylabel='Unconditional Bell fidelity',title='(b) Phase noise with erasure');axes[1].legend(frameon=False,fontsize=7);axes[1].set_ylim(.48,1.02)
for ax in axes:ax.title.set_fontsize(9)
fig.tight_layout();save(fig,'figure_5_error_limits')
print('Five original figures regenerated in vector PDF and PNG formats.')
