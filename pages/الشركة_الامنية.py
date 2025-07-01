import streamlit as st
import pandas as pd
import datetime
import os

# اسم الملف لحفظ بيانات السائقين والباصات
DRIVERS_DATA_FILE = "drivers_and_buses_data.csv" # تم تغيير اسم الملف ليعكس المحتوى

# دالة لتحميل بيانات السائقين والباصات
def load_drivers_data():
    if os.path.exists(DRIVERS_DATA_FILE):
        try:
            # تحديد الأعمدة المتوقعة لتجنب الأخطاء إذا كان الملف فارغاً أو قديماً
            expected_columns = ["التاريخ", "اسم_السائق", "وقت_الدوام", "حالة_الدوام", "رقم_الباص", "حالة_الباص", "ملاحظات"]
            df = pd.read_csv(DRIVERS_DATA_FILE)
            # التأكد من وجود جميع الأعمدة، وإضافة الناقصة بقيم فارغة
            for col in expected_columns:
                if col not in df.columns:
                    df[col] = ""
            return df[expected_columns] # إعادة ترتيب الأعمدة حسب الترتيب المتوقع
        except pd.errors.EmptyDataError:
            return pd.DataFrame(columns=["التاريخ", "اسم_السائق", "وقت_الدوام", "حالة_الدوام", "رقم_الباص", "حالة_الباص", "ملاحظات"])
    return pd.DataFrame(columns=["التاريخ", "اسم_السائق", "وقت_الدوام", "حالة_الدوام", "رقم_الباص", "حالة_الباص", "ملاحظات"])

# دالة لحفظ بيانات السائقين والباصات
def save_drivers_data(df):
    df.to_csv(DRIVERS_DATA_FILE, index=False)

def run():
    st.title("🚌 إدارة السائقين والباصات")
    st.info("هنا يتم تتبع دوام السائقين، حالة الباصات، وتسجيل الملاحظات.")

    # قسم تسجيل البيانات (للمشرف/المديرة)
    st.header("تسجيل بيانات السائقين والباصات اليومية")
    with st.form("drivers_entry_form", clear_on_submit=True):
        entry_date = st.date_input("تاريخ التسجيل:", datetime.date.today())
        
        driver_name = st.text_input("اسم السائق:", key="driver_name_input")
        shift_time = st.text_input("مواعيد الدوام (مثال: 7AM-4PM):", key="shift_time_input")
        
        attendance_status = st.radio("حالة الدوام:", ("حاضر", "غائب", "إجازة"), key="attendance_radio")
        
        # حقول خاصة بالباصات
        bus_number = st.selectbox(
            "رقم الباص (إن وجد):",
            ["لا يوجد", "B01", "B02", "B03", "B04", "B05", "B06", "B07", "B08", "B09", "B10"],
            key="bus_number_select"
        )
        bus_status = st.radio("حالة الباص:", ("جيدة", "يحتاج صيانة", "معطل"), key="bus_status_radio")
        
        notes = st.text_area("ملاحظات إضافية أو طلبات مهمة:", key="driver_notes_text")

        submitted = st.form_submit_button("تسجيل البيانات")
        if submitted:
            if not driver_name.strip():
                st.error("الرجاء إدخال اسم السائق.")
            else:
                new_entry = pd.DataFrame([{
                    "التاريخ": entry_date.isoformat(),
                    "اسم_السائق": driver_name,
                    "وقت_الدوام": shift_time,
                    "حالة_الدوام": attendance_status,
                    "رقم_الباص": bus_number,
                    "حالة_الباص": bus_status,
                    "ملاحظات": notes
                }])
                
                all_data = load_drivers_data()
                if all_data.empty:
                    updated_data = new_entry
                else:
                    updated_data = pd.concat([all_data, new_entry], ignore_index=True)
                save_drivers_data(updated_data)
                st.success("✅ تم تسجيل بيانات السائق والباص بنجاح!")
                st.rerun()

    # قسم عرض البيانات (للمتابعة)
    st.header("📊 ملخص دوام السائقين وحالة الباصات اليومية")
    current_day_data = load_drivers_data()
    today_date_str = datetime.date.today().isoformat()
    daily_records = current_day_data[current_day_data["التاريخ"] == today_date_str]

    if not daily_records.empty:
        st.subheader("👨‍✈️ السائقون المداومون اليوم:")
        present_drivers = daily_records[daily_records["حالة_الدوام"] == "حاضر"]
        if not present_drivers.empty:
            st.dataframe(present_drivers[['اسم_السائق', 'وقت_الدوام', 'رقم_الباص', 'حالة_الباص', 'ملاحظات']].style.set_properties(**{'text-align': 'right', 'font-size': '16px'}), hide_index=True)
        else:
            st.info("لا يوجد سائقون حاضرون اليوم.")

        st.subheader("⚠️ حالة الباصات:")
        bus_issues = daily_records[daily_records["حالة_الباص"] != "جيدة"]
        if not bus_issues.empty:
            st.warning("توجد باصات تحتاج متابعة:")
            for index, row in bus_issues.iterrows():
                st.write(f"- **رقم {row['رقم_الباص']}** (السائق: {row['اسم_السائق']}) - الحالة: **{row['حالة_الباص']}** - ملاحظات: {row['ملاحظات']}")
        else:
            st.success("جميع الباصات في حالة جيدة اليوم.")
            
        st.subheader("📜 جميع سجلات اليوم:")
        st.dataframe(daily_records.style.set_properties(**{'text-align': 'right', 'font-size': '14px'}), use_container_width=True, hide_index=True)

    else:
        st.info("لا توجد بيانات تسجيل للسائقين والباصات لهذا اليوم حتى الآن.")

# استدعاء الدالة لتشغيل الصفحة
run()
