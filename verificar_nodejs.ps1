# Verificar instalacion de Node.js

Write-Host "=== Verificacion de Node.js ===" -ForegroundColor Cyan
Write-Host ""

# Verificar Node.js
Write-Host "Verificando Node.js..." -ForegroundColor Yellow
try {
    $nodeVersion = node --version 2>&1
    Write-Host "  ✓ Node.js instalado: $nodeVersion" -ForegroundColor Green
} catch {
    Write-Host "  ✗ Node.js NO encontrado" -ForegroundColor Red
    Write-Host ""
    Write-Host "SOLUCION:" -ForegroundColor Yellow
    Write-Host "1. Descarga Node.js desde: https://nodejs.org/" -ForegroundColor Cyan
    Write-Host "2. Instala la version LTS (recomendada)" -ForegroundColor Cyan
    Write-Host "3. Reinicia PowerShell/CMD" -ForegroundColor Cyan
    Write-Host "4. Ejecuta nuevamente start_frontend.bat" -ForegroundColor Cyan
    Write-Host ""
    pause
    exit 1
}

# Verificar npm
Write-Host "Verificando npm..." -ForegroundColor Yellow
try {
    $npmVersion = npm --version 2>&1
    Write-Host "  ✓ npm instalado: $npmVersion" -ForegroundColor Green
} catch {
    Write-Host "  ✗ npm NO encontrado" -ForegroundColor Red
}

Write-Host ""
Write-Host "Todo listo para ejecutar el frontend!" -ForegroundColor Green
Write-Host "Ejecuta: .\start_frontend.bat" -ForegroundColor Cyan
