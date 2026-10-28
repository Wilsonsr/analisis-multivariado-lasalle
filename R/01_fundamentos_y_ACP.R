# Unidad 1 · Fundamentos y ACP (script opcional en R; complemento del cuaderno 01)
# Ejecuta desde la carpeta R/ del repositorio. Paquetes: FactoMineR, factoextra, corrplot

# Llevémoslo a R: matriz de datos, vector de medias, covarianzas y correlaciones
datos <- read.csv("../data/datos_guia1_calidad_aire.csv")
str(datos)                          # estructura: tipo de cada variable
X <- datos[, 3:10]                  # variables cuantitativas (sin estacion ni zona)

colSums(is.na(X))                   # valores faltantes por variable
round(colMeans(X), 2)               # vector de medias
round(cov(X), 2)                    # matriz de varianzas y covarianzas
R <- cor(X)                         # matriz de correlaciones de Pearson
round(R, 2)

# Mapa de calor de correlaciones (paquete corrplot)
library(corrplot)
corrplot(R, method = "color", type = "upper", addCoef.col = "black",
         tl.col = "black", number.cex = 0.7)

# Llevémoslo a R: ACP con FactoMineR y gráficos con factoextra
library(FactoMineR)
library(factoextra)

datos <- read.csv("../data/datos_guia1_calidad_aire.csv")
datos$zona <- factor(datos$zona)

# scale.unit = TRUE: ACP sobre la matriz de correlaciones (datos estandarizados)
# quali.sup = 1: zona (1.a columna tras quitar "estacion") es variable suplementaria:
# se proyecta en el plano, pero no participa en el cálculo de los componentes
acp <- PCA(datos[, -1], scale.unit = TRUE, quali.sup = 1, graph = FALSE)

round(acp$eig, 2)                     # valores propios y varianza explicada
round(acp$var$coord[, 1:2], 3)        # cargas: correlación variable-componente
round(acp$var$contrib[, 1:2], 1)      # contribuciones (%) de cada variable
round(acp$var$cos2[, 1:2], 3)         # calidad de representación

fviz_eig(acp, addlabels = TRUE)                       # gráfico de sedimentación
fviz_pca_var(acp, col.var = "contrib", repel = TRUE)  # círculo de correlaciones
fviz_pca_ind(acp, habillage = "zona", addEllipses = TRUE, repel = TRUE)  # individuos
fviz_pca_biplot(acp, habillage = "zona", repel = TRUE)                   # biplot
