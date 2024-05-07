install:
	pipenv shell
	pipenv install --dev

test:
	pytest -v --cov=example/src example/

fix:
	ruff check -v --fix .

watch:
	ruff check . --watch

format:
	ruff check --fix .
	ruff format .