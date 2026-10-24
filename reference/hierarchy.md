---
type: Hierarchy
properties:
  - Name
  - Description
  - DisplayFolder
  - HideMembers
  - IsHidden
  - Levels
  - LineageTag
---

# Hierarchy

An ordered set of levels on a table (for example Year → Quarter → Month). In TMDL it is a
`hierarchy <name>` block inside a `table`, with one `level` per level. TOM type: `Hierarchy`.

## Properties

| TMDL keyword | TOM name | What it is | Gotcha |
|---|---|---|---|
| `description` | `Description` | documentation string | — |
| `displayFolder` | `DisplayFolder` | field-list folder | — |
| `hideMembers` | `HideMembers` | whether to hide blank members (`hideBlankMembers`) | useful for ragged hierarchies |
| `isHidden` | `IsHidden` | hide the hierarchy | — |
| `lineageTag` | `LineageTag` | stable GUID | keep it |

`Levels` is a child collection: each level is a `level <name>` block whose `column` points at the
column that supplies that level.

## Example

```tmdl
hierarchy Calendar
	displayFolder: Dates
	hideMembers: hideBlankMembers
	lineageTag: c3e5a7b9-1d2f-4830-9a1b-c3e5a7b91d2f

	level Year
		column: Year

	level Month
		column: 'Month Name'
```
