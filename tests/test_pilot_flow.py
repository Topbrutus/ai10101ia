"""
Tests de validation métier et flux pilote AI10101IA.
Couvre T0029 (bootstrap), T0030 (validation), T0031 (CLI), T0032 (audit), T0033 (flux).
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

ENTITIES_PATH = ROOT / "project" / "bootstrap_entities.yaml"
PROOFS_PATH = ROOT / "project" / "bootstrap_proofs.yaml"
EVENTS_PATH = ROOT / "project" / "bootstrap_events.yaml"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def load_yaml(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def run_script(script_name: str, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(ROOT / "scripts" / script_name), *args],
        capture_output=True,
        text=True,
    )


# ---------------------------------------------------------------------------
# T0029 — Dataset bootstrap
# ---------------------------------------------------------------------------

class TestBootstrapDataset:
    """Tests du dataset bootstrap canonique (T0029)."""

    def test_entities_file_exists(self) -> None:
        assert ENTITIES_PATH.exists(), f"Fichier manquant : {ENTITIES_PATH}"

    def test_proofs_file_exists(self) -> None:
        assert PROOFS_PATH.exists(), f"Fichier manquant : {PROOFS_PATH}"

    def test_events_file_exists(self) -> None:
        assert EVENTS_PATH.exists(), f"Fichier manquant : {EVENTS_PATH}"

    def test_entities_hub_present(self) -> None:
        data = load_yaml(ENTITIES_PATH)
        hub = data.get("hub")
        assert hub is not None, "Section 'hub' absente."
        assert hub.get("id"), "Hub sans 'id'."

    def test_entities_has_dieux(self) -> None:
        data = load_yaml(ENTITIES_PATH)
        dieux = data.get("dieux", [])
        assert len(dieux) >= 1, "Au moins un dieu attendu."

    def test_entities_has_robots(self) -> None:
        data = load_yaml(ENTITIES_PATH)
        robots = data.get("robots", [])
        assert len(robots) >= 2, "Au moins deux robots attendus."

    def test_entities_has_academies(self) -> None:
        data = load_yaml(ENTITIES_PATH)
        academies = data.get("academies", [])
        assert len(academies) >= 1, "Au moins une académie attendue."

    def test_entities_has_lignees(self) -> None:
        data = load_yaml(ENTITIES_PATH)
        lignees = data.get("lignees", [])
        assert len(lignees) >= 1, "Au moins une lignée attendue."

    def test_entities_robot_scores_positive(self) -> None:
        data = load_yaml(ENTITIES_PATH)
        for robot in data.get("robots", []):
            scores = robot.get("scores", {})
            for champ in ("points", "prestige", "credit_social"):
                val = scores.get(champ)
                assert val is not None, f"Robot {robot.get('id')}: score '{champ}' absent."
                assert isinstance(val, (int, float)) and val >= 0, (
                    f"Robot {robot.get('id')}: score '{champ}' invalide ({val})."
                )

    def test_entities_robot_lineage_references_valid(self) -> None:
        data = load_yaml(ENTITIES_PATH)
        lignee_ids = {l["id"] for l in data.get("lignees", []) if l.get("id")}
        for robot in data.get("robots", []):
            lignee_id = robot.get("lignee_id")
            if lignee_id:
                assert lignee_id in lignee_ids, (
                    f"Robot {robot.get('id')}: lignee_id '{lignee_id}' introuvable."
                )

    def test_entities_robot_academie_references_valid(self) -> None:
        data = load_yaml(ENTITIES_PATH)
        academie_ids = {a["id"] for a in data.get("academies", []) if a.get("id")}
        for robot in data.get("robots", []):
            academie_id = robot.get("academie_id")
            if academie_id:
                assert academie_id in academie_ids, (
                    f"Robot {robot.get('id')}: academie_id '{academie_id}' introuvable."
                )

    def test_entities_filiation_parent_exists(self) -> None:
        data = load_yaml(ENTITIES_PATH)
        robot_ids = {r["id"] for r in data.get("robots", []) if r.get("id")}
        for robot in data.get("robots", []):
            for rel in robot.get("relations", []):
                if rel.get("type") == "descendant_de":
                    parent_id = rel.get("cible")
                    assert parent_id in robot_ids, (
                        f"Robot {robot.get('id')}: parent '{parent_id}' introuvable."
                    )

    def test_proofs_have_required_fields(self) -> None:
        data = load_yaml(PROOFS_PATH)
        preuves = data.get("preuves", [])
        assert len(preuves) >= 1, "Au moins une preuve attendue."
        for preuve in preuves:
            assert preuve.get("id"), "Preuve sans 'id'."
            assert preuve.get("type_preuve"), f"Preuve {preuve.get('id')}: 'type_preuve' absent."
            assert preuve.get("date_preuve"), f"Preuve {preuve.get('id')}: 'date_preuve' absent."
            assert preuve.get("auteur"), f"Preuve {preuve.get('id')}: 'auteur' absent."

    def test_events_have_required_fields(self) -> None:
        data = load_yaml(EVENTS_PATH)
        evenements = data.get("evenements", [])
        assert len(evenements) >= 1, "Au moins un événement attendu."
        for evt in evenements:
            assert evt.get("id"), "Événement sans 'id'."
            assert evt.get("type"), f"Événement {evt.get('id')}: 'type' absent."
            assert evt.get("date"), f"Événement {evt.get('id')}: 'date' absente."


# ---------------------------------------------------------------------------
# T0030 — Pipeline de validation métier
# ---------------------------------------------------------------------------

class TestValidateDomainAssets:
    """Tests du pipeline de validation métier (T0030)."""

    def test_script_exists(self) -> None:
        assert (ROOT / "scripts" / "validate_domain_assets.py").exists()

    def test_validation_passes_on_bootstrap(self) -> None:
        result = run_script("validate_domain_assets.py")
        assert result.returncode == 0, (
            f"Validation échouée :\n{result.stderr}"
        )

    def test_validation_detects_invalid_score(self, tmp_path: Path) -> None:
        data = load_yaml(ENTITIES_PATH)
        # Corrompre un score
        data["robots"][0]["scores"]["points"] = -1
        bad_entities = tmp_path / "bad_entities.yaml"
        bad_entities.write_text(
            yaml.dump(data, allow_unicode=True, sort_keys=False),
            encoding="utf-8",
        )
        result = run_script(
            "validate_domain_assets.py",
            "--entities", str(bad_entities),
        )
        assert result.returncode == 1
        assert "score" in result.stderr.lower() or "invalide" in result.stderr.lower()

    def test_validation_detects_missing_lineage(self, tmp_path: Path) -> None:
        data = load_yaml(ENTITIES_PATH)
        data["robots"][0]["lignee_id"] = "LIGNEE-999"
        bad_entities = tmp_path / "bad_entities2.yaml"
        bad_entities.write_text(
            yaml.dump(data, allow_unicode=True, sort_keys=False),
            encoding="utf-8",
        )
        result = run_script(
            "validate_domain_assets.py",
            "--entities", str(bad_entities),
        )
        assert result.returncode == 1
        assert "lignee" in result.stderr.lower() or "introuvable" in result.stderr.lower()


# ---------------------------------------------------------------------------
# T0031 — CLI de pilotage
# ---------------------------------------------------------------------------

class TestRegistryCLI:
    """Tests de la CLI de pilotage (T0031)."""

    def test_script_exists(self) -> None:
        assert (ROOT / "scripts" / "run_registry_cli.py").exists()

    def test_cli_load(self) -> None:
        result = run_script("run_registry_cli.py", "load")
        assert result.returncode == 0, result.stderr
        assert "OK" in result.stdout

    def test_cli_validate(self) -> None:
        result = run_script("run_registry_cli.py", "validate")
        assert result.returncode == 0, result.stderr

    def test_cli_show_robot(self) -> None:
        result = run_script("run_registry_cli.py", "show", "ROBOT-0001")
        assert result.returncode == 0, result.stderr
        assert "ROBOT-0001" in result.stdout

    def test_cli_show_unknown_entity(self) -> None:
        result = run_script("run_registry_cli.py", "show", "ROBOT-9999")
        assert result.returncode == 1
        assert "introuvable" in result.stderr.lower()

    def test_cli_list_robots(self) -> None:
        result = run_script("run_registry_cli.py", "list", "ROBOT")
        assert result.returncode == 0, result.stderr
        assert "ROBOT" in result.stdout

    def test_cli_list_unknown_type(self) -> None:
        result = run_script("run_registry_cli.py", "list", "INCONNU")
        assert result.returncode == 1

    def test_cli_index(self) -> None:
        result = run_script("run_registry_cli.py", "index")
        assert result.returncode == 0, result.stderr
        assert "index" in result.stdout.lower()


# ---------------------------------------------------------------------------
# T0032 — Vues d'audit lisibles
# ---------------------------------------------------------------------------

class TestBuildAuditReport:
    """Tests du générateur de rapport d'audit (T0032)."""

    def test_script_exists(self) -> None:
        assert (ROOT / "scripts" / "build_audit_report.py").exists()

    def test_markdown_report_generated(self, tmp_path: Path) -> None:
        out_file = tmp_path / "audit.md"
        result = run_script(
            "build_audit_report.py",
            "--format", "markdown",
            "--output", str(out_file),
        )
        assert result.returncode == 0, result.stderr
        assert out_file.exists()
        content = out_file.read_text(encoding="utf-8")
        assert "# Rapport d'audit" in content

    def test_json_report_generated(self, tmp_path: Path) -> None:
        out_file = tmp_path / "audit.json"
        result = run_script(
            "build_audit_report.py",
            "--format", "json",
            "--output", str(out_file),
        )
        assert result.returncode == 0, result.stderr
        assert out_file.exists()
        data = json.loads(out_file.read_text(encoding="utf-8"))
        assert "synthese" in data
        assert "filiation" in data
        assert "preuves_par_entite" in data
        assert "incoherences" in data
        assert data["statut"] == "OK"

    def test_report_has_no_incoherences_on_clean_bootstrap(self, tmp_path: Path) -> None:
        out_file = tmp_path / "audit_clean.json"
        result = run_script(
            "build_audit_report.py",
            "--format", "json",
            "--output", str(out_file),
        )
        assert result.returncode == 0, result.stderr
        data = json.loads(out_file.read_text(encoding="utf-8"))
        assert data["incoherences"] == [], (
            f"Incohérences inattendues : {data['incoherences']}"
        )

    def test_report_contains_filiation(self, tmp_path: Path) -> None:
        out_file = tmp_path / "audit_filiation.json"
        run_script("build_audit_report.py", "--format", "json", "--output", str(out_file))
        data = json.loads(out_file.read_text(encoding="utf-8"))
        # ROBOT-0002 est descendant de ROBOT-0001
        filiation = data.get("filiation", [])
        assert any(
            r["enfant"] == "ROBOT-0002" and r["parent"] == "ROBOT-0001"
            for r in filiation
        ), f"Relation de filiation ROBOT-0002→ROBOT-0001 introuvable : {filiation}"


# ---------------------------------------------------------------------------
# T0033 — Flux bout-en-bout pilote
# ---------------------------------------------------------------------------

class TestPilotFlow:
    """Tests du flux bout-en-bout pilote (T0033)."""

    def test_script_exists(self) -> None:
        assert (ROOT / "scripts" / "run_pilot_flow.py").exists()

    def test_pilot_flow_succeeds(self) -> None:
        result = run_script("run_pilot_flow.py")
        assert result.returncode == 0, (
            f"Flux pilote échoué :\nstdout:\n{result.stdout}\nstderr:\n{result.stderr}"
        )
        assert "flux pilote réussi" in result.stdout.lower()

    def test_pilot_flow_with_audit_output(self, tmp_path: Path) -> None:
        audit_file = tmp_path / "pilot_audit.md"
        result = run_script("run_pilot_flow.py", "--audit-output", str(audit_file))
        assert result.returncode == 0, result.stderr
        assert audit_file.exists()
        content = audit_file.read_text(encoding="utf-8")
        assert "# Rapport d'audit" in content
