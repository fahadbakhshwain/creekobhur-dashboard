import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="المهام اليومية - Creek Obhur", layout="wide")
st.title("📋 جدول المهام اليومية - Creek Obhur")

try:
    # قراءة آخر ملف تم حفظه
    df = pd.read_csv("last_message.csv")
    
    st.markdown("✅ **تم تحديث الجدول بناءً على رسالة الإدارة الأخيرة.**")
    st.dataframe(df, use_container_width=True)

except FileNotFoundError:
    st.warning("⚠️ لم يتم إدخال أي مهام بعد. يرجى مراجعة صفحة الإدارة.")
