py3 = python3

clean:
	rm -rf .vscode .vim venv coverage.xml out samples/out
	rm -rf .tox build dist src/clickgen.egg-info .mypy_cache .pytest_cache .coverage htmlcov .python-version
	rm -rf src/clickgen/__pycache__ tests/__pycache__
	make -C docs clean
	$(py3) -m pip uninstall -y clickgen

install_deps:
	$(py3) -m pip install -r requirements.txt
	$(py3) -m pip install -r requirements.dev.txt
	$(py3) -m pip install -r docs/requirements.txt

install:
	$(py3) -m pip install -e .

test:
	pytest

coverage:
	pytest --cov=clickgen --cov-report=html

build: clean
	$(py3) setup.py sdist bdist_wheel

stubgen:
	find src/clickgen/ -type f -name '*.pyi' -delete
	stubgen "src/clickgen" -o src

docsgen: build install
	make -C docs html

tox: build install
	pyenv local 3.7.5 3.8.12 3.9.10 3.10.2
	tox

dev: clean install_deps stubgen install test coverage docsgen
