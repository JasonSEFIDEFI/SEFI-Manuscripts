from pathlib import Path
import argparse, json, csv
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

parser=argparse.ArgumentParser()
parser.add_argument('--output',required=True)
args=parser.parse_args()
out=Path(args.output); out.mkdir(parents=True,exist_ok=True)
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.labelsize':10,'axes.titlesize':12,'pdf.fonttype':42,'ps.fonttype':42,'savefig.facecolor':'white'})
BLUE='#0072B2'; ORANGE='#D55E00'; GREEN='#009E73'; GRAY='#6b7280'
t=np.linspace(-2,2,501); f=lambda x,y: .25*x*x-.25*y*y
ref=np.array([t,np.sin(t),f(t,np.sin(t))]); pert=ref+np.array([np.zeros_like(t),np.zeros_like(t),.15*np.cos(t)])
corr=pert.copy(); corr[2]=f(corr[0],corr[1])
manifest=[]
def save(fig,n,slug,caption,kind):
    stem=f'figure_{n:02d}_{slug}'
    fig.savefig(out/(stem+'.png'),dpi=350,bbox_inches='tight')
    fig.savefig(out/(stem+'.pdf'),bbox_inches='tight')
    manifest.append({'figure':n,'stem':stem,'type':kind,'caption':caption})
    plt.close(fig)
def base3(title):
    fig=plt.figure(figsize=(7.2,5.3),layout='constrained'); ax=fig.add_subplot(projection='3d')
    ax.set(xlabel='x (dimensionless)',ylabel='y (dimensionless)',zlabel='z (dimensionless)',title=title)
    ax.view_init(24,-59)
    ax.set_box_aspect((1.4,1,1))
    for axis in (ax.xaxis,ax.yaxis,ax.zaxis): axis.pane.fill=False
    return fig,ax
def surface(ax,alpha=.2):
    x,y=np.meshgrid(np.linspace(-2,2,35),np.linspace(-1.2,1.2,29))
    ax.plot_surface(x,y,f(x,y),color='#bac7d2',alpha=alpha,edgecolor='#a5afb9',linewidth=.25,shade=False)
def curve(ax,p,color=BLUE,style='-',label=None,lw=2.5): ax.plot(*p,color=color,ls=style,lw=lw,label=label)
def note(fig,text): fig.text(.5,-.045,text,ha='center',fontsize=8,color=GRAY)

fig,ax=base3('Proposed stability manifold'); surface(ax);curve(ax,ref,label=r'Reference $\gamma_\Sigma(t)$')
ax.text(-1.75,.95, f(-1.75,.95),r'$\Sigma$' ,fontsize=16)
i=320;v=ref[:,i+8]-ref[:,i];ax.quiver(*ref[:,i],*v,color=BLUE,arrow_length_ratio=.45,linewidth=2)
ax.legend(loc='upper left');note(fig,'Conceptual geometry • not a measured energy landscape or a stability proof')
save(fig,1,'stability_manifold','Illustrative proposed constraint manifold and reference trajectory; surface geometry alone does not establish dynamical stability.','conceptual mathematical illustration')

fig,ax=base3('Reference evolution on the manifold');surface(ax)
curve(ax,ref,label=r'$\gamma_\Sigma(t)$')
for v in [-1,0,1]:
    p=(v,np.sin(v),f(v,np.sin(v)));ax.scatter(*p,color=BLUE,s=28,depthshade=False);ax.text(p[0],p[1],p[2]+.14,f't = {v}')
ax.legend(loc='upper left');note(fig,r'$\alpha=\beta=0.25$ • parameter t and coordinates are dimensionless')
save(fig,2,'reference_trajectory','Reference curve (t, sin t, 0.25 t² − 0.25 sin² t), for −2 ≤ t ≤ 2, on the illustrative manifold.','computed mathematical illustration')

