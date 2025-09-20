""" Clase que maneja el estado del juego y las reglas """
from nodo import Nodo

class EstadoJuego:
    # nivel: matriz 2D representando el nivel (0=vacío, 1=pared, 2=luz)
    def __init__(self, nivel, robot_x, robot_y):
        self.nivel = nivel
        self.filas = len(nivel)
        self.columnas = len(nivel[0])
        self.robot_x = robot_x
        self.robot_y = robot_y
        
        # Encontrar posiciones de las luces
        self.posiciones_luces = []
        for i in range(self.filas):
            for j in range(self.columnas):
                if nivel[i][j] == 2:
                    self.posiciones_luces.append((i, j))
        
        # Estado inicial: todas las luces apagadas
        self.luces_iniciales = tuple([0] * len(self.posiciones_luces))

    # Verifica si una posición está dentro de los límites del nivel
    def es_posicion_valida(self, x, y):
        return 0 <= x < self.filas and 0 <= y < self.columnas

    # Verifica si el robot puede moverse a una posición (no es pared)
    def puede_moverse_a(self, x, y):
        return self.es_posicion_valida(x, y) and self.nivel[x][y] != 1

    # Verifica si el robot puede encender una luz en su posición actual
    def puede_encender_luz(self, x, y, luces):
        indice_luz = None
        for i, (lx, ly) in enumerate(self.posiciones_luces):
            if lx == x and ly == y:
                indice_luz = i
                break
        return indice_luz is not None and luces[indice_luz] == 0

    # Genera los sucesores de un nodo dado
    def obtener_sucesores(self, nodo):
        sucesores = []
        direcciones = [
            (-1, 0, 'ARRIBA'),
            (1, 0, 'ABAJO'),
            (0, -1, 'IZQUIERDA'),
            (0, 1, 'DERECHA')
        ]

        # Intentar movimientos en las 4 direcciones
        for dx, dy, accion in direcciones:
            nuevo_x = nodo.x + dx
            nuevo_y = nodo.y + dy

            if self.puede_moverse_a(nuevo_x, nuevo_y):
                sucesor = Nodo(
                    nuevo_x, 
                    nuevo_y, 
                    list(nodo.luces), 
                    nodo, 
                    accion, 
                    nodo.costo + 1
                )
                sucesores.append(sucesor)

        # Intentar encender luz en la posición actual
        if self.puede_encender_luz(nodo.x, nodo.y, nodo.luces):
            indice_luz = None
            for i, (lx, ly) in enumerate(self.posiciones_luces):
                if lx == nodo.x and ly == nodo.y:
                    indice_luz = i
                    break
            
            nuevas_luces = list(nodo.luces)
            nuevas_luces[indice_luz] = 1

            sucesor = Nodo(
                nodo.x, 
                nodo.y, 
                nuevas_luces, 
                nodo, 
                'ENCENDER', 
                nodo.costo + 1
            )
            sucesores.append(sucesor)

        return sucesores

    # Verifica si un nodo es el estado objetivo (todas las luces encendidas)
    def es_meta(self, nodo):
        return all(luz == 1 for luz in nodo.luces)

    # Heurística: número de luces apagadas + distancia a la luz apagada más cercana
    def heuristica(self, nodo):
        luces_apagadas = sum(1 for luz in nodo.luces if luz == 0)
        
        if luces_apagadas == 0:
            return 0

        distancia_minima = float('inf')
        
        for i, (lx, ly) in enumerate(self.posiciones_luces):
            if nodo.luces[i] == 0:
                distancia = abs(nodo.x - lx) + abs(nodo.y - ly)
                distancia_minima = min(distancia_minima, distancia)

        return luces_apagadas + distancia_minima

    # Retorna el nodo inicial del juego
    def obtener_nodo_inicial(self):
        return Nodo(self.robot_x, self.robot_y, list(self.luces_iniciales))