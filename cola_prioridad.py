""" Implementacion de una cola de prioridad usando un heap binario """
import heapq

class ColaPrioridad:
    def __init__(self, funcion_comparacion=None):
        self.elementos = []
        self.comparar = funcion_comparacion or (lambda a, b: a - b)
        self.contador = 0  # Para evitar comparaciones entre objetos

    #Agrega un elemento a la cola
    def encolar(self, elemento):
        # Usamos el counter para evitar comparaciones entre nodos
        heapq.heappush(self.elementos, (elemento.costo_total, self.contador, elemento))
        self.contador += 1

    #Elimina y retorna el elemento con mayor prioridad (menor valor)
    def desencolar(self):
        if self.esta_vacia():
            return None
        _, _, elemento = heapq.heappop(self.elementos)
        return elemento

    # Verifica si la cola esta vacia
    def esta_vacia(self):
        return len(self.elementos) == 0

    # Retorna el tamaño actual de la cola
    def tamaño(self):
        return len(self.elementos)