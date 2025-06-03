import requests
from Pokemon import Pokemon

#--------------------------------------------------------importar arquivo json da PokeAPI
class Game_Request:
    def __init__(self, pokemon_ID):
        self.pokemon_ID = pokemon_ID
    
    def response(self):
        """Obtém dados do Pokémon e retorna um objeto instanciado"""
        url = f"https://pokeapi.co/api/v2/pokemon/{self.pokemon_ID}"
        response = requests.get(url).json()
        
        id = self.pokemon_ID
        name = response["name"]
        types = [t["type"]["name"] for t in response["types"]]  # Lista de tipos
        species = types[0]
        weight = response["weight"]/10 #colocar valor em kg
        height = response["height"]/10 #colocar valor em metros
        photo = response["sprites"]["other"]["official-artwork"]["front_default"] if "sprites" in response else None

        # Criando o objeto Pokémon
        pokemon = Pokemon(id, name, types, species, weight, height, photo)

        return pokemon

