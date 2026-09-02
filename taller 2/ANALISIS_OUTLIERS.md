# Análisis Estadístico de Datos Salientes y Detección de Outliers (IQR)

**Taller**: Minería de Datos - Taller 2  
**Dataset Fuente**: `netflix_titles_para_taller.csv`  
**Variable Analizada**: `duration_min` (Duración en minutos para películas)  

---

## 1. Contexto y Preprocesamiento de Datos

Antes de realizar el análisis estadístico y la detección de anomalías, el conjunto de datos fue sometido a un proceso de saneamiento:
1. **Ajuste de Duplicados**: Se detectaron y eliminaron registros lógicamente duplicados por título y tipo (diferencias de espaciado o mayúsculas/minúsculas), reduciendo el dataset a 8,803 registros limpios.
2. **Llenado de Datos Vacíos (Nulos)**:
   - Atributos textuales (`director`, `cast`, `country`) se estandarizaron con la constante `"Sin Información"`.
   - La columna `date_added` se completó con `"Sin Fecha"`.
   - La columna categórica de clasificación (`rating`) se completó con su categoría dominante (moda: `"TV-MA"`).
   - En caso de nulos en variables temporales o continuas, se utilizó la mediana para evitar introducir sesgos.
3. **Segmentación por Tipo**: Se aisló el subconjunto de **6,128 películas**, permitiendo evaluar la variable continua de duración (`duration_min`) de forma homogénea (separada de las series de TV medidas en temporadas).

---

## 2. Resultados de Salida del Modelo IQR

Al aplicar la técnica no paramétrica del **Rango Intercuartílico (IQR)** sobre la duración de las películas, se obtuvieron las siguientes métricas estadísticas:

| Métrica Estadística | Valor Obtenido | Interpretación en el Dominio |
|---|---|---|
| **Media ($\mu$)** | **99.56 min** | Duración promedio global de una película en el catálogo. |
| **Desviación Estándar ($\sigma$)** | **28.30 min** | Dispersión considerable respecto al promedio. |
| **Primer Cuartil ($Q_1$)** | **87.00 min** | El 25% de las películas dura 87 minutos o menos. |
| **Tercer Cuartil ($Q_3$)** | **114.00 min** | El 75% de las películas dura 114 minutos o menos (el 25% dura más). |
| **Rango Intercuartílico ($IQR$)** | **27.00 min** | Amplitud donde se concentra el 50% central de la muestra ($114 - 87$). |
| **Límite Inferior ($Q_1 - 1.5 \times IQR$)** | **46.50 min** | Umbral mínimo; duraciones inferiores se consideran valores atípicos. |
| **Límite Superior ($Q_3 + 1.5 \times IQR$)** | **154.50 min** | Umbral máximo; duraciones superiores se consideran valores atípicos. |

```text
===================================
     ANÁLISIS DE OUTLIERS (IQR)
===================================
Media:               99.56
Desviación estándar: 28.30
Q1:                  87.00
Q3:                  114.00
IQR:                 27.00
Límite inferior:     46.50
Límite superior:     154.50
-----------------------------------
Valores atípicos (Outliers):
Total detectados: 450 de 6128 películas (7.34%)
===================================
```

---

## 3. Análisis de los Datos Salientes (Valores Atípicos)

Se identificaron **450 películas atípicas** (aproximadamente el **7.34%** del total de películas analizadas). Estos registros se dividen en dos grupos con comportamientos bien diferenciados:

### A. Valores Atípicos Inferiores ($< 46.50\text{ minutos}$)
* **Naturaleza de los datos**: No corresponden a errores de carga, sino a piezas de contenido especial de corta duración que Netflix clasifica en la categoría `Movie`.
* **Subformatos identificados**:
  - **Cortometrajes y especiales infantiles**: Títulos como *A StoryBots Space Adventure* (13 min), *Canvas* (9 min) o *Cops and Robbers* (8 min).
  - **Mediometrajes y documentales breves**: Títulos como *My Heroes Were Cowboys* (23 min) o reportajes históricos de guerra como *WWII: Report from the Aleutians* (45 min).

### B. Valores Atípicos Superiores ($> 154.50\text{ minutos}$)
* **Naturaleza de los datos**: Obras que superan las 2 horas y media de duración, características de producciones de gran escala o patrones cinematográficos regionales específicos.
* **Subformatos identificados**:
  - **Cine de Bollywood e India**: Producciones como *Avvai Shanmughi* (161 min), *Jeans* (166 min) o *Yaadein* (171 min). En esta industria, la duración extendida es un estándar comercial que incorpora pausas y números musicales.
  - **Grandes clásicos y dramas épicos**: Obras maestras de larga duración como *Once Upon a Time in America* (229 min), *Magnolia* (189 min), *Wyatt Earp* (191 min), *Django Unchained* (165 min) y *Zodiac* (158 min).
  - **Contenido interactivo/experimental**: *Black Mirror: Bandersnatch* (312 min), cuya duración en catálogo suma el tiempo de todas las bifurcaciones y rutas posibles.

---

## 4. Conclusión

1. **Robustez del Método IQR**: A diferencia de los métodos paramétricos que asumen una distribución normal perfecta (como el puntaje Z o $\mu \pm 3\sigma$), el método del Rango Intercuartílico demostró ser adecuado para esta variable continua, ya que no se ve distorsionado por las duraciones extremas (desde 3 hasta 312 minutos).
2. **Validez e Integridad de los Outliers**: En este dataset, los valores atípicos detectados representan **información de negocio real y válida** (cortometrajes, cine internacional y epopeyas históricas) en lugar de fallas o corrupciones en la toma de datos. Por lo tanto, no deben ser eliminados de manera indiscriminada en análisis posteriores, sino tratados según el objetivo del modelo (por ejemplo, segmentando entre largometrajes estándar y formatos especiales).
3. **Importancia de la Limpieza Previa**: Estandarizar títulos para remover duplicados y asegurar la imputación controlada de vacíos garantiza que los cuartiles calculados ($Q_1$ y $Q_3$) reflejen fielmente la estructura del catálogo sin sesgos artificiales.
