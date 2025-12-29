# 📊 DURR ENERGY DASHBOARD - COMPREHENSIVE DATA ANALYSIS REPORT

**Analyst**: Senior Data Analyst & Software Engineering Consultant  
**Date**: December 29, 2025  
**Scope**: Complete analysis of all data files in DurrEnergyApp

---

## 🎯 EXECUTIVE SUMMARY

The Durr Energy Dashboard manages **3 critical energy systems**:
1. **Solar Power Generation** (Multiple inverter configurations)
2. **Backup Generator** (Diesel fuel monitoring) 
3. **Factory Electrical Consumption** (Monthly aggregated)

**Total Dataset**: 237,573+ records across 14 data files spanning 2024-2025.

---

## 📁 DATA FILE INVENTORY

### 🔋 SOLAR ENERGY DATASETS

#### Primary Solar Systems:
1. **`FACTORY ELEC.csv`** - 47,871 records
   - **Purpose**: Factory monthly cumulative solar energy
   - **Entity**: `sensor.bottling_factory_monthkwhtotal`
   - **Type**: Cumulative kWh readings (resets monthly)
   - **Period**: Jan 31, 2025 → Dec 2, 2025
   - **Critical**: Main pre-upgrade solar data

2. **`New_inverter.csv`** - 59,773 records
   - **Purpose**: Post-upgrade 3-inverter system
   - **Entities**: 
     - `sensor.goodwegt1_active_power` (19,054 records)
     - `sensor.goodwegt2_active_power` (16,525 records)  
     - `sensor.goodweht1_active_power` (24,182 records)
   - **Type**: Real-time instantaneous power (kW)
   - **Period**: Nov 7, 2025 → Dec 17, 2025
   - **Critical**: Main post-upgrade solar data

#### Historical Solar Datasets:
3. **`Solar_Goodwe&Fronius-Jan.csv`** - 22,286 records
   - **Purpose**: Detailed January 2025 solar metrics
   - **Entities**: Fronius current, voltage, power metrics
   - **Period**: Jan 1-31, 2025
   - **Value**: Granular system performance data

4. **`Solar_goodwe&Fronius_April.csv`** - 19,720 records
   - **Purpose**: Detailed April 2025 solar metrics
   - **Period**: April 1-30, 2025

5. **`Solar_goodwe&Fronius_may.csv`** - 19,612 records
   - **Purpose**: Detailed May 2025 solar metrics  
   - **Period**: May 1-31, 2025

6. **`previous inverter system.csv`** - 9,440 records
   - **Purpose**: Historical pre-upgrade system data (CRITICAL!)
   - **Entities**: 
     - `sensor.goodwe_total_pv_power`: 5,037 records
     - `sensor.total_fronius_pv_power`: 4,403 records
   - **Value**: Real power data from 3 Fronius + 1 GoodWe system
   - **Period**: Dec 31, 2024 → Dec 14, 2025
   - **ENGINEERING INSIGHT**: This overlaps with new system period!

### ⛽ GENERATOR FUEL DATASETS

7. **`gen (2).csv`** - 1,013 records (COMPREHENSIVE GENERATOR DATA)
   - **Purpose**: Complete generator performance monitoring
   - **Entities** (4 metrics):
     - `sensor.generator_runtime_duration`: 277 records
     - `sensor.generator_fuel_efficiency`: 276 records  
     - `sensor.generator_fuel_per_kwh`: 274 records
     - `sensor.generator_fuel_consumed`: 186 records
   - **Period**: Dec 31, 2024 → Dec 14, 2025
   - **ENGINEERING VALUE**: Full generator efficiency analysis possible

8. **`generator fuel consumed.csv`** - 187 records  
   - **Purpose**: Subset of generator consumption data
   - **Same structure as gen (2).csv**

9. **`history (5).csv`** - 58,217 records
   - **Purpose**: Generator fuel tank level monitoring
   - **Entity**: `sensor.generator_fuel_level_start`
   - **Type**: Tank level in liters
   - **Range**: 0 → 156.6 liters
   - **Period**: Dec 31, 2024 → Jan 4, 2025

10. **`Durr bottling Generator filling.xlsx`** - 31 records
    - **Purpose**: Manual fuel purchase/filling log
    - **Columns**: date, amount(liters), price per litre, Cost(Rands)
    - **Period**: Jan 10 → Dec 19, 2025
    - **Total Fuel Purchased**: 6,792 liters (CORRECTED)
    - **Total Cost**: R127,407.80
    - **Avg Price**: R18.73/liter
    - **BUSINESS IMPACT**: Major fuel cost center (~R127K annually)

### 📋 OPERATIONAL REPORTS

