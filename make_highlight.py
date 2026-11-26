"""Original analytic artwork and recorded timing results; no experimental data."""
from pathlib import Path
import json, hashlib
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
from PIL import Image

root=Path(__file__).resolve().parent
data_path=root/'numerical/model-verification.json'
data=json.loads(data_path.read_text())
assert data['all_passed']
navy,teal,gold,gray='#16334C','#007E87','#A3662D','#596C79'
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':9,'mathtext.fontset':'dejavusans','pdf.fonttype':42,'svg.fonttype':'none','axes.spines.top':False,'axes.spines.right':False})
fig=plt.figure(figsize=(8.0139,6.2739),facecolor='white')
bg=fig.add_axes([0,0,1,1]);bg.axis('off');bg.set(xlim=(0,1),ylim=(0,1))
def txt(x,y,s,size=10,**kwargs):
    bg.text(x,y,s,fontsize=size,color=kwargs.pop('color',navy),transform=bg.transAxes,**kwargs)
txt(.055,.943,'Coherent saddle recovery',20,weight='bold')
txt(.055,.897,'Residual-state criteria and quantitative timing limits',12)
bg.plot([.055,.945],[.865,.865],color='#CBD8DE',lw=.8)

txt(.055,.826,'a  One scalar, conjugate phases',10,weight='bold')
ax=fig.add_axes([.07,.591,.35,.196]);ax.axis('off');ax.set(xlim=(-1.32,1.32),ylim=(-1.12,1.12));ax.set_aspect('equal')
t=np.linspace(0,2*np.pi,250)
ax.plot(np.cos(t),np.sin(t),color='#CBD8DE',lw=.9)
for phi,col,style in [(1.05,teal,'-'),(-1.05,gold,'--')]:
    tt=np.linspace(0,phi,80)
    ax.plot(np.cos(tt),np.sin(tt),style,c=col,lw=2.4)
    ax.annotate('',xy=(np.cos(phi),np.sin(phi)),xytext=(np.cos(phi*.72),np.sin(phi*.72)),arrowprops={'arrowstyle':'-|>','color':col,'lw':1.4})
    ax.plot([0,np.cos(phi)],[0,np.sin(phi)],color=col,lw=1)
    ax.scatter([np.cos(phi)],[np.sin(phi)],s=22,c=col,zorder=4)
ax.text(-1.19,.76,r'$\psi$',color=teal,fontsize=15)
ax.text(-1.19,-.82,r'$\psi^*$',color=gold,fontsize=15)
ax.scatter([0],[0],s=9,c=navy)
txt(.24,.556,r'$\Phi=(\psi,\psi^*)^{\mathsf{T}}/\sqrt{2}$',13,ha='center')
txt(.24,.525,'Constrained representation; no extra scalar',8,ha='center',color=gray)

txt(.515,.826,'b  Two controlled auxiliary modes',10,weight='bold')
ax=fig.add_axes([.52,.587,.42,.211],projection='3d');ax.patch.set_alpha(0)
u=np.linspace(-1,1,13);X,Y=np.meshgrid(u,u)
for off,fun,col in [(-1.35,.25*X**2-.15*Y**2,teal),(1.35,-.25*X**2-.15*Y**2,gold)]:
    ax.plot_wireframe(X+off,Y,fun,rstride=1,cstride=1,color=col,lw=.65)
ax.view_init(27,-63);ax.set_box_aspect((2.8,1,.8));ax.set_axis_off()
txt(.616,.573,'Saddle',9,color=teal,ha='center')
txt(.839,.573,'Companion',9,color=gold,ha='center')
txt(.73,.538,'Both coordinates and the logical phase retained',8,ha='center',color=gray)
txt(.73,.515,'Quantum controls are additional assumptions',8,ha='center',color=gray)

bg.add_patch(FancyBboxPatch((.055,.405),.89,.084,boxstyle='round,pad=.009',facecolor='#EDF5F6',edgecolor='none'))
txt(.078,.457,'EXACT RECOVERY',8,color=teal,weight='bold')
txt(.078,.426,'Residual states independent of logical label',9)
txt(.702,.441,r'$\chi_b=\chi_c\ \ \forall b,c\quad\Longleftrightarrow\quad\Lambda=\mathrm{id}$',12,ha='center')

