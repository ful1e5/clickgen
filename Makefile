py3 = python3

clean:
	rm -rf .vscode .vim venv
	rm -rf .tox build dist src/clickgen.egg-info .mypy_cache .pytest_cache .coverage htmlcov .python-version
	rm -rf src/clickgen/__pycache__ tests/__pycache__
	make -C src/xcursorgen clean
	make -C docs clean
	$(py3) -m pip uninstall -y clickgen

install_requirements:
	$(py3) -m pip install -r requirements.txt

install_dev_requirements:
	$(py3) -m pip install -r requirements.dev.txt

install:
	sudo $(py3) -m pip install --user -e .

test:
	$(py3) -m pytest

coverage:
	$(py3) -m coverage run -m pytest
	coverage html

xcursorgen.so:
	@make -C src/xcursorgen

build: clean xcursorgen.so
	$(py3) setup.py sdist bdist_wheel

MODULES = __init__ builders core db packagers util
stubgen:
	rm -rf src/clickgen/*.pyi
	$(foreach module,$(MODULES), stubgen "src/clickgen/$(module).py" -o src;)

docsgen: build install
	make -C docs html

dev: clean install_requirements install_dev_requirements stubgen install xcursorgen.so test coverage docsgen
