.PHONY: install test help clean

install:
	pip install -e .
	pip install -r requirements.txt

test:
	pytest -q

help:
	research --help

clean:
	find . -type d -name "__pycache__" -prune -exec rm -rf {} +
	find . -name "*.pyc" -delete
	rm -rf build dist *.egg-info src/*.egg-info
