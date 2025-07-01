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
