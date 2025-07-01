import streamlit as st

def run():
    st.title("👥 الموظفين الحاليين في الوردية")

    roles = {
        "👨‍✈️ مشرف الوردية": 1,
        "🎯 مشرفي الشواطئ": 3,
        "🧹 عمال النظافة": 10,
        "🧺 عمال النظافة الإضافيين": 30,
        "💰 الكاشير": 5,
        "🛟 المنقذين": 2,
        "👮‍♂️ الأمن": 22
    }

    staff_counts = {}

    for role, default_num in roles.items():
        count = st.number_input(f"{role} - اختر العدد", min_value=0, value=default_num, step=1, key=role)
        staff_counts[role] = count

    if st.button("✅ تحديث الحضور"):
        st.success("✔️ تم تحديث عدد الموظفين")
        st.subheader("👁‍🗨 عرض الموظفين في الوردية الحالية:")
        st.write(staff_counts)
