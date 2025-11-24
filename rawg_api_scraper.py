import requests
import sqlite3
import time
import pandas as pd
from datetime import datetime


def crear_base_datos(db_name='juegos_rawg.db'):
    
    # Crea la base de datos y la tabla para almacenar los juegos.
    
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    
    # Crear tabla si no existe
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS rawg_games (
            id INTEGER PRIMARY KEY,
            name TEXT,
            background_image TEXT,
            metacritic INTEGER,
            genres TEXT,
            tags TEXT,
            fecha_extraccion TEXT
        )
    ''')
    
    conn.commit()
    return conn


def extraer_generos(genres_list): 
    
    # Extrae los nombres de los géneros y los convierte a string separado por comas.

    if not genres_list:
        return None
    return ', '.join([genre['name'] for genre in genres_list])


def extraer_tags(tags_list):
    
    # Extrae los nombres de los tags y los convierte a string separado por comas.
    
    if not tags_list:
        return None
    return ', '.join([tag['name'] for tag in tags_list])


def obtener_juegos_rawg(api_key, max_paginas=None, delay_entre_requests=1.5, pagina_inicio=1):

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
        
        try:
            # Hacer la request
            print(f"Página {page}: Solicitando datos...", end=' ')
            response = requests.get(base_url, params=params, timeout=10)
            
            # Verificar el status code
            if response.status_code != 200:
                print(f"\n  Error: Status code {response.status_code}")
                print(f"Respuesta: {response.text[:200]}")
                if response.status_code == 429:  # Too many requests
                    print(f"Esperando 10 segundos antes de reintentar...")
                    time.sleep(10)
                    continue
                break
            
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
                
                # Extraer información relevante
                game_data = {
                    'id': game.get('id'),
                    'name': game.get('name'),
                    'background_image': game.get('background_image'),
                    'metacritic': game.get('metacritic'),
                    'genres': extraer_generos(game.get('genres', [])),
                    'tags': extraer_tags(game.get('tags', [])),
                    'fecha_extraccion': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }
                
                # Insertar en la base de datos
                cursor.execute('''
                    INSERT OR REPLACE INTO rawg_games 
                    (id, name, background_image, metacritic, genres, tags, fecha_extraccion)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (
                    game_data['id'],
                    game_data['name'],
                    game_data['background_image'],
                    game_data['metacritic'],
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
            
        except requests.exceptions.Timeout:
            print(f"\n  Timeout en página {page}. Reintentando en 5 segundos...")
            time.sleep(5)
            continue
            
        except requests.exceptions.RequestException as e:
            print(f"\n Error en la request: {e}")
            break
            
        except Exception as e:
            print(f"\n Error inesperado: {e}")
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


def obtener_dataframe_juegos(db_name='juegos_rawg.db'):
    
    # Obtiene un DataFrame con todos los juegos de la base de datos.
    
    conn = sqlite3.connect(db_name)
    df = pd.read_sql_query('''
        SELECT id, name, background_image, metacritic, genres, tags, fecha_extraccion
        FROM rawg_games
    ''', conn)
    conn.close()
    return df


def main():
    
    # IMPORTANTE: Obtén tu API key gratuita en: https://rawg.io/apidocs
    API_KEY = '9fc0fd5a13c34921aa0fea1a1515b205'
    
    # Configuración
    MAX_PAGINAS = None  # None para extraer todas las páginas, o un número específico
    DELAY = 1.5  # Segundos entre requests (1.5s es conservador)
    PAGINA_INICIO = 5661  # Cambiar a 1 para empezar desde el principio
    
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
