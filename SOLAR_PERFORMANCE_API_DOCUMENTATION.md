# Solar Performance Analysis - API Documentation

**Version**: 2.0 Enhanced  
**API Type**: Python Module API  
**Target Audience**: Developers, Data Scientists, System Integrators

---

## 🔌 API Overview

The Solar Performance Analysis API provides programmatic access to advanced solar system analysis, statistical comparisons, and industry benchmarking capabilities.

### Key Features
- **Statistical Analysis**: Professional-grade confidence intervals and significance testing
- **Data Quality Assessment**: Automated validation and reliability scoring
- **Industry Benchmarking**: South African solar performance standards
- **Weather Normalization**: Seasonal adjustment algorithms
- **Real-time Monitoring**: Performance alerts and anomaly detection

### Architecture
```python
solar_analysis/
├── core/
│   ├── data_loader.py          # Data ingestion and validation
│   ├── statistical_engine.py   # Statistical analysis functions
│   ├── quality_assessment.py   # Data quality validation
│   └── benchmark_engine.py     # Industry comparison
├── visualization/
│   ├── chart_generator.py      # Interactive chart creation
│   └── dashboard_components.py # UI component generation
└── utils/
    ├── seasonal_adjustment.py  # Weather normalization
    └── alert_system.py         # Performance monitoring
```

---

## 📚 Core API Reference

### Data Loading Module

#### `load_solar_data(file_path, data_type='legacy')`
**Purpose**: Load and validate solar performance data from CSV files

**Parameters**:
- `file_path` (str): Path to the CSV data file
- `data_type` (str): Either 'legacy' (pre-upgrade) or 'new' (post-upgrade)

**Returns**: `pandas.DataFrame` with validated and cleaned data

**Example**:
```python
from solar_analysis.core.data_loader import load_solar_data

# Load legacy system data
legacy_df = load_solar_data('FACTORY ELEC.csv', data_type='legacy')

# Load new system data  
new_df = load_solar_data('New_inverter.csv', data_type='new')

print(f"Legacy records: {len(legacy_df)}")
print(f"New system records: {len(new_df)}")
```

#### `validate_data_schema(df, expected_columns)`
**Purpose**: Validate DataFrame structure against expected schema

**Parameters**:
- `df` (DataFrame): Data to validate
- `expected_columns` (list): Required column names

**Returns**: `dict` with validation results

**Example**:
```python
validation = validate_data_schema(
    df, 
    ['entity_id', 'state', 'last_changed']
)

if validation['valid']:
    print("✅ Data schema is valid")
else:
    print(f"❌ Schema issues: {validation['errors']}")
```

### Statistical Analysis Module

#### `calculate_confidence_intervals(data_series, confidence_level=0.95)`
**Purpose**: Calculate statistical confidence intervals for performance metrics

**Parameters**:
- `data_series` (array-like): Numeric data for analysis
- `confidence_level` (float): Confidence level (default: 0.95 for 95%)

**Returns**: `tuple` (mean, lower_bound, upper_bound)

**Example**:
```python
from solar_analysis.core.statistical_engine import calculate_confidence_intervals

daily_generation = [45.2, 52.1, 48.7, 55.3, 49.8, 51.2, 47.9]
mean, lower, upper = calculate_confidence_intervals(daily_generation)

print(f"Mean: {mean:.1f} kWh")
print(f"95% CI: [{lower:.1f}, {upper:.1f}] kWh")
```

#### `perform_significance_test(before_data, after_data, alpha=0.05)`
**Purpose**: Test statistical significance of performance improvement

**Parameters**:
- `before_data` (array-like): Pre-upgrade performance data
- `after_data` (array-like): Post-upgrade performance data  
- `alpha` (float): Significance threshold (default: 0.05)

**Returns**: `dict` with test results

**Example**:
```python
from solar_analysis.core.statistical_engine import perform_significance_test

test_result = perform_significance_test(legacy_generation, new_generation)

print(f"p-value: {test_result['p_value']:.4f}")
print(f"Significant: {test_result['is_significant']}")
print(f"Effect size: {test_result['effect_size']:.2f}")
```

### Quality Assessment Module

#### `assess_data_quality(df)`
**Purpose**: Comprehensive data quality assessment with scoring

