@echo off
echo ================================
echo Starting Flask Backend
echo ================================
echo.

cd backend

REM Check if virtual environment exists
if exist venv goto activar_venv
goto crear_venv

:activar_venv
echo Activating virtual environment...
call venv\Scripts\activate.bat
goto verificar_modelo

:crear_venv
echo Creating virtual environment...
py -m venv venv
if errorlevel 1 goto error_python

call venv\Scripts\activate.bat

echo Updating pip...
python -m pip install --upgrade pip

echo Installing dependencies - this may take several minutes...
pip install flask flask-cors requests
pip install pandas numpy scikit-learn

if errorlevel 1 goto error_instalacion

:verificar_modelo
REM Check if model exists
if not exist ..\data goto advertencia_modelo
goto iniciar_servidor

:advertencia_modelo
echo.
echo WARNING: data folder with model not found
echo Please run the export cell in pruebas.ipynb
echo.
pause

:iniciar_servidor
echo.
echo Starting server at http://localhost:5000
echo Press Ctrl+C to stop
echo.

python app.py
goto fin

:error_python
echo ERROR: Could not create virtual environment
echo Make sure Python is installed from python.org
pause
exit /b 1

:error_instalacion
echo.
echo ERROR: Dependency installation failed
echo Try installing Visual Studio Build Tools if error persists
pause
exit /b 1

:fin
