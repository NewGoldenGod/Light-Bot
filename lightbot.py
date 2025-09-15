"""
Juego LightBot
"""
from estado import EstadoJuego
from renderizador import Renderizador
from a_estrella import AEstrella
from bfs import BusquedaAnchura
from niveles import get_level

class LightBot:
    def __init__(self):
        self.renderizador = Renderizador()
        self.nivel_actual = None
        self.estado_juego = None

    def jugar(self):
        """Inicia el juego principal"""
        print("LIGHTBOT")
        print("=" * 50)
        
        while True:
            self._mostrar_menu()
            opcion = input("Selecciona una opcion: ").strip()
            
            if opcion == '1':
                self._jugar()
            elif opcion == '2':
                self._mostrar_instrucciones()
            elif opcion == '3':
                print("¡Gracias por jugar!")
                break
            else:
                print("Opcion invalida. Intenta de nuevo.")

    def _mostrar_menu(self):
        """Muestra el menú principal"""
        print("\n" + "=" * 50)
        print("MENU PRINCIPAL")
        print("=" * 50)
        print("1. Jugar")
        print("2. Instrucciones")
        print("3. Salir")
        print()

    def _mostrar_instrucciones(self):
        """Muestra las instrucciones del juego"""
        print("\n" + "=" * 60)
        print("INSTRUCCIONES")
        print("=" * 60)
        print("El objetivo es encender todas las luces del nivel.")
        print("Comandos:")
        print("  1 = ARRIBA")
        print("  2 = ABAJO")
        print("  3 = IZQUIERDA")
        print("  4 = DERECHA")
        print("  5 = ENCENDER")
        print()
        print("Al ejecutar ENCENDER, el robot enciende la luz solo si")
        print("esta en una casilla con luz apagada.")
        print("Si el movimiento choca con un obstaculo, el robot no se mueve.")
        print()
        input("Presiona ENTER para volver al menu principal...")

    def _jugar(self):
        """Modo donde el usuario juega"""
        print("\nMODO DE JUEGO - Ingresa tu solucion")
        print("=" * 50)
        
        # Seleccionar nivel
        while True:
            try:
                nivel_num = int(input("Selecciona nivel (1-3): "))
                if 1 <= nivel_num <= 3:
                    break
                else:
                    print("Nivel debe estar entre 1 y 3")
            except ValueError:
                print("Por favor ingresa un numero valido")
        
        nivel = get_level(nivel_num)
        robot_x, robot_y = nivel['robot_start']
        
        # Mostrar el problema completo
        print("\n" + "="*60)
        print("PROBLEMA A RESOLVER")
        print("="*60)
        self.renderizador.render_level(nivel, robot_x, robot_y)
        
        print("Comandos disponibles:")
        print("  1 = ARRIBA")
        print("  2 = ABAJO")
        print("  3 = IZQUIERDA")
        print("  4 = DERECHA")
        print("  5 = ENCENDER")
        print()
        
        # Solicitar solucion del usuario
        camino_usuario = []
        print("Ingresa tu solucion paso a paso (escribe '0' para terminar):")
        
        while True:
            paso = input(f"Paso {len(camino_usuario) + 1}: ").strip()
            
            if paso == '0':
                break
            elif paso in ['1', '2', '3', '4', '5']:
                # Convertir numero a accion
                acciones = {
                    '1': 'ARRIBA',
                    '2': 'ABAJO', 
                    '3': 'IZQUIERDA',
                    '4': 'DERECHA',
                    '5': 'ENCENDER'
                }
                camino_usuario.append(acciones[paso])
                print(f"  Agregado: {acciones[paso]}")
            else:
                print("  Comando invalido. Usa: 1, 2, 3, 4, 5, 0")
        
        if not camino_usuario:
            print("No ingresaste ninguna solucion.")
            return
        
        # Evaluar la solucion del usuario
        es_correcto, pasos_usuario = self.renderizador.evaluar_solucion_usuario(
            nivel, (robot_x, robot_y), camino_usuario
        )
        
        input("\nPresiona ENTER para ver las soluciones de los algoritmos...")
        
        # Resolver con algoritmos
        estado_juego = EstadoJuego(nivel['grid'], robot_x, robot_y)
        
        resolver_astar = AEstrella(estado_juego)
        resultado_astar = resolver_astar.resolver()
        
        resolver_bfs = BusquedaAnchura(estado_juego)
        resultado_bfs = resolver_bfs.resolver()
        
        # Mostrar comparacion incluyendo solucion del usuario
        print("\n" + "="*60)
        print("COMPARACION COMPLETA")
        print("="*60)
        print()
        print("Tu solucion:")
        print(f"  Pasos: {pasos_usuario}")
        print(f"  Correcta: {'Si' if es_correcto else 'No'}")
        print()
        
        # Mostrar explicacion de la heuristica
        nodo_inicial = estado_juego.get_initial_node()
        self.renderizador.mostrar_explicacion_heuristica(nodo_inicial, estado_juego.light_positions)
        
        # Mostrar resultados de algoritmos
        self.renderizador.mostrar_estadisticas(resultado_astar, resultado_bfs)
        
        if es_correcto and resultado_astar['success']:
            pasos_optimos = resultado_astar['steps']
            if pasos_usuario == pasos_optimos:
                print("¡FELICITACIONES! Encontraste la solucion optima!")
            elif pasos_usuario > pasos_optimos:
                print(f"Tu solucion usa {pasos_usuario - pasos_optimos} pasos adicionales")
        
        # Preguntar si desea jugar nuevamente
        jugar_de_nuevo = input("\n¿Deseas jugar de nuevo? (s/n): ").strip().lower()
        if jugar_de_nuevo == 's':
            self._jugar()

def main():
    """Funcion principal"""
    juego = LightBot()
    juego.jugar()

if __name__ == "__main__":
    main()