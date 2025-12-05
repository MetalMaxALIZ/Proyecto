"""
Script para exportar los datos del modelo a archivos pickle
Ejecuta esto en un notebook o Python después de entrenar el modelo
"""
import pickle
import os
import pandas as pd

# Asegurarse de que el directorio data existe
data_path = os.path.join(os.path.dirname(__file__), '..', 'data')
os.makedirs(data_path, exist_ok=True)

# Guardar los DataFrames y el modelo
# Ejecuta esto en el notebook después de crear las variables

def guardar_modelo(df_combinado_final, df_modelo, df_modelo_normalizado, knn_modelo, juegos_dict):
    """
    Guarda todos los componentes necesarios para el sistema de recomendaciones
    """
    print("Guardando datos del modelo...")
    
    # Guardar DataFrames
    df_combinado_final.to_pickle(os.path.join(data_path, 'df_combinado_final.pkl'))
    print("✓ df_combinado_final guardado")
    
    df_modelo.to_pickle(os.path.join(data_path, 'df_modelo.pkl'))
    print("✓ df_modelo guardado")
    
    # Guardar array normalizado
    with open(os.path.join(data_path, 'df_modelo_normalizado.pkl'), 'wb') as f:
        pickle.dump(df_modelo_normalizado, f)
    print("✓ df_modelo_normalizado guardado")
    
    # Guardar modelo KNN
    with open(os.path.join(data_path, 'knn_modelo.pkl'), 'wb') as f:
        pickle.dump(knn_modelo, f)
    print("✓ knn_modelo guardado")
    
    # Guardar diccionario de juegos
    with open(os.path.join(data_path, 'juegos_dict.pkl'), 'wb') as f:
        pickle.dump(juegos_dict, f)
    print("✓ juegos_dict guardado")
    
    print("\n¡Todos los datos se guardaron correctamente!")
    print(f"Ubicación: {data_path}")

# Ejemplo de uso (ejecutar en el notebook):
# guardar_modelo(df_combinado_final, df_modelo, df_modelo_normalizado, knn_modelo, juegos_dict)
