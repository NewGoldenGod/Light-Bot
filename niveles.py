"""
Definición de los niveles del juego
0: Piso normal
1: Obstáculo
2: Luz (objetivo)
"""

LEVELS = {
    1: {
        'grid': [
            [0, 0, 2],
            [0, 1, 0],
            [0, 0, 2]
        ],
        'robot_start': (0, 0),
        'name': "Nivel Básico",
        'description': "Dos luces simples"
    },
    
    2: {
        'grid': [
            [2, 0, 0, 1],
            [0, 1, 0, 0],
            [0, 0, 1, 2],
            [2, 0, 0, 0]
        ],
        'robot_start': (1, 0),
        'name': "Nivel Intermedio", 
        'description': "Tres luces con obstáculos"
    },
    
    3: {
        'grid': [
            [0, 1, 2, 0, 0],
            [0, 0, 0, 1, 2],
            [1, 0, 1, 0, 0],
            [2, 0, 0, 0, 1],
            [0, 0, 2, 0, 0]
        ],
        'robot_start': (0, 0),
        'name': "Nivel Avanzado",
        'description': "Cuatro luces en laberinto complejo"
    }
}

def get_level(level_number):
    """Obtiene la configuración de un nivel específico"""
    return LEVELS.get(level_number, LEVELS[1])