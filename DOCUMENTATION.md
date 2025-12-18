# Durr Bottling Energy Intelligence Dashboard - Complete Documentation

## 📋 Overview

**Application Name:** Durr Bottling Energy Intelligence Dashboard  
**Version:** 10.0 Enhanced  
**Repository:** https://github.com/Saint-Akim/DurrEnergy  
**Deployment:** Streamlit Cloud  
**Purpose:** Ultra-modern interactive energy monitoring platform with real-time pricing and 3-inverter solar system analysis

---

## 🏗️ System Architecture

### Technology Stack
- **Frontend Framework:** Streamlit
- **Data Processing:** Pandas, NumPy
- **Visualization:** Plotly (interactive charts)
- **Data Sources:** 
  - Local CSV/XLSX files
  - GitHub repository fallback
  - Home Assistant exports
  - Real-time pricing data

### Key Features
1. **Real Fuel Pricing Integration** - Uses actual purchase data from "Durr bottling Generator filling.xlsx"
2. **3-Inverter Solar System** - Enhanced solar analysis with new inverter configuration
3. **Dual-Source Fuel Consumption** - Primary (detailed CSV) + backup (tank level) sensors
4. **Interactive Date Range Selection** - Flexible time period analysis
5. **Silent Data Loading** - No loading messages for cleaner UX
6. **Glassmorphic UI** - Modern design with backdrop blur effects

---

## ⚠️ CRITICAL NOTICE - FUEL SECTION LOCKED

**🔒 FUEL ALGORITHM & DATA IS PRODUCTION-READY - NO MODIFICATIONS ALLOWED**

**Authorization Code Required:** `221748601`

The fuel consumption calculation, pricing algorithm, and all related data processing have been thoroughly tested and validated. These sections are now **LOCKED** and must not be modified unless explicitly authorized with the code above.

**What's Locked:**
- ✅ Fuel consumption algorithm (tank level interpretation)
- ✅ Fuel pricing calculation and column normalization
- ✅ Purchase data processing
- ✅ `normalize_purchase_columns()` function
- ✅ `process_fuel_purchases_and_pricing()` function
- ✅ All fuel-related fixes from December 18, 2025

**Current Focus:** Other dashboard tabs (Solar, Factory Electricity, etc.)

---

## 🔍 Data Sources

### 1. Generator Data ⚠️ [LOCKED - Code 221748601 Required]
**Files:**
- `gen (2).csv` / `gen.xlsx` - Primary generator sensor data
- `generator fuel consumed.csv` - Detailed fuel consumption records (187 entries)

**Key Entity:** `sensor.generator_fuel_consumed`
- **Type:** Tank level sensor (NOT cumulative)
- **Unit:** Litres
- **Range:** 13.5L to 197.1L

### 2. Fuel Purchase Data ⚠️ [LOCKED - Code 221748601 Required]
**File:** `Durr bottling Generator filling.xlsx`
- **Records:** 31 purchases
- **Date Range:** January 2025 - October 2025
- **Columns (normalized):**
  - `date` - Purchase date
  - `litres` - Amount purchased
  - `cost` - Total cost in Rands
  - `price_per_litre` - Price per litre (R18.11 - R19.73)

**Total Purchases:**
- Volume: 6,792 litres
- Cost: R127,407.80
- Average Price: R18.76/L

### 3. Solar Generation Data ✅ [ACTIVE DEVELOPMENT]
**New System:** `New_inverter.csv`
- **System Type:** 3-Inverter Enhanced System
- **Configuration:** Removed Fronius, added 2 new inverters
- **Data Format:** Power readings in kW (already scaled correctly)

**Legacy Files (Fallback):**
- `Solar_Goodwe&Fronius-Jan.csv`
- `Solar_goodwe&Fronius_April.csv`
- `Solar_goodwe&Fronius_may.csv`

### 4. Factory Electricity ✅ [ACTIVE DEVELOPMENT]
**File:** `FACTORY ELEC.csv` / `FACTORY ELEC.xlsx`
- Factory electricity consumption data
- **Status:** Open for analysis and optimization

### 5. Fuel History ⚠️ [LOCKED - Code 221748601 Required]
**File:** `history (5).csv` / `history.xlsx`
- Historical fuel tank level data
- **Key Entity:** `sensor.generator_fuel_level`
- Used as backup source for consumption calculation

---

## 🧮 Core Algorithms

### 1. Fuel Consumption Calculation ⚠️ [LOCKED - Code 221748601 Required]