**Parameters**:
- `df` (DataFrame): Data to assess

**Returns**: `dict` with quality metrics

**Example**:
```python
from solar_analysis.core.quality_assessment import assess_data_quality

quality = assess_data_quality(solar_df)

print(f"Quality Score: {quality['overall_score']}/100")
print(f"Grade: {quality['grade']}")
print(f"Issues: {quality['issue_count']}")

for issue in quality['issues']:
    print(f"⚠️ {issue}")
```

#### Quality Score Components
```python
{
    'overall_score': float,      # 0-100 composite score
    'grade': str,               # A, B, C, or D
    'completeness_score': float, # Missing data assessment
    'continuity_score': float,   # Time gap analysis
    'consistency_score': float,  # Outlier detection
    'issues': list,             # Human-readable issues
    'recommendations': list      # Improvement suggestions
}
```

### Benchmark Engine Module

#### `get_sa_benchmarks()`
**Purpose**: Retrieve South African solar industry benchmarks

**Returns**: `dict` with benchmark data

**Example**:
```python
from solar_analysis.core.benchmark_engine import get_sa_benchmarks

benchmarks = get_sa_benchmarks()

print(f"Excellent CF: {benchmarks['capacity_factor_excellent']}%")
print(f"Average CF: {benchmarks['capacity_factor_average']}%")
print(f"Annual kWh/kW: {benchmarks['kwh_per_kw_annual']}")
```

#### `evaluate_performance(capacity_factor, annual_generation)`
**Purpose**: Evaluate system performance against industry standards

**Parameters**:
- `capacity_factor` (float): System capacity factor (%)
- `annual_generation` (float): Annual kWh/kW generation

**Returns**: `dict` with performance evaluation

**Example**:
```python
evaluation = evaluate_performance(capacity_factor=24.5, annual_generation=1580)

print(f"Grade: {evaluation['grade']}")           # "Good"
print(f"Percentile: {evaluation['percentile']}")  # "Top 30%"
print(f"Ranking: {evaluation['ranking']}")       # "Above Average"
```

---

## 🎨 Visualization API

### Chart Generator Module

#### `create_before_after_comparison(legacy_data, new_data, config=None)`
**Purpose**: Generate comprehensive before/after comparison charts

**Parameters**:
- `legacy_data` (DataFrame): Pre-upgrade system data
- `new_data` (DataFrame): Post-upgrade system data
- `config` (dict): Chart configuration options

**Returns**: `plotly.graph_objects.Figure` object

**Example**:
```python
from solar_analysis.visualization.chart_generator import create_before_after_comparison

config = {
    'title': 'Solar System Upgrade Analysis',
    'height': 800,
    'show_confidence_bands': True,
    'include_benchmarks': True
}

fig = create_before_after_comparison(legacy_df, new_df, config)

# Display in Streamlit
st.plotly_chart(fig, use_container_width=True)

# Save as HTML
fig.write_html('solar_comparison.html')
```

#### `create_performance_dashboard(system_data, alerts=None)`
**Purpose**: Generate real-time performance monitoring dashboard

**Parameters**:
- `system_data` (DataFrame): Current system performance data
- `alerts` (list): Performance alerts to display

**Returns**: `plotly.graph_objects.Figure` with dashboard layout

**Example**:
```python
dashboard_fig = create_performance_dashboard(
    new_system_df, 
    alerts=['Inverter GT2 underperforming']
)

st.plotly_chart(dashboard_fig)
```

### Dashboard Components Module

#### `render_metric_card(title, value, subtitle, color='blue', icon=None)`
**Purpose**: Create standardized metric display cards

**Parameters**:
- `title` (str): Card title
- `value` (str): Primary metric value
- `subtitle` (str): Additional context
- `color` (str): Card color theme
- `icon` (str): Optional icon

**Example**:
```python
from solar_analysis.visualization.dashboard_components import render_metric_card

# In Streamlit app
col1, col2, col3 = st.columns(3)

with col1:
    render_metric_card(
        "Daily Generation Improvement",
        "+15.2%",
        "✅ High Confidence",
        color="green",
        icon="📈"
    )

with col2:
    render_metric_card(
        "Capacity Factor",
        "24.1%",
        "Above SA Average",
        color="blue",
        icon="⚡"
    )
```

---

