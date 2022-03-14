from chalice.test import Client
from app import app
from http import HTTPStatus

def test_random(client):
    response = client.get('/random')
    print(response.json)
    assert response.status_code == HTTPStatus.OK

def test_random_max_id(client):
    response = client.get('/random?max_id=2')
    print(response.json)
    assert response.status_code == HTTPStatus.OK

def test_random_with_seed(client):
    response = client.get('/random?seed=1')
    assert response.status_code == HTTPStatus.OK
    assert response.json == {
        "id": 490, 
        "name": 
        "manaphy",
        "sprites_back_default": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/back/490.png",
        'sprites_front_default': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/490.png',
        "stats": {"a": 100, "b": 100, "c": 100, "d": 100, "h": 100, "s": 100},"types": {"type1": "water", "type2": "none"}}


def test_find_detail(client):
    response = client.get('/detail?id=1')
    assert response.status_code == HTTPStatus.OK
    assert response.json == {
        'flavor_text_entry': 'うまれたときから\u3000せなかに\nふしぎな\u3000たねが\u3000うえてあって\nからだと\u3000ともに\u3000そだつという。',
        'flavor_text_entry_ja': '生まれたときから\u3000背中に\n不思議な\u3000タネが\u3000植えてあって\n体と\u3000ともに\u3000育つという。',
        'name': 'フシギダネ',
        'name_hira': 'ふしぎだね'
        }