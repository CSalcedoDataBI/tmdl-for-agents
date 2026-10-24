---
type: CalculatedColumn
properties:
  - Name
  - Expression
  - DataType
  - FormatString
  - SummarizeBy
  - SortByColumn
  - DisplayFolder
  - Description
  - IsHidden
  - IsKey
  - LineageTag
---

# Calculated column — CalculatedColumn

A column whose values come from a DAX expression evaluated row by row at refresh time. In TMDL it
is a `column <name> = <DAX>` block — the `=` is what distinguishes it from a sourced column. TOM
type: `CalculatedColumn`. For a column from the source query, see [data-column.md](data-column.md).

## Properties

| TMDL keyword | TOM name | What it is | Gotcha |
|---|---|---|---|
| `=` (the expression) | `Expression` | the DAX, evaluated in row context | required; this makes it a `CalculatedColumn` rather than a `DataColumn` |
| `dataType` | `DataType` | the result type | usually inferred from the expression |
| `formatString` | `FormatString` | display format | — |
| `summarizeBy` | `SummarizeBy` | default aggregation | `none` for text or category columns |
| `sortByColumn` | `SortByColumn` | column that defines sort order | — |
| `displayFolder` | `DisplayFolder` | field-list folder | — |
| `isHidden` | `IsHidden` | hide from the field list | — |
| `isKey` | `IsKey` | marks it as the table key | — |
| `lineageTag` | `LineageTag` | stable GUID | keep it |

## Example

```tmdl
column 'Full Name' = Customer[First Name] & " " & Customer[Last Name]
	dataType: string
	summarizeBy: none
	displayFolder: Naming
	isHidden: false
	lineageTag: 9e7c5a30-8642-4b1f-90da-7c5a30864268
```
