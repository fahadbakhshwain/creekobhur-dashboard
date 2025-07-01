import streamlit as st
import pandas as pd
import datetime
import os

# اسم الملف لحفظ بيانات الموارد البشرية (متابعة الحضور والإجازات)
HR_DATA_FILE = "hr_daily_records.csv"
LEAVE_REQUESTS_FILE = "leave_requests.csv" # ملف خاص بطلبات الإجازات
CIRCULARS_FILE = "hr_circulars.csv" # ملف خاص بالتعاميم

# --- دوال تحميل وحفظ البيانات ---

# دالة لتحميل بيانات الموارد البشرية (الحضور)
def load_hr_data():
    expected_cols = [
        "التاريخ", "اسم_الموظف", "القسم_الوظيفة", "حالة_الحضور", 
        "وقت_الحضور", "وقت_المغادرة", "ملاحظات_خاصة"
    ]
    if os.path.exists(HR_DATA_FILE):
        try:
            df = pd.read_csv(HR_DATA_FILE)
            for col in expected_cols:
                if col not in df.columns:
                    df[col] = "" 
            return df[expected_cols]
        except pd.errors.EmptyDataError:
            return pd.DataFrame(columns=expected_cols)
    return pd.DataFrame(columns=expected_cols)

# دالة لحفظ بيانات الموارد البشرية (الحضور)
def save_hr_data(df):
    df.to_csv(HR_DATA_FILE, index=False)

# دالة لتحميل طلبات الإجازات
def load_leave_requests():
    expected_cols = [
        "تاريخ_الطلب", "اسم_الموظف", "القسم_الوظيفة", "نوع_الإجازة", 
        "تاريخ_البداية", "تاريخ_النهاية", "المدة_بالأيام", "سبب_الإجازة", 
        "حالة_الطلب" 
    ]
    if os.path.exists(LEAVE_REQUESTS_FILE):
        try:
            df = pd.read_csv(LEAVE_REQUESTS_FILE)
            for col in expected_cols:
                if col not in df.columns:
                    df[col] = "" 
            return df[expected_cols]
        except pd.errors.EmptyDataError:
            return pd.DataFrame(columns=expected_cols)
    return pd.DataFrame(columns=expected_cols)

# دالة لحفظ طلبات الإجازات
def save_leave_requests(df):
    df.to_csv(LEAVE_REQUESTS_FILE, index=False)

# دالة لتحميل التعاميم
def load_circulars():
    expected_cols = [
        "تاريخ_النشر", "عنوان_التعميم", "محتوى_التعميم", 
        "تاريخ_الانتهاء", "الناشر"
    ]
    if os.path.exists(CIRCULARS_FILE):
        try:
            df = pd.read_csv(CIRCULARS_FILE)
            for col in expected_cols:
                if col not in df.columns:
                    df[col] = "" 
            return df[expected_cols]
        except pd.errors.EmptyDataError:
            return pd.DataFrame(columns=expected_cols)
    return pd.DataFrame(columns=expected_cols)

# دالة لحفظ التعاميم
def save_circulars(df):
    df.to_csv(CIRCULARS_FILE, index=False)


