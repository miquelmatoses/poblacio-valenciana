"""
Genera visualitzacions estatiques (PNG) per al README a partir de
data/valencianpop.csv. Un sol fitxer, totes les figures, estil mm-design.

Sortida: assets/viz/*.png

Us:
  python scripts/generate_visuals.py
"""

import csv
import glob
import os
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
matplotlib.set_loglevel("error")  # silencia avisos de fallback de font (Roboto absent al runner)
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
import pandas as pd

from update_data import clean_municipality_name, is_disappeared, is_province_total

ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = ROOT / "data" / "valencianpop.csv"
OUT_DIR = ROOT / "assets" / "viz"
OUT_DIR.mkdir(parents=True, exist_ok=True)

# mm-design palette
BLUE, RED, GREEN, YELLOW, BLACK = "#0047ba", "#cf3339", "#427c42", "#f1c22f", "#111111"
GREY = "#c9ccd6"

plt.rcParams.update({
    "font.family": ["Roboto", "DejaVu Sans"],
    "axes.edgecolor": "#888",
    "axes.grid": True,
    "grid.color": "#e6e6ea",
    "figure.dpi": 120,
    "savefig.bbox": "tight",
})


def thousands(x, _pos=None):
    return f"{x:,.0f}".replace(",", ".")


def load():
    df = pd.read_csv(DATA_PATH).dropna(subset=["population"])
    df["population"] = df["population"].astype(int)
    df["year"] = df["year"].astype(int)
    return df


def province_map():
    """city -> provincia, reconstruit dels CSV de raw/ (un per provincia)."""
    prov = {"alacant": "Alacant", "castello": "Castelló", "valencia": "València"}
    out = {}
    for f in glob.glob(str(ROOT / "raw" / "*.csv")):
        p = prov[os.path.basename(f).split("_")[0]]
        for r in csv.DictReader(open(f, encoding="utf-8")):
            c = r["city"]
            if is_province_total(c) or is_disappeared(c):
                continue
            out[clean_municipality_name(c)] = p
    return out


def save(fig, name):
    path = OUT_DIR / name
    fig.savefig(path, facecolor="white")
    plt.close(fig)
    print(f"  {path.relative_to(ROOT)}")


# 1 — Poblacio total de la CV
def total_population(df):
    t = df.groupby("year")["population"].sum().sort_index()
    fig, ax = plt.subplots(figsize=(9, 4.5))
    ax.fill_between(t.index, t.values, color=BLUE, alpha=0.12)
    ax.plot(t.index, t.values, color=BLUE, lw=2.4, marker="o", ms=3)
    ax.set_title("Població total de la Comunitat Valenciana, 1900–%d" % t.index.max(),
                 fontsize=13, weight="bold", color=BLACK)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(thousands))
    ax.set_ylabel("habitants")
    ax.margins(x=0.01)
    save(fig, "01_total_population.png")


# 2 — Municipis mes grans i mes menuts (ultim any)
def top_bottom(df):
    y = df["year"].max()
    last = df[df["year"] == y]
    top = last.nlargest(10, "population").iloc[::-1]
    bot = last.nsmallest(10, "population").iloc[::-1]
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(11, 4.5))
    for ax, d, col, title in [
        (a1, top, BLUE, f"10 més grans ({y})"),
        (a2, bot, RED, f"10 més menuts ({y})"),
    ]:
        ax.barh(d["city"], d["population"], color=col, alpha=0.9)
        ax.set_title(title, fontsize=12, weight="bold", color=BLACK)
        ax.xaxis.set_major_formatter(mticker.FuncFormatter(thousands))
        ax.grid(axis="y", visible=False)
        for yi, v in enumerate(d["population"]):
            ax.text(v, yi, f" {thousands(v)}", va="center", fontsize=8)
        ax.margins(x=0.18)
    save(fig, "02_top_bottom.png")


# 3 — Guanyadors i perdedors (% de canvi des de 1950)
def winners_losers(df, base=1950, min_base=1000):
    y = df["year"].max()
    b = df[df["year"] == base].set_index("city")["population"]
    n = df[df["year"] == y].set_index("city")["population"]
    common = b.index.intersection(n.index)
    b, n = b.loc[common], n.loc[common]
    b = b[b >= min_base]
    pct = ((n.loc[b.index] / b) - 1) * 100
    sel = pd.concat([pct.nlargest(10), pct.nsmallest(10)]).sort_values()
    colors = [RED if v < 0 else GREEN for v in sel.values]
    fig, ax = plt.subplots(figsize=(9, 6.5))
    ax.barh(sel.index, sel.values, color=colors, alpha=0.9)
    ax.axvline(0, color=BLACK, lw=0.8)
    ax.set_title(f"Qui creix i qui perd població, {base}→{y}\n(% de canvi, municipis ≥ {thousands(min_base)} hab. el {base})",
                 fontsize=12, weight="bold", color=BLACK)
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda v, p: f"{v:+.0f}%"))
    ax.grid(axis="y", visible=False)
    save(fig, "03_winners_losers.png")


