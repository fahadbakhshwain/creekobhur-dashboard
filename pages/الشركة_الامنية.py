import streamlit as st
import pandas as pd
import datetime
import os

# اسم الملف لحفظ بيانات الشركة الأمنية
SECURITY_DATA_FILE = "security_company_data.csv"

# مجلد لحفظ صور مشاكل الصيانة (لا نحتاجها هنا لكن للتأكد)
# MAINTENANCE_IMAGES_DIR = "maintenance_images"
# if not os.path.exists(MAINTENANCE_IMAGES_DIR):
#    os.makedirs(MAINTENANCE_IMAGES_DIR)

# قائمة المناطق المحددة للمراقبة (ثابتة)
MONITORING_AREAS = [
    "البوابة الشمالية",
    "الشاطئ الكبير",
    "الشاطئ الصغير",
    "ميدان السمكة",
    "منطقة ألعاب 1",
    "منطقة ألعاب 2",
    "الساحة الكبيرة",
    "هاشتاق أبحر"
]

# دالة لتحميل بيانات الشركة الأمنية
def load_security_data():
    # تعريف الأعمدة المتوقعة هنا لتكون متاحة دائماً
    expected_columns = [
        "التاريخ", 
        "المشرف_المسؤول", 
        "عدد_العناصر_المتواجدين_إجمالي", 
        "المفروض_تواجدهم_إجمالي",
        "وصف_الحالة_المباشرة", 
        "ملاحظات_عامة"
    ] 
    # إضافة أعمدة خاصة بكل منطقة لتوزيع العناصر وحالة الالتزام
    for area in MONITORING_AREAS:
        expected_columns.append(f"عناصر_في_{area}")
        expected_columns.append(f"التزام_في_{area}") # "نعم", "لا", "غير مطبق"

    if os.path.exists(SECURITY_DATA_FILE):
        try:
            df = pd.read_csv(SECURITY_DATA_FILE)
            # التأكد من وجود جميع الأعمدة، وإضافة الناقصة بقيم فارغة
            for col in expected_columns:
                if col not in df.columns:
                    df[col] = "" 
            return df[expected_columns] # إعادة ترتيب الأعمدة حسب الترتيب المتوقع
        except pd.errors.EmptyDataError:
            return pd.DataFrame(columns=expected_columns)
    return pd.DataFrame(columns=expected_columns)

# دالة لحفظ بيانات الشركة الأمنية
def save_security_data(df):
    df.to_csv(SECURITY_DATA_FILE, index=False)

