#!/usr/bin/env python3
"""
Streamlit Debug Test - Isolated Solar Performance Module Test
"""

import streamlit as st
import pandas as pd
import sys
import os

# Add current directory to path
sys.path.append('.')

def test_solar_module():
    st.title("🔧 Solar Performance Debug Test")
    
    try:
        st.write("**Step 1: Testing module import...**")
        from solar_performance_redesign import load_old_system_data, load_new_system_data, calculate_system_metrics
        st.success("✅ Module functions imported successfully")
        
        st.write("**Step 2: Testing data loading...**")
        
        # Test old system data loading
        with st.spinner("Loading old system data..."):
            old_data = load_old_system_data("FACTORY ELEC.csv")
            
        if len(old_data) > 0:
            st.success(f"✅ Old system data loaded: {len(old_data)} records")
            st.write("Old data sample:")
            st.dataframe(old_data.head())
        else:
            st.error("❌ Old system data loading returned 0 records")
            
        # Test new system data loading  
        with st.spinner("Loading new system data..."):
            new_data = load_new_system_data("New_inverter.csv")
            
        if len(new_data) > 0:
            st.success(f"✅ New system data loaded: {len(new_data)} records")
            st.write("New data sample:")
            st.dataframe(new_data.head())
        else:
            st.error("❌ New system data loading returned 0 records")
            
        st.write("**Step 3: Testing metrics calculation...**")
        
        if len(old_data) > 0:
            old_metrics = calculate_system_metrics(old_data, "Old System Test", is_multi_inverter=False)
            st.success(f"✅ Old system metrics calculated: {len(old_metrics)} daily records")
            
        if len(new_data) > 0:
            new_metrics = calculate_system_metrics(new_data, "New System Test", is_multi_inverter=True)
            st.success(f"✅ New system metrics calculated: {len(new_metrics)} daily records")
            
        st.write("**Step 4: Testing full render function...**")
        
        from solar_performance_redesign import render_solar_performance_analysis
        
        st.write("Calling main render function...")
        render_solar_performance_analysis()
        
    except Exception as e:
        st.error(f"❌ Debug test failed: {str(e)}")
        st.exception(e)

if __name__ == "__main__":
    test_solar_module()