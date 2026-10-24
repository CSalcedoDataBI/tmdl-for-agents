# exports — the source of truth for the catalogue

`tmdl-tom.catalog.json`: the TMDL object types and property names, exported by reflection over the
`Microsoft.AnalysisServices.Tabular` (TOM) assembly, version 19.114.8 — not from a model's memory.
**54 object types, 220 unique property names.**

Each entry is one TOM object type and the property names it exposes:

```json
{
  "type": "Measure",
  "properties": ["Annotations", "DataType", "Description", "DisplayFolder", "Expression",
                 "FormatString", "IsHidden", "LineageTag", "Name", "..."]
}
```

The names are PascalCase TOM names. In TMDL the same property is written lowercase-first
(`FormatString` → `formatString`). See the repository README for the full explanation.

This file is regenerated from the assembly by the maintainer; it is **not edited by hand**. Every
name an agent reads elsewhere in the repo is validated against it by `scripts/check_repo.py`.
