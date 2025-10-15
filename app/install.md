Para ejecutar la aplicación de Streamlit, necesitas instalar las dependencias requeridas. El error indica que falta el módulo `plotly`. Aquí tienes las instrucciones para arrancarlo:

## Pasos para ejecutar la aplicación:

### 1. Instalar las dependencias
Primero, instala las librerías necesarias:

```bash
pip install streamlit plotly pandas
```

### 2. Ejecutar la aplicación
Desde el directorio donde está el archivo app.py, ejecuta:

```bash
cd /Users/mgar/Documents/datadonsaloocupacio/output_tables
streamlit run app.py
```

### 3. Crear un archivo de requirements (opcional pero recomendado)

Para facilitar futuras instalaciones, crea un archivo con las dependencias:

### [requirements.txt](file:///Users/mgar/Documents/datadonsaloocupacio/output_tables/requirements.txt)

```txt
streamlit>=1.28.0
plotly>=5.15.0
pandas>=2.0.0
```

Y luego instala con:
```bash
pip install -r requirements.txt
```

### 4. Si usas un entorno virtual (recomendado)

```bash
# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# En macOS/Linux:
source venv/bin/activate
# En Windows:
# venv\Scripts\activate

# Instalar dependencias
pip install streamlit plotly pandas

# Ejecutar la aplicación
streamlit run app.py
```

Una vez ejecutado, Streamlit abrirá automáticamente tu navegador en `http://localhost:8501` donde podrás ver el dashboard interactivo con los datos de consumo de agua.

La aplicación cargará automáticamente todos los archivos CSV del directorio y creará visualizaciones interactivas incluyendo:
- Gráficos de series temporales
- Mapas de calor
- Gráficos de barras por distrito
- Filtros interactivos por fecha, distrito y tipo de uso

Made changes.