clean:
	rm -rf .vscode .vim venv 	
	# remove build & test cache files
	rm -rf build dist clickgen.egg-info .mypy_cache .pytest_cache
	rm -rf clickgen/__pycache__ tests/__pycache__
	cd xcursorgen && make clean
	cd docs && make clean
	python3 -m pip uninstall -y clickgen


MODULES = __init__ builders core db packagers util
stubgen:
	rm -rf clickgen/*.pyi
	$(foreach module,$(MODULES), stubgen "clickgen/$(module).py" -o .;)

test:
	python3 -m pytest -s -vv --cache-clear

setup_install:
	python3 setup.py install --user

pip_install:
	python3 -m pip install -e .

build: clean
	python3 setup.py install --user sdist bdist_wheel 

docs_gen:
	cd docs && make html

dev: clean stubgen setup_install pip_install test docs_gen
