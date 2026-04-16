import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from collections import Counter

st.set_page_config(page_title="MAYA AI - Frequency Saturation Engine", layout="wide")

st.title("MAYA AI: Saturation & Elimination Filter")
st.markdown("Yeh system har timeframe mein numbers ki repetition frequency check karta hai. Jo numbers apni limit (Saturation Point) par pohoch chuke hain, unhe eliminate karta hai aur 'Growth Phase' wale numbers ko highlight karta hai.")

# --- Independent Date Selection for Accuracy ---
st.sidebar.header("Shift Date Controls")
st.sidebar.markdown("**Base Shift**")
base_start = st.sidebar.date_input("Start Date (Base)", datetime(2026, 1, 1))
base_end = st.sidebar.date_input("End Date (Base)", datetime(2026, 4, 1))

st.sidebar.markdown("**Other Shifts**")
other_start = st.sidebar.date_input("Start Date (Others)", datetime(2026, 1, 1))
other_end = st.sidebar.date_input("End Date (Others)", datetime(2026, 4, 1))

# --- Frequency Limits (User Controls) ---
st.sidebar.header("Elimination Rules")
max_repeat_limit = st.sidebar.number_input("Maximum Repeat Limit (e.g., 4 times)", min_value=2, max_value=10, value=4)

# --- Dummy Data Generation ---
def generate_data():
    dates = pd.date_range(start='2026-01-01', end='2026-04-01')
    return pd.DataFrame({
        'Date': dates,
        'Base_Shift': np.random.randint(0, 100, size=len(dates)),
        'Other_Shift': np.random.randint(0, 100, size=len(dates))
    })

df = generate_data()

# Apply Independent Date Filters
base_data = df[(df['Date'].dt.date >= base_start) & (df['Date'].dt.date <= base_end)]

def analyze_frequency_and_eliminate(data, days_window, max_limit):
    """
    Yeh function pichle 'N' dino ka data uthata hai, numbers ginta hai, 
    aur elimination ya promotion list banata hai.
    """
    recent_data = data.tail(days_window)['Base_Shift'].tolist()
    counts = Counter(recent_data)
    
    eliminated = []
    high_probability = []
    
    # 00 se 99 tak sabhi numbers ko check karna
    for num in range(100):
        freq = counts.get(num, 0)
        
        # Rule 1: Agar limit (e.g., 4) touch kar li, toh bahar nikal do
        if freq >= max_limit:
            eliminated.append(num)
            
        # Rule 2: Agar limit se thoda door hai (e.g., 1 ya 2 baar aaye hain) 
        # toh unke upar aane ke chances zyada hain (Growth phase)
        elif freq == max_limit - 2 or freq == max_limit - 3:
            high_probability.append(num)
            
    return eliminated, high_probability

# --- Multi-Timeframe Frequency Analysis ---
st.write("### Frequency & Saturation Report")

timeframes = {"3 Days": 3, "5 Days": 5, "Weekly (7)": 7, "15 Days": 15, "Monthly (30)": 30}
results = []

for label, days in timeframes.items():
    if len(base_data) >= days:
        elim, high_prob = analyze_frequency_and_eliminate(base_data, days, max_repeat_limit)
        results.append({
            "Timeframe": label,
            "Eliminated Numbers (Won't Come)": len(elim),
            "High Prob. Candidates (Will Grow)": len(high_prob),
            "Eliminated List": ", ".join([f"{x:02d}" for x in elim[:10]]) + ("..." if len(elim)>10 else ""),
            "Hot Candidates": ", ".join([f"{x:02d}" for x in high_prob[:10]]) + ("..." if len(high_prob)>10 else "")
        })

if results:
    results_df = pd.DataFrame(results)
    st.table(results_df)
    
    st.markdown("---")
    st.subheader("Actionable Insights")
    st.success(f"**Filter Logic Applied:** Jo numbers {max_repeat_limit} baar aa chuke hain, unhe direct pool se bahar kar diya gaya hai. Ab aapke paas predictions ke liye chhota aur solid dataset bacha hai.")
    st.info("Aap upar diye gaye 'Hot Candidates' ko apne Random Forest ya LSTM model me feed kar sakte hain taaki sirf inhi numbers me se final prediction nikale.")
else:
    st.warning("Data range kafi nahi hai analysis ke liye.")
    
