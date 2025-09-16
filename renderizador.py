"""
Clase para mostrar el estado del juego en consola
"""

from estado import EstadoJuego

class Renderizador:
    def __init__(self):
        self.simbolos = {
            0: '.',  # Piso normal
            1: '#',  # Obstaculo
            2: 'L',  # Luz apagada
            'light_on': 'O',  # Luz encendida
            'robot': 'R',     # Robot
            'robot_on_light': '@'  # Robot en luz encendida
        }

    def render_level(self, nivel, robot_x, robot_y, light_states=None):
        """Renderiza un nivel en la consola"""
        grid = nivel['grid']
        filas = len(grid)
        columnas = len(grid[0])
        
        # Si no se proporcionan estados de luces, todas estan apagadas
        if light_states is None:
            light_count = self._contar_luces(grid)
            light_states = [0] * light_count
        
        print(f"\n=== {nivel['name']} ===")
        print(f"Descripcion: {nivel['description']}")
        print()
        
        # Crear representacion visual
        display_grid = []
        for i in range(filas):
            fila = []
            for j in range(columnas):
                celda = self._get_cell_symbol(grid[i][j], i, j, robot_x, robot_y, light_states, grid)
                fila.append(celda)
            display_grid.append(fila)
        
        # Mostrar el tablero
        for fila in display_grid:
            print(' '.join(f'{celda:^3}' for celda in fila))
        
        print()
        self._mostrar_leyenda()

    def _get_cell_symbol(self, cell_type, row, col, robot_x, robot_y, light_states, grid):
        """Determina el simbolo a mostrar en una celda"""
        # Si el robot esta aqui
        if row == robot_x and col == robot_y:
            if cell_type == 2:  # Robot en una luz
                light_index = self._get_light_index(row, col, grid)
                if light_index is not None and light_states[light_index] == 1:
                    return self.simbolos['robot_on_light']
                else:
                    return self.simbolos['robot']
            else:
                return self.simbolos['robot']
        else:
            # Celda sin robot
            if cell_type == 0:
                return self.simbolos[0]
            elif cell_type == 1:
                return self.simbolos[1]
            elif cell_type == 2:
                light_index = self._get_light_index(row, col, grid)
                if light_index is not None and light_states[light_index] == 1:
                    return self.simbolos['light_on']
                else:
                    return self.simbolos[2]

    def _get_light_index(self, row, col, grid):
        """Obtiene el indice de una luz en las posiciones de luces"""
        light_positions = self._get_light_positions(grid)
        for i, (lx, ly) in enumerate(light_positions):
            if lx == row and ly == col:
                return i
        return None

    def _get_light_positions(self, grid):
        """Obtiene todas las posiciones de luces en el nivel"""
        positions = []
        for i in range(len(grid)):
            for j in range(len(grid[0])):
                if grid[i][j] == 2:
                    positions.append((i, j))
        return positions

    def _contar_luces(self, grid):
        """Cuenta el numero total de luces en el nivel"""
        count = 0
        for i in range(len(grid)):
            for j in range(len(grid[0])):
                if grid[i][j] == 2:
                    count += 1
        return count

    def _mostrar_leyenda(self):
        """Muestra la leyenda de simbolos"""
        print("Leyenda:")
        print(f"  {self.simbolos[0]} = Piso normal")
        print(f"  {self.simbolos[1]} = Obstaculo")
        print(f"  {self.simbolos[2]} = Luz apagada")
        print(f"  {self.simbolos['light_on']} = Luz encendida")
        print(f"  {self.simbolos['robot']} = Robot")
        print(f"  {self.simbolos['robot_on_light']} = Robot en luz encendida")
        print()
        print("Comandos de movimiento:")
        print("  1 = ARRIBA, 2 = ABAJO, 3 = IZQUIERDA, 4 = DERECHA, 5 = ENCENDER")
        print()



    def mostrar_solucion(self, camino, nombre_algoritmo=""):
        """Muestra la solucion encontrada"""
        if not camino:
            print("El robot ya esta en la meta!")
            return
        
        if nombre_algoritmo:
            print(f"Solucion encontrada por {nombre_algoritmo}:")
        else:
            print("Solucion encontrada:")
        
        # Mostrar paso a paso (sin la secuencia con flechas)
        for i, paso in enumerate(camino, 1):
            print(f"  {i}. {paso}")
        print()

    def mostrar_explicacion_heuristica(self, nodo, light_positions):
        """Muestra el calculo detallado de la heuristica"""
        luces_apagadas = sum(1 for luz in nodo.lights if luz == 0)
        
        print(f"\nCALCULO DE HEURISTICA para posicion ({nodo.x}, {nodo.y}):")
        print(f"   Estado de luces: {nodo.lights}")
        print(f"   Luces apagadas: {luces_apagadas}")
        
        if luces_apagadas == 0:
            print(f"   Distancia minima: 0 (todas las luces encendidas)")
            print(f"   h(n) = {luces_apagadas} + 0 = 0")
            return 0
        
        distancia_minima = float('inf')
        luz_mas_cercana = None
        
        for i, (lx, ly) in enumerate(light_positions):
            if nodo.lights[i] == 0:
                distancia = abs(nodo.x - lx) + abs(nodo.y - ly)
                if distancia < distancia_minima:
                    distancia_minima = distancia
                    luz_mas_cercana = (lx, ly)
        
        print(f"   Luz mas cercana: {luz_mas_cercana}")
        print(f"   Distancia minima: {distancia_minima}")
        print(f"   h(n) = {luces_apagadas} + {distancia_minima} = {luces_apagadas + distancia_minima}")
        print(f"   g(n) = {nodo.cost}, f(n) = g(n) + h(n) = {nodo.cost + luces_apagadas + distancia_minima}")
        
        return luces_apagadas + distancia_minima

    def _obtener_descripcion_movimientos(self, visited_nodes):
        """Genera una descripción de los movimientos realizados"""
        if not visited_nodes:
            return "No hay movimientos para analizar"
        
        # Solo mostrar el coste total
        coste_total = visited_nodes[-1].cost if visited_nodes else 0
        return f"Coste total: {coste_total}"

    def mostrar_estadisticas(self, resultado_astar, resultado_bfs):
        """Muestra las estadisticas de comparacion"""
        print("\n" + "="*60)
        print("COMPARACION DE ALGORITMOS")
        print("="*60)
        print()
        
        print("A* (Heuristica - Algoritmo Informado):")
        print(f"  Nodos explorados: {resultado_astar['nodes_explored']}")
        print(f"  Pasos solucion: {resultado_astar['steps']}")
        print(f"  Tiempo: {resultado_astar['execution_time']:.2f}ms")
        print()
        
        # Mostrar descripción de movimientos para A*
        if resultado_astar['visited_nodes']:
            descripcion = self._obtener_descripcion_movimientos(resultado_astar['visited_nodes'])
            print(f"  {descripcion}")
            print()

        
        self.mostrar_solucion(resultado_astar['path'], "A*")
        
        print("BFS (Busqueda Ciega - Sin informacion):")
        print(f"  Nodos explorados: {resultado_bfs['nodes_explored']}")
        print(f"  Pasos solucion: {resultado_bfs['steps']}")
        print(f"  Tiempo: {resultado_bfs['execution_time']:.2f}ms")
        
        # Mostrar descripción de movimientos para BFS
        if resultado_bfs['visited_nodes']:
            descripcion = self._obtener_descripcion_movimientos(resultado_bfs['visited_nodes'])
            print(f"  {descripcion}")
            print()
        
        self.mostrar_solucion(resultado_bfs['path'], "BFS")
        print()
    
        if resultado_astar['success'] and resultado_bfs['success']:
            print("=== ANALISIS DE EFICIENCIA ===")
            print()
            
            # Cálculo de eficiencia en nodos
            nodos_astar = resultado_astar['nodes_explored']
            nodos_bfs = resultado_bfs['nodes_explored']
            
            if nodos_bfs > 0:
                eficiencia_nodos = ((nodos_bfs - nodos_astar) / nodos_bfs) * 100
                print(f"A* exploro {eficiencia_nodos:.1f}% menos nodos que BFS")
            else:
                print("No se puede calcular eficiencia en nodos (división por cero)")
            
            # Cálculo de eficiencia en tiempo
            tiempo_astar = resultado_astar['execution_time']
            tiempo_bfs = resultado_bfs['execution_time']
            
            if tiempo_bfs > 0 and tiempo_astar > 0:
                if tiempo_bfs > tiempo_astar:
                    # A* es más rápido
                    eficiencia_tiempo = ((tiempo_bfs - tiempo_astar) / tiempo_bfs) * 100
                    print(f"A* fue {eficiencia_tiempo:.1f}% mas rapido que BFS")
                else:
                    # BFS es más rápido
                    eficiencia_tiempo = ((tiempo_astar - tiempo_bfs) / tiempo_astar) * 100
                    print(f"BFS fue {eficiencia_tiempo:.1f}% mas rapido que A*")
            else:
                print("El tiempo de ejecucion es muy rapido para comparar")
            
            print()
            
            # Mostrar fórmulas de cálculo
            print("Evaluación por nodos: ", end="")
            if nodos_bfs > 0:
                print(f"(({nodos_bfs} - {nodos_astar}) / {nodos_bfs}) * 100 = {eficiencia_nodos:.1f}%")
            else:
                print("No aplicable")
            
            print("Evaluación por tiempo: ", end="")
            if tiempo_bfs > 0 and tiempo_astar > 0:
                if tiempo_bfs > tiempo_astar:
                    print(f"(({tiempo_bfs:.2f} - {tiempo_astar:.2f}) / {tiempo_bfs:.2f}) * 100 = {eficiencia_tiempo:.1f}%")
                else:
                    print(f"(({tiempo_astar:.2f} - {tiempo_bfs:.2f}) / {tiempo_astar:.2f}) * 100 = {eficiencia_tiempo:.1f}%")
            else:
                print("No aplicable")
            
            print()

    def evaluar_solucion_usuario(self, nivel, robot_start, camino_usuario):
        """Evalua si la solucion del usuario es correcta"""
        print("\n" + "="*60)
        print("EVALUANDO TU SOLUCION")
        print("="*60)
        
        # Simular la ejecucion de la solucion del usuario
        estado_juego = EstadoJuego(nivel['grid'], robot_start[0], robot_start[1])
        nodo_actual = estado_juego.get_initial_node()
        
        print(f"Secuencia ingresada: {' → '.join(camino_usuario)}")
        print(f"Total de pasos: {len(camino_usuario)}")
        print("\nSimulando ejecucion:")
        
        for i, accion in enumerate(camino_usuario, 1):
            print(f"  Paso {i}: {accion}")
            
            # Intentar ejecutar la accion
            sucesores = estado_juego.get_successors(nodo_actual)
            siguiente_nodo = None
            
            for sucesor in sucesores:
                if sucesor.action == accion:
                    siguiente_nodo = sucesor
                    break
            
            if siguiente_nodo is None:
                print(f"    Accion invalida en posicion ({nodo_actual.x}, {nodo_actual.y})")
                return False, len(camino_usuario)
            
            nodo_actual = siguiente_nodo
            print(f"    Robot en ({nodo_actual.x}, {nodo_actual.y}), luces: {nodo_actual.lights}")
        
        # Verificar si se alcanzo la meta
        es_meta = estado_juego.is_goal(nodo_actual)
        
        if es_meta:
            print(f"\n¡SOLUCION CORRECTA! Todas las luces encendidas en {len(camino_usuario)} pasos")
            return True, len(camino_usuario)
        else:
            luces_encendidas = sum(nodo_actual.lights)
            total_luces = len(nodo_actual.lights)
            print(f"\nSolucion incompleta. Luces encendidas: {luces_encendidas}/{total_luces}")
            return False, len(camino_usuario)