import streamlit as st
import pandas as pd
import datetime
import os
import io # لإدارة سلاسل الإدخال/الإخراج النصية

# اسم الملف لحفظ المهام
TASKS_FILE = "tasks.csv"
SCHEDULE_FILE = "weekly_schedule.txt" # لجدول العمل الأسبوعي

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

# دالة لتحويل نص Markdown Table إلى DataFrame
def markdown_table_to_dataframe(markdown_text):
    lines = markdown_text.strip().split('\n')
    if len(lines) < 2: # على الأقل سطرين: رؤوس الأعمدة وفاصل
        return pd.DataFrame() # إرجاع DataFrame فارغ إذا لم يكن جدولاً صالحاً

    # رؤوس الأعمدة
    header = [h.strip() for h in lines[0].strip('|').split('|')]
    
    # تحقق من وجود خط الفاصل (مثل ---|---|---)
    if len(lines) > 1 and all(c in ['-', '|', ' ', ':'] for c in lines[1].strip()):
        data_lines = lines[2:] # تبدأ البيانات من السطر الثالث
    else:
        # إذا لم يكن هناك خط فاصل، افترض أن السطر الثاني هو أول صف بيانات
        data_lines = lines[1:]

    data = []
    for line in data_lines:
        if line.strip(): # تجاهل الأسطر الفارغة
            row = [item.strip() for item in line.strip('|').split('|')]
            # تأكد من أن عدد العناصر في الصف يطابق عدد الأعمدة
            if len(row) == len(header):
                data.append(row)
            else:
                st.warning(f"تم تجاهل صف غير متطابق في الجدول الأسبوعي: {line}")

    return pd.DataFrame(data, columns=header) if data else pd.DataFrame(columns=header)


def run():
    st.title("📋 المهام اليومية")
    st.info("هنا يتم تسجيل وتتبع المهام اليومية والجدول الأسبوعي.")

    # قسم المديرة: لإدخال المهام والجدول الأسبوعي
    st.header("إدارة المهام والجدول (للمديرة)")
    with st.expander("إضافة مهمة جديدة"):
        with st.form("new_task_form", clear_on_submit=True):
            current_date_jeddah = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=3))).date() 
            task_date = st.date_input("تاريخ المهمة:", current_date_jeddah)
            
            supervisor_options = ["المشرف الأول", "المشرف الثاني", "المشرف الثالث", "العمالة العامة", "فريق الصيانة", "المديرة"]
            supervisor = st.selectbox(
                "المشرف المسؤول:",
                supervisor_options,
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

    with st.expander("تحديث الجدول الأسبوعي"):
        st.markdown("**يرجى إدخال الجدول الأسبوعي بتنسيق Markdown للجدول (مثال بالأسفل):**")
        st.code("""
| اليوم | الوقت | المهمة | المسؤول |
|---|---|---|---|
| الثلاثاء | 08:00 ص | اجتماع إداري | المديرة |
| الثلاثاء | 09:00 ص | تفقد دورات المياه | المشرف الأول |
""", language='markdown') # مثال لتنسيق الجدول

        current_schedule_text = load_weekly_schedule()
        new_schedule_text = st.text_area("أدخل الجدول الأسبوعي هنا:", value=current_schedule_text, height=300)
        
        if st.button("حفظ الجدول الأسبوعي"):
            save_weekly_schedule(new_schedule_text)
            st.success("✅ تم حفظ الجدول الأسبوعي بنجاح!")
            st.rerun()

    # قسم عرض المهام (للمشرفين)
    st.header("عرض المهام اليومية والجدول الأسبوعي")

    st.subheader("🗓️ المهام المطلوبة لليوم:")
    all_tasks = load_tasks()
    
    current_date_jeddah = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=3))).date()
    today_date_str = current_date_jeddah.isoformat()

    daily_tasks = all_tasks[all_tasks["التاريخ"] == today_date_str]

    if not daily_tasks.empty:
        st.dataframe(daily_tasks[['التاريخ', 'المشرف', 'المهمة', 'ملاحظات']].style.set_properties(**{'text-align': 'right', 'font-size': '16px'}), hide_index=True)
        
        st.markdown("---") # فاصل مرئي
        st.subheader("🔍 تصفية المهام حسب المشرف:")
        available_supervisors = daily_tasks["المشرف"].unique().tolist()
        
        default_selection_index = 0
        if "المشرف الأول" in available_supervisors:
            default_selection_index = available_supervisors.index("المشرف الأول")
        elif available_supervisors: 
            default_selection_index = 0
        else: 
            available_supervisors = ["لا يوجد مشرفون لهذا اليوم"]
            default_selection_index = 0
            
        selected_supervisor_filter = st.selectbox(
            "🔍 اختر المشرف لتصفية المهام:",
            options=available_supervisors,
            index=default_selection_index
        )

        if selected_supervisor_filter == "لا يوجد مشرفون لهذا اليوم":
            st.info("لا توجد مهام حالياً لأي مشرفين.")
        else:
            filtered_tasks = daily_tasks[daily_tasks["المشرف"] == selected_supervisor_filter]
            st.dataframe(filtered_tasks[['التاريخ', 'المشرف', 'المهمة', 'ملاحظات']].style.set_properties(**{'text-align': 'right', 'font-size': '16px'}), hide_index=True)

    else:
        st.info("لا توجد مهام محددة لهذا اليوم حتى الآن. يرجى من المديرة إضافتها.")

    st.subheader("جدول العمل الأسبوعي الحالي:")
    # عرض الجدول الأسبوعي كـ DataFrame إذا كان بتنسيق Markdown صالح
    weekly_schedule_text = load_weekly_schedule()
    weekly_schedule_df = markdown_table_to_dataframe(weekly_schedule_text)
    
    if not weekly_schedule_df.empty:
        st.dataframe(weekly_schedule_df.style.set_properties(**{'text-align': 'right', 'font-size': '16px'}), hide_index=True)
    else:
        st.markdown(weekly_schedule_text) # إذا لم يكن جدولاً صالحاً، اعرضه كنص عادي
        st.warning("الجدول الأسبوعي المدخل ليس بتنسيق جدول Markdown صالح لعرضه كجدول بيانات. يرجى مراجعة التنسيق.")


# استدعاء الدالة لتشغيل الصفحة
run()
   
