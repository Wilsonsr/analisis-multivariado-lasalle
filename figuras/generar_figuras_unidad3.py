# Genera las figuras de la guía de la Unidad 3 (PNG y SVG editables). Ejecutar desde la carpeta figuras/.
import numpy as np, pandas as pd, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score, confusion_matrix
from sklearn.decomposition import PCA
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.model_selection import cross_val_predict, LeaveOneOut
from scipy.cluster.hierarchy import linkage, dendrogram, fcluster
from scipy.spatial.distance import pdist, squareform
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.spines.top':False,'axes.spines.right':False,'savefig.dpi':200})
NAVY='#113054'; BLUE='#3B64B4'; YEL='#F6CD46'; ORA='#E8A33D'; GRY='#8A93A6'; RED='#C0392B'; GRN='#2E8B57'
def save(f,n): f.savefig(f'unidad3/{n}.png',bbox_inches='tight'); f.savefig(f'unidad3/{n}.svg',bbox_inches='tight'); plt.close(f)
d=pd.read_csv('../data/datos_guia3_clientes.csv'); V=d.columns[1:7]; X=StandardScaler().fit_transform(d[V])
# 1 matriz de distancias (12 clientes)
D=squareform(pdist(X[:12])); lab=d.cliente[:12]
f,ax=plt.subplots(figsize=(6.6,5.6)); im=ax.imshow(D,cmap='Blues')
ax.set_xticks(range(12),lab,rotation=90,fontsize=8); ax.set_yticks(range(12),lab,fontsize=8)
for i in range(12):
    for j in range(12): ax.text(j,i,f'{D[i,j]:.1f}'.replace('.',','),ha='center',va='center',fontsize=6.5,color='white' if D[i,j]>4 else NAVY)
for s in ax.spines.values(): s.set_visible(False)
f.colorbar(im,ax=ax,shrink=0.8,label='Distancia euclidiana (datos estandarizados)'); save(f,'g3_distancias')
# 2 dendrograma
Z=linkage(X,'ward')
f,ax=plt.subplots(figsize=(9,4.2))
dendrogram(Z,no_labels=True,color_threshold=10,above_threshold_color=GRY,ax=ax)
ax.axhline(10,ls='--',color=RED); ax.text(ax.get_xlim()[1]*0.99,10.4,'corte: 4 grupos',color=RED,ha='right',fontsize=9)
ax.set_ylabel('Altura de fusión (Ward)'); ax.set_xlabel('Clientes (120)'); save(f,'g3_dendrograma')
# 3 selección k: codo + silueta
ks=range(1,9); wss=[KMeans(k,n_init=25,random_state=2026).fit(X).inertia_ for k in ks]
sil=[silhouette_score(X,fcluster(Z,k,'maxclust')) for k in range(2,7)]
f,axs=plt.subplots(1,3,figsize=(11,3.4))
h=Z[-7:,2][::-1]; axs[0].bar(range(1,8),h,color=['#DCE4F5']*7,edgecolor=BLUE); axs[0].set_xticks(range(1,8),[f'{k+1}→{k}' for k in range(1,8)],fontsize=8)
axs[0].set_title('Alturas de las últimas fusiones',fontsize=10,color=NAVY); axs[0].set_xlabel('Paso (grupos antes → después)'); axs[0].annotate('salto: de 4,5\n(5→4) a 15,8 (4→3)',xy=(3.5,10),xytext=(4.3,14),arrowprops=dict(arrowstyle='->',color=RED),color=RED,fontsize=8)
axs[1].plot(ks,wss,marker='o',color=NAVY); axs[1].set_title('Método del codo (k-means)',fontsize=10,color=NAVY); axs[1].set_xlabel('k'); axs[1].set_ylabel('Suma de cuadrados intragrupo'); axs[1].scatter([4],[wss[3]],s=120,facecolor='none',edgecolor=RED)
axs[2].bar(range(2,7),sil,color=[RED if k==4 else '#DCE4F5' for k in range(2,7)],edgecolor=BLUE); axs[2].set_title('Silueta promedio (Ward)',fontsize=10,color=NAVY); axs[2].set_xlabel('k')
for k,s in zip(range(2,7),sil): axs[2].text(k,s+0.01,f'{s:.3f}'.replace('.',','),ha='center',fontsize=8)
axs[2].set_ylim(0,0.6); f.tight_layout(); save(f,'g3_numero_grupos')
# 4 clusters en plano ACP
km=KMeans(4,n_init=25,random_state=2026).fit(X); lab_km=km.labels_
cents=pd.DataFrame(km.cluster_centers_,columns=V)
orig=d.groupby(lab_km)[list(V)].mean()
def name(i):
    r=orig.loc[i]
    if r.recencia_dias>90: return 'En riesgo de abandono'
    if r.antiguedad_meses<12: return 'Nuevos exploradores'
    if r.frecuencia_anual>18: return 'Frecuentes de alto valor'
    return 'Ocasionales de ticket alto'
