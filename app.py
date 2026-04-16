import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from collections import Counter

st.set_page_config(page_title="MAYA AI - Ultimate Engine", layout="wide")

st.title("MAYA AI: 22-Pattern Multi-Tier Analysis")

# --- 1. Sidebar Controls (Independent Shifts) ---
st.sidebar.header("Shift & Pattern Controls")
base_end_date = st.sidebar.date_input("Base Shift End Date", datetime(2026, 4, 16))
max_repeat_limit = st.sidebar.slider("Max Repeat Limit", 2, 5, 4)

# --- 2. Data Locking Logic ---
@st.cache_data
def load_full_data():
    np.random.seed(42)
    dates = pd.date_range(start='2025-01-01', end='2026-04-16')
    return pd.DataFrame({
        'Date': dates,
        'Base_Shift': np.random.randint(0, 100, size=len(dates)),
        'Shift_A': np.random.randint(0, 100, size=len(dates)),
        'Shift_B': np.random.randint(0, 100, size=len(dates))
    })

df = load_full_data()
current_data = df[df['Date'].dt.date <= base_end_date]

# --- 3. Elimination & Pattern Scoring Engine ---
def analyze_all_sheets(data_df, limit):
    eliminated_total = set()
    pattern_scores = Counter() # Scoring for High/Medium/Low
    
    shifts = ['Base_Shift', 'Shift_A', 'Shift_B']
    
    for shift in shifts:
        shift_list = data_df[shift].tolist()
        
        # 1 se 30 din ki har ek sheet (timeframe) ko check karna
        for days in range(1, 31):
            if len(shift_list) < days: continue
            
            sheet = shift_list[-days:]
            counts = Counter(sheet)
            
            # RULE 1: Zero-Repeat Elimination (Entire sheet out)
            if len(counts) == len(sheet) and len(sheet) > 1:
                eliminated_total.update(sheet)
            
            # RULE 2: Max Hit Elimination
            for num, freq in counts.items():
                if freq >= limit:
                    eliminated_total.add(num)
                else:
                    # PATTERN SCORING: Agar number safe hai, toh uska score badhao
                    # Jitni zyada sheets mein ye number "Unique" aur "Within Limit" milega, 
                    # utna hi ye Strong (High) hoga.
                    pattern_scores[num] += 1
                    
    return eliminated_total, pattern_scores

# --- 4. Tiering & Verification Logic ---
eliminated, scores = analyze_all_sheets(current_data, max_repeat_limit)
safe_pool = [n for n in range(100) if n not in eliminated]

# Scores ke basis par divide karna (High, Medium, Low)
if safe_pool:
    sorted_safe = sorted(safe_pool, key=lambda x: scores[x], reverse=True)
    
    n = len(sorted_safe)
    high_tier = sorted_safe[:int(n*0.2)]      # Top 20%
    med_tier = sorted_safe[int(n*0.2):int(n*0.6)] # Mid 40%
    low_tier = sorted_safe[int(n*0.6):]       # Bottom 40%
    
    # --- 5. Back-Testing (Verification) ---
    # Pichle 5 din ka data utha kar check karna ki kaunsa tier zyada hit ho raha hai
    last_5_days = current_data['Base_Shift'].tail(5).tolist()
    hits = {"High": 0, "Medium": 0, "Low": 0}
    
    for val in last_5_days:
        if val in high_tier: hits["High"] += 1
        elif val in med_tier: hits["Medium"] += 1
        elif val in low_tier: hits["Low"] += 1
    
    best_tier = max(hits, key=hits.get)
else:
    high_tier, med_tier, low_tier = [], [], []
    best_tier = "None"

# --- 6. Final UI Display ---
target_date = base_end_date + timedelta(days=1)
st.markdown(f"### 🎯 Prediction for: {target_date.strftime('%d %B %Y')}")

col1, col2, col3 = st.columns(3)
with col1:
    st.error(f"Eliminated: {len(eliminated)}")
with col2:
    st.success(f"Safe Pool: {len(safe_pool)}")
with col3:
    st.info(f"Hot Category: {best_tier} Tier")

st.markdown("---")

# Category Wise Table
st.subheader("📊 Tiered Classification (Based on 1-30 Day Patterns)")
t1, t2, t3 = st.columns(3)

with t1:
    st.markdown("#### 🔥 High (Strong)")
    st.write(", ".join([f"{x:02d}" for x in high_tier]))
    st.caption(f"Verification: {hits['High']} hits in last 5 days")

with t2:
    st.markdown("#### ⚡ Medium (Neutral)")
    st.write(", ".join([f"{x:02d}" for x in med_tier]))
    st.caption(f"Verification: {hits['Medium']} hits in last 5 days")

with t3:
    st.markdown("#### ❄️ Low (Weak)")
    st.write(", ".join([f"{x:02d}" for x in low_tier]))
    st.caption(f"Verification: {hits['Low']} hits in last 5 days")

st.markdown("---")
st.subheader("💡 Analysis Summary")
if best_tier != "None":
    st.write(f"Historical data ke hisab se, filhaal **{best_tier} Tier** ke numbers sabse zyada pattern match kar rahe hain. Agli date ke liye is tier par focus karna sabse behtar ho sakta hai.")

st.info("Is engine mein 1-30 din ki sabhi shifton ko compare karke elimination aur tiering ek sath perform ki gayi hai.")
