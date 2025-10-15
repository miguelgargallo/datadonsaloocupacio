# filename: app.py
import os
import glob
import io
import tempfile
import unicodedata
from datetime import datetime, date
from typing import List, Optional, Tuple

import pandas as pd
import plotly.express as px
import gradio as gr

# Columnas esperadas
EXPECTED_COLUMNS = [
    "Seccio_censal",
    "Districte",
    "Municipi",
    "Data",
    "Tipus_us",
    "Numero_de_comptadors",
    "Consum_litres_per_dia"
]

def normalize_text(s: str) -> str:
    if pd.isna(s):
        return ""
    s = unicodedata.normalize("NFKD", str(s)).encode("ascii", "ignore").decode("ascii")
    return s

# Cache simple en memoria
_cache = {"dir": None, "df": None, "district_map": None}

def load_district_map(root_dir: str) -> Optional[pd.DataFrame]:
    """Carga districtes.csv si existe, para mapear ID→nombre."""
    path = os.path.join(root_dir, "districtes.csv")
    if not os.path.isfile(path):
        return None
    # tolerancia de separador
    for sep in [",", ";", "\t"]:
        try:
            df = pd.read_csv(path, sep=sep)
            break
        except Exception:
            df = None
    if df is None:
        return None

    cols = {normalize_text(c).lower(): c for c in df.columns}
    id_col = None
    name_col = None
    for guess in ["id", "districte", "district", "codigo", "cod"]:
        g = guess.lower()
        if g in cols:
            id_col = cols[g]
            break
    for guess in ["nom", "nombre", "name", "districte_nom", "district_name"]:
        g = guess.lower()
        if g in cols:
            name_col = cols[g]
            break
    if id_col is None or name_col is None:
        if len(df.columns) >= 2:
            id_col, name_col = df.columns[0], df.columns[1]
        else:
            return None
    m = df[[id_col, name_col]].copy()
    m.columns = ["Districte", "NombreDistrito"]
    m["Districte"] = pd.to_numeric(m["Districte"], errors="coerce")
    m["NombreDistrito"] = m["NombreDistrito"].astype(str)
    m = m.dropna(subset=["Districte"])
    return m

def load_all_csv(root_dir: str) -> pd.DataFrame:
    """Carga todos los CSVs de 'tablas_pequenas' bajo root_dir y unifica."""
    global _cache
    data_dir = os.path.join(root_dir, "tablas_pequenas")
    if _cache["dir"] == data_dir and _cache["df"] is not None:
        return _cache["df"].copy()

    files = sorted(glob.glob(os.path.join(data_dir, "*.csv")))
    if not files:
        _cache = {"dir": data_dir, "df": pd.DataFrame(columns=EXPECTED_COLUMNS), "district_map": None}
        return _cache["df"].copy()

    dfs = []
    for f in files:
        df = None
        for sep in [",", ";", "\t"]:
            try:
                df = pd.read_csv(f, sep=sep)
                break
            except Exception:
                df = None
        if df is None:
            continue

        colmap = {normalize_text(c).lower().strip(): c for c in df.columns}
        mapped = {}
        for target in EXPECTED_COLUMNS:
            tkey = normalize_text(target).lower().strip()
            if tkey in colmap:
                mapped[target] = colmap[tkey]
            else:
                df[target] = None
                mapped[target] = target

        df = df[[mapped[c] for c in EXPECTED_COLUMNS]]
        df.columns = EXPECTED_COLUMNS

        df["Data"] = pd.to_datetime(df["Data"], errors="coerce")
        for num_col in ["Numero_de_comptadors", "Consum_litres_per_dia", "Districte"]:
            df[num_col] = pd.to_numeric(df[num_col], errors="coerce")
        for txt_col in ["Seccio_censal", "Municipi", "Tipus_us"]:
            df[txt_col] = df[txt_col].astype(str)

        df = df.dropna(subset=["Data", "Consum_litres_per_dia"])
        dfs.append(df)

    if not dfs:
        _cache = {"dir": data_dir, "df": pd.DataFrame(columns=EXPECTED_COLUMNS), "district_map": None}
        return _cache["df"].copy()

    all_df = pd.concat(dfs, ignore_index=True)
    all_df["Fecha"] = all_df["Data"].dt.date
    all_df["Uso"] = all_df["Tipus_us"].apply(lambda s: str(s).split("/")[-1] if isinstance(s, str) else s)
    all_df = all_df.sort_values("Data").reset_index(drop=True)

    district_map = load_district_map(root_dir)
    if district_map is not None and not district_map.empty:
        all_df = all_df.merge(district_map, on="Districte", how="left")

    _cache = {"dir": data_dir, "df": all_df, "district_map": district_map}
    return all_df.copy()

