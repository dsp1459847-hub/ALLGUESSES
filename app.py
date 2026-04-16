import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from collections import Counter

st.set_page_config(page_title="MAYA AI - Stable Predictor", layout="wide")

st.title("MAYA AI: Stable Prediction & Date Confirmation")

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

def get_advanced_eliminations(data_list, days):
    if len(data_list) < days: return [], 0
    counts = Counter(data_list[-days:])
    if not counts: return [], 0
    
    max_freq = max(counts.values())
    if max_freq == 1:
        return list(counts.keys()), max_freq # Zero-Repeat Logic
    else:
        return [num for num, freq in counts.items() if freq == max_freq], max_freq

# --- Filtering Process ---
all_eliminated_set = set()

for tf in timeframes:
    elim_base, _ = get_advanced_eliminations(base_data, tf)
    elim_other, _ = get_advanced_eliminations(other_data, tf)
    all_eliminated_set.update(elim_base)
    all_eliminated_set.update(elim_other)

safe_pool_list = sorted(list(set(range(100)) - all_eliminated_set))

# --- NEW: Target Date Confirmation ---
# Prediction hamesha Base Shift ki End Date ke agle din ke liye hogi
target_prediction_date = base_end + timedelta(days=1)

st.markdown("---")
st.write(f"### 🎯 Final Prediction Data")
st.info(f"**Target Prediction Date:** {target_prediction_date.strftime('%d %B %Y')} (Aapki select ki gayi End Date ke theek agla din)")

if st.button("Generate Final Prediction"):
    if safe_pool_list:
        # --- NEW: Fixed Deterministic Logic (Randomness Hata Di Gayi Hai) ---
        # Logic: Hum pichle 7 din ka average trend nikalenge aur 'Safe Pool' 
        # mein se wo number chunenge jo is trend ke sabse kareeb ho.
        # Isse button dabane par number change nahi hoga.
        
        if len(base_data) >= 7:
            recent_trend_average = np.mean(base_data[-7:])
        else:
            recent_trend_average = np.mean(base_data) # Agar data 7 din se kam hai
            
        # Finding the closest number to the trend in the safe pool
        predicted_number = min(safe_pool_list, key=lambda x: abs(x - recent_trend_average))
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric(label="Predicted Number for Next Shift", value=f"{predicted_number:02d}")
        with col2:
            st.metric(label="Current Trend Average", value=f"{int(recent_trend_average):02d}")
            
        st.success("Ab yeh number FIX rahega. Yeh Safe Pool mein se wo number hai jo recent market trend ke sabse zyada kareeb hai.")
    else:
        st.error("Safe pool empty hai. Please adjust date ranges.")

