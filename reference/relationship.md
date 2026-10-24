---
type: SingleColumnRelationship
properties:
  - Name
  - FromColumn
  - ToColumn
  - FromCardinality
  - ToCardinality
  - CrossFilteringBehavior
  - IsActive
  - SecurityFilteringBehavior
  - RelyOnReferentialIntegrity
  - JoinOnDateBehavior
---

# Relationship — SingleColumnRelationship

A join between two tables on one column each. In TMDL it is a top-level `relationship <name>` block
inside the model, written once (not under a table). TOM type: `SingleColumnRelationship` — the
standard single-column relationship. The `relationship` keyword in TMDL maps to this type.

## Properties

| TMDL keyword | TOM name | What it is | Gotcha |
|---|---|---|---|
| `fromColumn` | `FromColumn` | the many-side column, as `Table.Column` | the "from" side is the fact/many side |
| `toColumn` | `ToColumn` | the one-side column, as `Table.Column` | — |
| `fromCardinality` | `FromCardinality` | `many` / `one` on the from side | usually `many` |
| `toCardinality` | `ToCardinality` | `many` / `one` on the to side | usually `one` |
| `crossFilteringBehavior` | `CrossFilteringBehavior` | `oneDirection` / `bothDirections` | both-directions filtering can create ambiguity |
| `isActive` | `IsActive` | whether the relationship is active | only one active path between two tables; inactive ones are used with `USERELATIONSHIP` |
| `securityFilteringBehavior` | `SecurityFilteringBehavior` | how RLS flows across the join | — |
| `relyOnReferentialIntegrity` | `RelyOnReferentialIntegrity` | allow inner-join optimization (DirectQuery) | only when integrity is guaranteed |
| `joinOnDateBehavior` | `JoinOnDateBehavior` | date/datetime join handling | — |

`Name` is the relationship's identifier (often a GUID). The `many`/`one` and direction values come
from TOM enumerations, not from this catalogue of property names.

## Example

```tmdl
relationship a1b2c3d4-e5f6-4071-8293-a4b5c6d7e8f9
	fromColumn: Sales.CustomerKey
	toColumn: Customer.CustomerKey
	fromCardinality: many
	toCardinality: one
	crossFilteringBehavior: oneDirection
	isActive: true
```
