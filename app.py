import streamlit as st

# إعداد الصفحة
st.set_page_config(
    page_title="Creek Obhur - نظام إدارة الواجهة البحرية",
    page_icon="🏖️",
    layout="wide"
)

# عنوان الصفحة
st.markdown("## 🏖️ نظام إدارة الواجهة البحرية - Creek Obhur")
st.markdown("### 👇 اختر القسم الذي تريد الدخول إليه:")

# مربعات الأقسام
col1, col2 = st.columns(2)

with col1:
    if st.button("📋 المهام اليومية", use_container_width=True):
        st.switch_page("pages/المهام_اليومية.py")

    if st.button("📦 دورات المياه", use_container_width=True):
        st.switch_page("pages/دورات_المياه.py")

    if st.button("🌴 الشواطئ", use_container_width=True):
        st.switch_page("pages/الشواطئ.py")

with col2:
    if st.button("🧑‍🤝‍🧑 الموظفين الحاليين", use_container_width=True):
        st.switch_page("pages/الموظفين_الحاليين.py")

    if st.button("🏢 الإدارة", use_container_width=True):
        st.switch_page("pages/الإدارة.py")

# ملاحظة
st.markdown("---")
st.info("🛠️ هذا النظام تحت التطوير - يرجى إبلاغ الإدارة بأي ملاحظات.")
