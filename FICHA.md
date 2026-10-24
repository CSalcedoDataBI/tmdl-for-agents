# Ficha — tmdl-for-agents

> Ficha de esta herramienta. La lee su experto (`.claude/agents/experto.md`) en cada PR.
> Se mantiene con las reglas internas del mantenedor: su norte es `FICHA.md` y el agente `experto`
> fusiona contra ella. Cambiarla exige una nueva aprobación del mantenedor.

## Qué es

- **Qué construye y para quién:** la referencia de TMDL para agentes de IA. Un único catálogo
  —`exports/tmdl-tom.catalog.json`— con los 54 tipos de objeto del Tabular Object Model (TOM) y
  sus 220 nombres de propiedad únicos, **extraídos por reflexión sobre el ensamblado
  `Microsoft.AnalysisServices.Tabular`**, no de la memoria del modelo. Es para quien escribe un
  modelo semántico como código (TMDL) con un agente y necesita que no invente propiedades.
- **Papel** (`repo-roles`): tool (referencia pública de la familia `*-for-agents`).
- **Gemelo público/privado:** la capa de autoría y *craft* de Power BI (medidas, cross-filter,
  plantillas) vive aparte en una capa privada. Hermanos de familia públicos: `dax-for-agents`,
  `powerquery-m-for-agents`, `spark-for-agents`, `vega-for-agents`.

## Norte

- **Plan vigente:** [épica v0.1 — catálogo TOM y fichas de referencia](https://github.com/CSalcedoDataBI/tmdl-for-agents/issues/2)
- **Lo que esta herramienta NO es:**
  - No es la capa de autoría de Power BI: eso vive en una capa privada aparte.
  - No es un tutorial de TMDL: es una referencia que un agente consulta.
  - No lee, escribe ni despliega modelos: eso es TOM, Tabular Editor y las herramientas de Fabric.

## Zonas protegidas

Lo que no se toca sin un paso del plan que lo nombre:

- `exports/tmdl-tom.catalog.json`: lo regenera la reflexión sobre TOM, nunca una edición a mano. Un
  catálogo escrito a mano rompe la promesa de «ningún nombre inventado».
- El contrato de forma del catálogo (`catalog: [{ type, properties }]`, `source`,
  `assemblyVersion`): el check y las fichas dependen de él.
- `LICENSE` (MIT) y la visibilidad pública del repo.

## Capa y feedback

- **Capa de nodo:** la capa de modelo semántico (TMDL/TOM).
- **Skill de feedback:** `tmdl-feedback` (planeada en la v0.1).

## Check y experto

- **Check de CI requerido:** `Validate` (ruleset de `main`).
- **Suite de pruebas:** `python scripts/check_repo.py` y `python -m unittest discover -s tests`.
- **Runner:** GitHub (repo público).
- **Formato de tag:** `vX.Y.Z`, con release-please (`release-please-config.json`).
- **Experto:** `.claude/agents/experto.md`.
- **¿Plugin del directorio?:** todavía no. Se envía cuando salga de pre-release; desde entonces,
  `stable` no se toca y publicar es una decisión aparte del mantenedor.
- **Partes visibles que aprueba el mantenedor:** el README de cara al público, la salida de
  pre-release, y las cards/plugin cuando se promuevan.

## Aprobación

Aprobada: 2026-10-24 (docker-lab)
