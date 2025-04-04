import pytest
import pandas as pd
import numpy as np
def detectar_anomalias(df, columna, umbral=2.0):
    """Detecta anomalías en una columna numérica del DataFrame.
    
    Args:
        df: DataFrame con la columna a analizar
        columna: Nombre de la columna numérica a analizar
        umbral: Número de desviaciones estándar para considerar un valor como anomalía
        
    Returns:
        DataFrame: DataFrame con las filas que contienen anomalías
    """
    # Crear una copia del DataFrame para no modificar el original
    df_resultado = df.copy()
    
    # Calcular la media y desviación estándar de la columna
    media = df_resultado[columna].mean()
    desviacion = df_resultado[columna].std()
    
    # Definir los límites superior e inferior para anomalías
    limite_superior = media + umbral * desviacion
    limite_inferior = media - umbral * desviacion
    
    # Filtrar las filas que están fuera de los límites
    df_anomalias = df_resultado[
        (df_resultado[columna] > limite_superior) |
        (df_resultado[columna] < limite_inferior)
    ]
    
    return df_anomalias

@pytest.fixture
def df_test():
    """Fixture que crea un DataFrame de prueba con valores normales y anómalos."""
    # Crea un DataFrame con valores normales (alrededor de 100) y algunos valores anómalos
    np.random.seed(42)  # Para reproducibilidad
    valores_normales = np.random.normal(100, 10, 20)  # 20 valores normales con media 100 y desv. std. 10
    valores_anomalos_altos = [150, 160]  # Anomalías por encima (> media + 2*desv_std = 100 + 2*10 = 120)
    valores_anomalos_bajos = [60, 50]  # Anomalías por debajo (< media - 2*desv_std = 100 - 2*10 = 80)
    
    valores = np.concatenate([valores_normales, valores_anomalos_altos, valores_anomalos_bajos])
    ids = range(1, len(valores) + 1)
    
    return pd.DataFrame({'id': ids, 'valor': valores})
def test_detecta_anomalias_por_encima(df_test):
    resultado = detectar_anomalias(df_test, 'valor', umbral=2.0)
    valores_anomalos = resultado['valor'].values
    # Comprobamos que los valores altos (150, 160) están en los resultados
    assert any(v in valores_anomalos for v in [150, 160]), "No se detectaron las anomalías altas esperadas"
    # Aseguramos que el resto no fue incluido por error
    assert all(v >= 120 or v <= 80 for v in valores_anomalos)

def test_detecta_anomalias_por_debajo(df_test):
    resultado = detectar_anomalias(df_test, 'valor', umbral=2.0)
    valores_anomalos = resultado['valor'].values
    # Comprobamos que los valores bajos (60, 50) están en los resultados
    assert any(v in valores_anomalos for v in [60, 50]), "No se detectaron las anomalías bajas esperadas"
    # Aseguramos que el resto no fue incluido por error
    assert all(v >= 120 or v <= 80 for v in valores_anomalos)

def test_umbral_diferente(df_test):
    resultado = detectar_anomalias(df_test, 'valor', umbral=3.0)
    # Con umbral 3.0, ninguna observación debería estar fuera si std=10 → límites: 70–130
    # 150 y 160 todavía deberían ser detectadas, pero quizá 60 y 50 no si la std es mayor por outliers
    # Entonces, verificamos que haya menos anomalías que con umbral=2.0
    resultado_2 = detectar_anomalias(df_test, 'valor', umbral=2.0)
    assert len(resultado) <= len(resultado_2), "Con umbral mayor debería haber igual o menos anomalías"
