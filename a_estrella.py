""" Implementacion del algoritmo A* """
import time
from cola_prioridad import ColaPrioridad

class AEstrella:
    def __init__(self, estado_juego):
        self.estado_juego = estado_juego
        self.nodos_explorados = 0
        self.nodos_visitados = []

    #Ejecuta el algoritmo A* para encontrar la solucion
    def resolver(self):
        self.nodos_explorados = 0
        self.nodos_visitados = []
        tiempo_inicio = time.perf_counter()
    
        nodo_inicial = self.estado_juego.get_initial_node()
        nodo_inicial.heuristic = self.estado_juego.heuristic(nodo_inicial)
        nodo_inicial.total_cost = nodo_inicial.cost + nodo_inicial.heuristic

        conjunto_abierto = ColaPrioridad()
        conjunto_cerrado = set()
    
        conjunto_abierto.enqueue(nodo_inicial)
        contador_visitas = 0

        while not conjunto_abierto.is_empty():
            nodo_actual = conjunto_abierto.dequeue()
            self.nodos_explorados += 1
            contador_visitas += 1
            nodo_actual.visited_order = contador_visitas
            self.nodos_visitados.append(nodo_actual)

            # Verificar si llegamos a la meta
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
            if clave_actual in conjunto_cerrado:
                continue
        
            conjunto_cerrado.add(clave_actual)

            # Generar sucesores
            sucesores = self.estado_juego.get_successors(nodo_actual)
        
            for sucesor in sucesores:
                clave_sucesor = sucesor.get_key()
            
                if clave_sucesor not in conjunto_cerrado:
                    sucesor.heuristic = self.estado_juego.heuristic(sucesor)
                    sucesor.total_cost = sucesor.cost + sucesor.heuristic
                    conjunto_abierto.enqueue(sucesor)

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