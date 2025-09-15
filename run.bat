@echo off
chcp 65001 >nul
echo ================================
echo     LIGHTBOT GAME - RUNNER
echo ================================
echo.

REM Verificar si Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python no encontrado.
    echo Por favor instala Python desde https://www.python.org/
    echo Asegurate de agregar Python al PATH durante la instalacion.
    pause
    exit /b 1
)

REM Verificar si el archivo principal existe
if not exist "lightbot.py" (
    echo ERROR: No se encuentra el archivo lightbot_game.py
    echo Asegurate de que este archivo .bat este en la misma carpeta que el juego.
    pause
    exit /b 1
)

echo Ejecutando LightBot Game...
echo.
echo Presiona Ctrl+C para salir en cualquier momento.
echo.

REM Ejecutar el juego
python lightbot.py

REM Pausar al finalizar
echo.
echo Juego terminado.
pause