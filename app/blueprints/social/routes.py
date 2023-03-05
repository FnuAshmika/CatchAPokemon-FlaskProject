from . import bp as social_bp
from .models import User , PokeCatch, db
from app.forms import PokeForm
from flask import redirect, render_template, flash, url_for, request, jsonify
from flask_login import login_required, current_user
import requests, random

@social_bp.route('/user/<username>')
def user(username):
    user_match = User.query.filter_by(username=username).first()
    if not user_match:
        redirect('/')
    pokemons = user_match.pokemons
    return render_template('user.jinja', user=user_match, pokemons=pokemons )

@social_bp.route('/search_pokemon', methods=['GET', 'POST'])
def search_pokemon():
    form = PokeForm()
    if form.validate_on_submit():
        pokemon_name = form.pokemon_name.data
        response = requests.get(f'https://pokeapi.co/api/v2/pokemon/{pokemon_name}')
        if response.ok:
            pokemon_data = response.json()
            img_url = pokemon_data['sprites']['front_default']
            return render_template('add_pokemon.jinja', pokemon_name=pokemon_name.title(), img_url=img_url, form=form)
        else:
            flash('Invalid Pokemon name', 'error')
    # Get data for 4 random Pokemon
    pokemon_list = []
    for i in range(4):
        pokemon_id = random.randint(1, 898) # 898 is the total number of Pokemon
        response = requests.get(f'https://pokeapi.co/api/v2/pokemon/{pokemon_id}')
        if response.ok:
            pokemon_data = response.json()
            name = pokemon_data['name']
            img_url = pokemon_data['sprites']['front_default']
            pokemon_list.append({'name': name, 'img_url': img_url})    
            
    return render_template('search_pokemon.jinja', form=form, pokemon_list=pokemon_list)

@social_bp.route('/add_pokemon', methods=['POST'])
def add_pokemon():
    form=PokeForm()
    if request.method == 'POST':
        pokemon_name = request.form.get('pokemon_name')
        if pokemon_name:
            pokecatch = PokeCatch(poke=pokemon_name, user_id=current_user.id)
            db.session.add(pokecatch)
            db.session.commit()
            flash(f"{pokemon_name} added to your collection!")
        else:
            flash("Please enter a valid Pokemon name.")  
    return redirect(url_for('social.user', username=current_user.username))