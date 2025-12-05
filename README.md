# What Should I Play? 🎮

Sistema de recomendación de juegos de Steam con frontend React y backend Flask.

## Estructura del Proyecto

```
Proyecto_con_FrontEnd/
├── backend/                 # Servidor Flask
│   ├── app.py              # API principal
│   ├── export_model.py     # Script para exportar el modelo
│   └── requirements.txt    # Dependencias Python
├── frontend/               # Aplicación React
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   │   ├── GameList.js
│   │   │   ├── GameList.css
│   │   │   ├── Recommendations.js
│   │   │   └── Recommendations.css
│   │   ├── App.js
│   │   ├── App.css
│   │   ├── index.js
│   │   └── index.css
│   └── package.json
├── data/                   # Datos del modelo (se genera automáticamente)
└── steam_profile_games.py  # Funciones para obtener juegos de Steam
```

## Configuración Inicial

### 1. Preparar el Modelo de Recomendación

Antes de ejecutar la aplicación, necesitas exportar el modelo desde el notebook:

1. Abre el notebook `pruebas.ipynb`
2. Ejecuta todas las celdas hasta que tengas las siguientes variables:
   - `df_combinado_final`
   - `df_modelo`
   - `df_modelo_normalizado`
   - `knn_modelo`
   - `juegos_dict`

3. Al final del notebook, ejecuta:

```python
# Importar la función de exportación
import sys
sys.path.append('./backend')
from export_model import guardar_modelo

# Guardar el modelo
guardar_modelo(df_combinado_final, df_modelo, df_modelo_normalizado, knn_modelo, juegos_dict)
```

Esto creará la carpeta `data/` con todos los archivos necesarios.

### 2. Configurar el Backend (Flask)

1. Navega a la carpeta backend:
```powershell
cd backend
```

2. Crea un entorno virtual (opcional pero recomendado):
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

3. Instala las dependencias:
```powershell
pip install -r requirements.txt
```

4. Inicia el servidor Flask:
```powershell
python app.py
```

El servidor estará corriendo en `http://localhost:5000`

### 3. Configurar el Frontend (React)

1. Abre una nueva terminal y navega a la carpeta frontend:
```powershell
cd frontend
```

2. Instala las dependencias de Node.js:
```powershell
npm install
```

3. Inicia la aplicación React:
```powershell
npm start
```

La aplicación se abrirá automáticamente en `http://localhost:3000`

## Uso de la Aplicación

1. **Introduce tu URL de perfil de Steam** en el campo de texto:
   - Ejemplo: `https://steamcommunity.com/id/TuNombre/`
   - O: `https://steamcommunity.com/profiles/76561198XXXXXXXXX/`

2. **Haz clic en "Obtener Juegos"** para cargar tu biblioteca

3. **Selecciona los juegos** en los que quieres basarte para las recomendaciones (haz clic en las tarjetas)

4. **Haz clic en el botón "WSIP"** para obtener recomendaciones personalizadas

5. **Explora las recomendaciones** con información detallada de cada juego

## Características

- ✅ Obtención automática de juegos desde perfiles públicos de Steam
- ✅ Visualización de juegos con imágenes y tiempo de juego
- ✅ Selección múltiple de juegos con interfaz intuitiva
- ✅ Sistema de recomendación basado en KNN (K-Nearest Neighbors)
- ✅ Información detallada de recomendaciones (géneros, valoraciones, similitud)
- ✅ Enlaces directos a la tienda de Steam
- ✅ Diseño responsive y moderno

## Notas Importantes

- **Perfil Público**: Tu perfil de Steam debe ser público para que la aplicación pueda acceder a tu biblioteca
- **API Key**: La API key de Steam está incluida en el código, pero puedes usar la tuya propia en `backend/app.py`
- **Modelo Pre-entrenado**: El modelo debe estar entrenado y exportado antes de usar la aplicación

## Troubleshooting

### El backend no puede cargar el modelo
- Asegúrate de haber ejecutado el script `export_model.py` desde el notebook
- Verifica que la carpeta `data/` existe y contiene los archivos `.pkl`

### Error al obtener juegos de Steam
- Verifica que la URL del perfil sea correcta
- Asegúrate de que el perfil sea público
- Comprueba que el backend esté ejecutándose en el puerto 5000

### El frontend no se conecta al backend
- Verifica que el backend esté ejecutándose
- Comprueba la consola del navegador para ver errores específicos
- Asegúrate de que no haya otro servicio usando el puerto 5000

## Tecnologías Utilizadas

### Backend
- Flask - Framework web de Python
- Flask-CORS - Manejo de CORS
- Pandas - Procesamiento de datos
- NumPy - Operaciones numéricas
- Scikit-learn - Modelo de machine learning (KNN)

### Frontend
- React - Librería de UI
- Axios - Cliente HTTP
- CSS3 - Estilos personalizados

## Licencia

Este proyecto es de uso educativo.