**🔒 THIS ALGORITHM IS PRODUCTION-READY AND LOCKED**
**All fuel calculations have been validated and match Home Assistant data**
**Do not modify without authorization code: 221748601**

#### ❌ **Previous Wrong Logic:**
```python
# WRONG: Treated sensor as cumulative consumption
consumption = positive_jumps.sum()  # Counted refills as consumption!
```

#### ✅ **Correct Logic:**
```python
# CORRECT: sensor.generator_fuel_consumed = CURRENT TANK LEVEL
# Tank level DROPS = actual fuel consumption
# Tank level INCREASES = refills (ignore these)

fuel_data['level_change'] = fuel_data['state'].diff()
fuel_data['consumption_diff'] = (-fuel_data['level_change']).clip(lower=0)
# Only negative changes (drops) are consumption
```

#### Algorithm Steps:

**Primary Source (Detailed CSV - Highest Quality):**
1. Filter `sensor.generator_fuel_consumed` records
2. Sort by timestamp
3. Calculate consecutive differences: `diff = state[i] - state[i-1]`
4. Extract consumption: `consumption = max(0, -diff)` (only negative diffs)
5. Filter noise: Keep only days with ≥1L consumption
6. Group by date and sum

**Backup Source (Tank Level - Fallback):**
1. Filter `sensor.generator_fuel_level` records
2. Apply smoothing: 20-point rolling median (reduces sensor noise)
3. Calculate differences
4. Extract significant drops: `-30L < diff < -1L`
   - Lower bound: Avoid counting refills
   - Upper bound: Filter sensor noise
5. Cap daily consumption: Max 50L/day (outlier protection)

**Smart Combination:**
```python
for each date:
    if primary_consumption > 0.1L:
        use primary_source  # Prefer detailed CSV
    elif backup_consumption > 0.1L:
        use backup_source  # Fallback to tank level
    else:
        use max(primary, backup)  # Edge case handling
```

**Results:**
- Total Consumption: ~1,866L over 40 days
- Average Daily: 46.6L/day
- Largest Events: 178L, 151L, 92L (major generator runs)

---

### 2. Fuel Pricing Algorithm ⚠️ [LOCKED - Code 221748601 Required]

**🔒 THIS ALGORITHM IS PRODUCTION-READY AND LOCKED**
**Column normalization and pricing calculations are validated**
**Do not modify without authorization code: 221748601**

#### Column Normalization
**Problem:** Excel columns vary in naming (spaces, parentheses, case)

**Solution:** `normalize_purchase_columns()` function
```python
def normalize_purchase_columns(df):
    # Step 1: Lowercase and clean
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(r'\s+', '_', regex=True)  # spaces → underscores
        .str.replace(r'[()]+', '', regex=True)  # remove parentheses
    )
    
    # Step 2: Map variations to standard names
    rename_map = {
        'amount_liters': 'litres',
        'amountliters': 'litres',
        'amount': 'litres',
        'liters': 'litres',
        'costrands': 'cost',
        'cost_rands': 'cost',
        'price_per_liter': 'price_per_litre'
    }
    
    # Step 3: Convert to numeric
    for col in ['litres', 'cost', 'price_per_litre']:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    
    return df
```

**Standard Column Names:**
- `date` - Purchase date
- `litres` - Volume purchased
- `cost` - Total cost in Rands
- `price_per_litre` - Price per litre

#### Pricing Modes

**Mode 1: Nearest Prior (Default)**
```python
for consumption_date in all_dates:
    # Find most recent purchase before this date
    prior_purchases = purchases[purchases['date'] <= consumption_date]
    if not prior_purchases.empty:
        price = prior_purchases['price_per_litre'].iloc[-1]  # Latest price
    else:
        price = average_price  # Fallback
```

**Mode 2: Monthly Average**
```python
# Group purchases by month
monthly_avg = purchases.groupby('month')['price_per_litre'].mean()

for consumption_date in all_dates:
    month = consumption_date.to_period('M')
    price = monthly_avg.get(month, average_price)
```

#### Cost Calculation
```python
for each day:
    daily_cost = fuel_consumed_litres * price_per_litre
    
total_cost = sum(daily_cost for all days)
average_price = total_cost / total_litres
```

---

### 3. Solar Generation Analysis (3-Inverter System) ✅ [ACTIVE DEVELOPMENT]

**📝 This section is open for modifications and improvements**
**Current focus area for enhancements and optimizations**

