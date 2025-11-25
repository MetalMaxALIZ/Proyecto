import requests
import sqlite3
import time
import pandas as pd
from datetime import datetime


def crear_base_datos(db_name='juegos_rawgv2.db'):
    #
    # Crea la base de datos y la tabla para almacenar los juegos.
    #
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    
    # Eliminar la tabla si existe para recrearla con la nueva estructura
    cursor.execute('DROP TABLE IF EXISTS rawg_games')
    
    # Crear tabla con la estructura actualizada
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS rawg_games (
            id INTEGER PRIMARY KEY,
            name TEXT,
            background_image TEXT,
            metacritic INTEGER,
            is_pc BOOLEAN,
            steam_store_id INTEGER,
            genres TEXT,
            tags TEXT,
            fecha_extraccion TEXT
        )
    ''')
    
    conn.commit()
    return conn


def extraer_generos(genres_list): # Extrae los nombres de los géneros y los convierte a string separado por comas.
    if not genres_list:
        return None
    return ', '.join([genre['name'] for genre in genres_list])


def extraer_tags(tags_list):
    #
    # Extrae los nombres de los tags y los convierte a string separado por comas.
    #
    if not tags_list:
        return None
    return ', '.join([tag['name'] for tag in tags_list])


def es_juego_pc(platforms_list):
    """
    Verifica si el juego está disponible para PC.
    """
    if not platforms_list:
        return False
    
    for platform_info in platforms_list:
        platform = platform_info.get('platform', {})
        if platform.get('name') == 'PC':
            return True
    return False


def obtener_steam_store_id(stores_list):
    """
    Obtiene el ID de Steam Store si el juego está disponible en Steam.
    """
    if not stores_list:
        return None
    
    for store_info in stores_list:
        store = store_info.get('store', {})
        if store.get('name') == 'Steam':
            return store_info.get('id')
    return None


def obtener_juegos_rawg(api_key, max_paginas=None, delay_entre_requests=1.5, pagina_inicio=1):
    
    # Obtiene todos los juegos de la API de RAWG y los guarda en la base de datos.

    base_url = 'https://api.rawg.io/api/games'
    page_size = 40  # Tamaño máximo permitido por la API
    page = pagina_inicio
    total_juegos = 0
    juegos_insertados = 0
    
    # Crear base de datos
    conn = crear_base_datos()
    cursor = conn.cursor() # Cursor para ejecutar queries
    
    print(f"{'='*70}")
    print(f"Iniciando extracción de juegos de RAWG API")
    print(f"Tamaño de página: {page_size}")
    print(f"Delay entre requests: {delay_entre_requests}s")
    print(f"{'='*70}\n")
    
    inicio = datetime.now()
    
    while True:
        # Preparar parámetros de la request
        params = {
            'key': api_key,
            'page': page,
            'page_size': page_size
           
        }
        
        # Sistema de reintentos para la página actual
        reintentos = 0
        max_reintentos = 10
        request_exitosa = False
        
        while reintentos < max_reintentos and not request_exitosa:
            try:
                # Hacer la request
                if reintentos == 0:
                    print(f"Página {page}: Solicitando datos...", end=' ')
                else:
                    print(f"Página {page}: Reintento {reintentos}/{max_reintentos}...", end=' ')
                
                response = requests.get(base_url, params=params, timeout=10)
                
                # Verificar el status code
                if response.status_code == 502:
                    reintentos += 1
                    print(f"\n  Error 502 (Bad Gateway). Esperando 5 segundos...")
                    time.sleep(5)
                    continue
                
                if response.status_code == 429:  # Too many requests
                    reintentos += 1
                    print(f"\n  Error 429 (Rate limit). Esperando 10 segundos...")
                    time.sleep(10)
                    continue
                
                if response.status_code != 200:
                    print(f"\n  Error: Status code {response.status_code}")
                    print(f"Respuesta: {response.text[:200]}")
                    reintentos += 1
                    time.sleep(5)
                    continue
                
                # Si llegamos aquí, la request fue exitosa
                request_exitosa = True
                
            except requests.exceptions.Timeout:
                reintentos += 1
                print(f"\n  Timeout. Esperando 5 segundos...")
                time.sleep(5)
                continue
                
            except requests.exceptions.RequestException as e:
                reintentos += 1
                print(f"\n  Error en la request: {e}. Esperando 5 segundos...")
                time.sleep(5)
                continue
                
            except Exception as e:
                print(f"\n Error inesperado: {e}")
                reintentos += 1
                time.sleep(5)
                continue
        
        # Si agotamos los reintentos sin éxito, salir del bucle principal
        if not request_exitosa:
            print(f"\n Máximo de reintentos alcanzado en página {page}. Deteniendo extracción.")
            break
        
        try:
            data = response.json()
            
            # Debug: mostrar estructura de la respuesta
            if page == 1:
                print(f"\nEstructura de la respuesta: {list(data.keys())}")
            
            # Verificar si hay resultados
            if 'results' not in data or not data['results']:
                print(f"No hay más resultados. Data keys: {list(data.keys())}")
                if 'detail' in data:
                    print(f"Error de API: {data['detail']}")
                break
            
            games = data['results']
            print(f"Recibidos {len(games)} juegos.", end=' ')
            
            # Procesar y guardar cada juego
            for game in games:
                total_juegos += 1
                
                # Verificar si es para PC y está en Steam
                is_pc = es_juego_pc(game.get('platforms', []))
                steam_id = obtener_steam_store_id(game.get('stores', []))
                
                # Solo guardar si es para PC Y está en Steam
                if not is_pc or steam_id is None:
                    continue
                
                # Extraer información relevante
                game_data = {
                    'id': game.get('id'),
                    'name': game.get('name'),
                    'background_image': game.get('background_image'),
                    'metacritic': game.get('metacritic'),
                    'is_pc': is_pc,
                    'steam_store_id': steam_id,
                    'genres': extraer_generos(game.get('genres', [])),
                    'tags': extraer_tags(game.get('tags', [])),
                    'fecha_extraccion': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }
                
                # Insertar en la base de datos
                cursor.execute('''
                    INSERT OR REPLACE INTO rawg_games 
                    (id, name, background_image, metacritic, is_pc, steam_store_id, genres, tags, fecha_extraccion)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    game_data['id'],
                    game_data['name'],
                    game_data['background_image'],
                    game_data['metacritic'],
                    game_data['is_pc'],
                    game_data['steam_store_id'],
                    game_data['genres'],
                    game_data['tags'],
                    game_data['fecha_extraccion']
                ))
                
                juegos_insertados += 1
            
            # Commit cada página
            conn.commit()
            print(f"✓ Guardados {juegos_insertados} juegos en total.")
            
            # Verificar si hay más páginas
            if not data.get('next'):
                print("\n✓ Se han procesado todas las páginas disponibles.")
                break
            
            # Verificar límite de páginas
            if max_paginas and page >= max_paginas:
                print(f"\n✓ Alcanzado el límite de {max_paginas} páginas.")
                break
            
            # Siguiente página
            page += 1
            
            # Esperar antes de la siguiente request
            time.sleep(delay_entre_requests)
            
        except Exception as e:
            print(f"\n❌ Error inesperado procesando datos: {e}")
            break
    
    # Obtener estadísticas finales
    cursor.execute('SELECT COUNT(*) FROM rawg_games')
    total_en_db = cursor.fetchone()[0]
    
    fin = datetime.now()
    duracion = (fin - inicio).total_seconds()
    
    print(f"\n{'='*70}")
    print(f"Extracción completada")
    print(f"{'='*70}")
    print(f"Páginas procesadas: {page}")
    print(f"Total de juegos en BD: {total_en_db}")
    print(f"Tiempo total: {duracion:.2f} segundos ({duracion/60:.2f} minutos)")
    print(f"{'='*70}\n")
    
    # Crear DataFrame con los resultados
    df = pd.read_sql_query('SELECT * FROM rawg_games', conn)
    
    conn.close()
    
    return df


