import requests
import pandas as pd
import re


def extraer_steam_id(perfil_url):
    """
    Extrae el Steam ID o vanity URL de una URL de perfil de Steam.
    
    Args:
        perfil_url: URL del perfil de Steam (puede ser /id/nombre o /profiles/numero)
    
    Returns:
        tuple: (tipo, identificador) donde tipo es 'vanity' o 'steamid64'
    """
    # Patrón para vanity URL: steamcommunity.com/id/nombre
    vanity_pattern = r'steamcommunity\.com/id/([^/]+)'
    # Patrón para Steam ID64: steamcommunity.com/profiles/numero
    steamid_pattern = r'steamcommunity\.com/profiles/(\d+)'
    
    vanity_match = re.search(vanity_pattern, perfil_url)
    if vanity_match:
        return 'vanity', vanity_match.group(1)
    
    steamid_match = re.search(steamid_pattern, perfil_url)
    if steamid_match:
        return 'steamid64', steamid_match.group(1)
    
    raise ValueError("URL de perfil de Steam no válida")


def obtener_steam_id64(vanity_url, api_key):
    """
    Convierte una vanity URL a Steam ID64.
    
    Args:
        vanity_url: Nombre personalizado del perfil (ej: 'MetalMaxALIZ')
        api_key: Clave de API de Steam
    
    Returns:
        str: Steam ID64
    """
    url = 'http://api.steampowered.com/ISteamUser/ResolveVanityURL/v0001/'
    params = {
        'key': api_key,
        'vanityurl': vanity_url
    }
    
    response = requests.get(url, params=params)
    data = response.json()
    
    if data['response']['success'] == 1:
        return data['response']['steamid']
    else:
        raise ValueError(f"No se pudo resolver la vanity URL: {vanity_url}")


def obtener_juegos_steam(perfil_url, api_key):
    """
    Obtiene todos los juegos de una cuenta de Steam y los devuelve en un DataFrame.
    
    Args:
        perfil_url: URL del perfil de Steam
        api_key: Clave de API de Steam (obtener en: https://steamcommunity.com/dev/apikey)
    
    Returns:
        pandas.DataFrame: DataFrame con la información de los juegos
    """
    # Extraer el identificador del perfil
    tipo, identificador = extraer_steam_id(perfil_url)
    
    # Si es vanity URL, convertir a Steam ID64
    if tipo == 'vanity':
        steam_id64 = obtener_steam_id64(identificador, api_key)
    else:
        steam_id64 = identificador
    
    # Obtener la lista de juegos
    url = 'http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/'
    params = {
        'key': api_key,
        'steamid': steam_id64,
        'include_appinfo': 1,
        'include_played_free_games': 1,
        'format': 'json'
    }
    
    response = requests.get(url, params=params)
    
    if response.status_code != 200:
        raise Exception(f"Error en la solicitud: {response.status_code}")
    
    data = response.json()
    
    # Verificar si la respuesta contiene juegos
    if 'response' not in data or 'games' not in data['response']:
        raise ValueError("No se pudieron obtener los juegos. El perfil puede ser privado.")
    
    games = data['response']['games']
    
    # Crear DataFrame
    df = pd.DataFrame(games)
    
    # Renombrar columnas para mayor claridad
    columnas_renombradas = {
        'appid': 'app_id',
        'name': 'nombre',
        'playtime_forever': 'tiempo_juego_minutos',
        'playtime_windows_forever': 'tiempo_windows_minutos',
        'playtime_mac_forever': 'tiempo_mac_minutos',
        'playtime_linux_forever': 'tiempo_linux_minutos',
        'playtime_2weeks': 'tiempo_2semanas_minutos'
    }
    
    df.rename(columns=columnas_renombradas, inplace=True)
    
    # Convertir minutos a horas para mejor legibilidad
    df['tiempo_juego_horas'] = df['tiempo_juego_minutos'] / 60
    
    # Añadir URL de la imagen del juego
    df['imagen_url'] = df['app_id'].apply(
        lambda x: f'https://cdn.cloudflare.steamstatic.com/steam/apps/{x}/header.jpg'
    )
    
    # Añadir URL de la página del juego
    df['store_url'] = df['app_id'].apply(
        lambda x: f'https://store.steampowered.com/app/{x}'
    )
    
    return df


def main():
    """
    Función principal de ejemplo.
    """
    # IMPORTANTE: Debes obtener tu propia API key en: https://steamcommunity.com/dev/apikey
    API_KEY = '5EF8885FBA34D73C53DD4AF7564C44C7'
    
    # URL del perfil de Steam
    perfil_url = 'https://steamcommunity.com/id/MetalMaxALIZ/'
    
    try:
        # Obtener los juegos
        df_juegos = obtener_juegos_steam(perfil_url, API_KEY)
        
        # Mostrar información básica
        # print(f"\n{'='*60}")
        # print(f"Total de juegos: {len(df_juegos)}")
        # print(f"{'='*60}\n")
        
        # # Mostrar los primeros juegos
        # print("Primeros 10 juegos:")
        # print(df_juegos[['nombre', 'tiempo_juego_horas']].head(10))
        
        # # Top 10 juegos más jugados
        # print("\n\nTop 10 juegos más jugados:")
        # top_juegos = df_juegos.nlargest(10, 'tiempo_juego_horas')[['nombre', 'tiempo_juego_horas']]
        # print(top_juegos)
        
        # # Estadísticas
        # print(f"\n\nTiempo total de juego: {df_juegos['tiempo_juego_horas'].sum():.2f} horas")
        # print(f"Promedio de tiempo por juego: {df_juegos['tiempo_juego_horas'].mean():.2f} horas")
        
        # Guardar a CSV (opcional)
        # df_juegos.to_csv('mis_juegos_steam.csv', index=False, encoding='utf-8')
        # print("\nDatos guardados en 'mis_juegos_steam.csv'")
        
        return df_juegos
        
    except ValueError as e:
        print(f"Error: {e}")
        print("\nNota: El perfil debe ser público para poder acceder a la biblioteca de juegos.")
    except Exception as e:
        print(f"Error inesperado: {e}")


if __name__ == "__main__":
    df = main()

