import streamlit as st
import pandas as pd
import datetime
import os
import plotly.express as px

# --- تعريف مسارات الملفات (يجب أن تكون متطابقة مع الصفحات الأخرى) ---
TASKS_FILE = "tasks.csv"
TOILETS_DATA_FILE = "toilets_data.csv"
SECURITY_DATA_FILE = "security_company_data.csv"
BEACHES_DATA_FILE = "beaches_status_data.csv"
DRIVERS_DATA_FILE = "drivers_and_buses_data.csv"
MAINTENANCE_DATA_FILE = "maintenance_issues.csv"
FINANCIAL_DATA_FILE = "financial_data.csv"
WAREHOUSE_DATA_FILE = "warehouse_inventory_data.csv"
STAFF_DAILY_DATA_FILE = "staff_daily_records.csv"
CLEANING_STAFF_DATA_FILE = "cleaning_staff_daily_data.csv"
AGRICULTURE_DATA_FILE = "agriculture_daily_report.csv"
ASSISTANT_TASKS_FILE = "assistant_tasks_data.csv"


# --- دوال تحميل البيانات من مختلف الملفات (مكررة هنا لضمان العمل) ---
# هذه الدوال هي نسخ مماثلة للدوال في ملفاتها الأصلية
def load_tasks():
    expected_cols = ["التاريخ", "المشرف", "المهمة", "ملاحظات"]
    if os.path.exists(TASKS_FILE):
        try: return pd.read_csv(TASKS_FILE)
        except pd.errors.EmptyDataError: return pd.DataFrame(columns=expected_cols)
    return pd.DataFrame(columns=expected_cols)

def load_toilets_data():
    expected_cols = ["التاريخ", "الوقت", "المسؤول", "رقم_المياه", "النوع", "مرات_التنظيف", "نواقص_مواد", "ملاحظات", "مسار_الصورة"]
    if os.path.exists(TOILETS_DATA_FILE):
        try: return pd.read_csv(TOILETS_DATA_FILE)
        except pd.errors.EmptyDataError: return pd.DataFrame(columns=expected_cols)
    return pd.DataFrame(columns=expected_cols)

def load_security_data():
    expected_cols = ["التاريخ", "المشرف_المسؤول", "عدد_العناصر_المتواجدين_إجمالي", "المفروض_تواجدهم_إجمالي", "وصف_الحالة_المباشرة", "ملاحظات_عامة"]
    for area in ["البوابة الشمالية","الشاطئ الكبير","الشاطئ الصغير","ميدان السمكة","منطقة ألعاب 1","منطقة ألعاب 2","الساحة الكبيرة","هاشتاق أبحر"]:
        expected_cols.append(f"عناصر_في_{area}"); expected_cols.append(f"التزام_في_{area}")
    if os.path.exists(SECURITY_DATA_FILE):
        try: return pd.read_csv(SECURITY_DATA_FILE)
        except pd.errors.EmptyDataError: return pd.DataFrame(columns=expected_cols)
    return pd.DataFrame(columns=expected_cols)

def load_beaches_data():
    expected_cols = ["التاريخ", "اسم_المشرف", "اسم_الشاطئ", "حالة_الكاشير", "عدد_المنقذين_المتواجدين", "المفروض_تواجدهم_منقذين", "حالة_ابراج_المراقبة", "حالة_الشاطئ_العامة", "موعد_الاخلاء", "موعد_فتح_السباحة", "الحالة_الجوية_والإغلاق", "حالة_الشبك", "حالة_اجهزة_النداء", "حالة_ادوات_السلامة", "حالة_الاسعافات_الاولية", "ملاحظات_عامة", "مسار_الصورة"]
    if os.path.exists(BEACHES_DATA_FILE):
        try: return pd.read_csv(BEACHES_DATA_FILE)
        except pd.errors.EmptyDataError: return pd.DataFrame(columns=expected_cols)
    return pd.DataFrame(columns=expected_cols)

