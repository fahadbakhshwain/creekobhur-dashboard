import streamlit as st
import pandas as pd
import datetime
import os

# اسم الملف لحفظ بيانات الشركة الأمنية
SECURITY_DATA_FILE = "security_company_data.csv"

# دالة لتحميل بيانات الشركة الأمنية
def load_security_data():
    if os.path.exists(SECURITY_DATA_FILE):
        try:
            # الأعمدة المتوقعة
            expected_columns = ["التاريخ", "المشرف_المسؤول", "عدد_العناصر_المتواجدين", "المفروض_تواجدهم", 
                                "المنطقة_المراقبة", "عناصر_متواجدون_بالمنطقة", "هل_ملتزمون_بالموقع",
                                "وصف_الحالة_المباشرة", "ملاحظات_عامة"]
            df = pd.read_csv(SECURITY_DATA_FILE)
            for col in expected_columns:
                if col not in df.columns:
                    df[col] = "" # إضافة الأعمدة الناقصة
            return df[expected_columns]
        except pd.errors.EmptyDataError:
            return pd.DataFrame(columns=expected_columns)
    return pd.DataFrame(columns=expected_columns)

# دالة لحفظ بيانات الشركة الأمنية
def save_security_data(df):
    df.to_csv(SECURITY_DATA_FILE, index=False)

