# Genera las figuras de la guía de la Unidad 1 (PNG y SVG editables). Ejecutar desde la carpeta figuras/.
import numpy as np, pandas as pd, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.spines.top':False,'axes.spines.right':False,'savefig.dpi':200})
NAVY='#113054'; BLUE='#3B64B4'; YEL='#F6CD46'; ORA='#E8A33D'; GRY='#8A93A6'
ZC={'Industrial':'#C0392B','Residencial':BLUE,'Periurbana':'#2E8B57'}
d=pd.read_csv('../data/datos_guia1_calidad_aire.csv'); X=d.iloc[:,2:]; names=list(X.columns)
def save(f,name):
    f.savefig(f'unidad1/{name}.png',bbox_inches='tight'); f.savefig(f'unidad1/{name}.svg',bbox_inches='tight'); plt.close(f)

# 1 Esquema matriz de datos
f,ax=plt.subplots(figsize=(8,4.2)); ax.axis('off')
cols=['PM25','PM10','NO2','…','Viento']; rows=['E01','E02','E03','⋮','E30']
x0,y0,cw,ch=2.0,0.6,1.25,0.62
for j,c in enumerate(cols):
    ax.add_patch(Rectangle((x0+j*cw,y0+5*ch),cw,ch,fc=NAVY,ec='white')); ax.text(x0+j*cw+cw/2,y0+5*ch+ch/2,c,color='white',ha='center',va='center',fontsize=10,weight='bold')
vals=[['24,9','47,6','29,7','…','1,7'],['24,1','48,2','37,5','…','1,7'],['15,6','33,2','28,0','…','2,3'],['⋮','⋮','⋮','⋱','⋮'],['10,6', '21,5', '24,3', '…', '3,4']]
for i,r in enumerate(rows):
    yy=y0+(4-i)*ch
    ax.add_patch(Rectangle((x0-cw,yy),cw,ch,fc='#EEF2FA',ec='white')); ax.text(x0-cw/2,yy+ch/2,r,ha='center',va='center',weight='bold',color=NAVY)
    for j in range(5):
        fc='#FCE9A6' if (i==1 and j==2) else ('#F7F7FB' if i%2==0 else 'white')
        ax.add_patch(Rectangle((x0+j*cw,yy),cw,ch,fc=fc,ec=GRY,lw=0.6)); ax.text(x0+j*cw+cw/2,yy+ch/2,vals[i][j],ha='center',va='center')
ax.annotate('',xy=(x0-cw-0.25,y0),xytext=(x0-cw-0.25,y0+5*ch),arrowprops=dict(arrowstyle='<->',color=BLUE))
ax.text(x0-cw-0.45,y0+2.5*ch,'n = 30 individuos\n(estaciones)',rotation=90,ha='center',va='center',color=BLUE)
ax.annotate('',xy=(x0,y0+6*ch+0.2),xytext=(x0+5*cw,y0+6*ch+0.2),arrowprops=dict(arrowstyle='<->',color=BLUE))
ax.text(x0+2.5*cw,y0+6*ch+0.42,'p = 8 variables cuantitativas',ha='center',color=BLUE)
ax.text(x0+5*cw+0.3,y0+3.3*ch,'$x_{23}$ = 37,5 µg/m³\nvalor de la variable 3 (NO₂)\nen el individuo 2 (E02)',va='center',fontsize=9,color=NAVY)
ax.text(x0+5*cw+0.3,y0+1.2*ch,'Fila i: vector $\\mathbf{x}_i$\n(perfil de una estación)\nColumna j: variable $X_j$',va='center',fontsize=9,color=GRY)
ax.set_xlim(0.3,12.2); ax.set_ylim(0.3,5.6); save(f,'g1_matriz_datos')

# 2 boxplots escalas
f,ax=plt.subplots(figsize=(8,3.6))
bp=ax.boxplot([X[c] for c in names],tick_labels=names,patch_artist=True,widths=0.55)
for b in bp['boxes']: b.set(facecolor='#DCE4F5',edgecolor=BLUE)
for m in bp['medians']: m.set(color=NAVY,lw=2)
ax.set_ylabel('Valor en la unidad original'); ax.set_title('Variables en su escala original',loc='left',color=NAVY)
save(f,'g1_boxplots')

