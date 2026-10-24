# Reference cards

One card per TMDL object type, for the types an author writes most. Each card's frontmatter names
its catalogue `type` and the `properties` it documents; the `Validate` check fails if any name is
not in [`../exports/tmdl-tom.catalog.json`](../exports/tmdl-tom.catalog.json). The property tables
give both the TMDL keyword (lowercase-first, as written in a `.tmdl` file) and the TOM name (as the
catalogue lists it).

| Card | TOM type | TMDL keyword |
|---|---|---|
| [table.md](table.md) | `Table` | `table` |
| [measure.md](measure.md) | `Measure` | `measure` |
| [data-column.md](data-column.md) | `DataColumn` | `column` (sourced) |
| [calculated-column.md](calculated-column.md) | `CalculatedColumn` | `column` (`= <DAX>`) |
| [relationship.md](relationship.md) | `SingleColumnRelationship` | `relationship` |
| [hierarchy.md](hierarchy.md) | `Hierarchy` | `hierarchy` |
| [partition.md](partition.md) | `Partition` | `partition` |
| [model.md](model.md) | `Model` | `model` |

These cover the common object types; the catalogue has all 54. A property not listed on a card may
still be valid — check the catalogue.
