import streamlit as st
import pandas as pd
import datetime
import os

# اسم الملف لحفظ بيانات مهام مساعدة المديرة
ASSISTANT_TASKS_FILE = "assistant_tasks_data.csv"

# دالة لتحميل بيانات مهام مساعدة المديرة
def load_assistant_tasks():
    # تعريف الأعمدة المتوقعة هنا لتكون متاحة دائماً
    expected_columns = [
        "التاريخ", "وقت_التكليف", "الوصف", "الحالة", 
        "الموعد_النهائي", "الملاحظات_الإدارية"
    ]
    if os.path.exists(ASSISTANT_TASKS_FILE):
        try:
            df = pd.read_csv(ASSISTANT_TASKS_FILE)
            for col in expected_columns:
                if col not in df.columns:
                    df[col] = "" 
            return df[expected_columns]
        except pd.errors.EmptyDataError:
            return pd.DataFrame(columns=expected_columns)
    return pd.DataFrame(columns=expected_columns)

# دالة لحفظ بيانات مهام مساعدة المديرة
def save_assistant_tasks(df):
    df.to_csv(ASSISTANT_TASKS_FILE, index=False)

def run():
    st.title("👩‍💼 مهام مساعدة المديرة")
    st.info("هنا يتم تسجيل ومتابعة المهام الخاصة الموكلة لمساعدة المديرة.")

    st.header("تسجيل مهمة جديدة لمساعدة المديرة")
    with st.form("assistant_task_form", clear_on_submit=True):
        task_date = st.date_input("تاريخ التكليف:", datetime.date.today())
        task_time = st.time_input("وقت التكليف:", datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=3))).time())
        
        task_description = st.text_area("وصف المهمة المطلوبة:", height=150, key="task_description_input")
        
        task_status = st.selectbox("حالة المهمة:", ["قيد التنفيذ", "تم الإنجاز", "معلقة", "تحتاج مراجعة"], key="task_status_select")
        
        due_date = st.date_input("الموعد النهائي (اختياري):", value=None, key="due_date_input")
        
        admin_notes = st.text_area("ملاحظات إضافية (خاصة بالمديرة/المساعد):", height=100, key="admin_notes_text")

        submitted = st.form_submit_button("تسجيل المهمة")
        if submitted:
            if not task_description.strip():
                st.error("الرجاء إدخال وصف للمهمة.")
            else:
                new_entry = pd.DataFrame([{
                    "التاريخ": task_date.isoformat(),
                    "وقت_التكليف": task_time.strftime("%H:%M"),
                    "الوصف": task_description,
                    "الحالة": task_status,
                    "الموعد_النهائي": due_date.isoformat() if due_date else "", # حفظ التاريخ إذا تم اختياره
                    "الملاحظات_الإدارية": admin_notes
                }])
                
                all_data = load_assistant_tasks()
                if all_data.empty:
                    updated_data = new_entry
                else:
                    updated_data = pd.concat([all_data, new_entry], ignore_index=True)
                save_assistant_tasks(updated_data)
                st.success("✅ تم تسجيل المهمة بنجاح!")
                st.rerun()

    # قسم عرض ملخص مهام مساعدة المديرة
    st.header("📊 ملخص المهام الموكلة")
    current_day_data = load_assistant_tasks()
    today_date_str = datetime.date.today().isoformat()
    
    # فلترة المهام المعلقة أو قيد التنفيذ فقط لليوم
    pending_or_in_progress_tasks = current_day_data[
        (current_day_data["الحالة"].isin(["قيد التنفيذ", "معلقة", "تحتاج مراجعة"]))
    ]

    if not pending_or_in_progress_tasks.empty:
        st.subheader("المهام المعلقة أو قيد التنفيذ:")
        for index, row in pending_or_in_progress_tasks.iterrows():
            status_color = "red" if row['الحالة'] == 'معلقة' else "orange" if row['الحالة'] == 'قيد التنفيذ' or row['الحالة'] == 'تحتاج مراجعة' else "green"
            st.markdown(f"**- <span style='color: {status_color};'>المهمة: {row['الوصف']}</span>**", unsafe_allow_html=True)
            st.markdown(f"**الحالة:** {row['الحالة']}")
            if row['الموعد_النهائي']:
                st.markdown(f"**الموعد النهائي:** {row['الموعد_النهائي']}")
            if row['الملاحظات_الإدارية']:
                st.info(f"**ملاحظات:** {row['الملاحظات_الإدارية']}")
            st.markdown("---")
        
        st.subheader("جميع المهام المسجلة:")
        st.dataframe(current_day_data[['التاريخ', 'وقت_التكليف', 'الوصف', 'الحالة', 'الموعد_النهائي', 'الملاحظات_الإدارية']].style.set_properties(**{'text-align': 'right', 'font-size': '14px'}), use_container_width=True, hide_index=True)
            
    else:
        st.info("لا توجد مهام معلقة أو قيد التنفيذ حالياً لمساعدة المديرة. كل شيء تم إنجازه!")

# استدعاء الدالة لتشغيل الصفحة
run()