def load_drivers_data():
    expected_cols = ["التاريخ", "اسم_السائق", "وقت_الدوام", "حالة_الدوام", "رقم_الباص", "حالة_الباص", "ملاحظات"]
    if os.path.exists(DRIVERS_DATA_FILE):
        try: return pd.read_csv(DRIVERS_DATA_FILE)
        except pd.errors.EmptyDataError: return pd.DataFrame(columns=expected_cols)
    return pd.DataFrame(columns=expected_cols)

def load_maintenance_issues():
    expected_cols = ["التاريخ", "الوقت", "المبلغ_عنه", "الموقع", "وصف_المشكلة", "الحالة", "ملاحظات_إدارية", "مسار_الصورة"]
    if os.path.exists(MAINTENANCE_DATA_FILE):
        try: return pd.read_csv(MAINTENANCE_DATA_FILE)
        except pd.errors.EmptyDataError: return pd.DataFrame(columns=expected_cols)
    return pd.DataFrame(columns=expected_cols)

def load_financial_data():
    expected_cols = ["التاريخ", "البند", "النوع", "القيمة", "الشاطئ", "ملاحظات", "تم_التحقق_منه"]
    if os.path.exists(FINANCIAL_DATA_FILE):
        try: return pd.read_csv(FINANCIAL_DATA_FILE)
        except pd.errors.EmptyDataError: return pd.DataFrame(columns=expected_cols)
    return pd.DataFrame(columns=expected_cols)

def load_warehouse_data():
    expected_cols = ["التاريخ", "وقت_التسجيل", "المسؤول", "نوع_العملية", "الصنف", "اسم_المادة", "الكمية", "الوحدة", "المورد", "ملاحظات"]
    if os.path.exists(WAREHOUSE_DATA_FILE):
        try: return pd.read_csv(WAREHOUSE_DATA_FILE)
        except pd.errors.EmptyDataError: return pd.DataFrame(columns=expected_cols)
    return pd.DataFrame(columns=expected_cols)

def load_staff_data():
    expected_cols = ["التاريخ", "المسؤول_المسجل", "اسم_الموظف", "القسم_الوظيفة", "حالة_الحضور", "وقت_الحضور_المسجل", "وقت_المغادرة_المسجل", "ملاحظات_خاصة", "تقييم_مبدئي_للأداء"]
    if os.path.exists(STAFF_DAILY_DATA_FILE):
        try: return pd.read_csv(STAFF_DAILY_DATA_FILE)
        except pd.errors.EmptyDataError: return pd.DataFrame(columns=expected_cols)
    return pd.DataFrame(columns=expected_cols)

def load_cleaning_staff_data():
    expected_cols = ["التاريخ", "المشرف_المسجل", "اسم_العامل", "وقت_الحضور", "حالة_الحضور", "المنطقة_المخصصة", "المهام_الموكلة", "حالة_المهام", "ملاحظات"]
    if os.path.exists(CLEANING_STAFF_DATA_FILE):
        try: return pd.read_csv(CLEANING_STAFF_DATA_FILE)
        except pd.errors.EmptyDataError: return pd.DataFrame(columns=expected_cols)
    return pd.DataFrame(columns=expected_cols)

def load_agriculture_data():
    expected_cols = ["التاريخ", "المسؤول_المسجل", "المنطقة_المعنية", "المهام_المنجزة", "حالة_النباتات_العامة", "احتياجات_خاصة", "ملاحظات_عامة", "مسار_الصورة"]
    if os.path.exists(AGRICULTURE_DATA_FILE):
        try: return pd.read_csv(AGRICULTURE_DATA_FILE)
        except pd.errors.EmptyDataError: return pd.DataFrame(columns=expected_cols)
    return pd.DataFrame(columns=expected_cols)

def load_assistant_tasks():
    expected_cols = ["التاريخ", "وقت_التكليف", "الوصف", "الحالة", "الموعد_النهائي", "الملاحظات_الإدارية"]
    if os.path.exists(ASSISTANT_TASKS_FILE):
        try: return pd.read_csv(ASSISTANT_TASKS_FILE)
        except pd.errors.EmptyDataError: return pd.DataFrame(columns=expected_cols)
    return pd.DataFrame(columns=expected_cols)


