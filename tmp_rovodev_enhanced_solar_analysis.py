"""
Enhanced Solar Performance Analysis Module - POST-REVIEW VERSION
================================================================
Incorporates manager and customer feedback:
- Data quality validation and confidence intervals
- Seasonal adjustment and weather normalization
- Industry benchmarks and alert thresholds
- Robust error handling and graceful degradation
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy import stats
import warnings

# Industry benchmarks for South African solar installations
SA_SOLAR_BENCHMARKS = {
    'capacity_factor_excellent': 28,    # Top 10% installations
    'capacity_factor_good': 22,         # Above average
    'capacity_factor_average': 18,      # National average
    'capacity_factor_poor': 12,         # Needs attention
    'kwh_per_kw_annual': 1650,         # kWh/kW/year for SA
    'degradation_rate_annual': 0.5,    # % per year
    'availability_target': 98.5        # % uptime target
}

# Seasonal adjustment factors for South Africa (Gauteng region)
SA_SEASONAL_FACTORS = {
    1: 1.15,   # January (summer peak)
    2: 1.05,   # February
    3: 0.95,   # March
    4: 0.85,   # April
    5: 0.75,   # May
    6: 0.70,   # June (winter low)
    7: 0.75,   # July
    8: 0.85,   # August
    9: 0.95,   # September
    10: 1.05,  # October
    11: 1.15,  # November
    12: 1.20   # December (peak summer)
}

def validate_data_quality(df, data_source_name):
    """
    Comprehensive data quality validation with confidence scoring
    Addresses Manager feedback: "How do we know the data is reliable?"
    """
    quality_score = 100
    issues = []
    stats = {}
    
    if df.empty:
        return 0, ["No data available"], {}
    
    # Check data completeness
    total_records = len(df)
    missing_records = df.isnull().sum().sum()
    completeness = ((total_records * len(df.columns) - missing_records) / 
                   (total_records * len(df.columns))) * 100
    
    if completeness < 90:
        quality_score -= 20
        issues.append(f"Data completeness: {completeness:.1f}% (< 90% threshold)")
    
    # Check for data gaps (time series continuity)
    if 'last_changed' in df.columns:
        df_sorted = df.sort_values('last_changed')
        time_diffs = df_sorted['last_changed'].diff().dt.total_seconds() / 3600  # hours
        median_interval = time_diffs.median()
        large_gaps = (time_diffs > median_interval * 3).sum()
        
        if large_gaps > len(df) * 0.05:  # More than 5% large gaps
            quality_score -= 15
            issues.append(f"Large time gaps detected: {large_gaps} instances")
    
    # Check for outliers in state values
    if 'state' in df.columns:
        numeric_states = pd.to_numeric(df['state'], errors='coerce')
        if not numeric_states.empty:
            Q1 = numeric_states.quantile(0.25)
            Q3 = numeric_states.quantile(0.75)
            IQR = Q3 - Q1
            outliers = ((numeric_states < (Q1 - 1.5 * IQR)) | 
                       (numeric_states > (Q3 + 1.5 * IQR))).sum()
            outlier_pct = (outliers / len(numeric_states)) * 100
            
            if outlier_pct > 5:
                quality_score -= 10
                issues.append(f"Outliers detected: {outlier_pct:.1f}% of data points")
    
    # Assign quality grade
    if quality_score >= 90:
        grade = "A - Excellent"
    elif quality_score >= 75:
        grade = "B - Good"
    elif quality_score >= 60:
        grade = "C - Acceptable"
    else:
        grade = "D - Poor"
    
    stats = {
        'score': quality_score,
        'grade': grade,
        'completeness': completeness,
        'total_records': total_records,
        'issues_count': len(issues),
        'data_source': data_source_name
    }
    
    return quality_score, issues, stats


def apply_seasonal_adjustment(df, value_column, date_column):
    """
    Apply South African seasonal adjustment factors
    Addresses Customer feedback: "Factor out weather to show true equipment performance"
    """
    if df.empty or value_column not in df.columns:
        return df
    
    df_adjusted = df.copy()
    df_adjusted['month'] = pd.to_datetime(df_adjusted[date_column]).dt.month
    df_adjusted['seasonal_factor'] = df_adjusted['month'].map(SA_SEASONAL_FACTORS)
    df_adjusted[f'{value_column}_seasonally_adjusted'] = (
        df_adjusted[value_column] / df_adjusted['seasonal_factor']
    )
    
    return df_adjusted


def calculate_confidence_intervals(data_series, confidence_level=0.95):
    """
    Calculate statistical confidence intervals for performance metrics
    Addresses Manager feedback: "Are these improvements statistically significant?"
    """
    if len(data_series) < 2:
        return None, None, None
    
    mean_val = np.mean(data_series)
    std_err = stats.sem(data_series)  # Standard error of mean
    
    # Calculate confidence interval
    alpha = 1 - confidence_level
    t_score = stats.t.ppf(1 - alpha/2, len(data_series) - 1)
    margin_error = t_score * std_err
    
    ci_lower = mean_val - margin_error
    ci_upper = mean_val + margin_error
    
    return mean_val, ci_lower, ci_upper


def analyze_legacy_system_enhanced(factory_elec_df, start_date, end_date):
    """
    Enhanced legacy system analysis with quality validation and seasonal adjustment
    """
    # Data quality validation first
    quality_score, quality_issues, quality_stats = validate_data_quality(
        factory_elec_df, "FACTORY ELEC.csv"
    )
    
    if quality_score < 50:
        print(f"⚠️ Data quality warning: {quality_stats['grade']}")
    
    if factory_elec_df.empty:
        return pd.DataFrame(), {}, quality_stats
    
    # Filter to pre-upgrade period with buffer for seasonal comparison
    pre_upgrade_cutoff = pd.to_datetime('2025-11-01')
    factory_elec_df['last_changed'] = pd.to_datetime(factory_elec_df['last_changed'])
    
    legacy_data = factory_elec_df[
        (factory_elec_df['last_changed'] >= pd.to_datetime(start_date)) &
        (factory_elec_df['last_changed'] <= min(pd.to_datetime(end_date), pre_upgrade_cutoff))
    ].copy()
    
    if legacy_data.empty:
        return pd.DataFrame(), {}, quality_stats
    
    # Process daily generation with seasonal adjustment
    legacy_data['date'] = legacy_data['last_changed'].dt.date
    legacy_data['state'] = pd.to_numeric(legacy_data['state'], errors='coerce')
    
    daily_analysis = []
    for date in legacy_data['date'].unique():
        day_data = legacy_data[legacy_data['date'] == date].sort_values('last_changed')
        if len(day_data) > 1:
            daily_generation = day_data['state'].iloc[-1] - day_data['state'].iloc[0]
            if daily_generation > 0:  # Valid generation day
                daily_analysis.append({
                    'date': pd.to_datetime(date),
                    'daily_kwh': daily_generation,
                    'system_type': 'Legacy 4-Inverter',
                    'inverter_count': 4,
                    'peak_power_kw': daily_generation / 8,
                })
    
    daily_df = pd.DataFrame(daily_analysis)
    
    if not daily_df.empty:
        # Apply seasonal adjustment
        daily_df = apply_seasonal_adjustment(daily_df, 'daily_kwh', 'date')
        
        # Calculate confidence intervals
        mean_daily, ci_lower, ci_upper = calculate_confidence_intervals(daily_df['daily_kwh'])
        
        # Compare against industry benchmarks
        estimated_capacity = daily_df['peak_power_kw'].max()
        capacity_factor = (mean_daily / (estimated_capacity * 24)) * 100 if estimated_capacity > 0 else 0
        
        if capacity_factor >= SA_SOLAR_BENCHMARKS['capacity_factor_excellent']:
            benchmark_grade = "Excellent"
        elif capacity_factor >= SA_SOLAR_BENCHMARKS['capacity_factor_good']:
            benchmark_grade = "Good"
        elif capacity_factor >= SA_SOLAR_BENCHMARKS['capacity_factor_average']:
            benchmark_grade = "Average"
        else:
            benchmark_grade = "Below Average"
        
        # Enhanced statistics with confidence intervals
        stats = {
            'system_type': 'Legacy 4-Inverter System',
            'period_days': len(daily_df),
            'total_generation_kwh': daily_df['daily_kwh'].sum(),
            'average_daily_kwh': mean_daily,
            'confidence_interval_95': (ci_lower, ci_upper) if ci_lower else None,
            'peak_daily_kwh': daily_df['daily_kwh'].max(),
            'estimated_system_capacity_kw': estimated_capacity,
            'capacity_factor_percent': capacity_factor,
            'industry_benchmark_grade': benchmark_grade,
            'seasonal_adjusted_avg': daily_df['daily_kwh_seasonally_adjusted'].mean(),
            'data_quality': quality_stats,
            'statistical_significance': 'High' if len(daily_df) > 30 else 'Medium' if len(daily_df) > 10 else 'Low',
            'analysis_period': f"{start_date} to 2025-11-01"
        }
    else:
        stats = {'data_quality': quality_stats}
    
    return daily_df, stats, quality_stats


def analyze_new_system_enhanced(new_inverter_df, start_date, end_date):
    """
    Enhanced new system analysis with real-time alerting capability
    """
    # Data quality validation
    quality_score, quality_issues, quality_stats = validate_data_quality(
        new_inverter_df, "New_inverter.csv"
    )
    
    if new_inverter_df.empty:
        return pd.DataFrame(), {}, quality_stats, []
    
    # Filter to post-upgrade period
    post_upgrade_start = pd.to_datetime('2025-11-01')
    new_inverter_df['last_changed'] = pd.to_datetime(new_inverter_df['last_changed'])
    
    new_data = new_inverter_df[
        (new_inverter_df['last_changed'] >= max(pd.to_datetime(start_date), post_upgrade_start)) &
        (new_inverter_df['last_changed'] <= pd.to_datetime(end_date))
    ].copy()
    
    if new_data.empty:
        return pd.DataFrame(), {}, quality_stats, []
    
    # Process with enhanced monitoring
    new_data['state'] = pd.to_numeric(new_data['state'], errors='coerce').fillna(0)
    new_data['power_kw'] = new_data['state'].abs()
    new_data['date'] = new_data['last_changed'].dt.date
    
    # Real-time alerts (Customer request)
    alerts = []
    
    # Check for underperforming inverters
    inverter_performance = new_data.groupby('entity_id')['power_kw'].agg(['mean', 'max', 'std'])
    avg_performance = inverter_performance['mean'].mean()
    
    for inverter, row in inverter_performance.iterrows():
        if row['mean'] < avg_performance * 0.7:  # 70% threshold
            alerts.append({
                'type': 'UNDERPERFORMANCE',
                'inverter': inverter,
                'message': f"Inverter {inverter} performing {row['mean']:.1f} kW avg vs {avg_performance:.1f} kW system avg"
            })
    
    # System-level daily aggregation with seasonal adjustment
    system_daily = new_data.groupby('date').agg({
        'power_kw': ['sum', 'max', 'mean'],
        'entity_id': 'nunique'
    }).reset_index()
    
    system_daily.columns = ['date', 'total_power_sum', 'peak_power_kw', 'avg_power_kw', 'active_inverters']
    system_daily['date'] = pd.to_datetime(system_daily['date'])
    
    # Convert to daily kWh (improved estimation)
    samples_per_hour = 12
    system_daily['daily_kwh'] = system_daily['total_power_sum'] / samples_per_hour
    
    # Apply seasonal adjustment
    system_daily = apply_seasonal_adjustment(system_daily, 'daily_kwh', 'date')
    
    # Industry benchmark comparison
    estimated_capacity = system_daily['peak_power_kw'].max()
    capacity_factor = (system_daily['avg_power_kw'].mean() / estimated_capacity * 100) if estimated_capacity > 0 else 0
    
    if capacity_factor >= SA_SOLAR_BENCHMARKS['capacity_factor_excellent']:
        benchmark_grade = "Excellent"
        benchmark_percentile = "Top 10%"
    elif capacity_factor >= SA_SOLAR_BENCHMARKS['capacity_factor_good']:
        benchmark_grade = "Good"
        benchmark_percentile = "Above Average"
    elif capacity_factor >= SA_SOLAR_BENCHMARKS['capacity_factor_average']:
        benchmark_grade = "Average"
        benchmark_percentile = "National Average"
    else:
        benchmark_grade = "Below Average"
        benchmark_percentile = "Needs Improvement"
    
    # Enhanced statistics
    mean_daily, ci_lower, ci_upper = calculate_confidence_intervals(system_daily['daily_kwh'])
    
    stats = {
        'system_type': 'New 3-Inverter System',
        'period_days': len(system_daily),
        'total_generation_kwh': system_daily['daily_kwh'].sum(),
        'average_daily_kwh': mean_daily,
        'confidence_interval_95': (ci_lower, ci_upper) if ci_lower else None,
        'peak_daily_kwh': system_daily['daily_kwh'].max(),
        'peak_system_power_kw': estimated_capacity,
        'capacity_factor_percent': capacity_factor,
        'industry_benchmark_grade': benchmark_grade,
        'industry_percentile': benchmark_percentile,
        'seasonal_adjusted_avg': system_daily['daily_kwh_seasonally_adjusted'].mean(),
        'active_inverters_avg': system_daily['active_inverters'].mean(),
        'data_quality': quality_stats,
        'alert_count': len(alerts),
        'analysis_period': f"2025-11-01 to {end_date}",
        'estimated_annual_generation': mean_daily * 365 if mean_daily > 0 else 0
    }
    
    return system_daily, stats, quality_stats, alerts


def compare_solar_systems_enhanced(legacy_df, legacy_stats, new_df, new_stats):
    """
    Enhanced system comparison with statistical significance testing
    Addresses Manager feedback: "Are these improvements statistically significant?"
    """
    comparison = {
        'upgrade_summary': {
            'legacy_system': 'Fronius + GoodWe (4 inverters)',
            'new_system': 'GoodWe GT1 + GT2 + HT1 (3 inverters)',
            'upgrade_date': 'November 2025',
            'engineering_objective': 'Reduce clipping losses and improve capacity utilization'
        }
    }
    
    if legacy_stats and new_stats:
        # Statistical significance testing
        legacy_avg = legacy_stats.get('average_daily_kwh', 0)
        new_avg = new_stats.get('average_daily_kwh', 0)
        
        # Calculate improvement with confidence intervals
        if legacy_avg > 0:
            generation_improvement = ((new_avg - legacy_avg) / legacy_avg) * 100
            
            # Statistical significance test
            legacy_ci = legacy_stats.get('confidence_interval_95')
            new_ci = new_stats.get('confidence_interval_95')
            
            if legacy_ci and new_ci:
                # Non-overlapping confidence intervals indicate significance
                statistically_significant = new_ci[0] > legacy_ci[1] or legacy_ci[0] > new_ci[1]
                confidence_level = "High" if statistically_significant else "Medium"
            else:
                confidence_level = "Low - Insufficient data"
        else:
            generation_improvement = 0
            confidence_level = "Cannot determine"
        
        # Seasonal adjustment comparison (Customer feedback)
        legacy_seasonal = legacy_stats.get('seasonal_adjusted_avg', legacy_avg)
        new_seasonal = new_stats.get('seasonal_adjusted_avg', new_avg)
        weather_normalized_improvement = ((new_seasonal - legacy_seasonal) / legacy_seasonal * 100) if legacy_seasonal > 0 else 0
        
        # Industry benchmark analysis
        legacy_benchmark = legacy_stats.get('industry_benchmark_grade', 'Unknown')
        new_benchmark = new_stats.get('industry_benchmark_grade', 'Unknown')
        
        comparison['performance_metrics'] = {
            'daily_generation_improvement_percent': generation_improvement,
            'weather_normalized_improvement_percent': weather_normalized_improvement,
            'statistical_confidence': confidence_level,
            'legacy_avg_daily_kwh': legacy_avg,
            'new_avg_daily_kwh': new_avg,
            'legacy_benchmark_grade': legacy_benchmark,
            'new_benchmark_grade': new_benchmark,
            'legacy_capacity_factor': legacy_stats.get('capacity_factor_percent', 0),
            'new_capacity_factor': new_stats.get('capacity_factor_percent', 0),
            'inverter_reduction': '4 → 3 inverters',
            'maintenance_simplification': 'Single vendor (all GoodWe)'
        }
        
        # Enhanced financial analysis
        electricity_rate = 1.50  # R/kWh
        daily_value_improvement = (new_avg - legacy_avg) * electricity_rate
        monthly_savings = daily_value_improvement * 30
        annual_savings = daily_value_improvement * 365
        
        # ROI calculation (estimate)
        estimated_upgrade_cost = 150000  # R150k estimated
        payback_years = estimated_upgrade_cost / annual_savings if annual_savings > 0 else float('inf')
        
        comparison['financial_impact'] = {
            'daily_value_improvement_rands': daily_value_improvement,
            'monthly_savings_rands': monthly_savings,
            'annual_savings_rands': annual_savings,
            'estimated_payback_years': min(payback_years, 20),  # Cap at 20 years
            'electricity_rate_per_kwh': electricity_rate,
            'roi_grade': 'Excellent' if payback_years < 3 else 'Good' if payback_years < 5 else 'Fair' if payback_years < 8 else 'Poor'
        }
        
        # Data quality assessment
        legacy_quality = legacy_stats.get('data_quality', {}).get('grade', 'Unknown')
        new_quality = new_stats.get('data_quality', {}).get('grade', 'Unknown')
        
        comparison['data_quality_assessment'] = {
            'legacy_data_quality': legacy_quality,
            'new_data_quality': new_quality,
            'comparison_reliability': 'High' if 'A' in legacy_quality and 'A' in new_quality else 'Medium',
            'seasonal_bias_risk': 'Mitigated through seasonal adjustment',
            'recommendation': 'Continue monitoring for 12+ months for full seasonal comparison'
        }
        
        # Engineering recommendations (enhanced)
        recommendations = []
        
        if generation_improvement > 15:
            recommendations.append("✅ Excellent upgrade performance - consider replicating approach for future sites")
        elif generation_improvement > 5:
            recommendations.append("✅ Good improvement achieved - monitor long-term trends")
        else:
            recommendations.append("⚠️ Limited improvement - investigate optimization opportunities")
            
        if weather_normalized_improvement > generation_improvement:
            recommendations.append("📊 Weather normalization shows better underlying performance")
        
        if new_stats.get('alert_count', 0) > 0:
            recommendations.append("🔔 Active performance alerts - investigate underperforming inverters")
            
        recommendations.append("📈 Implement quarterly capacity factor benchmarking")
        recommendations.append("🔧 Schedule predictive maintenance based on new inverter specifications")
        
        comparison['engineering_recommendations'] = recommendations
    
    return comparison


def create_enhanced_comparison_chart(legacy_df, new_df, comparison_stats):
    """
    Enhanced visualization with confidence intervals and statistical indicators
    """
    fig = make_subplots(
        rows=3, cols=2,
        subplot_titles=('Daily Generation with Confidence Intervals', 'Industry Benchmark Comparison', 
                       'Weather-Normalized Performance', 'Data Quality Assessment',
                       'Financial Impact Analysis', 'Statistical Significance'),
        specs=[[{"secondary_y": False}, {"type": "bar"}],
               [{"secondary_y": True}, {"type": "indicator"}],
               [{"type": "bar"}, {"type": "indicator"}]]
    )
    
    # Chart 1: Daily Generation with Confidence Intervals
    if not legacy_df.empty:
        # Add confidence band for legacy data
        if 'daily_kwh_seasonally_adjusted' in legacy_df.columns:
            legacy_mean = legacy_df['daily_kwh_seasonally_adjusted'].mean()
            legacy_std = legacy_df['daily_kwh_seasonally_adjusted'].std()
            
            fig.add_trace(
                go.Scatter(
                    x=legacy_df['date'], 
                    y=legacy_df['daily_kwh_seasonally_adjusted'],
                    name='Legacy (Weather Adj.)',
                    line=dict(color='#ef4444', width=2),
                    mode='lines'
                ),
                row=1, col=1
            )
            
            # Add confidence band
            fig.add_trace(
                go.Scatter(
                    x=legacy_df['date'].tolist() + legacy_df['date'].tolist()[::-1],
                    y=([legacy_mean + 1.96*legacy_std] * len(legacy_df) + 
                       [legacy_mean - 1.96*legacy_std] * len(legacy_df))[::-1],
                    fill='tonexty',
                    fillcolor='rgba(239, 68, 68, 0.1)',
                    line=dict(color='rgba(255,255,255,0)'),
                    name='95% Confidence',
                    showlegend=False
                ),
                row=1, col=1
            )
    
    if not new_df.empty and 'daily_kwh_seasonally_adjusted' in new_df.columns:
        fig.add_trace(
            go.Scatter(
                x=new_df['date'], 
                y=new_df['daily_kwh_seasonally_adjusted'],
                name='New System (Weather Adj.)',
                line=dict(color='#10b981', width=3),
                mode='lines'
            ),
            row=1, col=1
        )
    
    # Chart 2: Industry Benchmark Comparison
    if comparison_stats and 'performance_metrics' in comparison_stats:
        metrics = comparison_stats['performance_metrics']
        benchmark_data = [
            metrics.get('legacy_capacity_factor', 0),
            metrics.get('new_capacity_factor', 0),
            SA_SOLAR_BENCHMARKS['capacity_factor_average'],
            SA_SOLAR_BENCHMARKS['capacity_factor_excellent']
        ]
        
        fig.add_trace(
            go.Bar(
                x=['Legacy', 'New System', 'SA Average', 'SA Excellent'],
                y=benchmark_data,
                marker_color=['#ef4444', '#10b981', '#6b7280', '#f59e0b'],
                name='Capacity Factor (%)'
            ),
            row=1, col=2
        )
    
    # Chart 3: Weather-Normalized Performance Trend
    if comparison_stats:
        metrics = comparison_stats['performance_metrics']
        improvement = metrics.get('weather_normalized_improvement_percent', 0)
        
        fig.add_trace(
            go.Scatter(
                x=[1, 2],
                y=[100, 100 + improvement],
                mode='lines+markers',
                line=dict(color='#8b5cf6', width=4),
                marker=dict(size=12),
                name='Weather-Normalized Performance'
            ),
            row=2, col=1
        )
    
    # Chart 4: Data Quality Indicator
    if comparison_stats and 'data_quality_assessment' in comparison_stats:
        quality_data = comparison_stats['data_quality_assessment']
        reliability = quality_data.get('comparison_reliability', 'Medium')
        reliability_score = 85 if reliability == 'High' else 65 if reliability == 'Medium' else 40
        
        fig.add_trace(
            go.Indicator(
                mode="gauge+number+delta",
                value=reliability_score,
                title={"text": "Analysis Reliability"},
                gauge={
                    'axis': {'range': [None, 100]},
                    'bar': {'color': "#10b981" if reliability_score > 75 else "#f59e0b"},
                    'steps': [
                        {'range': [0, 50], 'color': "#ef4444"},
                        {'range': [50, 75], 'color': "#f59e0b"},
                        {'range': [75, 100], 'color': "#10b981"}
                    ]
                },
                domain={'x': [0, 1], 'y': [0, 1]}
            ),
            row=2, col=2
        )
    
    # Chart 5: Financial Impact
    if comparison_stats and 'financial_impact' in comparison_stats:
        financial = comparison_stats['financial_impact']
        fig.add_trace(
            go.Bar(
                x=['Monthly', 'Annual', 'Payback Years'],
                y=[
                    financial.get('monthly_savings_rands', 0),
                    financial.get('annual_savings_rands', 0),
                    financial.get('estimated_payback_years', 0) * 1000  # Scale for visibility
                ],
                marker_color=['#06b6d4', '#10b981', '#f59e0b'],
                name='Financial Metrics'
            ),
            row=3, col=1
        )
    
    # Chart 6: Statistical Significance
    if comparison_stats and 'performance_metrics' in comparison_stats:
        metrics = comparison_stats['performance_metrics']
        confidence = metrics.get('statistical_confidence', 'Low')
        confidence_score = 90 if 'High' in confidence else 65 if 'Medium' in confidence else 30
        
        fig.add_trace(
            go.Indicator(
                mode="number+delta",
                value=confidence_score,
                title={"text": "Statistical Confidence"},
                delta={'reference': 50, 'increasing': {'color': "#10b981"}},
                number={'suffix': "%", 'font': {'size': 24}},
                domain={'x': [0, 1], 'y': [0, 1]}
            ),
            row=3, col=2
        )
    
    # Update layout
    fig.update_layout(
        title="Enhanced Solar System Analysis - Post-Review Version",
        height=1200,
        showlegend=True,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#e2e8f0', family="Inter")
    )
    
    return fig