## 🔧 Utility Functions

### Seasonal Adjustment Module

#### `apply_seasonal_factors(df, value_column, date_column, region='south_africa')`
**Purpose**: Apply regional seasonal adjustment factors

**Parameters**:
- `df` (DataFrame): Data to adjust
- `value_column` (str): Column containing values to adjust
- `date_column` (str): Column containing dates
- `region` (str): Regional factor set to use

**Returns**: `DataFrame` with additional seasonally adjusted column

**Example**:
```python
from solar_analysis.utils.seasonal_adjustment import apply_seasonal_factors

adjusted_df = apply_seasonal_factors(
    solar_df, 
    value_column='daily_kwh',
    date_column='date',
    region='south_africa'
)

# New column: 'daily_kwh_seasonally_adjusted'
print(adjusted_df[['date', 'daily_kwh', 'daily_kwh_seasonally_adjusted']].head())
```

#### `get_seasonal_factors(region='south_africa')`
**Purpose**: Retrieve seasonal adjustment factors for a region

**Returns**: `dict` mapping months to adjustment factors

```python
factors = get_seasonal_factors('south_africa')
# {1: 1.15, 2: 1.05, ..., 12: 1.20}
```

### Alert System Module

#### `detect_performance_anomalies(df, threshold_std=2.0)`
**Purpose**: Detect performance anomalies and generate alerts

**Parameters**:
- `df` (DataFrame): System performance data
- `threshold_std` (float): Standard deviation threshold for anomaly detection

**Returns**: `list` of alert dictionaries

**Example**:
```python
from solar_analysis.utils.alert_system import detect_performance_anomalies

alerts = detect_performance_anomalies(inverter_data, threshold_std=1.5)

for alert in alerts:
    print(f"{alert['type']}: {alert['message']}")
    print(f"Severity: {alert['severity']}")
    print(f"Recommended action: {alert['action']}")
```

#### Alert Structure
```python
{
    'type': str,              # 'UNDERPERFORMANCE', 'DATA_QUALITY', 'ANOMALY'
    'severity': str,          # 'LOW', 'MEDIUM', 'HIGH', 'CRITICAL'
    'message': str,           # Human-readable description
    'entity_id': str,         # Affected inverter/sensor
    'value': float,           # Measured value
    'expected_range': tuple,   # (min, max) expected values
    'timestamp': datetime,     # When detected
    'action': str             # Recommended response
}
```

---

## 🚀 High-Level Analysis Functions

### Main Analysis Pipeline

#### `analyze_solar_upgrade(factory_file, new_file, start_date, end_date, config=None)`
**Purpose**: Complete end-to-end solar upgrade analysis

**Parameters**:
- `factory_file` (str): Path to legacy system data
- `new_file` (str): Path to new system data
- `start_date` (str): Analysis start date (YYYY-MM-DD)
- `end_date` (str): Analysis end date (YYYY-MM-DD)
- `config` (dict): Analysis configuration options

**Returns**: `dict` with comprehensive analysis results

**Example**:
```python
from solar_analysis import analyze_solar_upgrade

config = {
    'seasonal_adjustment': True,
    'confidence_level': 0.95,
    'benchmark_comparison': True,
    'generate_alerts': True
}

results = analyze_solar_upgrade(
    'FACTORY ELEC.csv',
    'New_inverter.csv', 
    '2025-01-01',
    '2025-12-31',
    config
)

# Access results
print(f"Generation improvement: {results['performance']['improvement_percent']:.1f}%")
print(f"Statistical confidence: {results['performance']['confidence_level']}")
print(f"Annual savings: R{results['financial']['annual_savings']:,.0f}")
print(f"Data quality: {results['quality']['overall_grade']}")
```

#### Results Structure
```python
{
    'performance': {
        'improvement_percent': float,
        'confidence_level': str,
        'capacity_factor_before': float,
        'capacity_factor_after': float,
        'weather_normalized_improvement': float
    },
    'financial': {
        'annual_savings': float,
        'monthly_savings': float,
        'payback_years': float,
        'roi_grade': str
    },
    'quality': {
        'overall_grade': str,
        'legacy_score': float,
        'new_score': float,
        'reliability_assessment': str
    },
    'benchmarks': {
        'current_grade': str,
        'industry_percentile': str,
        'comparison_vs_average': float
    },
    'alerts': list,
    'recommendations': list
}
```

