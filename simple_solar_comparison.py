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
    """Load solar data and clean for visualization - Streamlit Cloud compatible."""
    try:
        # Check if file exists first
        import os
        if not os.path.exists(file_path):
            st.error(f"Data file not found: {file_path}")
            return pd.DataFrame()
            
        df = pd.read_csv(file_path)
        
        # Validate required columns exist
        required_cols = ['entity_id', 'state', 'last_changed']
        missing_cols = [col for col in required_cols if col not in df.columns]
        if missing_cols:
            st.error(f"Missing required columns in {file_path}: {missing_cols}")
            return pd.DataFrame()
        
        # Parse timestamps with explicit UTC handling for Streamlit Cloud
        df['timestamp'] = pd.to_datetime(df['last_changed'], errors='coerce', utc=True)
        
        # Convert to naive datetime to avoid timezone issues on Streamlit Cloud
        if df['timestamp'].dt.tz is not None:
            df['timestamp'] = df['timestamp'].dt.tz_convert(None)
        
        df['power_kw'] = pd.to_numeric(df['state'], errors='coerce')
        
        # Remove invalid data
        df = df.dropna(subset=['timestamp', 'power_kw'])
        df = df[df['power_kw'] >= 0]  # Remove negative values
        df['system'] = system_label
        
        # Validate we have data after cleaning
        if df.empty:
            st.warning(f"No valid data found in {file_path} after cleaning")
            return pd.DataFrame()
        
        return df
    except Exception as e:
        st.error(f"Error loading {file_path}: {str(e)}")
        import traceback
        st.code(traceback.format_exc())
        return pd.DataFrame()

def aggregate_daily_data(df):
    """Aggregate to daily totals and peaks."""
    if df.empty:
        return pd.DataFrame()
    
    df['date'] = df['timestamp'].dt.date
    
    # Proper solar data aggregation methodology - Streamlit Cloud compatible
    try:
        df['hour'] = df['timestamp'].dt.floor('h') 
        df['date'] = df['timestamp'].dt.date
    except Exception as e:
        st.error(f"Error processing timestamps in aggregation: {e}")
        return pd.DataFrame()
    
    # CORRECTED: Get realistic individual inverter averages first, then sum per hour
    # Step 1: Average each inverter's power readings per hour  
    hourly_inverter_avg = df.groupby(['hour', 'system', 'entity_id']).agg({
        'power_kw': 'mean'  # Average power per inverter per hour
    }).reset_index()
    
    # Step 2: Sum all inverters to get total system power per hour
    hourly_system = hourly_inverter_avg.groupby(['hour', 'system']).agg({
        'power_kw': 'sum',  # Total system power = sum of individual inverter averages
        'entity_id': 'nunique'  # Number of active inverters
    }).reset_index()
    
    # Step 3: Aggregate to daily values
    hourly_system['date'] = hourly_system['hour'].dt.date
    
    daily = hourly_system.groupby(['date', 'system']).agg({
        'power_kw': ['mean', 'max'],  # Daily average and peak system power
        'entity_id': 'mean'  # Average inverters active
    }).reset_index()
    
    # Flatten columns and calculate realistic daily energy
    daily.columns = ['date', 'system', 'avg_system_kw', 'peak_system_kw', 'avg_inverters']
    
    # Calculate realistic daily energy: average system power * daylight hours
    daily['total_kwh'] = daily['avg_system_kw'] * 8  # 8 hours average sunlight
    daily['peak_kw'] = daily['peak_system_kw']
    daily['avg_kw'] = daily['avg_system_kw'] 
    daily['inverter_count'] = daily['avg_inverters'].round().astype(int)
    daily['readings'] = 1  # Placeholder
    
    # Realistic bounds for solar systems
    daily = daily[(daily['total_kwh'] >= 0) & (daily['total_kwh'] <= 500)]  # More realistic cap
    daily = daily[(daily['peak_kw'] >= 0) & (daily['peak_kw'] <= 150)]  # Realistic peak power cap
    daily['date'] = pd.to_datetime(daily['date'])
    
    return daily

def create_comparison_charts(old_data, new_data):
    """Create visualization charts for comparison - Streamlit Cloud compatible."""
    
    try:
        # Combine data with validation
        data_frames = []
        if not old_data.empty:
            data_frames.append(old_data)
        if not new_data.empty:
            data_frames.append(new_data)
        
        if not data_frames:
            st.error("No data available for visualization")
            return
            
        combined = pd.concat(data_frames, ignore_index=True)
        
        if combined.empty:
            st.error("Combined data is empty after concatenation")
            return
            
    except Exception as e:
        st.error(f"Error combining data for charts: {e}")
        return
    
    # Chart 1: Daily Energy Generation Timeline
    try:
        # Ensure date column is properly formatted for Plotly
        combined['date_str'] = combined['date'].astype(str)
        
        fig1 = px.line(
            combined, 
            x='date_str', 
            y='total_kwh',
            color='system',
            title='Daily Energy Generation - Old vs New System',
            labels={'total_kwh': 'Daily Energy (kWh)', 'date_str': 'Date'}
        )
        
        # Add system change marker with error handling
        try:
            fig1.add_vline(x="2025-11-01", line_dash="dash", annotation_text="System Change")
        except Exception:
            # Fallback: add as vertical shape
            fig1.add_shape(type="line", x0="2025-11-01", x1="2025-11-01", y0=0, y1=1, yref="paper", 
                          line=dict(color="orange", dash="dash"))
        
        st.plotly_chart(fig1, use_container_width=True)
        
    except Exception as e:
        st.error(f"Error creating energy timeline chart: {e}")
        # Fallback: show basic data table
        st.subheader("Daily Energy Data")
        st.dataframe(combined[['date', 'system', 'total_kwh']].head(10))
    
    # Chart 2: Daily Peak Power Timeline
    try:
        fig2 = px.line(
            combined, 
            x='date_str', 
            y='peak_kw',
            color='system',
            title='Daily Peak Power - Old vs New System',
            labels={'peak_kw': 'Peak Power (kW)', 'date_str': 'Date'}
        )
        
        try:
            fig2.add_vline(x="2025-11-01", line_dash="dash", annotation_text="System Change")
        except Exception:
            # Fallback: add as vertical shape  
            fig2.add_shape(type="line", x0="2025-11-01", x1="2025-11-01", y0=0, y1=1, yref="paper",
                          line=dict(color="orange", dash="dash"))
        
        st.plotly_chart(fig2, use_container_width=True)
        
    except Exception as e:
        st.error(f"Error creating peak power chart: {e}")
        st.subheader("Peak Power Data")
        st.dataframe(combined[['date', 'system', 'peak_kw']].head(10))
    
    # Chart 3: Box Plot Comparison
    try:
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
        
    except Exception as e:
        st.error(f"Error creating distribution charts: {e}")
        st.subheader("System Performance Summary")
        summary_stats = combined.groupby('system')[['total_kwh', 'peak_kw']].agg(['mean', 'max', 'min']).round(2)
        st.dataframe(summary_stats)
    
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