---
type: Measure
properties:
  - Name
  - Expression
  - FormatString
  - FormatStringDefinition
  - DisplayFolder
  - Description
  - IsHidden
  - DataType
  - DetailRowsDefinition
  - KPI
  - LineageTag
---

# Measure

A DAX calculation that returns a scalar, evaluated in the filter context of the report. In TMDL a
measure lives inside a `table` block and is declared `measure <name> = <DAX>`. TOM type: `Measure`.

## Properties

| TMDL keyword | TOM name | What it is | Gotcha |
|---|---|---|---|
| `=` (the expression) | `Expression` | the DAX. Single-line after `=`, or multi-line indented below | required; a measure with no expression will not deserialize |
| `formatString` | `FormatString` | the display format, e.g. `"\$#,0"` | a format string, not a format name; `General Date` only applies to date values |
| `formatStringDefinition` | `FormatStringDefinition` | a DAX expression that returns the format string (dynamic format) | mutually exclusive in practice with a static `formatString` |
| `displayFolder` | `DisplayFolder` | the folder shown in the field list | use `\` to nest folders |
| `description` | `Description` | the tooltip / documentation string | — |
| `isHidden` | `IsHidden` | hide from the field list | `false` by default |
| `dataType` | `DataType` | the return type (`int64`, `double`, `decimal`, `string`, …) | usually inferred; set it only to pin it |
| `detailRowsDefinition` | `DetailRowsDefinition` | the DAX for drill-through detail rows | a child block, not a scalar |
| (child block) | `KPI` | the KPI (goal, status, trend) attached to the measure | a `kpi` child block |
| `lineageTag` | `LineageTag` | a stable GUID that survives renames | keep it; the report binds to it |

`Name` is the identifier in `measure <name>`. `FormatStringDefinition` and `KPI` are child blocks.

## Example

```tmdl
measure 'Total Sales' = SUMX ( Sales, Sales[Quantity] * Sales[Unit Price] )
	formatString: "\$#,0"
	displayFolder: Key Measures
	description: "Revenue across every line of every order."
	isHidden: false
	lineageTag: 3f9a1c20-0f2e-4a7b-8f0d-9c2b6a1e4d55
```
