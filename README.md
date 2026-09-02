# Proyecto de Minería de Datos: Análisis y Preprocesamiento de Netflix

Repositorio central para el desarrollo de los talleres prácticos de Minería de Datos aplicados sobre el catálogo de contenidos audiovisuales de Netflix.

---

## 📑 Índice de Talleres

| Taller | Tema Principal | Archivo Fuente | Script Principal | Enlace al Informe |
|---|---|---|---|---|
| **Taller 1** | Calidad de Datos, Limpieza e Imputación Comparativa | `netflix_titles.csv` | [`solucion_taller.py`](taller%201/solucion_taller.py) | 📘 [**README Taller 1**](taller%201/README.md) |
| **Taller 2** | Ajuste de Duplicados y Detección de Outliers (IQR) | `netflix_titles_para_taller.csv` | [`taller_outliers_netflix.py`](taller%202/taller_outliers_netflix.py) | 📙 [**README Taller 2**](taller%202/README.md) |

---

### 📘 [Taller 1: Calidad de Datos, Limpieza e Imputación](taller%201/README.md)
* **Objetivo**: Diagnóstico integral de calidad de datos, resolución de anomalías estructurales y evaluación de técnicas de imputación.
* **Aspectos clave abordados**:
  1. Identificación de los 5 problemas críticos de calidad (nulos en `director`, `cast`, `country`, inconsistencia en `date_added`, etc.).
  2. Corrección del desplazamiento de celdas entre `rating` y `duration` (ej. registros de comedia con minutos en rating).
  3. Descomposición atómica de variables compuestas (`duration_min` y `duration_seasons`).
  4. Benchmark experimental controlado (10% nulos MCAR): comparación de **Media vs. Mediana vs. KNN Imputer ($K=5$)**.
  5. Imputación categórica: análisis del efecto sesgo de imputar la moda vs. etiqueta constante (`"Sin Información"`).
* **Acceso directo**: 👉 [Ver documentación y entrega de Taller 1](taller%201/README.md)

---

### 📙 [Taller 2: Detección y Análisis de Outliers (IQR)](taller%202/README.md)
* **Objetivo**: Limpieza de duplicados, llenado de nulos residuales y detección robusta de valores atípicos con Rango Intercuartílico (IQR).
* **Aspectos clave abordados**:
  1. Detección y ajuste de registros repetidos con variaciones tipográficas o de espacios.
  2. Llenado y saneamiento de campos vacíos.
  3. Implementación limpia en Python usando Pandas, NumPy y SciPy para calcular cuartiles ($Q_1$, $Q_3$), $IQR$ y umbrales.
  4. Identificación de **450 valores atípicos** en películas:
     - **Extremo inferior ($< 46.50\text{ min}$)**: Cortometrajes, especiales infantiles y documentales breves.
     - **Extremo superior ($> 154.50\text{ min}$)**: Superproducciones épicas y películas de Bollywood con números musicales.
  5. Análisis detallado de los datos salientes y conclusiones técnicas de minería de datos.
* **Acceso directo**: 👉 [Ver documentación de Taller 2](taller%202/README.md) | [Ver Análisis Detallado de Datos Salientes](taller%202/ANALISIS_OUTLIERS.md)

---

## 📂 Estructura del Repositorio

```text
proyecto_netflix/
│
├── README.md                              <- Este archivo (Índice y portal general)
│
├── taller 1/                              <- CARPETA TALLER 1
│   ├── README.md                          <- Informe completo de Calidad e Imputación
│   ├── solucion_taller.py                 <- Script integral de preprocesamiento e imputación
│   ├── netflix_titles.csv                 <- Dataset original crudo de Kaggle
│   ├── netflix_titles_cleaned.csv         <- Dataset resultante saneado
│   └── netflix_titles_para_taller.csv     <- Dataset base para el taller 2
│
└── taller 2/                              <- CARPETA TALLER 2
    ├── README.md                          <- Guía, metodología y resultados del Taller 2
    ├── ANALISIS_OUTLIERS.md               <- Análisis profundo de datos salientes y conclusiones
    ├── taller_outliers_netflix.py         <- Script Python limpio de análisis IQR
    ├── netflix_titles_para_taller.csv     <- Dataset utilizado en el análisis
    └── netflix_titles.csv                 <- Dataset complementario
```

---

## 🛠️ Requisitos de Ejecución

Para reproducir cualquiera de los talleres, asegúrate de contar con Python 3.8+ y las siguientes librerías instaladas:

```bash
pip install numpy pandas scipy scikit-learn
```

### Ejecución rápida:

* **Taller 1**:
  ```bash
  cd "taller 1"
  python solucion_taller.py
  ```

* **Taller 2**:
  ```bash
  cd "taller 2"
  python taller_outliers_netflix.py
  ```
