# Definiciones de niveles para LightBot
NIVELES = {
    1: {
        'cuadricula': [
            [0, 0, 2],
            [0, 1, 0],
            [0, 0, 2]
        ],
        'inicio_robot': (0, 0),
        'nombre': "Nivel Básico",
        'descripcion': "Dos luces simples"
    },
    
    2: {
        'cuadricula': [
            [2, 0, 0, 1],
            [0, 1, 0, 0],
            [0, 0, 1, 2],
            [2, 0, 0, 0]
        ],
        'inicio_robot': (1, 0),
        'nombre': "Nivel Intermedio", 
        'descripcion': "Tres luces con obstáculos"
    },
    
    3: {
        'cuadricula': [
            [0, 1, 2, 0, 0],
            [0, 0, 0, 1, 2],
            [1, 0, 1, 0, 0],
            [2, 0, 0, 0, 1],
            [0, 0, 2, 0, 0]
        ],
        'inicio_robot': (0, 0),
        'nombre': "Nivel Avanzado",
        'descripcion': "Cuatro luces en laberinto complejo"
    }
}

# Retorna el nivel correspondiente al numero dado
def obtener_nivel(numero_nivel):
    return NIVELES.get(numero_nivel, NIVELES[1])