# 3 heatmap
R=X.corr()
f,ax=plt.subplots(figsize=(6.4,5.2)); im=ax.imshow(R,cmap='RdBu_r',vmin=-1,vmax=1)
ax.set_xticks(range(8),names,rotation=45,ha='right'); ax.set_yticks(range(8),names)
for i in range(8):
    for j in range(8):
        v=R.iloc[i,j]; ax.text(j,i,f'{v:.2f}'.replace('.',','),ha='center',va='center',fontsize=8,color='white' if abs(v)>0.6 else 'black')
for s in ax.spines.values(): s.set_visible(False)
f.colorbar(im,ax=ax,label='Coeficiente de correlación de Pearson',shrink=0.85); save(f,'g1_heatmap')

# 4 pairs subset
sub=['PM25','NO2','O3','Viento']
f,axs=plt.subplots(4,4,figsize=(7,7))
for i,a in enumerate(sub):
    for j,b in enumerate(sub):
        ax=axs[i,j]
        if i==j: ax.hist(X[a],bins=8,color='#DCE4F5',edgecolor=BLUE)
        else:
            for z,c in ZC.items():
                m=d.zona==z; ax.scatter(X[b][m],X[a][m],s=12,color=c,label=z)
            ax.text(0.05,0.88,f'r = {R.loc[a,b]:.2f}'.replace('.',','),transform=ax.transAxes,fontsize=8)
        if i==3: ax.set_xlabel(b)
        if j==0: ax.set_ylabel(a)
        ax.tick_params(labelsize=7)
h,l=axs[0,1].get_legend_handles_labels(); f.legend(h,l,loc='upper center',ncol=3,frameon=False,bbox_to_anchor=(0.5,1.02))
f.tight_layout(); save(f,'g1_pares')

# 5 geometria ACP con PM25 y Viento estandarizados
Z2=StandardScaler().fit_transform(X[['PM25','Viento']])
p2=PCA().fit(Z2); v1=p2.components_[0]; v2=p2.components_[1]
if v1[0]<0: v1=-v1
f,ax=plt.subplots(figsize=(5.6,5.2))
ax.scatter(Z2[:,0],Z2[:,1],color=BLUE,s=22,zorder=3)
t=np.linspace(-3,3,2)
ax.plot(t*v1[0],t*v1[1],color='#C0392B',lw=2,label=f'CP1 ({p2.explained_variance_ratio_[0]*100:.1f} % de la varianza)'.replace('.',','))
ax.plot(t*v2[0]*0.6,t*v2[1]*0.6,color=ORA,lw=2,label=f'CP2 ({p2.explained_variance_ratio_[1]*100:.1f} %)'.replace('.',','))
k=np.argmax(Z2[:,0]); pt=Z2[k]; proj=(pt@v1)*v1
ax.plot([pt[0],proj[0]],[pt[1],proj[1]],ls=':',color=NAVY); ax.scatter(*proj,color='#C0392B',s=30,zorder=4)
ax.annotate('proyección de una\nestación sobre CP1',xy=proj,xytext=(proj[0]-1.9,proj[1]-1.4),fontsize=8,arrowprops=dict(arrowstyle='->',color=NAVY))
ax.axhline(0,color=GRY,lw=0.5); ax.axvline(0,color=GRY,lw=0.5); ax.set_aspect('equal')
ax.set_xlabel('PM2,5 estandarizado'); ax.set_ylabel('Velocidad del viento estandarizada'); ax.legend(fontsize=8,loc='upper right',frameon=False)
ax.set_xlim(-3,3); ax.set_ylim(-3,3); save(f,'g1_geometria')

