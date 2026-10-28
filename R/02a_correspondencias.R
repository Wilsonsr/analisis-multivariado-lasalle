# Unidad 2 · Correspondencias simple y múltiple (script opcional en R)
# Paquetes: FactoMineR, factoextra

# Llevémoslo a R: análisis de correspondencias simple
library(FactoMineR)
library(factoextra)

encuesta <- read.csv("../data/datos_guia2_encuesta_salud.csv", fileEncoding = "UTF-8")
encuesta$nivel_educativo <- factor(encuesta$nivel_educativo,
  levels = c("Primaria", "Secundaria", "Técnica", "Universitaria"))

tabla <- table(encuesta$nivel_educativo, encuesta$regimen)  # tabla de contingencia
tabla
chisq.test(tabla)                    # prueba de independencia chi-cuadrado
round(prop.table(tabla, 1), 3)       # perfiles fila
round(prop.table(tabla, 2), 3)       # perfiles columna

ac <- CA(tabla, graph = FALSE)
round(ac$eig, 3)                     # inercia por dimensión
round(ac$row$contrib, 1)             # contribuciones de las filas (%)
round(ac$col$contrib, 1)             # contribuciones de las columnas (%)
round(ac$row$cos2, 3)                # calidad de representación de las filas
fviz_ca_biplot(ac, repel = TRUE)     # mapa simétrico de correspondencias

# Llevémoslo a R: análisis de correspondencias múltiple
library(FactoMineR)
library(factoextra)

encuesta <- read.csv("../data/datos_guia2_encuesta_salud.csv", fileEncoding = "UTF-8")
vars <- c("zona", "nivel_educativo", "regimen", "consulta_preventiva", "percepcion_calidad")
datos_acm <- encuesta[, vars]
datos_acm[] <- lapply(datos_acm, factor)      # todas las variables como factores

sapply(datos_acm, table)                      # frecuencias de cada categoría

acm <- MCA(datos_acm, graph = FALSE)
round(head(acm$eig, 6), 3)                    # inercia por dimensión
round(acm$var$contrib[, 1:2], 1)              # contribución de las categorías (%)
round(acm$var$eta2[, 1:2], 3)                 # relación de cada variable con las dimensiones
fviz_screeplot(acm, addlabels = TRUE)
fviz_mca_var(acm, repel = TRUE)               # mapa de categorías
fviz_mca_var(acm, choice = "mca.cor")         # variables según su eta²
