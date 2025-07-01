import streamlit as st
import pandas as pd
import datetime
import os
import io

# اسم الملف لحفظ المهام
TASKS_FILE = "tasks.csv"
SCHEDULE_FILE = "weekly_schedule.txt" # لجدول العمل الأسبوعي
DAILY_STAFF_SCHEDULE_FILE = "daily_staff_schedule.txt" # لجدول دوام الموظفين اليومي

# دالة لتحميل المهام من ملف CSV
def load_tasks():
    if os.path.exists(TASKS_FILE):
        try:
            return pd.read_csv(TASKS_FILE)
        except pd.errors.EmptyDataError:
            return pd.DataFrame(columns=["التاريخ", "المشرف", "المهمة", "ملاحظات"])
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

# دالة لتحميل جدول دوام الموظفين اليومي
def load_daily_staff_schedule():
    # جدول الدوام يتعلق بتاريخ محدد. سنقوم بتخزينه بأسماء ملفات مختلفة لكل يوم
    # أو نضمن التاريخ في الكود نفسه.
    # للحفاظ على البساطة في البروتوتايب، سنستخدم ملفاً واحداً يتحدث يومياً.
    if os.path.exists(DAILY_STAFF_SCHEDULE_FILE):
        with open(DAILY_STAFF_SCHEDULE_FILE, "r", encoding="utf-8") as f:
            return f.read()
    return "لا يوجد جدول دوام يومي حالياً. يرجى من المديرة إدخال الجدول."

# دالة لحفظ جدول دوام الموظفين اليومي
def save_daily_staff_schedule(schedule_text):
    with open(DAILY_STAFF_SCHEDULE_FILE, "w", encoding="utf-8") as f:
        f.write(schedule_text)

# دالة لتحويل نص Markdown Table إلى DataFrame
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
                # يمكنك إظهار تحذير للمديرة إذا كان الصف غير متطابق
                pass # st.warning(f"تم تجاهل صف غير متطابق في الجدول: {line}")

    return pd.DataFrame(data, columns=header) if data else pd.DataFrame(columns=header)


