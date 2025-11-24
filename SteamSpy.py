import requests
import time
import sqlite3

def fetch_and_save_data():
    base_url = "https://steamspy.com/api.php?request=all&page="
    page = 0
    
    # Conectar a la base de datos SQLite (se crea si no existe)
    conn = sqlite3.connect('steam_data.db')
    cursor = conn.cursor()
    
    # Variable para controlar si ya creamos la tabla
    table_created = False

    while True:
        print(f"Obteniendo página {page}...")
        response = requests.get(base_url + str(page))
        
        if response.status_code != 200:
            print(f"Error: Código de estado {response.status_code}")
            break
        
        data = response.json()
        if not data or len(data) == 0:
            print("No hay más datos disponibles")
            break
        
        # Crear la tabla con la primera página de datos
        if not table_created:
            # Obtener las columnas del primer juego
            first_game = list(data.values())[0]
            columns = first_game.keys()
            
            # Crear la tabla
            columns_def = ', '.join([f'"{col}" TEXT' for col in columns])
            cursor.execute(f'CREATE TABLE IF NOT EXISTS steam_games ({columns_def})')
            table_created = True
            print("Tabla creada exitosamente")
        
        # Insertar los datos
        for game_id, game_data in data.items():
            columns = list(game_data.keys())
            placeholders = ', '.join(['?' for _ in columns]) 
            columns_str = ', '.join([f'"{col}"' for col in columns])
            values = [str(game_data[col]) for col in columns]
            
            cursor.execute(f'INSERT INTO steam_games ({columns_str}) VALUES ({placeholders})', values)
        
        conn.commit()
        print(f"Página {page} guardada exitosamente ({len(data)} juegos)")
        
        page += 1
        
        # Esperar 70 segundos antes de la siguiente solicitud
        time.sleep(70)
    
    # Cerrar la conexión
    conn.close()
    print(f"Recolección de datos completada. Total de páginas: {page}")

fetch_and_save_data()