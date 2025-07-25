"""Generate the code reference pages."""

from pathlib import Path

import mkdocs_gen_files

root = Path(__file__).parent.parent
src = root / "waveorder/scripts"  # (1)!

for path in sorted(src.rglob("*.py")):  # (2)!
    module_path = path.relative_to(src).with_suffix("")  # (3)!
    doc_path = path.relative_to(src).with_suffix(".md")  # (4)!
    full_doc_path = Path("reference", doc_path)  # (5)!

    parts = tuple(module_path.parts)

    if parts[-1] == "__init__":  # (6)!
        parts = parts[:-1]
    elif parts[-1] == "__main__":
        continue

    with mkdocs_gen_files.open(full_doc_path, "w") as fd:  # (7)!
        identifier = ".".join(parts)  # (8)!
        print("::: " + identifier, file=fd)  # (9)!

    mkdocs_gen_files.set_edit_path(full_doc_path, path.relative_to(root))  # (10)!
