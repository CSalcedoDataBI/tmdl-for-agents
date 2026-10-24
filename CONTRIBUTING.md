# Contributing

## Report a bug or a wrong card

Open an [issue](https://github.com/CSalcedoDataBI/tmdl-for-agents/issues/new). For a name that is
wrong or missing, include:

- the object type and property as the card describes them;
- what TOM / Power BI Desktop actually accepts (and the assembly version, if you know it);
- a minimal TMDL snippet and the error the model gave.

## Changes go through a pull request

Every change to `main` comes in through a pull request, and the required `Validate` check must pass
before it can merge. Run the same checks locally first:

```bash
python scripts/check_repo.py
python -m unittest discover -s tests
```

## No name outside the catalogue

The catalogue under `exports/` is extracted from the `Microsoft.AnalysisServices.Tabular` (TOM)
assembly, never typed by hand. Anything an agent reads may only name object types and properties
that are in it, and `Validate` fails otherwise. If a name is missing, the fix is a re-extraction
from a newer assembly, not a hand edit.

## License

By contributing, you agree that your contribution is licensed under the [MIT License](LICENSE).
