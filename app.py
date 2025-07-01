import streamlit as st

# --- إعداد الصفحة ---
st.set_page_config(page_title="نظام إدارة الواجهة البحرية", layout="wide")

# --- العنوان الرئيسي ---
st.title("🏖️ نظام إدارة الواجهة البحرية - Creek Obhur")

st.markdown("### 👇 اختر القسم الذي تريد الدخول إليه:")

# --- اختيار القسم من القائمة ---
section = st.selectbox("📋 الأقسام:", ["الرئيسية", "دورات المياه", "الشواطئ", "الموظفين الحاليين", "المهام اليومية"])

# --- واجهة رئيسية ---
if section == "الرئيسية":
    st.header("📦 الأقسام")
    col1, col2 = st.columns(2)

    with col1:
        if st.button("🚻 دورات المياه"):
            section = "دورات المياه"
    with col2:
        if st.button("📝 المهام اليومية"):
            section = "المهام اليومية"

    col3, col4 = st.columns(2)
    with col3:
        if st.button("🏖️ الشواطئ"):
            section = "الشواطئ"
    with col4:
        if st.button("👥 الموظفين الحاليين"):
            section = "الموظفين الحاليين"

# --- ربط الصفحات الفرعية ---
if section == "دورات المياه":
    import toilets
    toilets.run()

elif section == "المهام اليومية":
    import admin
    admin.run()

elif section == "الشواطئ":
    import beaches
    beaches.run()

elif section == "الموظفين الحاليين":
    import view
    view.run()

