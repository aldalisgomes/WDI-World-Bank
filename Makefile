.PHONY: setup run clean

setup:
	python3 -m venv venv
	venv/bin/pip install -r requirements.txt

run:
	venv/bin/python "src/Script WDI World Bank.py"

clean:
	rm -rf venv
	rm -rf __pycache__ .ipynb_checkpoints
	rm -rf resultados