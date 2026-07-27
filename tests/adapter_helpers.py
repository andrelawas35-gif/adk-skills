"""Shared assertions for namespaced generated adapter contracts."""

from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent


def namespaced_core_body(core_file):
    body = core_file.read_text().split("---", 2)[2].lstrip("\n").rstrip("\n")
    names = sorted((path.name for path in (ROOT / "skills" / "core").iterdir()
                    if path.is_dir()), key=len, reverse=True)
    for name in names:
        public_name = f"alawas-{name}"
        body = body.replace(f"`{name}`", f"`{public_name}`")
        _, separator, legacy_name = name.partition("-")
        if separator:
            body = body.replace(f"`{legacy_name}`", f"`{public_name}`")
    return body
