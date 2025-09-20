""" Implementacion de una cola de prioridad usando un heap binario """
import heapq

class ColaPrioridad:
    def __init__(self, compare_fn=None):
        self.items = []
        self.compare = compare_fn or (lambda a, b: a - b)
        self.counter = 0  # Para evitar comparaciones entre objetos

    #Agrega un elemento a la cola
    def enqueue(self, item):
        # Usamos el counter para evitar comparaciones entre nodos
        heapq.heappush(self.items, (item.total_cost, self.counter, item))
        self.counter += 1

    #Elimina y retorna el elemento con mayor prioridad (menor valor)
    def dequeue(self):
        if self.is_empty():
            return None
        _, _, item = heapq.heappop(self.items)
        return item

    # Verifica si la cola esta vacia
    def is_empty(self):
        return len(self.items) == 0

    # Retorna el tamaño actual de la cola
    def size(self):
        return len(self.items)