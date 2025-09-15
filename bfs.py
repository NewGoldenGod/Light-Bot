"""
Implementacion del algoritmo BFS (Busqueda en Anchura)
"""
import time
from collections import deque

class BusquedaAnchura:
    def __init__(self, estado_juego):
        self.estado_juego = estado_juego
        self.nodos_explorados = 0
        self.nodos_visitados = []

    def resolver(self):
        """Ejecuta el algoritmo BFS para encontrar la solucion"""
        self.nodos_explorados = 0
        self.nodos_visitados = []
        tiempo_inicio = time.perf_counter()
        
        nodo_inicial = self.estado_juego.get_initial_node()
        cola = deque([nodo_inicial])
        visitados = set()
        contador_visitas = 0

        while cola:
            nodo_actual = cola.popleft()
            self.nodos_explorados += 1
            contador_visitas += 1
            nodo_actual.visited_order = contador_visitas
            self.nodos_visitados.append(nodo_actual)

            # Verificar si llegamos to the goal
            if self.estado_juego.is_goal(nodo_actual):
                tiempo_fin = time.perf_counter()
                return {
                    'success': True,
                    'path': nodo_actual.get_path(),
                    'nodes_explored': self.nodos_explorados,
                    'execution_time': (tiempo_fin - tiempo_inicio) * 1000,
                    'steps': nodo_actual.cost,
                    'visited_nodes': self.nodos_visitados,
                    'final_node': nodo_actual
                }

            clave_actual = nodo_actual.get_key()
            if clave_actual in visitados:
                continue
            
            visitados.add(clave_actual)

            # Generar sucesores
            sucesores = self.estado_juego.get_successors(nodo_actual)
            
            for sucesor in sucesores:
                clave_sucesor = sucesor.get_key()
                
                if clave_sucesor not in visitados:
                    cola.append(sucesor)

        tiempo_fin = time.perf_counter()
        return {
            'success': False,
            'path': [],
            'nodes_explored': self.nodos_explorados,
            'execution_time': (tiempo_fin - tiempo_inicio) * 1000,
            'steps': 0,
            'visited_nodes': self.nodos_visitados,
            'final_node': None
        }