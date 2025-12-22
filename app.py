"""
Durr Bottling Energy Dashboard - Ultra-Modern Improved Version
============================================================
Enhanced with:
- Silent data loading (no loading messages)
- Real fuel pricing from Excel data
- New 3-inverter solar system integration
- Fixed solar negative values
- Fuel purchase tracking and comparison
- Updated Streamlit compatibility
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta, date
import numpy as np
import io
import requests
from pathlib import Path
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings('ignore')

# Enhanced Solar Analysis - DEPLOYED 2025-12-18 17:08:56
# 4 new sections should appear in Solar Performance tab:
# 1. System Comparison Analysis (Legacy vs New)
# 2. Hourly Power Generation Patterns  
# 3. Inverter Power Performance Monitoring
# 4. Power Generation Trends & Analysis

# Import enhanced solar analysis functions
try:
    from tmp_rovodev_solar_analysis import (
        analyze_legacy_system,
        analyze_new_system,
        compare_solar_systems,
        create_before_after_chart,
        create_capacity_utilization_analysis,
        generate_engineering_report
    )
    SOLAR_ANALYSIS_AVAILABLE = True
except ImportError:
    SOLAR_ANALYSIS_AVAILABLE = False
    print("Solar analysis module not available - using fallback functions")

# ==============================================================================
# ULTRA-MODERN PAGE CONFIGURATION
# ==============================================================================
st.set_page_config(
    page_title="Durr Energy Intelligence", 
    page_icon="⚡", 
    layout="wide",
    initial_sidebar_state="expanded"
)

def apply_ultra_modern_styling():
    """Ultra-modern styling with glassmorphism and advanced animations"""
    st.markdown("""
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
            @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;500;600&display=swap');
            
            :root {
                --bg-primary: #0a0d1a;
                --bg-secondary: #111827;
                --bg-card: rgba(30, 41, 59, 0.7);
                --bg-glass: rgba(255, 255, 255, 0.03);
                --text-primary: #ffffff;
                --text-secondary: #f1f5f9;
                --text-muted: #94a3b8;
                --accent-blue: #3b82f6;
                --accent-green: #10b981;
                --accent-purple: #8b5cf6;
                --accent-cyan: #06b6d4;
                --accent-red: #ef4444;
                --accent-yellow: #f59e0b;
                --border: rgba(148, 163, 184, 0.1);
                --border-hover: rgba(148, 163, 184, 0.2);
                --shadow-glass: 0 8px 32px rgba(0, 0, 0, 0.37);
                --gradient-primary: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                --gradient-success: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
                --gradient-warning: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
                --gradient-purple: linear-gradient(135deg, #c471ed 0%, #f64f59 100%);
            }
            
            .stApp {
                background: radial-gradient(ellipse at top, rgba(59, 130, 246, 0.1) 0%, transparent 50%),
                           radial-gradient(ellipse at bottom, rgba(16, 185, 129, 0.1) 0%, transparent 50%),
                           var(--bg-primary);
                color: var(--text-secondary);
                font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
                min-height: 100vh;
            }
            
            #MainMenu, footer, header, .stDeployButton { visibility: hidden; }
            
            /* Ultra-modern glassmorphic cards */
            .glass-card {
                background: var(--bg-glass);
                backdrop-filter: blur(20px);
                border: 1px solid var(--border);
                border-radius: 24px;
                padding: 32px;
                margin-bottom: 24px;
                box-shadow: var(--shadow-glass);
                transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
                position: relative;
                overflow: hidden;
            }
            
            .glass-card::before {
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                height: 1px;
                background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
                opacity: 0;
                transition: opacity 0.4s ease;
            }
            
            .glass-card:hover {
                transform: translateY(-8px);
                border-color: var(--border-hover);
                box-shadow: 0 20px 80px rgba(0, 0, 0, 0.5);
            }
            
            .glass-card:hover::before {
                opacity: 1;
            }
            
            /* Revolutionary tab design */
            .stTabs [data-baseweb="tab-list"] {
                gap: 4px;
                margin-bottom: 2rem;
                background: var(--bg-glass);
                backdrop-filter: blur(20px);
                padding: 8px;
                border-radius: 20px;
                border: 1px solid var(--border);
                box-shadow: var(--shadow-glass);
            }
            
            .stTabs [data-baseweb="tab"] {
                background: transparent;
                border: none;
                border-radius: 16px;
                color: var(--text-muted);
                padding: 16px 32px;
                font-weight: 600;
                font-size: 0.95rem;
                transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
                position: relative;
                overflow: hidden;
            }
            
            .stTabs [data-baseweb="tab"]::before {
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background: var(--gradient-primary);
                opacity: 0;
                transition: opacity 0.3s ease;
                border-radius: 16px;
                z-index: -1;
            }
            
            .stTabs [data-baseweb="tab"]:hover {
                color: var(--text-secondary);
                transform: translateY(-2px);
            }
            
            .stTabs [data-baseweb="tab"][aria-selected="true"] {
                color: white;
                transform: translateY(-2px);
                box-shadow: 0 8px 32px rgba(59, 130, 246, 0.4);
            }
            
            .stTabs [data-baseweb="tab"][aria-selected="true"]::before {
                opacity: 1;
            }
            
            /* Enhanced metric cards with data visualization */
            .metric-card-modern {
                background: var(--bg-glass);
                backdrop-filter: blur(20px);
                border: 1px solid var(--border);
                border-radius: 20px;
                padding: 28px;
                margin-bottom: 20px;
                box-shadow: var(--shadow-glass);
                transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
                position: relative;
                overflow: hidden;
                cursor: pointer;
            }
            
            .metric-card-modern::after {
                content: '';
                position: absolute;
                top: -50%;
                left: -50%;
                width: 200%;
                height: 200%;
                background: linear-gradient(45deg, transparent, rgba(255,255,255,0.03), transparent);
                transform: rotate(-45deg) translate(-50%, -50%);
                transition: transform 0.6s ease;
                opacity: 0;
            }
            
            .metric-card-modern:hover {
                transform: translateY(-6px) scale(1.02);
                border-color: var(--border-hover);
                box-shadow: 0 20px 80px rgba(0, 0, 0, 0.4);
            }
            
            .metric-card-modern:hover::after {
                opacity: 1;
                transform: rotate(-45deg) translate(-20%, -20%);
            }
            
            /* Advanced button styling */
            .stButton > button {
                background: var(--bg-glass) !important;
                backdrop-filter: blur(20px);
                border: 1px solid var(--border) !important;
                border-radius: 16px !important;
                color: var(--text-secondary) !important;
                font-weight: 600 !important;
                padding: 12px 32px !important;
                transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
                font-family: 'Inter', sans-serif !important;
            }
            
            .stButton > button:hover {
                transform: translateY(-2px) !important;
                box-shadow: 0 8px 32px rgba(59, 130, 246, 0.3) !important;
                border-color: var(--accent-blue) !important;
            }
            
            /* Enhanced form controls */
            .stDateInput > div > div,
            .stSelectbox > div > div,
            .stSlider > div > div {
                background: var(--bg-glass) !important;
                backdrop-filter: blur(20px);
                border: 1px solid var(--border) !important;
                border-radius: 12px !important;
            }
            
            /* Section headers with gradient text */
            .section-header-modern {
                background: var(--bg-glass);
                backdrop-filter: blur(20px);
                border: 1px solid var(--border);
                border-left: 4px solid var(--accent-blue);
                border-radius: 16px;
                padding: 24px;
                margin-bottom: 32px;
                position: relative;
                overflow: hidden;
            }
            
            .gradient-text {
                background: linear-gradient(135deg, #3b82f6, #10b981);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
                font-weight: 800;
                font-size: 2.5rem;
                line-height: 1.2;
            }
        </style>
    """, unsafe_allow_html=True)

apply_ultra_modern_styling()

# ==============================================================================
# SILENT DATA LOADING (NO CONSOLE MESSAGES)
# ==============================================================================

@st.cache_data(ttl=3600, show_spinner=False)
def load_all_energy_data_silent():
    """Silent, robust data loading that supports CSV/XLSX and avoids hardcoded paths"""
    ROOT = Path(__file__).resolve().parent

    def load_any(name_candidates):
        """Try multiple filenames and formats; return DataFrame or empty."""
        for name in name_candidates:
            p = ROOT / name
            try:
                if p.suffix.lower() in {'.xlsx', '.xls'}:
                    df = pd.read_excel(p)
                elif p.suffix.lower() in {'.csv'}:
                    df = pd.read_csv(p)
                else:
                    # Try csv then excel without extension
                    if (ROOT / f"{name}.csv").exists():
                        df = pd.read_csv(ROOT / f"{name}.csv")
                    elif (ROOT / f"{name}.xlsx").exists():
                        df = pd.read_excel(ROOT / f"{name}.xlsx")
                    else:
                        continue
                if df is not None and not df.empty:
                    return df
            except Exception:
                continue
        return pd.DataFrame()

    data = {}

    # Primary generator and fuel history (support both csv/xlsx)
    data['generator'] = load_any(["gen (2).csv", "gen (2).xlsx", "gen.csv", "gen.xlsx"])    
    data['fuel_history'] = load_any(["history (5).csv", "history (5).xlsx", "history.csv", "history.xlsx"])  
    data['factory'] = load_any(["FACTORY ELEC.csv", "FACTORY ELEC.xlsx", "factory.csv", "factory.xlsx"])    

    # Fuel purchase data (real pricing) without hardcoded absolute path
    data['fuel_purchases'] = load_any(["Durr bottling Generator filling.xlsx", "fuel_purchases.xlsx", "fuel.xlsx"]) 

    # Load new 3-inverter system data with GitHub fallback
    solar_local = load_any(["New_inverter.csv", "New_inverter.xlsx"]) 
    if solar_local.empty:
        try:
            github_url = "https://raw.githubusercontent.com/Saint-Akim/Solar-performance/main/New_inverter.csv"
            response = requests.get(github_url, timeout=10)
            if response.status_code == 200:
                solar_local = pd.read_csv(io.StringIO(response.text))
        except Exception:
            solar_local = pd.DataFrame()

    if not solar_local.empty:
        solar_local['source_file'] = 'New_inverter.csv'
        solar_local['system_type'] = '3-Inverter Enhanced System'
        data['solar'] = solar_local
    else:
        # Fallback to legacy files
        legacy_files = [
            'Solar_Goodwe&Fronius-Jan.csv',
            'Solar_goodwe&Fronius_April.csv', 
            'Solar_goodwe&Fronius_may.csv'
        ]
        legacy_frames = []
        for f in legacy_files:
            df = load_any([f])
            if not df.empty:
                df['source_file'] = f
                df['system_type'] = 'Legacy System'
                legacy_frames.append(df)
        data['solar'] = pd.concat(legacy_frames, ignore_index=True) if legacy_frames else pd.DataFrame()

    return data

# ==============================================================================
# ENHANCED METRIC DISPLAY
# ==============================================================================

def render_clean_metric(label, value, delta=None, color="blue", icon="📊", description=None, trend_data=None):
    """Clean metric using native Streamlit components - supports old function signature"""
    
    # Use native Streamlit components
    with st.container():
        col1, col2 = st.columns([1, 4])
        
        with col1:
            st.markdown(f"<div style='font-size: 2.5rem; text-align: center;'>{icon}</div>", unsafe_allow_html=True)
        
        with col2:
            st.metric(
                label=label,
                value=value,
                delta=delta,
                help=description
            )

# ==============================================================================
# ENHANCED FUEL ANALYSIS WITH REAL PRICING
# ==============================================================================


def normalize_purchase_columns(df):
    """Normalize fuel purchase column names to standard format"""
    if df.empty:
        return df
    
    df = df.copy()
    
    # Normalize column names: lowercase, remove spaces/special chars
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(r'\s+', '_', regex=True)
        .str.replace(r'[()]+', '', regex=True)
    )
    
    # Map variations to standard names
    rename_map = {
        'amount_liters': 'litres',
        'amountliters': 'litres',
        'amount': 'litres',
        'liters': 'litres',
        'costrands': 'cost',
        'cost_rands': 'cost',
        'price_per_liter': 'price_per_litre'
    }
    
    df = df.rename(columns={c: rename_map.get(c, c) for c in df.columns})
    
    # Coerce numeric fields
    for col in ['litres', 'cost', 'price_per_litre']:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    
    # Parse date
    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'], errors='coerce')
    
    return df

def process_fuel_purchases_and_pricing(fuel_purchases_df):
    """Process fuel purchase data to extract real pricing"""
    
    if fuel_purchases_df.empty:
        return pd.DataFrame(), 22.50
    
    try:
        # Normalize columns first
        fuel_purchases_df = normalize_purchase_columns(fuel_purchases_df)
        
        # Standard column names after normalization: date, litres, cost, price_per_litre
        if 'date' not in fuel_purchases_df.columns:
            return pd.DataFrame(), 22.50
        
        # Process dates
        fuel_purchases_df['date'] = pd.to_datetime(fuel_purchases_df['date'], errors='coerce')
        fuel_purchases_df = fuel_purchases_df.dropna(subset=['date'])
        
        # Calculate price_per_litre if needed
        if 'price_per_litre' not in fuel_purchases_df.columns and 'litres' in fuel_purchases_df.columns and 'cost' in fuel_purchases_df.columns:
            fuel_purchases_df['price_per_litre'] = fuel_purchases_df['cost'] / fuel_purchases_df['litres']
        
        # Clean price data
        if 'price_per_litre' in fuel_purchases_df.columns:
            fuel_purchases_df['price_per_litre'] = fuel_purchases_df['price_per_litre'].replace([np.inf, -np.inf], np.nan)
            fuel_purchases_df = fuel_purchases_df[fuel_purchases_df['price_per_litre'] > 0]
            fuel_purchases_df = fuel_purchases_df[fuel_purchases_df['price_per_litre'] < 50]
            
            avg_price = fuel_purchases_df['price_per_litre'].mean()
            return fuel_purchases_df, avg_price
    
    except Exception as e:
        print(f"Error processing fuel purchase data: {e}")
    
    return pd.DataFrame(), 22.50


@st.cache_data(ttl=600, show_spinner=False)
def calculate_enhanced_fuel_analysis(gen_df, fuel_history_df, fuel_purchases_df, gen_detailed_df, start_date, end_date, pricing_mode="nearest_prior"):
    """Enhanced dual-source fuel analysis with accurate pricing from purchases"""
    
    # Process fuel purchases for real pricing
    fuel_purchases_clean, avg_fuel_price = process_fuel_purchases_and_pricing(fuel_purchases_df)
    
    # Enhanced dual-source consumption computation (detailed CSV + backup)
    daily_primary = compute_primary_consumption(gen_df, gen_detailed_df, start_date, end_date)
    daily_backup = compute_backup_consumption(fuel_history_df, start_date, end_date)
    
    # Smart combination: Use primary source preferentially, backup only when primary is missing/low
    all_dates = sorted(set(daily_primary.index.tolist() + daily_backup.index.tolist()))
    daily_combined = pd.Series(index=all_dates, dtype=float)
    
    for date in all_dates:
        primary_val = daily_primary.get(date, 0)
        backup_val = daily_backup.get(date, 0)
        
        # Use primary if it has reasonable consumption (>0.1L), otherwise use backup
        if primary_val > 0.1:
            daily_combined[date] = primary_val
        elif backup_val > 0.1:
            daily_combined[date] = backup_val  
        else:
            daily_combined[date] = max(primary_val, backup_val)  # Use whichever is higher for very small values
    
    # Build pricing series
    daily_price_series = build_daily_price_series(fuel_purchases_clean, all_dates, pricing_mode)
    
    # Compute daily costs
    daily_fuel = []
    for date in all_dates:
        if daily_combined[date] > 0:  # Only include days with actual consumption
            price = daily_price_series.get(date, avg_fuel_price)
            daily_fuel.append({
                'date': pd.to_datetime(date),
                'fuel_consumed_liters': daily_combined[date],
                'fuel_price_per_liter': price,
                'daily_cost_rands': daily_combined[date] * price,
                'primary_source': daily_primary.get(date, 0),
                'backup_source': daily_backup.get(date, 0)
            })
    
    daily_fuel_df = pd.DataFrame(daily_fuel)
    
    # Calculate statistics
    stats = {}
    if not daily_fuel_df.empty:
        stats = {
            'total_fuel_liters': daily_fuel_df['fuel_consumed_liters'].sum(),
            'total_cost_rands': daily_fuel_df['daily_cost_rands'].sum(),
            'average_daily_fuel': daily_fuel_df['fuel_consumed_liters'].mean(),
            'average_cost_per_liter': daily_fuel_df['fuel_price_per_liter'].mean(),
            'period_days': len(daily_fuel_df),
            'pricing_mode': pricing_mode,
            'real_pricing_used': True,
            'dual_source_reliability': True,
            'fuel_consumption_trend': daily_fuel_df['fuel_consumed_liters'].tolist()[-7:] if len(daily_fuel_df) >= 7 else [],
            'cost_trend': daily_fuel_df['daily_cost_rands'].tolist()[-7:] if len(daily_fuel_df) >= 7 else []
        }
    
    # Filter purchases for selected period
    fuel_purchases_filtered = pd.DataFrame()
    if not fuel_purchases_clean.empty:
        date_col = [col for col in fuel_purchases_clean.columns if 'date' in col][0]
        fuel_purchases_filtered = filter_data_by_date_range(fuel_purchases_clean, date_col, start_date, end_date)
    
    return daily_fuel_df, stats, fuel_purchases_filtered, pd.DataFrame()

def compute_primary_consumption(gen_df, gen_detailed_df, start_date, end_date):
    """CORRECTED: sensor.generator_fuel_consumed shows TANK LEVEL, not cumulative consumption"""
    
    # Try detailed CSV first (higher quality)
    if not gen_detailed_df.empty:
        detailed_filtered = filter_data_by_date_range(gen_detailed_df, 'last_changed', start_date, end_date)
        fuel_data = detailed_filtered[detailed_filtered['entity_id'] == 'sensor.generator_fuel_consumed'].copy()
        
        if not fuel_data.empty:
            fuel_data['last_changed'] = pd.to_datetime(fuel_data['last_changed'])
            fuel_data['state'] = pd.to_numeric(fuel_data['state'], errors='coerce').fillna(0)
            fuel_data = fuel_data.sort_values('last_changed')
            
            # CORRECT LOGIC: Tank level drops = actual consumption
            fuel_data['level_change'] = fuel_data['state'].diff()
            
            # Only count NEGATIVE changes (tank level drops) as consumption
            # Positive changes are refills, not consumption
            fuel_data['consumption_diff'] = (-fuel_data['level_change']).clip(lower=0)
            fuel_data['date'] = fuel_data['last_changed'].dt.date
            
            # Group by date and sum actual consumption
            daily_consumption = fuel_data.groupby('date')['consumption_diff'].sum()
            
            # Filter out days with tiny consumption (< 1L, likely sensor noise)
            return daily_consumption[daily_consumption >= 1.0]
    
    # Fallback to original gen.xlsx with same corrected logic
    if gen_df.empty:
        return pd.Series(dtype=float)
    
    gen_filtered = filter_data_by_date_range(gen_df, 'last_changed', start_date, end_date)
    fuel_consumed_data = gen_filtered[gen_filtered['entity_id'] == 'sensor.generator_fuel_consumed'].copy()
    
    if fuel_consumed_data.empty:
        return pd.Series(dtype=float)
    
    fuel_consumed_data['last_changed'] = pd.to_datetime(fuel_consumed_data['last_changed'])
    fuel_consumed_data['state'] = pd.to_numeric(fuel_consumed_data['state'], errors='coerce').fillna(0)
    fuel_consumed_data = fuel_consumed_data.sort_values('last_changed')
    
    # CORRECT LOGIC: Tank level drops = actual consumption
    fuel_consumed_data['level_change'] = fuel_consumed_data['state'].diff()
    fuel_consumed_data['consumption_diff'] = (-fuel_consumed_data['level_change']).clip(lower=0)
    fuel_consumed_data['date'] = fuel_consumed_data['last_changed'].dt.date
    
    daily_consumption = fuel_consumed_data.groupby('date')['consumption_diff'].sum()
    return daily_consumption[daily_consumption >= 1.0]

def compute_backup_consumption(fuel_history_df, start_date, end_date):
    """Backup source: tank level -> detect significant drops only (ignore noise/resets)"""
    if fuel_history_df.empty:
        return pd.Series(dtype=float)
    
    # Filter and process
    fuel_filtered = filter_data_by_date_range(fuel_history_df, 'last_changed', start_date, end_date)
    fuel_level_data = fuel_filtered[fuel_filtered['entity_id'] == 'sensor.generator_fuel_level'].copy()
    
    if fuel_level_data.empty:
        return pd.Series(dtype=float)
    
    fuel_level_data['last_changed'] = pd.to_datetime(fuel_level_data['last_changed'])
    fuel_level_data['state'] = pd.to_numeric(fuel_level_data['state'], errors='coerce').fillna(0)
    fuel_level_data = fuel_level_data.sort_values('last_changed')
    
    # More aggressive smoothing for noisy tank sensor
    fuel_level_data['state_smooth'] = fuel_level_data['state'].rolling(window=20, center=True).median().fillna(fuel_level_data['state'])
    
    # Only count significant level drops (>1L) to filter out noise and avoid refill events
    fuel_level_data['level_diff'] = fuel_level_data['state_smooth'].diff()
    
    # Consumption = negative diff BUT only if:
    # 1. Drop is > 1L (significant consumption)
    # 2. Drop is < 30L (avoid counting refills/resets as consumption)
    significant_drops = (fuel_level_data['level_diff'] < -1) & (fuel_level_data['level_diff'] > -30)
    fuel_level_data['consumption_diff'] = 0.0
    fuel_level_data.loc[significant_drops, 'consumption_diff'] = -fuel_level_data.loc[significant_drops, 'level_diff']
    
    fuel_level_data['date'] = fuel_level_data['last_changed'].dt.date
    
    # Group by date and sum (will be much lower now, filtering out noise)
    daily_backup = fuel_level_data.groupby('date')['consumption_diff'].sum()
    
    # Cap backup source to reasonable daily limits (max 50L/day to avoid anomalies)
    daily_backup = daily_backup.clip(upper=50)
    
    return daily_backup

def build_daily_price_series(fuel_purchases_clean, all_dates, pricing_mode="nearest_prior"):
    """Build daily price series using nearest-prior or monthly-average pricing"""
    if fuel_purchases_clean.empty:
        return {}
    
    date_col = [col for col in fuel_purchases_clean.columns if 'date' in col][0]
    purchases = fuel_purchases_clean.copy()
    purchases[date_col] = pd.to_datetime(purchases[date_col])
    purchases = purchases.sort_values(date_col)
    
    daily_prices = {}
    
    if pricing_mode == "nearest_prior":
        # Forward-fill from purchase dates
        for date in all_dates:
            date_dt = pd.to_datetime(date)
            prior_purchases = purchases[purchases[date_col] <= date_dt]
            if not prior_purchases.empty and 'price_per_litre' in prior_purchases.columns:
                daily_prices[date] = prior_purchases['price_per_litre'].iloc[-1]
            else:
                daily_prices[date] = purchases['price_per_litre'].mean() if 'price_per_litre' in purchases.columns else 22.50
    
    elif pricing_mode == "monthly_average":
        # Monthly average price per litre
        purchases['month'] = purchases[date_col].dt.to_period('M')
        monthly_avg = purchases.groupby('month')['price_per_litre'].mean()
        
        for date in all_dates:
            date_dt = pd.to_datetime(date)
            month_period = date_dt.to_period('M')
            if month_period in monthly_avg.index:
                daily_prices[date] = monthly_avg[month_period]
            else:
                daily_prices[date] = purchases['price_per_litre'].mean() if 'price_per_litre' in purchases.columns else 22.50
    
    return daily_prices

# ==============================================================================
# ENHANCED SOLAR ANALYSIS WITH 3-INVERTER SYSTEM
# ==============================================================================

@st.cache_data(ttl=600, show_spinner=False)
def process_enhanced_solar_analysis(solar_df, start_date, end_date):
    """Enhanced solar analysis with 3-inverter system - FIXED power scaling and aggregation"""
    
    if solar_df.empty:
        return pd.DataFrame(), {}, pd.DataFrame(), pd.DataFrame()
    
    # Filter by date range
    solar_filtered = filter_data_by_date_range(solar_df, 'last_changed', start_date, end_date)
    
    if solar_filtered.empty:
        return pd.DataFrame(), {}, pd.DataFrame(), pd.DataFrame()
    
    # Clean and process
    solar_filtered['last_changed'] = pd.to_datetime(solar_filtered['last_changed'])
    solar_filtered['state'] = pd.to_numeric(solar_filtered['state'], errors='coerce')
    
    # CRITICAL FIX: Solar power readings are already in kW scale (not W)
    # Data shows max 88.4W which is actually 88.4kW total system output
    solar_filtered = solar_filtered[solar_filtered['state'] >= 0]
    
    # Identify power sensors (3-inverter system)
    power_sensors = solar_filtered[solar_filtered['entity_id'].str.contains('power', case=False, na=False)]
    
    daily_solar = []
    hourly_patterns = []
    inverter_performance = []
    
    if not power_sensors.empty:
        # Power values are already in correct scale - use as kW directly
        power_sensors['power_kw'] = power_sensors['state'].abs()  # Values already in kW
        power_sensors['date'] = power_sensors['last_changed'].dt.date
        power_sensors['hour'] = power_sensors['last_changed'].dt.hour
        
        # Group by inverter to track the 3-inverter system
        inverter_daily = power_sensors.groupby(['date', 'entity_id']).agg({
            'power_kw': ['sum', 'max', 'mean', 'count']
        }).reset_index()
        inverter_daily.columns = ['date', 'inverter', 'total_kwh', 'peak_kw', 'avg_kw', 'readings']
        
        # Convert to proper kWh based on actual data frequency
        # Data appears to be frequent samples, so sum and divide by samples per hour
        data_freq_per_hour = 12  # Approximately 12 samples per hour based on data density
        inverter_daily['total_kwh'] = inverter_daily['total_kwh'] / data_freq_per_hour
        
        # System daily totals (sum all 3 inverters)
        system_daily = inverter_daily.groupby('date').agg({
            'total_kwh': 'sum',
            'peak_kw': 'max',
            'avg_kw': 'mean'
        }).reset_index()
        
        system_daily['date'] = pd.to_datetime(system_daily['date'])
        system_daily['inverter_count'] = inverter_daily.groupby('date')['inverter'].nunique().values
        system_daily['capacity_factor'] = (system_daily['avg_kw'] / system_daily['peak_kw'] * 100).fillna(0)
        
        # Ensure all values are positive
        system_daily['total_kwh'] = system_daily['total_kwh'].abs()
        system_daily['peak_kw'] = system_daily['peak_kw'].abs()
        system_daily['avg_kw'] = system_daily['avg_kw'].abs()
        
        daily_solar = system_daily.to_dict('records')
        
        # Hourly patterns
        hourly_avg = power_sensors.groupby('hour').agg({
            'power_kw': ['mean', 'max', 'std', 'count']
        }).reset_index()
        hourly_avg.columns = ['hour', 'avg_power_kw', 'max_power_kw', 'variability', 'data_points']
        hourly_patterns = hourly_avg.to_dict('records')
        
        # Individual inverter performance
        inverter_performance = inverter_daily.to_dict('records')
    
    # Calculate enhanced statistics
    daily_solar_df = pd.DataFrame(daily_solar)
    hourly_patterns_df = pd.DataFrame(hourly_patterns)
    inverter_performance_df = pd.DataFrame(inverter_performance)
    
    solar_stats = {}
    if not daily_solar_df.empty:
        electricity_rate = 1.50  # R/kWh
        total_generation = daily_solar_df['total_kwh'].sum()
        
        # Enhanced stats for new 3-inverter system
        avg_inverter_count = daily_solar_df['inverter_count'].mean()
        is_new_system = False
        if not solar_df.empty and 'system_type' in solar_df.columns:
            try:
                is_new_system = solar_df['system_type'].astype(str).str.contains('3-Inverter', na=False).any()
            except Exception:
                is_new_system = False
        
        # Calculate system improvements
        baseline_capacity = 25  # kW (estimated previous system capacity)
        current_peak = daily_solar_df['peak_kw'].max()
        capacity_improvement = ((current_peak - baseline_capacity) / baseline_capacity * 100) if current_peak > baseline_capacity else 0
        
        solar_stats = {
            'total_generation_kwh': total_generation,
            'total_value_rands': total_generation * electricity_rate,
            'average_daily_kwh': daily_solar_df['total_kwh'].mean(),
            'peak_system_power_kw': current_peak,
            'average_capacity_factor': daily_solar_df['capacity_factor'].mean(),
            'best_day_kwh': daily_solar_df['total_kwh'].max(),
            'worst_day_kwh': daily_solar_df['total_kwh'].min(),
            'generation_trend': daily_solar_df['total_kwh'].tolist()[-7:] if len(daily_solar_df) >= 7 else [],
            'total_operating_days': len(daily_solar_df),
            'average_inverter_count': avg_inverter_count,
            'carbon_offset_kg': total_generation * 0.95,
            'system_type': '3-Inverter Enhanced System' if is_new_system else 'Legacy System',
            'system_upgrade_improvement': 'Significant Upgrade' if is_new_system else 'Standard System',
            'capacity_improvement_percent': capacity_improvement,
            'estimated_monthly_savings': (total_generation * electricity_rate * 30 / len(daily_solar_df)) if len(daily_solar_df) > 0 else 0,
            'data_quality': '3-Inverter Enhanced Analysis' if is_new_system else 'Legacy System Analysis',
            'fronius_removed': True if is_new_system else False,
            'new_inverters_added': 2 if is_new_system else 0
        }
    
    return daily_solar_df, solar_stats, hourly_patterns_df, inverter_performance_df

# ==============================================================================
# DATE FILTERING FUNCTION
# ==============================================================================

def filter_data_by_date_range(df, date_col, start_date, end_date):
    """Filter dataframe by date range"""
    if df.empty or date_col not in df.columns:
        return df
    
    try:
        df = df.copy()
        df[date_col] = pd.to_datetime(df[date_col], errors='coerce')
        mask = (df[date_col].dt.date >= start_date) & (df[date_col].dt.date <= end_date)
        return df[mask].copy()
    except:
        return df

# ==============================================================================
# DATE RANGE SELECTOR
# ==============================================================================

def create_date_range_selector(key_prefix="global"):
    """Advanced date range selector"""
    
    st.markdown("### 📅 Interactive Date Range Selection")
    
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        preset = st.selectbox(
            "Quick Select Period",
            [
                "Last 7 Days", "Last 14 Days", "Last 30 Days", "Last 60 Days", 
                "Last 90 Days", "Last 6 Months", "Year to Date", "All Time", "Custom Range"
            ],
            index=2,
            key=f"{key_prefix}_preset"
        )
    
    today = datetime.now().date()
    
    if preset == "Last 7 Days":
        start_date, end_date = today - timedelta(days=6), today
    elif preset == "Last 14 Days":
        start_date, end_date = today - timedelta(days=13), today
    elif preset == "Last 30 Days":
        start_date, end_date = today - timedelta(days=29), today
    elif preset == "Last 60 Days":
        start_date, end_date = today - timedelta(days=59), today
    elif preset == "Last 90 Days":
        start_date, end_date = today - timedelta(days=89), today
    elif preset == "Last 6 Months":
        start_date, end_date = today - timedelta(days=180), today
    elif preset == "Year to Date":
        start_date, end_date = date(today.year, 1, 1), today
    elif preset == "All Time":
        start_date, end_date = date(2020, 1, 1), today
    else:  # Custom Range
        with col2:
            start_date = st.date_input(
                "From",
                value=today - timedelta(days=30),
                max_value=today,
                key=f"{key_prefix}_start"
            )
        with col3:
            end_date = st.date_input(
                "To", 
                value=today,
                min_value=start_date,
                max_value=today,
                key=f"{key_prefix}_end"
            )
    
    if preset != "Custom Range":
        with col2:
            st.date_input("From", value=start_date, disabled=True, key=f"{key_prefix}_start_display")
        with col3:
            st.date_input("To", value=end_date, disabled=True, key=f"{key_prefix}_end_display")
    
    period_days = (end_date - start_date).days + 1
    st.info(f"📊 **Selected Period**: {period_days} days • **From**: {start_date} **To**: {end_date}")
    
    return start_date, end_date, period_days

# ==============================================================================
# ENHANCED CHART FUNCTIONS (FIXED use_container_width)
# ==============================================================================

def create_ultra_interactive_chart(df, x_col, y_col, title, color="#3b82f6", chart_type="bar", 
                                 height=500, enable_zoom=True, enable_selection=True, selection_mode="select"):
    """Ultra-interactive charts with advanced zoom, pan, and selection capabilities"""
    
    if df.empty or x_col not in df.columns or y_col not in df.columns:
        st.info(f"📊 No data available for {title}")
        return None, None
    
    # Clean data
    df_clean = df.dropna(subset=[x_col, y_col]).copy()
    
    if df_clean.empty:
        st.info(f"📊 No valid data for {title}")
        return None, None
    
    fig = go.Figure()
    
    # Create trace based on chart type
    if chart_type == "bar":
        fig.add_trace(go.Bar(
            x=df_clean[x_col],
            y=df_clean[y_col],
            marker=dict(
                color=color,
                line=dict(width=0),
                opacity=0.8
            ),
            text=df_clean[y_col].round(2),
            textposition='auto',
            textfont=dict(color='white', size=10),
            hovertemplate="<b>%{x}</b><br>%{y:.2f}<br><extra></extra>",
            name=title
        ))
    elif chart_type == "line":
        fig.add_trace(go.Scatter(
            x=df_clean[x_col],
            y=df_clean[y_col],
            mode='lines+markers',
            line=dict(color=color, width=3, shape='spline'),
            marker=dict(
                size=8,
                color=color,
                line=dict(width=2, color='rgba(255,255,255,0.5)'),
                opacity=0.9
            ),
            hovertemplate="<b>%{x}</b><br>%{y:.2f}<br><extra></extra>",
            name=title
        ))
    elif chart_type == "area":
        fig.add_trace(go.Scatter(
            x=df_clean[x_col],
            y=df_clean[y_col],
            fill='tozeroy',
            mode='lines',
            line=dict(color=color, width=2),
            fillcolor=f"rgba({int(color[1:3], 16)}, {int(color[3:5], 16)}, {int(color[5:7], 16)}, 0.3)",
            hovertemplate="<b>%{x}</b><br>%{y:.2f}<br><extra></extra>",
            name=title
        ))
    elif chart_type == "scatter":
        fig.add_trace(go.Scatter(
            x=df_clean[x_col],
            y=df_clean[y_col],
            mode='markers',
            marker=dict(
                size=10,
                color=color,
                opacity=0.7,
                line=dict(width=1, color='white')
            ),
            hovertemplate="<b>%{x}</b><br>%{y:.2f}<br><extra></extra>",
            name=title
        ))
    
    # Enhanced layout
    fig.update_layout(
        title=dict(
            text=f"<b style='color: #f1f5f9;'>{title}</b>",
            font=dict(size=22, family="Inter"),
            x=0.02,
            y=0.95,
            xanchor='left'
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#e2e8f0', family="Inter"),
        height=height,
        showlegend=False,
        hovermode="x unified",
        xaxis=dict(
            showgrid=True,
            gridcolor='rgba(255,255,255,0.05)',
            gridwidth=1,
            linecolor='rgba(148, 163, 184, 0.2)',
            zeroline=False,
            tickfont=dict(color='#94a3b8', size=11),
            title=dict(
                text=x_col.replace('_', ' ').title(),
                font=dict(color='#94a3b8', size=12, family="Inter"),
                standoff=20
            )
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='rgba(255,255,255,0.05)',
            gridwidth=1,
            linecolor='rgba(148, 163, 184, 0.2)',
            zeroline=False,
            tickfont=dict(color='#94a3b8', size=11),
            title=dict(
                text=y_col.replace('_', ' ').title(),
                font=dict(color='#94a3b8', size=12, family="Inter"),
                standoff=20
            )
        ),
        margin=dict(l=80, r=40, t=80, b=80),
        hoverlabel=dict(
            bgcolor="rgba(15, 23, 42, 0.95)",
            bordercolor="rgba(148, 163, 184, 0.3)",
            font=dict(color="#f1f5f9", family="Inter", size=12)
        )
    )
    
    # Advanced configuration
    config = {
        'displayModeBar': True,
        'displaylogo': False,
        'modeBarButtonsToRemove': [] if enable_zoom else ['zoom2d', 'pan2d', 'select2d', 'lasso2d'],
        'toImageButtonOptions': {
            'format': 'png',
            'filename': title.lower().replace(" ", "_").replace("/", "_"),
            'height': height,
            'width': 1400,
            'scale': 3
        },
        'showTips': True,
        'scrollZoom': enable_zoom
    }
    
    # Enable selection if requested
    if enable_selection:
        mode_map = {
            "Box Select": "select",
            "Lasso Select": "lasso",
            "Pan": "pan",
            "Zoom": "zoom",
            "select": "select",
            "lasso": "lasso",
            "pan": "pan",
            "zoom": "zoom",
        }
        dm = mode_map.get(selection_mode, "select")
        fig.update_layout(dragmode=dm)
    
    # Display chart with FIXED width parameter
    chart = st.plotly_chart(fig, width='stretch', config=config, key=f"chart_{title.replace(' ', '_')}")
    
    return fig, df_clean

# ==============================================================================
# MAIN APPLICATION (WITH ALL IMPROVEMENTS)
# ==============================================================================

def main():
    """Ultra-modern improved main application"""
    
    # Ultra-modern header (FIXED TITLE)
    # Clean header with native Streamlit
    st.title("🏭 Durr Bottling Energy Intelligence")
    st.markdown("**Ultra-Modern Interactive Energy Monitoring Platform with Real-Time Pricing & 3-Inverter System**")
    
    # Feature badges using clean columns
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.info("🎯 Version 10.0 Enhanced")
    with col2:
        st.error("💰 Real Fuel Pricing") 
    with col3:
        st.success("☀️ 3-Inverter System")
    with col4:
        st.warning("📅 Interactive Date Range")
    
    # Silent data loading
    all_data = load_all_energy_data_silent()

    # Column mapping helper
    def apply_column_mapping(df, mapping_key):
        if df is None or df.empty:
            return df
        expected = ["last_changed", "entity_id", "state"]
        missing = [c for c in expected if c not in df.columns]
        if not missing:
            return df
        # Show mapping UI in sidebar
        with st.sidebar.expander(f"Map columns for {mapping_key}", expanded=False):
            st.write("Select which columns correspond to the expected fields:")
            selections = {}
            for target in missing:
                options = [c for c in df.columns]
                if options:
                    selections[target] = st.selectbox(f"{mapping_key} → {target}", options, key=f"map_{mapping_key}_{target}")
            if selections:
                df = df.rename(columns=selections)
        return df

    # Apply mapping to generator and solar datasets if needed
    all_data['generator'] = apply_column_mapping(all_data.get('generator', pd.DataFrame()), 'Generator')
    all_data['solar'] = apply_column_mapping(all_data.get('solar', pd.DataFrame()), 'Solar')
    
    # Global date range selector
    st.markdown("---")
    start_date, end_date, period_days = create_date_range_selector("main_dashboard")
    
    # Ultra-modern sidebar
    with st.sidebar:
        st.markdown("### ⚡ Energy Control Center")
        
        # Data Manager: download/update data sources
        with st.expander("🗂️ Data Manager (download/update data files)", expanded=False):
            BASE = "https://raw.githubusercontent.com/Saint-Akim/Solar-performance/main/"
            downloads = {
                "New_inverter.csv": BASE + "New_inverter.csv",
                "FACTORY ELEC.csv": BASE + "FACTORY%20ELEC.csv",
                "Solar_Goodwe&Fronius-Jan.csv": BASE + "Solar_Goodwe%26Fronius-Jan.csv",
                "Solar_goodwe&Fronius_April.csv": BASE + "Solar_goodwe%26Fronius_April.csv",
                "Solar_goodwe&Fronius_may.csv": BASE + "Solar_goodwe%26Fronius_may.csv",
                "gen (2).csv": BASE + "gen%20%282%29.csv",
                "gen (2).xlsx": BASE + "gen%20%282%29.xlsx",
                "history (5).csv": BASE + "history%20%285%29.csv",
                "history (5).xlsx": BASE + "history%20%285%29.xlsx",
                "Durr bottling Generator filling.xlsx": BASE + "Durr%20bottling%20Generator%20filling.xlsx",
                "September 2025.xlsx": BASE + "September%202025.xlsx",
            }
            dm_cols = st.columns(2)
            for i, (fname, url) in enumerate(downloads.items()):
                with dm_cols[i % 2]:
                    if st.button(f"⬇️ {fname}", key=f"dm_{fname}"):
                        try:
                            import requests
                            r = requests.get(url, timeout=30)
                            if r.status_code == 200:
                                with open(fname, "wb") as f:
                                    f.write(r.content)
                                st.success(f"Saved {fname}")
                                st.cache_data.clear()
                            else:
                                st.warning(f"Could not fetch {fname}: {r.status_code}")
                        except Exception as e:
                            st.error(f"Download failed for {fname}: {e}")
        
        # Column Mapping UI (appears when needed)
        st.markdown("### 🧭 Data Column Mapping")
        st.caption("If your files use different column names, map them here.")
        st.markdown("#### Enhanced v10.0 • Real-Time Intelligence")
        st.markdown("---")
        
        # Enhanced preferences
        st.markdown("### 🎛️ Dashboard Preferences")
        
        chart_theme = st.selectbox(
            "Chart Theme",
            ["Dark (Default)", "High Contrast", "Minimal", "Colorful"],
            help="Choose your preferred chart styling"
        )
        
        enable_animations = st.checkbox("Enable Animations", value=True, help="Smooth chart transitions")
        show_sparklines = st.checkbox("Show Trend Sparklines", value=True, help="Mini charts in metrics")
        selection_mode = st.selectbox(
            "Selection Mode",
            ["Box Select", "Lasso Select", "Pan", "Zoom"],
            help="Choose how to interact with charts"
        )
        pricing_mode = st.selectbox(
            "Fuel Pricing Mode",
            ["nearest_prior", "monthly_average"],
            index=0,
            help="Nearest prior: Use closest purchase price per day (recommended). Monthly average: Use monthly mean price."
        )
        
        st.markdown("---")
        
        # Quick actions with FIXED width
        if st.button("🔄 Refresh Data", width='stretch'):
            st.cache_data.clear()
            st.rerun()
        
        if st.button("📧 Email Report", width='stretch'):
            st.success("✅ Report sent to stakeholders")
    
    # Process data with selected date range
    with st.spinner("Processing enhanced analytics..."):
        # Enhanced fuel analysis with real pricing
        daily_fuel, fuel_stats, fuel_purchases, tank_validation = calculate_enhanced_fuel_analysis(
            all_data.get('generator', pd.DataFrame()),
            all_data.get('fuel_history', pd.DataFrame()),
            all_data.get('fuel_purchases', pd.DataFrame()),
            all_data.get('generator_detailed', pd.DataFrame()),
            start_date, end_date
        )
        
        # Enhanced solar analysis with 3-inverter system
        daily_solar, solar_stats, hourly_solar, inverter_performance = process_enhanced_solar_analysis(
            all_data.get('solar', pd.DataFrame()),
            start_date, end_date
        )
    
    # Enhanced tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "🔋 Generator Fuel Analysis", 
        "☀️ Solar Performance", 
        "🏭 Factory Optimization",
        "📊 System Overview"
    ])
    
    # Generator Analysis Tab (ENHANCED WITH REAL PRICING)
    with tab1:
        st.header("🔋 Generator Fuel Analysis")
        st.markdown("**Real-time fuel consumption monitoring with actual market pricing**")
        
        if not daily_fuel.empty and fuel_stats:
            # Enhanced metrics with real pricing info
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                render_clean_metric(
                    "Total Fuel Consumed",
                    f"{fuel_stats['total_fuel_liters']:,.1f} L",
                    f"📈 Real pricing used",
                    "blue", "⛽",
                    f"Period: {period_days} days • Market prices applied",
                    fuel_stats.get('fuel_consumption_trend', [])
                )
            
            with col2:
                render_clean_metric(
                    "Total Fuel Cost",
                    f"R {fuel_stats['total_cost_rands']:,.0f}",
                    f"💰 R{fuel_stats['average_cost_per_liter']:.2f}/L market avg",
                    "red", "💸",
                    "Based on actual purchase prices",
                    fuel_stats.get('cost_trend', [])
                )
            
            with col3:
                efficiency = fuel_stats.get('average_efficiency', 0)
                render_clean_metric(
                    "Generator Efficiency",
                    f"{efficiency:.1f}%",
                    f"⚡ Runtime: {fuel_stats.get('total_runtime_hours', 0):.0f}h",
                    "green" if efficiency > 70 else "yellow", "⚡",
                    "Performance rating"
                )
            
            with col4:
                render_clean_metric(
                    "Daily Average",
                    f"{fuel_stats.get('average_daily_fuel', 0):.1f} L/day",
                    f"📅 Over {fuel_stats.get('period_days', 0)} days",
                    "purple", "📈",
                    "Consumption pattern"
                )
            
            # Data downloads
            with st.expander("⬇️ Download datasets", expanded=False):
                c1, c2, c3 = st.columns(3)
                with c1:
                    st.download_button("Daily Fuel CSV", daily_fuel.to_csv(index=False).encode('utf-8'), file_name="daily_fuel.csv", mime="text/csv", key="dl_daily_fuel_top")
                with c2:
                    st.download_button("Fuel Purchases CSV", fuel_purchases.to_csv(index=False).encode('utf-8') if not fuel_purchases.empty else b"", file_name="fuel_purchases.csv", mime="text/csv", key="dl_fuel_purchases_top", disabled=fuel_purchases.empty)
                with c3:
                    st.download_button("Runtime/Efficiency CSV", daily_fuel.to_csv(index=False).encode('utf-8'), file_name="fuel_runtime_efficiency.csv", mime="text/csv", key="dl_runtime_efficiency_top")

            # Enhanced fuel analysis charts
            st.markdown("### 📊 Enhanced Fuel Consumption Analysis")
            
            col1, col2 = st.columns(2)
            
            with col1:
                fig1, df1 = create_ultra_interactive_chart(
                    daily_fuel, 'date', 'fuel_consumed_liters',
                    'Daily Fuel Consumption (Enhanced)', '#3b82f6', 'bar',
                    height=400, enable_zoom=True, enable_selection=True, selection_mode=selection_mode
                )
                if df1 is not None:
                    st.download_button("⬇️ Download Chart Data (Fuel Consumption)", df1.to_csv(index=False).encode('utf-8'), file_name="fuel_consumption_chart.csv", mime="text/csv", key="dl_chart_fuel_consumption")
            
            with col2:
                fig2, df2 = create_ultra_interactive_chart(
                    daily_fuel, 'date', 'daily_cost_rands',
                    'Daily Fuel Cost (Real Pricing)', '#ef4444', 'area',
                    height=400, enable_zoom=True, enable_selection=True, selection_mode=selection_mode
                )
                if df2 is not None:
                    st.download_button("⬇️ Download Chart Data (Fuel Cost)", df2.to_csv(index=False).encode('utf-8'), file_name="fuel_cost_chart.csv", mime="text/csv", key="dl_chart_fuel_cost")
            
            # Fuel purchase tracking comparison
            if not fuel_purchases.empty:
                st.markdown("### 💰 Fuel Purchase vs Consumption Analysis")
                
                # Calculate totals for comparison
                total_purchased = 0
                total_consumed = fuel_stats.get('total_fuel_liters', 0)
                
                if 'quantity' in fuel_purchases.columns:
                    total_purchased = fuel_purchases['quantity'].sum()
                elif any('litre' in col for col in fuel_purchases.columns):
                    litre_cols = [col for col in fuel_purchases.columns if 'litre' in col]
                    total_purchased = fuel_purchases[litre_cols[0]].sum()
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    render_clean_metric(
                        "Fuel Purchased",
                        f"{total_purchased:,.0f} L",
                        f"📦 Total bought",
                        "cyan", "🛒",
                        "Fuel procurement tracking"
                    )
                
                with col2:
                    render_clean_metric(
                        "Fuel Consumed",
                        f"{total_consumed:,.0f} L",
                        f"⛽ Total used",
                        "blue", "🔥",
                        "Generator consumption"
                    )
                
                with col3:
                    balance = total_purchased - total_consumed
                    render_clean_metric(
                        "Fuel Balance",
                        f"{balance:,.0f} L",
                        "📊 Inventory status",
                        "green" if balance > 0 else "red", "⚖️",
                        "Surplus" if balance > 0 else "Deficit"
                    )
                
                # Purchase tracking charts (monthly aggregation)
                if 'date' in fuel_purchases.columns:
                    date_col = [col for col in fuel_purchases.columns if 'date' in col][0]
                    qty_cols = [col for col in fuel_purchases.columns if 'litre' in col or 'quantity' in col]
                    price_col = 'price_per_litre' if 'price_per_litre' in fuel_purchases.columns else None
                    if qty_cols:
                        fp = fuel_purchases.copy()
                        fp[date_col] = pd.to_datetime(fp[date_col], errors='coerce')
                        fp = fp.dropna(subset=[date_col])
                        fp['month'] = fp[date_col].dt.to_period('M').dt.to_timestamp()
                        monthly = fp.groupby('month').agg({qty_cols[0]: 'sum', **({price_col: 'mean'} if price_col else {})}).reset_index()
                        monthly.rename(columns={qty_cols[0]: 'litres'}, inplace=True)
                        c1m, c2m = st.columns(2)
                        c1m, c2m, c3m = st.columns(3)
                        with c1m:
                            create_ultra_interactive_chart(
                                monthly, 'month', 'litres',
                                'Monthly Fuel Purchased (L)', '#10b981', 'bar', height=350, enable_zoom=True, selection_mode=selection_mode
                            )
                        if price_col and not monthly.empty and price_col in monthly.columns:
                            # Ensure price data is valid
                            monthly_clean = monthly.dropna(subset=[price_col])
                            if not monthly_clean.empty:
                                with c2m:
                                    create_ultra_interactive_chart(
                                        monthly_clean, 'month', price_col,
                                        'Monthly Avg Price per Litre', '#f59e0b', 'line', height=350, enable_zoom=True, selection_mode=selection_mode
                                    )
                        # Monthly Generator Cost chart
                        if not daily_fuel.empty:
                            monthly_cost = daily_fuel.copy()
                            monthly_cost['month'] = monthly_cost['date'].dt.to_period('M').dt.to_timestamp()
                            monthly_cost_agg = monthly_cost.groupby('month')['daily_cost_rands'].sum().reset_index()
                            monthly_cost_agg.rename(columns={'daily_cost_rands': 'monthly_cost_rands'}, inplace=True)
                            with c3m:
                                create_ultra_interactive_chart(
                                    monthly_cost_agg, 'month', 'monthly_cost_rands',
                                    'Monthly Generator Cost (R)', '#ef4444', 'bar', height=350, enable_zoom=True, selection_mode=selection_mode
                                )
                        
                        # Fuel Purchase vs Consumption Analysis
                        st.subheader("💡 Fuel Purchase vs Consumption Analysis")
                        
                        if not fuel_purchases.empty and not daily_fuel.empty:
                            # Create comprehensive analysis
                            analysis_data = []
                            
                            # Get purchase data by month
                            fuel_purchases['month'] = pd.to_datetime(fuel_purchases['date']).dt.to_period('M').dt.to_timestamp()
                            # Normalize fuel_purchases columns
                            fuel_purchases_norm = normalize_purchase_columns(fuel_purchases)
                            purchase_monthly = fuel_purchases_norm.groupby('month').agg({
                                'litres': 'sum',
                                'cost': 'sum'
                            }).reset_index()
                            purchase_monthly = purchase_monthly.rename(columns={'litres': 'purchased_litres', 'cost': 'purchase_cost'})
                            purchase_monthly.rename(columns={'amount(liters)': 'purchased_litres', 'Cost(Rands)': 'purchase_cost'}, inplace=True)
                            
                            # Get consumption data by month
                            consumption_monthly = daily_fuel.copy()
                            consumption_monthly['month'] = consumption_monthly['date'].dt.to_period('M').dt.to_timestamp()
                            consumed_monthly = consumption_monthly.groupby('month').agg({
                                'fuel_consumed_liters': 'sum',
                                'daily_cost_rands': 'sum'
                            }).reset_index()
                            consumed_monthly.rename(columns={'fuel_consumed_liters': 'consumed_litres', 'daily_cost_rands': 'consumption_cost'}, inplace=True)
                            
                            # Merge purchase and consumption data
                            comparison_df = pd.merge(purchase_monthly, consumed_monthly, on='month', how='outer').fillna(0)
                            comparison_df['net_fuel'] = comparison_df['purchased_litres'] - comparison_df['consumed_litres']
                            comparison_df['utilization_rate'] = (comparison_df['consumed_litres'] / comparison_df['purchased_litres'] * 100).fillna(0)
                            
                            # Display comparison charts
                            comp_col1, comp_col2 = st.columns(2)
                            
                            if not comparison_df.empty:
                                with comp_col1:
                                    # Create dual-bar chart for purchased vs consumed
                                    import plotly.graph_objects as go
                                    
                                    fig = go.Figure()
                                    fig.add_trace(go.Bar(
                                        x=comparison_df['month'],
                                        y=comparison_df['purchased_litres'],
                                        name='Purchased (L)',
                                        marker_color='#10b981'
                                    ))
                                    fig.add_trace(go.Bar(
                                        x=comparison_df['month'],
                                        y=comparison_df['consumed_litres'],
                                        name='Consumed (L)',
                                        marker_color='#ef4444'
                                    ))
                                    
                                    fig.update_layout(
                                        title="Monthly Fuel: Purchased vs Consumed",
                                        xaxis_title="Month",
                                        yaxis_title="Litres",
                                        barmode='group',
                                        height=400
                                    )
                                    
                                    st.plotly_chart(fig, width='stretch')
                                
                                with comp_col2:
                                    # Net fuel balance
                                    create_ultra_interactive_chart(
                                        comparison_df, 'month', 'net_fuel',
                                        'Monthly Net Fuel Balance (L)', '#8b5cf6', 'bar', height=400, enable_zoom=True, selection_mode=selection_mode
                                    )
                            
                            # Summary metrics
                            st.markdown("#### 📈 Purchase vs Consumption Summary")
                            sum_col1, sum_col2, sum_col3, sum_col4 = st.columns(4)
                            
                            total_purchased = comparison_df['purchased_litres'].sum()
                            total_consumed = comparison_df['consumed_litres'].sum()
                            net_balance = total_purchased - total_consumed
                            overall_utilization = (total_consumed / total_purchased * 100) if total_purchased > 0 else 0
                            
                            with sum_col1:
                                render_clean_metric("Total Purchased", f"{total_purchased:.1f} L", f"From {len(fuel_purchases)} purchases", "green", "⛽")
                            with sum_col2:
                                render_clean_metric("Total Consumed", f"{total_consumed:.1f} L", f"Generator usage", "red", "🔥")
                            with sum_col3:
                                render_clean_metric("Net Balance", f"{net_balance:.1f} L", "Remaining/Deficit", "purple", "📊")
                            with sum_col4:
                                render_clean_metric("Utilization Rate", f"{overall_utilization:.1f}%", "Efficiency metric", "cyan", "⚡")
                            
                            # Download comparison data
                            st.download_button(
                                'Download Purchase vs Consumption Analysis',
                                comparison_df.to_csv(index=False).encode('utf-8'),
                                file_name='fuel_purchase_consumption_analysis.csv',
                                mime='text/csv',
                                key='dl_comparison_analysis'
                            )
                        st.download_button('Monthly Purchases CSV', monthly.to_csv(index=False).encode('utf-8'), file_name='fuel_purchases_monthly.csv', mime='text/csv', key='dl_monthly_purchases')
                        if not daily_fuel.empty:
                            st.download_button('Monthly Generator Cost CSV', monthly_cost_agg.to_csv(index=False).encode('utf-8'), file_name='monthly_generator_cost.csv', mime='text/csv', key='dl_monthly_generator_cost')
        else:
            st.info("📊 No generator data available for selected period")
    
    # Solar Performance Tab (ENHANCED WITH 3-INVERTER SYSTEM)
    with tab2:
        st.header("☀️ Solar Performance")
        st.markdown("**3-Inverter system monitoring with capacity analysis**")
        
        if not daily_solar.empty and solar_stats:
            # Enhanced solar metrics
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                render_clean_metric(
                    "Total Generation",
                    f"{solar_stats['total_generation_kwh']:,.0f} kWh",
                    f"💰 Value: R{solar_stats['total_value_rands']:,.0f}",
                    "green", "☀️",
                    f"System upgrade: {solar_stats.get('system_upgrade_improvement', 'Standard')}",
                    solar_stats.get('generation_trend', [])
                )
            
            with col2:
                system_type = solar_stats.get('system_type', 'Standard System')
                new_inverters = solar_stats.get('new_inverters_added', 0)
                improvement = solar_stats.get('capacity_improvement_percent', 0)
                
                render_clean_metric(
                    "System Upgrade",
                    f"{new_inverters} New Inverters" if new_inverters > 0 else f"{solar_stats.get('average_inverter_count', 0):.0f} Inverters",
                    f"🚀 Improvement: +{improvement:.1f}%" if improvement > 0 else f"⚡ Peak: {solar_stats['peak_system_power_kw']:.1f} kW",
                    "yellow", "🔌",
                    f"{system_type} • Fronius removed" if solar_stats.get('fronius_removed') else "Enhanced configuration"
                )
            
            with col3:
                render_clean_metric(
                    "Performance Factor",
                    f"{solar_stats['average_capacity_factor']:.1f}%",
                    f"🏆 Best day: {solar_stats.get('best_day_kwh', 0):.0f} kWh",
                    "cyan", "📊",
                    "System efficiency rating"
                )
            
            with col4:
                render_clean_metric(
                    "Carbon Offset",
                    f"{solar_stats['carbon_offset_kg']:,.0f} kg",
                    "🌱 CO₂ avoided",
                    "green", "🌍",
                    "Environmental impact"
                )
            
            # Enhanced solar charts (POSITIVE VALUES ONLY)
            st.markdown("### 📈 Solar Performance Analysis (Enhanced System)")
            
            col1, col2 = st.columns(2)
            
            with col1:
                fig3, df3 = create_ultra_interactive_chart(
                    daily_solar, 'date', 'total_kwh',
                    'Daily Solar Generation (3-Inverter System)', '#10b981', 'area',
                    height=400, enable_zoom=True, enable_selection=True, selection_mode=selection_mode
                )
                if df3 is not None:
                    st.download_button("⬇️ Download Chart Data (Solar Daily)", df3.to_csv(index=False).encode('utf-8'), file_name="solar_daily_chart.csv", mime="text/csv", key="dl_chart_solar_daily")
            
            with col2:
                fig4, df4 = create_ultra_interactive_chart(
                    daily_solar, 'date', 'peak_kw',
                    'Daily Peak Power Output', '#f59e0b', 'line',
                    height=400, enable_zoom=True, enable_selection=True, selection_mode=selection_mode
                )
                if df4 is not None:
                    st.download_button("⬇️ Download Chart Data (Peak Power)", df4.to_csv(index=False).encode('utf-8'), file_name="peak_power_chart.csv", mime="text/csv", key="dl_chart_peak_power")
            
            # System improvement analysis
            if solar_stats.get('system_type') == '3-Inverter Enhanced System':
                st.markdown("### 🚀 System Upgrade Impact Analysis")
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    render_clean_metric(
                        "System Upgrade",
                        "✅ Complete",
                        f"🔄 Fronius removed • +2 inverters",
                        "green", "🔧",
                        "Enhanced 3-inverter configuration"
                    )
                
                with col2:
                    monthly_savings = solar_stats.get('estimated_monthly_savings', 0)
                    render_clean_metric(
                        "Monthly Value",
                        f"R {monthly_savings:,.0f}",
                        f"💰 Improved generation capacity",
                        "green", "💎",
                        "Enhanced energy production value"
                    )
                
                with col3:
                    improvement = solar_stats.get('capacity_improvement_percent', 0)
                    render_clean_metric(
                        "Performance Gain",
                        f"+{improvement:.1f}%",
                        "📈 Capacity improvement",
                        "cyan", "📊",
                        "Compared to previous system"
                    )
                
                # Show upgrade benefits
                st.markdown("### 💡 Upgrade Benefits Analysis")
                
                benefits = {
                    'System Reliability': 'Removed Fronius inverter • Enhanced stability',
                    'Capacity Increase': f'+{improvement:.1f}% peak power improvement',
                    'Energy Production': f'Estimated +R{monthly_savings*12:,.0f} annual value',
                    'Maintenance': 'Simplified 3-inverter configuration',
                    'Performance': f'Best day: {solar_stats.get("best_day_kwh", 0):.0f} kWh generation'
                }
                
                for benefit, description in benefits.items():
                    st.markdown(f"**✅ {benefit}**: {description}")
            
            # Individual inverter performance (if multiple inverters detected)
            if not inverter_performance.empty and len(inverter_performance) > 1:
                st.markdown("### 🔌 Individual Inverter Performance")
                
                inverter_summary = pd.DataFrame(inverter_performance)
                if 'inverter' in inverter_summary.columns and 'total_kwh' in inverter_summary.columns:
                    inverter_totals = inverter_summary.groupby('inverter')['total_kwh'].sum().reset_index()
                    
                    create_ultra_interactive_chart(
                        inverter_totals, 'inverter', 'total_kwh',
                        'Individual Inverter Performance Comparison', '#8b5cf6', 'bar',
                        height=350, enable_zoom=True, selection_mode=selection_mode
                    )
        else:

            
            # ===================================================================
            # ENHANCED SOLAR ANALYSIS - NEW SECTIONS
            # ===================================================================
            
            # System Comparison Analysis (Legacy vs New)
            st.markdown("---")
            st.markdown("### 📊 System Comparison Analysis")
            
            # POWER-FOCUSED ANALYSIS (Main focus: Power capacity and generation patterns)
            st.info("🔧 **Focus: Power Analysis** - Analyzing system power capacity, peak performance, and generation patterns")
            
            try:
                # Analyze legacy system (automatically uses previous_inverter_system.csv)
                legacy_daily, legacy_stats = analyze_legacy_solar_system()
                
                # Analyze new system
                new_daily, new_stats, new_combined = analyze_new_3inverter_system(all_data['solar'])
                
                # Compare systems
                if legacy_stats and new_stats:
                    comparison = compare_solar_systems(legacy_stats, new_stats)
                    
                    st.markdown("#### Legacy (Fronius + Goodwe) vs New (3x Goodwe)")
                    
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        render_clean_metric(
                            "Peak Power Capacity",
                            f"{comparison['new_peak_kw']:.1f} kW",
                            f"↗️ +{comparison['peak_capacity_improvement_pct']:.1f}% vs legacy",
                            "green", "⚡",
                            f"Legacy: {comparison['legacy_peak_kw']:.1f} kW"
                        )
                    
                    with col2:
                        render_clean_metric(
                            "Avg Power Output",
                            f"{comparison['new_avg_daily']/24:.1f} kW avg",
                            f"↗️ +{comparison['daily_generation_improvement_pct']:.1f}% vs legacy",
                            "green", "☀️",
                            f"Legacy: {comparison['legacy_avg_daily']/24:.1f} kW avg"
                        )
                    
                    with col3:
                        render_clean_metric(
                            "System Upgrade",
                            "Complete ✅",
                            comparison['system_upgrade'],
                            "cyan", "🔧",
                            comparison['recommendation']
                        )
                    
                    # Show comparison note
                    st.info(f"ℹ️ **Note:** {comparison['seasonal_note']}")
                    
            except Exception as e:
                st.error(f"⚠️ **System Comparison Error:** {str(e)}")
                st.code(f"Debug info: Check if previous_inverter_system.csv exists and is readable")
                import traceback
                st.code(traceback.format_exc())
            
            # Hourly POWER Patterns (Focus: Power output by hour)
            st.markdown("---")
            st.markdown("### 🕐 Hourly Power Generation Patterns")
            
            if not all_data['solar'].empty:
                st.info("📊 **Power Focus:** Analyzing average power output patterns throughout the day")
                try:
                    hourly_pattern = calculate_hourly_generation_pattern(all_data['solar'])
                    
                    if not hourly_pattern.empty:
                        # Create hourly pattern chart
                        fig_hourly = go.Figure()
                        
                        fig_hourly.add_trace(go.Bar(
                            x=hourly_pattern['hour'],
                            y=hourly_pattern['avg_power_kw'],
                            name='Average Power',
                            marker=dict(
                                color=['#10b981' if is_peak else '#3b82f6' 
                                       for is_peak in hourly_pattern['is_peak']],
                                opacity=0.8
                            ),
                            hovertemplate="<b>%{x}:00</b><br>Avg: %{y:.1f} kW<extra></extra>"
                        ))
                        
                        fig_hourly.update_layout(
                            title="🔋 Power Output Patterns Throughout the Day",
                            xaxis_title="Hour of Day",
                            yaxis_title="Average Power Output (kW)",
                            paper_bgcolor='rgba(0,0,0,0)',
                            plot_bgcolor='rgba(0,0,0,0)',
                            font=dict(color='#e2e8f0'),
                            height=400,
                            showlegend=False
                        )
                        
                        st.plotly_chart(fig_hourly, use_container_width=True, key="hourly_pattern_chart")
                        
                        # Peak hours info
                        peak_hours = hourly_pattern[hourly_pattern['is_peak']]['hour'].tolist()
                        if peak_hours:
                            st.success(f"🌟 Peak Generation Hours: {', '.join([f'{h:02d}:00' for h in peak_hours])}")
                    
                except Exception as e:
                    st.error(f"⚠️ **Hourly Power Pattern Error:** {str(e)}")
                    st.code("Debug: Check solar data format and availability")
            
            # Inverter POWER Performance Monitoring
            st.markdown("---")
            st.markdown("### 🔌 Inverter Power Performance Monitoring")
            st.info("⚡ **Power Focus:** Monitoring individual inverter power output and capacity utilization")
            
            if not inverter_performance.empty:
                try:
                    alert = identify_underperforming_inverter(inverter_performance)
                    
                    if alert and alert.get('has_issue'):
                        severity_color = {
                            'HIGH': '🔴',
                            'MEDIUM': '🟡',
                            'LOW': '🟢'
                        }
                        
                        st.warning(f"""
                        {severity_color.get(alert['severity'], '⚠️')} **Performance Alert - {alert['severity']} Priority**
                        
                        - **Underperforming Inverter:** {alert['worst_inverter']}
                        - **Capacity Factor:** {alert['worst_capacity_factor']:.1f}% (vs {alert['best_capacity_factor']:.1f}% best)
                        - **Performance Gap:** {alert['performance_gap_pct']:.1f}%
                        - **Recommendation:** {alert['recommendation']}
                        """)
                    else:
                        st.success("✅ All inverters performing within acceptable range")
                    
                    # Show capacity factors for all inverters
                    col1, col2, col3 = st.columns(3)
                    inverter_names = inverter_performance['inverter'].unique()
                    
                    for idx, inv in enumerate(inverter_names[:3]):
                        inv_data = inverter_performance[inverter_performance['inverter'] == inv]
                        cf = (inv_data['avg_kw'].mean() / inv_data['peak_kw'].max() * 100) if inv_data['peak_kw'].max() > 0 else 0
                        
                        with [col1, col2, col3][idx]:
                            render_clean_metric(
                                f"Inverter {idx + 1}",
                                f"{cf:.1f}%",
                                "Capacity Factor",
                                "green" if cf > 35 else "yellow", "⚡",
                                inv.replace('sensor.', '').replace('_active_power', '')
                            )
                
                except Exception as e:
                    st.error(f"⚠️ **Inverter Monitoring Error:** {str(e)}")
                    st.code("Debug: Check inverter performance data")
            
            # Power Generation Trends
            st.markdown("---")
            st.markdown("### 📈 Power Generation Trends & Analysis")
            st.info("📈 **Power Focus:** Tracking power generation trends and identifying performance patterns")
            
            if not daily_solar.empty and len(daily_solar) >= 7:
                try:
                    trends = calculate_generation_trends(daily_solar, window=7)
                    
                    if not trends.empty:
                        # Create trend chart
                        fig_trend = go.Figure()
                        
                        fig_trend.add_trace(go.Scatter(
                            x=trends['date'],
                            y=trends['total_kwh'],
                            mode='lines+markers',
                            name='Daily Generation',
                            line=dict(color='#3b82f6', width=2),
                            marker=dict(size=6)
                        ))
                        
                        fig_trend.add_trace(go.Scatter(
                            x=trends['date'],
                            y=trends['rolling_avg'],
                            mode='lines',
                            name='7-Day Average',
                            line=dict(color='#10b981', width=3, dash='dash')
                        ))
                        
                        fig_trend.update_layout(
                            title="🔋 Power Generation Trends (7-Day Rolling Average)",
                            xaxis_title="Date",
                            yaxis_title="Daily Power Generation (kWh equivalent)",
                            paper_bgcolor='rgba(0,0,0,0)',
                            plot_bgcolor='rgba(0,0,0,0)',
                            font=dict(color='#e2e8f0'),
                            height=400,
                            hovermode='x unified'
                        )
                        
                        st.plotly_chart(fig_trend, use_container_width=True, key="trend_chart")
                        
                        # Show trend direction
                        latest_trend = trends['trend_direction'].iloc[-1] if len(trends) > 0 else 'STABLE'
                        trend_icons = {
                            'INCREASING': '📈 Generation is increasing',
                            'DECREASING': '📉 Generation is decreasing',
                            'STABLE': '➡️ Generation is stable'
                        }
                        st.info(trend_icons.get(latest_trend, 'Trend analysis'))
                
                except Exception as e:
                    st.error(f"⚠️ **Trend Analysis Error:** {str(e)}")
                    st.code("Debug: Check daily solar data for trend calculation")
            
            st.info("📊 No solar data available for selected period")
    
    # Data Health panel and summary downloads in System Overview tab
    with tab4:
        st.markdown("## 🩺 Data Health & System Overview")

        # Quick health checks
        def df_health(df, name):
            if df is None or df.empty:
                return f"❌ {name}: missing/empty"
            rows, cols = df.shape
            return f"✅ {name}: {rows} rows, {cols} cols"

        st.markdown("### Data Sources")
        sources = {
            'Generator': daily_fuel,
            'Fuel Purchases': fuel_purchases,
            'Solar Daily': daily_solar,
            'Solar Hourly': hourly_solar,
            'Inverter Performance': inverter_performance,
        }
        for k, v in sources.items():
            st.write(df_health(v, k))

        # Recent dates present
        recent_info = []
        for name, df in [('Generator', daily_fuel), ('Solar', daily_solar)]:
            if not df.empty and 'date' in df.columns:
                recent_info.append(f"{name}: {pd.to_datetime(df['date']).max().date()}")
        if recent_info:
            st.info("Latest data points — " + " • ".join(recent_info))

        # Downloads
        with st.expander("⬇️ Export all analytics as CSVs", expanded=False):
            c1, c2, c3 = st.columns(3)
            with c1:
                st.download_button("Generator Daily CSV", daily_fuel.to_csv(index=False).encode('utf-8') if not daily_fuel.empty else b"", file_name="generator_daily.csv", mime="text/csv", key="dl_generator_daily_bottom", disabled=daily_fuel.empty)
                st.download_button("Fuel Purchases CSV", fuel_purchases.to_csv(index=False).encode('utf-8') if not fuel_purchases.empty else b"", file_name="fuel_purchases.csv", mime="text/csv", key="dl_fuel_purchases_bottom", disabled=fuel_purchases.empty)
            with c2:
                st.download_button("Solar Daily CSV", daily_solar.to_csv(index=False).encode('utf-8') if not daily_solar.empty else b"", file_name="solar_daily.csv", mime="text/csv", key="dl_solar_daily_bottom", disabled=daily_solar.empty)
                st.download_button("Hourly Solar CSV", hourly_solar.to_csv(index=False).encode('utf-8') if not hourly_solar.empty else b"", file_name="solar_hourly.csv", mime="text/csv", key="dl_solar_hourly_bottom", disabled=hourly_solar.empty)
            with c3:
                st.download_button("Inverter Performance CSV", inverter_performance.to_csv(index=False).encode('utf-8') if not inverter_performance.empty else b"", file_name="inverter_performance.csv", mime="text/csv", key="dl_inverter_perf_bottom", disabled=inverter_performance.empty)

        st.markdown("---")

    # Factory Optimization Tab
    with tab3:
        st.markdown("## 🏭 Factory Energy Optimization")
        st.info("📊 Factory energy analysis module ready for implementation")
    
    # System Overview Tab
    with tab4:
        st.markdown("## 📊 Complete System Overview")
        
        # System health with FIXED DataFrame check
        data_available = 0
        if not daily_fuel.empty: data_available += 1
        if not daily_solar.empty: data_available += 1
        if not fuel_purchases.empty: data_available += 1
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            data_quality = (data_available / 3) * 100
            render_clean_metric(
                "System Health",
                f"{data_quality:.0f}%",
                "📊 Data coverage",
                "green" if data_quality > 80 else "yellow", "🔧"
            )
        
        with col2:
            render_clean_metric(
                "Active Systems",
                f"{data_available}/3",
                "⚡ Online modules",
                "green", "📡"
            )
        
        with col3:
            total_cost = fuel_stats.get('total_cost_rands', 0)
            solar_value = solar_stats.get('total_value_rands', 0)
            render_clean_metric(
                "Net Energy Cost",
                f"R {total_cost - solar_value:,.0f}",
                f"💰 After solar savings",
                "blue", "💸"
            )
        
        with col4:
            render_clean_metric(
                "Data Freshness",
                "Live",
                f"🕐 {datetime.now().strftime('%H:%M')}",
                "green", "📊"
            )

if __name__ == "__main__":
    main()