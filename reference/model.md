---
type: Model
properties:
  - Name
  - Culture
  - Collation
  - DefaultMode
  - DefaultPowerBIDataSourceVersion
  - DiscourageImplicitMeasures
  - SourceQueryCulture
  - Description
---

# Model

The root object. Everything else — tables, relationships, roles, perspectives, cultures,
expressions — hangs off it. In TMDL the `model` block carries the model-wide settings; the children
usually live in their own files. TOM type: `Model`.

## Properties

| TMDL keyword | TOM name | What it is | Gotcha |
|---|---|---|---|
| `culture` | `Culture` | the model culture, e.g. `en-US` | drives default formatting and sorting |
| `collation` | `Collation` | string collation | — |
| `defaultMode` | `DefaultMode` | default storage mode for new tables | — |
| `defaultPowerBIDataSourceVersion` | `DefaultPowerBIDataSourceVersion` | the Power BI data-source version, e.g. `powerBI_V3` | — |
| `discourageImplicitMeasures` | `DiscourageImplicitMeasures` | block implicit (drag-a-column) measures | `true` in calculation-group models |
| `sourceQueryCulture` | `SourceQueryCulture` | culture used for source queries | — |
| `description` | `Description` | documentation string | — |

Child collections (not scalar properties): `Tables`, `Relationships`, `Roles`, `Perspectives`,
`Cultures`, `Expressions`, `Functions`, `QueryGroups`.

## Example

```tmdl
model Model
	culture: en-US
	defaultPowerBIDataSourceVersion: powerBI_V3
	discourageImplicitMeasures: true
	sourceQueryCulture: en-US
```
