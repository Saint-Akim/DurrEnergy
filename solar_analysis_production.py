"""
Solar Performance Analysis - Production Module
==============================================
Engineering-grade before/after analysis for solar system upgrade.

Author: Senior Technical Consultant  
Date: 2025-12-29
Version: 1.0.0
"""

import pandas as pd
import numpy as np
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')


def load_and_analyze_solar_systems(data_dir=None):
    """
    Load both old and new solar system data and perform complete analysis.
    
    Returns:
        dict with all metrics and processed data
    """
    data_dir = Path(data_dir) if data_dir else Path.cwd()
    
    # ========== LOAD NEW SYSTEM (3 inverters) ==========
    try:
        new_df = pd.read_csv(data_dir / 'New_inverter.csv')
        new_df['timestamp'] = pd.to_datetime(new_df['last_changed'], utc=True).dt.tz_localize(None)
        new_df['power_kw'] = pd.to_numeric(new_df['state'], errors='coerce')
        new_df = new_df.dropna(subset=['power_kw'])
        
        # Hourly aggregation: average per inverter per hour, then sum
        new_df['hour'] = new_df['timestamp'].dt.floor('h')
        new_hourly_inv = new_df.groupby(['hour', 'entity_id'])['power_kw'].mean().reset_index()
        new_system = new_hourly_inv.groupby('hour')['power_kw'].sum().reset_index()
        new_system.columns = ['timestamp', 'system_power_kw']
        new_system['system'] = 'New (3 Inverters)'
        
    except Exception as e:
        print(f"Error loading new system: {e}")
        new_system = pd.DataFrame()
    
    # ========== LOAD OLD SYSTEM (4 inverters) ==========
    try:
        old_df = pd.read_csv(data_dir / 'previous_inverter_system.csv')
        old_df['timestamp'] = pd.to_datetime(old_df['last_changed'], utc=True).dt.tz_localize(None)
        old_df['power_kw'] = pd.to_numeric(old_df['state'], errors='coerce')
        old_df = old_df.dropna(subset=['power_kw'])
        
        # Hourly aggregation
        old_df['hour'] = old_df['timestamp'].dt.floor('h')
        old_hourly_src = old_df.groupby(['hour', 'entity_id'])['power_kw'].mean().reset_index()
        old_system = old_hourly_src.groupby('hour')['power_kw'].sum().reset_index()
        old_system.columns = ['timestamp', 'system_power_kw']
        old_system['system'] = 'Old (4 Inverters)'
        
    except Exception as e:
        print(f"Error loading old system: {e}")
        old_system = pd.DataFrame()
    
    # ========== CALCULATE DAILY ENERGY ==========
    def calc_daily(hourly_df):
        if hourly_df.empty:
            return pd.DataFrame()
        df = hourly_df.copy()
        df['date'] = df['timestamp'].dt.date
        daily = df.groupby('date')['system_power_kw'].sum().reset_index()
        daily.columns = ['date', 'daily_kwh']
        return daily[daily['daily_kwh'] > 1.0]
    
    new_daily = calc_daily(new_system)
    old_daily = calc_daily(old_system)
    
    # ========== CALCULATE STATISTICS ==========
    def calc_stats(hourly_df, daily_df, name):
        if hourly_df.empty or daily_df.empty:
            return {}
        
        gen_hours = hourly_df[hourly_df['system_power_kw'] > 0.1]
        
        return {
            'name': name,
            'data_days': len(daily_df),
            'peak_power_kw': gen_hours['system_power_kw'].max(),
            'mean_power_kw': gen_hours['system_power_kw'].mean(),
            'median_power_kw': gen_hours['system_power_kw'].median(),
            'avg_daily_kwh': daily_df['daily_kwh'].mean(),
            'peak_daily_kwh': daily_df['daily_kwh'].max(),
            'min_daily_kwh': daily_df['daily_kwh'].min(),
            'total_kwh': daily_df['daily_kwh'].sum(),
        }
    
    old_stats = calc_stats(old_system, old_daily, 'Old (4 Inverters)')
    new_stats = calc_stats(new_system, new_daily, 'New (3 Inverters)')
    
    # ========== COMPARISON METRICS ==========
    def pct_change(old_val, new_val):
        if old_val == 0:
            return 0
        return ((new_val - old_val) / old_val) * 100
    
    comparison = {
        'peak_power_change_pct': pct_change(old_stats.get('peak_power_kw', 0), new_stats.get('peak_power_kw', 0)),
        'avg_power_change_pct': pct_change(old_stats.get('mean_power_kw', 0), new_stats.get('mean_power_kw', 0)),
        'daily_energy_change_pct': pct_change(old_stats.get('avg_daily_kwh', 0), new_stats.get('avg_daily_kwh', 0)),
        'median_power_change_pct': pct_change(old_stats.get('median_power_kw', 0), new_stats.get('median_power_kw', 0)),
        'annual_savings_rands': (new_stats.get('avg_daily_kwh', 0) - old_stats.get('avg_daily_kwh', 0)) * 1.50 * 365,
    }
    
    # ========== HOURLY PATTERNS ==========
    def hourly_pattern(hourly_df):
        if hourly_df.empty:
            return pd.DataFrame()
        df = hourly_df.copy()
        df['hour_of_day'] = df['timestamp'].dt.hour
        pattern = df.groupby('hour_of_day')['system_power_kw'].mean().reset_index()
        pattern.columns = ['hour', 'avg_power_kw']
        return pattern
    
    old_hourly_pattern = hourly_pattern(old_system)
    new_hourly_pattern = hourly_pattern(new_system)
    
    return {
        'old_stats': old_stats,
        'new_stats': new_stats,
        'comparison': comparison,
        'old_daily': old_daily,
        'new_daily': new_daily,
        'old_hourly': old_system,
        'new_hourly': new_system,
        'old_hourly_pattern': old_hourly_pattern,
        'new_hourly_pattern': new_hourly_pattern,
    }
