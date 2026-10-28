# Unidad 3 · Análisis discriminante (script opcional en R)
# Paquete: MASS

# Llevémoslo a R: análisis discriminante lineal
library(MASS)

clientes <- read.csv("../data/datos_guia3_clientes.csv")
clientes$estado_6m <- factor(clientes$estado_6m)
table(clientes$estado_6m)                        # tamaño de los grupos

modelo <- lda(estado_6m ~ recencia_dias + frecuencia_anual + ticket_promedio +
                antiguedad_meses + visitas_mes + devoluciones_pct, data = clientes)
modelo$prior                                     # probabilidades a priori
round(modelo$svd^2 / sum(modelo$svd^2), 3)       # proporción de separación por función

# Coeficientes estandarizados: comparables entre variables
X <- scale(clientes[, 2:7])
modelo_z <- lda(X, grouping = clientes$estado_6m)
round(modelo_z$scaling, 3)

# Validación cruzada dejando uno fuera (CV = TRUE)
cv <- lda(estado_6m ~ recencia_dias + frecuencia_anual + ticket_promedio +
            antiguedad_meses + visitas_mes + devoluciones_pct, data = clientes, CV = TRUE)
confusion <- table(real = clientes$estado_6m, predicho = cv$class)
confusion
round(sum(diag(confusion)) / sum(confusion), 3)  # tasa de aciertos global
round(diag(confusion) / rowSums(confusion), 3)   # tasa de aciertos por grupo

plot(modelo, col = as.integer(clientes$estado_6m))  # individuos en las funciones discriminantes

# Matriz de estructura: correlación entre cada variable y cada función discriminante
round(cor(X, predict(modelo_z)$x), 2)

# Revisión de la homogeneidad de dispersiones y comparación con el discriminante cuadrático
aggregate(clientes[, 2:7], by = list(estado = clientes$estado_6m), FUN = function(v) round(sd(v), 1))
cv_q <- qda(estado_6m ~ recencia_dias + frecuencia_anual + ticket_promedio +
              antiguedad_meses + visitas_mes + devoluciones_pct, data = clientes, CV = TRUE)
round(mean(cv_q$class == clientes$estado_6m), 3)  # aciertos del cuadrático con validación cruzada
