# 🎮 What Should I Play? - Frontend React + Backend Flask

## 📋 Resumen del Proyecto

Sistema completo de recomendación de juegos de Steam con interfaz web moderna desarrollada en React y backend en Flask.

### ✨ Características Principales

- **Integración con Steam API**: Obtiene automáticamente la biblioteca de juegos de cualquier perfil público
- **Sistema de Recomendación Inteligente**: Basado en algoritmo KNN (K-Nearest Neighbors)
- **Interfaz Moderna**: Diseño responsive con gradientes y animaciones
- **Selección Visual**: Selecciona juegos mediante tarjetas interactivas
- **Recomendaciones Detalladas**: Información completa con géneros, valoraciones y similitud

---

## 🚀 Inicio Rápido

### Opción 1: Scripts Automáticos (Recomendado)

```powershell
# Terminal 1 - Backend
.\start_backend.ps1

# Terminal 2 - Frontend
.\start_frontend.ps1
```

### Opción 2: Manual

**Backend:**
```powershell
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py
```

**Frontend:**
```powershell
cd frontend
npm install
npm start
```

---

## 📁 Archivos Creados

### Backend
- ✅ `backend/app.py` - Servidor Flask con API REST
- ✅ `backend/requirements.txt` - Dependencias Python
- ✅ `backend/export_model.py` - Script de exportación del modelo

### Frontend
- ✅ `frontend/package.json` - Configuración del proyecto React
- ✅ `frontend/public/index.html` - HTML base
- ✅ `frontend/src/index.js` - Punto de entrada
- ✅ `frontend/src/index.css` - Estilos globales
- ✅ `frontend/src/App.js` - Componente principal
- ✅ `frontend/src/App.css` - Estilos principales
- ✅ `frontend/src/components/GameList.js` - Lista de juegos
- ✅ `frontend/src/components/GameList.css` - Estilos de lista
- ✅ `frontend/src/components/Recommendations.js` - Recomendaciones
- ✅ `frontend/src/components/Recommendations.css` - Estilos de recomendaciones

### Documentación
- ✅ `README.md` - Documentación completa
- ✅ `QUICKSTART.md` - Guía rápida de inicio
- ✅ `ARQUITECTURA.md` - Arquitectura del sistema
- ✅ `API_REFERENCE.md` - Referencia de la API
- ✅ `PROYECTO_COMPLETO.md` - Este archivo

### Scripts de Utilidad
- ✅ `start_backend.ps1` - Inicia el backend automáticamente
- ✅ `start_frontend.ps1` - Inicia el frontend automáticamente
- ✅ `verificar.ps1` - Verifica la instalación

### Modificaciones
- ✅ `steam_profile_games.py` - Añadido soporte para img_icon_url
- ✅ `pruebas.ipynb` - Añadidas celdas para exportar el modelo

---

## 🎯 Flujo de Uso

1. **Exportar el Modelo** (Solo una vez)
   - Abre `pruebas.ipynb`
   - Ejecuta todas las celdas
   - Ejecuta la celda "Exportar Modelo para el Frontend"

2. **Iniciar el Backend**
   - `.\start_backend.ps1`
   - Espera a que diga "Running on http://127.0.0.1:5000"

3. **Iniciar el Frontend**
   - `.\start_frontend.ps1`
   - Se abrirá automáticamente en el navegador

4. **Usar la Aplicación**
   - Introduce tu URL de perfil de Steam
   - Haz clic en "Obtener Juegos"
   - Selecciona los juegos que te gustan
   - Haz clic en "WSIP" para recomendaciones

---

## 🎨 Interfaz de Usuario

### Pantalla Principal
```
┌─────────────────────────────────────────────────────┐
│                                                     │
│          What should i play?                        │
│                                                     │
│  ┌────────────────────────────┐  ┌──────────────┐  │
│  │ URL de perfil de Steam     │  │ Obtener      │  │
│  └────────────────────────────┘  │ Juegos       │  │
│                                  └──────────────┘  │
│                                                     │
│  Tus Juegos (150)                                  │
│  Selecciona los juegos en los que quieres...       │
│                                                     │
│  ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐             │
│  │ ✓    │ │      │ │ ✓    │ │      │             │
│  │[IMG] │ │[IMG] │ │[IMG] │ │[IMG] │             │
│  │Juego1│ │Juego2│ │Juego3│ │Juego4│             │
│  │100h  │ │50h   │ │200h  │ │30h   │             │
│  └──────┘ └──────┘ └──────┘ └──────┘             │
│                                                     │
│            ┌──────────────────┐                    │
│            │   WSIP (3)       │                    │
│            └──────────────────┘                    │
│                                                     │
│  🎮 Recomendaciones para ti                         │
│                                                     │
│  #1 ┌────────────────────────────────────────┐    │
│     │ [Imagen Header]    Nombre del Juego    │    │
│     │                    Géneros: Action     │    │
│     │                    Valoración: 95%     │    │
│     │                    Similitud: ████ 89% │    │
│     │                    [Ver en Steam →]    │    │
│     └────────────────────────────────────────┘    │
│                                                     │
└─────────────────────────────────────────────────────┘
```

---

## 🛠️ Stack Tecnológico

