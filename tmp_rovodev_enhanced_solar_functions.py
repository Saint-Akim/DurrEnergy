"""
Enhanced Solar Analysis Functions for Durr Energy Dashboard
============================================================
New functions to compare legacy vs new solar system and provide advanced analytics
DO NOT MODIFY UI - These are backend analysis functions only
"""

import pandas as pd
import numpy as np
from datetime import datetime

# ==============================================================================
# LEGACY vs NEW SYSTEM COMPARISON FUNCTIONS
# ==============================================================================

def analyze_legacy_solar_system(solar_legacy_files=None):
    """
    Analyze the old Fronius + Goodwe system
    Returns: DataFrame with daily generation, statistics dict
    
    Automatically uses previous_inverter_system.csv if available
    """
    from pathlib import Path
    
    # Try to load previous_inverter_system.csv first (preferred)
    ROOT = Path(__file__).resolve().parent
    prev_system_file = ROOT / 'previous_inverter_system.csv'
    
    if prev_system_file.exists():
        try:
            df_legacy = pd.read_csv(prev_system_file)
        except Exception as e:
            print(f"Error loading previous_inverter_system.csv: {e}")
            return pd.DataFrame(), {}
    elif solar_legacy_files:
        # Fallback to provided files
        legacy_data = []
        for file_path in solar_legacy_files:
            try:
                df = pd.read_csv(file_path)
                df['source_file'] = file_path
                legacy_data.append(df)
            except Exception as e:
                print(f"Error loading {file_path}: {e}")
                continue
        
        if not legacy_data:
            return pd.DataFrame(), {}
        
        df_legacy = pd.concat(legacy_data, ignore_index=True)
    else:
        return pd.DataFrame(), {}
    df_legacy['last_changed'] = pd.to_datetime(df_legacy['last_changed'])
    df_legacy['state'] = pd.to_numeric(df_legacy['state'], errors='coerce')
    df_legacy['date'] = df_legacy['last_changed'].dt.date
    
    # Check if this is previous_inverter_system.csv (hourly data) or legacy CSV files
    has_fronius = 'sensor.total_fronius_pv_power' in df_legacy['entity_id'].values
    has_goodwe_total = 'sensor.goodwe_total_pv_power' in df_legacy['entity_id'].values
    
    if has_fronius and has_goodwe_total:
        # This is previous_inverter_system.csv - HOURLY AGGREGATED DATA
        # State values are already in kWh (hourly average), just sum them
        fronius_df = df_legacy[df_legacy['entity_id'] == 'sensor.total_fronius_pv_power'].copy()
        goodwe_df = df_legacy[df_legacy['entity_id'] == 'sensor.goodwe_total_pv_power'].copy()
        
        # Daily aggregation - simply sum the hourly values
        fronius_daily = fronius_df.groupby('date')['state'].sum()
        goodwe_daily = goodwe_df.groupby('date')['state'].sum()
    else:
        # Legacy CSV files - need time integration
        fronius_grid = df_legacy[df_legacy['entity_id'] == 'sensor.fronius_grid_power'].copy()
        goodwe_grid = df_legacy[df_legacy['entity_id'] == 'sensor.goodwe_grid_power'].copy()
        
        # Convert to kW (negative values = generation)
        fronius_grid['power_kw'] = fronius_grid['state'].abs() / 1000
        goodwe_grid['power_kw'] = goodwe_grid['state'].abs() / 1000
        
        # Calculate energy using time integration
        def calc_energy(df):
            df = df.sort_values('last_changed').copy()
            df['time_diff_hours'] = df['last_changed'].diff().dt.total_seconds() / 3600
            df['time_diff_hours'] = df['time_diff_hours'].fillna(0).clip(upper=1.0)
            df['energy_kwh'] = df['power_kw'] * df['time_diff_hours']
            return df
        
        fronius_grid = calc_energy(fronius_grid)
        goodwe_grid = calc_energy(goodwe_grid)
        
        # Daily aggregation
        fronius_daily = fronius_grid.groupby('date')['energy_kwh'].sum()
        goodwe_daily = goodwe_grid.groupby('date')['energy_kwh'].sum()
    
    # Check if we have valid data
    if len(fronius_daily) == 0 and len(goodwe_daily) == 0:
        return pd.DataFrame(), {}
    
    # Combine for overlapping days
    all_dates = sorted(set(fronius_daily.index) | set(goodwe_daily.index))
    combined_daily = pd.DataFrame({
        'date': all_dates,
        'fronius_kwh': [fronius_daily.get(d, 0) for d in all_dates],
        'goodwe_kwh': [goodwe_daily.get(d, 0) for d in all_dates],
    })
    combined_daily['total_kwh'] = combined_daily['fronius_kwh'] + combined_daily['goodwe_kwh']
    combined_daily['date'] = pd.to_datetime(combined_daily['date'])
    
    # Statistics
    # Calculate peak power from the original dataframe
    fronius_peak = df_legacy[df_legacy['entity_id'].str.contains('fronius', case=False, na=False)]['state'].max()
    goodwe_peak = df_legacy[df_legacy['entity_id'].str.contains('goodwe', case=False, na=False)]['state'].max()
    
    # For hourly data, values are already in correct units
    # For legacy files with grid_power, they would have been converted
    peak_system_kw = max(fronius_peak if not pd.isna(fronius_peak) else 0,
                        goodwe_peak if not pd.isna(goodwe_peak) else 0)
    
    stats = {
        'system_type': 'Legacy (Fronius + Goodwe)',
        'total_kwh': combined_daily['total_kwh'].sum(),
        'avg_daily_kwh': combined_daily['total_kwh'].mean(),
        'best_day_kwh': combined_daily['total_kwh'].max(),
        'peak_system_kw': peak_system_kw,
        'fronius_contribution_pct': (combined_daily['fronius_kwh'].sum() / combined_daily['total_kwh'].sum() * 100) if combined_daily['total_kwh'].sum() > 0 else 0,
        'goodwe_contribution_pct': (combined_daily['goodwe_kwh'].sum() / combined_daily['total_kwh'].sum() * 100) if combined_daily['total_kwh'].sum() > 0 else 0,
        'days_active': len(combined_daily),
        'date_range': f"{combined_daily['date'].min().date()} to {combined_daily['date'].max().date()}"
    }
    
    return combined_daily, stats