# ACP completo
Z=StandardScaler().fit_transform(X); acp=PCA().fit(Z); lam=np.linalg.eigvalsh(R)[::-1]
car=acp.components_.T*np.sqrt(lam); sc=acp.transform(Z); car[:,1]*=-1; sc[:,1]*=-1
ve=100*lam/8
# 6 scree
f,ax=plt.subplots(figsize=(7,3.8))
ax.bar(range(1,9),lam,color='#DCE4F5',edgecolor=BLUE,width=0.6)
ax.plot(range(1,9),lam,marker='o',color=NAVY)
for k,(l,v) in enumerate(zip(lam,ve),1): ax.text(k+0.08,l+0.18,f'λ={l:.2f}\n{v:.1f} %'.replace('.',','),ha='left',fontsize=7.5,color=NAVY)
ax.axhline(1,ls='--',color='#C0392B',lw=1); ax.text(8.5,1.08,'λ = 1 (criterio de Kaiser)',color='#C0392B',fontsize=8,ha='right')
ax.set_xlabel('Componente principal'); ax.set_ylabel('Valor propio (λ)'); ax.set_xticks(range(1,9)); ax.set_ylim(0,6)
ax.annotate('“codo”',xy=(3,lam[2]+0.05),xytext=(3.6,3.0),arrowprops=dict(arrowstyle='->',color=GRY),color=GRY)
save(f,'g1_scree')
# 7 circulo
f,ax=plt.subplots(figsize=(5.6,5.6)); ax.add_patch(plt.Circle((0,0),1,fill=False,color=GRY))
for v,(a,b) in zip(names,car[:,:2]):
    col='#C0392B' if v in ['PM25','PM10','NO2','CO'] else (ORA if v in ['O3','Temp','Humedad'] else NAVY)
    ax.arrow(0,0,a,b,head_width=0.035,length_includes_head=True,color=col,lw=1.4)
    off={'PM25':(0.10,0.07),'CO':(0.13,-0.01),'NO2':(-0.02,0.12),'PM10':(0.14,-0.07)}.get(v,(0,0)); ax.text(a*1.1+off[0],b*1.1+off[1],v,ha='center',va='center',fontsize=9,color=col,weight='bold')
ax.axhline(0,color=GRY,lw=0.5); ax.axvline(0,color=GRY,lw=0.5); ax.set_aspect('equal'); ax.set_xlim(-1.2,1.2); ax.set_ylim(-1.2,1.2)
ax.set_xlabel(f'CP1 ({ve[0]:.1f} %)'.replace('.',',')); ax.set_ylabel(f'CP2 ({ve[1]:.1f} %)'.replace('.',',')); save(f,'g1_circulo')
# 8 individuos
f,ax=plt.subplots(figsize=(6.6,5))
for z,c in ZC.items():
    m=(d.zona==z).values; ax.scatter(sc[m,0],sc[m,1],color=c,label=z,s=28)
    ax.scatter(sc[m,0].mean(),sc[m,1].mean(),marker='s',s=90,color=c,edgecolor='black')
for i in range(30): ax.text(sc[i,0]+0.08,sc[i,1]+0.08,d.estacion[i],fontsize=6.5,color=GRY)
ax.axhline(0,color=GRY,lw=0.5); ax.axvline(0,color=GRY,lw=0.5)
ax.set_xlabel(f'CP1 ({ve[0]:.1f} %)'.replace('.',',')); ax.set_ylabel(f'CP2 ({ve[1]:.1f} %)'.replace('.',',')); ax.legend(frameon=False,title='Zona (■ = centro de la zona)',fontsize=8,title_fontsize=8,loc='upper center',bbox_to_anchor=(0.5,-0.13),ncol=3)
save(f,'g1_individuos')
# 9 biplot
f,ax=plt.subplots(figsize=(6.6,5.4)); s=sc[:,:2]/np.abs(sc[:,:2]).max(0)
for z,c in ZC.items():
    m=(d.zona==z).values; ax.scatter(s[m,0],s[m,1],color=c,label=z,s=20,alpha=0.8)
for v,(a,b) in zip(names,car[:,:2]):
    ax.arrow(0,0,a,b,head_width=0.03,length_includes_head=True,color=NAVY); off={'PM25':(0.08,0.08),'CO':(0.14,0.0),'NO2':(-0.04,0.14),'PM10':(0.14,-0.08)}.get(v,(0,0)); ax.text(a*1.1+off[0],b*1.1+off[1],v,fontsize=8.5,color=NAVY,weight='bold',ha='center')
ax.axhline(0,color=GRY,lw=0.5); ax.axvline(0,color=GRY,lw=0.5); ax.legend(frameon=True,fontsize=8,loc='lower left')
ax.set_xlabel('CP1 (escalado)'); ax.set_ylabel('CP2 (escalado)'); save(f,'g1_biplot')
print('ok', np.round(sc[:,:2].std(0),2))
