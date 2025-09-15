"""
Clase que maneja el estado del juego y las reglas
"""
from nodo import Nodo

class EstadoJuego:
    def __init__(self, level, robot_x, robot_y):
        self.level = level
        self.rows = len(level)
        self.cols = len(level[0])
        self.robot_x = robot_x
        self.robot_y = robot_y
        
        # Encontrar posiciones de las luces
        self.light_positions = []
        for i in range(self.rows):
            for j in range(self.cols):
                if level[i][j] == 2:
                    self.light_positions.append((i, j))
        
        # Estado inicial: todas las luces apagadas
        self.initial_lights = tuple([0] * len(self.light_positions))

    def is_valid_position(self, x, y):
        """Verifica si una posición está dentro del tablero"""
        return 0 <= x < self.rows and 0 <= y < self.cols

    def can_move_to(self, x, y):
        """Verifica si el robot puede moverse a una posición"""
        return self.is_valid_position(x, y) and self.level[x][y] != 1

    def can_turn_on_light(self, x, y, lights):
        """Verifica si el robot puede encender una luz en su posición actual"""
        # Buscar si hay una luz en esta posición
        light_index = None
        for i, (lx, ly) in enumerate(self.light_positions):
            if lx == x and ly == y:
                light_index = i
                break
        
        # Puede encender si hay una luz y está apagada
        return light_index is not None and lights[light_index] == 0

    def get_successors(self, node):
        """Genera todos los sucesores posibles de un nodo"""
        successors = []
        directions = [
            (-1, 0, 'ARRIBA'),
            (1, 0, 'ABAJO'),
            (0, -1, 'IZQUIERDA'),
            (0, 1, 'DERECHA')
        ]

        # Intentar movimientos en las 4 direcciones
        for dx, dy, action in directions:
            new_x = node.x + dx
            new_y = node.y + dy

            if self.can_move_to(new_x, new_y):
                successor = Nodo(
                    new_x, 
                    new_y, 
                    list(node.lights), 
                    node, 
                    action, 
                    node.cost + 1
                )
                successors.append(successor)

        # Intentar encender luz en la posición actual
        if self.can_turn_on_light(node.x, node.y, node.lights):
            light_index = None
            for i, (lx, ly) in enumerate(self.light_positions):
                if lx == node.x and ly == node.y:
                    light_index = i
                    break
            
            new_lights = list(node.lights)
            new_lights[light_index] = 1

            successor = Nodo(
                node.x, 
                node.y, 
                new_lights, 
                node, 
                'ENCENDER', 
                node.cost + 1
            )
            successors.append(successor)

        return successors

    def is_goal(self, node):
        """Verifica si un nodo representa el estado meta (todas las luces encendidas)"""
        return all(light == 1 for light in node.lights)

    def heuristic(self, node):
        """
        Calcula la heurística para A*
        Heurística = número de luces apagadas + distancia a la luz más cercana
        """
        lights_off = sum(1 for light in node.lights if light == 0)
        
        if lights_off == 0:
            return 0

        # Encontrar distancia a la luz apagada más cercana
        min_distance = float('inf')
        
        for i, (lx, ly) in enumerate(self.light_positions):
            if node.lights[i] == 0:
                distance = abs(node.x - lx) + abs(node.y - ly)
                min_distance = min(min_distance, distance)

        return lights_off + min_distance

    def get_initial_node(self):
        """Crea el nodo inicial"""
        return Nodo(self.robot_x, self.robot_y, list(self.initial_lights))