def run():
    st.title("🛡️ إدارة الشركة الأمنية")
    st.info("هنا يتم تتبع تواجد عناصر الأمن، التزامهم بالمواقع، وتسجيل الحالات المباشرة.")

    security_supervisors = ["مشرف الأمن الأول", "مشرف الأمن الثاني", "مشرف الأمن الثالث"]

    st.header("تسجيل بيانات الشركة الأمنية اليومية")
    with st.form("security_entry_form", clear_on_submit=True):
        entry_date = st.date_input("تاريخ التسجيل:", datetime.date.today())
        responsible_supervisor = st.selectbox("المشرف المسؤول عن المتابعة:", security_supervisors, key="security_supervisor_select")
        
        col1, col2 = st.columns(2)
        with col1:
            present_elements_total = st.number_input("إجمالي عدد عناصر الأمن المتواجدين اليوم:", min_value=0, step=1, key="present_elements_total_input")
        with col2:
            expected_elements_total = st.number_input("العدد المفروض تواجده إجمالاً:", min_value=0, step=1, key="expected_elements_total_input")
        
        st.subheader("توزيع عناصر الأمن على المناطق")
        st.markdown("**(يرجى إدخال عدد العناصر لكل منطقة وحالة التزامهم)**")
        
        area_distribution_data = []
        for area in MONITORING_AREAS:
            area_distribution_data.append({"المنطقة": area, "عدد العناصر": 0, "ملتزمون بالموقع": "نعم"})
        
        edited_distribution_df = st.data_editor(
            pd.DataFrame(area_distribution_data),
            column_config={
                "المنطقة": st.column_config.Column("المنطقة", disabled=True),
                "عدد العناصر": st.column_config.NumberColumn("عدد العناصر", min_value=0, step=1),
                "ملتزمون بالموقع": st.column_config.SelectboxColumn(
                    "ملتزمون بالموقع", options=["نعم", "لا", "غير مطبق"]
                ),
            },
            hide_index=True,
            use_container_width=True,
            key="area_distribution_editor"
        )
        
        st.subheader("تسجيل الحالات التي تم مباشرتها (الحوادث/البلاغات)")
        incident_description = st.text_area("وصف الحالات التي تم مباشرتها اليوم:", height=150, help="اذكر تفاصيل أي حوادث أو بلاغات تم التعامل معها.", key="incident_desc_input")
        
        general_notes = st.text_area("ملاحظات عامة لليوم:", height=100, key="general_notes_input")

        submitted = st.form_submit_button("تسجيل البيانات الأمنية")
        if submitted:
            if not responsible_supervisor.strip():
                st.error("الرجاء اختيار المشرف المسؤول.")
            else:
                area_data_for_save = {}
                for index, row in edited_distribution_df.iterrows():
                    area_name = row["المنطقة"]
                    area_data_for_save[f"عناصر_في_{area_name}"] = row["عدد العناصر"]
                    area_data_for_save[f"التزام_في_{area_name}"] = row["ملتزمون بالموقع"]

                new_entry_dict = {
                    "التاريخ": entry_date.isoformat(),
                    "المشرف_المسؤول": responsible_supervisor,
                    "عدد_العناصر_المتواجدين_إجمالي": present_elements_total,
                    "المفروض_تواجدهم_إجمالي": expected_elements_total,
                    "وصف_الحالة_المباشرة": incident_description,
                    "ملاحظات_عامة": general_notes,
                    **area_data_for_save
                }
                new_entry = pd.DataFrame([new_entry_dict])
                
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
        # استخدام آخر قيمة مسجلة لليوم للإجمالي
        latest_total_present = daily_records["عدد_العناصر_المتواجدين_إجمالي"].iloc[-1]
        latest_total_expected = daily_records["المفروض_تواجدهم_إجمالي"].iloc[-1]
        
        st.metric(label="عناصر الأمن المتواجدون اليوم", value=f"{latest_total_present} من {latest_total_expected}")
        if latest_total_present < latest_total_expected:
            st.warning(f"⚠️ يوجد نقص في عدد عناصر الأمن اليوم: {latest_total_expected - latest_total_present} عنصر.")
        elif latest_total_present > latest_total_expected:
             st.info(f"✅ يوجد عدد عناصر زائد عن المطلوب: {latest_total_present - latest_total_expected} عنصر.") # تم تصحيح هذا السطر
        else:
            st.success("✅ عدد عناصر الأمن مطابق للمطلوب اليوم.")

        st.subheader("تفاصيل توزيع العناصر في المناطق لليوم:")
        if not daily_records.empty:
            # هنا سنعرض جميع إدخالات توزيع المناطق التي تمت لليوم
            # لتبسيط العرض ولأن كل submission يحفظ كل توزيعات المناطق، 
            # سنعرض آخر توزيع تم إدخاله لليوم ليعكس الوضع الحالي
            latest_record = daily_records.iloc[-1] 
            area_summary_list = []
            for area in MONITORING_AREAS:
                num_elements = latest_record.get(f"عناصر_في_{area}", 0) # افتراضياً 0 إذا لم يتم تسجيلها
                commitment = latest_record.get(f"التزام_في_{area}", "غير مسجل")
                area_summary_list.append({
                    "المنطقة": area,
                    "عدد العناصر": num_elements,
                    "الالتزام": commitment
                })
            
            # فلترة الصفوف التي بها عناصر فقط للعرض
            summary_df = pd.DataFrame(area_summary_list)
            # عرض فقط المناطق التي تم تحديد عدد عناصر لها (أو التي ليست 0)
            displayed_summary_df = summary_df[summary_df["عدد العناصر"] > 0] 

            if not displayed_summary_df.empty:
                st.dataframe(displayed_summary_df.style.set_properties(**{'text-align': 'right', 'font-size': '14px'}), hide_index=True, use_container_width=True)
            else:
                st.info("لم يتم تسجيل توزيع عناصر الأمن على المناطق لهذا اليوم.")
        else:
            st.info("لا توجد بيانات توزيع عناصر الأمن على المناطق لهذا اليوم.")

        st.subheader("الحالات التي تم مباشرتها اليوم:")
        incidents = daily_records[daily_records["وصف_الحالة_المباشرة"].str.strip() != ""]
        if not incidents.empty:
            # عرض كل الحالات المبلغ عنها اليوم، حتى لو كانت في إدخالات منفصلة
            for index, row in incidents.iterrows():
                st.markdown(f"**⏰ {row['التاريخ']} - المشرف: {row['المشرف_المسؤول']}**")
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
  
        
         
