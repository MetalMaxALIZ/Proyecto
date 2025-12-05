# 🚀 Inicio Rápido - What Should I Play?

## Pasos para ejecutar la aplicación

### 1️⃣ Exportar el Modelo (Solo la primera vez)

1. Abre el notebook `pruebas.ipynb` en VS Code
2. Ejecuta todas las celdas secuencialmente
3. Al final del notebook, ejecuta la celda titulada "**Exportar Modelo para el Frontend**"
4. Verás un mensaje de confirmación indicando que los datos se guardaron en la carpeta `data/`

### 2️⃣ Iniciar el Backend

Opción A - Usando el script automático:
```powershell
.\start_backend.ps1
```

Opción B - Manual:
```powershell
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py
```

El backend estará corriendo en: **http://localhost:5000**

### 3️⃣ Iniciar el Frontend

**Abre una nueva terminal** y ejecuta:

Opción A - Usando el script automático:
```powershell
.\start_frontend.ps1
```

Opción B - Manual:
```powershell
cd frontend
npm install
npm start
```

El frontend se abrirá automáticamente en: **http://localhost:3000**

## ✅ ¡Listo para usar!

1. Introduce tu URL de perfil de Steam (debe ser público)
2. Haz clic en "Obtener Juegos"
3. Selecciona los juegos que te gustan
4. Haz clic en "WSIP" para obtener recomendaciones

## ⚠️ Solución de Problemas

### "No se encontró la carpeta data"
- Ejecuta la celda de exportación en el notebook `pruebas.ipynb`

### "Error al conectar con el servidor"
- Asegúrate de que el backend esté ejecutándose en el puerto 5000
- Verifica que no haya firewall bloqueando la conexión

### "No se pudieron obtener los juegos"
- Verifica que tu perfil de Steam sea público
- Comprueba que la URL del perfil sea correcta

## 📝 Notas

- La primera vez tardará más porque necesita instalar las dependencias
- Necesitas tener Python 3.8+ y Node.js 14+ instalados
- El perfil de Steam DEBE ser público para obtener los juegos

## 🎮 ¡Disfruta descubriendo nuevos juegos!
