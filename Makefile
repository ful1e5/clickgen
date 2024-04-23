py3 = python3

clean:
	rm -rf .vscode .vim venv coverage.xml out samples/out
	rm -rf .tox build dist src/clickgen.egg-info .mypy_cache .pytest_cache .coverage htmlcov .python-version
	find . -name "__pycache__" -type d -exec /bin/rm -rf {} +

install_deps:
	$(py3) -m pip install -r requirements.txt
	$(py3) -m pip install -r requirements.dev.txt

install:
	$(py3) -m pip install -e .

test:
	pytest

coverage:
	pytest --cov=clickgen --cov-report=html

build: clean
	$(py3) -m build

stubgen:
	find src/clickgen/ -type f -name '*.pyi' -delete
	stubgen "src/clickgen" -o src

tox: clean
	pyenv local 3.7.5 3.8.0 3.9.0 3.10.0 3.11.0 3.12.0
	tox
	pyenv local system

dev: install_deps clean stubgen install coverage
