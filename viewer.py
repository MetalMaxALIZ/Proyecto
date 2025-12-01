import pickle
from pathlib import Path

# Cargar el diccionario de juegos
checkpoint_folder = Path('checkpoints')
apps_dict_path = checkpoint_folder / 'apps_dict-ckpt-fin.p'

with open(apps_dict_path, 'rb') as f:
    apps_dict = pickle.load(f)

print(f"Total de juegos: {len(apps_dict)}")

# Ver un ejemplo de juego
first_appid = list(apps_dict.keys())[0]
print(apps_dict[first_appid])