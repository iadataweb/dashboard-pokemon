import pandas as pd
import requests
from tqdm import tqdm

# Diccionario para traducir tipos
type_translation = {
    'normal': 'normal',
    'fighting': 'lucha',
    'flying': 'volador',
    'poison': 'veneno',
    'ground': 'tierra',
    'rock': 'roca',
    'bug': 'bicho',
    'ghost': 'fantasma',
    'steel': 'acero',
    'fire': 'fuego',
    'water': 'agua',
    'grass': 'planta',
    'electric': 'eléctrico',
    'psychic': 'psíquico',
    'ice': 'hielo',
    'dragon': 'dragón',
    'dark': 'oscuro',
    'fairy': 'hada'
}

# Definir la función para obtener los datos de un Pokémon
def get_pokemon_data(pokemon_id):
    url = f'https://pokeapi.co/api/v2/pokemon/{pokemon_id}'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        type1 = type_translation.get(data['types'][0]['type']['name'], data['types'][0]['type']['name'])
        type2 = type_translation.get(data['types'][1]['type']['name'], data['types'][1]['type']['name']) if len(data['types']) > 1 else None

        combo = f"{type1}/{type2}" if type2 else type1

        pokemon_data = []
        # Agregar entrada para el tipo principal con combinación completa
        pokemon_data.append({
            'code': f"{pokemon_id}_1",
            'name': data['name'],
            'type': type1,
            'combo': combo
        })
        # Agregar entrada para el tipo secundario si existe con combinación completa
        if type2:
            pokemon_data.append({
                'code': f"{pokemon_id}_2",
                'name': data['name'],
                'type': type2,
                'combo': combo
            })
        return pokemon_data
    else:
        return None

# Extraer datos de los primeros 1025 Pokémon con barra de progreso
pokemon_list = []
for i in tqdm(range(1, 1026), desc="Extrayendo datos de Pokémon"):
    pokemon_data = get_pokemon_data(i)
    if pokemon_data:
        pokemon_list.extend(pokemon_data)

# Crear un DataFrame con los datos extraídos
df = pd.DataFrame(pokemon_list)

# Guardar los datos en un archivo CSV
file_path_save = 'pokemon_types.csv'
df.to_csv(file_path_save, index=False)

print(f"Datos de Pokémon guardados en 'pokemon_types.csv'")
