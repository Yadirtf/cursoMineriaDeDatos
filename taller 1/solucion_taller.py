"""
Solución Completa del Taller de Minería de Datos - Dataset Netflix Titles
Autor: Experto en Minería de Datos
"""

import pandas as pd
import numpy as np
from sklearn.impute import KNNImputer
from sklearn.metrics import mean_absolute_error, mean_squared_error

def main():
    print("=========================================================")
    print("  1. CARGA Y ANÁLISIS PRELIMINAR DEL DATASET NETFLIX")
    print("=========================================================")
    df = pd.read_csv('netflix_titles.csv')
    print(f"Dimensiones iniciales: {df.shape[0]} filas, {df.shape[1]} columnas.\n")
    
    print("--- Resumen de Valores Faltantes ---")
    null_summary = pd.DataFrame({
        'Faltantes': df.isnull().sum(),
        'Porcentaje (%)': (df.isnull().sum() / len(df) * 100).round(2)
    })
    print(null_summary[null_summary['Faltantes'] > 0])
    print("\n")

    print("=========================================================")
    print("  2. DETECCIÓN Y CORRECCIÓN DE ANOMALÍAS (DESPLAZAMIENTO)")
    print("=========================================================")
    shifted_mask = df['rating'].str.contains('min', na=False)
    print(f"Se encontraron {shifted_mask.sum()} filas con duraciones en la columna 'rating':")
    print(df.loc[shifted_mask, ['show_id', 'title', 'rating', 'duration']])
    
    # Corrección de filas desplazadas
    df.loc[shifted_mask, 'duration'] = df.loc[shifted_mask, 'rating']
    df.loc[shifted_mask, 'rating'] = np.nan
    print("\n[OK] Filas desplazadas reubicadas correctamente.\n")

    print("=========================================================")
    print("  3. ESTRUCTURACIÓN Y DESCOMPOSICIÓN DE VARIABLES")
    print("=========================================================")
    # Conversión de date_added
    df['date_added_clean'] = df['date_added'].str.strip()
    df['date_added_dt'] = pd.to_datetime(df['date_added_clean'], format='%B %d, %Y', errors='coerce')
    df['date_added_year'] = df['date_added_dt'].dt.year
    df['date_added_month'] = df['date_added_dt'].dt.month
    
    # Separación de duration en minutos y temporadas
    df['duration_min'] = df['duration'].str.extract(r'(\d+)\s*min').astype(float)
    df['duration_seasons'] = df['duration'].str.extract(r'(\d+)\s*Season').astype(float)
    
    print("Resumen de variable derivada 'duration_min' (Películas):")
    movies_df = df[df['type'] == 'Movie']
    print(movies_df['duration_min'].describe())
    print("\n")

    print("=========================================================")
    print("  4. EJERCICIO 1: IMPUTACIÓN NUMÉRICA CONTINUA DERIVADA")
    print("=========================================================")
    print("Se extrajo la duración en minutos para 6,131 películas.")
    print(f"Valores nulos en duration_min para Películas: {movies_df['duration_min'].isnull().sum()}")
    print("\n")

    print("=========================================================")
    print("  5. EJERCICIO 2: EXPERIMENTO Y COMPARACIÓN DE IMPUTACIÓN")
    print("     (Media vs Mediana vs KNN Imputer)")
    print("=========================================================")
    valid_movies = movies_df.dropna(subset=['duration_min']).copy()
    y_true = valid_movies['duration_min'].values
    
    # Inducir 10% de valores nulos MCAR aleatorios para evaluar desempeño
    np.random.seed(42)
    missing_mask = np.random.rand(len(y_true)) < 0.10
    
    y_corrupted = y_true.copy()
    y_corrupted[missing_mask] = np.nan
    actual_test_values = y_true[missing_mask]

    # Strategy 1: Mean Imputation
    mean_val = np.nanmean(y_corrupted)
    y_imputed_mean = np.where(np.isnan(y_corrupted), mean_val, y_corrupted)
    mae_mean = mean_absolute_error(actual_test_values, y_imputed_mean[missing_mask])
    rmse_mean = np.sqrt(mean_squared_error(actual_test_values, y_imputed_mean[missing_mask]))

    # Strategy 2: Median Imputation
    median_val = np.nanmedian(y_corrupted)
    y_imputed_median = np.where(np.isnan(y_corrupted), median_val, y_corrupted)
    mae_median = mean_absolute_error(actual_test_values, y_imputed_median[missing_mask])
    rmse_median = np.sqrt(mean_squared_error(actual_test_values, y_imputed_median[missing_mask]))

    # Strategy 3: KNN Imputer (usando release_year y date_added_year)
    feature_matrix = valid_movies[['release_year', 'date_added_year', 'duration_min']].copy()
    feature_matrix.loc[missing_mask, 'duration_min'] = np.nan
    # Imputar date_added_year con mediana si hay nulos
    feature_matrix['date_added_year'] = feature_matrix['date_added_year'].fillna(feature_matrix['date_added_year'].median())
    
    knn = KNNImputer(n_neighbors=5)
    knn_result = knn.fit_transform(feature_matrix)
    y_imputed_knn = knn_result[:, 2]
    mae_knn = mean_absolute_error(actual_test_values, y_imputed_knn[missing_mask])
    rmse_knn = np.sqrt(mean_squared_error(actual_test_values, y_imputed_knn[missing_mask]))

    results_df = pd.DataFrame({
        'Estrategia': ['Original (Ground Truth)', 'Imputación Media', 'Imputación Mediana', 'Imputación KNN (K=5)'],
        'Media': [y_true.mean(), y_imputed_mean.mean(), y_imputed_median.mean(), y_imputed_knn.mean()],
        'Mediana': [np.median(y_true), np.median(y_imputed_mean), np.median(y_imputed_median), np.median(y_imputed_knn)],
        'Desv. Estándar': [y_true.std(), y_imputed_mean.std(), y_imputed_median.std(), y_imputed_knn.std()],
        'MAE': [0.0, mae_mean, mae_median, mae_knn],
        'RMSE': [0.0, rmse_mean, rmse_median, rmse_knn]
    })
    print(results_df.to_string(index=False))
    print("\n")

    print("=========================================================")
    print("  6. EJERCICIO 3: IMPUTACIÓN CATEGÓRICA Y VALOR CONSTANTE")
    print("=========================================================")
    df_imputed = df.copy()
    
    # Demostración del efecto bias de imputar la moda vs Constante
    mode_director = df['director'].mode()[0]
    print(f"Moda de director: '{mode_director}' (Frecuencia original: {(df['director']==mode_director).sum()})")
    print(f"Si imputáramos la moda a los 2,634 nulos de director, '{mode_director}' tendría {(df['director']==mode_director).sum() + 2634} registros, distorsionando masivamente el dataset.")
    
    # Imputación adecuada con valor constante "Sin Información"
    df_imputed['director'] = df_imputed['director'].fillna('Sin Información')
    df_imputed['cast'] = df_imputed['cast'].fillna('Sin Información')
    df_imputed['country'] = df_imputed['country'].fillna('Sin Información')
    df_imputed['rating'] = df_imputed['rating'].fillna(df_imputed['rating'].mode()[0]) # rating tiene solo 7 nulos desalineados/puros, la moda TV-MA es factible tras arreglar el desplazamietno
    df_imputed['date_added_clean'] = df_imputed['date_added_clean'].fillna('Sin Fecha')
    
    print("\nEstado de nulos tras imputación final:")
    print(df_imputed[['director', 'cast', 'country', 'rating', 'duration_min', 'duration_seasons']].isnull().sum())

    # Exportar dataset limpio
    df_imputed.to_csv('netflix_titles_cleaned.csv', index=False)
    print("\n[ÉXITO] Dataset procesado e imputado guardado en 'netflix_titles_cleaned.csv'.")

if __name__ == '__main__':
    main()
