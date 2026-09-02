"""
Taller 2: Detección y Análisis de Outliers con Rango Intercuartílico (IQR)
Dataset: netflix_titles_para_taller.csv
"""

import os
import numpy as np
import pandas as pd
from scipy import stats

# 1. Carga del conjunto de datos
archivo_csv = 'netflix_titles_para_taller.csv'
if not os.path.exists(archivo_csv):
    archivo_csv = os.path.join(os.path.dirname(__file__), 'netflix_titles_para_taller.csv')

df = pd.read_csv(archivo_csv)

# 2. Tratamiento y ajuste de registros repetidos (duplicados)
# Normalización de título para detectar redundancias con variaciones de espacios/mayúsculas
df['titulo_norm'] = df['title'].astype(str).str.strip().str.lower()
df = df.drop_duplicates(subset=['titulo_norm', 'type'], keep='first').copy()
df.drop(columns=['titulo_norm'], inplace=True)

# 3. Tratamiento y llenado de datos vacíos (nulos)
# Imputación de atributos de texto con valor constante
columnas_texto = ['director', 'cast', 'country']
for col in columnas_texto:
    if col in df.columns:
        df[col] = df[col].fillna('Sin Información')

if 'date_added' in df.columns:
    df['date_added'] = df['date_added'].fillna('Sin Fecha')

if 'rating' in df.columns:
    df['rating'] = df['rating'].fillna(df['rating'].mode()[0])

if 'date_added_year' in df.columns:
    df['date_added_year'] = df['date_added_year'].fillna(df['date_added_year'].median())

# 4. Preparación de la variable continua para el análisis (Películas)
# Filtramos solo registros de tipo 'Movie' para aislar la duración continua en minutos
df1 = df[df['type'] == 'Movie'].copy()

# En caso de nulos en la duración de películas, se completa con la mediana
df1['duration_min'] = df1['duration_min'].fillna(df1['duration_min'].median())

# 5. Calcular los valores, límites y detectar outliers (método IQR visto en clase)
datos = df1['duration_min']
media = datos.mean()
desviacion_estandar = datos.std()
Q1 = datos.quantile(0.25)
Q3 = datos.quantile(0.75)
iqr = Q3 - Q1

limite_inferior = Q1 - 1.5 * iqr
limite_superior = Q3 + 1.5 * iqr

outliers_iqr = df1[(datos < limite_inferior) | (datos > limite_superior)]

# 6. Imprimir resultados organizados (salida solicitada)
print("=" * 35)
print("     ANÁLISIS DE OUTLIERS (IQR)")
print("=" * 35)
print(f"Media:               {media:.2f}")
print(f"Desviación estándar: {desviacion_estandar:.2f}")
print(f"Q1:                  {Q1:.2f}")
print(f"Q3:                  {Q3:.2f}")
print(f"IQR:                 {iqr:.2f}")
print(f"Límite inferior:     {limite_inferior:.2f}")
print(f"Límite superior:     {limite_superior:.2f}")
print("-" * 35)
print("Valores atípicos (Outliers):")
print(outliers_iqr[['title', 'duration_min']])
print("=" * 35)
