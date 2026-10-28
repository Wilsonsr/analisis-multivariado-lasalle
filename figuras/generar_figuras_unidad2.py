# Genera las figuras de la guía de la Unidad 2 (PNG y SVG editables). Ejecutar desde la carpeta figuras/.
import numpy as np, pandas as pd, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Ellipse
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.spines.top':False,'axes.spines.right':False,'savefig.dpi':200})
NAVY='#113054'; BLUE='#3B64B4'; YEL='#F6CD46'; ORA='#E8A33D'; GRY='#8A93A6'; RED='#C0392B'; GRN='#2E8B57'
def save(f,n): f.savefig(f'unidad2/{n}.png',bbox_inches='tight'); f.savefig(f'unidad2/{n}.svg',bbox_inches='tight'); plt.close(f)
e=pd.read_csv('../data/datos_guia2_encuesta_salud.csv')
orden=['Primaria','Secundaria','Técnica','Universitaria']
N=pd.crosstab(e.nivel_educativo,e.regimen).loc[orden]
# 1 perfiles fila
prof=N.div(N.sum(1),axis=0); media=N.sum(0)/N.values.sum()
prof.loc['Perfil medio']=media
cols=[BLUE,YEL,RED,GRN]
f,ax=plt.subplots(figsize=(8,3.8)); left=np.zeros(len(prof))
for k,c in enumerate(prof.columns):
    ax.barh(range(len(prof)),prof[c],left=left,color=cols[k],label=c,edgecolor='white')
    for i,v in enumerate(prof[c]):
        if v>0.06: ax.text(left[i]+v/2,i,f'{v*100:.0f} %',ha='center',va='center',fontsize=8,color='white' if k!=1 else NAVY)
    left+=prof[c].values
ax.set_yticks(range(len(prof)),prof.index); ax.invert_yaxis(); ax.set_xlim(0,1); ax.set_xlabel('Proporción dentro de cada nivel educativo (perfil fila)')
ax.get_yticklabels()[-1].set_weight('bold')
ax.legend(ncol=4,frameon=False,loc='upper center',bbox_to_anchor=(0.5,1.15),fontsize=9); save(f,'g2_perfiles')
# 2 mapa CA
P=N/N.values.sum(); r=P.sum(1).values; c=P.sum(0).values
S=(P.values-np.outer(r,c))/np.sqrt(np.outer(r,c)); U,d,Vt=np.linalg.svd(S,full_matrices=False)
F=U[:,:2]*d[:2]/np.sqrt(r)[:,None]; G=Vt.T[:,:2]*d[:2]/np.sqrt(c)[:,None]
F[:,0]*=-1; G[:,0]*=-1  # alinear con R
pct=100*d**2/(d**2).sum()
f,ax=plt.subplots(figsize=(7,5))
ax.scatter(F[:,0],F[:,1],marker='o',s=60*r/r.max()+30,color=BLUE,label='Nivel educativo (filas)')
ax.scatter(G[:,0],G[:,1],marker='^',s=60*c/c.max()+30,color=RED,label='Régimen (columnas)')
for i,t in enumerate(N.index): ax.text(F[i,0],F[i,1]+0.035,t,color=BLUE,ha='center',fontsize=9,weight='bold')
for i,t in enumerate(N.columns): ax.text(G[i,0],G[i,1]-0.06,t,color=RED,ha='center',fontsize=9,weight='bold')
ax.axhline(0,color=GRY,lw=0.5); ax.axvline(0,color=GRY,lw=0.5)
ax.set_xlabel(f'Dimensión 1 ({pct[0]:.1f} %)'.replace('.',',')); ax.set_ylabel(f'Dimensión 2 ({pct[1]:.1f} %)'.replace('.',','))
ax.legend(frameon=False,fontsize=8,loc='lower right'); ax.set_ylim(-0.3,0.7); save(f,'g2_mapa_ac')
# 3 ACM
import prince
vars_acm=['zona','nivel_educativo','regimen','consulta_preventiva','percepcion_calidad']
X=e[vars_acm].astype('category'); m=prince.MCA(n_components=2,random_state=2026).fit(X)
cc=m.column_coordinates(X); ev=m.eigenvalues_; tot=m.total_inertia_
VC={'zona':NAVY,'nivel_educativo':BLUE,'regimen':RED,'consulta_preventiva':GRN,'percepcion_calidad':ORA}
VN={'zona':'Zona','nivel_educativo':'Nivel educativo','regimen':'Régimen','consulta_preventiva':'Consulta preventiva','percepcion_calidad':'Percepción de calidad'}
f,ax=plt.subplots(figsize=(7.5,5.6))
for v in vars_acm:
    idx=[i for i in cc.index if i.startswith(v+'__')]
    ax.scatter(cc.loc[idx,0],cc.loc[idx,1],color=VC[v],label=VN[v],s=40)
    for i in idx:
        lab=i.split('__')[1]
        if v=='consulta_preventiva': lab='Consulta: '+lab
        if v=='percepcion_calidad': lab='Percep. '+lab.lower()
        off={'Consulta: Sí':(0.0,0.09),'Percep. buena':(-0.2,0.07),'Contributivo':(-0.12,-0.13),'Urbana':(0.04,-0.1),'Percep. regular':(0.03,0.07),'Consulta: No':(0.03,-0.13),'No afiliado':(0.05,0.05),'Percep. mala':(0.04,-0.12),'Rural':(-0.05,0.08),'Primaria':(0.04,0.06)}.get(lab,(0.05,0.07))
        if cc.loc[i,1] < 3: ax.text(cc.loc[i,0]+off[0],cc.loc[i,1]+off[1],lab,fontsize=8,color=VC[v])