fig=plt.figure(figsize=(10,4.8),layout='constrained');ax=fig.add_subplot(121,projection='3d');surface(ax,.26)
on=np.array([1,.5,f(1,.5)]);off=on+[0,0,.65]
ax.scatter(*on,color=BLUE,s=45,label=r'$S(q_{on})=0$');ax.scatter(*off,color=ORANGE,s=45,label=r'$S(q_{off})\ne0$')
ax.set(xlabel='x',ylabel='y',zlabel='z',title=r'Constraint set $\Sigma\subset M$');ax.view_init(25,-55);ax.legend(fontsize=9,loc='upper left')
ax2=fig.add_subplot(122);ax2.axis('off');ax2.set(xlim=(0,1),ylim=(0,1),title='Conceptual relationship')
def box(ax,xy,w,h,text,color='#edf3f7',dashed=False,fontsize=10):
    ax.add_patch(FancyBboxPatch(xy,w,h,boxstyle='round,pad=0.012',facecolor=color,edgecolor=GRAY,linestyle='--' if dashed else '-',linewidth=1.1));ax.text(xy[0]+w/2,xy[1]+h/2,text,ha='center',va='center',fontsize=fontsize)
for y,txt in [(.74,'Proposed identity constraints\nS(q) = 0'),(.43,'Permissible set\nΣ = {q : S(q) = 0}'),(.12,'Reference trajectory\nγΣ(t) ∈ Σ')]:box(ax2,(.12,y),.76,.18,txt)
for y in [.72,.41]:ax2.annotate('',xy=(.5,y-.09),xytext=(.5,y),arrowprops={'arrowstyle':'->','color':GRAY})
note(fig,'Constraint schematic • dynamical preservation requires an independently specified evolution law')
save(fig,3,'identity_constraint','Proposed constraint S(q)=0 defining a permissible set. A constraint definition does not by itself establish conservation under dynamics.','conceptual schematic')

fig,ax=base3('Vertical displacement and surface normal');surface(ax,.16)
q=on+[0,0,.25];ax.scatter(*on,color=BLUE,s=35);ax.scatter(*q,color=ORANGE,s=35)
ax.quiver(*on,0,0,.25,color=ORANGE,linewidth=2,arrow_length_ratio=.23)
n=np.array([-.5,.25,1]);n=n/np.linalg.norm(n)*.5
ax.quiver(*on,*n,color=GRAY,linewidth=1.5,arrow_length_ratio=.18)
ax.text(*q,r'  $q$',color=ORANGE);ax.text(on[0],on[1]-.2,on[2]-.16,r'$\Pi_v(q)$',color=BLUE)
ax.text(on[0]+n[0],on[1]+n[1],on[2]+n[2]+.04,'Surface normal',fontsize=9)
ax.text(1.08,.5,.32,r'$d$',color=ORANGE,fontsize=14)
note(fig,'Vertical projection ≠ nearest-point projection; vertical direction ≠ surface normal in general')
save(fig,4,'vertical_displacement','q=(1,0.5,0.4375), Πv(q)=(1,0.5,0.1875). The orange displacement is vertical; the gray surface normal is a different direction.','computed geometric diagram')

fig=plt.figure(figsize=(10,4.8),layout='constrained')
for k,title in [(1,'(a) Before projection'),(2,'(b) After prescribed projection')]:
    ax=fig.add_subplot(1,2,k,projection='3d');surface(ax,.14);curve(ax,ref,BLUE,'--','Reference',2)
    if k==1:
        curve(ax,pert,ORANGE,'-','Perturbed',2)
        for i in [80,180,300,420]:ax.quiver(*pert[:,i],0,0,corr[2,i]-pert[2,i],color=GRAY,arrow_length_ratio=.3)
    else:curve(ax,corr,GREEN,':','Projected (coincident)',3)
    ax.set(xlabel='x',ylabel='y',zlabel='z',title=title);ax.view_init(24,-59);ax.legend(fontsize=8,loc='upper left')
note(fig,'Prescribed vertical map Πv(x,y,z) = (x,y,0.25x² − 0.25y²) • not autonomous recovery dynamics')
save(fig,5,'projection_mapping','Prescribed vertical projection removes the specified vertical perturbation by construction; physical quantum recovery is not demonstrated.','computed mathematical illustration')

