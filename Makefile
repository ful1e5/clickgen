py3 = python3

clean:
	rm -rf .vscode .vim venv
	rm -rf build dist src/clickgen.egg-info .mypy_cache .pytest_cache
	rm -rf src/clickgen/__pycache__ tests/__pycache__
	make -C src/xcursorgen clean
	make -C docs clean
	$(py3) -m pip uninstall -y clickgen

MODULES = __init__ builders core db packagers util
stubgen:
	$(py3) -m pip install -U mypy
	rm -rf src/clickgen/*.pyi
	$(foreach module,$(MODULES), stubgen "src/clickgen/$(module).py" -o src;)

compile_xcursorgen:
	@make -C src/xcursorgen

test:
	$(py3) -m pip install -U pytest
	$(py3) -m pytest -s -vv --cache-clear

coverage:
	$(py3) -m pip install -U pytest-cov
	$(py3) -m coverage run -m pytest -s -vv --cache-clear
	coverage html

pip_install:
	$(py3) -m pip install -e .

build: clean
	$(py3) setup.py install --user sdist bdist_wheel

docs_gen:
	$(py3) -m pip install -U sphinx sphinx_rtd_theme
	cd docs && make html

dev: clean stubgen compile_xcursorgen pip_install coverage docs_gen