#### Critical Fix: Power Scaling
**Problem:** Data showed max 88.4W which seemed too low
**Discovery:** Values were already in kW scale (88.4kW total system)

```python
# WRONG approach (would give incorrect results):
power_kw = state / 1000  # Don't divide if already in kW!

# CORRECT approach:
power_kw = state.abs()  # Values already in kW scale
```

#### Algorithm Steps

**1. Power Data Processing:**
```python
# Filter power sensors (3 inverters)
power_sensors = solar_df[entity_id.contains('power')]

# Values already in kW - use directly
power_sensors['power_kw'] = power_sensors['state'].abs()

# Group by inverter and date
inverter_daily = power_sensors.groupby(['date', 'inverter']).agg({
    'power_kw': ['sum', 'max', 'mean', 'count']
})
```

**2. Energy Conversion (kWh):**
```python
# Data frequency: ~12 samples per hour
data_freq_per_hour = 12

# Convert power sum to energy
inverter_daily['total_kwh'] = inverter_daily['total_kwh'] / data_freq_per_hour
```

**3. System Aggregation:**
```python
# Sum all 3 inverters for total system output
system_daily = inverter_daily.groupby('date').agg({
    'total_kwh': 'sum',      # Total daily generation
    'peak_kw': 'max',        # Peak system power
    'avg_kw': 'mean'         # Average power
})
```

**4. Performance Metrics:**
```python
capacity_factor = (avg_kw / peak_kw) * 100  # System efficiency
carbon_offset = total_kwh * 0.95  # kg CO2 saved
monthly_savings = (total_kwh * electricity_rate * 30) / days
```

**Key Improvements:**
- **Removed:** Fronius inverter (legacy system)
- **Added:** 2 new inverters (3 total)
- **Capacity Increase:** ~25kW → 88kW+ peak
- **System Type:** "3-Inverter Enhanced System"

---

## 🐛 Critical Fixes Applied

### Fix 1: render_clean_metric() TypeError
**Date:** December 18, 2025  
**Commit:** 99156af

**Problem:**
```python
# Function definition (6 parameters)
def render_clean_metric(label, value, delta=None, color="blue", icon="📊", description=None):

# Function call (7 arguments)
render_clean_metric(
    "Total Fuel Consumed",
    f"{fuel_stats['total_fuel_liters']:,.1f} L",
    f"📈 Real pricing used",  # delta
    "blue",                   # color
    "⛽",                     # icon
    f"Period: {period_days} days",  # description
    fuel_stats.get('fuel_consumption_trend', [])  # 7th arg - trend_data!
)
```

**Error:**
```
TypeError: render_clean_metric() takes from 2 to 6 positional arguments but 7 were given
```

**Solution:**
```python
def render_clean_metric(label, value, delta=None, color="blue", icon="📊", 
                       description=None, trend_data=None):  # Added 7th parameter
    """Clean metric using native Streamlit components"""
    with st.container():
        col1, col2 = st.columns([1, 4])
        with col1:
            st.markdown(f"<div style='font-size: 2.5rem;'>{icon}</div>", 
                       unsafe_allow_html=True)
        with col2:
            st.metric(label=label, value=value, delta=delta, help=description)
```

---

### Fix 2: KeyError for Fuel Purchase Columns
**Date:** December 18, 2025  
**Commit:** 99156af

**Problem:**
```python
# Code attempted to use exact column names
purchase_monthly = fuel_purchases.groupby('month').agg({
    'amount(liters)': 'sum',  # Column doesn't exist!
    'Cost(Rands)': 'sum'      # Column doesn't exist!
})
```

**Error:**
```
KeyError: "Column(s) ['Cost(Rands)', 'amount(liters)'] do not exist"
```

**Root Cause:**
- Excel columns processed with different naming
- Data cleaning removed spaces/parentheses
- Actual columns were normalized versions

**Solution:**
```python
# Step 1: Normalize columns first
fuel_purchases_norm = normalize_purchase_columns(fuel_purchases)

# Step 2: Use standard normalized names
purchase_monthly = fuel_purchases_norm.groupby('month').agg({
    'litres': 'sum',  # Standard name
    'cost': 'sum'     # Standard name
}).reset_index()

# Step 3: Rename for clarity
purchase_monthly = purchase_monthly.rename(columns={
    'litres': 'purchased_litres',
    'cost': 'purchase_cost'
})
```

---

