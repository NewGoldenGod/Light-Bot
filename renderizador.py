""" Clase para mostrar el estado del juego en consola """
from estado import EstadoJuego

class Renderizador:
    # Inicializa los simbolos para cada tipo de celda
    def __init__(self):
        self.simbolos = {
            0: '.',  # Piso normal
            1: '#',  # Obstaculo
            2: 'L',  # Luz apagada
            'luz_encendida': 'O',  # Luz encendida
            'robot': 'R',     # Robot
            'robot_en_luz': '@'  # Robot en luz encendida
        }

    # Renderiza el nivel en consola
    def renderizar_nivel(self, nivel, robot_x, robot_y, estados_luces=None):
        cuadricula = nivel['cuadricula']
        filas = len(cuadricula)
        columnas = len(cuadricula[0])
        
        if estados_luces is None:
            cantidad_luces = self._contar_luces(cuadricula)
            estados_luces = [0] * cantidad_luces
        
        print(f"\n=== {nivel['nombre']} ===")
        print(f"Descripcion: {nivel['descripcion']}")
        print()
        
        # Crear representacion visual
        cuadricula_mostrar = []
        for i in range(filas):
            fila = []
            for j in range(columnas):
                celda = self._obtener_simbolo_celda(cuadricula[i][j], i, j, robot_x, robot_y, estados_luces, cuadricula)
                fila.append(celda)
            cuadricula_mostrar.append(fila)
        
        # Mostrar el tablero
        for fila in cuadricula_mostrar:
            print(' '.join(f'{celda:^3}' for celda in fila))
        
        print()
        self._mostrar_leyenda()

    # Obtiene el simbolo adecuado para una celda
    def _obtener_simbolo_celda(self, tipo_celda, fila, col, robot_x, robot_y, estados_luces, cuadricula):
        if fila == robot_x and col == robot_y:
            if tipo_celda == 2:
                indice_luz = self._obtener_indice_luz(fila, col, cuadricula)
                if indice_luz is not None and estados_luces[indice_luz] == 1:
                    return self.simbolos['robot_en_luz']
                else:
                    return self.simbolos['robot']
            else:
                return self.simbolos['robot']
        else:
            if tipo_celda == 0:
                return self.simbolos[0]
            elif tipo_celda == 1:
                return self.simbolos[1]
            elif tipo_celda == 2:
                indice_luz = self._obtener_indice_luz(fila, col, cuadricula)
                if indice_luz is not None and estados_luces[indice_luz] == 1:
                    return self.simbolos['luz_encendida']
                else:
                    return self.simbolos[2]

    # Obtiene el indice de la luz en la lista de estados
    def _obtener_indice_luz(self, fila, col, cuadricula):
        posiciones_luces = self._obtener_posiciones_luces(cuadricula)
        for i, (lx, ly) in enumerate(posiciones_luces):
            if lx == fila and ly == col:
                return i
        return None

    # Obtiene las posiciones de todas las luces en el nivel
    def _obtener_posiciones_luces(self, cuadricula):
        posiciones = []
        for i in range(len(cuadricula)):
            for j in range(len(cuadricula[0])):
                if cuadricula[i][j] == 2:
                    posiciones.append((i, j))
        return posiciones

    # Cuenta cuantas luces hay en el nivel
    def _contar_luces(self, cuadricula):
        contador = 0
        for i in range(len(cuadricula)):
            for j in range(len(cuadricula[0])):
                if cuadricula[i][j] == 2:
                    contador += 1
        return contador

    # Muestra la leyenda de simbolos
    def _mostrar_leyenda(self):
        print("Leyenda:")
        print(f"  {self.simbolos[0]} = Piso normal")
        print(f"  {self.simbolos[1]} = Obstaculo")
        print(f"  {self.simbolos[2]} = Luz apagada")
        print(f"  {self.simbolos['luz_encendida']} = Luz encendida")
        print(f"  {self.simbolos['robot']} = Robot")
        print(f"  {self.simbolos['robot_en_luz']} = Robot en luz encendida")
        print()
        print("Comandos de movimiento:")
        print("  1 = ARRIBA, 2 = ABAJO, 3 = IZQUIERDA, 4 = DERECHA, 5 = ENCENDER")
        print()

    # Muestra la solucion encontrada
    def mostrar_solucion(self, camino, nombre_algoritmo=""):
        if not camino:
            print("El robot ya esta en la meta!")
            return
        
        if nombre_algoritmo:
            print(f"Solucion encontrada por {nombre_algoritmo}:")
        else:
            print("Solucion encontrada:")
        
        for i, paso in enumerate(camino, 1):
            print(f"  {i}. {paso}")
        print()

    # Muestra el calculo de la heuristica para un nodo dado
    def mostrar_explicacion_heuristica(self, nodo, posiciones_luces):
        luces_apagadas = sum(1 for luz in nodo.luces if luz == 0)
        print(f"\nCALCULO DE HEURISTICA para posicion ({nodo.x}, {nodo.y}):")
        print(f"   Estado de luces: {nodo.luces}")
        print(f"   Luces apagadas: {luces_apagadas}")
        
        if luces_apagadas == 0:
            print(f"   Distancia minima: 0 (todas las luces encendidas)")
            print(f"   h(n) = {luces_apagadas} + 0 = 0")
            return 0
        
        distancia_minima = float('inf')
        luz_mas_cercana = None
        
        for i, (lx, ly) in enumerate(posiciones_luces):
            if nodo.luces[i] == 0:
                distancia = abs(nodo.x - lx) + abs(nodo.y - ly)
                if distancia < distancia_minima:
                    distancia_minima = distancia
                    luz_mas_cercana = (lx, ly)
        
        print(f"   Luz mas cercana: {luz_mas_cercana}")
        print(f"   Distancia minima: {distancia_minima}")
        print(f"   h(n) = {luces_apagadas} + {distancia_minima} = {luces_apagadas + distancia_minima}")
        print(f"   g(n) = {nodo.costo}, f(n) = g(n) + h(n) = {nodo.costo + luces_apagadas + distancia_minima}")
        return luces_apagadas + distancia_minima

    # Obtiene una descripcion resumida de los movimientos realizados
    def _obtener_descripcion_movimientos(self, nodos_visitados):
        if not nodos_visitados:
            return "No hay movimientos para analizar"
        coste_total = nodos_visitados[-1].costo if nodos_visitados else 0
        return f"Coste total: {coste_total}"

    # Muestra estadisticas comparativas entre A* y BFS
    def mostrar_estadisticas(self, resultado_astar, resultado_bfs):
        print("\n" + "="*60)
        print("COMPARACION DE ALGORITMOS")
        print("="*60)
        print()
        
        print("A* (Heuristica - Algoritmo Informado):")
        print(f"  Nodos explorados: {resultado_astar['nodos_explorados']}")
        print(f"  Pasos solucion: {resultado_astar['pasos']}")
        print(f"  Tiempo: {resultado_astar['tiempo_ejecucion']:.2f}ms")
        print()
        
        # Mostrar descripción de movimientos para A*
        if resultado_astar['nodos_visitados']:
            descripcion = self._obtener_descripcion_movimientos(resultado_astar['nodos_visitados'])
            print(f"  {descripcion}")
            print()

        
        self.mostrar_solucion(resultado_astar['camino'], "A*")
        
        print("BFS (Busqueda Ciega - Sin informacion):")
        print(f"  Nodos explorados: {resultado_bfs['nodos_explorados']}")
        print(f"  Pasos solucion: {resultado_bfs['pasos']}")
        print(f"  Tiempo: {resultado_bfs['tiempo_ejecucion']:.2f}ms")
        
        # Mostrar descripción de movimientos para BFS
        if resultado_bfs['nodos_visitados']:
            descripcion = self._obtener_descripcion_movimientos(resultado_bfs['nodos_visitados'])
            print(f"  {descripcion}")
            print()
        
        self.mostrar_solucion(resultado_bfs['camino'], "BFS")
        print()
    
        if resultado_astar['exito'] and resultado_bfs['exito']:
            print("=== ANALISIS DE EFICIENCIA ===")
            print()
            
            # Cálculo de eficiencia en nodos
            nodos_astar = resultado_astar['nodos_explorados']
            nodos_bfs = resultado_bfs['nodos_explorados']
            
            if nodos_bfs > 0:
                eficiencia_nodos = ((nodos_bfs - nodos_astar) / nodos_bfs) * 100
                print(f"A* exploro {eficiencia_nodos:.1f}% menos nodos que BFS")
            else:
                print("No se puede calcular eficiencia en nodos (división por cero)")
            
            # Cálculo de eficiencia en tiempo
            tiempo_astar = resultado_astar['tiempo_ejecucion']
            tiempo_bfs = resultado_bfs['tiempo_ejecucion']
            
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

    # Evalua la solucion ingresada por el usuario
    def evaluar_solucion_usuario(self, nivel, inicio_robot, camino_usuario):
        print("\n" + "="*60)
        print("EVALUANDO TU SOLUCION")
        print("="*60)
        estado_juego = EstadoJuego(nivel['cuadricula'], inicio_robot[0], inicio_robot[1])
        nodo_actual = estado_juego.obtener_nodo_inicial()
        
        print(f"Secuencia ingresada: {' → '.join(camino_usuario)}")
        print(f"Total de pasos: {len(camino_usuario)}")
        print("\nSimulando ejecucion:")
        
        for i, accion in enumerate(camino_usuario, 1):
            print(f"  Paso {i}: {accion}")
            sucesores = estado_juego.obtener_sucesores(nodo_actual)
            siguiente_nodo = None
            
            for sucesor in sucesores:
                if sucesor.accion == accion:
                    siguiente_nodo = sucesor
                    break
            
            if siguiente_nodo is None:
                print(f"    Accion invalida en posicion ({nodo_actual.x}, {nodo_actual.y})")
                return False, len(camino_usuario)
            
            nodo_actual = siguiente_nodo
            print(f"    Robot en ({nodo_actual.x}, {nodo_actual.y}), luces: {nodo_actual.luces}")
        
        es_meta = estado_juego.es_meta(nodo_actual)
        
        if es_meta:
            print(f"\n¡SOLUCION CORRECTA! Todas las luces encendidas en {len(camino_usuario)} pasos")
            return True, len(camino_usuario)
        else:
            luces_encendidas = sum(nodo_actual.luces)
            total_luces = len(nodo_actual.luces)
            print(f"\nSolucion incompleta. Luces encendidas: {luces_encendidas}/{total_luces}")
            return False, len(camino_usuario)