def run():
    st.title("📊 لوحة تقارير الأداء الشاملة")
    st.info("تقرير يومي موجز ومفيد عن أداء الواجهة البحرية، يلخص الإنجازات والتحديات.")

    today_date_str = datetime.date.today().isoformat()
    
    st.header(f"تقرير الأداء اليومي - {today_date_str}")
    st.markdown("---")

    # --- 1. ملخص الأداء العام (KPIs) ---
    st.subheader("💡 ملخص الأداء العام")
    
    col_kpi1, col_kpi2, col_kpi3 = st.columns(3)

    # المهام اليومية المنجزة
    tasks_df = load_tasks()
    daily_completed_tasks = tasks_df[(tasks_df["التاريخ"] == today_date_str) & (tasks_df["حالة_المهام"] == "تم الإنجاز")].shape[0] if "حالة_المهام" in tasks_df.columns else 0 # Assuming 'حالة_المهام' exists for daily tasks
    total_daily_tasks = tasks_df[tasks_df["التاريخ"] == today_date_str].shape[0]
    col_kpi1.metric("مهام اليوم المنجزة", f"{daily_completed_tasks} من {total_daily_tasks}" if total_daily_tasks > 0 else "0")

    # حالة نظافة دورات المياه
    toilets_df = load_toilets_data()
    daily_toilets_data = toilets_df[toilets_df["التاريخ"] == today_date_str]
    clean_toilets_count = daily_toilets_data[daily_toilets_data["نواقص_مواد"].astype(str) == "لا يوجد"].shape[0]
    total_toilets_inspected = daily_toilets_data.shape[0]
    col_kpi2.metric("دورات المياه نظيفة اليوم", f"{clean_toilets_count} من {total_toilets_inspected}" if total_toilets_inspected > 0 else "0")

    # بلاغات الصيانة المعلقة
    maintenance_df = load_maintenance_issues()
    pending_maintenance = maintenance_df[maintenance_df["الحالة"].isin(["جديد", "قيد المراجعة"])].shape[0]
    total_maintenance = maintenance_df.shape[0]
    col_kpi3.metric("بلاغات صيانة معلقة", f"{pending_maintenance} من {total_maintenance}" if total_maintenance > 0 else "0")
    
    st.markdown("---")

    # --- 2. أداء الأقسام الرئيسية ---
    st.subheader("📈 أداء الأقسام الرئيسية")

    # المحاسبة - إيرادات الشواطئ
    st.markdown("##### 💵 إيرادات الشواطئ (اليوم)")
    financial_df = load_financial_data()
    daily_income_by_beach = financial_df[(financial_df["التاريخ"] == today_date_str) & (financial_df["النوع"] == "إيرادات")].groupby("الشاطئ")["القيمة"].sum().reset_index()
    if not daily_income_by_beach.empty:
        fig_income = px.bar(daily_income_by_beach, x="الشاطئ", y="القيمة", labels={"الشاطئ": "الشاطئ", "القيمة": "الإيرادات"}, color_discrete_sequence=px.colors.qualitative.Pastel)
        st.plotly_chart(fig_income, use_container_width=True)
    else:
        st.info("لا توجد إيرادات مسجلة للشواطئ اليوم.")

    # الشركة الأمنية - ملخص التواجد والالتزام
    st.markdown("##### 🛡️ ملخص أداء الشركة الأمنية")
    security_df = load_security_data()
    daily_security_records = security_df[security_df["التاريخ"] == today_date_str]
    if not daily_security_records.empty:
        latest_security_record = daily_security_records.iloc[-1]
        present_sec_elements = latest_security_record.get("عدد_العناصر_المتواجدين_إجمالي", 0)
        expected_sec_elements = latest_security_record.get("المفروض_تواجدهم_إجمالي", 0)
        st.write(f"**عدد عناصر الأمن:** {present_sec_elements} متواجدون من {expected_sec_elements} مطلوبين.")
        
        non_compliant_areas_count = 0
        compliant_areas_count = 0
        for area in ["البوابة الشمالية","الشاطئ الكبير","الشاطئ الصغير","ميدان السمكة","منطقة ألعاب 1","منطقة ألعاب 2","الساحة الكبيرة","هاشتاق أبحر"]:
            commitment = latest_security_record.get(f"التزام_في_{area}", "غير مسجل")
            if commitment == "لا": non_compliant_areas_count += 1
            elif commitment == "نعم": compliant_areas_count += 1
        
        st.write(f"**مناطق غير ملتزمة بالموقع:** {non_compliant_areas_count} - **مناطق ملتزمة:** {compliant_areas_count}")
        
        incidents_count = daily_security_records[daily_security_records["وصف_الحالة_المباشرة"].astype(str).str.strip() != ""].shape[0]
        st.write(f"**عدد الحالات المباشرة اليوم:** {incidents_count}")
    else:
        st.info("لا توجد بيانات أمنية مسجلة اليوم.")
    
    st.markdown("---")

    # --- 3. المهام والملاحظات الهامة ---
    st.subheader("🔔 المهام والملاحظات الهامة للمتابعة")

    # المهام الإدارية المعلقة (من load_assistant_tasks أو مصدر آخر إذا كان هناك فصل)
    # نستخدم load_assistant_tasks لأنها أقرب للأنشطة الإدارية الخاصة بالمساعدة
    assistant_tasks_df = load_assistant_tasks()
    pending_admin_tasks = assistant_tasks_df[assistant_tasks_df["الحالة"].isin(["معلقة", "تحتاج مراجعة"])]
    if not pending_admin_tasks.empty:
        st.markdown("##### مهام مساعدة المديرة المعلقة/تحتاج مراجعة:")
        for index, row in pending_admin_tasks.iterrows():
            st.warning(f"- **{row['الوصف']}** (الحالة: {row['الحالة']}) - الموعد: {row['الموعد_النهائي']}")
    else:
        st.info("لا توجد مهام معلقة لمساعدة المديرة حالياً.")

    # ملاحظات خاصة من الموظفين وعمال النظافة
    st.markdown("##### ملاحظات خاصة من الموظفين وعمال النظافة:")
    staff_df = load_staff_data()
    cleaning_staff_df = load_cleaning_staff_data()

    staff_notes = staff_df[staff_df["ملاحظات_خاصة"].astype(str).str.strip() != ""]
    cleaning_notes = cleaning_staff_df[cleaning_staff_df["ملاحظات"].astype(str).str.strip() != ""]

    if not staff_notes.empty or not cleaning_notes.empty:
        if not staff_notes.empty:
            for index, row in staff_notes.iterrows():
                st.write(f"- **موظف ({row['اسم_الموظف']}):** {row['ملاحظات_خاصة']}")
        if not cleaning_notes.empty:
            for index, row in cleaning_notes.iterrows():
                st.write(f"- **عامل نظافة ({row['اسم_العامل']}):** {row['ملاحظات']}")
    else:
        st.info("لا توجد ملاحظات خاصة من الموظفين أو عمال النظافة اليوم.")

    st.markdown("---")

    # --- 4. تصور للنمو والتطوير ---
    st.subheader("🚀 نظرة مستقبلية: تطوير النظام بالذكاء الاصطناعي")
    st.markdown("""
    يهدف هذا النظام إلى التحول لمنصة ذكية تعتمد على البيانات لتحسين الكفاءة واتخاذ القرارات. 
    يمكننا في المراحل القادمة دمج تقنيات الذكاء الاصطناعي لـ:
    * **تحليل المهام من رسائل الواتساب:** باستخدام معالجة اللغة الطبيعية (NLP) لأتمتة إدخال المهام.
    * **التنبؤ بالاحتياجات:** توقع نقص المخزون أو مشاكل الصيانة بناءً على الأنماط التاريخية.
    * **تحليل الأداء:** تقديم رؤى أعمق حول أداء الموظفين والأقسام بناءً على البيانات المسجلة.
    * **اقتراح جداول عمل محسّنة:** لتحقيق أقصى كفاءة للموارد البشرية.
    """)

# استدعاء الدالة لتشغيل الصفحة
run()
