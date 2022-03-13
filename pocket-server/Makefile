pip-install:
	curl -kL https://bootstrap.pypa.io/get-pip.py | python
init:
	pip install chalice
	pip install pytest
	pip install pytest-chalice
	pip install pokebase

deploy:
	pip freeze > requirements.txt
	chalice deploy
local-deploy:
	chalice local

test:
	py.test -s tests/test_app.py 
	