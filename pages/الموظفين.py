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
import streamlit as st

def run():
    st.title("الموظفين الساحليين في دورية (العبور)")
    # (باقي الكود الخاص بالصفحة)
    roles = {
        "المشرف": 1,
        "المشرف العام": 3,
        "مساعد المشرف": 10,
        "مستشار قانوني": 20,
        "المحاسب": 5,
        "موظف": 22,
    }
    staff_counts = {}

    for role, default_num in roles.items():
        count = st.number_input(f"ادخل عدد {role}:", value=default_num, key=role)
        staff_counts[role] = count

    if st.button("تحديث عدد الموظفين"):
        st.success("تم تحديث عدد الموظفين!")
        st.subheader("عدد الموظفين في الدورية كالتالي:")
        st.write(staff_counts)

# أضف هذا السطر في النهاية:
run()