names={i:name(i) for i in range(4)}; COL={'Frecuentes de alto valor':GRN,'Nuevos exploradores':BLUE,'Ocasionales de ticket alto':ORA,'En riesgo de abandono':RED}
pca=PCA(2).fit(X); S=pca.transform(X); C=pca.transform(km.cluster_centers_)
f,ax=plt.subplots(figsize=(7,5.2))
for i in range(4):
    m=lab_km==i; ax.scatter(S[m,0],S[m,1],s=22,color=COL[names[i]],label=f'{names[i]} (n = {m.sum()})',alpha=0.85)
    ax.scatter(C[i,0],C[i,1],marker='X',s=180,color=COL[names[i]],edgecolor='black')
ax.axhline(0,color=GRY,lw=0.5); ax.axvline(0,color=GRY,lw=0.5)
ev=pca.explained_variance_ratio_*100
ax.set_xlabel(f'CP1 ({ev[0]:.1f} %)'.replace('.',',')); ax.set_ylabel(f'CP2 ({ev[1]:.1f} %)'.replace('.',',')); ax.legend(frameon=False,fontsize=8,loc='best',title='Grupo k-means (X = centroide)',title_fontsize=8)
save(f,'g3_clusters')
# 5 centroides perfil
order=['Frecuentes de alto valor','Ocasionales de ticket alto','Nuevos exploradores','En riesgo de abandono']
inv={v:k for k,v in names.items()}
f,ax=plt.subplots(figsize=(8.5,3.8))
for nm in order:
    ax.plot(range(6),cents.loc[inv[nm]],marker='o',color=COL[nm],label=nm,lw=2)
ax.axhline(0,color=GRY,lw=0.8,ls='--'); ax.set_xticks(range(6),['Recencia','Frecuencia','Ticket','Antigüedad','Visitas','Devoluciones'])
ax.set_ylabel('Centroide (desviaciones respecto a la media)'); ax.legend(frameon=False,fontsize=8,ncol=2,loc='upper center',bbox_to_anchor=(0.5,1.2)); save(f,'g3_centroides')
# 6 matriz de confusión
y=d.estado_6m; et=['Activo','Inactivo','Retirado']
pred=cross_val_predict(LinearDiscriminantAnalysis(),X,y,cv=LeaveOneOut()); M=confusion_matrix(y,pred,labels=et)
f,ax=plt.subplots(figsize=(5.4,4.4)); ax.imshow(M/M.sum(1,keepdims=True),cmap='Blues',vmin=0,vmax=1)
for i in range(3):
    for j in range(3): ax.text(j,i,f'{M[i,j]}\n({100*M[i,j]/M[i].sum():.1f} %)'.replace('.',','),ha='center',va='center',fontsize=9,color='white' if i==j else NAVY)
ax.set_xticks(range(3),et); ax.set_yticks(range(3),et); ax.set_xlabel('Clase predicha (validación cruzada)'); ax.set_ylabel('Clase real')
for s in ax.spines.values(): s.set_visible(False)
save(f,'g3_confusion')
# 7 funciones discriminantes
lda=LinearDiscriminantAnalysis().fit(X,y); L=lda.transform(X)
# alinear signos con R: Retirado positivo en LD1, Inactivo negativo en LD2
if L[y=='Retirado',0].mean()<0: L[:,0]*=-1
if L[y=='Inactivo',1].mean()>0: L[:,1]*=-1
CC={'Activo':GRN,'Inactivo':ORA,'Retirado':RED}
f,ax=plt.subplots(figsize=(7,5))
for c in et:
    m=(y==c).values; ax.scatter(L[m,0],L[m,1],s=24,color=CC[c],label=c,alpha=0.85); ax.scatter(L[m,0].mean(),L[m,1].mean(),marker='X',s=180,color=CC[c],edgecolor='black')
ax.axhline(0,color=GRY,lw=0.5); ax.axvline(0,color=GRY,lw=0.5)
r=lda.explained_variance_ratio_*100
ax.set_xlabel(f'Función discriminante 1 ({r[0]:.1f} % de la separación)'.replace('.',',')); ax.set_ylabel(f'Función discriminante 2 ({r[1]:.1f} %)'.replace('.',','))
ax.legend(frameon=False,title='Estado a 6 meses (X = centroide)',fontsize=8,title_fontsize=8); save(f,'g3_discriminante')
print(names, pca.explained_variance_ratio_.round(3))
print(pd.crosstab(lab_km,y).rename(index=names))