def analyze_new_3inverter_system(solar_new_df):
    """
    Analyze the new 3-Goodwe inverter system
    Returns: DataFrame with daily generation per inverter, statistics dict
    """
    
    if solar_new_df.empty:
        return pd.DataFrame(), {}
    
    df = solar_new_df.copy()
    df['last_changed'] = pd.to_datetime(df['last_changed'])
    df['state'] = pd.to_numeric(df['state'], errors='coerce')
    df['date'] = df['last_changed'].dt.date
    df['hour'] = df['last_changed'].dt.hour
    
    # Calculate energy using time integration
    def calc_energy(df):
        df = df.sort_values('last_changed').copy()
        df['time_diff_hours'] = df['last_changed'].diff().dt.total_seconds() / 3600
        df['time_diff_hours'] = df['time_diff_hours'].fillna(0).clip(upper=1.0)
        df['energy_kwh'] = df['state'].abs() * df['time_diff_hours']
        return df
    
    # Process each inverter
    inverter_data = []
    inverter_stats = {}
    
    for inverter in df['entity_id'].unique():
        inv_df = df[df['entity_id'] == inverter].copy()
        inv_df = calc_energy(inv_df)
        
        daily = inv_df.groupby('date').agg({
            'energy_kwh': 'sum',
            'state': ['max', 'mean']
        }).reset_index()
        daily.columns = ['date', 'energy_kwh', 'peak_kw', 'avg_kw']
        daily['inverter'] = inverter
        inverter_data.append(daily)
        
        # Per-inverter stats
        inverter_stats[inverter] = {
            'total_kwh': daily['energy_kwh'].sum(),
            'avg_daily_kwh': daily['energy_kwh'].mean(),
            'best_day_kwh': daily['energy_kwh'].max(),
            'peak_kw': daily['peak_kw'].max(),
            'avg_kw': inv_df[inv_df['state'] > 0]['state'].mean(),
            'capacity_factor': (inv_df[inv_df['state'] > 0]['state'].mean() / daily['peak_kw'].max() * 100) if daily['peak_kw'].max() > 0 else 0
        }
    
    # Combine all inverters
    combined = pd.concat(inverter_data, ignore_index=True)
    combined['date'] = pd.to_datetime(combined['date'])
    
    # System totals
    system_daily = combined.groupby('date').agg({
        'energy_kwh': 'sum',
        'peak_kw': 'sum',
        'avg_kw': 'mean'
    }).reset_index()
    system_daily.columns = ['date', 'total_kwh', 'peak_kw', 'avg_kw']
    
    # System statistics
    total_kwh = sum([s['total_kwh'] for s in inverter_stats.values()])
    
    system_stats = {
        'system_type': 'New 3-Inverter Goodwe System',
        'total_kwh': total_kwh,
        'avg_daily_kwh': system_daily['total_kwh'].mean(),
        'best_day_kwh': system_daily['total_kwh'].max(),
        'peak_system_kw': system_daily['peak_kw'].max(),
        'inverter_count': len(inverter_stats),
        'inverter_breakdown': inverter_stats,
        'days_active': len(system_daily),
        'date_range': f"{system_daily['date'].min().date()} to {system_daily['date'].max().date()}"
    }
    
    return system_daily, system_stats, combined


