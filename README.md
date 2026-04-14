<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:1a3570,50:2b54ac,100:4a7de0&height=120&section=header&text=&animation=fadeIn" width="100%"/>

<img src="assets/banner.svg" alt="Mapa de la Comunitat Valenciana format pels seus municipis" width="550">

# Poblacio Valenciana

[![Typing SVG](https://readme-typing-svg.herokuapp.com?font=Fira+Code&weight=600&size=20&pause=1000&color=2B54AC&center=true&vCenter=true&random=false&width=600&lines=Evolucio+demografica+per+municipi+(1900%E2%80%932022);547+municipis+%C2%B7+3+provincies+%C2%B7+122+anys+de+dades;Dataset+obert+%C2%B7+Llicencia+CC0+%C2%B7+Domini+public)](https://git.io/typing-svg)

<br/>

[![Llicencia](https://img.shields.io/badge/Llicencia-CC0--1.0-2b54ac?style=for-the-badge&logo=creativecommons&logoColor=white)](LICENSE)
[![Municipis](https://img.shields.io/badge/Municipis-547-1a3570?style=for-the-badge&logo=openstreetmap&logoColor=white)](#dataset-principal-datavalencianpopcsv)
[![Periode](https://img.shields.io/badge/Periode-1900--2022-4a7de0?style=for-the-badge&logo=clockify&logoColor=white)](#que-es-aixo)
[![INE](https://img.shields.io/badge/Font-INE-c0392b?style=for-the-badge&logo=databricks&logoColor=white)](https://www.ine.es/)

</div>

---

## Que es aixo?

Un dataset consolidat amb la **poblacio de cada municipi de la Comunitat Valenciana** des de 1900 fins a 2022. Combina dades dels censos historics (1900–1991) i del padro municipal continu (1996–2022) publicats per l'[INE (Instituto Nacional de Estadistica)](https://www.ine.es/).

<div align="center">

| | | |
|:---:|:---:|:---:|
| **Alacant** | **Castello** | **Valencia** |
| 141 municipis | 135 municipis | 266 municipis |
| ![Alacant](https://img.shields.io/badge/provincia_03-2b54ac?style=flat-square) | ![Castello](https://img.shields.io/badge/provincia_12-1a3570?style=flat-square) | ![Valencia](https://img.shields.io/badge/provincia_46-4a7de0?style=flat-square) |

</div>

---

## En xifres

<div align="center">

| | |
|:---|:---|
| **547** municipis coberts | **20.053** registres al dataset consolidat |
| **122** anys de dades (1900–2022) | **6** fitxers en brut de l'INE |
| **3** provincies completes | **1** dataset net i llest per a analisi |

</div>

---

## Estructura del repositori

```
poblacio-valenciana/
|- data/
|  +- valencianpop.csv           # Dataset consolidat i net (llest per a analisi)
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

---

## Dataset principal: `data/valencianpop.csv`

Fitxer CSV llest per a usar directament en qualsevol eina d'analisi.

<div align="center">

| Columna | Tipus | Descripcio |
|:---:|:---:|:---|
| `city` | ![text](https://img.shields.io/badge/text-2b54ac?style=flat-square) | Nom del municipi amb codi INE (ex: `03014 Alacant/Alicante`) |
| `year` | ![int](https://img.shields.io/badge/int-1a3570?style=flat-square) | Any (1900, 1910, ..., 1991, 1996, 1997, ..., 2022) |
| `population` | ![int](https://img.shields.io/badge/int-1a3570?style=flat-square) | Poblacio total del municipi |

</div>

> ![CSV](https://img.shields.io/badge/20.053_registres-2b54ac?style=flat-square) ![Municipis](https://img.shields.io/badge/547_municipis-1a3570?style=flat-square) ![Delimiter](https://img.shields.io/badge/delimiter:_coma-4a7de0?style=flat-square) ![Encoding](https://img.shields.io/badge/encoding:_UTF--8-2b54ac?style=flat-square)

### Exemple

```csv
city,year,population
"03014 Alacant/Alicante",1900,50142
"03014 Alacant/Alicante",1910,55300
"03014 Alacant/Alicante",2022,337482
"46250 Valencia",1900,213550
"46250 Valencia",2022,791413
```

---

## Fitxers en brut: `raw/`

Dades originals descarregades directament de l'INE. Cada fitxer correspon a una taula INE:

<div align="center">

| Fitxer | Taula INE | Provincia | Periode | Contingut |
|:---|:---:|:---:|:---:|:---|
| `alacant_padro_1996-2022.csv` | ![2856](https://img.shields.io/badge/2856-2b54ac?style=flat-square) | Alacant | 1996–2022 | Poblacio per municipi i sexe |
| `castello_padro_1996-2022.csv` | ![2865](https://img.shields.io/badge/2865-2b54ac?style=flat-square) | Castello | 1996–2022 | Poblacio per municipi i sexe |
| `valencia_padro_1996-2022.csv` | ![2903](https://img.shields.io/badge/2903-2b54ac?style=flat-square) | Valencia | 1996–2022 | Poblacio per municipi i sexe |
| `alacant_censos_1900-1991.csv` | ![3036](https://img.shields.io/badge/3036-1a3570?style=flat-square) | Alacant | 1900–1991 | Censos historics |
| `castello_censos_1900-1991.csv` | ![3045](https://img.shields.io/badge/3045-1a3570?style=flat-square) | Castello | 1900–1991 | Censos historics |
| `valencia_censos_1900-1991.csv` | ![3079](https://img.shields.io/badge/3079-1a3570?style=flat-square) | Valencia | 1900–1991 | Censos historics |

</div>

> **Nota:** Els fitxers en brut usen tabuladors com a delimitador, BOM UTF-8, salts de linia CRLF i format numeric espanyol (punts com a separadors de milers). El dataset consolidat (`valencianpop.csv`) ja te tot aixo netejat.

---

## Limitacions conegudes

```yaml
dades_buides_1997:    Molts municipis no tenen dades per a l'any 1997
buit_1992-1995:       No hi ha dades entre l'ultim cens (1991) i el padro continu (1996)
municipis_desapareguts: Els codis *999 recullen poblacio de municipis fusionats o dissolguts
nomes_total:          El dataset consolidat no inclou desglossament per sexe
                      (disponible als fitxers en brut del padro)
```

---

## Font de les dades

Les dades provenen de l'[Instituto Nacional de Estadistica (INE)](https://www.ine.es/):

| Font | Periode | Descripcio |
|:---|:---:|:---|
| **Padro municipal continu** | 1996–2022 | Xifres oficials de poblacio per municipi |
| **Censos de poblacio** | 1900–1991 | Serie historica censal |

---

## Llicencia

Publicat sota [CC0 1.0 Universal (Domini Public)](LICENSE). Pots usar, copiar, modificar i distribuir lliurement sense cap restriccio.

---

## What is this? (English)

An open dataset with the **population of every municipality in the Valencian Community (Spain)** from 1900 to 2022. It combines historical census data (1900–1991) and continuous municipal register data (1996–2022) published by Spain's [INE (National Statistics Institute)](https://www.ine.es/).

The ready-to-use consolidated file is `data/valencianpop.csv` (CSV, UTF-8, comma-separated, ~20k rows, 547 municipalities). See the Valencian sections above for full documentation of the file structure.

Licensed under [CC0 1.0 (Public Domain)](LICENSE).

---

<div align="center">

![Last Updated](https://img.shields.io/badge/Darrera_actualitzacio-Abril_2026-2b54ac?style=flat-square)

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:4a7de0,50:2b54ac,100:1a3570&height=80&section=footer&text=&animation=fadeIn" width="100%"/>

</div>