def run():
    st.title("👥 إدارة الموارد البشرية (المتابعة الميدانية)")
    st.info("هنا يتم متابعة حضور الموظفين، تسجيل الحالات الخاصة، طلبات الإجازات، ونشر التعاميم.")

    # قوائم اختيار للموظفين والأقسام
    all_employees = ["أحمد علي", "فاطمة محمد", "سارة خالد", "خالد يوسف", "ليلى سعيد"] 
    all_departments = ["إدارة", "تشغيل", "صيانة", "أمن", "نظافة", "سائقون", "زراعة", "كاشيرات", "منقذون"]
    hr_publishers = ["مدير الموارد البشرية", "مساعد الموارد البشرية"]

    # --- قسم تسجيل حضور الموظفين ---
    st.header("تسجيل حضور الموظفين اليومي")
    with st.form("daily_attendance_form", clear_on_submit=True):
        entry_date = st.date_input("تاريخ اليوم:", datetime.date.today())
        
        employee_name_attendance = st.selectbox("اسم الموظف:", all_employees, key="emp_name_attendance")
        employee_dept_attendance = st.selectbox("القسم/الوظيفة:", all_departments, key="emp_dept_attendance")
        
        col1, col2 = st.columns(2)
        with col1:
            attendance_status = st.radio("حالة الحضور:", ["حاضر", "غائب", "تأخير"], key="attendance_status_radio")
            check_in_time = st.time_input("وقت الحضور:", datetime.time(8, 0), key="check_in_time_input")
        with col2:
            check_out_time = st.time_input("وقت المغادرة:", datetime.time(16, 0), key="check_out_time_input")
            
        attendance_notes = st.text_area("ملاحظات (مثلاً: سبب الغياب، التأخير):", key="attendance_notes_text")
        
        submitted_attendance = st.form_submit_button("تسجيل الحضور")
        if submitted_attendance:
            if not employee_name_attendance.strip():
                st.error("الرجاء اختيار اسم الموظف.")
            else:
                new_entry = pd.DataFrame([{
                    "التاريخ": entry_date.isoformat(),
                    "اسم_الموظف": employee_name_attendance,
                    "القسم_الوظيفة": employee_dept_attendance,
                    "حالة_الحضور": attendance_status,
                    "وقت_الحضور": check_in_time.strftime("%H:%M"),
                    "وقت_المغادرة": check_out_time.strftime("%H:%M"),
                    "ملاحظات_خاصة": attendance_notes
                }])
                all_data = load_hr_data()
                if all_data.empty: updated_data = new_entry
                else: updated_data = pd.concat([all_data, new_entry], ignore_index=True)
                save_hr_data(updated_data)
                st.success(f"✅ تم تسجيل حضور {employee_name_attendance} بنجاح!")
                st.rerun()

    # --- قسم تقديم طلب إجازة ---
    st.header("تقديم طلب إجازة")
    with st.form("leave_request_form", clear_on_submit=True):
        request_date = st.date_input("تاريخ تقديم الطلب:", datetime.date.today())
        
        employee_name_leave = st.selectbox("اسم الموظف طالب الإجازة:", all_employees, key="emp_name_leave")
        employee_dept_leave = st.selectbox("القسم/الوظيفة:", all_departments, key="emp_dept_leave")
        
        leave_type = st.selectbox("نوع الإجازة:", ["سنوية", "مرضية", "طارئة", "بدون أجر"], key="leave_type_select")
        
        col_leave1, col_leave2 = st.columns(2)
        with col_leave1:
            start_date = st.date_input("تاريخ بداية الإجازة:", datetime.date.today(), key="start_date_input")
        with col_leave2:
            end_date = st.date_input("تاريخ نهاية الإجازة:", datetime.date.today() + datetime.timedelta(days=7), key="end_date_input")
        
        duration_days = (end_date - start_date).days + 1
        st.write(f"المدة التقديرية للإجازة: **{duration_days}** أيام.")
        
        leave_reason = st.text_area("سبب الإجازة:", key="leave_reason_text")
        
        submitted_leave = st.form_submit_button("إرسال طلب الإجازة")
        if submitted_leave:
            if not leave_reason.strip() or duration_days <= 0:
                st.error("الرجاء إدخال سبب الإجازة وتواريخ صحيحة.")
            else:
                new_request = pd.DataFrame([{
                    "تاريخ_الطلب": request_date.isoformat(),
                    "اسم_الموظف": employee_name_leave,
                    "القسم_الوظيفة": employee_dept_leave,
                    "نوع_الإجازة": leave_type,
                    "تاريخ_البداية": start_date.isoformat(),
                    "تاريخ_النهاية": end_date.isoformat(),
                    "المدة_بالأيام": duration_days,
                    "سبب_الإجازة": leave_reason,
                    "حالة_الطلب": "جديد" 
                }])
                all_requests = load_leave_requests()
                if all_requests.empty: updated_requests = new_request
                else: updated_requests = pd.concat([all_requests, new_request], ignore_index=True)
                save_leave_requests(updated_requests)
                st.success(f"✅ تم إرسال طلب إجازة {employee_name_leave} بنجاح! سيتم مراجعته.")
                st.rerun()

    # --- قسم نشر التعاميم ---
    st.header("نشر تعميم جديد")
    with st.form("new_circular_form", clear_on_submit=True):
        publish_date = st.date_input("تاريخ النشر:", datetime.date.today(), key="circular_publish_date")
        circular_title = st.text_input("عنوان التعميم:", key="circular_title_input")
        circular_content = st.text_area("محتوى التعميم:", height=200, key="circular_content_text")
        expiry_date = st.date_input("تاريخ انتهاء التعميم (اختياري):", value=None, key="circular_expiry_date")
        publisher_name = st.selectbox("الناشر:", hr_publishers, key="circular_publisher_select")

        submitted_circular = st.form_submit_button("نشر التعميم")
        if submitted_circular:
            if not circular_title.strip() or not circular_content.strip():
                st.error("الرجاء إدخال عنوان ومحتوى التعميم.")
            else:
                new_circular = pd.DataFrame([{
                    "تاريخ_النشر": publish_date.isoformat(),
                    "عنوان_التعميم": circular_title,
                    "محتوى_التعميم": circular_content,
                    "تاريخ_الانتهاء": expiry_date.isoformat() if expiry_date else "",
                    "الناشر": publisher_name
                }])
                all_circulars = load_circulars()
                if all_circulars.empty: updated_circulars = new_circular
                else: updated_circulars = pd.concat([all_circulars, new_circular], ignore_index=True)
                save_circulars(updated_circulars)
                st.success("✅ تم نشر التعميم بنجاح!")
                st.rerun()

    # --- قسم عرض ملخص الموارد البشرية ---
    st.header("📊 ملخص الموارد البشرية اليومي")

    # ملخص الحضور والغياب لليوم
    st.subheader("حالات حضور الموظفين لليوم:")
    daily_attendance_df = load_hr_data()
    today_attendance = daily_attendance_df[daily_attendance_df["التاريخ"] == datetime.date.today().isoformat()]
    
    if not today_attendance.empty:
        total_present = today_attendance[today_attendance["حالة_الحضور"] == "حاضر"].shape[0]
        total_absent = today_attendance[today_attendance["حالة_الحضور"] == "غائب"].shape[0]
        total_late = today_attendance[today_attendance["حالة_الحضور"] == "تأخير"].shape[0]

        col_hr1, col_hr2, col_hr3 = st.columns(3)
        col_hr1.metric("حاضرون", total_present)
        col_hr2.metric("غائبون", total_absent)
        col_hr3.metric("متأخرون", total_late)
        
        st.dataframe(today_attendance[['اسم_الموظف', 'القسم_الوظيفة', 'حالة_الحضور', 'وقت_الحضور', 'ملاحظات_خاصة']].style.set_properties(**{'text-align': 'right', 'font-size': '14px'}), use_container_width=True, hide_index=True)
    else:
        st.info("لا توجد بيانات حضور مسجلة لهذا اليوم حتى الآن.")

    # ملخص طلبات الإجازات
    st.subheader("طلبات الإجازات (بانتظار المراجعة):")
    all_leave_requests = load_leave_requests()
    pending_requests = all_leave_requests[all_leave_requests["حالة_الطلب"] == "جديد"]

    if not pending_requests.empty:
        st.dataframe(pending_requests[['تاريخ_الطلب', 'اسم_الموظف', 'القسم_الوظيفة', 'نوع_الإجازة', 'تاريخ_البداية', 'تاريخ_النهاية', 'المدة_بالأيام', 'سبب_الإجازة', 'حالة_الطلب']].style.set_properties(**{'text-align': 'right', 'font-size': '14px'}), use_container_width=True, hide_index=True)
        
        st.markdown("---")
        st.subheader("تحديث حالة طلبات الإجازات:")
        editable_requests = all_leave_requests.copy()
        
        edited_requests_df = st.data_editor(
            editable_requests,
            column_config={
                "حالة_الطلب": st.column_config.SelectboxColumn(
                    "حالة الطلب", options=["جديد", "قيد المراجعة", "تمت الموافقة", "مرفوض"], required=True
                ),
                "تاريخ_الطلب": st.column_config.Column("تاريخ الطلب", disabled=True),
                "اسم_الموظف": st.column_config.Column("الموظف", disabled=True),
                "القسم_الوظيفة": st.column_config.Column("القسم", disabled=True),
                "نوع_الإجازة": st.column_config.Column("النوع", disabled=True),
                "تاريخ_البداية": st.column_config.Column("البداية", disabled=True),
                "تاريخ_النهاية": st.column_config.Column("النهاية", disabled=True),
                "المدة_بالأيام": st.column_config.Column("المدة (أيام)", disabled=True),
                "سبب_الإجازة": st.column_config.Column("السبب", disabled=True),
            },
            hide_index=True,
            use_container_width=True,
            num_rows="dynamic"
        )
        
        if st.button("حفظ تحديثات طلبات الإجازات", key="save_leave_updates"):
            save_leave_requests(edited_requests_df)
            st.success("✅ تم حفظ تحديثات طلبات الإجازات بنجاح!")
            st.rerun()

    else:
        st.info("لا توجد طلبات إجازات جديدة بانتظار المراجعة حالياً.")

    # --- عرض التعاميم النشطة ---
    st.subheader("التعاميم النشطة حالياً:")
    all_circulars_df = load_circulars()
    
    # فلترة التعاميم النشطة (تاريخ النشر <= اليوم و تاريخ الانتهاء >= اليوم أو فارغ)
    active_circulars = all_circulars_df[
        (pd.to_datetime(all_circulars_df["تاريخ_النشر"]) <= datetime.date.today().isoformat()) &
        (
            (pd.to_datetime(all_circulars_df["تاريخ_الانتهاء"], errors='coerce').isna()) | # تاريخ الانتهاء فارغ
            (pd.to_datetime(all_circulars_df["تاريخ_الانتهاء"], errors='coerce') >= datetime.date.today().isoformat())
        )
    ]
    
    if not active_circulars.empty:
        # عرض التعاميم بترتيب تنازلي حسب تاريخ النشر
        active_circulars = active_circulars.sort_values(by="تاريخ_النشر", ascending=False)
        for index, circular in active_circulars.iterrows():
            st.markdown(f"### 📢 {circular['عنوان_التعميم']}")
            st.markdown(f"**تاريخ النشر:** {circular['تاريخ_النشر']} | **الناشر:** {circular['الناشر']}")
            if circular['تاريخ_الانتهاء']:
                st.markdown(f"**تاريخ الانتهاء:** {circular['تاريخ_الانتهاء']}")
            st.write(circular['محتوى_التعميم'])
            st.markdown("---")
    else:
        st.info("لا توجد تعاميم نشطة حالياً.")

# استدعاء الدالة لتشغيل الصفحة
run()