# 4 — Trajectories de les 10 ciutats mes grans
def top10_trajectories(df):
    top = df.groupby("city")["population"].max().nlargest(10).index
    pv = df[df["city"].isin(top)].pivot(index="year", columns="city", values="population").sort_index()
    pv = pv[top]  # ordena per mida
    cmap = plt.get_cmap("tab10")
    fig, ax = plt.subplots(figsize=(9, 5))
    for i, c in enumerate(pv.columns):
        s = pv[c].dropna()
        ax.plot(s.index, s.values, lw=2, color=cmap(i), label=c)
    ax.set_yscale("log")
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(thousands))
    ax.set_title("Trajectòria de les 10 ciutats més grans (escala log)",
                 fontsize=13, weight="bold", color=BLACK)
    ax.legend(fontsize=8, ncol=2, loc="lower right")
    ax.margins(x=0.01)
    save(fig, "04_top10_trajectories.png")


# 5 — Distribucio rank-size (Zipf)
def rank_size(df):
    y = df["year"].max()
    s = df[df["year"] == y].sort_values("population", ascending=False)["population"].values
    rank = np.arange(1, len(s) + 1)
    fig, ax = plt.subplots(figsize=(7.5, 5.5))
    ax.loglog(rank, s, color=BLUE, lw=0, marker="o", ms=3, alpha=0.6)
    zipf = s[0] / rank
    ax.loglog(rank, zipf, color=RED, lw=1.5, ls="--", label="Llei de Zipf (1/rang)")
    for r, name in [(1, "València"), (2, "Alacant"), (3, "Elx")]:
        ax.annotate(name, (r, s[r - 1]), fontsize=8, xytext=(6, 0),
                    textcoords="offset points", va="center")
    ax.set_title(f"Distribució de mides municipals, {y}", fontsize=13, weight="bold", color=BLACK)
    ax.set_xlabel("rang (municipi n-èsim més gran)")
    ax.set_ylabel("població")
    ax.legend(fontsize=9)
    save(fig, "05_rank_size.png")


def annualized(pv, years):
    """% de creixement anual mitja (CAGR) entre columnes d'anys consecutius.
    Anualitzar fa comparables trams de 10 i de 5 anys al mateix mapa."""
    cols = [y for y in years if y in pv.columns]
    sub = pv[cols]
    out = {}
    for a, b in zip(cols, cols[1:]):
        out[f"{a}–{b}"] = ((sub[b] / sub[a]) ** (1 / (b - a)) - 1) * 100
    return pd.DataFrame(out)


def _heatmap(fig, ax, m, title, vlim=5):
    im = ax.imshow(m.values, cmap="RdYlGn", vmin=-vlim, vmax=vlim, aspect="auto")
    ax.set_xticks(range(m.shape[1]), m.columns, rotation=45, ha="right", fontsize=8)
    ax.set_yticks(range(m.shape[0]), m.index, fontsize=8)
    ax.set_title(title, fontsize=13, weight="bold", color=BLACK, pad=12)
    ax.grid(False)
    fig.colorbar(im, ax=ax, shrink=0.7, label="% creixement anual")


# 6 — Heatmap de creixement (top 20 ciutats), decades fins 1991 + 5 anys fins 2025
def growth_heatmap(df):
    years = [1900, 1910, 1920, 1930, 1940, 1950, 1960, 1970, 1981, 1991,
             2000, 2005, 2010, 2015, 2020, 2025]
    top = df.groupby("city")["population"].max().nlargest(20).index
    pv = df[df["city"].isin(top)].pivot(index="city", columns="year", values="population").reindex(index=top)
    m = annualized(pv, years)
    fig, ax = plt.subplots(figsize=(11, 7))
    _heatmap(fig, ax, m, "Creixement anual de població — 20 ciutats més grans")
    save(fig, "06_growth_heatmap.png")


# 7 — Heatmap de creixement per comarca (epoca moderna, cada 5 anys)
def comarca_heatmap(df):
    cmap = {r["city"]: r["comarca"] for r in csv.DictReader(open(ROOT / "data" / "comarques.csv"))}
    df = df.assign(comarca=df["city"].map(cmap)).dropna(subset=["comarca"])
    pv = df.groupby(["comarca", "year"])["population"].sum().unstack("year")
    years = [2000, 2005, 2010, 2015, 2020, 2025]
    order = df[df["year"] == df["year"].max()].groupby("comarca")["population"].sum().sort_values(ascending=False).index
    pv = pv.reindex(index=order)
    m = annualized(pv, years)
    fig, ax = plt.subplots(figsize=(8.5, 9))
    _heatmap(fig, ax, m, "Creixement anual per comarca, 2000–2025")
    save(fig, "07_comarca_heatmap.png")


# 8 — Poblacio per provincia (area apilada)
def province_area(df):
    p = province_map()
    df = df.assign(prov=df["city"].map(p)).dropna(subset=["prov"])
    pv = df.groupby(["year", "prov"])["population"].sum().unstack("prov").sort_index()
    pv = pv.dropna()
    fig, ax = plt.subplots(figsize=(9, 5))
    order = ["València", "Alacant", "Castelló"]
    ax.stackplot(pv.index, [pv[c] for c in order], labels=order,
                 colors=[BLUE, RED, YELLOW], alpha=0.9)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(thousands))
    ax.set_title("Població per província, 1900–%d" % pv.index.max(),
                 fontsize=13, weight="bold", color=BLACK)
    ax.legend(loc="upper left", fontsize=9)
    ax.margins(x=0.01, y=0)
    save(fig, "08_province_area.png")


def main():
    print("Generant visualitzacions...")
    df = load()
    total_population(df)
    top_bottom(df)
    winners_losers(df)
    top10_trajectories(df)
    rank_size(df)
    growth_heatmap(df)
    comarca_heatmap(df)
    province_area(df)
    print("Fet.")


if __name__ == "__main__":
    main()
