# Script para iniciar el frontend React
# Ejecuta este script desde el directorio raíz del proyecto

Write-Host "Iniciando aplicación React..." -ForegroundColor Green

# Navegar al directorio frontend
Set-Location -Path "frontend"

# Verificar si existen los node_modules
if (-not (Test-Path "node_modules")) {
    Write-Host "Instalando dependencias de Node.js..." -ForegroundColor Yellow
    npm install
}

# Iniciar la aplicación
Write-Host "`nIniciando aplicación en http://localhost:3000" -ForegroundColor Green
Write-Host "Asegúrate de que el backend esté ejecutándose en http://localhost:5000`n" -ForegroundColor Yellow

npm start
