import streamlit as st

def run():
    st.title("🚽 قسم دورات المياه")

    toilet = st.selectbox("اختر دورة المياه:", ["1 - رجال", "1 - نساء", "2 - رجال", "2 - نساء", "3 - رجال", "3 - نساء"])

    st.text_input("آخر وقت تم التنظيف فيه", key=f"clean_time_{toilet}")
    st.text_area("الملاحظات الخاصة بالنظافة", key=f"notes_clean_{toilet}")
    st.text_input("المستلزمات الناقصة (صابون، مناديل، ...)", key=f"missing_items_{toilet}")
    st.text_area("ملاحظات الصيانة المطلوبة", key=f"maintenance_notes_{toilet}")

    if st.button("✅ حفظ البيانات"):
        st.success("تم حفظ البيانات مؤقتًا (في الذاكرة فقط).")
import streamlit as st

def run():
    st.title("دورات المياه")
    toilet = st.selectbox(
        "اختر رقم دورة المياه:",
        ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14"],
        key="clean_time_toilet",
    )
    st.text_input("آخر وقت تم التنظيف فيه", key="last_clean_time")
    st.text_input("الملاحظات الخاصة بالنظافة", key="notes_clean_toilet")
    st.text_input("كمية المواد المستهلكة لخدمة دورة المياه", key="missing_items_toilet")
    st.text_input("ملاحظات خاصة بالمسؤول", key="maintainance_notes_toilet")

    if st.button("حفظ البيانات"):
        st.success("تم حفظ البيانات بنجاح في دورة المياه")

# أضف هذا السطر في النهاية:
run()