def obtener_dataframe_juegos(db_name='juegos_rawgv2.db'):
    
    # Obtiene un DataFrame con todos los juegos de PC disponibles en Steam.
    
    conn = sqlite3.connect(db_name)
    df = pd.read_sql_query('''
        SELECT id, name, background_image, metacritic, steam_store_id, genres, tags, fecha_extraccion
        FROM rawg_games
        WHERE is_pc = 1 AND steam_store_id IS NOT NULL
    ''', conn)
    conn.close()
    return df


def main():
    
    #Función principal.
    
    # IMPORTANTE: Obtén tu API key gratuita en: https://rawg.io/apidocs
    API_KEY = '9fc0fd5a13c34921aa0fea1a1515b205'
    
    # Configuración
    MAX_PAGINAS = None  # None para extraer todas las páginas, o un número específico
    DELAY = 1.5  # Segundos entre requests (1.5s es conservador)
    PAGINA_INICIO = 1  
    
    try:
        # Extraer juegos
        df_todos = obtener_juegos_rawg(API_KEY, max_paginas=MAX_PAGINAS, delay_entre_requests=DELAY, pagina_inicio=PAGINA_INICIO)
        
        # Obtener DataFrame desde la base de datos
        df_juegos = obtener_dataframe_juegos()
        
        print(f"DataFrame creado con {len(df_juegos)} juegos totales")
        
        # Mostrar algunos ejemplos
        print("\n--- Primeros 5 juegos ---")
        print(df_juegos[['name', 'metacritic', 'genres']].head())
        
        # Opcional: Guardar a CSV
        # df_juegos.to_csv('juegos_rawg.csv', index=False, encoding='utf-8')
        
        return df_juegos
        
    except Exception as e:
        print(f"Error en main: {e}")
        return None


if __name__ == "__main__":
    df_juegos = main()