---

## 🔒 Error Handling

### Exception Classes

#### `SolarAnalysisError(Exception)`
**Purpose**: Base exception class for solar analysis operations

#### `DataValidationError(SolarAnalysisError)`
**Purpose**: Raised when input data fails validation

**Example**:
```python
from solar_analysis.exceptions import DataValidationError

try:
    results = analyze_solar_upgrade('invalid_file.csv', 'another.csv')
except DataValidationError as e:
    print(f"Data validation failed: {e}")
    print(f"Error code: {e.error_code}")
    print(f"Suggested fix: {e.suggested_fix}")
```

#### `InsufficientDataError(SolarAnalysisError)`
**Purpose**: Raised when not enough data for statistical analysis

#### `CalculationError(SolarAnalysisError)`
**Purpose**: Raised when mathematical calculations fail

### Error Handling Patterns

#### Graceful Degradation
```python
try:
    # Attempt advanced statistical analysis
    result = calculate_with_confidence_intervals(data)
except InsufficientDataError:
    # Fall back to basic analysis
    result = calculate_basic_statistics(data)
    result['warning'] = "Limited data - using basic analysis"
```

#### Data Quality Warnings
```python
quality_check = assess_data_quality(df)

if quality_check['overall_score'] < 70:
    warnings.warn(
        f"Data quality score {quality_check['overall_score']} is below recommended threshold",
        category=DataQualityWarning
    )
```

---

## 📋 Configuration Options

### Analysis Configuration

```python
DEFAULT_CONFIG = {
    # Statistical settings
    'confidence_level': 0.95,
    'significance_threshold': 0.05,
    'min_data_points': 30,
    
    # Data quality settings
    'min_quality_score': 60,
    'outlier_detection': True,
    'gap_tolerance_hours': 6,
    
    # Seasonal adjustment
    'seasonal_adjustment': True,
    'region': 'south_africa',
    
    # Benchmarking
    'benchmark_comparison': True,
    'update_benchmarks': False,
    
    # Alerts
    'generate_alerts': True,
    'alert_threshold_std': 2.0,
    'underperformance_threshold': 0.7,
    
    # Financial analysis
    'electricity_rate_per_kwh': 1.50,
    'currency': 'ZAR',
    'discount_rate': 0.08,
    
    # Output options
    'include_raw_data': False,
    'generate_charts': True,
    'export_format': 'json'
}
```

### Chart Configuration

```python
CHART_CONFIG = {
    # Layout
    'width': 1200,
    'height': 800,
    'margin': {'l': 60, 'r': 60, 't': 80, 'b': 60},
    
    # Colors
    'legacy_color': '#ef4444',      # Red
    'new_color': '#10b981',         # Green
    'benchmark_color': '#f59e0b',   # Orange
    'confidence_alpha': 0.2,
    
    # Features
    'show_confidence_bands': True,
    'show_upgrade_line': True,
    'include_benchmarks': True,
    'interactive_tooltips': True,
    
    # Styling
    'theme': 'plotly_dark',
    'font_family': 'Inter',
    'background_color': 'rgba(0,0,0,0)'
}
```

---

## 🧪 Testing and Validation

### Unit Testing

```python
import pytest
from solar_analysis.core.statistical_engine import calculate_confidence_intervals

def test_confidence_intervals():
    """Test confidence interval calculation"""
    data = [10, 12, 11, 13, 9, 14, 10, 12]
    mean, lower, upper = calculate_confidence_intervals(data, 0.95)
    
    assert 10 < mean < 13
    assert lower < mean < upper
    assert (upper - lower) > 0

def test_empty_data_handling():
    """Test handling of empty datasets"""
    with pytest.raises(InsufficientDataError):
        calculate_confidence_intervals([])
```

### Integration Testing

```python
def test_end_to_end_analysis():
    """Test complete analysis pipeline"""
    
    # Create test data
    factory_df = create_test_factory_data()
    new_df = create_test_new_data()
    
    # Run analysis
    results = analyze_solar_upgrade_from_dataframes(
        factory_df, new_df, '2025-01-01', '2025-12-31'
    )
    
    # Validate results structure
    assert 'performance' in results
    assert 'financial' in results
    assert 'quality' in results
    assert isinstance(results['alerts'], list)
```

