import pytest
import pandas as pd
import numpy as np

class PipelinePreprocesamiento:
    """Pipeline de preprocesamiento para el dataset de ventas."""

    def __init__(self):
        pass

    def convertir_tipos(self, df):
        df_convertido = df.copy()
        df_convertido['fecha'] = pd.to_datetime(df_convertido['fecha'], errors='coerce')
        df_convertido['precio'] = pd.to_numeric(df_convertido['precio'], errors='coerce')
        df_convertido['cantidad'] = pd.to_numeric(df_convertido['cantidad'], errors='coerce').astype('Int64')
        df_convertido['descuento'] = pd.to_numeric(df_convertido['descuento'], errors='coerce')
        df_convertido['total'] = pd.to_numeric(df_convertido['total'], errors='coerce')
        return df_convertido

    def normalizar_categorias(self, df):
        df_normalizado = df.copy()
        if 'categoria' in df_normalizado.columns:
            df_normalizado['categoria'] = df_normalizado['categoria'].str.capitalize()
        return df_normalizado

    def eliminar_duplicados(self, df):
        # Primero convertir tipos y normalizar texto para asegurar duplicados detectables
        df_limpio = self.convertir_tipos(df)
        df_limpio = self.normalizar_categorias(df_limpio)
        df_sin_duplicados = df_limpio.drop_duplicates()
        return df_sin_duplicados

    def procesar(self, df):
        # Aplica todo el flujo correcto
        df_procesado = self.convertir_tipos(df)
        df_procesado = self.normalizar_categorias(df_procesado)
        df_procesado = self.eliminar_duplicados(df_procesado)
        return df_procesado

  


@pytest.fixture
def df_test():
    """Fixture que crea un DataFrame de prueba con problemas para preprocesar."""
    data = {
        'id': [1, 2, 3, 3],  # ID duplicado
        'fecha': ['2023-01-05', '2023-01-10', '2023-01-15', '2023-01-15'],
        'producto': ['Laptop HP', 'Monitor Dell', 'Teclado Logitech', 'Teclado Logitech'],
        'categoria': ['ELECTRÓNICA', 'electrónica', 'Accesorios', 'accesorios'],  # Inconsistencia en mayúsculas/minúsculas
        'precio': ['899.99', '249.99', '59.99', '59.99'],  # Strings en lugar de float
        'cantidad': ['1', '2', '3', '3'],  # Strings en lugar de int
        'descuento': [0.05, 0.00, 0.10, 0.10],
        'total': [854.99, 499.98, 161.97, 161.97]
    }
    return pd.DataFrame(data)

def test_convertir_tipos(df_test):
    pipeline = PipelinePreprocesamiento()
    df_convertido = pipeline.convertir_tipos(df_test)

    assert pd.api.types.is_datetime64_any_dtype(df_convertido['fecha']), "La columna 'fecha' no es datetime"
    assert pd.api.types.is_float_dtype(df_convertido['precio']), "La columna 'precio' no es float"
    assert pd.api.types.is_integer_dtype(df_convertido['cantidad']), "La columna 'cantidad' no es int"
    assert pd.api.types.is_float_dtype(df_convertido['descuento']), "La columna 'descuento' no es float"
    assert pd.api.types.is_float_dtype(df_convertido['total']), "La columna 'total' no es float"

def test_eliminar_duplicados(df_test):
    pipeline = PipelinePreprocesamiento()
    df_sin_duplicados = pipeline.eliminar_duplicados(df_test)
    assert len(df_sin_duplicados) < len(df_test), "No se eliminaron duplicados correctamente"
    assert df_sin_duplicados.duplicated().sum() == 0, "Aún quedan filas duplicadas"


def test_normalizar_categorias(df_test):
    pipeline = PipelinePreprocesamiento()
    df_normalizado = pipeline.normalizar_categorias(df_test)

    categorias = df_normalizado['categoria'].unique()
    for cat in categorias:
        assert cat == cat.capitalize(), f"La categoría '{cat}' no está correctamente capitalizada"

def test_procesar(df_test):
    pipeline = PipelinePreprocesamiento()
    df_procesado = pipeline.procesar(df_test)

    # Chequea tipos
    assert pd.api.types.is_datetime64_any_dtype(df_procesado['fecha'])
    assert pd.api.types.is_float_dtype(df_procesado['precio'])
    assert pd.api.types.is_integer_dtype(df_procesado['cantidad'])

    # Chequea duplicados
    assert df_procesado.duplicated().sum() == 0

    # Chequea categorías
    assert all(cat == cat.capitalize() for cat in df_procesado['categoria'].unique())
