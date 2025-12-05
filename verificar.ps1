# Script para verificar que todo está configurado correctamente

Write-Host "`n=== Verificación del Proyecto WSIP ===" -ForegroundColor Cyan
Write-Host ""

$errores = 0

# Verificar Python
Write-Host "Verificando Python..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "  ✓ Python instalado: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "  ✗ Python no encontrado. Por favor, instala Python 3.8 o superior." -ForegroundColor Red
    $errores++
}

# Verificar Node.js
Write-Host "`nVerificando Node.js..." -ForegroundColor Yellow
try {
    $nodeVersion = node --version 2>&1
    Write-Host "  ✓ Node.js instalado: $nodeVersion" -ForegroundColor Green
} catch {
    Write-Host "  ✗ Node.js no encontrado. Por favor, instala Node.js 14 o superior." -ForegroundColor Red
    $errores++
}

# Verificar npm
Write-Host "`nVerificando npm..." -ForegroundColor Yellow
try {
    $npmVersion = npm --version 2>&1
    Write-Host "  ✓ npm instalado: $npmVersion" -ForegroundColor Green
} catch {
    Write-Host "  ✗ npm no encontrado." -ForegroundColor Red
    $errores++
}

# Verificar estructura de carpetas
Write-Host "`nVerificando estructura de carpetas..." -ForegroundColor Yellow

$carpetasRequeridas = @(
    "backend",
    "frontend",
    "frontend\src",
    "frontend\public"
)

foreach ($carpeta in $carpetasRequeridas) {
    if (Test-Path $carpeta) {
        Write-Host "  ✓ Carpeta '$carpeta' encontrada" -ForegroundColor Green
    } else {
        Write-Host "  ✗ Carpeta '$carpeta' NO encontrada" -ForegroundColor Red
        $errores++
    }
}

# Verificar archivos críticos
Write-Host "`nVerificando archivos críticos..." -ForegroundColor Yellow

$archivosRequeridos = @(
    "backend\app.py",
    "backend\requirements.txt",
    "frontend\package.json",
    "frontend\src\App.js",
    "steam_profile_games.py"
)

foreach ($archivo in $archivosRequeridos) {
    if (Test-Path $archivo) {
        Write-Host "  ✓ Archivo '$archivo' encontrado" -ForegroundColor Green
    } else {
        Write-Host "  ✗ Archivo '$archivo' NO encontrado" -ForegroundColor Red
        $errores++
    }
}

# Verificar modelo exportado
Write-Host "`nVerificando modelo exportado..." -ForegroundColor Yellow
if (Test-Path "data") {
    $archivosModelo = @(
        "data\df_combinado_final.pkl",
        "data\df_modelo.pkl",
        "data\knn_modelo.pkl",
        "data\df_modelo_normalizado.pkl",
        "data\juegos_dict.pkl"
    )
    
    $modeloCompleto = $true
    foreach ($archivo in $archivosModelo) {
        if (Test-Path $archivo) {
            Write-Host "  ✓ $archivo" -ForegroundColor Green
        } else {
            Write-Host "  ✗ $archivo NO encontrado" -ForegroundColor Yellow
            $modeloCompleto = $false
        }
    }
    
    if (-not $modeloCompleto) {
        Write-Host "`n  ⚠ El modelo no está completamente exportado." -ForegroundColor Yellow
        Write-Host "  Ejecuta la celda de exportación en pruebas.ipynb" -ForegroundColor Yellow
    }
} else {
    Write-Host "  ⚠ Carpeta 'data' no encontrada" -ForegroundColor Yellow
    Write-Host "  El modelo aún no ha sido exportado." -ForegroundColor Yellow
    Write-Host "  Ejecuta la celda de exportación en pruebas.ipynb" -ForegroundColor Yellow
}

# Verificar dependencias del backend
Write-Host "`nVerificando dependencias del backend..." -ForegroundColor Yellow
if (Test-Path "backend\venv") {
    Write-Host "  ✓ Entorno virtual encontrado" -ForegroundColor Green
} else {
    Write-Host "  ⚠ Entorno virtual no encontrado (se creará al iniciar el backend)" -ForegroundColor Yellow
}

# Verificar dependencias del frontend
Write-Host "`nVerificando dependencias del frontend..." -ForegroundColor Yellow
if (Test-Path "frontend\node_modules") {
    Write-Host "  ✓ node_modules encontrado" -ForegroundColor Green
} else {
    Write-Host "  ⚠ node_modules no encontrado (se instalará al iniciar el frontend)" -ForegroundColor Yellow
}

# Resumen
Write-Host "`n=== Resumen ===" -ForegroundColor Cyan
if ($errores -eq 0) {
    Write-Host "✓ Todo parece estar en orden!" -ForegroundColor Green
    Write-Host "`nPróximos pasos:" -ForegroundColor Yellow
    Write-Host "1. Si no has exportado el modelo, ejecuta la celda final de pruebas.ipynb"
    Write-Host "2. Ejecuta .\start_backend.ps1 en una terminal"
    Write-Host "3. Ejecuta .\start_frontend.ps1 en otra terminal"
    Write-Host "4. Abre http://localhost:3000 en tu navegador"
} else {
    Write-Host "✗ Se encontraron $errores errores" -ForegroundColor Red
    Write-Host "Por favor, revisa los mensajes anteriores y corrige los problemas." -ForegroundColor Red
}

Write-Host ""
