"""
User-Friendly Helper Functions
===============================
Simple, non-technical language and helpful explanations for all users
"""

import streamlit as st

# ==============================================================================
# FRIENDLY EXPLANATIONS
# ==============================================================================

FRIENDLY_EXPLANATIONS = {
    # Generator/Fuel
    "fuel_consumed": "💡 This shows how much diesel fuel the generator used",
    "fuel_cost": "💡 This is how much money was spent on diesel fuel",
    "daily_average": "💡 This is the typical amount of fuel used each day",
    "price_per_liter": "💡 This is the cost of diesel fuel per liter (like the price at a petrol station)",
    
    # Solar
    "solar_generation": "💡 This shows how much electricity the solar panels produced",
    "solar_savings": "💡 This is how much money you saved by using solar power instead of buying electricity",
    "peak_power": "💡 This is the highest amount of power the solar panels produced at one time",
    "daily_solar": "💡 This is how much solar electricity was generated each day",
    
    # Factory
    "factory_consumption": "💡 This shows how much electricity the factory used",
    "electricity_cost": "💡 This is how much the factory's electricity cost",
    
    # General
    "date_range": "💡 Choose which dates you want to see information for",
    "trend": "💡 This shows whether the numbers are going up ↗️ or down ↘️",
    "comparison": "💡 This compares different time periods to see what changed",
}

SIMPLE_UNITS = {
    "L": "Liters (like bottles of water)",
    "kWh": "Kilowatt-hours (units of electricity)",
    "kW": "Kilowatts (power level)",
    "R": "Rands (South African money)",
    "kg": "Kilograms (weight)",
    "days": "Days",
    "%": "Percent (out of 100)",
}

# ==============================================================================
# HELPER TOOLTIPS
# ==============================================================================

def get_tooltip(key):
    """Get a user-friendly tooltip for any metric"""
    return FRIENDLY_EXPLANATIONS.get(key, "")

def format_unit_friendly(unit):
    """Convert technical units to friendly descriptions"""
    return SIMPLE_UNITS.get(unit, unit)

def render_help_icon(help_text):
    """Render a small help icon with tooltip"""
    st.markdown(f"""
        <span style="cursor: help; color: #3b82f6; margin-left: 5px;" 
              title="{help_text}">ℹ️</span>
    """, unsafe_allow_html=True)

# ==============================================================================
# FRIENDLY SECTION HEADERS
# ==============================================================================

def render_friendly_section(title, icon, explanation):
    """Render a section header with simple explanation"""
    st.markdown(f"""
        <div style="
            background: rgba(59, 130, 246, 0.1);
            border-left: 4px solid #3b82f6;
            border-radius: 12px;
            padding: 20px;
            margin: 24px 0 16px 0;
        ">
            <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 8px;">
                <span style="font-size: 1.8rem;">{icon}</span>
                <span style="font-size: 1.3rem; font-weight: 700; color: #f1f5f9;">{title}</span>
            </div>
            <div style="color: #cbd5e1; font-size: 1rem; line-height: 1.6; margin-left: 48px;">
                {explanation}
            </div>
        </div>
    """, unsafe_allow_html=True)

# ==============================================================================
# FRIENDLY METRIC DISPLAY
# ==============================================================================

def render_friendly_metric(label, value, explanation, icon="📊", delta=None, good_change=True):
    """Render a metric with simple explanation"""
    
    # Format delta with friendly indicator
    delta_html = ""
    if delta:
        if good_change:
            emoji = "📈" if "+" in str(delta) else "📉"
            color = "#10b981" if "+" in str(delta) else "#ef4444"
        else:
            emoji = "📉" if "+" in str(delta) else "📈"
            color = "#ef4444" if "+" in str(delta) else "#10b981"
        
        delta_html = f"""
            <div style="color: {color}; font-size: 0.95rem; font-weight: 600; margin-top: 8px;">
                {emoji} {delta}
            </div>
        """
    
    st.markdown(f"""
        <div style="
            background: var(--bg-glass-strong);
            border: 1px solid var(--border);
            border-radius: 16px;
            padding: 20px;
            margin-bottom: 16px;
        ">
            <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 10px;">
                <span style="font-size: 1.8rem;">{icon}</span>
                <span style="color: #94a3b8; font-size: 0.9rem; font-weight: 600;">
                    {label}
                </span>
            </div>
            <div style="font-size: 2rem; font-weight: 700; color: #f1f5f9; margin-bottom: 8px;">
                {value}
            </div>
            <div style="color: #94a3b8; font-size: 0.85rem; font-style: italic;">
                {explanation}
            </div>
            {delta_html}
        </div>
    """, unsafe_allow_html=True)

