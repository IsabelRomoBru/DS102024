import pytest
import pandas as pd
import numpy as np

def calcular_rentabilidad(df):
    """Calcula la rentabilidad de cada producto en el dataset de ventas."""
    df_resultado = df.copy()
    df_resultado['rentabilidad'] = (1 - df_resultado['descuento']) * 100
    return df_resultado

@pytest.fixture
def df_test():
    """Fixture que crea un DataFrame de prueba."""
    data = {
        'id': [1, 2, 3],
        'producto': ['Producto A', 'Producto B', 'Producto C'],
        'precio': [100.0, 200.0, 300.0],
        'cantidad': [2, 1, 3],
        'descuento': [0.1, 0.0, 0.25],
        'total': [180.0, 200.0, 675.0]
    }
    return pd.DataFrame(data)

def test_columna_rentabilidad_existe(df_test):
    resultado = calcular_rentabilidad(df_test)
    assert 'rentabilidad' in resultado.columns, "La columna 'rentabilidad' no fue añadida"

def test_valores_rentabilidad_correctos(df_test):
    resultado = calcular_rentabilidad(df_test)
    valores_esperados = [90.0, 100.0, 75.0]  # (1 - descuento) * 100
    np.testing.assert_allclose(resultado['rentabilidad'], valores_esperados, rtol=1e-2)

def test_caso_descuento_cero(df_test):
    resultado = calcular_rentabilidad(df_test)
    rentabilidad_producto_b = resultado.loc[resultado['producto'] == 'Producto B', 'rentabilidad'].values[0]
    assert rentabilidad_producto_b == 100.0, "Rentabilidad debería ser 100% cuando el descuento es 0"
