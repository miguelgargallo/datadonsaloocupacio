import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
import glob
from datetime import datetime, timedelta

# Must be the first Streamlit command
st.set_page_config(
    page_title="Water Consumption Analytics",
    page_icon="💧",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apple-style CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=SF+Pro+Display:wght@300;400;500;600;700&display=swap');
    
    .main {
        padding: 1rem 2rem;
    }
    
    .metric-card {
        background: linear-gradient(145deg, #ffffff, #f0f0f0);
        border-radius: 16px;
        padding: 24px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        border: 1px solid rgba(255,255,255,0.2);
        margin: 12px 0;
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 30px rgba(0,0,0,0.12);
    }
    
    .metric-title {
        font-family: 'SF Pro Display', -apple-system, BlinkMacSystemFont, sans-serif;
        font-size: 14px;
        font-weight: 500;
        color: #8E8E93;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 8px;
    }
    
    .metric-value {
        font-family: 'SF Pro Display', -apple-system, BlinkMacSystemFont, sans-serif;
        font-size: 32px;
        font-weight: 600;
        color: #1D1D1F;
        margin: 0;
        line-height: 1.1;
    }
    
    .metric-subtitle {
        font-family: 'SF Pro Display', -apple-system, BlinkMacSystemFont, sans-serif;
        font-size: 13px;
        color: #8E8E93;
        margin-top: 4px;
    }
    
    .section-title {
        font-family: 'SF Pro Display', -apple-system, BlinkMacSystemFont, sans-serif;
        font-size: 28px;
        font-weight: 700;
        color: #1D1D1F;
        margin: 32px 0 16px 0;
        text-align: center;
    }
    
    .filter-section {
        background: rgba(255,255,255,0.7);
        backdrop-filter: blur(20px);
        border-radius: 12px;
        padding: 20px;
        margin: 16px 0;
        border: 1px solid rgba(255,255,255,0.3);
    }
    
    .stSelectbox > div > div {
        border-radius: 8px;
        border: 1px solid #D1D1D6;
        font-family: 'SF Pro Display', sans-serif;
    }
    
    .stButton > button {
        background: linear-gradient(145deg, #007AFF, #0051D5);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 8px 16px;
        font-family: 'SF Pro Display', sans-serif;
        font-weight: 500;
        transition: all 0.2s ease;
    }
    
    .stButton > button:hover {
        transform: scale(1.02);
        box-shadow: 0 4px 15px rgba(0,122,255,0.3);
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #F2F2F7 0%, #FFFFFF 100%);
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    """Load and combine all CSV files"""
    # Get the directory where the script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Find all CSV files in the directory
    csv_files = glob.glob(os.path.join(script_dir, "*.csv"))
    
    if not csv_files:
        st.error("No CSV files found in the directory")
        return pd.DataFrame()
    
    # Load and combine all CSV files
    dfs = []
    for file in csv_files:
        try:
            df = pd.read_csv(file)
            if not df.empty:
                dfs.append(df)
        except Exception as e:
            st.warning(f"Could not load {os.path.basename(file)}: {e}")
    
    if not dfs:
        st.error("No valid data found in CSV files")
        return pd.DataFrame()
    
    # Combine all dataframes
    combined_df = pd.concat(dfs, ignore_index=True)
    
    # Convert date column to datetime and handle Period objects
    if 'Data' in combined_df.columns:
        # Convert Period objects to datetime if necessary
        if hasattr(combined_df['Data'].dtype, 'freq'):
            combined_df['Data'] = combined_df['Data'].dt.to_timestamp()
        else:
            combined_df['Data'] = pd.to_datetime(combined_df['Data'], errors='coerce')
    
    return combined_df

def create_metric_card(title, value, subtitle="", delta=None):
    """Create Apple-style metric card"""
    delta_html = ""
    if delta:
        color = "#34C759" if delta > 0 else "#FF3B30"
        delta_html = f'<div style="color: {color}; font-size: 12px; font-weight: 500;">{"+" if delta > 0 else ""}{delta:.1f}%</div>'
    
    return f"""
    <div class="metric-card">
        <div class="metric-title">{title}</div>
        <div class="metric-value">{value:,.0f}</div>
        <div class="metric-subtitle">{subtitle}</div>
        {delta_html}
    </div>
    """

def create_heatmap(df):
    """Create a heatmap of consumption by date and usage type"""
    # Ensure Data column is datetime
    if 'Data' in df.columns:
        if hasattr(df['Data'].dtype, 'freq'):
            df = df.copy()
            df['Data'] = df['Data'].dt.to_timestamp()
        else:
            df['Data'] = pd.to_datetime(df['Data'], errors='coerce')
    
    # Group by date and usage type
    heatmap_data = df.groupby(['Data', 'Tipus_us'])['Consum_litres_per_dia'].sum().reset_index()
    
    # Convert to pivot table for heatmap
    pivot_data = heatmap_data.pivot(index='Data', columns='Tipus_us', values='Consum_litres_per_dia')
    
    # Handle any remaining non-serializable objects
    pivot_data.index = pd.to_datetime(pivot_data.index)
    
    # Create heatmap
    fig = px.imshow(
        pivot_data.T,
        aspect="auto",
        title="Consumption Heatmap by Date and Usage Type",
        labels=dict(x="Date", y="Usage Type", color="Consumption (L/day)")
    )
    
    return fig

def create_time_series(df, selected_districts=None, selected_usage_types=None):
    """Create time series plot"""
    filtered_df = df.copy()
    
    # Ensure Data column is datetime
    if 'Data' in filtered_df.columns:
        if hasattr(filtered_df['Data'].dtype, 'freq'):
            filtered_df['Data'] = filtered_df['Data'].dt.to_timestamp()
        else:
            filtered_df['Data'] = pd.to_datetime(filtered_df['Data'], errors='coerce')
    
    # Apply filters
    if selected_districts:
        filtered_df = filtered_df[filtered_df['Districte'].isin(selected_districts)]
    
    if selected_usage_types:
        filtered_df = filtered_df[filtered_df['Tipus_us'].isin(selected_usage_types)]
    
    # Group by date and usage type
    time_series_data = filtered_df.groupby(['Data', 'Tipus_us'])['Consum_litres_per_dia'].sum().reset_index()
    
    # Create time series plot
    fig = px.line(
        time_series_data,
        x='Data',
        y='Consum_litres_per_dia',
        color='Tipus_us',
        title="Water Consumption Over Time",
        labels={
            'Data': 'Date',
            'Consum_litres_per_dia': 'Consumption (L/day)',
            'Tipus_us': 'Usage Type'
        }
    )
    
    return fig

def main():
    st.title("💧 Water Consumption Dashboard - Barcelona")
    st.markdown("### Interactive analysis of water consumption data by district and usage type")
    
    # Load data
    with st.spinner("Loading data..."):
        df = load_data()
    
    if df.empty:
        st.error("No data available to display")
        return
    
    # Display basic info
    st.sidebar.header("Conan Data - Assessoria de Data")
    st.sidebar.write(f"Total records: {len(df):,}")
    st.sidebar.write(f"Date range: {df['Data'].min().strftime('%Y-%m-%d')} to {df['Data'].max().strftime('%Y-%m-%d')}")
    
    # Filters
    st.sidebar.header("Filters")
    
    # District filter
    districts = sorted(df['Districte'].unique())
    selected_districts = st.sidebar.multiselect(
        "Select Districts",
        districts,
        default=districts[:3] if len(districts) > 3 else districts
    )
    
    # Usage type filter
    usage_types = sorted(df['Tipus_us'].unique())
    selected_usage_types = st.sidebar.multiselect(
        "Select Usage Types",
        usage_types,
        default=usage_types
    )
    
    # Date range filter
    min_date = df['Data'].min().date()
    max_date = df['Data'].max().date()
    
    start_date, end_date = st.sidebar.date_input(
        "Select Date Range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )
    
    # Filter data
    filtered_df = df[
        (df['Districte'].isin(selected_districts)) &
        (df['Tipus_us'].isin(selected_usage_types)) &
        (df['Data'].dt.date >= start_date) &
        (df['Data'].dt.date <= end_date)
    ]
    
    if filtered_df.empty:
        st.warning("No data matches the selected filters")
        return
    
    # Main content
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Summary Statistics")
        total_consumption = filtered_df['Consum_litres_per_dia'].sum()
        avg_consumption = filtered_df['Consum_litres_per_dia'].mean()
        
        st.metric("Total Consumption", f"{total_consumption:,.0f} L/day")
        st.metric("Average Consumption", f"{avg_consumption:,.0f} L/day")
    
    with col2:
        st.subheader("Consumption by Usage Type")
        usage_summary = filtered_df.groupby('Tipus_us')['Consum_litres_per_dia'].sum().sort_values(ascending=False)
        
        fig_pie = px.pie(
            values=usage_summary.values,
            names=usage_summary.index,
            title="Consumption Distribution"
        )
        st.plotly_chart(fig_pie, use_container_width=True)
    
    # Time series plot
    st.subheader("Consumption Over Time")
    try:
        fig_time = create_time_series(filtered_df, selected_districts, selected_usage_types)
        st.plotly_chart(fig_time, use_container_width=True)
    except Exception as e:
        st.error(f"Error creating time series plot: {e}")
    
    # Heatmap
    st.subheader("Consumption Heatmap")
    try:
        fig_heatmap = create_heatmap(filtered_df)
        st.plotly_chart(fig_heatmap, use_container_width=True)
    except Exception as e:
        st.error(f"Error creating heatmap: {e}")
        st.write("Debug info:")
        st.write(f"Data types: {filtered_df.dtypes}")
        if 'Data' in filtered_df.columns:
            st.write(f"Date column sample: {filtered_df['Data'].head()}")
    
    # District comparison
    st.subheader("District Comparison")
    district_summary = filtered_df.groupby('Districte')['Consum_litres_per_dia'].sum().sort_values(ascending=True)
    
    fig_bar = px.bar(
        x=district_summary.values,
        y=district_summary.index,
        orientation='h',
        title="Total Consumption by District",
        labels={'x': 'Consumption (L/day)', 'y': 'District'}
    )
    st.plotly_chart(fig_bar, use_container_width=True)
    
    # Data table
    st.subheader("Data Table")
    st.dataframe(filtered_df.head(1000), use_container_width=True)

if __name__ == "__main__":
    main()