ax.axhline(0,color=GRY,lw=0.5); ax.axvline(0,color=GRY,lw=0.5)
ax.set_xlabel(f'Dimensión 1 ({100*ev[0]/tot:.1f} %)'.replace('.',',')); ax.set_ylabel(f'Dimensión 2 ({100*ev[1]/tot:.1f} %)'.replace('.',','))
ax.set_ylim(-1.05,1.45); ax.set_xlim(-1.3,1.35)
ax.annotate('Especial (−0,43; 3,47):\nfuera del área del gráfico', xy=(-0.43,1.42), xytext=(-0.2,1.15), fontsize=8, color=RED, arrowprops=dict(arrowstyle='->',color=RED))
ax.legend(frameon=False,fontsize=8,loc='lower left'); save(f,'g2_mapa_acm')
# 4 esquema factores latentes
L={'Infraestructura':(['inst_limpieza','inst_comodidad','inst_equipos'],[0.76,0.69,0.64]),
   'Trato humano':(['trato_amabilidad','trato_escucha','trato_explicacion'],[0.74,0.74,0.68]),
   'Oportunidad':(['opor_cita','opor_espera','opor_tramites'],[0.69,0.77,0.64])}
f,ax=plt.subplots(figsize=(8.5,6)); ax.axis('off'); ax.set_xlim(0,10); ax.set_ylim(0,10)
fy={'Infraestructura':8.3,'Trato humano':5.0,'Oportunidad':1.7}; fcol={'Infraestructura':BLUE,'Trato humano':GRN,'Oportunidad':ORA}
k=0
for fac,(its,ls) in L.items():
    y0=fy[fac]; ax.add_patch(Ellipse((2.2,y0),2.8,1.3,fc=fcol[fac],ec='none',alpha=0.9)); ax.text(2.2,y0,fac,ha='center',va='center',color='white',weight='bold',fontsize=10)
    for j,(it,l) in enumerate(zip(its,ls)):
        y=y0+0.95-j*0.95; ax.add_patch(FancyBboxPatch((6.3,y-0.3),2.9,0.6,boxstyle='round,pad=0.02',fc='#F7F7FB',ec=GRY)); ax.text(7.75,y,it,ha='center',va='center',fontsize=8.5)
        ax.annotate('',xy=(6.28,y),xytext=(3.62,y0),arrowprops=dict(arrowstyle='->',color=fcol[fac],lw=1.2+2*(l-0.6)))
        ax.text(4.9,(y+y0)/2+0.12,f'{l:.2f}'.replace('.',','),fontsize=8,color=fcol[fac],ha='center')
        ax.annotate('',xy=(9.25,y),xytext=(9.75,y),arrowprops=dict(arrowstyle='->',color=GRY,lw=0.8)); 
    k+=1
