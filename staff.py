import streamlit as st

def run():
    st.title("👥 الموظفين الحاليين في الوردية")

    roles = {
        "المشرف العام": 1,
        "مشرفي الوردية": 3,
        "المنقذين": 10,
        "عمال النظافة": 30,
        "الكاشيرات": 5,
        "السائقين": 2,
        "الأمن": 22
    }

    for role, default_num in roles.items():
        count = st.number_input(f"{role} المتواجدين الآن:", min_value=0, value=default_num, step=1, key=role)

    if st.button("✅ تحديث الحضور"):
        st.success("تم تحديث عدد الموظفين (غير محفوظ في ملف حاليًا)")
