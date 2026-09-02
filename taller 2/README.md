# Taller 2: Detección y Análisis de Outliers con Rango Intercuartílico (IQR)

**Curso**: Minería de Datos  
**Dataset**: `netflix_titles_para_taller.csv`  
**Script Principal**: [`taller_outliers_netflix.py`](taller_outliers_netflix.py)  
**Informe Detallado**: [`ANALISIS_OUTLIERS.md`](ANALISIS_OUTLIERS.md)  

---

## 1. Descripción del Taller

En este taller se aplica la metodología no paramétrica del **Rango Intercuartílico (IQR)** para detectar y caracterizar valores atípicos (*outliers*) en variables numéricas continuas del catálogo de Netflix, partiendo de los datos transformados en el archivo `netflix_titles_para_taller.csv`.

El flujo de trabajo incluye:
1. **Ajuste de datos repetidos**: Normalización y eliminación de duplicados lógicos.
2. **Llenado de datos vacíos**: Imputación de atributos con constantes (`"Sin Información"`, `"Sin Fecha"`), moda y mediana.
3. **Detección de outliers**: Aplicación del modelo estadístico IQR sobre la variable de duración de películas (`duration_min`).
4. **Análisis de datos salientes**: Interpretación cualitativa y cuantitativa de los valores atípicos detectados.

---

## 2. Ejecución del Código

Para ejecutar el análisis sin salidas ruidosas (únicamente el bloque de resultados estadísticos):

```bash
cd "taller 2"
python taller_outliers_netflix.py
```

---

## 3. Resultados Obtenidos (Salida de Consola)

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
                                title  duration_min
22                    Avvai Shanmughi         161.0
24                              Jeans         166.0
45             My Heroes Were Cowboys          23.0
71        A StoryBots Space Adventure          13.0
73                       King of Boys         182.0
...                               ...           ...
8763  WWII: Report from the Aleutians          45.0
8764                       Wyatt Earp         191.0
8770                          Yaadein         171.0
8788                     You Carry Me         157.0
8802                           Zodiac         158.0

[450 rows x 2 columns]
===================================
```

---

## 4. Métricas Estadísticas Principales

* **$Q_1$ (Cuartil 25%)**: $87.00\text{ min}$ — El 25% de las producciones dura 87 minutos o menos.
* **$Q_3$ (Cuartil 75%)**: $114.00\text{ min}$ — El 75% de las producciones dura 114 minutos o menos.
* **IQR ($Q_3 - Q_1$)**: $27.00\text{ min}$ — Rango del 50% central de las películas.
* **Límite Inferior ($Q_1 - 1.5 \times IQR$)**: $46.50\text{ min}$ — Identifica cortometrajes y especiales (ej. 13 min, 23 min).
* **Límite Superior ($Q_3 + 1.5 \times IQR$)**: $154.50\text{ min}$ — Identifica superproducciones épicas y cine de Bollywood (ej. 165 min, 182 min, 229 min).
* **Total de Outliers**: **450 títulos** de 6,128 películas (**7.34%** del catálogo de películas).

---

## 5. Conclusiones

1. **Eficiencia del IQR**: El Rango Intercuartílico demostró ser la técnica ideal para esta variable, ya que no se ve distorsionada por duraciones extremas como películas de 3 min o 312 min.
2. **Naturaleza de los Outliers**: Los 450 datos atípicos no corresponden a fallos de captura o errores del sistema, sino a formatos específicos del catálogo (cortometrajes infantiles y documentales en el extremo inferior, vs. cine épico y películas indias con intermedios en el extremo superior).
3. Para una discusión detallada, consulta el informe complementario: [`ANALISIS_OUTLIERS.md`](ANALISIS_OUTLIERS.md).