u=np.linspace(-1.2,5,400);helix=np.array([np.cos(u),np.sin(u),.5*u]);p=np.array([1.,0.,0.]);T=np.array([0,1,.5])/np.sqrt(1.25);N=np.array([-1.,0.,0.]);B=np.cross(T,N)
fig,ax=base3('Frenet–Serret frame of an illustrative helix');curve(ax,helix,BLUE,label='Helix')
for vec,col,label in [(T,GREEN,'T'),(N,ORANGE,'N'),(B,'#8b5aa5','B')]:ax.quiver(*p,*vec,color=col,linewidth=2,arrow_length_ratio=.15);ax.text(*(p+vec*1.12),label,color=col,fontsize=13)
a,b=np.meshgrid(np.linspace(-.7,.7,2),np.linspace(-.7,.7,2));plane=p[:,None,None]+T[:,None,None]*a+N[:,None,None]*b
ax.plot_surface(*plane,alpha=.15,color=GREEN)
ax.text2D(.02,.95,r'$\gamma(u)=(\cos u,\sin u,0.5u)$'+'\n'+r'$\kappa=0.8,\quad\tau=0.4$',transform=ax.transAxes)
note(fig,'Dimensionless coordinates • u is not arc length • shaded patch is the osculating plane')
save(fig,6,'frenet_frame','Calculated curve frame at u=0 for the helix (cos u, sin u, 0.5u). Curvature 0.8, torsion 0.4; curve normal and surface normal are distinct concepts.','computed geometric diagram')

fig=plt.figure(figsize=(7.6,5.1),layout='constrained');ax=fig.add_subplot();ax.set_aspect('equal');ax.set(xlim=(-.07,.30),ylim=(-.04,.24),xlabel='Component along N',ylabel='Component along B',title='Transverse displacement in the local curve frame')
for end,col,label in [((.2,0),ORANGE,r'$d_N N$'),((0,.15),'#8b5aa5',r'$d_B B$'),((.2,.15),'#111827',r'$d$')]:ax.annotate('',xy=end,xytext=(0,0),arrowprops={'arrowstyle':'->','color':col,'lw':2});ax.text(end[0]+.008,end[1]+.008,label,color=col,fontsize=12)
ax.plot([.2,.2],[0,.15],'--',color=GRAY);ax.plot([0,.2],[.15,.15],'--',color=GRAY)
ax.text(.01,.205,r'$d=0.20N+0.15B$'+'\n'+r'General: $d=d_TT+d_NN+d_BB$',fontsize=11)
ax.grid(alpha=.15);note(fig,'Local N–B coordinates • chosen example has dT = 0 • no physical error-channel assignment')
save(fig,7,'frame_components','A deliberately transverse displacement decomposed in the normal–binormal plane of a curve. General displacement can include a tangent component.','mathematical schematic')

fig,ax=plt.subplots(figsize=(10,6));ax.axis('off');ax.set(xlim=(0,1),ylim=(0,1))
ax.text(.5,.98,'Proposed framework and geometric analysis workflow',ha='center',va='top',fontsize=14)
ax.text(.03,.88,'CONCEPTUAL ROLES',fontsize=9,color=GRAY)
for x,title in [(.04,'SEFI\nProposed identity constraints'),(.36,'GWFM\nTrajectory geometry'),(.68,'DEFI\nProposed coupled dynamics')]:box(ax,(x,.69),.27,.13,title,dashed=True,fontsize=9)
ax.text(.03,.60,'PROPOSED ANALYSIS SEQUENCE',fontsize=9,color=GRAY)
items=[('Model and\nparameters',.04),('Synthetic\ntrajectories',.235),('Constraint\ndiagnostics',.43),('Prescribed\nprojection',.625),('Comparison\nand outputs',.82)]
for txt,x in items:box(ax,(x,.36),.14,.13,txt,dashed=True,fontsize=9)
for i in range(4):ax.annotate('',xy=(items[i+1][1]-.014,.425),xytext=(items[i][1]+.155,.425),arrowprops={'arrowstyle':'->','linestyle':'--','color':GRAY})
ax.text(.5,.20,'Dashed boxes and arrows: proposed relationships / workflow',ha='center',fontsize=10)
ax.text(.5,.10,'Conceptual diagram; no source-code audit of SEFI_QEC_Stack is asserted.\nNo hardware control, quantum syndrome measurement, or logical recovery is shown.',ha='center',fontsize=9,color=GRAY)
save(fig,8,'proposed_workflow','Conceptual roles and proposed analysis sequence. All connections are marked proposed; this is not a verified implementation architecture for SEFI_QEC_Stack.','conceptual schematic; software audit pending')

