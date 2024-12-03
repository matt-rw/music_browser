# Variables



all: build run

venv:
	python3 -m venv $(VENV)

build: venv
	$(PIP) install --upgrade pip -r requirements.txt
	
clean:
	rm -rf $(VENV) 
