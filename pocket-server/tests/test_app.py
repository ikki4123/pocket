from chalice.test import Client
from app import app
from http import HTTPStatus

def test_random(client):
    response = client.get('/random')
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
        'flavor_text_entry': 'うまれたときからせなかにふしぎなたねがうえてあってからだとともにそだつという。',
        'flavor_text_entry_ja': '生まれたときから背中に不思議なタネが植えてあって体とともに育つという。',
        'name': 'フシギダネ',
        'name_hira': 'ふしぎだね'
        }