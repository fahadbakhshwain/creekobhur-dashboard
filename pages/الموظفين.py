import streamlit as st
import pandas as pd
import datetime
import os

# اسم الملف لحفظ بيانات الموظفين اليومية
STAFF_DAILY_DATA_FILE = "staff_daily_records.csv"

# دالة لتحميل بيانات الموظفين
def load_staff_data():
    # تعريف الأعمدة المتوقعة هنا لتكون متاحة دائماً
    expected_columns = [
        "التاريخ", "المسؤول_المسجل", "اسم_الموظف", "القسم_الوظيفة", 
        "حالة_الحضور", "وقت_الحضور_المسجل", "وقت_المغادرة_المسجل",
        "ملاحظات_خاصة", "تقييم_مبدئي_للأداء"
    ]
    if os.path.exists(STAFF_DAILY_DATA_FILE):
        try:
            df = pd.read_csv(STAFF_DAILY_DATA_FILE)
            for col in expected_columns:
                if col not in df.columns:
                    df[col] = "" 
            return df[expected_columns]
        except pd.errors.EmptyDataError:
            return pd.DataFrame(columns=expected_columns)
    return pd.DataFrame(columns=expected_columns)

# دالة لحفظ بيانات الموظفين
def save_staff_data(df):
    df.to_csv(STAFF_DAILY_DATA_FILE, index=False)

def run():
    st.title("🧑‍🤝‍🧑 إدارة الموظفين (المتابعة اليومية)")
    st.info("هنا يتم تسجيل ومتابعة حضور الموظفين الميدانيين اليومي وحالاتهم الخاصة.")

    # قائمة المشرفين الذين يسجلون البيانات
    recording_supervisors = ["المشرف الأول", "المشرف الثاني", "المشرف الثالث"]
    
    # قائمة بالأقسام/الوظائف المتاحة
    job_roles = ["مشرف", "كاشير", "منقذ", "حارس أمن", "عامل نظافة", "سائق باص", "فني صيانة", "عامل زراعة", "إدارة"]

    st.header("تسجيل حضور وحالات الموظفين اليومية")
    with st.form("staff_daily_form", clear_on_submit=True):
        entry_date = st.date_input("تاريخ التسجيل:", datetime.date.today())
        recorder_name = st.selectbox("المسؤول عن التسجيل:", recording_supervisors, key="recorder_name_select")
        
        col1, col2 = st.columns(2)
        with col1:
            staff_name = st.text_input("اسم الموظف:", key="staff_name_input")
            staff_role = st.selectbox("القسم/الوظيفة:", job_roles, key="staff_role_select")
            attendance_status = st.radio("حالة الحضور:", ["حاضر", "غائب", "تأخير", "إجازة (مسجلة مسبقاً)"], key="attendance_status_radio")
        
        with col2:
            check_in_time = st.time_input("وقت الحضور المسجل (إن أمكن):", datetime.time(8, 0), key="check_in_time_input")
            check_out_time = st.time_input("وقت المغادرة المسجل (إن أمكن):", datetime.time(16, 0), key="check_out_time_input")
            
            # تقييم مبدئي للأداء (اختياري)
            performance_rating = st.selectbox("تقييم مبدئي للأداء (لليوم/الملاحظة):", ["ممتاز", "جيد جداً", "جيد", "مقبول", "ضعيف"], index=2, key="performance_rating_select")
        
        special_notes = st.text_area("ملاحظات خاصة (مثل سبب التأخير، مشكلة سلوكية، أداء مميز):", height=100, key="special_notes_text")

        submitted = st.form_submit_button("تسجيل حالة الموظف")
        if submitted:
            if not staff_name.strip() or not staff_role.strip():
                st.error("الرجاء إدخال اسم الموظف والقسم/الوظيفة.")
            else:
                new_entry = pd.DataFrame([{
                    "التاريخ": entry_date.isoformat(),
                    "المسؤول_المسجل": recorder_name,
                    "اسم_الموظف": staff_name,
                    "القسم_الوظيفة": staff_role,
                    "حالة_الحضور": attendance_status,
                    "وقت_الحضور_المسجل": check_in_time.strftime("%H:%M"),
                    "وقت_المغادرة_المسجل": check_out_time.strftime("%H:%M"),
                    "ملاحظات_خاصة": special_notes,
                    "تقييم_مبدئي_للأداء": performance_rating
                }])
                
                all_data = load_staff_data()
                if all_data.empty:
                    updated_data = new_entry
                else:
                    updated_data = pd.concat([all_data, new_entry], ignore_index=True)
                save_staff_data(updated_data)
                st.success(f"✅ تم تسجيل حالة الموظف {staff_name} بنجاح!")
                st.rerun()

    # قسم عرض ملخص الموظفين اليومي
    st.header("📊 ملخص الموظفين اليومي")
    current_day_data = load_staff_data()
    today_date_str = datetime.date.today().isoformat()
    daily_records = current_day_data[current_day_data["التاريخ"] == today_date_str]

    if not daily_records.empty:
        st.subheader("عدد الموظفين المتواجدين اليوم حسب القسم:")
        # تلخيص عدد الحاضرين لكل قسم
        present_staff_summary = daily_records[daily_records["حالة_الحضور"] == "حاضر"].groupby("القسم_الوظيفة").size().reset_index(name='عدد المتواجدين')
        if not present_staff_summary.empty:
            st.dataframe(present_staff_summary.style.set_properties(**{'text-align': 'right', 'font-size': '14px'}), hide_index=True)
        else:
            st.info("لا يوجد موظفون حاضرون مسجلون لهذا اليوم.")

        st.subheader("حالات الحضور والغياب والملاحظات الخاصة اليومية:")
        # عرض جميع سجلات الحضور/الغياب
        st.dataframe(daily_records[['اسم_الموظف', 'القسم_الوظيفة', 'حالة_الحضور', 'وقت_الحضور_المسجل', 'وقت_المغادرة_المسجل', 'ملاحظات_خاصة', 'تقييم_مبدئي_للأداء']].style.set_properties(**{'text-align': 'right', 'font-size': '14px'}), use_container_width=True, hide_index=True)

        st.subheader("الموظفون الذين يحتاجون متابعة (تأخير، غياب، ملاحظات خاصة):")
        # فلترة الموظفين الذين حالتهم ليست "حاضر" أو لديهم ملاحظات خاصة
        attention_needed_staff = daily_records[
            (daily_records["حالة_الحضور"] != "حاضر") | (daily_records["ملاحظات_خاصة"].str.strip() != "")
        ]
        if not attention_needed_staff.empty:
            for index, row in attention_needed_staff.iterrows():
                status_color = "red" if row['حالة_الحضور'] in ["غائب", "تأخير"] else "orange"
                st.markdown(f"**- <span style='color: {status_color};'>{row['اسم_الموظف']} ({row['القسم_الوظيفة']}):</span>** الحالة: **{row['حالة_الحضور']}** - ملاحظات: **{row['ملاحظات_خاصة'] if row['ملاحظات_خاصة'] else 'لا توجد ملاحظات'}**", unsafe_allow_html=True)
                st.markdown("---")
        else:
            st.success("🎉 جميع الموظفين المتواجدين حاضرون ولا توجد ملاحظات خاصة اليوم.")
            
    else:
        st.info("لا توجد بيانات موظفين مسجلة لهذا اليوم حتى الآن.")

# استدعاء الدالة لتشغيل الصفحة
run()
   
