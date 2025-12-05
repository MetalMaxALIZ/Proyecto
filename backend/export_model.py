"""
Script to export model data to pickle files
Run this in a notebook or Python after training the model
"""
import pickle
import os
import pandas as pd

# Ensure data directory exists
data_path = os.path.join(os.path.dirname(__file__), '..', 'data')
os.makedirs(data_path, exist_ok=True)

# Save DataFrames and model
# Run this in the notebook after creating the variables

def guardar_modelo(df_combinado_final, df_modelo, df_modelo_normalizado, knn_modelo, juegos_dict):
    """
    Saves all necessary components for the recommendation system
    """
    print("Saving model data...")
    
    # Save DataFrames
    df_combinado_final.to_pickle(os.path.join(data_path, 'df_combinado_final.pkl'))
    print("✓ df_combinado_final saved")
    
    df_modelo.to_pickle(os.path.join(data_path, 'df_modelo.pkl'))
    print("✓ df_modelo saved")
    
    # Save normalized array
    with open(os.path.join(data_path, 'df_modelo_normalizado.pkl'), 'wb') as f:
        pickle.dump(df_modelo_normalizado, f)
    print("✓ df_modelo_normalizado saved")
    
    # Save KNN model
    with open(os.path.join(data_path, 'knn_modelo.pkl'), 'wb') as f:
        pickle.dump(knn_modelo, f)
    print("✓ knn_modelo saved")
    
    # Save games dictionary
    with open(os.path.join(data_path, 'juegos_dict.pkl'), 'wb') as f:
        pickle.dump(juegos_dict, f)
    print("✓ juegos_dict saved")
    
    print("\nAll data saved successfully!")
    print(f"Location: {data_path}")

# Usage example (run in the notebook):
# guardar_modelo(df_combinado_final, df_modelo, df_modelo_normalizado, knn_modelo, juegos_dict)
