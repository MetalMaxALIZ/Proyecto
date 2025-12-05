# Arquitectura del Proyecto - What Should I Play?

## 📊 Diagrama de Flujo

```
┌─────────────────────────────────────────────────────────────────┐
│                         USUARIO                                  │
└─────────────────────┬───────────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────────┐
│                    FRONTEND (React)                              │
│  - App.js (Componente principal)                                 │
│  - GameList.js (Lista de juegos)                                 │
│  - Recommendations.js (Recomendaciones)                          │
│                                                                   │
│  Puerto: 3000                                                    │
└─────────────────────┬───────────────────────────────────────────┘
                      │
                      │ HTTP Requests (Axios)
                      │
                      ▼
┌─────────────────────────────────────────────────────────────────┐
│                    BACKEND (Flask)                               │
│                                                                   │
│  Endpoints:                                                      │
│  - POST /api/obtener-juegos                                      │
│  - POST /api/recomendar                                          │
│  - GET  /api/health                                              │
│                                                                   │
│  Puerto: 5000                                                    │
└─────────┬───────────────────────────────┬───────────────────────┘
          │                               │
          │                               │
          ▼                               ▼
┌──────────────────────┐      ┌──────────────────────────┐
│   Steam Web API      │      │   Modelo KNN             │
│                      │      │                          │
│  - GetOwnedGames     │      │  - df_modelo             │
│  - ResolveVanityURL  │      │  - knn_modelo            │
│                      │      │  - df_combinado_final    │
└──────────────────────┘      │  - juegos_dict           │
                              │                          │
                              │  (Pickle files en /data) │
                              └──────────────────────────┘
```

## 🗂️ Estructura de Archivos

```
Proyecto_con_FrontEnd/
│
├── 📁 backend/
│   ├── app.py                    # Servidor Flask principal
│   ├── export_model.py           # Script de exportación del modelo
│   └── requirements.txt          # Dependencias Python
│
├── 📁 frontend/
│   ├── 📁 public/
│   │   └── index.html            # HTML base
│   │
│   ├── 📁 src/
│   │   ├── 📁 components/
│   │   │   ├── GameList.js       # Componente lista de juegos
│   │   │   ├── GameList.css      # Estilos lista de juegos
│   │   │   ├── Recommendations.js # Componente recomendaciones
│   │   │   └── Recommendations.css # Estilos recomendaciones
│   │   │
│   │   ├── App.js                # Componente principal
│   │   ├── App.css               # Estilos principales
│   │   ├── index.js              # Punto de entrada React
│   │   └── index.css             # Estilos globales
│   │
│   └── package.json              # Dependencias Node.js
│
├── 📁 data/                      # Generado al exportar el modelo
│   ├── df_combinado_final.pkl
│   ├── df_modelo.pkl
│   ├── df_modelo_normalizado.pkl
│   ├── knn_modelo.pkl
│   └── juegos_dict.pkl
│
├── 📄 steam_profile_games.py     # Funciones para Steam API
├── 📄 pruebas.ipynb              # Notebook de entrenamiento
│
├── 📄 README.md                  # Documentación completa
├── 📄 QUICKSTART.md              # Guía rápida de inicio
├── 📄 start_backend.ps1          # Script para iniciar backend
├── 📄 start_frontend.ps1         # Script para iniciar frontend
└── 📄 verificar.ps1              # Script de verificación
```

## 🔄 Flujo de Datos

### 1. Obtener Juegos de Steam

```
Usuario ingresa URL → Frontend envía POST /api/obtener-juegos
                    ↓
            Backend llama Steam API
                    ↓
            Procesa datos con Pandas
                    ↓
            Retorna lista de juegos ordenados
                    ↓
            Frontend muestra juegos con imágenes
```

### 2. Generar Recomendaciones

```
Usuario selecciona juegos → Frontend guarda en estado local
                          ↓
            Usuario presiona "WSIP"
                          ↓
            Frontend envía POST /api/recomendar
                          ↓
            Backend carga modelo KNN
                          ↓
            Calcula centroide de juegos seleccionados
                          ↓
            Encuentra vecinos más cercanos
                          ↓
            Retorna top 10 recomendaciones
                          ↓
            Frontend muestra recomendaciones detalladas
```

## 🎨 Componentes de la UI

### App.js (Contenedor Principal)
- Maneja el estado global de la aplicación
- Controla el flujo de datos entre componentes
- Gestiona llamadas a la API

### GameList.js (Lista de Juegos)
- Muestra grid de tarjetas de juegos
- Permite selección múltiple con checkmarks
- Muestra tiempo de juego y imagen
- Animaciones de hover y selección

### Recommendations.js (Recomendaciones)
- Muestra tarjetas horizontales de recomendaciones
- Incluye información detallada (géneros, valoración, similitud)
- Barra de progreso de similitud
- Enlaces a Steam Store

## 🔧 Tecnologías Utilizadas

### Backend
- **Flask 3.0.0**: Framework web ligero
- **Flask-CORS 4.0.0**: Manejo de CORS
- **Pandas 2.1.4**: Manipulación de datos
- **NumPy 1.26.2**: Operaciones numéricas
- **Scikit-learn 1.3.2**: Modelo KNN
- **Requests 2.31.0**: Llamadas HTTP a Steam API

### Frontend
- **React 18.2.0**: Librería UI
- **Axios 1.6.2**: Cliente HTTP
- **CSS3**: Estilos personalizados con gradientes y animaciones

## 🔐 Seguridad

- API Key de Steam visible en el código (solo para desarrollo local)
- CORS habilitado para desarrollo local
- Para producción: usar variables de entorno y HTTPS

## 📈 Rendimiento

- Modelo pre-entrenado cargado en memoria
- Respuestas rápidas para recomendaciones
- Carga lazy de imágenes
- Caché de datos en el frontend

## 🚀 Posibles Mejoras Futuras

- [ ] Autenticación con Steam OAuth
- [ ] Caché de resultados
- [ ] Filtros avanzados (por género, año, etc.)
- [ ] Guardar lista de juegos favoritos
- [ ] Compartir recomendaciones
- [ ] Modo oscuro
- [ ] Soporte multi-idioma
- [ ] PWA (Progressive Web App)
- [ ] Análisis de tendencias de juego
- [ ] Integración con otras plataformas (Epic, GOG, etc.)