### Backend
| Tecnología | Versión | Uso |
|------------|---------|-----|
| Python | 3.8+ | Lenguaje base |
| Flask | 3.0.0 | Framework web |
| Flask-CORS | 4.0.0 | Manejo de CORS |
| Pandas | 2.1.4 | Procesamiento de datos |
| NumPy | 1.26.2 | Operaciones numéricas |
| Scikit-learn | 1.3.2 | Modelo KNN |
| Requests | 2.31.0 | Llamadas a Steam API |

### Frontend
| Tecnología | Versión | Uso |
|------------|---------|-----|
| React | 18.2.0 | Librería UI |
| Axios | 1.6.2 | Cliente HTTP |
| CSS3 | - | Estilos y animaciones |

---

## 📊 API Endpoints

### Backend (Puerto 5000)

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/api/health` | Estado del servidor |
| POST | `/api/obtener-juegos` | Obtiene juegos de Steam |
| POST | `/api/recomendar` | Genera recomendaciones |

### Ejemplo de Petición

```javascript
// Obtener juegos
const response = await axios.post('/api/obtener-juegos', {
  perfil_url: 'https://steamcommunity.com/id/username/'
});

// Obtener recomendaciones
const recs = await axios.post('/api/recomendar', {
  nombres_juegos: ['Counter-Strike', 'Dota 2'],
  n_recomendaciones: 10
});
```

---

## 📝 Checklist de Configuración

### Antes de Empezar
- [ ] Python 3.8+ instalado
- [ ] Node.js 14+ instalado
- [ ] npm instalado
- [ ] Ejecutado notebook `pruebas.ipynb` completo
- [ ] Exportado modelo (carpeta `data/` creada)

### Verificación
```powershell
.\verificar.ps1
```

### Primera Ejecución
- [ ] Backend instalado y corriendo en puerto 5000
- [ ] Frontend instalado y corriendo en puerto 3000
- [ ] Navegador abierto en `http://localhost:3000`
- [ ] Perfil de Steam configurado como público

---

## 🐛 Solución de Problemas

### "No se encontró la carpeta data"
**Solución:** Ejecuta la celda de exportación en `pruebas.ipynb`

### "Error al conectar con el servidor"
**Solución:** 
- Verifica que el backend esté corriendo
- Comprueba que no haya otro servicio en el puerto 5000

### "No se pudieron obtener los juegos"
**Solución:**
- Verifica que el perfil de Steam sea público
- Comprueba que la URL sea correcta

### "El modelo no está cargado"
**Solución:**
- Ejecuta el notebook completo
- Exporta el modelo con la celda final
- Reinicia el backend

---

## 🎯 Casos de Uso

### Caso 1: Descubrir Nuevos Juegos
1. Conecta tu perfil de Steam
2. Selecciona tus 5-10 juegos favoritos
3. Obtén recomendaciones similares

### Caso 2: Expandir un Género
1. Selecciona solo juegos de un género específico
2. Obtén recomendaciones del mismo género

### Caso 3: Juegos Multiplataforma
1. Selecciona juegos que juegues en diferentes plataformas
2. Descubre juegos que combinen esas características

---

## 🔒 Seguridad

### Desarrollo Local
- API Key de Steam visible en el código
- CORS habilitado para localhost
- Sin autenticación

### Recomendaciones para Producción
- [ ] Mover API Key a variables de entorno
- [ ] Implementar rate limiting
- [ ] Configurar CORS específico
- [ ] Añadir HTTPS
- [ ] Implementar autenticación
- [ ] Añadir logging
- [ ] Implementar caché

---

## 📈 Mejoras Futuras

### Corto Plazo
- [ ] Caché de resultados de Steam API
- [ ] Mensaje de loading más descriptivo
- [ ] Filtros por género/año
- [ ] Modo oscuro

### Mediano Plazo
- [ ] Autenticación con Steam OAuth
- [ ] Guardar listas de favoritos
- [ ] Compartir recomendaciones
- [ ] Soporte multi-idioma

### Largo Plazo
- [ ] PWA (Progressive Web App)
- [ ] Integración con otras plataformas (Epic, GOG)
- [ ] Análisis de tendencias
- [ ] Recomendaciones basadas en amigos
- [ ] Sistema de valoraciones

---

## 📚 Documentación Adicional

- **README.md**: Documentación completa del proyecto
- **QUICKSTART.md**: Guía rápida de 5 minutos
- **ARQUITECTURA.md**: Diagrama y estructura del sistema
- **API_REFERENCE.md**: Documentación completa de la API

---

## 🤝 Contribuir

Este proyecto es educativo. Para mejoras:
1. Fork el proyecto
2. Crea una rama para tu feature
3. Commit tus cambios
4. Push a la rama
5. Abre un Pull Request

---

## 📄 Licencia

Este proyecto es de uso educativo.

---

## 👨‍💻 Autor

Proyecto desarrollado como parte del curso de Data Science.

---

## 🙏 Agradecimientos

- Steam Web API por proporcionar acceso a los datos
- Scikit-learn por el algoritmo KNN
- React y Flask por facilitar el desarrollo

---

## 📞 Soporte

Si encuentras problemas:
1. Revisa la sección de Troubleshooting en README.md
2. Verifica la instalación con `verificar.ps1`
3. Consulta los logs del backend y frontend
4. Revisa la documentación de la API

---

**¡Disfruta descubriendo nuevos juegos! 🎮**
