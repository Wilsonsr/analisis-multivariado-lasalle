# Unidad 3 · Conglomerados jerárquicos y k-means (script opcional en R)
# Paquete: cluster

# Llevémoslo a R: conglomerados jerárquicos
library(cluster)

clientes <- read.csv("../data/datos_guia3_clientes.csv")
X <- scale(clientes[, 2:7])            # estandarizar: variables en escalas distintas

D <- dist(X, method = "euclidean")     # matriz de distancias (120 x 120)
round(as.matrix(D)[1:5, 1:5], 2)       # vistazo a las primeras distancias

hc <- hclust(D, method = "ward.D2")    # enlace de Ward
plot(hc, labels = FALSE, hang = -1, main = "Dendrograma (Ward)")
rect.hclust(hc, k = 4, border = "red") # marca la partición en 4 grupos

tail(round(hc$height, 2), 6)           # alturas de las últimas fusiones

# Índice de silueta promedio para k = 2, ..., 6
for (k in 2:6) {
  g <- cutree(hc, k = k)
  s <- mean(silhouette(g, D)[, "sil_width"])
  cat("k =", k, " silueta =", round(s, 3), "\n")
}
grupos_hc <- cutree(hc, k = 4)
table(grupos_hc)

# Llevémoslo a R: k-means, perfiles y comparación con la solución jerárquica
clientes <- read.csv("../data/datos_guia3_clientes.csv")
X <- scale(clientes[, 2:7])

set.seed(2026)                                   # reproducibilidad
km <- kmeans(X, centers = 4, nstart = 25)        # 25 arranques aleatorios
km$size                                          # tamaño de cada grupo
round(km$centers, 2)                             # centroides (escala estandarizada)
round(km$betweenss / km$totss, 3)                # proporción de variabilidad entre grupos

# Método del codo: suma de cuadrados intragrupo para k = 1, ..., 8
wss <- sapply(1:8, function(k) kmeans(X, k, nstart = 25)$tot.withinss)
plot(1:8, wss, type = "b", xlab = "k", ylab = "Suma de cuadrados intragrupo")

# Perfiles en unidades originales (medias por grupo)
round(aggregate(clientes[, 2:7], by = list(grupo = km$cluster), FUN = mean), 1)

# Comparación con la solución jerárquica (tabla cruzada de asignaciones)
hc <- hclust(dist(X), method = "ward.D2")
table(jerarquico = cutree(hc, 4), kmeans = km$cluster)
