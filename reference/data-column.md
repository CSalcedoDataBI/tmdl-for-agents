---
type: DataColumn
properties:
  - Name
  - SourceColumn
  - DataType
  - FormatString
  - SummarizeBy
  - SortByColumn
  - DisplayFolder
  - Description
  - IsHidden
  - IsKey
  - DataCategory
  - LineageTag
---

# Column (sourced) — DataColumn

A column whose values come from the partition's source query (import or DirectQuery), not from a
DAX expression. In TMDL it is a `column <name>` block with a `sourceColumn`. TOM type: `DataColumn`.
For a column defined by DAX, see [calculated-column.md](calculated-column.md).

## Properties

| TMDL keyword | TOM name | What it is | Gotcha |
|---|---|---|---|
| `sourceColumn` | `SourceColumn` | the column name in the source query | required for a sourced column; this is what makes it a `DataColumn` |
| `dataType` | `DataType` | `int64`, `double`, `decimal`, `string`, `dateTime`, `boolean`, … | — |
| `formatString` | `FormatString` | display format | — |
| `summarizeBy` | `SummarizeBy` | default aggregation (`sum`, `none`, `count`, …) | set to `none` for keys and codes to stop implicit sums |
| `sortByColumn` | `SortByColumn` | another column that defines the sort order | e.g. a month name sorted by a month number |
| `displayFolder` | `DisplayFolder` | field-list folder | — |
| `isHidden` | `IsHidden` | hide from the field list | hide surrogate keys |
| `isKey` | `IsKey` | marks the column as the table's key | — |
| `dataCategory` | `DataCategory` | semantic role, e.g. `WebUrl`, `Latitude` | — |
| `lineageTag` | `LineageTag` | stable GUID | keep it |

## Example

```tmdl
column 'Customer Key'
	dataType: int64
	sourceColumn: CustomerKey
	summarizeBy: none
	isHidden: true
	isKey: true
	lineageTag: b2d4f6a8-1357-4e9a-ac0b-2d4f6a8c0e12
```