txt(.055,.369,'c  A quantitative boundary: timing errors',10,weight='bold')
ax=fig.add_axes([.105,.125,.505,.192])
x=np.linspace(0,.4,301);f=(1+np.exp(-.5*(.8*.3*np.sin(x))**2))/2
ax.plot(x,f,color=teal,lw=1.8,label='Exact Gaussian-noise law')
dx=np.array([r['delta'] for r in data['timing']]);fy=np.array([(1+r['direct_kernel_real'])/2 for r in data['timing']])
assert np.max(np.abs(fy-(1+np.exp(-.5*(.8*.3*np.sin(dx))**2))/2))<3e-12
ax.scatter(dx,fy,c=gold,marker='o',s=22,edgecolor='white',linewidth=.5,zorder=4,label='Direct oscillator calculation')
ax.set(xlim=(-.009,.405),ylim=(.99765,1.00012),xlabel=r'Timing offset $\delta t$ (normalized)',ylabel=r'Entanglement fidelity $F_{\mathrm{e}}$')
ax.set_xticks([0,.1,.2,.3,.4]);ax.set_yticks([.998,.999,1]);ax.tick_params(labelsize=8)
ax.grid(axis='y',color='#DBE3E7',lw=.6);ax.legend(loc='lower left',frameon=False,fontsize=7,handlelength=1.8)
txt(.675,.298,'Shared turning time',10,weight='bold')
txt(.675,.262,r'$F_{\mathrm{e}}=1$',17,color=teal)
txt(.675,.215,'Near that time',9,color=gray)
txt(.675,.177,r'$1-F_{\mathrm{e}}=C\,\delta t^2+O(\delta t^4)$',10)
txt(.675,.134,'Common translation noise',8,color=gray)
bg.plot([.055,.945],[.057,.057],color='#CBD8DE',lw=.8)
txt(.055,.025,'Analytic model with numerical verification.',8,color=gray)

stem='Highlight_Conjugate_Phase_Geometry'
fig.savefig(root/(stem+'.png'),dpi=600,facecolor='white')
fig.savefig(root/(stem+'.pdf'),facecolor='white')
fig.savefig(root/(stem+'.svg'),facecolor='white')
im=Image.open(root/(stem+'.png')).convert('RGB')
im.save(root/(stem+'.jpg'),quality=98,subsampling=0,dpi=(600,600))
im.save(root/(stem+'.tif'),compression='tiff_lzw',dpi=(600,600))
caption='Coherent saddle encoding and displacement recovery. (a) One complex scalar is represented by a constrained conjugate pair, rather than two independent scalar fields. Solid teal and dashed ochre arcs indicate conjugate phase orientations on the unit circle. (b) A separately specified quantum realization retains both saddle and companion displacements and the logical phase; the wireframes illustrate their shapes. (c) Exact recovery requires identical residual auxiliary states for all logical labels, almost everywhere over the noise. For common Gaussian translations and a matched inverse decoder, shared oscillator turning times satisfy this criterion. Timing offsets produce the displayed fidelity reduction. The curve uses force gap 0.8, displacement standard deviation 0.3, and normalized hbar=omega=1; dots are saved independent 50-level oscillator calculations from numerical/model-verification.json. C is the nonnegative quadratic timing coefficient defined in the manuscript. The plotted values are theoretical and numerical, not experimental measurements.'
(root/'Highlight_caption_and_alt_text.txt').write_text(caption+'\n\nALT TEXT\nA conjugate phase pair and saddle-plus-companion wireframes accompany an exact recovery criterion. A timing plot shows unit entanglement fidelity at zero offset, decreasing quadratically nearby; direct oscillator points agree with the analytic curve.\n',encoding='utf-8')
(root/'Highlight_provenance.txt').write_text('Original deterministic scientific artwork. Source: make_highlight.py. Model and equations: Conjugate_Phase_Geometry_AIP_Advances.tex. Timing markers: numerical/model-verification.json; SHA256 '+hashlib.sha256(data_path.read_bytes()).hexdigest()+'\nJPEG and TIFF: RGB, 600 dpi, '+str(im.size)+' pixels; requested canvas 8.0139 x 6.2739 inches. TIFF uses lossless LZW compression. PDF embeds fonts; SVG preserves editable text. Numeric agreement checked at tolerance 3e-12.\nAIP graphics guidance: https://pubs.aip.org/pages/author-instructions/ (accessed November 25, 2026). No acceptance guarantee is implied.\n',encoding='utf-8')
preview=im.copy();preview.thumbnail((1440,1440));preview.save(root/'highlight_preview.png')
print('Created 600 dpi RGB JPEG/TIFF, PNG, vector PDF/SVG, caption and provenance. Timing markers verified.')


