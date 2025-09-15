"""
Implementacion de una cola de prioridad usando un heap binario
"""
import heapq

class ColaPrioridad:
    def __init__(self, compare_fn=None):
        self.items = []
        self.compare = compare_fn or (lambda a, b: a - b)
        self.counter = 0  # Para evitar comparaciones entre objetos

    def enqueue(self, item):
        """Agrega un elemento a la cola"""
        # Usamos el counter para evitar comparaciones entre nodos
        heapq.heappush(self.items, (item.total_cost, self.counter, item))
        self.counter += 1

    def dequeue(self):
        """Remueve y retorna el elemento con mayor prioridad"""
        if self.is_empty():
            return None
        
        _, _, item = heapq.heappop(self.items)
        return item

    def is_empty(self):
        """Verifica si la cola está vacía"""
        return len(self.items) == 0

    def size(self):
        """Retorna el tamaño de la cola"""
        return len(self.items)