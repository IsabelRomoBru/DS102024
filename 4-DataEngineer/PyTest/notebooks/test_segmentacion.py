import pytest
import pandas as pd
import numpy as np

def segmentar_productos(df):
    """Segmenta los productos según su precio y popularidad (cantidad vendida)."""
    # Agrupa por producto y calcula el precio promedio y la cantidad total
    df_agrupado = df.groupby('producto').agg({
        'precio': 'mean',
        'cantidad': 'sum'
    }).reset_index()
    
    # Segmentación por precio
    condiciones_precio = [
        (df_agrupado['precio'] < 50),
        (df_agrupado['precio'] >= 50) & (df_agrupado['precio'] < 100),
        (df_agrupado['precio'] >= 100) & (df_agrupado['precio'] < 200),
        (df_agrupado['precio'] >= 200)
    ]
    categorias_precio = ['Económico', 'Estándar', 'Premium', 'Lujo']
    df_agrupado['segmento_precio'] = np.select(condiciones_precio, categorias_precio, default='Sin categoría')
    
    # Segmentación por popularidad
    condiciones_popularidad = [
        (df_agrupado['cantidad'] < 2),
        (df_agrupado['cantidad'] >= 2) & (df_agrupado['cantidad'] < 4),
        (df_agrupado['cantidad'] >= 4)
    ]
    categorias_popularidad = ['Baja', 'Media', 'Alta']
    df_agrupado['segmento_popularidad'] = np.select(condiciones_popularidad, categorias_popularidad, default='Sin categoría')
    
    return df_agrupado

@pytest.fixture
def df_test():
    """Fixture que crea un DataFrame de prueba con diferentes productos."""
    data = {
        'producto': ['Producto A', 'Producto A', 'Producto B', 'Producto C', 'Producto D', 'Producto E'],
        'precio': [30.0, 30.0, 75.0, 150.0, 250.0, 50.0],
        'cantidad': [1, 2, 2, 3, 1, 5]
    }
    return pd.DataFrame(data)

# Escribe tus tests aquí
def test_segmentacion_por_precio(df_test):
    resultado = segmentar_productos(df_test)
    segmentos = dict(zip(resultado['producto'], resultado['segmento_precio']))
    
    assert segmentos['Producto A'] == 'Económico'    # Precio: 30
    assert segmentos['Producto B'] == 'Estándar'     # Precio: 75
    assert segmentos['Producto C'] == 'Premium'      # Precio: 150
    assert segmentos['Producto D'] == 'Lujo'         # Precio: 250
    assert segmentos['Producto E'] == 'Estándar'     # Precio: 50

def test_segmentacion_por_popularidad(df_test):
    resultado = segmentar_productos(df_test)
    popularidades = dict(zip(resultado['producto'], resultado['segmento_popularidad']))
    
    assert popularidades['Producto A'] == 'Media'    # Cantidad: 1 + 2 = 3
    assert popularidades['Producto B'] == 'Media'    # Cantidad: 2
    assert popularidades['Producto C'] == 'Media'    # Cantidad: 3
    assert popularidades['Producto D'] == 'Baja'     # Cantidad: 1
    assert popularidades['Producto E'] == 'Alta'     # Cantidad: 5

def test_productos_multiples_ventas(df_test):
    resultado = segmentar_productos(df_test)
    producto_a = resultado[resultado['producto'] == 'Producto A']
    
    assert producto_a['precio'].values[0] == 30.0              # Promedio entre 30 y 30
    assert producto_a['cantidad'].values[0] == 3               # 1 + 2
    assert producto_a['segmento_precio'].values[0] == 'Económico'
    assert producto_a['segmento_popularidad'].values[0] == 'Media'
