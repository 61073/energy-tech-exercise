#
# Make file - for running various tasks

requirements:
	pip install -r requirements.txt
	touch $@

unittest: requirements
	@echo "\n=====> Running Unit Tests..."
	nose2 --pretty-assert

cov: requirements
	nose2 --coverage-report term --pretty-assert

covhtml: requirements
	nose2 --coverage-report html
	firefox htmlcov/index.html && \
	echo "\n=========> HTML coverage report created and opened in firefox"

start: requirements
	@echo "\n=====> Running Main Application..."
	PYTHONPATH=$(PYTHONPATH):src/app python main.py
