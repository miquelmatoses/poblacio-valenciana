<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:0047ba,50:0047ba,100:0047ba&height=120&section=header&text=&animation=fadeIn" width="100%"/>

<img src="assets/banner.svg" alt="Mapa de la Comunitat Valenciana format pels seus municipis" width="550">

# Població Valenciana

[![Typing SVG](https://readme-typing-svg.herokuapp.com?font=Roboto&weight=600&size=20&pause=1000&color=0047BA&center=true&vCenter=true&random=false&width=600&lines=Evoluci%C3%B3+demogr%C3%A0fica+per+municipi+(1900%E2%80%932025);678+municipis+%C2%B7+3+prov%C3%ADncies+%C2%B7+125+anys+de+dades;Dataset+obert+%C2%B7+Llic%C3%A8ncia+CC0+%C2%B7+Domini+p%C3%BAblic;Actualitzaci%C3%B3+autom%C3%A0tica+des+de+l'API+de+l'INE)](https://git.io/typing-svg)

<br/>

[![Llicència](https://img.shields.io/badge/Llic%C3%A8ncia-CC0--1.0-0047ba?style=for-the-badge&logo=creativecommons&logoColor=white)](LICENSE)
[![Municipis](https://img.shields.io/badge/Municipis-678-0047ba?style=for-the-badge&logo=openstreetmap&logoColor=white)](#dataset-principal-datavalencianpopcsv)
[![Període](https://img.shields.io/badge/Per%C3%ADode-1900--2025-0047ba?style=for-the-badge&logo=clockify&logoColor=white)](#qu%C3%A8-%C3%A9s-aix%C3%B2)
[![INE](https://img.shields.io/badge/Font-INE-cf3339?style=for-the-badge&logo=databricks&logoColor=white)](https://www.ine.es/)

</div>

---

## Visualització

<div align="center">

<img src="assets/bar_chart_race.gif" alt="Bar chart race de la població valenciana" width="700">

*Evolució de les ciutats més grans de la Comunitat Valenciana (1900–2025)*

</div>

---

## Què és això?

Un dataset consolidat amb la **població de cada municipi de la Comunitat Valenciana** des de 1900 fins a 2025. Combina dades dels censos històrics (1900–1991) i del padró municipal continu (1996–2025) publicats per l'[INE (Instituto Nacional de Estadística)](https://www.ine.es/). Les dades s'actualitzen automàticament cada trimestre via l'API de l'INE.

<div align="center">

| | | |
|:---:|:---:|:---:|
| **Alacant** | **Castelló** | **València** |
| 141 municipis | 135 municipis | 266 municipis |
| ![Alacant](https://img.shields.io/badge/prov%C3%ADncia_03-0047ba?style=flat-square) | ![Castelló](https://img.shields.io/badge/prov%C3%ADncia_12-0047ba?style=flat-square) | ![València](https://img.shields.io/badge/prov%C3%ADncia_46-0047ba?style=flat-square) |

</div>

---

## En xifres

<div align="center">

| | |
|:---|:---|
| **678** municipis coberts | **21.032** registres al dataset consolidat |
| **125** anys de dades (1900–2025) | **6** fitxers en brut de l'INE |
| **3** províncies completes | **1** dataset net i llest per a anàlisi |

</div>

---

## Estructura del repositori

```
poblacio-valenciana/
|- data/
|  +- valencianpop.csv           # Dataset consolidat i net (llest per a anàlisi)
|- raw/
|  |- alacant_padro_1996-2025.csv
|  |- alacant_censos_1900-1991.csv
|  |- castello_padro_1996-2025.csv
|  |- castello_censos_1900-1991.csv
|  |- valencia_padro_1996-2025.csv
|  +- valencia_censos_1900-1991.csv
|- scripts/
|  |- update_data.py             # Descarrega dades de l'API de l'INE
|  |- generate_chart.py          # Genera la visualització bar chart race
|  +- requirements.txt
|- assets/
|  |- banner.svg
|  +- bar_chart_race.gif         # Animació generada automàticament
|- .github/workflows/
|  +- update.yml                 # Actualització automàtica trimestral
|- LICENSE
+- README.md
```

---

## Dataset principal: `data/valencianpop.csv`

Fitxer CSV llest per a usar directament en qualsevol eina d'anàlisi.

<div align="center">

| Columna | Tipus | Descripció |
|:---:|:---:|:---|
| `city` | ![text](https://img.shields.io/badge/text-0047ba?style=flat-square) | Nom del municipi en valencià (ex: `Alacant`) |
| `year` | ![int](https://img.shields.io/badge/int-0047ba?style=flat-square) | Any (1900, 1910, ..., 1991, 1996, 1997, ..., 2025) |
| `population` | ![int](https://img.shields.io/badge/int-0047ba?style=flat-square) | Població total del municipi |

</div>

> ![CSV](https://img.shields.io/badge/21.032_registres-0047ba?style=flat-square) ![Municipis](https://img.shields.io/badge/678_municipis-0047ba?style=flat-square) ![Delimiter](https://img.shields.io/badge/delimiter:_coma-0047ba?style=flat-square) ![Encoding](https://img.shields.io/badge/encoding:_UTF--8-0047ba?style=flat-square)

### Exemple

```csv
city,year,population
Alacant,1900,50142
Alacant,1910,55300
Alacant,2025,366221
València,1900,213550
València,2025,840792
```

---

## Fitxers en brut: `raw/`

Dades originals descarregades directament de l'INE. Cada fitxer correspon a una taula INE:

<div align="center">

| Fitxer | Taula INE | Província | Període | Contingut |
|:---|:---:|:---:|:---:|:---|
| `alacant_padro_1996-2025.csv` | ![2856](https://img.shields.io/badge/2856-0047ba?style=flat-square) | Alacant | 1996–2025 | Població per municipi i sexe |
| `castello_padro_1996-2025.csv` | ![2865](https://img.shields.io/badge/2865-0047ba?style=flat-square) | Castelló | 1996–2025 | Població per municipi i sexe |
| `valencia_padro_1996-2025.csv` | ![2903](https://img.shields.io/badge/2903-0047ba?style=flat-square) | València | 1996–2025 | Població per municipi i sexe |
| `alacant_censos_1900-1991.csv` | ![3036](https://img.shields.io/badge/3036-0047ba?style=flat-square) | Alacant | 1900–1991 | Censos històrics |
| `castello_censos_1900-1991.csv` | ![3045](https://img.shields.io/badge/3045-0047ba?style=flat-square) | Castelló | 1900–1991 | Censos històrics |
| `valencia_censos_1900-1991.csv` | ![3079](https://img.shields.io/badge/3079-0047ba?style=flat-square) | València | 1900–1991 | Censos històrics |

</div>

> **Nota:** Els fitxers en brut usen tabuladors com a delimitador, BOM UTF-8, salts de línia CRLF i format numèric espanyol (punts com a separadors de milers). El dataset consolidat (`valencianpop.csv`) ja té tot això netejat.

---

## Limitacions conegudes

```yaml
dades_buides_1997:      Molts municipis no tenen dades per a l'any 1997
buit_1992-1995:         No hi ha dades entre l'últim cens (1991) i el padró continu (1996)
municipis_desapareguts: Els codis *999 recullen població de municipis fusionats o dissolguts
només_total:            El dataset consolidat no inclou desglossament per sexe
                        (disponible als fitxers en brut del padró)
```

---

## Font de les dades

Les dades provenen de l'[Instituto Nacional de Estadística (INE)](https://www.ine.es/):

| Font | Període | Descripció |
|:---|:---:|:---|
| **Padró municipal continu** | 1996–2025 | Xifres oficials de població per municipi |
| **Censos de població** | 1900–1991 | Sèrie històrica censal |

---

## Actualització automàtica

Les dades es descarreguen directament de l'[API de l'INE](https://servicios.ine.es/wstempus/js/) i es processen amb Python.

```bash
# Actualitzar dades manualment
pip install -r scripts/requirements.txt
python scripts/update_data.py

# Regenerar visualització
python scripts/generate_chart.py
```

Un [GitHub Actions workflow](.github/workflows/update.yml) executa aquest procés automàticament cada trimestre.

---

## Llicència

Publicat sota [CC0 1.0 Universal (Domini Públic)](LICENSE). Pots usar, copiar, modificar i distribuir lliurement sense cap restricció.

---

## What is this? (English)

An open dataset with the **population of every municipality in the Valencian Community (Spain)** from 1900 to 2025. It combines historical census data (1900–1991) and continuous municipal register data (1996–2025) published by Spain's [INE (National Statistics Institute)](https://www.ine.es/).

The ready-to-use consolidated file is `data/valencianpop.csv` (CSV, UTF-8, comma-separated, ~21k rows, 678 municipalities). All municipality names are in Valencian. See the sections above for full documentation.

Licensed under [CC0 1.0 (Public Domain)](LICENSE).

---

<div align="center">

![Last Updated](https://img.shields.io/badge/Darrera_actualitzaci%C3%B3-Abril_2026-0047ba?style=flat-square)

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:0047ba,50:0047ba,100:0047ba&height=80&section=footer&text=&animation=fadeIn" width="100%"/>

</div>
