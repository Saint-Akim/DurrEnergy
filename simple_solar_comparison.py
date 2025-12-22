"""
Simple Solar System Comparison - Data Visualization Only
=======================================================
Load old and new inverter data, present clear charts for analysis.
No interpretation, no recommendations, just data visualization.
"""

import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import streamlit as st
from datetime import datetime

def load_and_clean_data(file_path, system_label):
    """Load solar data and clean for visualization."""
    try:
        df = pd.read_csv(file_path)
        df['timestamp'] = pd.to_datetime(df['last_changed'], errors='coerce')
        df['power_kw'] = pd.to_numeric(df['state'], errors='coerce')
        
        # Remove invalid data
        df = df.dropna(subset=['timestamp', 'power_kw'])
        df = df[df['power_kw'] >= 0]  # Remove negative values
        df['system'] = system_label
        
        return df
    except Exception as e:
        st.error(f"Error loading {file_path}: {e}")
        return pd.DataFrame()

def aggregate_daily_data(df):
    """Aggregate to daily totals and peaks."""
    if df.empty:
        return pd.DataFrame()
    
    df['date'] = df['timestamp'].dt.date
    
    # Group by date and system, then sum individual inverter readings by hour first
    df['hour'] = df['timestamp'].dt.floor('h')
    
    # Sum all inverters per hour, then aggregate to daily
    hourly = df.groupby(['hour', 'system'])['power_kw'].sum().reset_index()
    hourly['date'] = hourly['hour'].dt.date
    
    daily = hourly.groupby(['date', 'system']).agg({
        'power_kw': ['sum', 'max', 'mean', 'count']
    }).reset_index()
    
    # Flatten column names and convert sum to kWh (sum of hourly kW readings)
    daily.columns = ['date', 'system', 'total_kwh', 'peak_kw', 'avg_kw', 'readings']
    
    # Add inverter count from original data
    inverter_counts = df.groupby(['date', 'system'])['entity_id'].nunique().reset_index()
    daily = daily.merge(inverter_counts, on=['date', 'system'], how='left')
    daily.rename(columns={'entity_id': 'inverter_count'}, inplace=True)
    daily['date'] = pd.to_datetime(daily['date'])
    
    return daily

def create_comparison_charts(old_data, new_data):
    """Create visualization charts for comparison."""
    
    # Combine data
    combined = pd.concat([old_data, new_data], ignore_index=True)
    
    if combined.empty:
        st.error("No data available for visualization")
        return
    
    # Chart 1: Daily Energy Generation Timeline
    fig1 = px.line(
        combined, 
        x='date', 
        y='total_kwh',
        color='system',
        title='Daily Energy Generation - Old vs New System',
        labels={'total_kwh': 'Daily Energy (kWh)', 'date': 'Date'}
    )
    fig1.add_vline(x="2025-11-01", line_dash="dash", annotation_text="System Change")
    st.plotly_chart(fig1, use_container_width=True)
    
    # Chart 2: Daily Peak Power Timeline
    fig2 = px.line(
        combined, 
        x='date', 
        y='peak_kw',
        color='system',
        title='Daily Peak Power - Old vs New System',
        labels={'peak_kw': 'Peak Power (kW)', 'date': 'Date'}
    )
    fig2.add_vline(x="2025-11-01", line_dash="dash", annotation_text="System Change")
    st.plotly_chart(fig2, use_container_width=True)
    
    # Chart 3: Box Plot Comparison
    fig3 = make_subplots(
        rows=1, cols=2,
        subplot_titles=['Energy Distribution', 'Peak Power Distribution']
    )
    
    for system in combined['system'].unique():
        system_data = combined[combined['system'] == system]
        
        fig3.add_trace(
            go.Box(y=system_data['total_kwh'], name=f'{system} Energy', boxpoints='outliers'),
            row=1, col=1
        )
        
        fig3.add_trace(
            go.Box(y=system_data['peak_kw'], name=f'{system} Peak Power', boxpoints='outliers'),
            row=1, col=2
        )
    
    fig3.update_layout(title_text="Performance Distribution Comparison", height=400)
    st.plotly_chart(fig3, use_container_width=True)
    
    # Chart 4: Hourly Generation Patterns
    if not combined.empty:
        # Get hourly patterns
        hourly_old = get_hourly_patterns(old_data, "Old System")
        hourly_new = get_hourly_patterns(new_data, "New System")
        
        if not hourly_old.empty or not hourly_new.empty:
            fig4 = go.Figure()
            
            if not hourly_old.empty:
                fig4.add_trace(go.Scatter(
                    x=hourly_old['hour'], 
                    y=hourly_old['avg_power'], 
                    mode='lines+markers',
                    name='Old System',
                    line=dict(color='red')
                ))
            
            if not hourly_new.empty:
                fig4.add_trace(go.Scatter(
                    x=hourly_new['hour'], 
                    y=hourly_new['avg_power'], 
                    mode='lines+markers',
                    name='New System',
                    line=dict(color='green')
                ))
            
            fig4.update_layout(
                title='Average Hourly Power Generation Patterns',
                xaxis_title='Hour of Day',
                yaxis_title='Average Power (kW)',
                height=400
            )
            st.plotly_chart(fig4, use_container_width=True)

