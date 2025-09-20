""" Clase que representa un nodo en el espacio de estados del juego LightBot """
class Nodo:
    def __init__(self, x, y, luces, padre=None, accion=None, costo=0):
        self.x = x                    # Posicion X del robot
        self.y = y                    # Posicion Y del robot
        self.luces = tuple(luces)     # Tupla con estado de las luces (0=apagada, 1=encendida)
        self.padre = padre            # Nodo padre para reconstruir el camino
        self.accion = accion          # Accion que llevo a este estado
        self.costo = costo            # Costo acumulado (g en A*)
        self.heuristica = 0           # Valor heuristico (h en A*)
        self.costo_total = 0          # Costo total (f = g + h en A*)
        self.orden_visita = -1        # Orden en que fue visitado

    # Genera una clave unica para el nodo basada en su estado
    def obtener_clave(self):
        return f"{self.x},{self.y},{','.join(map(str, self.luces))}"

    # Verifica si dos nodos son iguales en posicion y estado de luces
    def es_igual(self, otro):
        return (self.x == otro.x and 
                self.y == otro.y and 
                self.luces == otro.luces)

    # Crea una copia del nodo con posibles modificaciones
    def copiar(self, nuevo_x=None, nuevo_y=None, nuevas_luces=None):
        if nuevo_x is None:
            nuevo_x = self.x
        if nuevo_y is None:
            nuevo_y = self.y
        if nuevas_luces is None:
            nuevas_luces = list(self.luces)
        
        return Nodo(nuevo_x, nuevo_y, nuevas_luces, self.padre, self.accion, self.costo)

    # Reconstruye el camino desde el nodo inicial hasta este nodo
    def obtener_camino(self):
        camino = []
        actual = self
        
        while actual.padre is not None:
            camino.insert(0, actual.accion)
            actual = actual.padre
        
        return camino

    # Representacion en string del nodo para depuracion
    def __str__(self):
        return f"Nodo(x={self.x}, y={self.y}, luces={self.luces}, costo={self.costo})"