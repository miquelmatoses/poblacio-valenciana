# poblacio-valenciana — CLAUDE.md

Dataset consolidat de població per municipi de la Comunitat Valenciana (1900–present), combinant censos històrics i padró municipal de l'INE.

## Estructura

- `raw/` — CSVs descarregats de l'API de l'INE, un per província i font (censos / padró). Sortida directa de `scripts/update_data.py`.
- `data/valencianpop.csv` — Dataset consolidat final (long format: municipi, any, població). Únic artefacte que han de consumir usuaris externs.
- `scripts/update_data.py` — Descàrrega + consolidació INE → `raw/` i `data/`.
- `scripts/generate_chart.py` — Genera `assets/bar_chart_race.gif`.
- `assets/` — Banner, icones, GIF de la visualització.
- `.github/workflows/update.yml` — Actualització automàtica cada 3 mesos (cron `0 8 1 */3 *`).

## Pipeline de dades

Font: API INE `https://servicios.ine.es/wstempus/js/ES/DATOS_TABLA/{id}`. Taules a `scripts/update_data.py`:

- **Padró (1996–present)**: 2856 (Alacant), 2865 (Castelló), 2903 (València)
- **Censos històrics (1900–1991)**: 3036 (Alacant), 3045 (Castelló), 3079 (València)

Refresc manual:

```bash
pip install -r scripts/requirements.txt
python scripts/update_data.py
python scripts/generate_chart.py
```

El workflow ho fa automàticament cada trimestre i fa commit només si hi ha canvis. L'INE publica el padró nou cap a finals d'any (data de referència 1 de gener), així que normalment només una de les execucions trimestrals porta dades noves.

## Convencions de dades

- Noms de municipi: **només en valencià** (no bilingüe, no prefixos INE).
- Accents valencians correctes (València, Castelló, Alacant, etc.).
- Sense totals provincials ni autonòmics — només municipis.
- València i Alacant capital han d'aparèixer en tots els anys (1900–present). Si es perden, revisar el filtre de `parse_padro` / `parse_censos`.

## Design System (mm-design)

README i visuals segueixen mm-design (https://github.com/miquelmatoses/mm-design).

1. **Badge colors**: shields.io només amb la paleta mm-design:
   - Red: cf3339 | Blue: 0047ba | Yellow: f1c22f | Green: 427c42 | Black: 111111
2. **Fonts**: Roboto a typing-svg i elements visuals. No Fira Code.
3. **No hex arbitraris**: sempre el color de marca més pròxim.
4. **Icones de secció**: SVGs de `mm-design/icons/readme/` via raw.githubusercontent.com.