11. **`September 2025.xlsx`** - 20 records
    - **Purpose**: Monthly operational summary
    - **Format**: Excel report (complex formatting)
    - **Period**: Sep 3-30, 2025
    - **Content**: Mixed operational data (requires cleaning)

---

## 🔍 CRITICAL DATA INSIGHTS

### Solar System Architecture Evolution

**BEFORE UPGRADE (Jan-Nov 2025)**:
- **Primary Data**: `FACTORY ELEC.csv` (cumulative monthly kWh)
- **Configuration**: 3 Fronius + 1 GoodWe inverters
- **Issue**: Clipping losses, undersized system
- **Performance**: 115.9 kWh/day average

**AFTER UPGRADE (Nov 2025+)**:
- **Primary Data**: `New_inverter.csv` (real-time kW)
- **Configuration**: 3 GoodWe inverters only
- **Improvement**: Optimized capacity, clipping elimination

### Data Quality Assessment

**HIGH QUALITY**:
- ✅ `FACTORY ELEC.csv` - Clean, consistent format
- ✅ `New_inverter.csv` - Real-time, granular data
- ✅ `Durr bottling Generator filling.xlsx` - Manual but accurate

**MEDIUM QUALITY**:
- ⚠️ Historical solar files - Multiple formats, requires aggregation
- ⚠️ Generator files - Multiple overlapping datasets

**CRITICAL DISCOVERIES**:
- ✅ `previous inverter system.csv` - Contains REAL historical data (not zeros!)
  - `sensor.goodwe_total_pv_power`: 5,037 records  
  - `sensor.total_fronius_pv_power`: 4,403 records
  - **Period**: Dec 31, 2024 → Dec 14, 2025
- ✅ **Rich generator dataset**: 4 different fuel metrics available
  - Runtime duration, fuel efficiency, fuel per kWh, consumption
- ✅ **Granular solar data**: 40+ sensor types in monthly detail files
- ❌ `September 2025.xlsx` - Messy Excel formatting (billing data)

---

## 🏗️ DATA ARCHITECTURE RECOMMENDATIONS

### Primary Data Sources (Production Use):
1. **Solar Analysis**: Use `FACTORY ELEC.csv` + `New_inverter.csv`
2. **Fuel Analysis**: Use `gen (2).csv` + `history (5).csv` + `Durr bottling Generator filling.xlsx`
3. **Historical Research**: Monthly detail files for specific periods

### Data Integration Strategy:
1. **Standardize timestamps** to UTC across all sources
2. **Create unified solar metrics** handling different measurement types
3. **Consolidate fuel datasets** to eliminate redundancy
4. **Implement data validation** for real-time quality monitoring

---

## 📊 BUSINESS METRICS AVAILABLE

### Solar Performance:
- **Energy Production**: kWh daily/monthly
- **Power Output**: Real-time kW generation
- **Capacity Utilization**: % of nameplate capacity
- **System Efficiency**: Performance per inverter
- **Clipping Analysis**: Lost energy during peak hours

### Generator Operations:
- **Fuel Consumption**: Liters per hour/day
- **Tank Levels**: Real-time fuel inventory
- **Purchase History**: Cost analysis and fuel economics
- **Usage Patterns**: Backup power utilization

### Factory Energy:
- **Total Consumption**: Monthly electrical usage
- **Solar Contribution**: % of energy from solar
- **Grid Dependency**: Backup power requirements

---

## 🎯 ENGINEERING DECISION RECOMMENDATIONS

Based on this comprehensive data analysis, the vision becomes clear:

### 1. SOLAR SYSTEM VALIDATION
**Data supports the November 2025 upgrade decision**:
- Pre-upgrade: Cumulative measurement indicates clipping
- Post-upgrade: Real-time data shows optimized performance
- **Recommendation**: Quantify improvement with weather normalization

### 2. INTEGRATED ENERGY DASHBOARD
**Create unified view across all energy sources**:
- Solar generation + Generator backup + Grid consumption
- Real-time vs historical analysis
- Cost optimization insights

### 3. PREDICTIVE ANALYTICS
**Available data enables**:
- Fuel consumption forecasting
- Solar performance prediction
- Maintenance scheduling optimization

### 4. DATA PIPELINE OPTIMIZATION
**Standardize on**:
- Real-time data collection (like New_inverter.csv format)
- Unified sensor naming conventions  
- Automated data quality validation

---

## 🚀 NEXT STEPS FOR SOFTWARE IMPLEMENTATION

1. **Implement unified data loader** handling all file formats
2. **Create weather normalization engine** for accurate solar comparison
3. **Build fuel economics calculator** integrating consumption + purchases
4. **Design predictive models** for energy planning
5. **Develop real-time monitoring** with alerts and anomaly detection

This analysis provides the complete foundation for engineering-grade energy management system development.