# ==============================================================================
# FRIENDLY MESSAGES
# ==============================================================================

FRIENDLY_MESSAGES = {
    "welcome": """
        👋 **Welcome!** This dashboard helps you understand your energy usage in simple terms.
        
        You can see:
        - 🔥 How much diesel fuel your generator uses
        - ☀️ How much electricity your solar panels generate
        - ⚡ How much electricity your factory consumes
        - 💰 How much money you spend and save
    """,
    
    "no_data": """
        📭 **No data available yet**
        
        There's no data to show for the dates you selected. Try:
        - Choosing different dates
        - Checking if the data files are up to date
    """,
    
    "data_loading": """
        ⏳ **Loading your data...**
        
        Please wait while we gather all the information about your energy usage.
    """,
    
    "good_performance": """
        ✅ **Great job!** Your energy usage is looking good.
        
        Keep up the good work!
    """,
    
    "needs_attention": """
        ⚠️ **Heads up!** There might be something to check.
        
        Take a look at the details below to see what's happening.
    """,
}

def show_friendly_message(message_key):
    """Display a friendly message"""
    message = FRIENDLY_MESSAGES.get(message_key, "")
    if message:
        st.info(message)

# ==============================================================================
# QUICK TIPS
# ==============================================================================

def render_quick_tip(tip_text):
    """Render a helpful tip box"""
    st.markdown(f"""
        <div style="
            background: rgba(16, 185, 129, 0.1);
            border-left: 4px solid #10b981;
            border-radius: 12px;
            padding: 16px;
            margin: 16px 0;
        ">
            <div style="display: flex; align-items: start; gap: 10px;">
                <span style="font-size: 1.3rem;">💡</span>
                <div>
                    <div style="font-weight: 600; color: #10b981; margin-bottom: 4px;">
                        Quick Tip
                    </div>
                    <div style="color: #cbd5e1; font-size: 0.95rem; line-height: 1.5;">
                        {tip_text}
                    </div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

# ==============================================================================
# FRIENDLY DATE PICKER
# ==============================================================================

def render_friendly_date_picker():
    """Render a simple date picker with examples"""
    st.markdown("""
        <div style="
            background: rgba(59, 130, 246, 0.08);
            border-radius: 12px;
            padding: 16px;
            margin-bottom: 20px;
        ">
            <div style="color: #3b82f6; font-weight: 600; margin-bottom: 8px;">
                📅 Choose Your Date Range
            </div>
            <div style="color: #cbd5e1; font-size: 0.9rem;">
                Pick which time period you want to see. For example:
                <br>• Last 7 days - to see this week
                <br>• Last 30 days - to see this month
                <br>• Custom - to pick your own dates
            </div>
        </div>
    """, unsafe_allow_html=True)

# ==============================================================================
# SIMPLE GLOSSARY
# ==============================================================================

def render_glossary():
    """Render a simple glossary of terms"""
    with st.expander("📖 What do these words mean?"):
        st.markdown("""
            ### Simple Explanations
            
            **Generator** 🔥
            - A machine that makes electricity using diesel fuel
            - Like a big engine that powers your factory
            
            **Solar Panels** ☀️
            - Special panels on the roof that turn sunlight into electricity
            - Free electricity from the sun!
            
            **kWh (Kilowatt-hour)** ⚡
            - A unit that measures electricity
            - Like how you measure water in liters
            
            **Consumption** 📊
            - How much of something you use
            - Like how much water or electricity you use
            
            **Generation** 🔋
            - How much electricity is produced
            - What the solar panels make
            
            **Cost** 💰
            - How much money you spend
            - The price you pay
            
            **Savings** 💵
            - How much money you keep
            - What you don't have to spend
            
            **Trend** 📈
            - Whether numbers are going up or down over time
            - Helps you see if things are getting better or worse
        """)

# ==============================================================================
# COMPARISON HELPER
# ==============================================================================

def explain_comparison(old_value, new_value, unit="", is_cost=False):
    """Generate a simple comparison explanation"""
    change = new_value - old_value
    percent_change = (change / old_value * 100) if old_value != 0 else 0
    
    if abs(percent_change) < 5:
        trend = "stayed about the same"
        emoji = "➡️"
    elif change > 0:
        trend = "increased" if not is_cost else "went up"
        emoji = "📈" if not is_cost else "⬆️"
    else:
        trend = "decreased" if not is_cost else "went down"
        emoji = "📉" if not is_cost else "⬇️"
    
    explanation = f"{emoji} This {trend} by {abs(percent_change):.1f}% compared to before."
    
    if is_cost:
        if change > 0:
            explanation += " You're spending more money now."
        elif change < 0:
            explanation += " You're spending less money now - that's good!"
    
    return explanation
