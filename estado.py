""" Clase que maneja el estado del juego y las reglas """
from nodo import Nodo

class EstadoJuego:
    # level: matriz 2D representando el nivel (0=vacío, 1=pared, 2=luz)
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

    # Verifica si una posición está dentro de los límites del nivel
    def is_valid_position(self, x, y):
        return 0 <= x < self.rows and 0 <= y < self.cols

    # Verifica si el robot puede moverse a una posición (no es pared)
    def can_move_to(self, x, y):
        return self.is_valid_position(x, y) and self.level[x][y] != 1

    # Verifica si el robot puede encender una luz en su posición actual
    def can_turn_on_light(self, x, y, lights):
        light_index = None
        for i, (lx, ly) in enumerate(self.light_positions):
            if lx == x and ly == y:
                light_index = i
                break
        return light_index is not None and lights[light_index] == 0

    # Genera los sucesores de un nodo dado
    def get_successors(self, node):
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

    # Verifica si un nodo es el estado objetivo (todas las luces encendidas)
    def is_goal(self, node):
        return all(light == 1 for light in node.lights)

    # Heurística: número de luces apagadas + distancia a la luz apagada más cercana
    def heuristic(self, node):
        lights_off = sum(1 for light in node.lights if light == 0)
        
        if lights_off == 0:
            return 0

        min_distance = float('inf')
        
        for i, (lx, ly) in enumerate(self.light_positions):
            if node.lights[i] == 0:
                distance = abs(node.x - lx) + abs(node.y - ly)
                min_distance = min(min_distance, distance)

        return lights_off + min_distance

    # Retorna el nodo inicial del juego
    def get_initial_node(self):
        return Nodo(self.robot_x, self.robot_y, list(self.initial_lights))