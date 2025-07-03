import streamlit as st
import pandas as pd
import datetime
import os

TASKS_FILE = "tasks.csv"
SCHEDULE_FILE = "weekly_schedule.txt"
DAILY_STAFF_SCHEDULE_CSV = "daily_staff_schedule.csv"

def load_tasks():
    if os.path.exists(TASKS_FILE):
        try:
            return pd.read_csv(TASKS_FILE)
        except pd.errors.EmptyDataError:
            return pd.DataFrame(columns=["التاريخ", "المشرف", "المهمة", "ملاحظات"])
    return pd.DataFrame(columns=["التاريخ", "المشرف", "المهمة", "ملاحظات"])

def load_weekly_schedule():
    if os.path.exists(SCHEDULE_FILE):
        with open(SCHEDULE_FILE, "r", encoding="utf-8") as f:
            return f.read()
    return "لا يوجد جدول أسبوعي حالياً. يرجى من المديرة إدخال الجدول."

def load_daily_staff_schedule_df():
    if os.path.exists(DAILY_STAFF_SCHEDULE_CSV):
        try:
            return pd.read_csv(DAILY_STAFF_SCHEDULE_CSV)
        except pd.errors.EmptyDataError:
            return pd.DataFrame()
    return pd.DataFrame()

def markdown_table_to_dataframe(markdown_text):
    lines = markdown_text.strip().split('\n')
    if len(lines) < 2: 
        return pd.DataFrame() 

    header_line = lines[0].strip('|')
    header_parts = header_line.split('|')
    header = [h.strip() for h in header_parts]
    
    if len(lines) > 1 and all(c in ['-', '|', ' ', ':'] for c in lines[1].strip()):
        data_lines = lines[2:]
    else:
        data_lines = lines[1:]

    data = []
    for line in data_lines:
        if line.strip():
            row = [item.strip() for item in line.strip('|').split('|')]
            if len(row) == len(header):
                data.append(row)
            else:
                pass 

    return pd.DataFrame(data, columns=header) if data else pd.DataFrame(columns=header)

def run():
    st.title("📋 المهام اليومية")
    st.info("يُعرض هنا كل المهام المرسلة من المديرة (عبر الجوال أو الموقع) حسب التاريخ.")

    # تحميل المهام من ملف CSV
    all_tasks = load_tasks()

    # تحديد تاريخ اليوم بتوقيت جدة
    current_date_jeddah = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=3))).date()
    today_date_str = current_date_jeddah.isoformat()

    # تصفية المهام الخاصة بتاريخ اليوم
    daily_tasks = all_tasks[all_tasks["التاريخ"] == today_date_str]

    # قائمة المشرفين
    all_possible_supervisors = ["الكل", "المشرف الأول", "المشرف الثاني", "العمالة العامة", "فريق الصيانة", "المديرة", "أمن"]

    # فلترة حسب المشرف
    selected_supervisor = st.selectbox("اختر المشرف لتصفية المهام:", all_possible_supervisors)

    if selected_supervisor != "الكل":
        daily_tasks = daily_tasks[daily_tasks["المشرف"] == selected_supervisor]

    if not daily_tasks.empty:
        st.dataframe(
            daily_tasks[['التاريخ', 'المشرف', 'المهمة', 'ملاحظات']].style.set_properties(
                **{'text-align': 'right', 'font-size': '16px'}
            ),
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("لا توجد مهام لهذا اليوم.")

    # عرض الجدول الأسبوعي
    st.subheader("📅 جدول العمل الأسبوعي:")
    weekly_schedule_text = load_weekly_schedule()
    weekly_schedule_df = markdown_table_to_dataframe(weekly_schedule_text)
    
    if not weekly_schedule_df.empty:
        st.dataframe(weekly_schedule_df.style.set_properties(**{'text-align': 'right', 'font-size': '16px'}), hide_index=True)
    else:
        st.markdown(weekly_schedule_text)
        if weekly_schedule_text.strip() != "لا يوجد جدول أسبوعي حالياً. يرجى من المديرة إدخال الجدول.":
            st.warning("الجدول الأسبوعي المدخل ليس بتنسيق جدول Markdown صالح لعرضه كجدول بيانات.")

    # عرض جدول دوام الموظفين اليومي
    st.subheader("👥 جدول دوام الموظفين:")
    daily_staff_schedule_df = load_daily_staff_schedule_df()
    if not daily_staff_schedule_df.empty:
        with st.expander("اضغط لعرض جدول الدوام كاملاً"):
            st.dataframe(daily_staff_schedule_df.style.set_properties(**{'text-align': 'right', 'font-size': '16px'}), use_container_width=True, hide_index=True)
    else:
        st.info("لا يوجد جدول دوام يومي مرفوع حالياً.")

# تشغيل التطبيق
run()




   

    

    
        
