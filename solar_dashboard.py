"""
Durr Energy - Solar Performance Dashboard Integration
===================================================
Senior Technical Implementation - Production Ready

Replaces existing Solar Performance tab with engineered before/after analysis.

Author: Senior Technical Consultant
Date: 2025-12-17
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
from solar_performance_engine import SolarSystemAnalyzer

def render_solar_performance_tab():
    """
    Complete replacement for the Solar Performance tab.
    Focuses on quantitative before/after analysis of the November 2025 upgrade.
    """
    
    st.markdown("## ☀️ Solar Performance Analysis")
    st.markdown("**Engineering Focus**: Quantitative analysis of November 2025 inverter upgrade impact")
    
    # Initialize analyzer
    analyzer = SolarSystemAnalyzer()
    
    # Data loading section
    with st.expander("📋 Data Sources & Validation", expanded=True):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Pre-Upgrade System")
            st.info("📊 **Legacy Configuration**: 3× Fronius + 1× GoodWe inverters")
            
            # Load and validate pre-upgrade data
            pre_data, pre_validation = analyzer.load_and_validate_data("previous_inverter_system.csv")
            
            if pre_validation['errors']:
                st.error(f"⚠️ Pre-upgrade data issues: {'; '.join(pre_validation['errors'])}")
            else:
                st.success(f"✅ {pre_validation['total_records']} records loaded")
                if pre_validation['date_range']:
                    start, end = pre_validation['date_range']
                    st.write(f"📅 **Period**: {start.strftime('%Y-%m-%d')} to {end.strftime('%Y-%m-%d')}")
                st.write(f"🔌 **Entities**: {', '.join(pre_validation['entities'])}")
                st.write(f"📈 **Quality**: {pre_validation['data_quality']:.1f}%")
        
        with col2:
            st.markdown("### Post-Upgrade System")
            st.info("📊 **New Configuration**: 3× GoodWe inverters only")
            
            # Load and validate post-upgrade data
            post_data, post_validation = analyzer.load_and_validate_data("New_inverter.csv")
            
            if post_validation['errors']:
                st.error(f"⚠️ Post-upgrade data issues: {'; '.join(post_validation['errors'])}")
            else:
                st.success(f"✅ {post_validation['total_records']} records loaded")
                if post_validation['date_range']:
                    start, end = post_validation['date_range']
                    st.write(f"📅 **Period**: {start.strftime('%Y-%m-%d')} to {end.strftime('%Y-%m-%d')}")
                st.write(f"🔌 **Entities**: {', '.join(post_validation['entities'])}")
                st.write(f"📈 **Quality**: {post_validation['data_quality']:.1f}%")
    
    # Analysis section
    if not pre_data.empty or not post_data.empty:
        
        # Perform analysis
        with st.spinner("🔬 Performing engineering analysis..."):
            legacy_stats = analyzer.analyze_legacy_system(pre_data)
            new_stats = analyzer.analyze_new_system(post_data)
            comparison = analyzer.compare_systems(legacy_stats, new_stats)
        
        # Key Performance Metrics
        st.markdown("---")
        st.markdown("### 🎯 Key Performance Impact")
        
        if comparison:
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                energy_improvement = comparison['energy_improvement_pct']
                st.metric(
                    "Daily Energy Improvement",
                    f"{energy_improvement:+.1f}%",
                    delta=f"{comparison['new_daily_kwh']:.1f} kWh vs {comparison['legacy_daily_kwh']:.1f} kWh"
                )
            
            with col2:
                peak_improvement = comparison['peak_power_improvement_pct']
                st.metric(
                    "Peak Power Improvement",
                    f"{peak_improvement:+.1f}%",
                    delta=f"{comparison['new_peak_kw']:.1f} kW vs {comparison['legacy_peak_kw']:.1f} kW"
                )
            
            with col3:
                cf_improvement = comparison['capacity_factor_improvement_pct']
                st.metric(
                    "Capacity Factor Improvement",
                    f"{cf_improvement:+.1f}%",
                    delta="System efficiency gain"
                )
            
            with col4:
                annual_value = comparison['annual_value_increase_rands']
                st.metric(
                    "Annual Value Impact",
                    f"R {annual_value:,.0f}",
                    delta="Estimated additional revenue"
                )
            
            # Engineering summary
            st.markdown("### 📋 Engineering Summary")
            
            if energy_improvement > 0:
                st.success(f"✅ **Positive Impact**: {energy_improvement:.1f}% improvement in energy generation")
            else:
                st.warning(f"⚠️ **Performance Concern**: {energy_improvement:.1f}% decrease in energy generation")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**System Configuration Changes:**")
                st.write(f"• Fronius inverters removed: {comparison['fronius_removed']}")
                st.write(f"• Total inverter reduction: {comparison['inverter_reduction']}")
                st.write(f"• New configuration: 3× GoodWe only")
            
            with col2:
                st.markdown("**Performance Metrics:**")
                st.write(f"• Peak power gain: {peak_improvement:+.1f}%")
                st.write(f"• Capacity factor change: {cf_improvement:+.1f}%")
                st.write(f"• ROI impact: {comparison['upgrade_roi_impact']}")
        
        # Detailed Comparison Charts
        st.markdown("---")
        st.markdown("### 📊 System Performance Comparison")
        
        tab1, tab2 = st.tabs(["📈 Performance Metrics", "📉 Time Series Analysis"])
        
        with tab1:
            if comparison:
                fig_comparison = analyzer.create_comparison_chart(legacy_stats, new_stats, comparison)
                st.plotly_chart(fig_comparison, use_container_width=True)
                
                # Download data
                if st.button("⬇️ Download Comparison Data"):
                    comparison_df = pd.DataFrame([
                        {
                            'metric': 'Daily Energy (kWh)',
                            'legacy_system': legacy_stats['avg_daily_kwh'],
                            'new_system': new_stats['avg_daily_kwh'],
                            'improvement_pct': comparison['energy_improvement_pct']
                        },
                        {
                            'metric': 'Peak Power (kW)',
                            'legacy_system': legacy_stats['peak_system_kw'],
                            'new_system': new_stats['peak_system_kw'],
                            'improvement_pct': comparison['peak_power_improvement_pct']
                        },
                        {
                            'metric': 'Capacity Factor (%)',
                            'legacy_system': legacy_stats['avg_capacity_factor'] * 100,
                            'new_system': new_stats['avg_capacity_factor'] * 100,
                            'improvement_pct': comparison['capacity_factor_improvement_pct']
                        }
                    ])
                    
                    st.download_button(
                        "Download CSV",
                        comparison_df.to_csv(index=False),
                        "solar_system_comparison.csv",
                        "text/csv"
                    )
        
        with tab2:
            if legacy_stats and new_stats:
                fig_timeline = analyzer.create_time_series_chart(legacy_stats, new_stats)
                st.plotly_chart(fig_timeline, use_container_width=True)
        
        # Technical Details
        st.markdown("---")
        st.markdown("### 🔧 Technical Analysis Details")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Legacy System Analysis")
            if legacy_stats:
                st.write(f"**Analysis Period**: {legacy_stats['date_range'][0].strftime('%Y-%m-%d')} to {legacy_stats['date_range'][1].strftime('%Y-%m-%d')}")
                st.write(f"**Total Generation**: {legacy_stats['total_kwh']:.0f} kWh")
                st.write(f"**Average Daily**: {legacy_stats['avg_daily_kwh']:.1f} kWh/day")
                st.write(f"**Peak System Power**: {legacy_stats['peak_system_kw']:.1f} kW")
                st.write(f"**Capacity Factor**: {legacy_stats['avg_capacity_factor']:.2%}")
                st.write(f"**Operational Days**: {legacy_stats['total_days']}")
                st.write(f"**Inverter Count**: {legacy_stats['total_inverters']} ({legacy_stats['fronius_inverters']} Fronius + {legacy_stats['goodwe_inverters']} GoodWe)")
                st.write(f"**Economic Value**: R {legacy_stats['estimated_value_rands']:,.0f}")
            else:
                st.error("No legacy system data available")
        
        with col2:
            st.markdown("#### New System Analysis")
            if new_stats:
                st.write(f"**Analysis Period**: {new_stats['date_range'][0].strftime('%Y-%m-%d')} to {new_stats['date_range'][1].strftime('%Y-%m-%d')}")
                st.write(f"**Total Generation**: {new_stats['total_kwh']:.0f} kWh")
                st.write(f"**Average Daily**: {new_stats['avg_daily_kwh']:.1f} kWh/day")
                st.write(f"**Peak System Power**: {new_stats['peak_system_kw']:.1f} kW")
                st.write(f"**Capacity Factor**: {new_stats['avg_capacity_factor']:.2%}")
                st.write(f"**Operational Days**: {new_stats['total_days']}")
                st.write(f"**Inverter Count**: {new_stats['total_inverters']} (All GoodWe)")
                st.write(f"**Economic Value**: R {new_stats['estimated_value_rands']:,.0f}")
                
                # Individual inverter performance
                if 'inverter_performance' in new_stats:
                    st.markdown("**Individual Inverter Performance:**")
                    for inv in new_stats['inverter_performance']:
                        st.write(f"• {inv['inverter']}: {inv['avg_power_kw']:.1f} kW avg, {inv['peak_power_kw']:.1f} kW peak")
            else:
                st.error("No new system data available")
        
        # Professional Recommendations
        st.markdown("---")
        st.markdown("### 💡 Engineering Recommendations")
        
        if comparison:
            if comparison['energy_improvement_pct'] > 5:
                st.success("✅ **Upgrade Successful**: Significant performance improvement achieved")
                st.write("• Continue monitoring for sustained performance")
                st.write("• Consider expansion based on positive ROI")
            elif comparison['energy_improvement_pct'] > 0:
                st.info("ℹ️ **Marginal Improvement**: Modest gains achieved")
                st.write("• Monitor for seasonal variations")
                st.write("• Evaluate additional optimization opportunities")
            else:
                st.warning("⚠️ **Performance Concern**: System underperforming expectations")
                st.write("• Investigate potential configuration issues")
                st.write("• Verify inverter sizing and placement")
                st.write("• Consider professional system audit")
            
            st.write(f"• **System Reliability**: Reduced from {legacy_stats.get('total_inverters', 0)} to {new_stats.get('total_inverters', 0)} inverters may improve reliability")
            st.write(f"• **Maintenance**: Simplified to single-vendor (GoodWe) configuration")
    
    else:
        st.error("❌ **Critical Error**: No solar data available for analysis")
        st.write("**Required files:**")
        st.write("• `previous_inverter_system.csv` (pre-upgrade data)")
        st.write("• `New_inverter.csv` (post-upgrade data)")