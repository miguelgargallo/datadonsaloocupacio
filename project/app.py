# filename: app_gradio.py
import os
import glob
import io
import unicodedata
from datetime import date
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
    try:
        df = pd.read_csv(path)
    except Exception:
        try:
            df = pd.read_csv(path, sep=";")
        except Exception:
            return None
    # Intentar encontrar columnas de id/nombre
    cols = {normalize_text(c).lower(): c for c in df.columns}
    # Adivinar nombres comunes
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
    # Si no encontramos, intentar primeras dos columnas
    if id_col is None or name_col is None:
        if len(df.columns) >= 2:
            id_col, name_col = df.columns[0], df.columns[1]
        else:
            return None
    # Normalizar tipos
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
        # Leer con tolerancia de separador
        df = None
        for sep in [",", ";", "\t"]:
            try:
                df = pd.read_csv(f, sep=sep)
                break
            except Exception:
                df = None
        if df is None:
            continue

        # Mapear columnas con tolerancia a acentos/caso
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

        # Tipos
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

    # Cargar mapa de distritos si existe
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

def filter_df(
    df: pd.DataFrame,
    start_date: date,
    end_date: date,
    distritos: List[float],
    municipios: List[str],
    usos: List[str],
    secciones: List[str],
) -> pd.DataFrame:
    if df.empty:
        return df
    mask = (
        (df["Fecha"] >= start_date) &
        (df["Fecha"] <= end_date)
    )
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
    fmt = lambda x: f"{int(x):,}".replace(",", ".")
    return fmt(total_consumo), str(total_dias), fmt(total_contadores), fmt(promedio_dia)

def make_timeseries_plot(fdf: pd.DataFrame):
    if fdf.empty:
        return px.line(title="Sin datos"), px.area(title="Sin datos")
    gdf = (
        fdf.groupby("Fecha", as_index=False)["Consum_litres_per_dia"]
        .sum()
        .rename(columns={"Consum_litres_per_dia": "Consumo (L)"})
    )
    fig1 = px.line(gdf, x="Fecha", y="Consumo (L)", title="Consumo diario total", markers=True)
    # por uso
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

def to_csv_bytes(fdf: pd.DataFrame) -> bytes:
    if fdf.empty:
        return b""
    out = fdf.copy()
    out["Data"] = pd.to_datetime(out["Data"]).dt.strftime("%Y-%m-%d")
    # Orden amigable
    cols = [
        "Data", "Seccio_censal", "Districte",
        "Municipi", "Uso", "Numero_de_comptadors",
        "Consum_litres_per_dia"
    ]
    if "NombreDistrito" in out.columns:
        cols.insert(3, "NombreDistrito")
    out = out[[c for c in cols if c in out.columns]]
    buf = io.StringIO()
    out.to_csv(buf, index=False)
    return buf.getvalue().encode("utf-8")

# Gradio funciones de callback
def refresh_data(root_dir: str):
    df = load_all_csv(root_dir)
    distritos, municipios, usos, secciones, min_d, max_d = get_filter_options(df)
    return gr.update(choices=distritos, value=distritos), \
           gr.update(choices=municipios, value=municipios), \
           gr.update(choices=usos, value=usos), \
           gr.update(choices=secciones, value=[]), \
           min_d, max_d, df

def run_filter(
    df: pd.DataFrame,
    start_date: date,
    end_date: date,
    distritos: List[float],
    municipios: List[str],
    usos: List[str],
    secciones: List[str]
):
    fdf = filter_df(df, start_date, end_date, distritos, municipios, usos, secciones)
    total, dias, contadores, promedio = compute_metrics(fdf)
    ts_fig, uso_fig = make_timeseries_plot(fdf)
    top_fig = make_top_sections_plot(fdf)
    # Tabla: recortar columnas y formatear
    show = fdf.copy()
    show["Data"] = pd.to_datetime(show["Data"]).dt.strftime("%Y-%m-%d")
    table_cols = [
        "Data", "Seccio_censal", "Districte",
        "Municipi", "Uso", "Numero_de_comptadors",
        "Consum_litres_per_dia"
    ]
    if "NombreDistrito" in show.columns:
        table_cols.insert(3, "NombreDistrito")
    show = show[table_cols]
    # Archivo descarga
    csv_bytes = to_csv_bytes(fdf)
    return total, dias, contadores, promedio, ts_fig, uso_fig, top_fig, show, csv_bytes

def build_app():
    with gr.Blocks(title="WebUI Consumos de Agua · Barcelona") as demo:
        gr.Markdown("## WebUI Consumos de Agua · Barcelona")
        gr.Markdown("Explora, filtra y visualiza consumos diarios por distrito, uso y sección censal.")
        with gr.Row():
            root_dir = gr.Textbox(
                label="Directorio raíz del proyecto",
                value=".",
                info="La app buscará los CSV dentro de './tablas_pequenas' y, opcionalmente, 'districtes.csv'."
            )
            refresh_btn = gr.Button("Cargar / Refrescar datos")

        df_state = gr.State(pd.DataFrame())

        # Filtros
        with gr.Row():
            start_date = gr.Datepicker(label="Fecha inicio")
            end_date = gr.Datepicker(label="Fecha fin")
        with gr.Row():
            distritos = gr.CheckboxGroup(label="Distrito (ID)", choices=[])
            municipios = gr.CheckboxGroup(label="Municipio", choices=[])
        with gr.Row():
            usos = gr.CheckboxGroup(label="Tipo de uso", choices=[])
            secciones = gr.CheckboxGroup(label="Sección censal", choices=[])

        # Botón aplicar filtros
        apply_btn = gr.Button("Aplicar filtros")

        # Métricas
        with gr.Row():
            total_consumo = gr.Textbox(label="Consumo total (L)", interactive=False)
            total_dias = gr.Textbox(label="Días", interactive=False)
            total_contadores = gr.Textbox(label="Contadores totales", interactive=False)
            promedio_diario = gr.Textbox(label="Promedio diario (L)", interactive=False)

        # Gráficas
        with gr.Row():
            ts_plot = gr.Plot(label="Consumo diario total")
            uso_plot = gr.Plot(label="Consumo por tipo de uso (stacked)")
        top_plot = gr.Plot(label="Top 20 Secciones Censales por consumo (L)")

        # Tabla y descarga
        table = gr.Dataframe(headers=None, datatype="str", row_count=(10, "dynamic"), col_count=(7, "dynamic"))
        download = gr.File(label="Descargar CSV filtrado", interactive=False)

        # Eventos
        refresh_btn.click(
            fn=refresh_data,
            inputs=[root_dir],
            outputs=[distritos, municipios, usos, secciones, start_date, end_date, df_state]
        )

        apply_btn.click(
            fn=run_filter,
            inputs=[df_state, start_date, end_date, distritos, municipios, usos, secciones],
            outputs=[total_consumo, total_dias, total_contadores, promedio_diario,
                     ts_plot, uso_plot, top_plot, table, download]
        )

        gr.Markdown("---")
        gr.Markdown("Nota: Valores extremos pueden indicar outliers o eventos singulares. Revisa fechas específicas.")

    return demo

if __name__ == "__main__":
    app = build_app()
    # Puerto por defecto 7860, puedes cambiarlo
    app.launch(server_port=7860, show_error=True)
