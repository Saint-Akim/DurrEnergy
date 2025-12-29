"""
Simple Solar Performance Comparison - kW Only
Direct before/after upgrade comparison using real data
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

def load_before_upgrade_data():
    """Load pre-upgrade OLD inverter system data (kW only)"""
    try:
        st.info("📊 Loading OLD inverter system data...")
        
        # Use the previous inverter system file with real kW data
        df = pd.read_csv('previous inverter system.csv')
        
        st.info(f"   📁 Loaded {len(df):,} records from previous inverter system.csv")
        
        # Show available entities for debugging
        entities = df['entity_id'].unique()
        st.info(f"   🔍 Available entities: {entities[:5]}...")
        
        # Filter for power sensors only
        power_sensors = [
            'sensor.total_fronius_pv_power',
            'sensor.goodwe_total_pv_power'
        ]
        df = df[df['entity_id'].isin(power_sensors)].copy()
        
        st.info(f"   ⚡ Filtered to power sensors: {len(df):,} records")
        
        # Parse data
        df['timestamp'] = pd.to_datetime(df['last_changed'], utc=True)
        df['power_kw'] = pd.to_numeric(df['state'], errors='coerce')
        
        # Clean data
        df = df.dropna(subset=['power_kw'])
        df = df[df['power_kw'] >= 0]
        
        st.info(f"   🧹 After cleaning: {len(df):,} valid records")
        
        # Show breakdown by sensor
        for sensor in power_sensors:
            sensor_data = df[df['entity_id'] == sensor]
            if not sensor_data.empty:
                avg_power = sensor_data['power_kw'].mean()
                st.info(f"   📊 {sensor}: {len(sensor_data):,} records, avg {avg_power:.1f}kW")
        
        # Aggregate both sensors (Fronius + GoodWe) by hour
        df['hour'] = df['timestamp'].dt.floor('H')
        hourly_total = df.groupby('hour')['power_kw'].sum().reset_index()
        hourly_total['system'] = 'OLD System (Previous Inverters)'
        
        # Date range
        if not hourly_total.empty:
            date_range = f"{hourly_total['hour'].min().date()} → {hourly_total['hour'].max().date()}"
            st.success(f"   ✅ OLD system hourly data: {len(hourly_total):,} hours ({date_range})")
        
        return hourly_total
        
    except Exception as e:
        st.error(f"❌ Error loading OLD inverter system data: {e}")
        st.exception(e)
        return pd.DataFrame()

def load_after_upgrade_data():
    """Load post-upgrade NEW inverter system data (kW only)"""
    try:
        st.info("📊 Loading NEW inverter system data...")
        
        df = pd.read_csv('New_inverter.csv')
        
        st.info(f"   📁 Loaded {len(df):,} records from New_inverter.csv")
        
        # Show available entities for debugging
        entities = df['entity_id'].unique()
        st.info(f"   🔍 Available entities: {entities[:5]}...")
        
        # Filter for the 3 new inverters
        new_inverters = [
            'sensor.goodwegt1_active_power',
            'sensor.goodwegt2_active_power',
            'sensor.goodweht1_active_power'
        ]
        df = df[df['entity_id'].isin(new_inverters)].copy()
        
        st.info(f"   ⚡ Filtered to new inverters: {len(df):,} records")
        
        # Parse data
        df['timestamp'] = pd.to_datetime(df['last_changed'], utc=True)
        df['power_kw'] = pd.to_numeric(df['state'], errors='coerce')
        
        # Clean data
        df = df.dropna(subset=['power_kw'])
        df = df[df['power_kw'] >= 0]
        
        st.info(f"   🧹 After cleaning: {len(df):,} valid records")
        
        # Show breakdown by inverter
        for inverter in new_inverters:
            inverter_data = df[df['entity_id'] == inverter]
            if not inverter_data.empty:
                avg_power = inverter_data['power_kw'].mean()
                max_power = inverter_data['power_kw'].max()
                st.info(f"   📊 {inverter}: {len(inverter_data):,} records, avg {avg_power:.1f}kW, max {max_power:.1f}kW")
        
        # Aggregate all 3 inverters by hour
        df['hour'] = df['timestamp'].dt.floor('H')
        hourly_total = df.groupby('hour')['power_kw'].sum().reset_index()
        hourly_total['system'] = 'NEW System (3 New Inverters)'
        
        # Date range
        if not hourly_total.empty:
            date_range = f"{hourly_total['hour'].min().date()} → {hourly_total['hour'].max().date()}"
            st.success(f"   ✅ NEW system hourly data: {len(hourly_total):,} hours ({date_range})")
        
        return hourly_total
        
    except Exception as e:
        st.error(f"❌ Error loading NEW inverter system data: {e}")
        st.exception(e)
        return pd.DataFrame()

def create_simple_comparison(before_data, after_data):
    """Create simple before/after kW comparison"""
    
    # Combine data
    combined = pd.concat([before_data, after_data], ignore_index=True)
    combined['date_hour'] = combined['hour'].dt.strftime('%Y-%m-%d %H:00')
    
    # Summary stats
    before_stats = before_data['power_kw'].describe()
    after_stats = after_data['power_kw'].describe()
    
    # Display key metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Before Avg Power", f"{before_stats['mean']:.1f} kW")
        st.metric("Before Max Power", f"{before_stats['max']:.1f} kW")
    
    with col2:
        st.metric("After Avg Power", f"{after_stats['mean']:.1f} kW")
        st.metric("After Max Power", f"{after_stats['max']:.1f} kW")
    
    with col3:
        avg_improvement = ((after_stats['mean'] / before_stats['mean']) - 1) * 100 if before_stats['mean'] > 0 else 0
        max_improvement = ((after_stats['max'] / before_stats['max']) - 1) * 100 if before_stats['max'] > 0 else 0
        
        st.metric("Avg Power Change", f"{avg_improvement:+.1f}%")
        st.metric("Max Power Change", f"{max_improvement:+.1f}%")
    
    # Time series comparison
    st.subheader("⚡ Power Output Comparison (kW)")
    
    fig = px.line(
        combined,
        x='date_hour',
        y='power_kw', 
        color='system',
        title='Solar Power Output: Before vs After Upgrade',
        labels={'power_kw': 'Power Output (kW)', 'date_hour': 'Time'}
    )
    
    fig.update_layout(height=500)
    st.plotly_chart(fig, width='stretch')
    
    # Power distribution comparison  
    st.subheader("📊 Power Distribution Comparison")
    
    fig2 = px.box(
        combined,
        x='system',
        y='power_kw',
        color='system', 
        title='Power Distribution: Statistical Comparison',
        labels={'power_kw': 'Power Output (kW)', 'system': 'System Configuration'}
    )
    
    fig2.update_layout(height=400)
    st.plotly_chart(fig2, width='stretch')
    
    # Summary table
    st.subheader("📋 Statistical Summary")
    
    comparison_df = pd.DataFrame({
        'Before Upgrade': before_stats.round(2),
        'After Upgrade': after_stats.round(2)
    })
    
    st.dataframe(comparison_df)

def render_simple_solar_comparison():
    """Main function for simple solar comparison"""
    
    st.title("☀️ Simple Solar Performance Comparison")
    st.markdown("**OLD vs NEW Inverter System Comparison - Power Output (kW) Only**")
    st.markdown("🔄 **OLD System**: previous inverter system.csv (Fronius + GoodWe)")
    st.markdown("⚡ **NEW System**: New_inverter.csv (3 New GoodWe Inverters)")
    
    # Load data
    with st.spinner("Loading solar performance data..."):
        before_data = load_before_upgrade_data()
        after_data = load_after_upgrade_data()
    
    # Show data info
    if not before_data.empty and not after_data.empty:
        st.info(f"📊 Loaded data: {len(before_data):,} hours before upgrade, {len(after_data):,} hours after upgrade")
        
        # Date ranges
        before_range = f"{before_data['hour'].min().date()} to {before_data['hour'].max().date()}"
        after_range = f"{after_data['hour'].min().date()} to {after_data['hour'].max().date()}"
        
        st.info(f"📅 Before period: {before_range}")
        st.info(f"📅 After period: {after_range}")
        
        # Create comparison
        create_simple_comparison(before_data, after_data)
        
    elif before_data.empty:
        st.error("❌ No before upgrade data found")
    elif after_data.empty:
        st.error("❌ No after upgrade data found")
    else:
        st.error("❌ No data available for comparison")

if __name__ == "__main__":
    render_simple_solar_comparison()