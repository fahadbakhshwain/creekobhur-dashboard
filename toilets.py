import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="دورات المياه - Creek Obhur", layout="wide")
st.title("🚽 إدارة دورات المياه - Creek Obhur")

# اختيار رقم دورة المياه
toilet_number = st.selectbox("🔢 رقم دورة المياه:", ["1", "2", "3"])
gender = st.radio("🚻 النوع:", ["رجال", "نساء"])

# بيانات الحالة
cleaned = st.radio("✅ هل تم تنظيفها اليوم؟", ["نعم", "لا"])
missing_items = st.radio("🧼 هل يوجد أدوات ناقصة؟", ["نعم", "لا"])
maintenance_needed = st.radio("🔧 هل تحتاج صيانة؟", ["نعم", "لا"])
notes = st.text_area("📝 ملاحظات إضافية:")

# زر الحفظ
if st.button("💾 حفظ الحالة"):
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    new_entry = {
        "التاريخ": now,
        "رقم الدورة": toilet_number,
        "النوع": gender,
        "تم التنظيف": cleaned,
        "أدوات ناقصة": missing_items,
        "تحتاج صيانة": maintenance_needed,
        "ملاحظات": notes
    }

    try:
        df = pd.read_csv("toilets_log.csv")
    except FileNotFoundError:
        df = pd.DataFrame()

    df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)
    df.to_csv("toilets_log.csv", index=False)

    st.success("✅ تم حفظ بيانات دورة المياه بنجاح!")

# عرض السجل
with st.expander("📋 عرض السجل الكامل"):
    try:
        log_df = pd.read_csv("toilets_log.csv")
        st.dataframe(log_df, use_container_width=True)
    except FileNotFoundError:
        st.info("لا يوجد بيانات محفوظة بعد.")