def compare_solar_systems(legacy_stats, new_stats):
    """
    Compare legacy vs new system performance
    Returns: Comparison dictionary with improvements
    """
    
    if not legacy_stats or not new_stats:
        return {}
    
    comparison = {
        'peak_capacity_improvement_pct': ((new_stats['peak_system_kw'] - legacy_stats['peak_system_kw']) / legacy_stats['peak_system_kw'] * 100) if legacy_stats['peak_system_kw'] > 0 else 0,
        'daily_generation_improvement_pct': ((new_stats['avg_daily_kwh'] - legacy_stats['avg_daily_kwh']) / legacy_stats['avg_daily_kwh'] * 100) if legacy_stats['avg_daily_kwh'] > 0 else 0,
        'best_day_improvement_pct': ((new_stats['best_day_kwh'] - legacy_stats['best_day_kwh']) / legacy_stats['best_day_kwh'] * 100) if legacy_stats['best_day_kwh'] > 0 else 0,
        
        'legacy_peak_kw': legacy_stats['peak_system_kw'],
        'new_peak_kw': new_stats['peak_system_kw'],
        'legacy_avg_daily': legacy_stats['avg_daily_kwh'],
        'new_avg_daily': new_stats['avg_daily_kwh'],
        
        'system_upgrade': 'Fronius removed, 2 new Goodwe inverters added',
        'financial_improvement_monthly': ((new_stats['avg_daily_kwh'] - legacy_stats['avg_daily_kwh']) * 30 * 1.50),  # R/month
        'annual_additional_revenue': ((new_stats['avg_daily_kwh'] - legacy_stats['avg_daily_kwh']) * 365 * 1.50),  # R/year
        
        'seasonal_note': 'Legacy: Jan-Jun (Summer→Winter), New: Nov-Dec (Spring→Summer)',
        'recommendation': 'System upgrade SUCCESSFUL' if new_stats['avg_daily_kwh'] > legacy_stats['avg_daily_kwh'] else 'Needs investigation'
    }
    
    return comparison


# ==============================================================================
# ADVANCED ANALYTICS FUNCTIONS
# ==============================================================================

def calculate_hourly_generation_pattern(solar_df):
    """
    Calculate average generation pattern by hour of day
    Returns: DataFrame with hourly averages
    """
    
    if solar_df.empty:
        return pd.DataFrame()
    
    df = solar_df.copy()
    df['last_changed'] = pd.to_datetime(df['last_changed'])
    df['state'] = pd.to_numeric(df['state'], errors='coerce')
    df['hour'] = df['last_changed'].dt.hour
    df['power_kw'] = df['state'].abs()
    
    # Filter active generation only
    df_active = df[df['power_kw'] > 0].copy()
    
    hourly = df_active.groupby('hour').agg({
        'power_kw': ['mean', 'max', 'std', 'count']
    }).reset_index()
    hourly.columns = ['hour', 'avg_power_kw', 'max_power_kw', 'std_power_kw', 'readings']
    
    # Calculate peak hours
    hourly['is_peak'] = hourly['avg_power_kw'] >= hourly['avg_power_kw'].quantile(0.75)
    
    return hourly


def identify_underperforming_inverter(inverter_performance_df):
    """
    Identify if any inverter is underperforming compared to others
    Returns: Alert dictionary with recommendations
    """
    
    if inverter_performance_df.empty:
        return {}
    
    df = inverter_performance_df.copy()
    
    # Calculate capacity factor for each inverter
    inverter_cf = df.groupby('inverter').apply(
        lambda x: (x['avg_kw'].mean() / x['peak_kw'].max() * 100) if x['peak_kw'].max() > 0 else 0
    ).to_dict()
    
    if not inverter_cf:
        return {}
    
    best_inv = max(inverter_cf, key=inverter_cf.get)
    worst_inv = min(inverter_cf, key=inverter_cf.get)
    performance_gap = inverter_cf[best_inv] - inverter_cf[worst_inv]
    
    alert = {
        'has_issue': performance_gap > 10,  # >10% gap is concerning
        'best_inverter': best_inv,
        'worst_inverter': worst_inv,
        'best_capacity_factor': inverter_cf[best_inv],
        'worst_capacity_factor': inverter_cf[worst_inv],
        'performance_gap_pct': performance_gap,
        'recommendation': f"Inspect {worst_inv} for shading, soiling, or technical issues" if performance_gap > 10 else "All inverters performing well",
        'severity': 'HIGH' if performance_gap > 15 else 'MEDIUM' if performance_gap > 10 else 'LOW'
    }
    
    return alert


