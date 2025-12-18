# Durr Bottling Energy Intelligence Dashboard
## Technical Architecture & Implementation Guide

### 🎯 Purpose
Production-grade analytics platform for:
- Generator fuel usage & cost tracking
- Solar performance monitoring (3-inverter system)
- Factory electrical consumption analysis
- Automated billing invoice generation

### 📊 Data Flow Architecture
```
GitHub Raw Files → Data Fetch Layer → Normalization → Calculation Engine → Streamlit UI
```

### 🔧 Core Algorithms

#### Generator Fuel Calculation (Critical)
**Dual-Source Approach:**
1. **Primary**: `sensor.generator_fuel_consumed` (cumulative) → positive diffs → daily sum
2. **Backup**: `sensor.generator_fuel_level` (tank level) → smoothed drops → daily sum
3. **Smart Fusion**: Use primary preferentially, backup fills gaps

**Why Dual-Source:**
- Handles sensor failures/gaps
- Cross-validates consumption data
- Eliminates under-counting

#### Real Pricing Integration
- Forward-fill from purchase dates (nearest-prior per day)
- Fallback to monthly average if preferred
- No estimations - uses actual paid prices

#### Solar Processing
- Combines GoodWe + Fronius inverters
- Positive values only (filters noise)
- Proper kW scaling (values already in kW)
- Daily/hourly aggregations

#### Factory Consumption
- Handles meter resets (detects >1000 kWh drops)
- Segments data between resets
- Calculates daily consumption within segments

### 📁 File Structure & Purpose
```
gen (2).xlsx           → Primary generator cumulative data
history (5).xlsx       → High-frequency tank level backup
Durr bottling Generator filling.xlsx → Real fuel purchase prices
New_inverter.csv       → Solar 3-inverter system data
FACTORY ELEC.csv       → Factory cumulative kWh meter
September 2025.xlsx    → Editable billing template
```

### 🚀 Deployment & Caching
- **Platform**: Streamlit Cloud
- **Caching**: `@st.cache_data(ttl=600)` for GitHub data
- **Requirements**: Pinned for reproducibility
- **Error Handling**: Graceful degradation, no silent failures

### ✅ Validation Checklist
- [ ] Generator totals realistic (not 50k+ liters)
- [ ] Costs use real purchase prices (R18-20/L range)
- [ ] Solar shows meaningful kW generation
- [ ] Factory daily kWh reasonable (<500/day)
- [ ] No duplicate element ID errors
- [ ] No raw HTML tags visible
- [ ] Charts interactive (zoom, selection)

### 🔒 Developer Guidelines
**Never:**
- Estimate fuel from runtime alone
- Drop zero-usage days
- Use generic pricing
- Ignore timezone safety

**Always:**
- Cross-validate calculations
- Preserve audit trail
- Handle meter resets
- Maintain cumulative→delta logic

### 📈 Future Roadmap
**Phase 2:** Alerts, PDF exports, advanced analytics
**Phase 3:** Multi-site, AI insights, predictive modeling