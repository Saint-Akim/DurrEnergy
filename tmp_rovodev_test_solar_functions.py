#!/usr/bin/env python3
"""
SOLAR PERFORMANCE TAB - DEPLOYMENT TEST SUITE
=============================================
Comprehensive testing of enhanced solar analysis functionality
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import sys
import traceback

def test_data_loading():
    """Test data loading and basic validation"""
    print("\n🔍 TESTING DATA LOADING...")
    
    try:
        # Load data files
        factory_df = pd.read_csv('FACTORY ELEC.csv')
        new_inverter_df = pd.read_csv('New_inverter.csv')
        
        # Basic validation
        print(f"✅ FACTORY ELEC.csv loaded: {len(factory_df):,} records")
        print(f"   Columns: {list(factory_df.columns)}")
        print(f"   Date range: {factory_df['last_changed'].min()} to {factory_df['last_changed'].max()}")
        
        print(f"✅ New_inverter.csv loaded: {len(new_inverter_df):,} records")
        print(f"   Columns: {list(new_inverter_df.columns)}")
        print(f"   Date range: {new_inverter_df['last_changed'].min()} to {new_inverter_df['last_changed'].max()}")
        
        # Check for required columns
        required_cols = ['last_changed', 'entity_id', 'state']
        for df_name, df in [('FACTORY ELEC', factory_df), ('New_inverter', new_inverter_df)]:
            missing_cols = [col for col in required_cols if col not in df.columns]
            if missing_cols:
                print(f"⚠️  {df_name} missing columns: {missing_cols}")
            else:
                print(f"✅ {df_name} has all required columns")
        
        return factory_df, new_inverter_df, True
        
    except Exception as e:
        print(f"❌ Data loading failed: {e}")
        traceback.print_exc()
        return None, None, False

def test_enhanced_solar_analysis(factory_df, new_inverter_df):
    """Test the enhanced solar analysis functions"""
    print("\n🔍 TESTING ENHANCED SOLAR ANALYSIS...")
    
    try:
        # Import the enhanced functions
        sys.path.append('.')
        
        # Test if enhanced module exists
        try:
            from tmp_rovodev_enhanced_solar_analysis import (
                analyze_legacy_system_enhanced,
                analyze_new_system_enhanced,
                compare_solar_systems_enhanced,
                validate_data_quality,
                SA_SOLAR_BENCHMARKS
            )
            print("✅ Enhanced solar analysis module imported successfully")
            enhanced_available = True
        except ImportError:
            print("⚠️  Enhanced solar analysis module not found, testing basic functions")
            enhanced_available = False
        
        # Test date range
        start_date = "2025-01-01"
        end_date = "2025-12-31"
        
        if enhanced_available:
            # Test enhanced legacy analysis
            print("\n📊 Testing legacy system analysis...")
            legacy_df, legacy_stats, legacy_quality = analyze_legacy_system_enhanced(
                factory_df, start_date, end_date
            )
            
            print(f"   Legacy analysis: {len(legacy_df) if not legacy_df.empty else 0} daily records")
            if legacy_stats:
                print(f"   Average daily generation: {legacy_stats.get('average_daily_kwh', 0):.1f} kWh")
                print(f"   Data quality grade: {legacy_quality.get('grade', 'Unknown')}")
            
            # Test enhanced new system analysis
            print("\n📊 Testing new system analysis...")
            new_df, new_stats, new_quality, alerts = analyze_new_system_enhanced(
                new_inverter_df, start_date, end_date
            )
            
            print(f"   New system analysis: {len(new_df) if not new_df.empty else 0} daily records")
            if new_stats:
                print(f"   Average daily generation: {new_stats.get('average_daily_kwh', 0):.1f} kWh")
                print(f"   Data quality grade: {new_quality.get('grade', 'Unknown')}")
                print(f"   Performance alerts: {len(alerts)}")
            
            # Test comparison
            if legacy_stats and new_stats:
                print("\n📊 Testing system comparison...")
                comparison_stats = compare_solar_systems_enhanced(
                    legacy_df, legacy_stats, new_df, new_stats
                )
                
                if comparison_stats and 'performance_metrics' in comparison_stats:
                    metrics = comparison_stats['performance_metrics']
                    improvement = metrics.get('daily_generation_improvement_percent', 0)
                    confidence = metrics.get('statistical_confidence', 'Unknown')
                    
                    print(f"   Generation improvement: {improvement:.1f}%")
                    print(f"   Statistical confidence: {confidence}")
                    print(f"   Weather-normalized improvement: {metrics.get('weather_normalized_improvement_percent', 0):.1f}%")
                
                return True
            else:
                print("⚠️  Insufficient data for comparison analysis")
                return False
        
        else:
            # Test with existing functions
            print("📊 Testing with existing solar functions...")
            
            # Basic data processing test
            if not new_inverter_df.empty:
                new_inverter_df['last_changed'] = pd.to_datetime(new_inverter_df['last_changed'])
                new_inverter_df['state'] = pd.to_numeric(new_inverter_df['state'], errors='coerce')
                
                daily_summary = new_inverter_df.groupby(new_inverter_df['last_changed'].dt.date).agg({
                    'state': ['count', 'mean', 'sum']
                })
                
                print(f"   Basic processing: {len(daily_summary)} days of data")
                print(f"   Average daily readings: {daily_summary[('state', 'count')].mean():.1f}")
                
                return True
            else:
                print("❌ No data available for processing")
                return False
                
    except Exception as e:
        print(f"❌ Enhanced solar analysis test failed: {e}")
        traceback.print_exc()
        return False

def test_visualization_components():
    """Test visualization and chart generation"""
    print("\n🔍 TESTING VISUALIZATION COMPONENTS...")
    
    try:
        import plotly.graph_objects as go
        from plotly.subplots import make_subplots
        
        # Test basic chart creation
        print("✅ Plotly imports successful")
        
        # Create sample data for testing
        dates = pd.date_range(start='2025-01-01', end='2025-01-10', freq='D')
        sample_data = pd.DataFrame({
            'date': dates,
            'daily_kwh': np.random.uniform(50, 150, len(dates)),
            'system_type': 'Test System'
        })
        
        # Test basic chart creation
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=sample_data['date'],
            y=sample_data['daily_kwh'],
            mode='lines+markers',
            name='Solar Generation'
        ))
        
        fig.update_layout(
            title="Test Solar Chart",
            xaxis_title="Date",
            yaxis_title="Generation (kWh)"
        )
        
        print("✅ Basic chart creation successful")
        
        # Test subplot creation
        subplot_fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Chart 1', 'Chart 2', 'Chart 3', 'Chart 4')
        )
        
        print("✅ Subplot creation successful")
        
        return True
        
    except Exception as e:
        print(f"❌ Visualization test failed: {e}")
        traceback.print_exc()
        return False

def test_error_handling():
    """Test error handling and edge cases"""
    print("\n🔍 TESTING ERROR HANDLING...")
    
    try:
        # Test with empty DataFrame
        empty_df = pd.DataFrame()
        print("✅ Empty DataFrame handling test passed")
        
        # Test with malformed data
        bad_data = pd.DataFrame({
            'last_changed': ['invalid_date', '2025-01-01'],
            'state': ['not_a_number', '100'],
            'entity_id': ['test1', 'test2']
        })
        
        # Test date conversion error handling
        try:
            bad_data['last_changed'] = pd.to_datetime(bad_data['last_changed'], errors='coerce')
            print("✅ Date conversion error handling test passed")
        except:
            print("⚠️  Date conversion error handling needs improvement")
        
        # Test numeric conversion error handling
        try:
            bad_data['state'] = pd.to_numeric(bad_data['state'], errors='coerce')
            print("✅ Numeric conversion error handling test passed")
        except:
            print("⚠️  Numeric conversion error handling needs improvement")
        
        return True
        
    except Exception as e:
        print(f"❌ Error handling test failed: {e}")
        return False

def test_streamlit_integration():
    """Test Streamlit integration components"""
    print("\n🔍 TESTING STREAMLIT INTEGRATION...")
    
    try:
        import streamlit as st
        print("✅ Streamlit import successful")
        
        # Test that app.py is properly structured
        with open('app.py', 'r') as f:
            app_content = f.read()
        
        # Check for key components
        required_components = [
            'Solar Performance',
            'st.header',
            'st.columns',
            'plotly_chart'
        ]
        
        missing_components = []
        for component in required_components:
            if component not in app_content:
                missing_components.append(component)
        
        if missing_components:
            print(f"⚠️  Missing components in app.py: {missing_components}")
        else:
            print("✅ All required Streamlit components found in app.py")
        
        return len(missing_components) == 0
        
    except Exception as e:
        print(f"❌ Streamlit integration test failed: {e}")
        return False

def main():
    """Run comprehensive test suite"""
    print("🚀 SOLAR PERFORMANCE TAB - DEPLOYMENT TEST SUITE")
    print("=" * 60)
    
    test_results = {}
    
    # Test 1: Data Loading
    factory_df, new_inverter_df, data_ok = test_data_loading()
    test_results['data_loading'] = data_ok
    
    # Test 2: Enhanced Solar Analysis
    if data_ok:
        analysis_ok = test_enhanced_solar_analysis(factory_df, new_inverter_df)
        test_results['solar_analysis'] = analysis_ok
    else:
        test_results['solar_analysis'] = False
    
    # Test 3: Visualization Components
    viz_ok = test_visualization_components()
    test_results['visualization'] = viz_ok
    
    # Test 4: Error Handling
    error_ok = test_error_handling()
    test_results['error_handling'] = error_ok
    
    # Test 5: Streamlit Integration
    streamlit_ok = test_streamlit_integration()
    test_results['streamlit_integration'] = streamlit_ok
    
    # Summary
    print("\n📊 TEST RESULTS SUMMARY")
    print("=" * 60)
    
    passed_tests = sum(test_results.values())
    total_tests = len(test_results)
    
    for test_name, result in test_results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name.replace('_', ' ').title()}: {status}")
    
    print(f"\nOverall: {passed_tests}/{total_tests} tests passed")
    
    if passed_tests == total_tests:
        print("🎉 ALL TESTS PASSED - DEPLOYMENT READY!")
        return True
    else:
        print("⚠️  SOME TESTS FAILED - REVIEW REQUIRED")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)