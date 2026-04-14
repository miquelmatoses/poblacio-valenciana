"""
Genera una animacio bar chart race amb l'evolucio de les ciutats
mes grans de la Comunitat Valenciana (1900–present).

Exporta un GIF a assets/bar_chart_race.gif

Us:
  python scripts/generate_chart.py
"""

import re
from pathlib import Path

import bar_chart_race as bcr
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = ROOT / "data" / "valencianpop.csv"
OUTPUT_PATH = ROOT / "assets" / "bar_chart_race.gif"

N_BARS = 12
STEPS_PER_PERIOD = 3
PERIOD_LENGTH = 300

# Cercol brand palette + role colors
COLORS = [
    "#cf3339",  # Red (brand primary)
    "#0047ba",  # Blue (brand secondary)
    "#427c42",  # Green (brand)
    "#f1c22f",  # Yellow (brand)
    "#d46010",  # Orange (R02 Wolf)
    "#1a8c60",  # Emerald (R06 Falcon)
    "#0d8888",  # Teal (R07 Octopus)
    "#3355c8",  # Cobalt (R09 Bee)
    "#6630a8",  # Indigo (R10 Bear)
    "#a030a0",  # Violet (R11 Fox)
    "#b03070",  # Crimson (R12 Badger)
    "#c08800",  # Amber (R03 Elephant)
    "#6a8800",  # Olive (R04 Owl)
    "#1a68b0",  # Cerulean (R08 Tortoise)
    "#111111",  # Black (brand)
]


def clean_city_name(name: str) -> str:
    # Remove INE code prefix (e.g., "03014 ")
    name = re.sub(r"^\d{5}\s+", "", name)
    # Shorten very long names
    if len(name) > 25:
        name = name[:25] + "..."
    return name.strip()


def main():
    print("Llegint dades...")
    df = pd.read_csv(DATA_PATH)

    # Clean city names
    df["city"] = df["city"].apply(clean_city_name)

    # Remove entries with missing population
    df = df.dropna(subset=["population"])
    df["population"] = df["population"].astype(int)

    # Aggregate duplicates (some cities appear twice after name cleaning)
    df = df.groupby(["city", "year"], as_index=False)["population"].sum()

    # Pivot: years as rows, cities as columns
    pivot = df.pivot(index="year", columns="city", values="population")
    pivot = pivot.sort_index()

    # Interpolate missing years (1992-1995 gap) for smooth animation
    full_years = pd.RangeIndex(start=pivot.index.min(), stop=pivot.index.max() + 1)
    pivot = pivot.reindex(full_years)
    pivot = pivot.interpolate(method="linear")
    pivot = pivot.fillna(0)

    # Filter to top cities by max population
    top_cities = (
        df.groupby("city")["population"]
        .max()
        .nlargest(30)
        .index.tolist()
    )
    pivot = pivot[top_cities]

    print(f"Generant animacio ({pivot.index.min()}–{pivot.index.max()})...")
    print(f"  {len(top_cities)} ciutats | {len(pivot)} anys")

    bcr.bar_chart_race(
        df=pivot,
        filename=str(OUTPUT_PATH),
        n_bars=N_BARS,
        steps_per_period=STEPS_PER_PERIOD,
        period_length=PERIOD_LENGTH,
        sort="desc",
        title="Evolucio de la poblacio valenciana per municipi",
        title_size=14,
        bar_size=0.9,
        period_label=True,
        period_fmt="{x:.0f}",
        label_bars=True,
        bar_label_size=9,
        tick_label_size=10,
        cmap=COLORS,
        filter_column_colors=True,
        figsize=(8, 5),
        dpi=80,
        bar_kwargs={"alpha": 0.9, "lw": 0},
        writer="pillow",
    )

    size_mb = OUTPUT_PATH.stat().st_size / (1024 * 1024)
    print(f"\n=== Completat ===")
    print(f"  Fitxer: {OUTPUT_PATH}")
    print(f"  Tamany: {size_mb:.1f} MB")


if __name__ == "__main__":
    main()
