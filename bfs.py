""" Implementacion del algoritmo BFS (Busqueda en Anchura) """
import time
from collections import deque

class BusquedaAnchura:
    def __init__(self, estado_juego):
        self.estado_juego = estado_juego
        self.nodos_explorados = 0
        self.nodos_visitados = []

    #Ejecuta el algoritmo BFS para encontrar la solucion
    def resolver(self):
        self.nodos_explorados = 0
        self.nodos_visitados = []
        tiempo_inicio = time.perf_counter()
        
        nodo_inicial = self.estado_juego.obtener_nodo_inicial()
        cola = deque([nodo_inicial])
        visitados = set()
        contador_visitas = 0

        while cola:
            nodo_actual = cola.popleft()
            self.nodos_explorados += 1
            contador_visitas += 1
            nodo_actual.orden_visita = contador_visitas
            self.nodos_visitados.append(nodo_actual)

            # Verificar si llegamos al objetivo
            if self.estado_juego.es_meta(nodo_actual):
                tiempo_fin = time.perf_counter()
                return {
                    'exito': True,
                    'camino': nodo_actual.obtener_camino(),
                    'nodos_explorados': self.nodos_explorados,
                    'tiempo_ejecucion': (tiempo_fin - tiempo_inicio) * 1000,
                    'pasos': nodo_actual.costo,
                    'nodos_visitados': self.nodos_visitados,
                    'nodo_final': nodo_actual
                }

            clave_actual = nodo_actual.obtener_clave()
            if clave_actual in visitados:
                continue
            
            visitados.add(clave_actual)

            # Generar sucesores
            sucesores = self.estado_juego.obtener_sucesores(nodo_actual)
            
            for sucesor in sucesores:
                clave_sucesor = sucesor.obtener_clave()
                
                if clave_sucesor not in visitados:
                    cola.append(sucesor)

        tiempo_fin = time.perf_counter()
        return {
            'exito': False,
            'camino': [],
            'nodos_explorados': self.nodos_explorados,
            'tiempo_ejecucion': (tiempo_fin - tiempo_inicio) * 1000,
            'pasos': 0,
            'nodos_visitados': self.nodos_visitados,
            'nodo_final': None
        }