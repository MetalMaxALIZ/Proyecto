@echo off
echo ================================
echo Iniciando Frontend React
echo ================================
echo.

cd frontend

REM Verificar si existen los node_modules
if exist node_modules goto iniciar_app
goto instalar_dependencias

:instalar_dependencias
echo Instalando dependencias de Node.js - esto puede tardar varios minutos...
call npm install
if errorlevel 1 goto error_npm
goto iniciar_app

:iniciar_app
echo.
echo Iniciando aplicacion en http://localhost:3000
echo Asegurate de que el backend este ejecutandose en http://localhost:5000
echo.
echo Presiona Ctrl+C para detener
echo.

call npm start
goto fin

:error_npm
echo.
echo ERROR: Fallo la instalacion de dependencias
echo Asegurate de tener Node.js instalado desde nodejs.org
pause
exit /b 1

:fin
