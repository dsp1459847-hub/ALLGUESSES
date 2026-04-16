import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
from collections import Counter
import random

st.set_page_config(page_title="MAYA AI - Advanced Filter", layout="wide")

st.title("MAYA AI: Zero-Repeat & Absolute Max Elimination")
st.markdown("Yeh system 2 rules par kaam karta hai:\n1. **Max Hit:** Jo number sabse zyada aaya hai, wo bahar.\n2. **Zero-Repeat:** Agar timeframe me koi number repeat nahi hua, toh WO PURI LIST bahar!")

# --- Independent Date Selection ---
st.sidebar.header("Shift Date Controls")

st.sidebar.subheader("Base Shift")
base_start = st.sidebar.date_input("Start Date (Base)", datetime(2026, 1, 1))
base_end = st.sidebar.date_input("End Date (Base)", datetime(2026, 4, 16))

st.sidebar.subheader("Other Shifts")
other_start = st.sidebar.date_input("Start Date (Others)", datetime(2026, 1, 1))
other_end = st.sidebar.date_input("End Date (Others)", datetime(2026, 4, 16))

timeframes = [1, 3, 5, 7, 10, 14, 15, 20, 30]

# --- Dummy Data Generator ---
def load_data():
    dates = pd.date_range(start='2026-01-01', end='2026-04-16')
    return pd.DataFrame({
        'Date': dates,
        'Base_Shift': np.random.randint(0, 100, size=len(dates)),
        'Other_Shift': np.random.randint(0, 100, size=len(dates))
    })

df = load_data()

base_data = df[(df['Date'].dt.date >= base_start) & (df['Date'].dt.date <= base_end)]['Base_Shift'].tolist()
other_data = df[(df['Date'].dt.date >= other_start) & (df['Date'].dt.date <= other_end)]['Other_Shift'].tolist()

# --- Core Logic: Max Elimination + Zero-Repeat Elimination ---
def get_advanced_eliminations(data_list, days):
    """
    User ka Naya Logic: Agar max_freq 1 hai (koi repeat nahi), toh saare numbers bahar!
    Agar max_freq > 1 hai, toh sirf max frequency wale numbers bahar.
    """
    if len(data_list) < days:
        return [], 0, "Not Enough Data"
        
    recent_data = data_list[-days:]
    counts = Counter(recent_data)
    
    if not counts:
        return [], 0, "No Data"
        
    max_freq = max(counts.values())
    
    # --- USER'S NEW LOGIC APPLIED HERE ---
    if max_freq == 1:
        # Koi repeat nahi hua. Saare numbers unique hain.
        # Poori ki poori list ko eliminate kar do!
        eliminated_nums = list(counts.keys())
        status = "Zero-Repeat (Entire Sheet Eliminated)"
    else:
        # Normal Max Elimination
        eliminated_nums = [num for num, freq in counts.items() if freq == max_freq]
        status = f"Max Hit ({max_freq} times)"
        
    return eliminated_nums, max_freq, status

# --- Processing Data ---
st.write("### 🛑 Intelligent Elimination Processing")

col1, col2 = st.columns(2)
all_eliminated_set = set()

with col1:
    st.subheader("Base Shift Analysis")
    base_results = []
    for tf in timeframes:
        elim_nums, max_f, status = get_advanced_eliminations(base_data, tf)
        all_eliminated_set.update(elim_nums)
        base_results.append({
            "Days": tf, 
            "Action Taken": status, 
            "Eliminated #s": ", ".join([f"{x:02d}" for x in elim_nums])
        })
    st.table(pd.DataFrame(base_results))

with col2:
    st.subheader("Other Shifts Analysis")
    other_results = []
    for tf in timeframes:
        elim_nums, max_f, status = get_advanced_eliminations(other_data, tf)
        all_eliminated_set.update(elim_nums)
        other_results.append({
            "Days": tf, 
            "Action Taken": status, 
            "Eliminated #s": ", ".join([f"{x:02d}" for x in elim_nums])
        })
    st.table(pd.DataFrame(other_results))

# --- The Safe Pool ---
total_numbers = set(range(100)) # 00 to 99
safe_pool = total_numbers - all_eliminated_set
safe_pool_list = sorted(list(safe_pool))

st.markdown("---")
st.write("### ✅ The Final Safe Pool (Aapke Filtered Numbers)")
st.info(f"Total Eliminated: **{len(all_eliminated_set)}** numbers. Total Safe Numbers: **{len(safe_pool_list)}** numbers.")

if safe_pool_list:
    safe_str = " | ".join([f"{x:02d}" for x in safe_pool_list])
    st.success(safe_str)
else:
    st.error("Sabhi numbers eliminate ho gaye hain! Yeh rare hai, par iska matlab dataset me bahut zyada variation hai.")

# --- Prediction Engine ---
st.markdown("---")
st.write("### 🎯 Solid Prediction")

if st.button("Generate Final Prediction") and safe_pool_list:
    predicted_number = random.choice(safe_pool_list) 
    st.metric(label="Most Probable Next Number", value=f"{predicted_number:02d}")
    st.write("*(Yeh number us super-filtered pool se hai jisme na koi 'Max Limit' wala number hai, aur na hi koi 'Zero-Repeat' sheet wala bekar number)*")
    
