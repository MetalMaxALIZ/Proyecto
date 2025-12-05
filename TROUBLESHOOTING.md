# 🔧 Guía de Solución de Problemas - Backend

## Problema: "no se encontró Python"

### Solución 1: Usar el archivo .bat en lugar del .ps1
```cmd
.\start_backend.bat
```

### Solución 2: Instalar Python correctamente
1. Descarga Python desde [python.org](https://www.python.org/downloads/)
2. **IMPORTANTE**: Durante la instalación, marca "Add Python to PATH"
3. Reinicia PowerShell/CMD
4. Verifica: `py --version`

### Solución 3: Instalación manual
```powershell
cd backend

# Crear entorno virtual
py -m venv venv

# Activar entorno virtual
.\venv\Scripts\Activate.ps1

# Actualizar pip
python -m pip install --upgrade pip

# Instalar dependencias una por una
pip install flask
pip install flask-cors
pip install requests
pip install pandas
pip install numpy
pip install scikit-learn

# Iniciar servidor
python app.py
```

---

## Problema: Error al compilar NumPy/Pandas

### Causa
Python 3.13 es muy nuevo y algunas librerías requieren compilación.

### Solución 1: Instalar versiones precompiladas
```powershell
cd backend
.\venv\Scripts\Activate.ps1

# Instalar desde wheels precompilados
pip install --only-binary :all: numpy pandas scikit-learn
```

### Solución 2: Usar Python 3.11 o 3.12
1. Desinstala Python 3.13
2. Instala Python 3.11 desde [python.org](https://www.python.org/downloads/)
3. Ejecuta el script nuevamente

### Solución 3: Instalar Visual Studio Build Tools (para compilar)
1. Descarga [Build Tools para Visual Studio 2022](https://visualstudio.microsoft.com/downloads/#build-tools-for-visual-studio-2022)
2. Durante la instalación, selecciona "Desarrollo para escritorio con C++"
3. Reinicia e intenta nuevamente

---

## Problema: "Cannot activate venv"

### Solución: Cambiar política de ejecución de PowerShell
```powershell
# Como Administrador, ejecuta:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Luego intenta nuevamente
.\start_backend.ps1
```

O usa el archivo .bat:
```cmd
.\start_backend.bat
```

---

## Problema: "No se encontró la carpeta data"

### Solución
1. Abre el notebook `pruebas.ipynb`
2. Ejecuta TODAS las celdas
3. Al final, ejecuta la celda "Exportar Modelo para el Frontend"
4. Verifica que se creó la carpeta `data` con archivos `.pkl`

---

## Problema: Puerto 5000 ya está en uso

### Solución 1: Cambiar puerto en app.py
```python
# Al final de backend/app.py, cambia:
app.run(debug=True, port=5001)  # Usa 5001 en lugar de 5000
```

También actualiza frontend/package.json:
```json
"proxy": "http://localhost:5001"
```

### Solución 2: Detener el proceso que usa el puerto
```powershell
# Encuentra el proceso
netstat -ano | findstr :5000

# Detén el proceso (reemplaza PID con el número mostrado)
taskkill /PID <PID> /F
```

---

## Problema: Módulos no encontrados

### Solución
```powershell
cd backend

# Asegúrate de estar en el entorno virtual
.\venv\Scripts\Activate.ps1

# Reinstala todas las dependencias
pip install --force-reinstall -r requirements.txt
```

---

## Opción Simple: Usar Conda/Miniconda

Si tienes muchos problemas, usa Conda:

```bash
# Instalar Miniconda desde: https://docs.conda.io/en/latest/miniconda.html

# Crear entorno
conda create -n wsip python=3.11

# Activar
conda activate wsip

# Instalar dependencias
conda install flask pandas numpy scikit-learn requests
pip install flask-cors

# Navegar a backend
cd backend

# Iniciar servidor
python app.py
```

---

## Verificación Rápida

Antes de iniciar el backend, verifica:

```powershell
# 1. Python instalado
py --version
# Debe mostrar Python 3.10, 3.11 o 3.12 (3.13 puede dar problemas)

# 2. Pip funcional
py -m pip --version

# 3. Carpeta data existe
Test-Path data
# Debe mostrar "True"
```

---

## Script de Diagnóstico

Crea un archivo `diagnostico.ps1`:

```powershell
Write-Host "=== Diagnóstico del Sistema ===" -ForegroundColor Cyan

# Python
Write-Host "`nPython:" -ForegroundColor Yellow
try {
    $pyVersion = py --version 2>&1
    Write-Host "  ✓ $pyVersion" -ForegroundColor Green
} catch {
    Write-Host "  ✗ Python no encontrado" -ForegroundColor Red
}

# Backend
Write-Host "`nBackend:" -ForegroundColor Yellow
if (Test-Path "backend/app.py") {
    Write-Host "  ✓ app.py existe" -ForegroundColor Green
} else {
    Write-Host "  ✗ app.py no encontrado" -ForegroundColor Red
}

# Modelo
Write-Host "`nModelo:" -ForegroundColor Yellow
if (Test-Path "data") {
    Write-Host "  ✓ Carpeta data existe" -ForegroundColor Green
    $files = @("df_combinado_final.pkl", "df_modelo.pkl", "knn_modelo.pkl", "df_modelo_normalizado.pkl", "juegos_dict.pkl")
    foreach ($file in $files) {
        if (Test-Path "data/$file") {
            Write-Host "    ✓ $file" -ForegroundColor Green
        } else {
            Write-Host "    ✗ $file falta" -ForegroundColor Red
        }
    }
} else {
    Write-Host "  ✗ Carpeta data no existe - Exporta el modelo desde el notebook" -ForegroundColor Red
}

# Entorno virtual
Write-Host "`nEntorno Virtual:" -ForegroundColor Yellow
if (Test-Path "backend/venv") {
    Write-Host "  ✓ Entorno virtual existe" -ForegroundColor Green
} else {
    Write-Host "  ⚠ Entorno virtual no existe (se creará al iniciar)" -ForegroundColor Yellow
}
```

Ejecuta: `.\diagnostico.ps1`

---

## ¿Aún tienes problemas?

**Opción más simple**: Ejecuta directamente sin entorno virtual

```powershell
cd backend

# Instala globalmente (no recomendado pero funciona)
py -m pip install flask flask-cors pandas numpy scikit-learn requests

# Ejecuta
py app.py
```

---

## Contacto

Si nada funciona, proporciona:
1. Versión de Python: `py --version`
2. Sistema operativo: `systeminfo | findstr /B /C:"OS"`
3. El error completo que aparece