def run():
    st.title("🛡️ إدارة الشركة الأمنية")
    st.info("هنا يتم تتبع تواجد عناصر الأمن، التزامهم بالمواقع، وتسجيل الحالات المباشرة.")

    # قائمة المشرفين المسؤولين عن الشركة الأمنية (يمكن تعديلها)
    security_supervisors = ["مشرف الأمن الأول", "مشرف الأمن الثاني", "مشرف الأمن الثالث"]

    # المناطق المحددة للمراقبة
    monitoring_areas = [
        "البوابة الشمالية",
        "الشاطئ الكبير",
        "الشاطئ الصغير",
        "ميدان السمكة",
        "منطقة ألعاب 1",
        "منطقة ألعاب 2",
        "الساحة الكبيرة",
        "هاشتاق أبحر"
    ]

    st.header("تسجيل بيانات الشركة الأمنية اليومية")
    with st.form("security_entry_form", clear_on_submit=True):
        entry_date = st.date_input("تاريخ التسجيل:", datetime.date.today())
        
        responsible_supervisor = st.selectbox("المشرف المسؤول عن المتابعة:", security_supervisors, key="security_supervisor_select")
        
        col1, col2 = st.columns(2)
        with col1:
            present_elements = st.number_input("عدد عناصر الأمن المتواجدين اليوم:", min_value=0, step=1, key="present_elements_input")
        with col2:
            expected_elements = st.number_input("العدد المفروض تواجده:", min_value=0, step=1, key="expected_elements_input")
        
        st.subheader("متابعة تواجد العناصر في المناطق")
        
        # اختيار المنطقة وعدد العناصر فيها
        selected_area = st.selectbox("اختر المنطقة للمراقبة:", monitoring_areas, key="selected_monitoring_area")
        elements_in_area = st.number_input(f"عدد عناصر الأمن المتواجدين في '{selected_area}':", min_value=0, step=1, key="elements_in_area_input")
        
        # زر راديو للالتزام بالموقع
        is_committed_to_location = st.radio(
            f"هل العناصر ملتزمون بموقعهم في '{selected_area}'؟",
            ("نعم", "لا", "غير مطبق"),
            key="committed_to_location_radio"
        )
        
        st.subheader("تسجيل الحالات التي تم مباشرتها (الحوادث/البلاغات)")
        incident_description = st.text_area("وصف الحالات التي تم مباشرتها اليوم:", height=150, help="اذكر تفاصيل أي حوادث أو بلاغات تم التعامل معها.", key="incident_desc_input")
        
        general_notes = st.text_area("ملاحظات عامة لليوم:", height=100, key="general_notes_input")

        submitted = st.form_submit_button("تسجيل البيانات الأمنية")
        if submitted:
            if not responsible_supervisor.strip():
                st.error("الرجاء اختيار المشرف المسؤول.")
            else:
                new_entry = pd.DataFrame([{
                    "التاريخ": entry_date.isoformat(),
                    "المشرف_المسؤول": responsible_supervisor,
                    "عدد_العناصر_المتواجدين": present_elements,
                    "المفروض_تواجدهم": expected_elements,
                    "المنطقة_المراقبة": selected_area, # نسجل آخر منطقة تم تحديدها
                    "عناصر_متواجدون_بالمنطقة": elements_in_area,
                    "هل_ملتزمون_بالموقع": is_committed_to_location,
                    "وصف_الحالة_المباشرة": incident_description,
                    "ملاحظات_عامة": general_notes
                }])
                
                all_data = load_security_data()
                if all_data.empty:
                    updated_data = new_entry
                else:
                    updated_data = pd.concat([all_data, new_entry], ignore_index=True)
                save_security_data(updated_data)
                st.success("✅ تم تسجيل البيانات الأمنية بنجاح!")
                st.rerun()

    # قسم عرض البيانات (للمتابعة)
    st.header("📊 ملخص بيانات الشركة الأمنية اليومية")
    current_day_data = load_security_data()
    today_date_str = datetime.date.today().isoformat()
    daily_records = current_day_data[current_day_data["التاريخ"] == today_date_str]

    if not daily_records.empty:
        st.subheader("إجمالي تواجد العناصر:")
        total_present = daily_records["عدد_العناصر_المتواجدين"].sum()
        total_expected = daily_records["المفروض_تواجدهم"].sum()
        st.metric(label="عناصر الأمن المتواجدون اليوم", value=f"{total_present} من {total_expected}")
        if total_present < total_expected:
            st.warning(f"⚠️ يوجد نقص في عدد عناصر الأمن اليوم: {total_expected - total_present} عنصر.")
        elif total_present > total_expected:
             st.info(f"✅ يوجد عدد عناصر زائد عن المطلوب: {total_present - total_expected} عنصر.")
        else:
            st.success("✅ عدد عناصر الأمن مطابق للمطلوب اليوم.")

        st.subheader("تفاصيل تواجد العناصر في المناطق:")
        # بما أننا نسجل إدخال واحد لكل نموذج، سنعرض آخر إدخال للمنطقة أو نطلب تصفية
        # لغرض البروتوتايب، سنعرض قائمة بجميع الإدخالات المتعلقة بالمناطق لليوم
        area_records = daily_records[['المشرف_المسؤول', 'المنطقة_المراقبة', 'عناصر_متواجدون_بالمنطقة', 'هل_ملتزمون_بالموقع']].drop_duplicates(subset=['المنطقة_المراقبة'])
        if not area_records.empty:
            st.dataframe(area_records.style.set_properties(**{'text-align': 'right', 'font-size': '14px'}), hide_index=True)
            non_compliant_areas = area_records[area_records["هل_ملتزمون_بالموقع"] == "لا"]
            if not non_compliant_areas.empty:
                st.warning("⚠️ يوجد عدم التزام بالموقع في المناطق التالية:")
                for index, row in non_compliant_areas.iterrows():
                    st.write(f"- **المنطقة: {row['المنطقة_المراقبة']}** - المشرف: {row['المشرف_المسؤول']}")
        else:
            st.info("لا توجد بيانات تواجد عناصر في المناطق لهذا اليوم.")

        st.subheader("الحالات التي تم مباشرتها اليوم:")
        incidents = daily_records[daily_records["وصف_الحالة_المباشرة"].str.strip() != ""]
        if not incidents.empty:
            for index, row in incidents.iterrows():
                st.markdown(f"**⏰ {row['التاريخ']} - {row['المشرف_المسؤول']}**")
                st.info(f"**وصف الحالة:** {row['وصف_الحالة_المباشرة']}")
                st.markdown("---")
        else:
            st.info("لا توجد حالات تم مباشرتها من قبل الأمن اليوم.")
            
        st.subheader("ملاحظات عامة لليوم:")
        general_notes_today = daily_records[daily_records["ملاحظات_عامة"].str.strip() != ""]
        if not general_notes_today.empty:
            for index, row in general_notes_today.iterrows():
                st.markdown(f"**✍️ {row['المشرف_المسؤول']}:** {row['ملاحظات_عامة']}")
        else:
            st.info("لا توجد ملاحظات عامة مسجلة اليوم.")


    else:
        st.info("لا توجد بيانات مسجلة للشركة الأمنية لهذا اليوم حتى الآن.")

# استدعاء الدالة لتشغيل الصفحة
run()
     
