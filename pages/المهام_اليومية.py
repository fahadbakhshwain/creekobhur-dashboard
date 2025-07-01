import streamlit as st
import pandas as pd
import datetime
import os

# اسم الملف لحفظ المهام
TASKS_FILE = "tasks.csv"
SCHEDULE_FILE = "weekly_schedule.txt" # لجدول العمل الأسبوعي

# دالة لتحميل المهام من ملف CSV
def load_tasks():
    if os.path.exists(TASKS_FILE):
        return pd.read_csv(TASKS_FILE)
    return pd.DataFrame(columns=["التاريخ", "المشرف", "المهمة", "ملاحظات"])

# دالة لحفظ المهام في ملف CSV
def save_tasks(df):
    df.to_csv(TASKS_FILE, index=False)

# دالة لتحميل الجدول الأسبوعي
def load_weekly_schedule():
    if os.path.exists(SCHEDULE_FILE):
        with open(SCHEDULE_FILE, "r", encoding="utf-8") as f:
            return f.read()
    return "لا يوجد جدول أسبوعي حالياً. يرجى من المديرة إدخال الجدول."

# دالة لحفظ الجدول الأسبوعي
def save_weekly_schedule(schedule_text):
    with open(SCHEDULE_FILE, "w", encoding="utf-8") as f:
        f.write(schedule_text)

def run():
    st.title("📋 المهام اليومية")
    st.info("هنا يتم تسجيل وتتبع المهام اليومية والجدول الأسبوعي.")

    # قسم المديرة: لإدخال المهام والجدول الأسبوعي
    st.header("إدارة المهام والجدول (للمديرة)")
    with st.expander("إضافة مهمة جديدة"):
        with st.form("new_task_form", clear_on_submit=True):
            task_date = st.date_input("تاريخ المهمة:", datetime.date.today())
            supervisor = st.selectbox(
                "المشرف المسؤول:",
                ["المشرف الأول", "المشرف الثاني", "المشرف الثالث", "العمالة العامة", "فريق الصيانة"], # يمكنك تعديل هذه الأسماء لتشمل المشرفين الفعليين
                key="task_supervisor"
            )
            task_description = st.text_area("المهمة المطلوبة:", key="task_desc", height=100)
            notes = st.text_area("ملاحظات إضافية:", key="task_notes", height=70)

            submitted = st.form_submit_button("إضافة المهمة")
            if submitted:
                # التحقق من أن المهمة ليست فارغة
                if task_description.strip() == "":
                    st.error("الرجاء كتابة وصف للمهمة قبل الإضافة.")
                else:
                    new_task = pd.DataFrame([{
                        "التاريخ": task_date.isoformat(),
                        "المشرف": supervisor,
                        "المهمة": task_description,
                        "ملاحظات": notes
                    }])
                    all_tasks = load_tasks()
                    # إضافة تحقق لتجنب تكرار الصفوف إذا كان الملف فارغاً في البداية
                    if all_tasks.empty and os.path.exists(TASKS_FILE):
                        updated_tasks = new_task
                    else:
                        updated_tasks = pd.concat([all_tasks, new_task], ignore_index=True)
                    
                    save_tasks(updated_tasks)
                    st.success("✅ تم إضافة المهمة بنجاح!")
                    st.experimental_rerun() # لإعادة تحميل الصفحة وعرض المهمة المضافة

    with st.expander("تحديث الجدول الأسبوعي"):
        current_schedule = load_weekly_schedule()
        new_schedule_text = st.text_area("أدخل الجدول الأسبوعي هنا:", value=current_schedule, height=200)
        if st.button("حفظ الجدول الأسبوعي"):
            save_weekly_schedule(new_schedule_text)
            st.success("✅ تم حفظ الجدول الأسبوعي بنجاح!")
            st.experimental_rerun() # لإعادة تحميل الصفحة

    # قسم عرض المهام (للمشرفين)
    st.header("عرض المهام اليومية والجدول الأسبوعي")

    st.subheader("🗓️ المهام المطلوبة لليوم:")
    all_tasks = load_tasks()
    today_date_str = datetime.date.today().isoformat()
    daily_tasks = all_tasks[all_tasks["التاريخ"] == today_date_str]

    if not daily_tasks.empty:
        # عرض المهام في جدول جميل
        st.dataframe(daily_tasks[['المشرف', 'المهمة', 'ملاحظات']].style.set_properties(**{'text-align': 'right', 'font-size': '16px'}), hide_index=True)
        # خيار تصفية المهام حسب المشرف
        st.markdown("---")
        st.write("---") # فاصل مرئي
        st.subheader("🔍 تصفية المهام حسب المشرف:")
        unique_supervisors = ["الكل"] + daily_tasks["المشرف"].unique().tolist()
        selected_supervisor_filter = st.selectbox("اختر المشرف:", unique_supervisors)

        if selected_supervisor_filter == "الكل":
            st.dataframe(daily_tasks[['المشرف', 'المهمة', 'ملاحظات']].style.set_properties(**{'text-align': 'right', 'font-size': '16px'}), hide_index=True)
        else:
            filtered_tasks = daily_tasks[daily_tasks["المشرف"] == selected_supervisor_filter]
            st.dataframe(filtered_tasks[['المهمة', 'ملاحظات']].style.set_properties(**{'text-align': 'right', 'font-size': '16px'}), hide_index=True)

    else:
        st.info("لا توجد مهام محددة لهذا اليوم حتى الآن. يرجى من المديرة إضافتها.")

    st.subheader("جدول العمل الأسبوعي الحالي:")
    st.markdown(load_weekly_schedule())


# استدعاء الدالة لتشغيل الصفحة
run()
