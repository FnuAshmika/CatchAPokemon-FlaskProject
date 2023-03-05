from . import bp as main_bp
from flask import render_template
import requests
import random

@main_bp.route('/')
def index():
    response=requests.get('https://pokeapi.co/api/v2/pokemon?limit=1000')
    pokemon_data = response.json()['results']
    num_pokemon = random.randint(10, 15)
    random_pokemon = random.sample(pokemon_data, num_pokemon)
    pokemon_info = []
    for pokemon in random_pokemon:
        response = requests.get(pokemon['url'])
        pokemon_details = response.json()
        image_url = pokemon_details['sprites']['front_default']
        pokemon_info.append({
            'name': pokemon['name'].capitalize(),
            'image_url': image_url
        })
    return render_template('index.jinja', title='Home', pokemon_info=pokemon_info)

