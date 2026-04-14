"""
Descarrega i consolida les dades de poblacio valenciana des de l'API de l'INE.

Taules:
  - 2856 / 2865 / 2903: Padro municipal (1996–present), per provincia
  - 3036 / 3045 / 3079: Censos historics (1900–1991), per provincia

Us:
  python scripts/update_data.py
"""

import json
import logging
import time
from pathlib import Path

import pandas as pd
import requests

logging.basicConfig(level=logging.INFO, format="%(message)s")
log = logging.getLogger(__name__)

BASE_URL = "https://servicios.ine.es/wstempus/js/ES/DATOS_TABLA"

TABLES = {
    "padro": {
        2856: "alacant",
        2865: "castello",
        2903: "valencia",
    },
    "censos": {
        3036: "alacant",
        3045: "castello",
        3079: "valencia",
    },
}

ROOT = Path(__file__).resolve().parent.parent
RAW_DIR = ROOT / "raw"
DATA_DIR = ROOT / "data"


def fetch_table(table_id: int) -> list[dict]:
    url = f"{BASE_URL}/{table_id}"
    log.info(f"  Descarregant taula {table_id} ...")
    resp = requests.get(url, timeout=60)
    resp.raise_for_status()
    return resp.json()


def parse_padro(series: list[dict]) -> pd.DataFrame:
    rows = []
    for s in series:
        name = s["Nombre"]
        parts = name.split(".")
        municipality = parts[0].strip()
        sex = parts[1].strip() if len(parts) > 1 else ""
        if sex != "Total":
            continue
        for d in s.get("Data", []):
            val = d.get("Valor")
            if val is None:
                continue
            rows.append({
                "city": municipality,
                "year": d["Anyo"],
                "population": int(val),
            })
    return pd.DataFrame(rows)


def parse_censos(series: list[dict]) -> pd.DataFrame:
    rows = []
    for s in series:
        name = s["Nombre"]
        municipality = name.split(".")[0].strip()
        for d in s.get("Data", []):
            val = d.get("Valor")
            if val is None:
                continue
            rows.append({
                "city": municipality,
                "year": d["Anyo"],
                "population": int(val),
            })
    return pd.DataFrame(rows)


PROVINCE_NAMES = {
    "Alicante", "Castellón", "Castellon", "Valencia",
    "Alicante/Alacant", "Castellón/Castelló", "Valencia/València",
    "Alacant", "Castelló", "València",
}


def is_province_total(city: str) -> bool:
    code = city.split()[0] if city else ""
    # Provincial totals have 2-digit codes (e.g., "03 Alicante/Alacant")
    if len(code) == 2 and code.isdigit():
        return True
    # Census data may have prefixes like "Población de Hecho: Valencia"
    name = city
    for prefix in ("Población de Hecho: ", "Población de Derecho: ", "Total: "):
        if name.startswith(prefix):
            name = name[len(prefix):]
    # Only match exact province names (not "Castellón de la Plana" etc.)
    return name.strip() in PROVINCE_NAMES


def is_disappeared(city: str) -> bool:
    code = city.split()[0] if city else ""
    return code.endswith("999")