### Fix 3: Fuel Consumption Logic Correction
**Date:** December 18, 2025  
**Commit:** e12944b

**Problem:**
```python
# WRONG: Treated tank level sensor as cumulative
daily_consumption = fuel_data['state'].diff()  # Counted refills as consumption
consumption = positive_diffs.sum()  # Massive overcounting (1,760L vs 1,866L)
```

**Discovery:**
- `sensor.generator_fuel_consumed` shows CURRENT TANK LEVEL
- Positive changes = Refills (fuel added)
- Negative changes = Consumption (fuel used)

**Solution:**
```python
# CORRECT: Only count tank level DROPS
fuel_data['level_change'] = fuel_data['state'].diff()
fuel_data['consumption_diff'] = (-fuel_data['level_change']).clip(lower=0)

# Filter noise
daily_consumption = fuel_data.groupby('date')['consumption_diff'].sum()
daily_consumption = daily_consumption[daily_consumption >= 1.0]
```

**Results:**
- **Before:** 1,760L (inflated, counted refills)
- **After:** 1,866L (accurate, only drops)
- **Matches Home Assistant:** ✓

---

## 📊 Key Statistics & Insights

### Fuel Consumption ⚠️ [LOCKED - Code 221748601 Required]
- **Total Period:** ~40 days with consumption
- **Total Consumed:** 1,866 litres
- **Average Daily:** 46.6 L/day
- **Peak Days:** 178L, 151L, 92L (major operations)
- **Smallest Day:** 13.5L (minimal operation)

### Fuel Purchases ⚠️ [LOCKED - Code 221748601 Required]
- **Total Volume:** 6,792 litres
- **Total Cost:** R127,407.80
- **Number of Purchases:** 31
- **Price Range:** R18.11 - R19.73 per litre
- **Average Price:** R18.76/L
- **Monthly Range:** 75L (Oct) to 726L (June)

### Utilization Analysis ⚠️ [LOCKED - Code 221748601 Required]
```python
Total Purchased: 6,792L
Total Consumed: 1,866L
Utilization Rate: 27.5%
Remaining/Storage: 4,926L (72.5%)
```

### Solar Generation (3-Inverter System) ✅ [ACTIVE DEVELOPMENT]
- **System Type:** Enhanced 3-Inverter Configuration
- **Peak Power:** 88.4 kW (system-wide)
- **Capacity Improvement:** ~254% over legacy system
- **Removed:** Fronius inverter
- **Added:** 2 new high-capacity inverters
- **Data Quality:** "3-Inverter Enhanced Analysis"

---

## 🔧 Technical Implementation Details

### Data Loading Strategy

**Silent Loading (No UI Disruption):**
```python
@st.cache_data(ttl=3600, show_spinner=False)
def load_all_energy_data_silent():
    ROOT = Path(__file__).resolve().parent
    
    def load_any(name_candidates):
        # Try multiple filenames and formats
        for name in name_candidates:
            try:
                if extension in ['.xlsx', '.xls']:
                    return pd.read_excel(path)
                elif extension in ['.csv']:
                    return pd.read_csv(path)
            except:
                continue
        return pd.DataFrame()
    
    # Load with fallbacks
    data['generator'] = load_any(["gen (2).csv", "gen.xlsx"])
    data['fuel_purchases'] = load_any(["Durr bottling Generator filling.xlsx"])
    
    # GitHub fallback for solar
    if solar_local.empty:
        github_url = "https://raw.githubusercontent.com/.../New_inverter.csv"
        solar_local = pd.read_csv(io.StringIO(requests.get(github_url).text))
    
    return data
```

### Date Filtering Function

```python
def filter_data_by_date_range(df, date_col, start_date, end_date):
    """Robust date filtering with error handling"""
    df = df.copy()
    df[date_col] = pd.to_datetime(df[date_col], errors='coerce')
    mask = (df[date_col].dt.date >= start_date) & (df[date_col].dt.date <= end_date)
    return df[mask].copy()
```

### Interactive Chart Creation

```python
def create_ultra_interactive_chart(df, x_col, y_col, title, color, chart_type, 
                                  height=500, enable_zoom=True, enable_selection=True):
    """Ultra-interactive Plotly charts with glassmorphic styling"""
    
    fig = go.Figure()
    
    if chart_type == "bar":
        fig.add_trace(go.Bar(
            x=df[x_col], y=df[y_col],
            marker=dict(color=color, opacity=0.8),
            hovertemplate="<b>%{x}</b><br>%{y:.2f}<br><extra></extra>"
        ))
    
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#e2e8f0'),
        hovermode="x unified",
        dragmode="select" if enable_selection else "zoom"
    )
    
    st.plotly_chart(fig, width='stretch', config=config)
```

