.PHONY: clean clean-test clean-pyc clean-build format test help docs
.DEFAULT_GOAL := help

define BROWSER_PYSCRIPT
import os, webbrowser, sys

from urllib.request import pathname2url

webbrowser.open("file://" + pathname2url(os.path.abspath(sys.argv[1])))
endef
export BROWSER_PYSCRIPT

define PRINT_HELP_PYSCRIPT
import re, sys

for line in sys.stdin:
	match = re.match(r'^([a-zA-Z_-]+):.*?## (.*)$$', line)
	if match:
		target, help = match.groups()
		print("%-20s %s" % (target, help))
endef
export PRINT_HELP_PYSCRIPT

BROWSER := poetry run python -c "$$BROWSER_PYSCRIPT"

help:
	@python -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)

coverage: ## check code coverage
	poetry run coverage run --source cyberutils -m pytest
	poetry run coverage report -m
	poetry run coverage html
	# $(BROWSER) htmlcov/index.html

clean: clean-build clean-pyc clean-test ## remove all build, test, coverage and Python artifacts

clean-build: ## remove build artifacts
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +

clean-pyc: ## remove Python file artifacts
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-test: ## remove test and coverage artifacts
	rm -fr .tox/
	rm -f .coverage
	rm -fr htmlcov/
	rm -fr .pytest_cache

test: ## runs tests
	poetry run pytest --cov=cyberutils

qa: ## runs static analysis with mypy and flake8
	poetry run flake8 cyberutils
	poetry run mypy -p cyberutils

format: ## runs code style and formatter
	poetry run isort .
	poetry run black .

docs: ## build the documentation
	poetry run sphinx-build docs/ docs/_build/html
	# $(BROWSER) docs/_build/html/index.html

dev-docs:
	poetry run sphinx-autobuild docs/ docs/_build/html

release: clean qa test format ## build dist version and release to pypi
	poetry build
	poetry publish
