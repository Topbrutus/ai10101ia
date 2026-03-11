PYTHON ?= python3
PIP ?= pip3

install:
	$(PIP) install -r requirements.txt

validate:
	$(PYTHON) scripts/validate_todo_registry.py --check-master
	$(PYTHON) scripts/sync_checklist.py --mode check

test:
	PYTHONPATH=src $(PYTHON) -m pytest -q

sync-check:
	$(PYTHON) scripts/sync_checklist.py --mode check

sync-write:
	$(PYTHON) scripts/sync_checklist.py --mode write

zip:
	$(PYTHON) scripts/build_foundation_zip.py
