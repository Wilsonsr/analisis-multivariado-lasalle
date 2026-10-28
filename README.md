# Análisis Multivariado · Cuadernos y datos del curso

Material de código del espacio académico **Análisis Multivariado** del Programa de Ciencia de Datos (pregrado, modalidad virtual) de la Universidad de La Salle. Complementa las tres guías de desarrollo temático del curso y prepara cada avance del proyecto de aula *De los datos a las decisiones*.

Autor: **Wilson Sandoval Rodríguez** (2026).

> Los conjuntos de datos son **simulados con fines didácticos**. Reproducen relaciones plausibles entre variables, pero no corresponden a mediciones, encuestas ni clientes reales.

## Cuadernos

Ábrelos directamente en Google Colab (no necesitas instalar nada):

| Unidad | Cuaderno | Técnicas | Abrir |
|---|---|---|---|
| 1 | `01_fundamentos_y_ACP.ipynb` | Matriz de datos, vector de medias, covarianzas y correlaciones, atípicos, ACP | [![Abrir en Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/wilsonsr/analisis-multivariado-lasalle/blob/main/notebooks/01_fundamentos_y_ACP.ipynb) |
| 2 | `02a_correspondencias_simple_y_multiple.ipynb` | Tablas de contingencia, perfiles, ACS, ACM, inercia ajustada | [![Abrir en Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/wilsonsr/analisis-multivariado-lasalle/blob/main/notebooks/02a_correspondencias_simple_y_multiple.ipynb) |
| 2 | `02b_analisis_factorial_exploratorio.ipynb` | KMO, Bartlett, análisis paralelo, AFE, rotaciones, patrones y estructura | [![Abrir en Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/wilsonsr/analisis-multivariado-lasalle/blob/main/notebooks/02b_analisis_factorial_exploratorio.ipynb) |
| 3 | `03a_conglomerados_jerarquicos_y_kmeans.ipynb` | Distancias, Ward, dendrograma, k-means, silueta, estabilidad | [![Abrir en Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/wilsonsr/analisis-multivariado-lasalle/blob/main/notebooks/03a_conglomerados_jerarquicos_y_kmeans.ipynb) |
| 3 | `03b_analisis_discriminante.ipynb` | Análisis discriminante lineal y cuadrático, validación cruzada, métricas | [![Abrir en Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/wilsonsr/analisis-multivariado-lasalle/blob/main/notebooks/03b_analisis_discriminante.ipynb) |

Cada cuaderno sigue la lógica de las guías: explicación breve, código comentado, un bloque **«¿Qué observar?»** después de cada resultado y un ejercicio **«Tu turno»** con una solución posible.

## Estructura del repositorio

```
├── notebooks/   cuadernos de Python (material principal), guardados con sus salidas
├── data/        datos simulados del curso y su diccionario (data/README.md)
├── R/           scripts equivalentes en R (complemento opcional)
├── figuras/     scripts que regeneran las figuras de las guías (PNG y SVG)
├── requirements.txt
├── LICENSE              licencia MIT (código)
└── LICENSE-CONTENIDO.md licencia CC BY-NC-SA 4.0 (textos y datos)
```

## Uso local

```bash
git clone https://github.com/wilsonsr/analisis-multivariado-lasalle.git
cd analisis-multivariado-lasalle
python -m venv .venv
source .venv/bin/activate        # en Windows: .venv\Scripts\activate
pip install -r requirements.txt
jupyter lab notebooks/
```

Los cuadernos buscan los datos en `data/`; si no los encuentran (por ejemplo, en Colab), los descargan desde este repositorio.

## Versiones y reproducibilidad

Los cuadernos se ejecutaron de principio a fin, sin errores, con las versiones fijadas en `requirements.txt` (Python 3.13, NumPy 2.5.4, pandas 3.1.0, SciPy 1.18.1, scikit-learn 1.9.1, prince 0.23.1). Las cifras que aparecen en las guías provienen de esas ejecuciones. Con otras versiones puede cambiar el **signo** de un componente o de una función discriminante (los cuadernos orientan los signos con una regla basada en los datos) o los últimos decimales.

- **factor_analyzer:** la versión 0.5.1 publicada en PyPI no funciona con scikit-learn 1.8 o posterior. Se instala la versión corregida del repositorio oficial, fijada en un *commit* concreto (ver `requirements.txt`).
- **R y Python:** con R 4.3.3 (FactoMineR 2.9, psych 2.4.1, MASS 7.3-60, cluster 2.1.6) se obtienen los mismos resultados, salvo signos y diferencias en el segundo decimal cuando la estandarización usa $n-1$ (`scale()` en R) en lugar de $n$ (`StandardScaler` en Python).

## Scripts de R (opcionales)

La carpeta `R/` contiene el mismo análisis de cada cuaderno en R. Ejecútalos desde esa carpeta. Paquetes: `FactoMineR`, `factoextra`, `corrplot`, `psych`, `GPArotation`, `cluster` y `MASS`.

```r
install.packages(c("FactoMineR", "factoextra", "corrplot", "psych", "GPArotation", "cluster"))
```

## Relación con el proyecto de aula

| Avance del proyecto | Cuadernos de apoyo |
|---|---|
| Actividad 1: exploración multivariada y ACP | 01 |
| Actividad 2: asociaciones y estructuras latentes | 02a (variables categóricas) o 02b (variables cuantitativas) |
| Actividad 3: segmentación, clasificación e informe final | 03a y 03b |

## Licencia y cita

- Código: [MIT](LICENSE).
- Textos de los cuadernos y datos: [CC BY-NC-SA 4.0](LICENSE-CONTENIDO.md).

Cita sugerida: Sandoval Rodríguez, W. (2026). *Análisis Multivariado: cuadernos y datos del curso* [Repositorio de GitHub]. Programa de Ciencia de Datos, Universidad de La Salle. https://github.com/wilsonsr/analisis-multivariado-lasalle
