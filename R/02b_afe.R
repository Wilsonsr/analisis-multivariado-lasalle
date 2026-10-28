# Unidad 2 · Análisis factorial exploratorio (script opcional en R)
# Paquetes: psych, GPArotation

# Llevémoslo a R: análisis factorial exploratorio
library(psych)
library(GPArotation)

encuesta <- read.csv("../data/datos_guia2_encuesta_salud.csv", fileEncoding = "UTF-8")
items <- encuesta[, 7:15]            # nueve ítems de percepción (escala 1 a 5)

R <- cor(items)
KMO(R)                                # adecuación muestral (global y por ítem)
cortest.bartlett(R, n = nrow(items))  # esfericidad de Bartlett

set.seed(2026)                        # el análisis paralelo usa datos simulados
fa.parallel(items, fa = "fa")         # análisis paralelo sobre la matriz reducida (factores)

afe <- fa(items, nfactors = 3, fm = "minres", rotate = "oblimin")
print(afe$loadings, cutoff = 0.30, sort = TRUE)  # cargas (matriz de patrones)
round(afe$communality, 3)            # comunalidades h²
round(afe$Phi, 2)                    # correlaciones entre factores (rotación oblicua)
round(unclass(afe$Structure), 2)     # matriz de estructura: correlación ítem-factor
fa.diagram(afe)                      # diagrama de la estructura factorial

# Sensibilidad: ítems Likert con correlaciones policóricas (las cargas suelen ser mayores)
afe_poly <- fa(items, nfactors = 3, fm = "minres", rotate = "oblimin", cor = "poly")
print(afe_poly$loadings, cutoff = 0.30, sort = TRUE)
round(afe_poly$communality, 3)
