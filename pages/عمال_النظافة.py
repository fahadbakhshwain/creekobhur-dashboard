import streamlit as st
import pandas as pd
import datetime
import os

# اسم الملف لحفظ بيانات عمال النظافة
CLEANING_STAFF_DATA_FILE = "cleaning_staff_daily_data.csv"

# دالة لتحميل بيانات عمال النظافة
def load_cleaning_staff_data():
    if os.path.exists(CLEANING_STAFF_DATA_FILE):
        try:
            expected_columns = [
                "التاريخ", "المشرف_المسجل", "اسم_العامل", "وقت_الحضور", 
                "حالة_الحضور", "المنطقة_المخصصة", "المهام_الموكلة", 
                "حالة_المهام", "ملاحظات"
            ]
            df = pd.read_csv(CLEANING_STAFF_DATA_FILE)
            for col in expected_columns:
                if col not in df.columns:
                    df[col] = "" 
            return df[expected_columns]
        except pd.errors.EmptyDataError:
            return pd.DataFrame(columns=expected_columns)
    return pd.DataFrame(columns=expected_columns)

# دالة لحفظ بيانات عمال النظافة
def save_cleaning_staff_data(df):
    df.to_csv(CLEANING_STAFF_DATA_FILE, index=False)

def run():
    st.title("🧹 إدارة عمال النظافة")
    st.info("هنا يتم تسجيل حضور عمال النظافة، توزيع المهام، ومتابعة الإنجاز.")

    # المشرفون المسؤولون عن عمال النظافة
    cleaning_supervisors = ["مشرف النظافة الأول", "مشرف النظافة الثاني", "مشرف عام"]
    
    # قائمة بأسماء عمال النظافة (لتبسيط الإدخال في البروتوتايب)
    # يمكن تحديثها يدوياً أو سحبها من قائمة مركزية مستقبلاً
    cleaning_staff_names = [
        "عامل نظافة 1", "عامل نظافة 2", "عامل نظافة 3", "عاملة نظافة 1", 
        "عاملة نظافة 2", "عامل نظافة 4", "عامل نظافة 5"
    ]

    # المناطق التي يمكن تعيين المهام لها
    cleaning_areas = [
        "الشاطئ الكبير", "الشاطئ الصغير", "كوكيان", "جميع دورات المياه", 
        "ميدان السمكة", "مناطق الألعاب", "الساحة الكبيرة", "الممرات"
    ]

    st.header("تسجيل حضور وتوزيع مهام عمال النظافة")
    with st.form("cleaning_staff_form", clear_on_submit=True):
        entry_date = st.date_input("تاريخ التسجيل:", datetime.date.today())
        recording_supervisor = st.selectbox("المشرف المسؤول عن التسجيل:", cleaning_supervisors, key="recording_supervisor_select")
        
        # اختيار العامل
        selected_staff_name = st.selectbox("اسم العامل:", cleaning_staff_names, key="selected_staff_name_select")
        
        col1, col2 = st.columns(2)
        with col1:
            attendance_status = st.radio("حالة الحضور:", ["حاضر", "غائب", "تأخير"], key="attendance_status_radio")
            check_in_time = st.time_input("وقت الحضور المسجل:", datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=3))).time(), key="check_in_time_input")
        
        with col2:
            assigned_area = st.selectbox("المنطقة المخصصة للعمل:", cleaning_areas, key="assigned_area_select")
            assigned_tasks = st.text_area("المهام الموكلة (مثل: تنظيف دورة مياه 5، كنس الشاطئ الكبير):", height=100, key="assigned_tasks_text")
            task_status = st.selectbox("حالة إنجاز المهام:", ["قيد التنفيذ", "تم الإنجاز", "لم يتم البدء", "مشكلة"], key="task_status_select")
        
        general_notes = st.text_area("ملاحظات عامة حول العامل/أداء النظافة:", height=100, key="general_notes_text")

        submitted = st.form_submit_button("تسجيل بيانات عامل النظافة")
        if submitted:
            if not selected_staff_name.strip() or not assigned_tasks.strip():
                st.error("الرجاء اختيار اسم العامل وإدخال المهام الموكلة.")
            else:
                new_entry = pd.DataFrame([{
                    "التاريخ": entry_date.isoformat(),
                    "المشرف_المسجل": recording_supervisor,
                    "اسم_العامل": selected_staff_name,
                    "وقت_الحضور": check_in_time.strftime("%H:%M"),
                    "حالة_الحضور": attendance_status,
                    "المنطقة_المخصصة": assigned_area,
                    "المهام_الموكلة": assigned_tasks,
                    "حالة_المهام": task_status,
                    "ملاحظات": general_notes
                }])
                
                all_data = load_cleaning_staff_data()
                if all_data.empty:
                    updated_data = new_entry
                else:
                    updated_data = pd.concat([all_data, new_entry], ignore_index=True)
                save_cleaning_staff_data(updated_data)
                st.success(f"✅ تم تسجيل بيانات العامل {selected_staff_name} بنجاح!")
                st.rerun()

    # قسم عرض ملخص عمال النظافة اليومي
    st.header("📊 ملخص عمال النظافة اليومي")
    current_day_data = load_cleaning_staff_data()
    today_date_str = datetime.date.today().isoformat()
    daily_records = current_day_data[current_day_data["التاريخ"] == today_date_str]

    if not daily_records.empty:
        st.subheader("إجمالي عدد العمال الحاضرين:")
        present_workers_count = daily_records[daily_records["حالة_الحضور"] == "حاضر"].shape[0]
        st.metric("عدد عمال النظافة الحاضرين", present_workers_count)

        st.subheader("توزيع المهام وحالة الإنجاز اليومية:")
        # عرض المهام الموكلة وحالة إنجازها
        st.dataframe(daily_records[['اسم_العامل', 'المنطقة_المخصصة', 'المهام_الموكلة', 'حالة_المهام', 'ملاحظات']].style.set_properties(**{'text-align': 'right', 'font-size': '14px'}), use_container_width=True, hide_index=True)

        st.subheader("حالات تحتاج متابعة (غياب، مشاكل مهام):")
        # فلترة الحالات التي تحتاج متابعة
        attention_needed = daily_records[
            (daily_records["حالة_الحضور"] != "حاضر") | 
            (daily_records["حالة_المهام"] == "لم يتم البدء") | 
            (daily_records["حالة_المهام"] == "مشكلة")
        ]
        if not attention_needed.empty:
            for index, row in attention_needed.iterrows():
                status_color = "red" if row['حالة_الحضور'] in ["غائب"] or row['حالة_المهام'] == "مشكلة" else "orange"
                st.markdown(f"**- <span style='color: {status_color};'>{row['اسم_العامل']} ({row['المنطقة_المخصصة']}):</span>** الحضور: **{row['حالة_الحضور']}** - المهام: **{row['حالة_المهام']}** - ملاحظات: {row['ملاحظات']}", unsafe_allow_html=True)
                st.markdown("---")
        else:
            st.success("🎉 جميع عمال النظافة حاضرون ومهامهم تسير بشكل جيد اليوم.")
            
    else:
        st.info("لا توجد بيانات مسجلة لعمال النظافة لهذا اليوم حتى الآن.")

# استدعاء الدالة لتشغيل الصفحة
run()
