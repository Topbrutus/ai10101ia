from __future__ import annotations

from pathlib import Path
import zipfile

EXCLUDED_PARTS = {".git", ".pytest_cache", "__pycache__", ".mypy_cache"}
EXCLUDED_SUFFIXES = {".pyc", ".pyo", ".zip"}


def should_include(path: Path, root: Path) -> bool:
    relative = path.relative_to(root)
    if any(part in EXCLUDED_PARTS for part in relative.parts):
        return False
    if path.suffix in EXCLUDED_SUFFIXES:
        return False
    return True


def build_zip(root: str | Path, output_path: str | Path) -> Path:
    root_path = Path(root).resolve()
    output = Path(output_path).resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for file_path in sorted(root_path.rglob("*")):
            if file_path.is_file() and should_include(file_path, root_path):
                archive.write(file_path, file_path.relative_to(root_path).as_posix())
    return output