def calculate_generation_trends(daily_solar_df, window=7):
    """
    Calculate generation trends using rolling averages
    Returns: DataFrame with trends
    """
    
    if daily_solar_df.empty or len(daily_solar_df) < window:
        return pd.DataFrame()
    
    df = daily_solar_df.copy()
    df = df.sort_values('date')
    
    df['rolling_avg'] = df['total_kwh'].rolling(window=window, min_periods=1).mean()
    df['rolling_std'] = df['total_kwh'].rolling(window=window, min_periods=1).std()
    df['trend'] = df['rolling_avg'].diff()
    
    # Classify trend
    df['trend_direction'] = 'STABLE'
    df.loc[df['trend'] > df['rolling_std'] * 0.5, 'trend_direction'] = 'INCREASING'
    df.loc[df['trend'] < -df['rolling_std'] * 0.5, 'trend_direction'] = 'DECREASING'
    
    return df


def calculate_financial_metrics(solar_stats, electricity_rate=1.50):
    """
    Calculate detailed financial metrics
    Returns: Dictionary with financial analysis
    """
    
    if not solar_stats:
        return {}
    
    total_kwh = solar_stats.get('total_kwh', 0)
    avg_daily = solar_stats.get('avg_daily_kwh', 0)
    days = solar_stats.get('days_active', 0)
    
    financial = {
        'total_value_rands': total_kwh * electricity_rate,
        'daily_savings': avg_daily * electricity_rate,
        'monthly_projection': avg_daily * 30 * electricity_rate,
        'annual_projection': avg_daily * 365 * electricity_rate,
        'cost_per_kwh_saved': electricity_rate,
        'carbon_offset_kg': total_kwh * 0.95,  # kg CO2
        'carbon_offset_trees': (total_kwh * 0.95) / 21,  # trees per year equivalent
    }
    
    return financial


# ==============================================================================
# DATA EXPORT FUNCTION
# ==============================================================================

def export_solar_comparison_data(legacy_stats, new_stats, comparison, filepath='solar_comparison_export.csv'):
    """
    Export comparison data to CSV for external analysis
    """
    
    export_data = []
    
    # Legacy system row
    if legacy_stats:
        export_data.append({
            'system': 'Legacy (Fronius + Goodwe)',
            'total_kwh': legacy_stats.get('total_kwh', 0),
            'avg_daily_kwh': legacy_stats.get('avg_daily_kwh', 0),
            'best_day_kwh': legacy_stats.get('best_day_kwh', 0),
            'peak_system_kw': legacy_stats.get('peak_system_kw', 0),
            'days_active': legacy_stats.get('days_active', 0),
            'date_range': legacy_stats.get('date_range', 'N/A')
        })
    
    # New system row
    if new_stats:
        export_data.append({
            'system': 'New (3x Goodwe)',
            'total_kwh': new_stats.get('total_kwh', 0),
            'avg_daily_kwh': new_stats.get('avg_daily_kwh', 0),
            'best_day_kwh': new_stats.get('best_day_kwh', 0),
            'peak_system_kw': new_stats.get('peak_system_kw', 0),
            'days_active': new_stats.get('days_active', 0),
            'date_range': new_stats.get('date_range', 'N/A')
        })
    
    # Comparison row
    if comparison:
        export_data.append({
            'system': 'IMPROVEMENT',
            'total_kwh': comparison.get('annual_additional_revenue', 0) / 1.50,  # Convert back to kWh
            'avg_daily_kwh': comparison.get('daily_generation_improvement_pct', 0),
            'best_day_kwh': comparison.get('best_day_improvement_pct', 0),
            'peak_system_kw': comparison.get('peak_capacity_improvement_pct', 0),
            'days_active': 0,
            'date_range': 'Percentage improvements shown'
        })
    
    df_export = pd.DataFrame(export_data)
    df_export.to_csv(filepath, index=False)
    
    return filepath