ax.text(9.5,0.25,'→ error único de cada ítem',color=GRY,fontsize=7.5,ha='center')
def arc(a,b,lab):
    ax.annotate('',xy=(0.85,fy[b]),xytext=(0.85,fy[a]),arrowprops=dict(arrowstyle='<->',color=GRY,connectionstyle='arc3,rad=0.45'))
arc('Infraestructura','Trato humano','0,36'); arc('Trato humano','Oportunidad','0,26')
ax.annotate('',xy=(0.6,fy['Oportunidad']),xytext=(0.6,fy['Infraestructura']),arrowprops=dict(arrowstyle='<->',color=GRY,connectionstyle='arc3,rad=0.5'))
ax.text(0.05,6.7,'0,36',fontsize=8,color=GRY); ax.text(0.05,3.4,'0,26',fontsize=8,color=GRY); ax.text(-0.45,5.0,'0,31',fontsize=8,color=GRY)
ax.text(2.2,9.7,'Factores latentes (no observados)',ha='center',fontsize=9,color=NAVY,weight='bold'); ax.text(7.75,9.7,'Ítems observados (escala 1 a 5)',ha='center',fontsize=9,color=NAVY,weight='bold')
save(f,'g2_factores')
# 5 gráfico de cargas
load=pd.DataFrame([[-0.028,0.009,0.760],[-0.022,-0.022,0.691],[0.098,0.020,0.643],[0.735,-0.013,-0.013],[0.739,0.007,0.004],[0.682,0.015,0.034],[0.024,0.693,0.016],[-0.064,0.772,0.030],[0.090,0.637,-0.065]],
  index=['inst_limpieza','inst_comodidad','inst_equipos','trato_amabilidad','trato_escucha','trato_explicacion','opor_cita','opor_espera','opor_tramites'],columns=['F1 Trato humano','F2 Oportunidad','F3 Infraestructura'])
f,axs=plt.subplots(1,3,figsize=(9,4),sharey=True)
for k,col in enumerate(load.columns):
    ax=axs[k]; v=load[col]; ax.barh(range(9),v,color=[[GRN,ORA,BLUE][k] if abs(x)>=0.4 else '#CCD3E0' for x in v])
    ax.axvline(0.4,ls='--',color=GRY,lw=0.8); ax.axvline(0,color='black',lw=0.6); ax.set_xlim(-0.2,1); ax.set_title(col,fontsize=9.5,color=NAVY)
    if k==0: ax.set_yticks(range(9),load.index)
    ax.invert_yaxis() if k==0 else None
f.supxlabel('Carga factorial (matriz de patrones, rotación oblimin)',fontsize=9); f.tight_layout(); save(f,'g2_cargas')
# 6 análisis paralelo sobre la matriz reducida (misma variante que psych::fa.parallel(fa = "fa"))
items=e.iloc[:,6:15]
def reduced_eigs(M):
    R=np.corrcoef(M,rowvar=False); smc=1-1/np.diag(np.linalg.inv(R)); Rr=R.copy(); np.fill_diagonal(Rr,smc)
    return np.linalg.eigvalsh(Rr)[::-1]
ev=reduced_eigs(items.values.astype(float))
rng=np.random.default_rng(2026); sims=np.array([reduced_eigs(rng.normal(size=items.shape)) for _ in range(500)])
q=np.percentile(sims,95,axis=0)
f,ax=plt.subplots(figsize=(7,3.6)); ax.plot(range(1,10),ev,marker='o',color=NAVY,label='Valores propios observados (matriz reducida)')
ax.plot(range(1,10),q,ls='--',marker='x',color=RED,label='Percentil 95 de datos aleatorios')
ax.axhline(0,color=GRY,lw=0.8,ls=':'); ax.set_xticks(range(1,10)); ax.set_xlabel('Número de factor'); ax.set_ylabel('Valor propio'); ax.legend(frameon=False,fontsize=8)
save(f,'g2_scree_afe')
print(ev.round(2)[:5], q.round(2)[:5])
