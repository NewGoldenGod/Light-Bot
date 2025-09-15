# LightBot Python - Comparación A* vs BFS

## Descripción del Proyecto

Este proyecto implementa una versión simplificada del juego LightBot en Python donde un robot debe encender todas las luces azules en un tablero. El objetivo principal es comparar la eficiencia de dos algoritmos de búsqueda:

- **A*** (con heurística)
- **BFS** (búsqueda ciega)

## Reglas del Juego Simplificado

1. **Movimiento**: El robot puede moverse instantáneamente en 4 direcciones (arriba, abajo, izquierda, derecha) sin necesidad de girar.

2. **Objetivo**: Encender todas las luces azules del tablero.

3. **Acciones disponibles**:
   - **MOVER**: A una casilla adyacente (si no es obstáculo)
   - **ENCENDER**: La luz en la posición actual (si hay una luz apagada)

## Representación del Tablero

- **0**: Piso normal (el robot puede caminar)
- **1**: Obstáculo (el robot NO puede pasar)
- **2**: Casilla objetivo con luz azul (debe ser encendida)

## Algoritmos Implementados

### A* (A-Star)
- Utiliza una heurística optimista: `h(n) = luces_apagadas + distancia_a_luz_más_cercana`
- Explora nodos de manera inteligente priorizando los más prometedores
- Garantiza encontrar la solución óptima

### BFS (Breadth-First Search)
- Búsqueda ciega que explora todos los nodos nivel por nivel
- No utiliza información heurística
- Garantiza encontrar la solución óptima pero puede ser menos eficiente

## Estructura del Código

### Archivos Principales

1. **node.py**: Representa un estado del juego (posición del robot + estado de luces)
2. **game_state.py**: Maneja las reglas del juego y generación de sucesores
3. **astar.py**: Implementación del algoritmo A*
4. **bfs.py**: Implementación del algoritmo BFS
5. **game_renderer.py**: Renderizado en consola del juego
6. **priority_queue.py**: Cola de prioridad para A*
7. **levels.py**: Definición de los 3 niveles
8. **lightbot_game.py**: Clase principal del juego

### Niveles Incluidos

1. **Nivel 1**: Tablero 3x3 con 2 luces
2. **Nivel 2**: Tablero 4x4 con 3 luces y obstáculos
3. **Nivel 3**: Tablero 5x5 con 4 luces en laberinto complejo

## Cómo Ejecutar

```bash
python lightbot_game.py
```

## Funcionalidades

1. **Resolución Automática**: Ve cómo A* y BFS resuelven cada nivel
2. **Comparación de Rendimiento**: Estadísticas detalladas de ambos algoritmos
3. **Modo Manual**: Juega tú mismo e intenta encontrar el camino óptimo
4. **Análisis Completo**: Compara el rendimiento en todos los niveles

## Métricas de Comparación

Para cada algoritmo se muestran:
- **Nodos explorados**: Cantidad de estados visitados
- **Pasos de la solución**: Longitud del camino encontrado
- **Tiempo de ejecución**: Tiempo en milisegundos

## Resultados Esperados

Generalmente A* debería:
- Explorar menos nodos que BFS
- Encontrar la solución en menos tiempo
- Mantener la optimalidad de la solución

Esto demuestra la ventaja de usar información heurística en problemas de búsqueda.

## Ejemplo de Uso

```
🤖 LIGHTBOT - Comparación de algoritmos A* vs BFS
==================================================

MENÚ PRINCIPAL
==================================================
1. Resolver Nivel 1 (Básico)
2. Resolver Nivel 2 (Intermedio)
3. Resolver Nivel 3 (Avanzado)
4. Comparar todos los niveles
5. Juego manual (adivinar camino)
6. Salir

Selecciona una opción: 1

=== Nivel Básico ===
Descripción: Dos luces simples

 R   .   L 
 .   #   . 
 .   .   L 

Resolviendo con A*...
Resolviendo con BFS...

=== COMPARACIÓN DE ALGORITMOS ===

A* (Heurística):
  Nodos explorados: 8
  Pasos solución: 6
  Tiempo: 0.15ms

BFS (Búsqueda Ciega):
  Nodos explorados: 12
  Pasos solución: 6
  Tiempo: 0.23ms

=== ANÁLISIS ===
A* exploró 33.3% menos nodos que BFS
A* fue 34.8% más rápido que BFS

Solución encontrada:
  1. DERECHA
  2. DERECHA
  3. ENCENDER
  4. ABAJO
  5. ABAJO
  6. ENCENDER
```