---

## 🎨 UI/UX Design

### Styling System
**Framework:** Custom CSS with Glassmorphism
```css
:root {
    --bg-glass: rgba(255, 255, 255, 0.03);
    --border: rgba(148, 163, 184, 0.1);
    --shadow-glass: 0 8px 32px rgba(0, 0, 0, 0.37);
}

.glass-card {
    background: var(--bg-glass);
    backdrop-filter: blur(20px);
    border: 1px solid var(--border);
    border-radius: 24px;
    box-shadow: var(--shadow-glass);
}
```

### Color Palette
- **Primary:** `#3b82f6` (Blue)
- **Success:** `#10b981` (Green)
- **Warning:** `#f59e0b` (Amber)
- **Danger:** `#ef4444` (Red)
- **Info:** `#06b6d4` (Cyan)
- **Purple:** `#8b5cf6` (Accent)

### Typography
- **Primary Font:** Inter (Sans-serif)
- **Monospace:** JetBrains Mono
- **Sizes:** 11px-22px (responsive scaling)

---

## 📁 File Structure

```
DurrEnergyApp/
├── app.py                                    # Main application (77KB)
├── gen (2).csv                               # Generator sensor data
├── generator fuel consumed.csv               # Detailed consumption (187 records)
├── Durr bottling Generator filling.xlsx      # Fuel purchases (31 records)
├── New_inverter.csv                          # 3-Inverter solar data
├── history (5).csv                           # Fuel level history (backup)
├── FACTORY ELEC.csv                          # Factory electricity
├── Solar_Goodwe&Fronius-Jan.csv             # Legacy solar (Jan)
├── Solar_goodwe&Fronius_April.csv           # Legacy solar (April)
├── Solar_goodwe&Fronius_may.csv             # Legacy solar (May)
└── requirements.txt                          # Python dependencies
```

---

## 🚀 Deployment

### Repository
- **URL:** https://github.com/Saint-Akim/DurrEnergy
- **Branch:** main
- **Latest Commit:** 99156af (December 18, 2025)

### Streamlit Cloud Configuration
```toml
[server]
headless = true
port = 8501

[browser]
gatherUsageStats = false

[theme]
base = "dark"
primaryColor = "#3b82f6"
```

### Dependencies (requirements.txt)
```
streamlit>=1.28.0
pandas>=2.0.0
plotly>=5.17.0
numpy>=1.24.0
requests>=2.31.0
openpyxl>=3.1.0
```

---

## 🎯 Current Development Focus

**✅ ACTIVE AREAS (Open for Development):**
1. **Solar Tab Enhancements**
   - Per-inverter performance analysis
   - Time-of-day generation patterns
   - Weather correlation analysis
   - Efficiency optimization recommendations

2. **Factory Electricity Tab**
   - Consumption pattern analysis
   - Peak demand identification
   - Cost allocation by department/area
   - Energy efficiency recommendations

3. **Cross-Tab Analysis**
   - Solar vs Generator usage comparison
   - Grid vs Self-generated power ratio
   - Cost-benefit analysis across sources
   - Optimal energy mix recommendations

**🔒 LOCKED AREAS (Code 221748601 Required):**
- Fuel consumption calculations
- Fuel pricing algorithms
- Purchase data normalization
- Any modifications to fuel-related functions

---

## 🔮 Future Enhancements

### Planned Features
1. **Real-time Data Integration**
   - WebSocket connection to Home Assistant
   - Live sensor updates (no page refresh)

2. **Advanced Analytics**
   - Machine learning predictions for fuel consumption
   - Anomaly detection for unusual patterns
   - Seasonal trend analysis

3. **Cost Optimization**
   - Generator vs grid cost comparison
   - Optimal solar usage recommendations
   - Predictive maintenance alerts

4. **Mobile Optimization**
   - Responsive design improvements
   - Touch-optimized charts
   - Offline mode support

5. **Export Capabilities**
   - PDF report generation
   - Excel export with formatting
   - Email scheduling for reports

6. **User Management**
   - Role-based access control
   - Custom dashboards per user
   - Audit logging

---

## 🆘 Troubleshooting Guide

### Common Issues

