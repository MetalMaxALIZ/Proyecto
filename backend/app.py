from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
import os
import pandas as pd
import numpy as np
import pickle
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import NearestNeighbors

# Añadir el directorio padre al path para importar los módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from steam_profile_games import obtener_juegos_steam

app = Flask(__name__)
CORS(app)  # Permitir peticiones desde React

# API Key de Steam
API_KEY = '5EF8885FBA34D73C53DD4AF7564C44C7'

# Variables globales para el modelo
knn_modelo = None
df_modelo_normalizado = None
df_modelo = None
df_combinado_final = None
juegos_dict = None

def cargar_modelo():
    """Carga el modelo y los datos necesarios"""
    global knn_modelo, df_modelo_normalizado, df_modelo, df_combinado_final, juegos_dict
    
    try:
        # Cargar datos (asumiendo que están guardados en archivos pickle o CSV)
        # Ajusta las rutas según donde guardes los datos del notebook
        data_path = os.path.join(os.path.dirname(__file__), '..', 'data')
        
        # Intentar cargar los datos si existen
        if os.path.exists(os.path.join(data_path, 'df_combinado_final.pkl')):
            df_combinado_final = pd.read_pickle(os.path.join(data_path, 'df_combinado_final.pkl'))
            df_modelo = pd.read_pickle(os.path.join(data_path, 'df_modelo.pkl'))
            
            with open(os.path.join(data_path, 'knn_modelo.pkl'), 'rb') as f:
                knn_modelo = pickle.load(f)
            
            with open(os.path.join(data_path, 'df_modelo_normalizado.pkl'), 'rb') as f:
                df_modelo_normalizado = pickle.load(f)
                
            with open(os.path.join(data_path, 'juegos_dict.pkl'), 'rb') as f:
                juegos_dict = pickle.load(f)
            
            print("Modelo cargado correctamente")
            return True
        else:
            print("No se encontraron los archivos del modelo. Ejecuta el notebook primero.")
            return False
    except Exception as e:
        print(f"Error al cargar el modelo: {e}")
        return False

@app.route('/api/obtener-juegos', methods=['POST'])
def obtener_juegos():
    """Endpoint para obtener los juegos de Steam de un perfil"""
    try:
        data = request.json
        perfil_url = data.get('perfil_url')
        
        if not perfil_url:
            return jsonify({'error': 'Se requiere perfil_url'}), 400
        
        # Obtener los juegos del perfil
        df_juegos = obtener_juegos_steam(perfil_url, API_KEY)
        
        # Ordenar por tiempo de juego
        df_juegos = df_juegos.sort_values('tiempo_juego_minutos', ascending=False)
        
        # Convertir a formato JSON compatible
        # Asegurarse de que img_icon_url tenga la URL correcta
        df_juegos['img_icon_url'] = df_juegos.apply(
            lambda row: f"https://cdn.cloudflare.steamstatic.com/steam/apps/{row['app_id']}/header.jpg",
            axis=1
        )
        
        juegos = df_juegos[['app_id', 'nombre', 'tiempo_juego_minutos', 'tiempo_juego_horas', 'img_icon_url']].to_dict('records')
        
        return jsonify({
            'success': True,
            'juegos': juegos,
            'total': len(juegos)
        })
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': f'Error inesperado: {str(e)}'}), 500

@app.route('/api/recomendar', methods=['POST'])
def recomendar():
    """Endpoint para recomendar juegos basados en una lista de juegos seleccionados"""
    try:
        data = request.json
        nombres_juegos = data.get('nombres_juegos', [])
        n_recomendaciones = data.get('n_recomendaciones', 10)
        
        if not nombres_juegos:
            return jsonify({'error': 'Se requiere una lista de nombres de juegos'}), 400
        
        if knn_modelo is None:
            return jsonify({'error': 'El modelo no está cargado. Ejecuta el notebook primero.'}), 500
        
        # Llamar a la función de recomendación
        recomendaciones = recomendar_juegos(nombres_juegos, n_recomendaciones)
        
        if recomendaciones is None or len(recomendaciones) == 0:
            return jsonify({
                'success': False,
                'error': 'No se pudieron generar recomendaciones'
            }), 400
        
        # Convertir a formato JSON
        recomendaciones_json = recomendaciones.to_dict('records')
        
        return jsonify({
            'success': True,
            'recomendaciones': recomendaciones_json,
            'total': len(recomendaciones_json)
        })
        
    except Exception as e:
        return jsonify({'error': f'Error al generar recomendaciones: {str(e)}'}), 500

def recomendar_juegos(nombres_juegos, n_recomendaciones=10):
    """
    Función para recomendar juegos similares basándose en juegos del diccionario juegos_dict
    """
    if isinstance(nombres_juegos, str):
        nombres_juegos = [nombres_juegos]
    
    indices_juegos = []
    for nombre in nombres_juegos:
        if nombre in juegos_dict['app_id']:
            app_id = juegos_dict['app_id'][nombre]
            mask = df_combinado_final['appid'] == str(app_id)
            if mask.any():
                idx = df_combinado_final[mask].index[0]
                if idx in df_modelo.index:
                    indice_en_modelo = df_modelo.index.get_loc(idx)
                    indices_juegos.append(indice_en_modelo)
    
    if len(indices_juegos) == 0:
        return None
    
    juegos_vectores = df_modelo_normalizado[indices_juegos]
    centroide = juegos_vectores.mean(axis=0).reshape(1, -1)
    
    distancias, indices = knn_modelo.kneighbors(centroide, n_neighbors=n_recomendaciones + len(indices_juegos))
    
    indices_recomendados = []
    distancias_recomendadas = []
    
    for i, idx in enumerate(indices[0]):
        if idx not in indices_juegos:
            indices_recomendados.append(idx)
            distancias_recomendadas.append(distancias[0][i])
        
        if len(indices_recomendados) == n_recomendaciones:
            break
    
    indices_originales = df_modelo.index[indices_recomendados].tolist()
    
    juegos_recomendados = df_combinado_final.loc[indices_originales][['appid', 'name', 'genres', 'owners', 'porcentaje_votos_positivos']].copy()
    juegos_recomendados['similitud'] = 1 / (1 + np.array(distancias_recomendadas))
    
    # Añadir imagen URL
    juegos_recomendados['imagen_url'] = juegos_recomendados['appid'].apply(
        lambda x: f'https://cdn.cloudflare.steamstatic.com/steam/apps/{x}/header.jpg'
    )
    
    return juegos_recomendados

@app.route('/api/health', methods=['GET'])
def health():
    """Endpoint para verificar el estado del servidor"""
    modelo_cargado = knn_modelo is not None
    return jsonify({
        'status': 'ok',
        'modelo_cargado': modelo_cargado
    })

if __name__ == '__main__':
    print("Iniciando servidor Flask...")
    cargar_modelo()
    app.run(debug=True, port=5000)
