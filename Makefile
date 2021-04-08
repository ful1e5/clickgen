clean:
		@rm -rf .vscode .vim venv .pytest_cache build dist 
		@cd xcursorgen && make clean

