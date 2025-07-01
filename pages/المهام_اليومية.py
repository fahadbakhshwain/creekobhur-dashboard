import streamlit as st
import pandas as pd
import datetime
import os
import io

# اسم الملف لحفظ المهام
TASKS_FILE = "tasks.csv"
SCHEDULE_FILE = "weekly_schedule.txt" # لجدول العمل الأسبوعي
DAILY_STAFF_SCHEDULE_CSV = "daily_staff_schedule.csv" # لحفظ جدول دوام الموظفين كـ CSV

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

# دالة لتحميل جدول دوام الموظفين اليومي من CSV
def load_daily_staff_schedule_df():
    if os.path.exists(DAILY_STAFF_SCHEDULE_CSV):
        try:
            return pd.read_csv(DAILY_STAFF_SCHEDULE_CSV)
        except pd.errors.EmptyDataError:
            return pd.DataFrame() # إرجاع DataFrame فارغ إذا كان الملف موجوداً وفارغاً
    return pd.DataFrame() # إرجاع DataFrame فارغ إذا كان الملف غير موجود

# دالة لحفظ جدول دوام الموظفين اليومي كـ CSV
def save_daily_staff_schedule_df(df):
    df.to_csv(DAILY_STAFF_SCHEDULE_CSV, index=False)

# دالة لتحويل نص Markdown Table إلى DataFrame (سنبقيها لدعم الجدول الأسبوعي)
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
    st.info("هنا يتم تسجيل وتتبع المهام اليومية والجدول الأسبوعي وجدول دوام الموظفين.")

    all_possible_supervisors = ["المشرف الأول", "المشرف الثاني", "المشرف الثالث", "العمالة العامة", "فريق الصيانة", "المديرة", "أمن"] 

    st.header("إدارة المهام والجداول (للمديرة)")

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

    # نموذج رفع وتحديث جدول دوام الموظفين اليومي
    with st.expander("⬆️ رفع وتحديث جدول دوام الموظفين اليومي"):
        st.markdown("**يرجى رفع ملف جدول الدوام (CSV أو Excel):**")
        uploaded_file = st.file_uploader(
            "اختر ملف CSV أو Excel", 
            type=["csv", "xlsx"], 
            key="daily_staff_schedule_uploader"
        )
        
        if uploaded_file is not None:
            try:
                # قراءة الملف حسب نوعه
                if uploaded_file.name.endswith('.csv'):
                    df_uploaded = pd.read_csv(uploaded_file)
                elif uploaded_file.name.endswith('.xlsx'):
                    df_uploaded = pd.read_excel(uploaded_file)
                
                st.write("تم تحميل الملف بنجاح. هذا هو محتوى الجدول:")
                st.dataframe(df_uploaded, use_container_width=True) # عرض لمحة عن الجدول المرفوع
                
                if st.button("تأكيد وحفظ جدول الدوام", key="confirm_save_daily_schedule_btn"):
                    save_daily_staff_schedule_df(df_uploaded)
                    st.success("✅ تم حفظ جدول الدوام اليومي بنجاح!")
                    st.rerun()
            except Exception as e:
                st.error(f"حدث خطأ أثناء قراءة الملف: {e}. يرجى التأكد من تنسيق الملف.")
                st.warning("تأكد أن الملف لا يحتوي على خلايا مدمجة أو تنسيقات معقدة.")


    # قسم عرض المهام والجداول (للمشرفين)
    st.header("عرض المهام اليومية والجداول")

    st.subheader("🗓️ المهام المطلوبة لليوم:")
    all_tasks = load_tasks()
    
    current_date_jeddah = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=3))).date()
    today_date_str = current_date_jeddah.isoformat()

    daily_tasks = all_tasks[all_tasks["التاريخ"] == today_date_str]

    filter_supervisor_options = ["الكل"] + all_possible_supervisors 

    default_filter_index = 0 
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
    st.subheader("📅 جدول العمل الأسبوعي الحالي:")
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
    daily_staff_schedule_df = load_daily_staff_schedule_df() # نستخدم الدالة الجديدة هنا
    
    if not daily_staff_schedule_df.empty:
        # هنا نستخدم expander للتوسع و use_container_width لجعل الجدول يملأ العرض
        with st.expander("اضغط لعرض جدول الدوام كاملاً"):
            st.dataframe(daily_staff_schedule_df.style.set_properties(**{'text-align': 'right', 'font-size': '16px'}), use_container_width=True, hide_index=True)
    else:
        st.info("لا يوجد جدول دوام يومي لعرضه حالياً. يرجى رفعه من قسم الإدارة.")


# استدعاء الدالة لتشغيل الصفحة
run()
       
      

   
   
    

    
        
