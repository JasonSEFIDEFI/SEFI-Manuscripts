"""Vector diagrams and source-based field/timing plots with embedded fonts."""
from pathlib import Path
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
root=Path(__file__).resolve().parent;out=root/'figures'
navy,teal,gold,gray='#16334C','#007E87','#A3662D','#69757F'
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':9,'pdf.fonttype':42,'axes.spines.top':False,'axes.spines.right':False})
def save(fig,name):
    fig.savefig(out/(name+'.pdf'),bbox_inches='tight');fig.savefig(out/(name+'.png'),dpi=300,bbox_inches='tight');plt.close(fig)
fig,ax=plt.subplots(figsize=(7,2.8));ax.set(xlim=(0,12),ylim=(0,4.5));ax.axis('off')
def box(x,y,title,lines):
    ax.add_patch(FancyBboxPatch((x,y),3.45,1.45,boxstyle='round,pad=.1',facecolor='#F3F7FA',edgecolor='#CEDBE2'))
    ax.text(x+.12,y+1.06,title,fontsize=9,weight='bold',color=navy)
    ax.text(x+.12,y+.72,'\n'.join(lines),fontsize=7.5,color=gray,va='top',linespacing=1.5)
for x,title,lines in [(0.15,'One complex scalar',['Action, current and energy','Constrained conjugate pair']),(4.25,'Internal response',['Additional mediator fields','Positive stiffness spectrum']),(8.35,'Localized configuration',['Nonlinear scalar benchmark','Numerical refinement'])]:box(x,2.8,title,lines)
for x,title,lines in [(0.15,'Coherent mode register',['Complex amplitudes and readout','Additional quantum assumptions']),(4.25,'Controlled auxiliaries',['Oscillator phase and parity','Difference and companion']),(8.35,'Recovery criterion',['Identical residual vectors','Unknown coherence retained'])]:box(x,.15,title,lines)
for y in [3.52,.88]:
    for x in [3.72,7.82]:ax.annotate('',(x+.43,y),(x,y),arrowprops={'arrowstyle':'->','color':gray,'lw':1})
ax.plot([.2,11.8],[2.28,2.28],color='#CEDBE2',lw=.8)
ax.text(6,1.99,'Separate model definitions: the quantum construction is not derived from the scalar model.',ha='center',fontsize=7.4,color=gray)
fig.tight_layout();save(fig,'model-structure')
profile=np.load(root/'numerical/radial-profile.npz')
fig,axes=plt.subplots(1,2,figsize=(7,2.7))
mask=profile['r']<=12;axes[0].plot(profile['r'][mask],profile['f'][mask],c=teal,lw=1.8)
axes[0].set(xlabel='Spatial radius r',ylabel='Scalar profile f(r)',title='(a) Local stationary scalar benchmark',xlim=(0,12))
r=np.linspace(0,.99,200)
for values,c,style,label in [(1-r,teal,'-','Lower: 1 - r'),(np.ones_like(r),gray,':','Double unit branch: 1'),(1+r,gold,'--','Upper: 1 + r')]:axes[1].plot(r,values,c=c,ls=style,label=label,lw=1.6)
axes[1].set(xlabel='Internal coupling radius r',ylabel='Stiffness eigenvalue',title='(b) Internal linear spectrum',xlim=(0,1),ylim=(0,2));axes[1].legend(frameon=False,fontsize=7)
for a in axes:a.grid(alpha=.15);a.title.set_fontsize(9)
fig.tight_layout();save(fig,'localization-spectrum')
data=json.loads((root/'numerical/model-verification.json').read_text())
x=np.linspace(0,.4,400);exact=(1+np.exp(-.5*(.8*.3*np.sin(x))**2))/2;quad=1-(.8*.3*x)**2/4
fig,ax=plt.subplots(figsize=(7,2.8))
ax.plot(x,exact,c=teal,lw=1.8,label='Exact Gaussian translation law')
ax.plot(x,quad,c=navy,lw=1.2,ls='--',label='Local quadratic approximation')
ax.scatter([row['delta'] for row in data['timing']],[(1+row['direct_kernel_real'])/2 for row in data['timing']],c=gold,s=25,zorder=4,label='Direct 50-level oscillator calculation')
ax.set(xlabel=r'Matched encoding-time offset $\delta t$ ($\hbar=\omega_0=1$)',ylabel=r'Entanglement fidelity $F_{\mathrm{e}}$',xlim=(-.006,.405),ylim=(.9975,1.00014))
ax.ticklabel_format(axis='y',style='plain',useOffset=False);ax.grid(alpha=.18);ax.legend(frameon=False,fontsize=7.5,loc='lower left')
fig.tight_layout();save(fig,'saddle-timing')
print('Generated three vector figures with embedded fonts and fully keyed timing curves.')

