"""
Clase que representa un nodo en el espacio de estados del juego LightBot
"""

class Nodo:
    def __init__(self, x, y, lights, parent=None, action=None, cost=0):
        self.x = x                    # Posicion X del robot
        self.y = y                    # Posicion Y del robot
        self.lights = tuple(lights)   # Tupla con estado de las luces (0=apagada, 1=encendida)
        self.parent = parent          # Nodo padre para reconstruir el camino
        self.action = action          # Accion que llevo a este estado
        self.cost = cost              # Costo acumulado (g en A*)
        self.heuristic = 0            # Valor heuristico (h en A*)
        self.total_cost = 0           # Costo total (f = g + h en A*)
        self.visited_order = -1       # Orden en que fue visitado

    def get_key(self):
        """Genera una clave unica para este estado"""
        return f"{self.x},{self.y},{','.join(map(str, self.lights))}"

    def equals(self, other):
        """Verifica si dos nodos representan el mismo estado"""
        return (self.x == other.x and 
                self.y == other.y and 
                self.lights == other.lights)

    def copy(self, new_x=None, new_y=None, new_lights=None):
        """Crea una copia del nodo con nuevos valores"""
        if new_x is None:
            new_x = self.x
        if new_y is None:
            new_y = self.y
        if new_lights is None:
            new_lights = list(self.lights)
        
        return Nodo(new_x, new_y, new_lights, self.parent, self.action, self.cost)

    def get_path(self):
        """Reconstruye el camino desde el nodo inicial hasta este nodo"""
        path = []
        current = self
        
        while current.parent is not None:
            path.insert(0, current.action)
            current = current.parent
        
        return path

    def __str__(self):
        return f"Nodo(x={self.x}, y={self.y}, lights={self.lights}, cost={self.cost})"