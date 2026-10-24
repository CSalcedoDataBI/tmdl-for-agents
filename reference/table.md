---
type: Table
properties:
  - Name
  - Description
  - IsHidden
  - IsPrivate
  - DataCategory
  - LineageTag
  - ExcludeFromModelRefresh
  - ShowAsVariationsOnly
  - Columns
  - Measures
  - Partitions
  - Hierarchies
---

# Table

A table in the model: a set of columns, the partitions that load its rows, and the measures and
hierarchies defined on it. In TMDL a `table` block holds those as child blocks. TOM type: `Table`.

## Properties

| TMDL keyword | TOM name | What it is | Gotcha |
|---|---|---|---|
| `description` | `Description` | documentation string | — |
| `isHidden` | `IsHidden` | hide the whole table from the field list | — |
| `isPrivate` | `IsPrivate` | hide from client tools entirely (used for helper tables) | stronger than `isHidden` |
| `dataCategory` | `DataCategory` | semantic role, e.g. `Time` for a date table | marking a date table enables time intelligence |
| `excludeFromModelRefresh` | `ExcludeFromModelRefresh` | skip this table on refresh | — |
| `showAsVariationsOnly` | `ShowAsVariationsOnly` | surface the table only through variations | rare; date tables |
| `lineageTag` | `LineageTag` | stable GUID | keep it |

Child collections (not scalar properties): `Columns`, `Measures`, `Partitions`, `Hierarchies` —
written as nested `column`, `measure`, `partition` and `hierarchy` blocks.

## Example

```tmdl
table Sales
	lineageTag: 7c1e9b44-2a10-4d8e-9b3f-1e5c2a0f6d81

	column 'Order Date'
		dataType: dateTime
		sourceColumn: OrderDate
		summarizeBy: none

	measure 'Order Count' = COUNTROWS ( Sales )
		formatString: "#,0"

	partition Sales = m
		mode: import
		source = // Power Query (M) expression lives here
```