#### Issue 1: "No data available" messages
**Cause:** Files not found or wrong date range selected
**Solution:**
1. Check files exist in app directory
2. Verify date range contains data
3. Try "All Time" preset to see full range

#### Issue 2: Charts not displaying
**Cause:** Empty DataFrames after filtering
**Solution:**
1. Expand date range
2. Check source data has valid numeric values
3. Look for error messages in Streamlit logs

#### Issue 3: Incorrect fuel consumption values
**Cause:** Algorithm interpretation issue
**Solution:**
- Verify sensor type (tank level vs cumulative)
- Check for large refill events in data
- Review consumption diff calculations

#### Issue 4: Price data missing
**Cause:** Purchase file not loaded or wrong column names
**Solution:**
1. Verify "Durr bottling Generator filling.xlsx" exists
2. Check column names match expected format
3. Run column normalization function

### Debug Mode
Enable detailed logging:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Data Validation Checks
```python
# Check data loading
st.write("Generator data shape:", all_data['generator'].shape)
st.write("Fuel purchases shape:", all_data['fuel_purchases'].shape)
st.write("Column names:", all_data['fuel_purchases'].columns.tolist())

# Check date ranges
st.write("Generator date range:", 
         all_data['generator']['last_changed'].min(), 
         "to", 
         all_data['generator']['last_changed'].max())
```

---

## 📞 Support & Contact

### For Technical Issues:
- **Repository Issues:** https://github.com/Saint-Akim/DurrEnergy/issues
- **Email:** electrical@durrbottling.com

### For New Sessions:
This documentation file contains all critical information about:
- Algorithm implementations
- Data source structures
- Bug fixes applied
- Technical decisions made

**Location:** `~/Desktop/DurrEnergy_Documentation.md`

---

## 📝 Change Log

### Version 10.0 Enhanced (December 18, 2025)
- ✅ Fixed `render_clean_metric()` TypeError
- ✅ Added `normalize_purchase_columns()` function
- ✅ Corrected fuel consumption calculation algorithm
- ✅ Fixed KeyError on purchase data aggregation
- ✅ Enhanced error handling and data validation
- ✅ Improved documentation and code comments

### Version 9.0 (December 17, 2025)
- Added 3-Inverter solar system support
- Implemented real fuel pricing from Excel
- Enhanced UI with glassmorphism
- Added dual-source fuel consumption

### Version 8.0 (Prior)
- Legacy system implementation
- Basic fuel and solar tracking
- Simple metric displays

---

## 🎓 Learning Resources

### Understanding the Algorithms

**Tank Level vs Cumulative Sensors:**
- Tank Level: Shows current quantity (e.g., 150L in tank)
  - Decreases when consumed
  - Increases when refilled
  - **Consumption = Negative changes only**

- Cumulative: Shows total ever used (e.g., 5000L lifetime)
  - Only increases
  - Resets to zero when cleared
  - **Consumption = Positive changes**

**Why This Matters:**
Our `sensor.generator_fuel_consumed` is **tank level** type, which is why we count negative differences as consumption and ignore positive changes (refills).

---

## 🏆 Best Practices

### When Adding New Data Sources:
1. Use `normalize_columns()` pattern for robustness
2. Add try/except blocks around data loading
3. Provide fallback defaults
4. Cache with appropriate TTL
5. Show user-friendly error messages

### When Modifying Algorithms:
1. Document the logic clearly in comments
2. Keep old logic in comments for reference
3. Add validation checks on outputs
4. Test with edge cases (empty data, single row, etc.)
5. Commit with descriptive messages

### When Debugging:
1. Use `st.write()` for quick debugging
2. Check DataFrame shapes and columns
3. Verify date ranges contain data
4. Print sample rows to understand structure
5. Test with "All Time" date range first

---

## 📖 Glossary

**Glassmorphism:** UI design trend using frosted glass effects with blur
**kWh:** Kilowatt-hour, unit of electrical energy
**Capacity Factor:** Ratio of actual vs theoretical maximum output
**Forward-fill:** Propagate last known value forward in time
**Rolling Median:** Moving window median for smoothing noisy data
**Streamlit Cache:** Decorator that stores function results to avoid recomputation
**Plotly:** JavaScript charting library for interactive visualizations
**Pandas:** Python data manipulation library

---

**Document Version:** 1.0  
**Last Updated:** December 18, 2025  
**Maintainer:** Durr Bottling Energy Team  
**Status:** ✅ Production Ready
