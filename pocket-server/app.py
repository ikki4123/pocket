from chalice import Chalice
from chalice import CORSConfig
import random
import requests
import json
import pprint
import jaconv

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
        "id": random_id,
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
        "sprites_front_default": pokemon["sprites"]["front_default"],
    })

@app.route('/detail', cors=cors_config)
def findDetail():
    id = app.current_request.query_params["id"]
    base_url = "https://pokeapi.co/api/v2/pokemon-species/" + str(id)
    result = json.loads(requests.get(base_url).text)
    names = result["names"]
    name = list(filter(lambda x: x["language"]["name"] == 'ja', names))[0]["name"]
    flavor_text_entries = result["flavor_text_entries"]
    flavor_text_entry = list(filter(lambda x: x["language"]["name"] == 'ja-Hrkt', flavor_text_entries))[0]["flavor_text"]
    flavor_text_entry_ja = list(filter(lambda x: x["language"]["name"] == 'ja', flavor_text_entries))[0]["flavor_text"]
    return {
        "name": name,
        "name_hira": jaconv.kata2hira(name),
        "flavor_text_entry" : jaconv.kata2hira(''.join(flavor_text_entry)),
        "flavor_text_entry_ja": ''.join(flavor_text_entry_ja)
        }


def callPokemonApi(id):
    base_url = "https://pokeapi.co/api/v2/pokemon/" + str(id)
    return requests.get(base_url)

def getType2(pokemon):
    if len(pokemon["types"]) == 1:
        return "none"
    return pokemon["types"][1]["type"]["name"]

def getRandomId(request):
    if request.query_params is None:
        return random.randint(MIN_ID, MAX_ID)
        
    if "seed" in request.query_params:
        random.seed(request.query_params["seed"])
        
    if  "max_id" in request.query_params:
        print (request.query_params["max_id"])
        return random.randint(MIN_ID, int(request.query_params["max_id"]))
    
    return random.randint(MIN_ID, MAX_ID)