import streamlit as st
import toilets
import beaches
import view
import staff  # أضف هذا

st.set_page_config(page_title="Creek Obhur", layout="wide")

st.title("🏖️ نظام إدارة الواجهة البحرية - Creek Obhur")
st.markdown("👇 اختر القسم الذي تريد الدخول إليه:")

section = st.selectbox("📋 الأقسام:", ["الرئيسية", "دورات المياه", "الشواطئ", "المهام اليومية", "الموظفين الحاليين"])

if section == "دورات المياه":
    toilets.run()
elif section == "الشواطئ":
    beaches.run()
elif section == "المهام اليومية":
    view.run()
elif section == "الموظفين الحاليين":
    staff.run()
else:
    st.subheader("👈 الرجاء اختيار قسم من القائمة.")