def get_filter_options(df: pd.DataFrame):
    if df.empty:
        return [], [], [], [], date(2023, 1, 1), date(2023, 12, 31)
    distritos = sorted(df["Districte"].dropna().unique().tolist())
    municipios = sorted(df["Municipi"].dropna().unique().tolist())
    usos = sorted(df["Uso"].dropna().unique().tolist())
    secciones = sorted(df["Seccio_censal"].dropna().unique().tolist())
    min_d = df["Fecha"].min()
    max_d = df["Fecha"].max()
    return distritos, municipios, usos, secciones, min_d, max_d

def parse_date_text(s: str, fallback: date) -> date:
    """Convierte 'YYYY-MM-DD' a date; si falla, usa fallback."""
    if not s:
        return fallback
    try:
        return datetime.strptime(s.strip(), "%Y-%m-%d").date()
    except Exception:
        return fallback

def filter_df(
    df: pd.DataFrame,
    start_date_txt: str,
    end_date_txt: str,
    distritos: List[float],
    municipios: List[str],
    usos: List[str],
    secciones: List[str],
) -> pd.DataFrame:
    if df.empty:
        return df
    # Rango de fechas seguro
    min_d = df["Fecha"].min() or date(2023, 1, 1)
    max_d = df["Fecha"].max() or date(2023, 12, 31)
    start_date = parse_date_text(start_date_txt, min_d)
    end_date = parse_date_text(end_date_txt, max_d)

    mask = (df["Fecha"] >= start_date) & (df["Fecha"] <= end_date)
    if distritos:
        mask &= df["Districte"].isin(distritos)
    if municipios:
        mask &= df["Municipi"].isin(municipios)
    if usos:
        mask &= df["Uso"].isin(usos)
    if secciones:
        mask &= df["Seccio_censal"].isin(secciones)
    return df.loc[mask].copy()

def compute_metrics(fdf: pd.DataFrame) -> Tuple[str, str, str, str]:
    if fdf.empty:
        return "0", "0", "0", "0"
    total_consumo = float(fdf["Consum_litres_per_dia"].sum())
    total_dias = int(fdf["Fecha"].nunique())
    total_contadores = int(pd.to_numeric(fdf["Numero_de_comptadors"], errors="coerce").sum())
    promedio_dia = (total_consumo / total_dias) if total_dias else 0.0
    fmt_int = lambda x: f"{int(x):,}".replace(",", ".")
    return fmt_int(total_consumo), str(total_dias), fmt_int(total_contadores), fmt_int(promedio_dia)

def make_timeseries_plot(fdf: pd.DataFrame):
    if fdf.empty:
        return px.line(title="Sin datos"), px.area(title="Sin datos")
    gdf = (
        fdf.groupby("Fecha", as_index=False)["Consum_litres_per_dia"]
        .sum()
        .rename(columns={"Consum_litres_per_dia": "Consumo (L)"})
    )
    fig1 = px.line(gdf, x="Fecha", y="Consumo (L)", title="Consumo diario total", markers=True)
    guso = (
        fdf.groupby(["Fecha", "Uso"], as_index=False)["Consum_litres_per_dia"]
        .sum()
        .rename(columns={"Consum_litres_per_dia": "Consumo (L)"})
    )
    fig2 = px.area(guso, x="Fecha", y="Consumo (L)", color="Uso", title="Consumo por tipo de uso (stacked)")
    return fig1, fig2

def make_top_sections_plot(fdf: pd.DataFrame):
    if fdf.empty:
        return px.bar(title="Sin datos")
    gsec = (
        fdf.groupby("Seccio_censal", as_index=False)["Consum_litres_per_dia"]
        .sum()
        .sort_values("Consum_litres_per_dia", ascending=False)
        .head(20)
    )
    fig = px.bar(gsec, x="Seccio_censal", y="Consum_litres_per_dia", title="Top 20 Secciones Censales por consumo (L)")
    fig.update_layout(xaxis={'type': 'category'})
    return fig

def to_csv_file(fdf: pd.DataFrame) -> str:
    """Graba el CSV en un temp file y
