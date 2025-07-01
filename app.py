import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="نظام إدارة الواجهة البحرية", layout="wide")

st.title("🏖️ نظام إدارة الواجهة البحرية - Creek Obhur")
st.markdown("### 👇 اختر القسم الذي تريد الدخول إليه:")

# تحديد القسم المختار
section = st.selectbox(
    "🔲 الأقسام:",
    ["🏠 الرئيسية", "🧼 دورات المياه", "📋 المهام اليومية", "🏖️ الشواطئ", "👥 الموظفين الحاليين"]
)

# 🏠 الرئيسية - مربعات تنقل
if section == "🏠 الرئيسية":
    st.markdown("## 📦 الأقسام")
    col1, col2 = st.columns(2)

    with col1:
        if st.button("🧼 دورات المياه", use_container_width=True):
            section = "🧼 دورات المياه"
    with col2:
        if st.button("📋 المهام اليومية", use_container_width=True):
            section = "📋 المهام اليومية"

    col3, col4 = st.columns(2)
    with col3:
        if st.button("🏖️ الشواطئ", use_container_width=True):
            section = "🏖️ الشواطئ"
    with col4:
        if st.button("👥 الموظفين الحاليين", use_container_width=True):
            section = "👥 الموظفين الحاليين"

# 🧼 دورات المياه
if section == "🧼 دورات المياه":
    st.h

