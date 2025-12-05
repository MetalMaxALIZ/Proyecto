# API Reference - What Should I Play?

Documentación de los endpoints de la API del backend.

## Base URL

```
http://localhost:5000/api
```

---

## Endpoints

### 1. Health Check

Verifica el estado del servidor y si el modelo está cargado.

**Endpoint:** `GET /api/health`

**Respuesta exitosa:**
```json
{
  "status": "ok",
  "modelo_cargado": true
}
```

**Ejemplo cURL:**
```bash
curl http://localhost:5000/api/health
```

**Ejemplo JavaScript:**
```javascript
const response = await axios.get('/api/health');
console.log(response.data);
```

---

### 2. Obtener Juegos de Steam

Obtiene la lista de juegos de un perfil público de Steam.

**Endpoint:** `POST /api/obtener-juegos`

**Request Body:**
```json
{
  "perfil_url": "https://steamcommunity.com/id/username/"
}
```

**Parámetros:**
- `perfil_url` (string, required): URL del perfil de Steam (puede ser /id/username o /profiles/steamid64)

**Respuesta exitosa:**
```json
{
  "success": true,
  "juegos": [
    {
      "app_id": 730,
      "nombre": "Counter-Strike: Global Offensive",
      "tiempo_juego_minutos": 12450,
      "tiempo_juego_horas": 207.5,
      "img_icon_url": "https://cdn.cloudflare.steamstatic.com/steam/apps/730/header.jpg"
    },
    {
      "app_id": 570,
      "nombre": "Dota 2",
      "tiempo_juego_minutos": 8900,
      "tiempo_juego_horas": 148.33,
      "img_icon_url": "https://cdn.cloudflare.steamstatic.com/steam/apps/570/header.jpg"
    }
  ],
  "total": 2
}
```

**Respuesta de error:**
```json
{
  "error": "No se pudieron obtener los juegos. El perfil puede ser privado."
}
```

**Códigos de estado:**
- `200`: Éxito
- `400`: Error en los parámetros
- `500`: Error del servidor

**Ejemplo cURL:**
```bash
curl -X POST http://localhost:5000/api/obtener-juegos \
  -H "Content-Type: application/json" \
  -d '{"perfil_url": "https://steamcommunity.com/id/username/"}'
```

**Ejemplo JavaScript:**
```javascript
const response = await axios.post('/api/obtener-juegos', {
  perfil_url: 'https://steamcommunity.com/id/username/'
});
console.log(response.data.juegos);
```

---

### 3. Obtener Recomendaciones

Genera recomendaciones basadas en una lista de juegos seleccionados.

**Endpoint:** `POST /api/recomendar`

**Request Body:**
```json
{
  "nombres_juegos": ["Counter-Strike", "Dota 2", "Team Fortress 2"],
  "n_recomendaciones": 10
}
```

**Parámetros:**
- `nombres_juegos` (array, required): Lista de nombres de juegos para basar las recomendaciones
- `n_recomendaciones` (integer, optional): Número de recomendaciones a retornar (default: 10)

**Respuesta exitosa:**
```json
{
  "success": true,
  "recomendaciones": [
    {
      "appid": "440",
      "name": "Team Fortress 2",
      "genres": "Action, Free to Play",
      "owners": 50000000,
      "porcentaje_votos_positivos": 92.5,
      "similitud": 0.95,
      "imagen_url": "https://cdn.cloudflare.steamstatic.com/steam/apps/440/header.jpg"
    },
    {
      "appid": "4000",
      "name": "Garry's Mod",
      "genres": "Indie, Simulation",
      "owners": 20000000,
      "porcentaje_votos_positivos": 95.2,
      "similitud": 0.89,
      "imagen_url": "https://cdn.cloudflare.steamstatic.com/steam/apps/4000/header.jpg"
    }
  ],
  "total": 2
}
```

**Respuesta de error:**
```json
{
  "error": "No se pudieron generar recomendaciones",
  "success": false
}
```

**Códigos de estado:**
- `200`: Éxito
- `400`: Error en los parámetros o no se encontraron juegos válidos
- `500`: Error del servidor o modelo no cargado

