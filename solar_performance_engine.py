"""
Durr Energy - Solar Performance Analysis Engine
==============================================
Senior Technical Implementation - Production Ready

Engineering Approach:
- Pre-upgrade: previous_inverter_system.csv (4 inverters: 3x Fronius + 1x GoodWe)
- Post-upgrade: New_inverter.csv (3 inverters: 3x GoodWe)
- Cutoff: November 1, 2025
- Focus: Power (kW), Energy (kWh), Capacity Utilization, Clipping Reduction

Author: Senior Technical Consultant
Date: 2025-12-17
"""

import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import streamlit as st
from typing import Tuple, Dict, List, Optional

# Engineering Constants
UPGRADE_DATE = "2025-11-01"
ELECTRICITY_RATE_R_PER_KWH = 1.50  # R/kWh
PRE_UPGRADE_NOMINAL_CAPACITY = 25.0  # kW estimated
POST_UPGRADE_NOMINAL_CAPACITY = 30.0  # kW estimated

class SolarSystemAnalyzer:
    """Production-ready solar system performance analyzer."""
    
    def __init__(self):
        self.upgrade_date = pd.to_datetime(UPGRADE_DATE).tz_localize(None)  # Remove timezone for comparison
    
    def load_and_validate_data(self, file_path: str) -> Tuple[pd.DataFrame, Dict]:
        """Load and validate solar data with engineering-grade quality checks."""
        try:
            df = pd.read_csv(file_path)
            
            validation_report = {
                'file_path': file_path,
                'total_records': len(df),
                'date_range': None,
                'entities': [],
                'data_quality': 0,
                'errors': []
            }
            
            if df.empty:
                validation_report['errors'].append("File is empty")
                return pd.DataFrame(), validation_report
            
            required_cols = ['entity_id', 'state', 'last_changed']
            missing_cols = [col for col in required_cols if col not in df.columns]
            if missing_cols:
                validation_report['errors'].append(f"Missing columns: {missing_cols}")
                return df, validation_report
            
            # Parse timestamps and normalize timezone
            df['timestamp'] = pd.to_datetime(df['last_changed'], errors='coerce')
            if df['timestamp'].dt.tz is not None:
                df['timestamp'] = df['timestamp'].dt.tz_convert(None)  # Convert to naive datetime
            invalid_timestamps = df['timestamp'].isna().sum()
            if invalid_timestamps > 0:
                validation_report['errors'].append(f"{invalid_timestamps} invalid timestamps")
            
            df = df.dropna(subset=['timestamp'])
            
            # Parse numeric state values
            df['power_kw'] = pd.to_numeric(df['state'], errors='coerce')
            invalid_power = df['power_kw'].isna().sum()
            if invalid_power > 0:
                validation_report['errors'].append(f"{invalid_power} invalid power readings")
            
            # Filter valid data only
            df_clean = df.dropna(subset=['power_kw'])
            df_clean = df_clean[df_clean['power_kw'] >= 0]  # Remove negative values
            
            if not df_clean.empty:
                validation_report['date_range'] = (
                    df_clean['timestamp'].min(),
                    df_clean['timestamp'].max()
                )
                validation_report['entities'] = df_clean['entity_id'].unique().tolist()
                validation_report['data_quality'] = len(df_clean) / len(df) * 100
            
            return df_clean, validation_report
            
        except Exception as e:
            validation_report = {
                'file_path': file_path,
                'total_records': 0,
                'errors': [f"Load error: {str(e)}"]
            }
            return pd.DataFrame(), validation_report
    
    def analyze_legacy_system(self, df: pd.DataFrame) -> Dict:
        """Analyze pre-upgrade system (3x Fronius + 1x GoodWe)."""
        if df.empty:
            return {}
        
        # Filter to pre-upgrade period
        pre_upgrade = df[df['timestamp'] < self.upgrade_date].copy()
        
        if pre_upgrade.empty:
            return {}
        
        # Identify sensor types
        fronius_sensors = pre_upgrade[
            pre_upgrade['entity_id'].str.contains('fronius', case=False, na=False)
        ]
        goodwe_sensors = pre_upgrade[
            pre_upgrade['entity_id'].str.contains('goodwe', case=False, na=False)
        ]
        
        # Daily aggregation
        pre_upgrade['date'] = pre_upgrade['timestamp'].dt.date
        
        daily_stats = []
        for date in pre_upgrade['date'].unique():
            day_data = pre_upgrade[pre_upgrade['date'] == date]
            
            # Calculate total system power for each timestamp, then aggregate
            hourly_totals = day_data.groupby(day_data['timestamp'].dt.floor('H'))['power_kw'].sum()
            
            if len(hourly_totals) > 0:
                daily_stats.append({
                    'date': date,
                    'total_kwh': hourly_totals.mean() * len(hourly_totals),  # Simplified energy calc
                    'peak_kw': hourly_totals.max(),
                    'avg_kw': hourly_totals.mean(),
                    'capacity_factor': hourly_totals.max() / PRE_UPGRADE_NOMINAL_CAPACITY,
                    'operating_hours': len(hourly_totals[hourly_totals > 1.0])  # Hours with meaningful generation
                })
        
        if not daily_stats:
            return {}
        
        daily_df = pd.DataFrame(daily_stats)
        
        return {
            'period': 'Pre-upgrade (Legacy System)',
            'date_range': (pre_upgrade['timestamp'].min(), pre_upgrade['timestamp'].max()),
            'total_kwh': daily_df['total_kwh'].sum(),
            'avg_daily_kwh': daily_df['total_kwh'].mean(),
            'peak_system_kw': daily_df['peak_kw'].max(),
            'avg_capacity_factor': daily_df['capacity_factor'].mean(),
            'total_days': len(daily_df),
            'fronius_inverters': len(fronius_sensors['entity_id'].unique()),
            'goodwe_inverters': len(goodwe_sensors['entity_id'].unique()),
            'total_inverters': len(pre_upgrade['entity_id'].unique()),
            'estimated_value_rands': daily_df['total_kwh'].sum() * ELECTRICITY_RATE_R_PER_KWH,
            'daily_data': daily_df
        }
    
    def analyze_new_system(self, df: pd.DataFrame) -> Dict:
        """Analyze post-upgrade system (3x GoodWe)."""
        if df.empty:
            return {}
        
        # Filter to post-upgrade period
        post_upgrade = df[df['timestamp'] >= self.upgrade_date].copy()
        
        if post_upgrade.empty:
            return {}
        
        # All should be GoodWe sensors in new system
        goodwe_sensors = post_upgrade[
            post_upgrade['entity_id'].str.contains('goodwe', case=False, na=False)
        ]
        
        # Daily aggregation
        post_upgrade['date'] = post_upgrade['timestamp'].dt.date
        
        daily_stats = []
        for date in post_upgrade['date'].unique():
            day_data = post_upgrade[post_upgrade['date'] == date]
            
            # Calculate total system power for each timestamp, then aggregate
            hourly_totals = day_data.groupby(day_data['timestamp'].dt.floor('H'))['power_kw'].sum()
            
            if len(hourly_totals) > 0:
                daily_stats.append({
                    'date': date,
                    'total_kwh': hourly_totals.mean() * len(hourly_totals),  # Simplified energy calc
                    'peak_kw': hourly_totals.max(),
                    'avg_kw': hourly_totals.mean(),
                    'capacity_factor': hourly_totals.max() / POST_UPGRADE_NOMINAL_CAPACITY,
                    'operating_hours': len(hourly_totals[hourly_totals > 1.0])
                })
        
        if not daily_stats:
            return {}
        
        daily_df = pd.DataFrame(daily_stats)
        
        # Inverter-level analysis
        inverter_stats = []
        for inverter in goodwe_sensors['entity_id'].unique():
            inv_data = goodwe_sensors[goodwe_sensors['entity_id'] == inverter]
            if not inv_data.empty:
                inverter_stats.append({
                    'inverter': inverter,
                    'avg_power_kw': inv_data['power_kw'].mean(),
                    'peak_power_kw': inv_data['power_kw'].max(),
                    'total_records': len(inv_data)
                })
        
        return {
            'period': 'Post-upgrade (New 3-Inverter System)',
            'date_range': (post_upgrade['timestamp'].min(), post_upgrade['timestamp'].max()),
            'total_kwh': daily_df['total_kwh'].sum(),
            'avg_daily_kwh': daily_df['total_kwh'].mean(),
            'peak_system_kw': daily_df['peak_kw'].max(),
            'avg_capacity_factor': daily_df['capacity_factor'].mean(),
            'total_days': len(daily_df),
            'goodwe_inverters': len(goodwe_sensors['entity_id'].unique()),
            'total_inverters': len(post_upgrade['entity_id'].unique()),
            'estimated_value_rands': daily_df['total_kwh'].sum() * ELECTRICITY_RATE_R_PER_KWH,
            'daily_data': daily_df,
            'inverter_performance': inverter_stats
        }
    
    def compare_systems(self, legacy_stats: Dict, new_stats: Dict) -> Dict:
        """Engineering comparison between legacy and new systems."""
        if not legacy_stats or not new_stats:
            return {}
        
        # Normalize by operational days for fair comparison
        legacy_daily_avg = legacy_stats['avg_daily_kwh']
        new_daily_avg = new_stats['avg_daily_kwh']
        
        # Performance improvements
        energy_improvement_pct = ((new_daily_avg - legacy_daily_avg) / legacy_daily_avg * 100) if legacy_daily_avg > 0 else 0
        
        legacy_peak = legacy_stats['peak_system_kw']
        new_peak = new_stats['peak_system_kw']
        peak_improvement_pct = ((new_peak - legacy_peak) / legacy_peak * 100) if legacy_peak > 0 else 0
        
        # Capacity factor improvements
        legacy_cf = legacy_stats['avg_capacity_factor']
        new_cf = new_stats['avg_capacity_factor']
        cf_improvement_pct = ((new_cf - legacy_cf) / legacy_cf * 100) if legacy_cf > 0 else 0
        
        # Economic impact
        annual_energy_increase_kwh = energy_improvement_pct / 100 * legacy_stats['total_kwh'] * (365 / legacy_stats['total_days'])
        annual_value_increase_rands = annual_energy_increase_kwh * ELECTRICITY_RATE_R_PER_KWH
        
        return {
            'energy_improvement_pct': energy_improvement_pct,
            'peak_power_improvement_pct': peak_improvement_pct,
            'capacity_factor_improvement_pct': cf_improvement_pct,
            'legacy_daily_kwh': legacy_daily_avg,
            'new_daily_kwh': new_daily_avg,
            'legacy_peak_kw': legacy_peak,
            'new_peak_kw': new_peak,
            'inverter_reduction': legacy_stats['total_inverters'] - new_stats['total_inverters'],
            'fronius_removed': legacy_stats.get('fronius_inverters', 0),
            'annual_energy_increase_kwh': annual_energy_increase_kwh,
            'annual_value_increase_rands': annual_value_increase_rands,
            'upgrade_roi_impact': 'Positive' if energy_improvement_pct > 0 else 'Negative'
        }
    
    def create_comparison_chart(self, legacy_stats: Dict, new_stats: Dict, comparison: Dict) -> go.Figure:
        """Create professional before/after comparison chart."""
        
        if not legacy_stats or not new_stats:
            fig = go.Figure()
            fig.add_annotation(text="Insufficient data for comparison", 
                             xref="paper", yref="paper", x=0.5, y=0.5, showarrow=False)
            return fig
        
        # Create side-by-side comparison
        categories = ['Daily Energy\n(kWh)', 'Peak Power\n(kW)', 'Capacity Factor\n(%)']
        legacy_values = [
            legacy_stats['avg_daily_kwh'],
            legacy_stats['peak_system_kw'],
            legacy_stats['avg_capacity_factor'] * 100
        ]
        new_values = [
            new_stats['avg_daily_kwh'],
            new_stats['peak_system_kw'],
            new_stats['avg_capacity_factor'] * 100
        ]
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            name='Legacy System (3x Fronius + 1x GoodWe)',
            x=categories,
            y=legacy_values,
            marker_color='#ef4444',
            text=[f'{v:.1f}' for v in legacy_values],
            textposition='auto'
        ))
        
        fig.add_trace(go.Bar(
            name='New System (3x GoodWe)',
            x=categories,
            y=new_values,
            marker_color='#10b981',
            text=[f'{v:.1f}' for v in new_values],
            textposition='auto'
        ))
        
        fig.update_layout(
            title="Solar System Upgrade Performance Comparison",
            xaxis_title="Performance Metrics",
            yaxis_title="Values",
            barmode='group',
            template='plotly_white',
            height=500
        )
        
        # Add improvement annotations
        for i, category in enumerate(categories):
            if category == 'Daily Energy\n(kWh)':
                improvement = comparison['energy_improvement_pct']
            elif category == 'Peak Power\n(kW)':
                improvement = comparison['peak_power_improvement_pct']
            else:
                improvement = comparison['capacity_factor_improvement_pct']
            
            fig.add_annotation(
                x=i,
                y=max(legacy_values[i], new_values[i]) * 1.1,
                text=f"+{improvement:.1f}%" if improvement > 0 else f"{improvement:.1f}%",
                showarrow=True,
                arrowhead=2,
                arrowcolor="green" if improvement > 0 else "red",
                font=dict(color="green" if improvement > 0 else "red", size=12)
            )
        
        return fig
    
    def create_time_series_chart(self, legacy_stats: Dict, new_stats: Dict) -> go.Figure:
        """Create time series chart showing performance over time."""
        
        fig = make_subplots(
            rows=2, cols=1,
            subplot_titles=('Daily Energy Generation (kWh)', 'Daily Peak Power (kW)'),
            shared_xaxes=True,
            vertical_spacing=0.1
        )
        
        # Legacy system data
        if legacy_stats and 'daily_data' in legacy_stats:
            legacy_df = legacy_stats['daily_data']
            legacy_df['date'] = pd.to_datetime(legacy_df['date'])
            
            fig.add_trace(
                go.Scatter(
                    x=legacy_df['date'],
                    y=legacy_df['total_kwh'],
                    mode='lines+markers',
                    name='Legacy System - Energy',
                    line=dict(color='#ef4444'),
                    marker=dict(size=4)
                ),
                row=1, col=1
            )
            
            fig.add_trace(
                go.Scatter(
                    x=legacy_df['date'],
                    y=legacy_df['peak_kw'],
                    mode='lines+markers',
                    name='Legacy System - Peak Power',
                    line=dict(color='#ef4444'),
                    marker=dict(size=4)
                ),
                row=2, col=1
            )
        
        # New system data
        if new_stats and 'daily_data' in new_stats:
            new_df = new_stats['daily_data']
            new_df['date'] = pd.to_datetime(new_df['date'])
            
            fig.add_trace(
                go.Scatter(
                    x=new_df['date'],
                    y=new_df['total_kwh'],
                    mode='lines+markers',
                    name='New System - Energy',
                    line=dict(color='#10b981'),
                    marker=dict(size=4)
                ),
                row=1, col=1
            )
            
            fig.add_trace(
                go.Scatter(
                    x=new_df['date'],
                    y=new_df['peak_kw'],
                    mode='lines+markers',
                    name='New System - Peak Power',
                    line=dict(color='#10b981'),
                    marker=dict(size=4)
                ),
                row=2, col=1
            )
        
        # Add upgrade date line
        fig.add_vline(
            x=self.upgrade_date,
            line_dash="dash",
            line_color="orange",
            annotation_text="System Upgrade",
            annotation_position="top"
        )
        
        fig.update_layout(
            height=600,
            title="Solar Performance Timeline - Before vs After Upgrade",
            template='plotly_white'
        )
        
        return fig