### Performance Benchmarks

```python
def benchmark_large_dataset():
    """Benchmark performance with large datasets"""
    import time
    
    large_df = generate_large_test_dataset(100000)  # 100k records
    
    start_time = time.time()
    results = analyze_system_performance(large_df)
    processing_time = time.time() - start_time
    
    assert processing_time < 10  # Should complete within 10 seconds
    assert results is not None
```

---

## 📊 Usage Examples

### Basic Analysis
```python
# Simple before/after comparison
from solar_analysis import analyze_solar_upgrade

results = analyze_solar_upgrade('before.csv', 'after.csv', '2025-01-01', '2025-12-31')
print(f"Improvement: {results['performance']['improvement_percent']:.1f}%")
```

### Advanced Analysis with Custom Configuration
```python
# Custom analysis configuration
config = {
    'confidence_level': 0.99,          # 99% confidence intervals
    'seasonal_adjustment': True,        # Weather normalization
    'benchmark_comparison': True,       # Industry comparison
    'generate_alerts': True,           # Performance monitoring
    'electricity_rate_per_kwh': 1.75   # Custom electricity rate
}

results = analyze_solar_upgrade('legacy.csv', 'new.csv', '2025-01-01', '2025-12-31', config)

# Access detailed results
performance = results['performance']
financial = results['financial']

print(f"Weather-normalized improvement: {performance['weather_normalized_improvement']:.1f}%")
print(f"ROI payback period: {financial['payback_years']:.1f} years")
```

### Real-time Monitoring
```python
# Monitor current system performance
from solar_analysis.utils.alert_system import detect_performance_anomalies

# Load recent data (last 24 hours)
recent_data = load_solar_data('current_system.csv')
recent_data = recent_data[recent_data['timestamp'] > datetime.now() - timedelta(days=1)]

# Detect issues
alerts = detect_performance_anomalies(recent_data, threshold_std=1.5)

if alerts:
    for alert in alerts:
        if alert['severity'] == 'HIGH':
            send_notification(alert['message'])
            print(f"🚨 {alert['message']}")
```

### Custom Visualization
```python
# Create custom charts
from solar_analysis.visualization.chart_generator import create_performance_dashboard

# Load and process data
system_data = load_and_process_solar_data('system.csv')

# Generate dashboard with custom styling
config = {
    'theme': 'plotly_white',
    'height': 600,
    'show_alerts': True,
    'include_benchmarks': True
}

dashboard = create_performance_dashboard(system_data, config=config)

# Export or display
dashboard.write_html('performance_dashboard.html')
```

---

## 🔗 Integration Examples

### Streamlit Integration
```python
import streamlit as st
from solar_analysis import analyze_solar_upgrade

# Streamlit app integration
st.title("Solar Performance Analysis")

# File uploads
factory_file = st.file_uploader("Upload legacy system data", type=['csv'])
new_file = st.file_uploader("Upload new system data", type=['csv'])

if factory_file and new_file:
    # Save uploaded files temporarily
    factory_path = save_uploaded_file(factory_file)
    new_path = save_uploaded_file(new_file)
    
    # Run analysis
    with st.spinner("Analyzing solar performance..."):
        results = analyze_solar_upgrade(factory_path, new_path)
    
    # Display results
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "Generation Improvement", 
            f"{results['performance']['improvement_percent']:.1f}%"
        )
    
    with col2:
        st.metric(
            "Annual Savings", 
            f"R{results['financial']['annual_savings']:,.0f}"
        )
    
    with col3:
        st.metric(
            "Data Quality", 
            results['quality']['overall_grade']
        )
```

### REST API Integration
```python
from flask import Flask, request, jsonify
from solar_analysis import analyze_solar_upgrade

app = Flask(__name__)

@app.route('/api/solar/analyze', methods=['POST'])
def api_analyze_solar():
    """REST API endpoint for solar analysis"""
    
    try:
        # Get parameters from request
        data = request.json
        factory_file = data['factory_file_path']
        new_file = data['new_file_path']
        start_date = data.get('start_date', '2025-01-01')
        end_date = data.get('end_date', '2025-12-31')
        
        # Run analysis
        results = analyze_solar_upgrade(factory_file, new_file, start_date, end_date)
        
        return jsonify({
            'status': 'success',
            'results': results
        })
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 400

if __name__ == '__main__':
    app.run(debug=True)
```

