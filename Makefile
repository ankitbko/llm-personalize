VENV = .venv
OS := $(shell uname)

ifneq (,$(findstring $(OS),Darwin Linux))
    PYTHON = $(VENV)/bin/python
else
    PYTHON = $(VENV)/Scripts/python
endif

venv:
	python -m venv $(VENV) 

print: 
	@echo $(OS)
	@echo $(PYTHON)

install: venv
	$(PYTHON) -m pip install -r requirements.txt

flake8:
	$(PYTHON) -m flake8 --max-line-length=120 --exclude=$(VENV)

lint: flake8

test:  
	$(PYTHON) -m pytest -v

run:
	$(PYTHON) -m streamlit run app.py

server:
	$(PYTHON) -m uvicorn api:app --reload