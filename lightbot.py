""" Juego LightBot """
import os
import time
from estado import EstadoJuego
from renderizador import Renderizador
from a_estrella import AEstrella
from bfs import BusquedaAnchura
from niveles import get_level

# Limpia la consola
def clearconsole():
    os.system('cls' if os.name == 'nt' else 'clear')

class LightBot:
    def __init__(self):
        self.renderizador = Renderizador()
        self.nivel_actual = None
        self.estado_juego = None

    # Función principal para jugar el juego
    def jugar(self):
        clearconsole()
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

    # Muestra el menu principal
    def _mostrar_menu(self):
        print("\n" + "=" * 50)
        print("MENU PRINCIPAL")
        print("=" * 50)
        print("1. Jugar")
        print("2. Instrucciones")
        print("3. Salir")
        print()

    # Muestra las instrucciones del juego
    def _mostrar_instrucciones(self):
        clearconsole()
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
        clearconsole()

    # Modo de juego interactivo
    def _jugar(self):
        clearconsole()
        print("\nMODO DE JUEGO - Ingresa tu solucion")
        print("=" * 50)
        
        # Seleccionar nivel con nuevo formato
        print("DIFICULTAD DEL JUEGO")
        print("1. Fácil")
        print("2. Medio")
        print("3. Difícil")
        
        while True:
            try:
                nivel_num = int(input("Elige tu dificultad (1-3): "))
                if 1 <= nivel_num <= 3:
                    break
                else:
                    print("Nivel debe estar entre 1 y 3")
            except ValueError:
                print("Por favor ingresa un numero valido")
        
        nivel = get_level(nivel_num)
        robot_x, robot_y = nivel['robot_start']
        
        clearconsole()
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
        print("  0 = TERMINAR")
        print()
        
        camino_usuario = []
        estado_actual = EstadoJuego(nivel['grid'], robot_x, robot_y)
        nodo_actual = estado_actual.get_initial_node()
        
        print("Ingresa tu solucion paso a paso:")
        
        while True:
            clearconsole()
            print(f"Paso actual: {len(camino_usuario)}")
            self.renderizador.render_level(nivel, nodo_actual.x, nodo_actual.y, nodo_actual.lights)
            
            paso = input("Siguiente comando (1-5, 0 para terminar): ").strip()
            
            if paso == '0':
                break
            elif paso in ['1', '2', '3', '4', '5']:
                acciones = {
                    '1': 'ARRIBA',
                    '2': 'ABAJO', 
                    '3': 'IZQUIERDA',
                    '4': 'DERECHA',
                    '5': 'ENCENDER'
                }
                accion = acciones[paso]
                sucesores = estado_actual.get_successors(nodo_actual)
                siguiente = None
                
                for suc in sucesores:
                    if suc.action == accion:
                        siguiente = suc
                        break
                
                if siguiente:
                    nodo_actual = siguiente
                    camino_usuario.append(accion)
                    print(f"Ejecutado: {accion}")
                    time.sleep(0.5)
                else:
                    print("Movimiento no válido. Intenta otro comando.")
                    time.sleep(1)
            else:
                print("Comando inválido. Usa: 1, 2, 3, 4, 5, 0")
                time.sleep(1)
        
        if not camino_usuario:
            print("No ingresaste ninguna solucion.")
            return
        
        es_correcto = estado_actual.is_goal(nodo_actual)
        pasos_usuario = len(camino_usuario)
        
        clearconsole()
        print("\n" + "="*60)
        print("EVALUANDO TU SOLUCION")
        print("="*60)
        
        print(f"Secuencia ingresada: {' → '.join(camino_usuario)}")
        print(f"Total de pasos: {pasos_usuario}")
        
        if es_correcto:
            print(f"\n¡SOLUCION CORRECTA! Todas las luces encendidas en {pasos_usuario} pasos")
        else:
            luces_encendidas = sum(nodo_actual.lights)
            total_luces = len(nodo_actual.lights)
            print(f"\nSolucion incompleta. Luces encendidas: {luces_encendidas}/{total_luces}")
        
        input("\nPresiona ENTER para ver las soluciones de los algoritmos...")
        
        clearconsole()
        print("Resolviendo con algoritmos...")
        estado_juego = EstadoJuego(nivel['grid'], robot_x, robot_y)
        
        resolver_astar = AEstrella(estado_juego)
        resultado_astar = resolver_astar.resolver()
        
        resolver_bfs = BusquedaAnchura(estado_juego)
        resultado_bfs = resolver_bfs.resolver()
        
        # Mostrar comparacion incluyendo solucion del usuario
        clearconsole()
        print("\n" + "="*60)
        print("COMPARACION COMPLETA")
        print("="*60)
        print()
        print("Tu solucion:")
        print(f"Pasos: {pasos_usuario}")
        print(f"Correcta: {'Si' if es_correcto else 'No'}")
        print()
        
        # Mostrar resultados de algoritmos
        self.renderizador.mostrar_estadisticas(resultado_astar, resultado_bfs)
        
        # Mostrar explicacion de la heuristica al final
        nodo_inicial = estado_juego.get_initial_node()
        self.renderizador.mostrar_explicacion_heuristica(nodo_inicial, estado_juego.light_positions)
        
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
        else:
            clearconsole()

def main():
    juego = LightBot()
    juego.jugar()

if __name__ == "__main__":
    main()