**Ejemplo cURL:**
```bash
curl -X POST http://localhost:5000/api/recomendar \
  -H "Content-Type: application/json" \
  -d '{
    "nombres_juegos": ["Counter-Strike", "Dota 2"],
    "n_recomendaciones": 5
  }'
```

**Ejemplo JavaScript:**
```javascript
const response = await axios.post('/api/recomendar', {
  nombres_juegos: ['Counter-Strike', 'Dota 2', 'Team Fortress 2'],
  n_recomendaciones: 10
});

response.data.recomendaciones.forEach(juego => {
  console.log(`${juego.name} - Similitud: ${(juego.similitud * 100).toFixed(1)}%`);
});
```

---

## Códigos de Error Comunes

### 400 Bad Request
- Falta el parámetro `perfil_url`
- Falta el parámetro `nombres_juegos`
- Lista de juegos vacía
- URL de perfil inválida
- Perfil privado

### 500 Internal Server Error
- Modelo no cargado (ejecuta primero la exportación del notebook)
- Error al conectar con Steam API
- Error en el procesamiento de datos

---

## Estructura de Datos

### Game Object
```typescript
{
  app_id: number,              // ID del juego en Steam
  nombre: string,              // Nombre del juego
  tiempo_juego_minutos: number,// Tiempo jugado en minutos
  tiempo_juego_horas: number,  // Tiempo jugado en horas
  img_icon_url: string        // URL de la imagen del juego
}
```

### Recommendation Object
```typescript
{
  appid: string,                      // ID del juego (string)
  name: string,                       // Nombre del juego
  genres: string,                     // Géneros separados por coma
  owners: number,                     // Número de propietarios
  porcentaje_votos_positivos: number, // Porcentaje de votos positivos
  similitud: number,                  // Similitud (0-1)
  imagen_url: string                  // URL de la imagen header
}
```

---

## Notas de Implementación

### CORS
El servidor está configurado con CORS habilitado para permitir peticiones desde el frontend React en desarrollo.

### Rate Limiting
Actualmente no hay rate limiting implementado. Para producción, considera implementar límites de peticiones.

### Caché
No hay sistema de caché implementado. Las peticiones a Steam API y al modelo se procesan en tiempo real.

### Timeout
- Peticiones a Steam API: 30 segundos
- Procesamiento del modelo: Sin límite (generalmente < 1 segundo)

---

## Ejemplos de Integración

### React Component Example
```javascript
import React, { useState } from 'react';
import axios from 'axios';

function SteamGames() {
  const [juegos, setJuegos] = useState([]);
  
  const obtenerJuegos = async (perfilUrl) => {
    try {
      const response = await axios.post('/api/obtener-juegos', {
        perfil_url: perfilUrl
      });
      setJuegos(response.data.juegos);
    } catch (error) {
      console.error('Error:', error.response?.data?.error);
    }
  };
  
  return (
    // JSX aquí
  );
}
```

### Python Example
```python
import requests

# Obtener juegos
response = requests.post('http://localhost:5000/api/obtener-juegos', json={
    'perfil_url': 'https://steamcommunity.com/id/username/'
})
juegos = response.json()['juegos']

# Obtener recomendaciones
nombres = [juego['nombre'] for juego in juegos[:5]]
response = requests.post('http://localhost:5000/api/recomendar', json={
    'nombres_juegos': nombres,
    'n_recomendaciones': 10
})
recomendaciones = response.json()['recomendaciones']
```

---

## Testing

### Probar con curl
```bash
# Health check
curl http://localhost:5000/api/health

# Obtener juegos (reemplaza con tu URL)
curl -X POST http://localhost:5000/api/obtener-juegos \
  -H "Content-Type: application/json" \
  -d '{"perfil_url": "https://steamcommunity.com/id/MetalMaxALIZ/"}'

# Obtener recomendaciones
curl -X POST http://localhost:5000/api/recomendar \
  -H "Content-Type: application/json" \
  -d '{"nombres_juegos": ["Counter-Strike", "Dota 2"], "n_recomendaciones": 5}'
```

### Probar con Postman
1. Importa la siguiente colección o crea las peticiones manualmente
2. Configura la URL base: `http://localhost:5000`
3. Para POST requests, selecciona Body → raw → JSON
4. Copia los ejemplos de request body de esta documentación