def get_hourly_patterns(daily_data, system_name):
    """Extract hourly generation patterns from raw data."""
    # This would need the raw timestamp data
    # For now, return empty - would need to process from original files
    return pd.DataFrame()

def render_simple_solar_comparison():
    """Main function to render the simplified solar comparison."""
    
    st.markdown("## Solar System Comparison - Old vs New Inverters")
    st.markdown("**Data visualization for your analysis - no interpretation provided**")
    
    # Load data
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Old System Data")
        old_raw = load_and_clean_data("previous_inverter_system.csv", "Old System (Pre-Nov 2025)")
        if not old_raw.empty:
            st.success(f"Loaded: {len(old_raw)} records")
            st.write(f"Date range: {old_raw['timestamp'].min()} to {old_raw['timestamp'].max()}")
            st.write(f"Inverters: {old_raw['entity_id'].nunique()}")
        else:
            st.error("Failed to load old system data")
    
    with col2:
        st.markdown("### New System Data")
        new_raw = load_and_clean_data("New_inverter.csv", "New System (Post-Nov 2025)")
        if not new_raw.empty:
            st.success(f"Loaded: {len(new_raw)} records")
            st.write(f"Date range: {new_raw['timestamp'].min()} to {new_raw['timestamp'].max()}")
            st.write(f"Inverters: {new_raw['entity_id'].nunique()}")
        else:
            st.error("Failed to load new system data")
    
    # Process and visualize
    if not old_raw.empty or not new_raw.empty:
        
        st.markdown("---")
        st.markdown("### Data Processing")
        
        old_daily = aggregate_daily_data(old_raw)
        new_daily = aggregate_daily_data(new_raw)
        
        # Basic stats
        col1, col2 = st.columns(2)
        
        with col1:
            if not old_daily.empty:
                st.markdown("**Old System Summary:**")
                st.write(f"• Days of data: {len(old_daily)}")
                st.write(f"• Avg daily energy: {old_daily['total_kwh'].mean():.1f} kWh")
                st.write(f"• Max peak power: {old_daily['peak_kw'].max():.1f} kW")
        
        with col2:
            if not new_daily.empty:
                st.markdown("**New System Summary:**")
                st.write(f"• Days of data: {len(new_daily)}")
                st.write(f"• Avg daily energy: {new_daily['total_kwh'].mean():.1f} kWh")
                st.write(f"• Max peak power: {new_daily['peak_kw'].max():.1f} kW")
        
        st.markdown("---")
        st.markdown("### Visual Comparison")
        
        # Create comparison charts
        create_comparison_charts(old_daily, new_daily)
        
        # Raw data download
        st.markdown("### Export Data for Your Analysis")
        col1, col2 = st.columns(2)
        
        with col1:
            if not old_daily.empty:
                st.download_button(
                    "Download Old System Data",
                    old_daily.to_csv(index=False),
                    "old_system_daily.csv",
                    "text/csv"
                )
        
        with col2:
            if not new_daily.empty:
                st.download_button(
                    "Download New System Data", 
                    new_daily.to_csv(index=False),
                    "new_system_daily.csv",
                    "text/csv"
                )