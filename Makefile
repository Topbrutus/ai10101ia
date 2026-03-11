PYTHON ?= python3
PIP ?= pip3

install:
	$(PIP) install -r requirements.txt

validate:
	$(PYTHON) scripts/validate_todo_registry.py --check-master
	$(PYTHON) scripts/sync_checklist.py --mode check

validate-domain:
	$(PYTHON) scripts/validate_domain_assets.py

test:
	PYTHONPATH=src $(PYTHON) -m pytest -q

sync-check:
	$(PYTHON) scripts/sync_checklist.py --mode check

sync-write:
	$(PYTHON) scripts/sync_checklist.py --mode write

audit:
	$(PYTHON) scripts/build_audit_report.py --output /tmp/audit_report.md
	@echo "Rapport d'audit écrit dans /tmp/audit_report.md"

pilot:
	$(PYTHON) scripts/run_pilot_flow.py

zip:
	$(PYTHON) scripts/build_foundation_zip.py
