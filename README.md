<p align="center">
  <img src="assets/banner.svg" alt="Mapa de la Comunitat Valenciana format pels seus municipis" width="600">
</p>

<h1 align="center">Poblacio Valenciana</h1>

<p align="center">
  <strong>Evolucio de la poblacio valenciana per municipi (1900–2022)</strong><br>
  Dataset obert amb dades demografiques de tots els municipis de la Comunitat Valenciana
</p>

<p align="center">
  <a href="LICENSE"><img src="https://img.shields.io/badge/llicencia-CC0--1.0-blue.svg" alt="Llicencia CC0"></a>
  <img src="https://img.shields.io/badge/municipis-547-green.svg" alt="547 municipis">
  <img src="https://img.shields.io/badge/periode-1900--2022-orange.svg" alt="1900-2022">
</p>

---

## Que es aixo?

Un dataset consolidat amb la **poblacio de cada municipi de la Comunitat Valenciana** des de 1900 fins a 2022. Combina dades dels censos historics (1900–1991) i del padro municipal continu (1996–2022) publicats per l'[INE (Instituto Nacional de Estadistica)](https://www.ine.es/).

Cobreix les tres provincies:
- **Alacant** — 141 municipis
- **Castello** — 135 municipis
- **Valencia** — 266 municipis

## Estructura del repositori

```
poblacio-valenciana/
|- data/
|  +- valencianpop.csv        # Dataset consolidat i net (llest per a analisi)
|- raw/
|  |- alacant_padro_1996-2022.csv
|  |- alacant_censos_1900-1991.csv
|  |- castello_padro_1996-2022.csv
|  |- castello_censos_1900-1991.csv
|  |- valencia_padro_1996-2022.csv
|  +- valencia_censos_1900-1991.csv
|- assets/
|  +- banner.svg
|- LICENSE
+- README.md
```

## Dataset principal: `data/valencianpop.csv`

Fitxer CSV llest per a usar directament en qualsevol eina d'analisi.

| Columna | Tipus | Descripcio |
|---------|-------|-----------|
| `city` | text | Nom del municipi amb codi INE (ex: `03014 Alacant/Alicante`) |
| `year` | int | Any (1900, 1910, ..., 1991, 1996, 1997, ..., 2022) |
| `population` | int | Poblacio total del municipi |

- **20.053 registres** | **547 municipis** | **Delimiter:** coma | **Encoding:** UTF-8
- Nombres enters sense separador de milers, llests per a processar

### Exemple

```csv
city,year,population
"03014 Alacant/Alicante",1900,50142
"03014 Alacant/Alicante",1910,55300
"03014 Alacant/Alicante",2022,337482
"46250 Valencia",1900,213550
"46250 Valencia",2022,791413
```

## Fitxers en brut: `raw/`

Dades originals descarregades directament de l'INE. Cada fitxer correspon a una taula INE:

| Fitxer | Taula INE | Provincia | Periode | Contingut |
|--------|-----------|-----------|---------|-----------|
| `alacant_padro_1996-2022.csv` | 2856 | Alacant | 1996–2022 | Poblacio per municipi i sexe |
| `castello_padro_1996-2022.csv` | 2865 | Castello | 1996–2022 | Poblacio per municipi i sexe |
| `valencia_padro_1996-2022.csv` | 2903 | Valencia | 1996–2022 | Poblacio per municipi i sexe |
| `alacant_censos_1900-1991.csv` | 3036 | Alacant | 1900–1991 | Censos historics |
| `castello_censos_1900-1991.csv` | 3045 | Castello | 1900–1991 | Censos historics |
| `valencia_censos_1900-1991.csv` | 3079 | Valencia | 1900–1991 | Censos historics |

> **Nota:** Els fitxers en brut usen tabuladors com a delimitador, BOM UTF-8, salts de linia CRLF i format numeric espanyol (punts com a separadors de milers). El dataset consolidat (`valencianpop.csv`) ja te tot aixo netejat.

## Limitacions conegudes

- **Dades buides al 1997:** Molts municipis no tenen dades de poblacio per a l'any 1997 als fitxers del padro.
- **Buit 1992–1995:** No hi ha dades entre l'ultim cens historic (1991) i l'inici del padro continu (1996).
- **Municipis desapareguts:** Els codis `*999` (ex: `03999`) recullen la poblacio de municipis que han sigut fusionats o dissolguts.
- **Nomes poblacio total:** El dataset consolidat no inclou desglossament per sexe (disponible als fitxers en brut del padro).

## Font de les dades

Les dades provenen de l'[Instituto Nacional de Estadistica (INE)](https://www.ine.es/):
- **Padro municipal continu** (1996–2022): Xifres oficials de poblacio per municipi
- **Censos de poblacio** (1900–1991): Serie historica censal

## Llicencia

Publicat sota [CC0 1.0 Universal (Domini Public)](LICENSE). Pots usar, copiar, modificar i distribuir lliurement sense cap restriccio.

---

## What is this? (English)

An open dataset with the **population of every municipality in the Valencian Community (Spain)** from 1900 to 2022. It combines historical census data (1900–1991) and continuous municipal register data (1996–2022) published by Spain's [INE (National Statistics Institute)](https://www.ine.es/).

The ready-to-use consolidated file is `data/valencianpop.csv` (CSV, UTF-8, comma-separated, ~20k rows, 547 municipalities). See the Valencian sections above for full documentation of the file structure.

Licensed under [CC0 1.0 (Public Domain)](LICENSE).