def run():
    st.title("📋 المهام اليومية")
    st.info("هنا يتم تسجيل وتتبع المهام اليومية والجدول الأسبوعي وجدول دوام الموظفين.")

    # قائمة المشرفين الكاملة التي يمكن استخدامها في جميع الـ selectbox
    all_possible_supervisors = ["المشرف الأول", "المشرف الثاني", "المشرف الثالث", "العمالة العامة", "فريق الصيانة", "المديرة", "أمن"] # أضفت "أمن"

    # قسم المديرة: لإدخال المهام والجداول
    st.header("إدارة المهام والجداول (للمديرة)")

    # نموذج إضافة المهام اليومية
    with st.expander("➕ إضافة مهمة جديدة"):
        with st.form("new_task_form", clear_on_submit=True):
            current_date_jeddah = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=3))).date() 
            task_date = st.date_input("تاريخ المهمة:", current_date_jeddah)
            
            supervisor = st.selectbox(
                "المشرف المسؤول:",
                all_possible_supervisors,
                key="task_supervisor"
            )
            task_description = st.text_area("المهمة المطلوبة:", key="task_desc", height=100)
            notes = st.text_area("ملاحظات إضافية:", key="task_notes", height=70)

            submitted = st.form_submit_button("إضافة المهمة")
            if submitted:
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
                    
                    if all_tasks.empty:
                        updated_tasks = new_task
                    else:
                        updated_tasks = pd.concat([all_tasks, new_task], ignore_index=True)
                    
                    save_tasks(updated_tasks)
                    st.success("✅ تم إضافة المهمة بنجاح!")
                    st.rerun()

    # نموذج تحديث الجدول الأسبوعي
    with st.expander("📅 تحديث الجدول الأسبوعي"):
        st.markdown("**يرجى إدخال الجدول الأسبوعي بتنسيق Markdown للجدول (مثال بالأسفل):**")
        st.code("""
| اليوم | الوقت | المهمة | المسؤول |
|---|---|---|---|
| الثلاثاء | 08:00 ص | اجتماع إداري | المديرة |
| الثلاثاء | 09:00 ص | تفقد دورات المياه | المشرف الأول |
""", language='markdown') 

        current_schedule_text = load_weekly_schedule()
        new_schedule_text = st.text_area("أدخل الجدول الأسبوعي هنا:", value=current_schedule_text, height=300, key="weekly_schedule_input")
        
        if st.button("حفظ الجدول الأسبوعي", key="save_weekly_schedule_btn"):
            save_weekly_schedule(new_schedule_text)
            st.success("✅ تم حفظ الجدول الأسبوعي بنجاح!")
            st.rerun()

    # نموذج تحديث جدول دوام الموظفين اليومي
    with st.expander("👥 تحديث جدول دوام الموظفين اليومي"):
        st.markdown("**يرجى إدخال جدول الدوام اليومي بتنسيق Markdown للجدول (مثال بالأسفل):**")
        st.code("""
| الاسم | الوقت       | الوظيفة | الأحد | الاثنين | الثلاثاء | الأربعاء | الخميس | الجمعة | السبت |
|---|------------|--------|---|---|---|---|---|---|---|
| فهد  | 7AM-4PM    | مشرف   | ON  | OFF    | ON     | ON     | ON    | ON   | ON   |
| منى  | 6AM-3PM    | كاشير  | ON  | ON     | ON     | OFF    | ON    | ON   | ON   |
| جياد | 3PM-11PM   | حارس أمن | ON  | ON     | ON     | ON     | ON    | ON   | ON   |
""", language='markdown') 

        current_daily_staff_schedule_text = load_daily_staff_schedule()
        new_daily_staff_schedule_text = st.text_area("أدخل جدول الدوام اليومي هنا:", value=current_daily_staff_schedule_text, height=350, key="daily_staff_schedule_input")
        
        if st.button("حفظ جدول الدوام اليومي", key="save_daily_staff_schedule_btn"):
            save_daily_staff_schedule(new_daily_staff_schedule_text)
            st.success("✅ تم حفظ جدول الدوام اليومي بنجاح!")
            st.rerun()


    # قسم عرض المهام والجداول (للمشرفين)
    st.header("عرض المهام اليومية والجداول")

    st.subheader("🗓️ المهام المطلوبة لليوم:")
    all_tasks = load_tasks()
    
    current_date_jeddah = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=3))).date()
    today_date_str = current_date_jeddah.isoformat()

    daily_tasks = all_tasks[all_tasks["التاريخ"] == today_date_str]

    # قائمة المشرفين الشاملة للتصفية (بما في ذلك "الكل")
    filter_supervisor_options = ["الكل"] + all_possible_supervisors 

    # تحديد القيمة الافتراضية لـ selectbox التصفية
    default_filter_index = 0 # "الكل" افتراضياً
    if "المشرف الأول" in filter_supervisor_options:
        default_filter_index = filter_supervisor_options.index("المشرف الأول")

    selected_supervisor_filter = st.selectbox(
        "🔍 اختر المشرف لتصفية المهام:",
        options=filter_supervisor_options,
        index=default_filter_index
    )

    if not daily_tasks.empty:
        if selected_supervisor_filter == "الكل":
            st.dataframe(daily_tasks[['التاريخ', 'المشرف', 'المهمة', 'ملاحظات']].style.set_properties(**{'text-align': 'right', 'font-size': '16px'}), hide_index=True)
        else:
            filtered_tasks = daily_tasks[daily_tasks["المشرف"] == selected_supervisor_filter]
            if not filtered_tasks.empty: 
                st.dataframe(filtered_tasks[['التاريخ', 'المشرف', 'المهمة', 'ملاحظات']].style.set_properties(**{'text-align': 'right', 'font-size': '16px'}), hide_index=True)
            else:
                st.info(f"لا توجد مهام للمشرف **{selected_supervisor_filter}** لهذا اليوم.")

    else:
        st.info("لا توجد مهام محددة لهذا اليوم حتى الآن. يرجى من المديرة إضافتها.")

    # عرض الجدول الأسبوعي
    st.subheader("جدول العمل الأسبوعي الحالي:")
    weekly_schedule_text = load_weekly_schedule()
    weekly_schedule_df = markdown_table_to_dataframe(weekly_schedule_text)
    
    if not weekly_schedule_df.empty:
        st.dataframe(weekly_schedule_df.style.set_properties(**{'text-align': 'right', 'font-size': '16px'}), hide_index=True)
    else:
        st.markdown(weekly_schedule_text)
        if weekly_schedule_text.strip() != "لا يوجد جدول أسبوعي حالياً. يرجى من المديرة إدخال الجدول.":
            st.warning("الجدول الأسبوعي المدخل ليس بتنسيق جدول Markdown صالح لعرضه كجدول بيانات. يرجى مراجعة التنسيق.")

    # عرض جدول دوام الموظفين اليومي
    st.subheader("👥 جدول دوام الموظفين اليومي:")
    daily_staff_schedule_text = load_daily_staff_schedule()
    daily_staff_schedule_df = markdown_table_to_dataframe(daily_staff_schedule_text)
    
    if not daily_staff_schedule_df.empty:
        st.dataframe(daily_staff_schedule_df.style.set_properties(**{'text-align': 'right', 'font-size': '16px'}), hide_index=True)
    else:
        st.markdown(daily_staff_schedule_text)
        if daily_staff_schedule_text.strip() != "لا يوجد جدول دوام يومي حالياً. يرجى من المديرة إدخال الجدول.":
            st.warning("جدول الدوام اليومي المدخل ليس بتنسيق جدول Markdown صالح لعرضه كجدول بيانات. يرجى مراجعة التنسيق.")


# استدعاء الدالة لتشغيل الصفحة
run()
    
