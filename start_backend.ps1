# Script para iniciar el backend Flask
# Ejecuta este script desde el directorio raíz del proyecto

Write-Host "Iniciando servidor Flask..." -ForegroundColor Green

# Navegar al directorio backend
Set-Location -Path "backend"

# Buscar Python instalado
$pythonCmd = $null
$pythonPaths = @(
    "C:\Users\Metal\AppData\Local\Programs\Python\Python313\python.exe",
    "C:\Python313\python.exe",
    "C:\Python312\python.exe",
    "C:\Python311\python.exe",
    "C:\Python310\python.exe",
    "py.exe"
)

foreach ($path in $pythonPaths) {
    if (Test-Path $path -ErrorAction SilentlyContinue) {
        $pythonCmd = $path
        Write-Host "Python encontrado en: $pythonCmd" -ForegroundColor Green
        break
    }
}

if (-not $pythonCmd) {
# Iniciar el servidor
Write-Host "`nIniciando servidor en http://localhost:5000" -ForegroundColor Green
Write-Host "Presiona Ctrl+C para detener el servidor`n" -ForegroundColor Yellow

if (Test-Path ".\venv\Scripts\python.exe") {
    & ".\venv\Scripts\python.exe" app.py
} else {
    & $pythonCmd app.py
}-Host "Usando py launcher" -ForegroundColor Green
    } catch {
        Write-Host "ERROR: No se encontró Python instalado." -ForegroundColor Red
        Write-Host "Por favor, instala Python desde python.org" -ForegroundColor Yellow
        pause
        exit 1
    }
}

# Verificar si existe el entorno virtual
if (Test-Path "venv") {
    Write-Host "Activando entorno virtual..." -ForegroundColor Yellow
    & ".\venv\Scripts\Activate.ps1"
} else {
    Write-Host "No se encontró entorno virtual. Creando uno nuevo..." -ForegroundColor Yellow
    & $pythonCmd -m venv venv
    
    if (Test-Path ".\venv\Scripts\Activate.ps1") {
        & ".\venv\Scripts\Activate.ps1"
    }
    
    Write-Host "Instalando dependencias (esto puede tardar varios minutos)..." -ForegroundColor Yellow
    Write-Host "Nota: Si falla, instala Visual Studio Build Tools desde:" -ForegroundColor Yellow
    Write-Host "https://visualstudio.microsoft.com/downloads/#build-tools-for-visual-studio-2022" -ForegroundColor Cyan
    
    & ".\venv\Scripts\pip.exe" install --upgrade pip
    & ".\venv\Scripts\pip.exe" install -r requirements.txt
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host "`nERROR: Falló la instalación de dependencias." -ForegroundColor Red
        Write-Host "Intenta instalar manualmente:" -ForegroundColor Yellow
        Write-Host "  cd backend" -ForegroundColor Cyan
        Write-Host "  .\venv\Scripts\Activate.ps1" -ForegroundColor Cyan
        Write-Host "  pip install flask flask-cors pandas numpy scikit-learn requests" -ForegroundColor Cyan
        pause
        exit 1
    }
}

# Verificar si existen los datos del modelo
if (-not (Test-Path "..\data")) {
    Write-Host "`nADVERTENCIA: No se encontró la carpeta 'data' con el modelo entrenado." -ForegroundColor Red
    Write-Host "Por favor, ejecuta el notebook 'pruebas.ipynb' y exporta el modelo primero." -ForegroundColor Red
    Write-Host "Lee el archivo README.md para más información.`n" -ForegroundColor Yellow
    pause
}

# Iniciar el servidor
Write-Host "`nIniciando servidor en http://localhost:5000" -ForegroundColor Green
python app.py