fig,ax=base3('Specified validation geometry');surface(ax,.24);curve(ax,ref,label=r'$\gamma_\Sigma(t)$')
ax.legend(loc='upper left');ax.text2D(.02,.82,r'$\Sigma:\ z=0.25x^2-0.25y^2$'+'\n'+r'$-2\leq t\leq2$',transform=ax.transAxes)
note(fig,'Illustration parameters: α = β = 0.25 • reconcile with submitted calculation before replacement')
save(fig,9,'validation_surface','Computed saddle surface and reference curve using proposed illustration parameters alpha=beta=0.25. These are not recovered original experimental settings.','computed toy-model plot')

fig=plt.figure(figsize=(11,4.8),layout='constrained');ax=fig.add_subplot(121,projection='3d');surface(ax,.12)
curve(ax,ref,BLUE,'--','Reference',2);curve(ax,pert,ORANGE,'-','Perturbed',2);curve(ax,corr,GREEN,':','Projected (coincident)',3)
ax.set(xlabel='x',ylabel='y',zlabel='z',title='(a) Prescribed trajectory projection');ax.view_init(24,-59);ax.legend(fontsize=8,loc='upper left')
before=np.abs(pert[2]-f(pert[0],pert[1]));after=np.abs(corr[2]-f(corr[0],corr[1]))
ax=fig.add_subplot(122);ax.plot(t,before,color=ORANGE,label=r'Before: $|\epsilon\cos t|$');ax.plot(t,after,color=GREEN,ls='--',label='After projection');ax.set(xlabel='t (dimensionless)',ylabel='Vertical constraint residual',title='(b) Residual before and after projection',ylim=(-.008,.17));ax.grid(alpha=.2);ax.legend(fontsize=9)
note(fig,f'α = β = 0.25; ε = 0.15; 501 samples • maximum post-projection residual = {after.max():.1e} (by construction)')
save(fig,10,'validation_projection','Perturbation epsilon*cos(t) and its removal by vertical projection. Post-projection constraint satisfaction follows algebraically from the prescribed map; this is not quantum error-rate evidence.','computed toy-model plot')

with (out/'validation_trajectory_data.csv').open('w',newline='',encoding='utf-8') as h:
    writer=csv.writer(h);writer.writerow(['t','x','y','z_reference','z_perturbed','z_projected','vertical_residual_before','vertical_residual_after']);writer.writerows(zip(t,ref[0],ref[1],ref[2],pert[2],corr[2],before,after))
assert np.allclose(before,np.abs(.15*np.cos(t)),atol=1e-15)
assert np.array_equal(corr,ref)
assert np.allclose(np.cross(T,N),B) and np.isclose(np.linalg.norm(B),1)
(out/'figure_manifest.json').write_text(json.dumps({'parameters':{'alpha':.25,'beta':.25,'epsilon':.15,'samples':501,'domain':[-2,2]},'max_post_projection_residual':float(after.max()),'figures':manifest},indent=2),encoding='utf-8')
lines=['# Candidate photonics replacement figures','','Generated as reproducible mathematical plots and diagrams. These are review candidates, not a revised journal submission.','', '## Files','', 'Each figure has a 350 dpi PNG and a PDF with vector elements. The script and CSV permit reproduction.','', '## Captions and scope','']
for item in manifest: lines.extend([f"### Figure {item['figure']}: {item['stem']}",item['caption'],f"Type: {item['type']}",''])
lines.extend(['## Review before submission','','The submitted PDF and original image contents were not visually inspected. Match figure numbering and update captions against that PDF. Figure 8 is explicitly conceptual, pending a software audit. Parameters for Figures 2, 4, 5, 9 and 10 are proposed illustration choices, not recovered original data. The vertical projection is not nearest-point projection, a vertical perturbation is not generally binormal, and the toy model does not establish physical photonic QEC. Existing captions and text require reconciliation where they assert these equivalences.'])
(out/'README.md').write_text('\n'.join(lines),encoding='utf-8')
# Contact sheet for visual QA.
fig,axs=plt.subplots(5,2,figsize=(14,19))
for ax,item in zip(axs.flat,manifest):
    ax.imshow(plt.imread(out/(item['stem']+'.png')));ax.axis('off');ax.set_title(f"Figure {item['figure']}",fontsize=11)
fig.tight_layout();fig.savefig(out/'contact_sheet.png',dpi=110);plt.close(fig)
print(json.dumps({'output':str(out),'figures':len(manifest),'max_residual':float(after.max()),'checks':'passed'}))
