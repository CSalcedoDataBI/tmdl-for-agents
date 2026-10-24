---
type: Partition
properties:
  - Name
  - Mode
  - Source
  - SourceType
  - Description
  - DataView
  - QueryGroup
---

# Partition

A partition supplies a table's rows from a source query. A table has one partition for a simple
import, or several for incremental refresh. In TMDL it is a `partition <name> = <sourceType>` block
inside a `table`. TOM type: `Partition`.

## Properties

| TMDL keyword | TOM name | What it is | Gotcha |
|---|---|---|---|
| (after `=`) | `SourceType` | the kind of source: `m` (Power Query), `calculated` (DAX), `query`, `entity` | declared on the `partition` line, e.g. `partition Sales = m` |
| `source` | `Source` | the query itself — the M, DAX or SQL that returns the rows | a multi-line expression block |
| `mode` | `Mode` | storage mode: `import`, `directQuery`, `dual` | — |
| `description` | `Description` | documentation string | — |
| `dataView` | `DataView` | `full` / `sample` data view | — |
| `queryGroup` | `QueryGroup` | the Power Query group this partition belongs to | — |

## Example

```tmdl
partition Sales = m
	mode: import
	source =
			let
				Source = Sql.Database("server", "warehouse")
				Sales = Source{[Schema="dbo", Item="Sales"]}[Data]
			in
				Sales
```
