@echo off
echo ================================
echo Iniciando Backend Flask
echo ================================
echo.

cd backend

REM Verificar si existe el entorno virtual
if exist venv goto activar_venv
goto crear_venv

:activar_venv
echo Activando entorno virtual...
call venv\Scripts\activate.bat
goto verificar_modelo

:crear_venv
echo Creando entorno virtual...
py -m venv venv
if errorlevel 1 goto error_python

call venv\Scripts\activate.bat

echo Actualizando pip...
python -m pip install --upgrade pip

echo Instalando dependencias - esto puede tardar varios minutos...
pip install flask flask-cors requests
pip install pandas numpy scikit-learn

if errorlevel 1 goto error_instalacion

:verificar_modelo
REM Verificar si existe el modelo
if not exist ..\data goto advertencia_modelo
goto iniciar_servidor

:advertencia_modelo
echo.
echo ADVERTENCIA: No se encontro la carpeta data con el modelo
echo Por favor, ejecuta la celda de exportacion en pruebas.ipynb
echo.
pause

:iniciar_servidor
echo.
echo Iniciando servidor en http://localhost:5000
echo Presiona Ctrl+C para detener
echo.

python app.py
goto fin

:error_python
echo ERROR: No se pudo crear el entorno virtual
echo Asegurate de tener Python instalado desde python.org
pause
exit /b 1

:error_instalacion
echo.
echo ERROR: Fallo la instalacion de dependencias
echo Intenta instalar Visual Studio Build Tools si el error persiste
pause
exit /b 1

:fin
