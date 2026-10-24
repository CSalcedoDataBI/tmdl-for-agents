"""Repository checks that run in CI (the required `Validate` check).

- The catalogue (exports/tmdl-tom.catalog.json) keeps its shape: a list of {type, properties},
  and its headline counts (objectTypes, propertyNamesTotal) match the data.
- Every skills/*/SKILL.md opens with frontmatter that has `name` (matching its folder) and
  `description`.
- Every workflow job sets `timeout-minutes` and runs on `ubuntu-latest`, and every workflow
  declares `concurrency` (Actions cost rules).
- No name outside the catalogue. In what an agent reads (the reference cards under reference/ and
  any skills/**/*.md):
    * each card's frontmatter `type` must be a catalogue object type, and every name in its
      `properties:` list must be a property of that type;
    * every property keyword in a fenced ```tmdl example must be a catalogue property name
      (compared case-insensitively, since TMDL writes TOM's PascalCase names lowercase-first).
  "No invented name", for TMDL.

Standard library only, so CI needs no install step. Exit code 1 lists every failure.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CATALOG_PATH = ROOT / "exports" / "tmdl-tom.catalog.json"

# A fenced block whose info string is `tmdl`, capturing the body.
TMDL_FENCE = re.compile(r"^```tmdl\s*\n(.*?)^```", re.M | re.S)
# A TMDL property-assignment line: indented `keyword: value` or a boolean shorthand `keyword`.
# A declaration line (`measure 'X' = ...`, `column Amount`) has the keyword followed by a name,
# so it never matches and is correctly skipped.
TMDL_PROP_LINE = re.compile(r"^[ \t]+([a-z][A-Za-z0-9]*)(?::|[ \t]*$)")


def tmdl_keywords(body: str) -> list[str]:
    """The property keywords in a ```tmdl block.

    A line ending in `=` opens a multi-line DAX / M expression (`measure X =`, `source =`); its
    more-indented body is skipped, so expression tokens (`let`, `in`, `RETURN`) are never read as
    property keywords. A single-line expression (`measure X = SUM(...)`) does not open a block, so
    the properties that follow it are checked.
    """
    out: list[str] = []
    expr_indent: int | None = None
    for raw in body.splitlines():
        if not raw.strip():
            continue
        indent = len(raw) - len(raw.lstrip())
        if expr_indent is not None:
            if indent > expr_indent:
                continue  # inside the expression body
            expr_indent = None  # back to the object's level; re-examine this line
        if raw.rstrip().endswith("="):
            expr_indent = indent
            continue
        m = TMDL_PROP_LINE.match(raw)
        if m:
            out.append(m.group(1))
    return out


def load_catalog(path: Path = CATALOG_PATH) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    entries = data.get("catalog", [])
    type_props = {e["type"]: set(e.get("properties", [])) for e in entries}
    all_props = set().union(*type_props.values()) if type_props else set()
    return {
        "raw": data,
        "entries": entries,
        "types": set(type_props),
        "type_props": type_props,
        "all_props": all_props,
        "all_props_ci": {p.lower() for p in all_props},
    }


# --- catalogue shape (a protected contract the check and the cards depend on) ----------------

def check_catalog_shape(cat: dict) -> list[str]:
    errors: list[str] = []
    data = cat["raw"]
    if not cat["entries"]:
        return ["exports/tmdl-tom.catalog.json: empty or missing `catalog` list"]
    for i, e in enumerate(cat["entries"]):
        if not isinstance(e.get("type"), str):
            errors.append(f"catalog[{i}]: `type` is missing or not a string")
        if not isinstance(e.get("properties"), list):
            errors.append(f"catalog entry '{e.get('type', i)}': `properties` is not a list")
    declared_types = data.get("objectTypes")
    if declared_types is not None and declared_types != len(cat["entries"]):
        errors.append(
            f"objectTypes says {declared_types} but the catalogue has {len(cat['entries'])} entries")
    declared_props = data.get("propertyNamesTotal")
    if declared_props is not None and declared_props != len(cat["all_props"]):
        errors.append(
            f"propertyNamesTotal says {declared_props} but there are {len(cat['all_props'])} "
            "unique property names")
    return errors


# --- repo-shape checks (skills, workflows) --------------------------------------------------

def check_skills() -> list[str]:
    errors = []
    for skill in sorted((ROOT / "skills").glob("*/SKILL.md")):
        text = skill.read_text(encoding="utf-8")
        match = re.match(r"^---\n(.*?)\n---\n", text, re.S)
        rel = skill.relative_to(ROOT).as_posix()
        if not match:
            errors.append(f"{rel}: missing frontmatter")
            continue
        fields = dict(
            line.split(":", 1) for line in match.group(1).splitlines()
            if ":" in line and not line.startswith(" ")
        )
        name = fields.get("name", "").strip()
        if name != skill.parent.name:
            errors.append(f"{rel}: name '{name}' does not match folder '{skill.parent.name}'")
        if not fields.get("description", "").strip():
            errors.append(f"{rel}: empty description")
    return errors


def check_workflows() -> list[str]:
    errors = []
    for wf in sorted((ROOT / ".github" / "workflows").glob("*.y*ml")):
        text = wf.read_text(encoding="utf-8")
        rel = wf.relative_to(ROOT).as_posix()
        if not re.search(r"^concurrency:", text, re.M):
            errors.append(f"{rel}: no top-level concurrency")
        jobs = len(re.findall(r"^\s+runs-on:", text, re.M))
        timeouts = len(re.findall(r"^\s+timeout-minutes:", text, re.M))
        if timeouts < jobs:
            errors.append(f"{rel}: {jobs} jobs but {timeouts} timeout-minutes")
        for runner in re.findall(r"^\s+runs-on:\s*(.+)$", text, re.M):
            if runner.strip() != "ubuntu-latest":
                errors.append(f"{rel}: runs-on {runner.strip()} (no self-hosted on a public repo)")
    return errors


# --- the name check -------------------------------------------------------------------------

def parse_frontmatter(text: str) -> dict | None:
    """Minimal YAML frontmatter: scalar `key: value` and a `properties:` list of `- item` lines."""
    match = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not match:
        return None
    fields: dict[str, object] = {}
    lines = match.group(1).splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        m = re.match(r"^([A-Za-z0-9_]+):\s*(.*)$", line)
        if m:
            key, value = m.group(1), m.group(2).strip()
            if value == "":
                items = []
                j = i + 1
                while j < len(lines) and re.match(r"^\s*-\s+", lines[j]):
                    items.append(re.sub(r"^\s*-\s+", "", lines[j]).strip())
                    j += 1
                fields[key] = items if items else ""
                i = j
                continue
            fields[key] = value
        i += 1
    return fields


def check_card(text: str, rel: str, cat: dict) -> list[str]:
    errors: list[str] = []
    fm = parse_frontmatter(text)
    if fm is None:
        return [f"{rel}: missing frontmatter (needs `type:` and `properties:`)"]
    obj_type = fm.get("type")
    if not isinstance(obj_type, str) or not obj_type:
        errors.append(f"{rel}: frontmatter has no `type`")
        obj_type = None
    elif obj_type not in cat["types"]:
        errors.append(f"{rel}: object type '{obj_type}' is not in the catalogue")
        obj_type = None
    props = fm.get("properties", [])
    if obj_type is not None and isinstance(props, list):
        allowed = cat["type_props"][obj_type]
        for p in props:
            if p not in allowed:
                errors.append(f"{rel}: property '{p}' is not on type '{obj_type}'")
    # Fenced ```tmdl examples: every property keyword must be a catalogue name.
    for i, body in enumerate(TMDL_FENCE.findall(text), 1):
        for kw in tmdl_keywords(body):
            if kw.lower() not in cat["all_props_ci"]:
                errors.append(
                    f"{rel} (tmdl block #{i}): property keyword '{kw}' is not in the catalogue")
    return errors


def check_names(cat: dict, root: Path = ROOT) -> list[str]:
    errors: list[str] = []
    card_files = [p for p in sorted((root / "reference").glob("**/*.md"))
                  if p.name.lower() != "readme.md"]
    skill_md = sorted((root / "skills").glob("**/*.md"))
    for md in card_files:
        rel = md.relative_to(root).as_posix()
        errors += check_card(md.read_text(encoding="utf-8"), rel, cat)
    # Skills cards only need their tmdl examples checked, not the type/properties frontmatter.
    for md in skill_md:
        rel = md.relative_to(root).as_posix()
        text = md.read_text(encoding="utf-8")
        for i, body in enumerate(TMDL_FENCE.findall(text), 1):
            for kw in tmdl_keywords(body):
                if kw.lower() not in cat["all_props_ci"]:
                    errors.append(
                        f"{rel} (tmdl block #{i}): property keyword '{kw}' "
                        "is not in the catalogue")
    return errors


def main() -> int:
    cat = load_catalog()
    errors = (check_catalog_shape(cat) + check_skills() + check_workflows()
              + check_names(cat))
    for error in errors:
        print(f"FAIL {error}")
    if not errors:
        print("OK repo checks")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
