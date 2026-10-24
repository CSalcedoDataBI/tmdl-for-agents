# tmdl-for-agents

**Pre-release.** A TMDL reference for AI agents: the catalogue of object types and property
names comes straight from the Tabular Object Model (TOM) — the source of truth — so an agent that
writes a Power BI / Analysis Services semantic model as code (TMDL) never invents a property.

TMDL (Tabular Model Definition Language) is the text format for tabular semantic models. Each
object in a model (a table, a column, a measure, a relationship…) maps to a type in TOM, and each
line of a TMDL object sets one of that type's properties. A model fails to deserialize if it names
a property the type does not have. This repository lists every real name so that does not happen.

## What is in here

- [`exports/tmdl-tom.catalog.json`](exports/tmdl-tom.catalog.json) — the catalogue: **54 object
  types** and **220 unique property names**, extracted by reflection over
  `Microsoft.AnalysisServices.Tabular` (TOM). It is the source of truth for every name in this repo.
- [`reference/`](reference/) — reference cards for the most-used object types (Table, Measure,
  Column, Relationship, Hierarchy, Partition, Model…). Each card names only types and properties
  that are in the catalogue; the `Validate` check fails otherwise.

## The names are TOM names

The catalogue holds TOM **class and property names**, in PascalCase (`FormatString`, `DisplayFolder`,
`IsHidden`). In a TMDL file the same property is written as a lowercase-first keyword
(`formatString`, `displayFolder`, `isHidden`). Each reference card gives both spellings. The
catalogue is the authority on *which* names exist; TMDL decides how they are cased on the page.

## Why it exists

A model author working through an agent is one hallucinated property away from a file that will not
open. Grounding the agent in the real TOM surface — not the model's memory — removes that whole
class of error. This is the same idea as its sibling references
`dax-for-agents`, `powerquery-m-for-agents` and `spark-for-agents`.

## License

[MIT](LICENSE).
