# Ficha — tmdl-for-agents

> Ficha de esta herramienta. La lee su experto (`.claude/agents/experto.md`) en cada PR.
> Se mantiene con las reglas del mantenedor. La aprueba el mantenedor (línea `Aprobada:`); cambiarla exige una nueva aprobación.

## Qué es

- **Qué construye y para quién:** una referencia de TMDL para agentes de IA. Es un catálogo de los tipos de objeto y nombres de propiedad del Tabular Object Model (TOM), extraído por reflexión del ensamblado `Microsoft.AnalysisServices.Tabular` (`exports/tmdl-tom.catalog.json`), más fichas de referencia de los tipos más usados (`reference/`). Es para quien escribe un modelo semántico de Power BI / Analysis Services como código (TMDL) con un agente y necesita que no invente propiedades.
- **Papel:** knowledge
- **Gemelo público/privado:** tiene un gemelo privado

## Norte

- **Plan vigente:** [épica v0.1 — catálogo TOM y fichas de referencia](https://github.com/CSalcedoDataBI/tmdl-for-agents/issues/2)
- **Lo que esta herramienta NO es:**
  - No es una capa de autoría de modelos ni de buenas prácticas de Power BI.
  - No es un tutorial de TMDL: es una referencia que consulta un agente.
  - No lee, escribe ni despliega modelos (eso es TOM, Tabular Editor o Fabric).
  - No es un catálogo escrito a mano: ningún nombre entra si no está en el catálogo extraído.
- **Pendiente:** el extractor que regenera el catálogo por reflexión sobre TOM queda fuera del repo por ahora; lo ejecuta el mantenedor. Si entra al repo, pasa a ser zona protegida.

## Zonas protegidas

Lo que no se toca sin un paso del plan que lo nombre:

- `exports/tmdl-tom.catalog.json`: solo se regenera por reflexión sobre TOM, nunca a mano. Un nombre escrito a mano rompe la promesa de «ningún nombre inventado».
- La forma del catálogo (`source`, `assemblyVersion`, `exportedAt`, `objectTypes`, `propertyNamesTotal`, `catalog: [{ type, properties }]`): de ella dependen `scripts/check_repo.py` y las fichas.
- `scripts/check_repo.py` y `tests/`: son el check `Validate`; debilitarlos abre la puerta a nombres inventados.
- `.github/workflows/`: solo runners de GitHub (`ubuntu-latest`), nunca uno propio, porque el repo es público.
- `LICENSE` (MIT) y la visibilidad pública del repo.

## Capa y feedback

- **Capa de nodo:** meaning
- **Skill de feedback:** ninguna

## Check y experto

- **Check de CI requerido:** `Validate`
- **Suite de pruebas:** `python scripts/check_repo.py` y `python -m unittest discover -s tests`
- **Runner:** GitHub (repo público)
- **Formato de tag:** `vX.Y.Z` (release-please, `.github/workflows/release-please.yml`, con `include-component-in-tag: false`)
- **Experto:** `.claude/agents/experto.md`
- **¿Plugin del directorio?:** no
- **Partes visibles que aprueba el mantenedor:** el README público, la salida de pre-release y la promoción de skills o de un plugin cuando existan.

## Aprobación

Aprobada: 2026-10-24 (mantenedor)