---

## 📈 Performance and Scaling

### Optimization Strategies

#### Data Processing Optimization
```python
# Use efficient data types
def optimize_dataframe(df):
    """Optimize DataFrame memory usage"""
    
    # Convert to appropriate dtypes
    df['state'] = pd.to_numeric(df['state'], downcast='float')
    df['last_changed'] = pd.to_datetime(df['last_changed'], infer_datetime_format=True)
    
    # Use categorical for entity_id if many repeats
    if df['entity_id'].nunique() < len(df) * 0.5:
        df['entity_id'] = df['entity_id'].astype('category')
    
    return df

# Chunked processing for large files
def process_large_dataset(file_path, chunk_size=10000):
    """Process large CSV files in chunks"""
    
    results = []
    for chunk in pd.read_csv(file_path, chunksize=chunk_size):
        chunk_result = process_data_chunk(chunk)
        results.append(chunk_result)
    
    return combine_results(results)
```

#### Caching Strategy
```python
import functools
import pickle
from datetime import datetime, timedelta

@functools.lru_cache(maxsize=128)
def cached_analysis(file_hash, start_date, end_date, config_hash):
    """Cache analysis results to avoid recomputation"""
    return expensive_analysis_function(file_hash, start_date, end_date, config_hash)

def get_file_hash(file_path):
    """Generate hash of file for caching"""
    import hashlib
    with open(file_path, 'rb') as f:
        return hashlib.md5(f.read()).hexdigest()
```

---

## 🔧 Development and Contributing

### Setting up Development Environment

```bash
# Clone repository
git clone https://github.com/Saint-Akim/DurrEnergy.git
cd DurrEnergyApp

# Create virtual environment
python -m venv solar_analysis_env
source solar_analysis_env/bin/activate  # Linux/Mac
# or
solar_analysis_env\Scripts\activate     # Windows

# Install development dependencies
pip install -r requirements-dev.txt

# Install in development mode
pip install -e .

# Run tests
pytest tests/ -v --cov=solar_analysis
```

### Code Style and Standards

```python
# Follow PEP 8 style guidelines
# Use type hints for function signatures

from typing import Dict, List, Tuple, Optional, Union
import pandas as pd

def analyze_performance(
    data: pd.DataFrame,
    start_date: str,
    end_date: str,
    config: Optional[Dict] = None
) -> Dict[str, Union[float, str, List]]:
    """
    Analyze solar system performance with proper type annotations.
    
    Args:
        data: Solar performance data
        start_date: Analysis start date in YYYY-MM-DD format
        end_date: Analysis end date in YYYY-MM-DD format  
        config: Optional configuration parameters
        
    Returns:
        Dictionary containing analysis results
        
    Raises:
        DataValidationError: If input data is invalid
        InsufficientDataError: If not enough data for analysis
    """
    pass
```

### Contributing Guidelines

1. **Fork the repository** and create a feature branch
2. **Write tests** for new functionality
3. **Update documentation** for API changes
4. **Follow code style** guidelines (PEP 8)
5. **Submit pull request** with clear description

---

## 📞 Support and Resources

### Getting Help

| Issue Type | Contact | Response Time |
|------------|---------|---------------|
| **Bug Reports** | github.com/Saint-Akim/DurrEnergy/issues | 2-3 business days |
| **Feature Requests** | product@durrenergy.com | 1 week |
| **API Questions** | developers@durrenergy.com | 1 business day |
| **Documentation** | docs@durrenergy.com | 2 business days |

### Additional Resources

- **GitHub Repository**: https://github.com/Saint-Akim/DurrEnergy
- **API Examples**: https://github.com/Saint-Akim/DurrEnergy/tree/main/examples
- **Tutorial Notebooks**: https://github.com/Saint-Akim/DurrEnergy/tree/main/tutorials
- **Performance Benchmarks**: https://github.com/Saint-Akim/DurrEnergy/wiki/Performance

---

**API Documentation Version**: 2.0  
**Last Updated**: December 2024  
**Next Review**: March 2025  
**Feedback**: api-feedback@durrenergy.com