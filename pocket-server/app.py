from chalice import Chalice
from chalice import CORSConfig
import random
import requests
import json
import pprint


cors_config = CORSConfig(
    allow_credentials=True
)

app = Chalice(app_name='pocket-server')
MIN_ID = 1
MAX_ID = 898

@app.route('/', cors=cors_config)
def index():
    return {"message": "welcom!"}

@app.route('/random', cors=cors_config)
def index():
    request = app.current_request
    random_id = getRandomId(request)
    pokemon = json.loads(callPokemonApi(random_id).text)
    return json.dumps({
        "name": pokemon["name"],
        "stats": {
            "h":pokemon["stats"][0]["base_stat"],
            "a":pokemon["stats"][1]["base_stat"],
            "b":pokemon["stats"][2]["base_stat"],
            "c":pokemon["stats"][3]["base_stat"],
            "d":pokemon["stats"][4]["base_stat"],
            "s":pokemon["stats"][5]["base_stat"]
        },
        "types": {
            "type1":pokemon["types"][0]["type"]["name"],
            "type2":getType2(pokemon)
        },
        "sprites_back_default": pokemon["sprites"]["back_default"],
    })

def callPokemonApi(id):
    base_url = "https://pokeapi.co/api/v2/pokemon/" + str(id)
    return requests.get(base_url)

def getType2(pokemon):
    if len(pokemon["types"]) == 1:
        return "none"
    return pokemon["types"][1]["type"]["name"]

def getRandomId(request):
    if request.query_params is None or request.query_params["seed"] is None:
        return random.randint(MIN_ID, MAX_ID)
    
    random.seed(request.query_params["seed"])
    return random.randint(MIN_ID, MAX_ID)