import pandas as pd
import requests
from tqdm import tqdm

# Diccionario para mapear la generación a números del 1 al 9
generation_mapping = {
    'generation-i': 1,
    'generation-ii': 2,
    'generation-iii': 3,
    'generation-iv': 4,
    'generation-v': 5,
    'generation-vi': 6,
    'generation-vii': 7,
    'generation-viii': 8,
    'generation-ix': 9
}

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
        # Obtener la generación del Pokémon
        species_url = data['species']['url']
        species_response = requests.get(species_url)
        if species_response.status_code == 200:
            species_data = species_response.json()
            generation = generation_mapping.get(species_data['generation']['name'], None)
            is_legendary = species_data['is_legendary']
            is_mythical = species_data['is_mythical']
            is_ultra_beast = species_data.get('is_ultra_beast', False)  # Algunos endpoints pueden no tener esta clave
            if is_legendary:
                category = 'Legendario'
            elif is_mythical:
                category = 'Mítico'
            elif is_ultra_beast:
                category = 'Ultraente'
            else:
                category = 'Común'
        else:
            generation = None
            category = None
        
        # Calcular la suma total de las estadísticas base
        total_stats = sum([stat['base_stat'] for stat in data['stats']])
        
        pokemon_data = {
            'id': data['id'],
            'name': data['name'],
            'type1': type_translation.get(data['types'][0]['type']['name'], data['types'][0]['type']['name']),
            'type2': type_translation.get(data['types'][1]['type']['name'], data['types'][1]['type']['name']) if len(data['types']) > 1 else None,
            'hp': data['stats'][0]['base_stat'],
            'attack': data['stats'][1]['base_stat'],
            'defense': data['stats'][2]['base_stat'],
            'special-attack': data['stats'][3]['base_stat'],
            'special-defense': data['stats'][4]['base_stat'],
            'speed': data['stats'][5]['base_stat'],
            'weight': data['weight'],
            'height': data['height'],
            'image_url': data['sprites']['front_default'],  # Enlace de la imagen
            'generation': generation,  # Generación
            'category': category,  # Categoría
            'total_stats': total_stats  # Suma total de estadísticas base
        }
        return pokemon_data
    else:
        return None

# Extraer datos de los primeros 1025 Pokémon con barra de progreso
pokemon_list = []
for i in tqdm(range(1, 1026), desc="Extrayendo datos de Pokémon"):
    pokemon_data = get_pokemon_data(i)
    if pokemon_data:
        pokemon_list.append(pokemon_data)

# Crear un DataFrame con los datos extraídos
df = pd.DataFrame(pokemon_list)

# Crear una columna 'combined_type' combinando 'type1' y 'type2'
df['combined_type'] = df.apply(lambda row: row['type1'] if row['type2'] is None else f"{row['type1']}/{row['type2']}", axis=1)

# Guardar los datos en un archivo CSV
file_path_save = 'pokemon_data.csv'
df.to_csv(file_path_save, index=False)

print(f"Datos de Pokémon guardados en 'pokemon_data.csv'")
