import pandas as pd
import requests
from tqdm import tqdm

# Función para obtener la URL de la cadena evolutiva
def get_evolution_chain_url(species_url):
    response = requests.get(species_url)
    if response.status_code == 200:
        species_data = response.json()
        return species_data['evolution_chain']['url'], species_data['id']
    else:
        return None, None

# Función para obtener la cadena evolutiva
def get_evolution_chain(evolution_chain_url):
    response = requests.get(evolution_chain_url)
    if response.status_code == 200:
        evolution_chain_data = response.json()
        return evolution_chain_data
    else:
        return None

# Función para extraer las evoluciones de la cadena evolutiva
def extract_evolutions(chain, evolution_group):
    evolutions = []
    def traverse(chain, evolution_phase=1):
        current_species = chain['species']['name']
        response = requests.get(chain['species']['url'])
        species_data = response.json()
        evolutions.append({
            'ID': species_data['id'],
            'Pokémon': current_species,
            'Grupo de Evolución': evolution_group,
            'Fase de Evolución': evolution_phase
        })
        for evolution in chain['evolves_to']:
            traverse(evolution, evolution_phase + 1)
    
    traverse(chain['chain'])
    return evolutions

# Lista para almacenar las evoluciones
evolution_list = []

# Diccionario para rastrear los grupos de evolución únicos
evolution_groups = {}

# Obtener datos para los primeros 1025 Pokémon
for i in tqdm(range(1, 1026), desc="Extrayendo evoluciones de Pokémon"):
    pokemon_url = f'https://pokeapi.co/api/v2/pokemon-species/{i}/'
    evolution_chain_url, species_id = get_evolution_chain_url(pokemon_url)
    if evolution_chain_url:
        evolution_chain = get_evolution_chain(evolution_chain_url)
        if evolution_chain:
            evolution_group = evolution_chain['chain']['species']['name']
            if evolution_group not in evolution_groups:
                evolution_groups[evolution_group] = f'Grupo_{len(evolution_groups) + 1}'
            evolutions = extract_evolutions(evolution_chain, evolution_groups[evolution_group])
            evolution_list.extend(evolutions)

# Crear un DataFrame con los datos de evoluciones
df_evolutions = pd.DataFrame(evolution_list)

# Eliminar duplicados
df_evolutions.drop_duplicates(inplace=True)

# Guardar los datos en un archivo CSV
file_path_save = 'pokemon_evolution.csv'
df_evolutions.to_csv(file_path_save, index=False)

print(f"Evoluciones de Pokémon guardadas en '{file_path_save}'")
