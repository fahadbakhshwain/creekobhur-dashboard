import streamlit as st

def run():
    st.title("📝 المهام اليومية")

    sections = [
        "نظافة الواجهة", "تشغيل الإضاءات", "طاولات الزوار", 
        "تنظيم الفواتير", "متابعة الكاشيرات", "ملاحظات المشرف"
    ]

    for section in sections:
        st.text_area(f"{section}:", key=section)

    if st.button("✅ حفظ المهام"):
        st.success("تم حفظ المهام بنجاح (حفظ مؤقت)")
