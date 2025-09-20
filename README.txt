LIGHTBOT - JUEGO DE LOGICA CON ALGORITMOS DE BUSQUEDA

Este proyecto implementa el juego LightBot, un puzzle de lógica donde el jugador controla un robot que debe encender todas las luces de un nivel. El robot puede moverse en cuatro direcciones (arriba, abajo, izquierda, derecha) y encender luces cuando se encuentra sobre ellas. El objetivo es encontrar la secuencia optima de movimientos para completar cada nivel.

El juego incluye tres niveles de dificultad (fácil, medio y difícil) y permite al usuario ingresar su propia solución paso a paso. Además, implementa dos algoritmos de búsqueda para resolver automáticamente los puzzles: A* (algoritmo informado que usa heurística) y BFS (búsqueda en anchura sin información). Esto permite comparar la eficiencia entre algoritmos informados y no informados.

El sistema muestra estadísticas detalladas de rendimiento, incluyendo numero de nodos explorados, tiempo de ejecución y pasos de la solución. También evalúa la solución del usuario comparándola con las soluciones optimas encontradas por los algoritmos, proporcionando retroalimentación educativa sobre la eficiencia de diferentes enfoques de resolución de problemas.

La heurística implementada en el algoritmo A* combina dos factores clave para estimar la distancia al objetivo: el número de luces que aún faltan por encender y la distancia Manhattan (suma de diferencias absolutas en coordenadas x e y) hasta la luz apagada más cercana. Esta función heurística es admisible porque nunca sobreestima el costo real para alcanzar la meta, garantizando que A* encuentre la solución óptima. La comparación entre A* y BFS demuestra claramente cómo el uso de información heurística reduce significativamente el espacio de búsqueda, explorando menos nodos y encontrando la solución de manera más eficiente.

Puedes compilar lightbot.py o doble clic en run.bat