# Mapping of Castilian names to Valencian names for municipalities
VALENCIAN_NAMES = {
    # Bilingual forms (with slash)
    "Alicante/Alacant": "Alacant",
    "Alcoy/Alcoi": "Alcoi",
    "Elche/Elx": "Elx",
    "Orihuela/Orihuela": "Oriola",
    "San Vicente del Raspeig/Sant Vicent del Raspeig": "Sant Vicent del Raspeig",
    "Castellón de la Plana/Castelló de la Plana": "Castelló de la Plana",
    "Valencia/València": "València",
    "Sagunto/Sagunt": "Sagunt",
    "Villarreal/Vila-real": "Vila-real",
    "Játiva/Xàtiva": "Xàtiva",
    "Denia/Dénia": "Dénia",
    "Burriana/Borriana": "Borriana",
    "Onteniente/Ontinyent": "Ontinyent",
    "Torrente/Torrent": "Torrent",
    "Burjasot/Burjassot": "Burjassot",
    "Aldaya/Aldaia": "Aldaia",
    "Alcira/Alzira": "Alzira",
    # Castilian-only forms (padro data)
    "Alicante": "Alacant",
    "Elche": "Elx",
    "Orihuela": "Oriola",
    "Alcoy": "Alcoi",
    "San Vicente del Raspeig": "Sant Vicent del Raspeig",
    "Castellón de la Plana": "Castelló de la Plana",
    "Sagunto": "Sagunt",
    "Burriana": "Borriana",
    "Torrevieja": "Torrevella",
    "Gandía": "Gandia",
    "Villena": "Villena",
    "Villajoyosa/la Vila Joiosa": "la Vila Joiosa",
    "Villajoyosa": "la Vila Joiosa",
    "Jávea/Xàbia": "Xàbia",
    "Jávea": "Xàbia",
    "Novelda": "Novelda",
    "Petrer/Petrel": "Petrer",
    "Crevillente/Crevillent": "Crevillent",
    "Crevillente": "Crevillent",
    "Santa Pola": "Santa Pola",
    "Campello (el)/el Campello": "el Campello",
    "Calpe/Calp": "Calp",
    "Altea": "Altea",
    "Ibi": "Ibi",
    "Aspe": "Asp",
    "Muchamiel/Mutxamel": "Mutxamel",
    "Muchamiel": "Mutxamel",
    "Pilar de la Horadada": "Pilar de la Horadada",
    "Rojales": "Rojals",
    "San Fulgencio": "San Fulgenci",
    "Alfaz del Pi/l'Alfàs del Pi": "l'Alfàs del Pi",
    "Ondara": "Ondara",
    "Pedreguer": "Pedreguer",
    # Census historical forms
    "Játiva": "Xàtiva",
    "Onteniente": "Ontinyent",
    "Torrente": "Torrent",
    "Burjasot": "Burjassot",
    "Aldaya": "Aldaia",
    "Alcira": "Alzira",
}


def clean_municipality_name(name: str) -> str:
    # Remove common INE prefixes from census data
    prefixes = [
        "Población de Hecho: ",
        "Población de Derecho: ",
        "Total: ",
    ]
    for prefix in prefixes:
        if name.startswith(prefix):
            name = name[len(prefix):]
    name = name.strip()

    # Use Valencian name if available
    if name in VALENCIAN_NAMES:
        return VALENCIAN_NAMES[name]

    # For bilingual names with slash, take the first part (Valencian in most INE data)
    if "/" in name:
        parts = name.split("/")
        return parts[0].strip()

    return name


def save_raw(df: pd.DataFrame, province: str, period: str):
    filename = f"{province}_{period}.csv"
    path = RAW_DIR / filename
    df.to_csv(path, index=False, encoding="utf-8")
    log.info(f"  Escrit {path.name} ({len(df)} files)")


def main():
    log.info("=== Actualitzant dades de poblacio valenciana ===\n")

    all_frames = []

    # Padro municipal
    log.info("Padro municipal (1996–present):")
    for table_id, province in TABLES["padro"].items():
        series = fetch_table(table_id)
        df = parse_padro(series)
        save_raw(df, province, f"padro_{df['year'].min()}-{df['year'].max()}")
        all_frames.append(df)
        time.sleep(0.5)

    # Censos historics
    log.info("\nCensos historics (1900–1991):")
    for table_id, province in TABLES["censos"].items():
        series = fetch_table(table_id)
        df = parse_censos(series)
        save_raw(df, province, f"censos_{df['year'].min()}-{df['year'].max()}")
        all_frames.append(df)
        time.sleep(0.5)

    # Consolidar
    log.info("\nConsolidant dataset...")
    consolidated = pd.concat(all_frames, ignore_index=True)

    # Eliminar totals provincials i municipis desapareguts ABANS de netejar noms
    mask = consolidated["city"].apply(
        lambda c: not is_province_total(c) and not is_disappeared(c)
    )
    consolidated = consolidated[mask]

    # Netejar noms de municipis (valencianitzar)
    consolidated["city"] = consolidated["city"].apply(clean_municipality_name)

    # Eliminar duplicats (censos i padro poden solapar-se)
    consolidated = consolidated.drop_duplicates(subset=["city", "year"], keep="first")

    # Ordenar
    consolidated = consolidated.sort_values(["city", "year"]).reset_index(drop=True)

    # Exportar
    out_path = DATA_DIR / "valencianpop.csv"
    consolidated.to_csv(out_path, index=False, encoding="utf-8")

    n_cities = consolidated["city"].nunique()
    n_years = consolidated["year"].nunique()
    year_min = consolidated["year"].min()
    year_max = consolidated["year"].max()

    log.info(f"\n=== Completat ===")
    log.info(f"  Fitxer: {out_path}")
    log.info(f"  {len(consolidated)} registres | {n_cities} municipis | {year_min}–{year_max}")


if __name__ == "__main__":
    main()
