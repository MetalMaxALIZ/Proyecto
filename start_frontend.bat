@echo off
echo ================================
echo Starting React Frontend
echo ================================
echo.

cd frontend

REM Check if node_modules exist
if exist node_modules goto iniciar_app
goto instalar_dependencias

:instalar_dependencias
echo Installing Node.js dependencies - this may take several minutes...
call npm install
if errorlevel 1 goto error_npm
goto iniciar_app

:iniciar_app
echo.
echo Starting application at http://localhost:3000
echo Make sure the backend is running at http://localhost:5000
echo.
echo Press Ctrl+C to stop
echo.

call npm start
goto fin

:error_npm
echo.
echo ERROR: Dependency installation failed
echo Make sure Node.js is installed from nodejs.org
pause
exit /b 1

:fin
