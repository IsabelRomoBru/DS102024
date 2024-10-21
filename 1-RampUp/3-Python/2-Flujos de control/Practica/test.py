def test1(mi_funcion):
    caso_1 = '123-456-789-101-213-3'
    caso_2 = '456-213454325-324-970-0-231-5654-1287-5'
    caso_3 = '2-1-4-5-3-6-7-23-6-7-2-32-7-54-2-31-23-6-8-995-423-312-123156-643-12136-12-85-342-134-1'
    caso_4 = '2'
    assert mi_funcion(caso_1) == (3,1581), f"error con la tira {caso_1}"
    assert mi_funcion(caso_2) == (5,213455295), f"error con la tira {caso_2}"
    assert mi_funcion(caso_3) == (1,138467), f"error con la tira {caso_3}"
    assert mi_funcion(caso_4) == (2,0), f"error con la tira {caso_4}"
    print('Salio todo piola')

def test2(mi_funcion):
    caso_1 = './test/borges1.txt'
    caso_1_clave = 6
    with open('./test/borges1_encriptado_6.txt', 'r') as f:
        contenido = f.read()     
        assert mi_funcion(caso_1, caso_1_clave) == contenido, f"error con la tira {caso_1}"
    caso_2 = './test/borges2.txt'
    caso_2_clave = 11
    with open('./test/borges2_encriptado_11.txt', 'r') as f:
        contenido = f.read()     
        assert mi_funcion(caso_2, caso_2_clave) == contenido, f"error con la tira {caso_2}"
    print('¡Mensaje encriptado correctamente! Son hackers.')

def test2_mayusculas(mi_funcion):
    caso_1 = './test/borges1.txt'
    caso_1_clave = 6
    with open('./test/borges1_encriptado_6_cap.txt', 'r') as f:
        contenido = f.read()     
        assert mi_funcion(caso_1, caso_1_clave) == contenido, f"error con la tira {caso_1}"
    caso_2 = 'borges2.txt'
    caso_2_clave = 11
    with open('./test/borges2_encriptado_11_cap.txt', 'r') as f:
        contenido = f.read()     
        assert mi_funcion(caso_2, caso_2_clave) == contenido, f"error con la tira {caso_2}"
    print('¡Mensaje encriptado correctamente! Son hackers.')

def test3(mi_funcion):
    caso_1 = ['Gatito','Ornitorrinco','Vaca','Elefante','Pato']
    rotacion1_1 = 11
    rotacion1_2 = 3
    caso_2 = ['Minotauro','Grifo']
    rotacion2_1 = 0
    rotacion2_2 = 20
    assert mi_funcion(caso_1, rotacion1_1) == ['Pato', 'Gatito', 'Ornitorrinco', 'Vaca', 'Elefante'], f"error con rotar {rotacion1_1} veces la calesita: {caso_1}"
    assert mi_funcion(caso_1, rotacion1_2) == ['Vaca', 'Elefante', 'Pato', 'Gatito', 'Ornitorrinco'], f"error con rotar {rotacion1_2} veces la calesita: {caso_1}"
    assert mi_funcion(caso_2, rotacion2_1) == ['Minotauro','Grifo'], f"error con rotar {rotacion2_1} veces la calesita: {caso_2}"
    assert mi_funcion(caso_2, rotacion2_2) == ['Minotauro','Grifo'], f"error con rotar {rotacion2_2} veces la calesita: {caso_2}"
    print('¡La calesita anda!')

def test4(mi_funcion):
    caso_1 = ['Gatito','Ornitorrinco','Vaca','Elefante','Pato']
    rotacion1_1 = 11
    rotacion1_2 = 3
    rotacion1_3 = 0
    assert mi_funcion(caso_1, rotacion1_1, 'Gatito') == ['Vaca', 'Elefante', 'Pato', 'Ornitorrinco'], f"error con rotar {rotacion1_1} veces la calesita: {caso_1}"
    assert mi_funcion(caso_1, rotacion1_2, 'Pato') == ['Ornitorrinco', 'Vaca', 'Elefante', 'Gatito'], f"error con rotar {rotacion1_2} veces la calesita: {caso_1}"
    assert mi_funcion(caso_1, rotacion1_3, 'Vaca') == ['Gatito','Ornitorrinco','Elefante','Pato'], f"error con rotar {rotacion1_3} veces la calesita: {caso_1}"
    print('¡Perfecto! Ahora a ganar dinero para Jacinto')