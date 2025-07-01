import streamlit as st
import pandas as pd
import datetime
import os

# اسم الملف لحفظ بيانات الزراعة
AGRICULTURE_DATA_FILE = "agriculture_daily_report.csv"
# مجلد لحفظ صور أعمال الزراعة
AGRICULTURE_IMAGES_DIR = "agriculture_images"

# التأكد من وجود مجلد حفظ الصور
if not os.path.exists(AGRICULTURE_IMAGES_DIR):
    os.makedirs(AGRICULTURE_IMAGES_DIR)

# دالة لتحميل بيانات الزراعة
def load_agriculture_data():
    # تعريف الأعمدة المتوقعة هنا لتكون متاحة دائماً
    expected_columns = [
        "التاريخ", "المسؤول_المسجل", "المنطقة_المعنية", "المهام_المنجزة", 
        "حالة_النباتات_العامة", "احتياجات_خاصة", "ملاحظات_عامة", "مسار_الصورة"
    ]
    if os.path.exists(AGRICULTURE_DATA_FILE):
        try:
            df = pd.read_csv(AGRICULTURE_DATA_FILE)
            for col in expected_columns:
                if col not in df.columns:
                    df[col] = "" 
            return df[expected_columns]
        except pd.errors.EmptyDataError:
            return pd.DataFrame(columns=expected_columns)
    return pd.DataFrame(columns=expected_columns)

# دالة لحفظ بيانات الزراعة
def save_agriculture_data(df):
    df.to_csv(AGRICULTURE_DATA_FILE, index=False)

def run():
    st.title("🌳 إدارة قسم الزراعة")
    st.info("هنا يتم تسجيل التقارير اليومية لأعمال الزراعة، حالة النباتات، والملاحظات.")

    agriculture_supervisors = ["مشرف الزراعة", "عامل الزراعة الرئيسي"]
    
    # المناطق الزراعية في الواجهة البحرية وكوكيان
    agriculture_areas = [
        "الواجهة البحرية - المنطقة الشمالية", 
        "الواجهة البحرية - المنطقة الوسطى", 
        "الواجهة البحرية - المنطقة الجنوبية", 
        "كوكيان - المناطق الخضراء", 
        "كوكيان - الحدائق",
        "المداخل الرئيسية",
        "الممرات الداخلية",
        "مناطق أخرى"
    ]

    st.header("تسجيل التقرير اليومي لأعمال الزراعة")
    with st.form("agriculture_report_form", clear_on_submit=True):
        entry_date = st.date_input("تاريخ التقرير:", datetime.date.today())
        responsible_person = st.selectbox("المسؤول عن إعداد التقرير:", agriculture_supervisors, key="responsible_person_select")
        
        selected_area = st.multiselect("المناطق التي تمت بها الأعمال اليوم:", agriculture_areas, key="selected_area_multiselect")
        
        tasks_completed = st.text_area("المهام الزراعية المنجزة اليوم (مثال: ري، تقليم، تسميد، زراعة شتلات):", height=150, key="tasks_completed_text")
        
        plant_general_status = st.selectbox(
            "الحالة العامة للنباتات في المناطق التي تمت بها الأعمال:", 
            ["ممتازة", "جيدة", "متوسطة", "تحتاج اهتمام", "مشاكل ظاهرة"], 
            key="plant_status_select"
        )
        
        special_needs = st.text_area("احتياجات خاصة أو مشاكل ملاحظة (مثال: نقص مياه في منطقة X، آفة حشرية، نباتات ذابلة):", height=100, key="special_needs_text")
        
        general_notes = st.text_area("ملاحظات عامة لليوم:", height=100, key="general_notes_text")

        # رفع الصور
        uploaded_image = st.file_uploader("ارفع صورة لسير العمل/حالة النباتات (اختياري):", type=["png", "jpg", "jpeg"], key="agriculture_image_uploader")
        
        submitted = st.form_submit_button("تسجيل التقرير الزراعي")
        if submitted:
            if not tasks_completed.strip():
                st.error("الرجاء إدخال المهام المنجزة.")
            else:
                image_path = ""
                if uploaded_image is not None:
                    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                    image_name = f"agriculture_{'_'.join(selected_area[:2])}_{timestamp}_{uploaded_image.name}" # اسم بناءً على أول منطقتين
                    image_path = os.path.join(AGRICULTURE_IMAGES_DIR, image_name)
                    
                    with open(image_path, "wb") as f:
                        f.write(uploaded_image.getbuffer())
                    st.success(f"تم حفظ الصورة: {image_name}")

                new_entry = pd.DataFrame([{
                    "التاريخ": entry_date.isoformat(),
                    "المسؤول_المسجل": responsible_person,
                    "المنطقة_المعنية": ", ".join(selected_area), # حفظ المناطق كقائمة نصية مفصولة بفاصلة
                    "المهام_المنجزة": tasks_completed,
                    "حالة_النباتات_العامة": plant_general_status,
                    "احتياجات_خاصة": special_needs,
                    "ملاحظات_عامة": general_notes,
                    "مسار_الصورة": image_path
                }])
                
                all_data = load_agriculture_data()
                if all_data.empty:
                    updated_data = new_entry
                else:
                    updated_data = pd.concat([all_data, new_entry], ignore_index=True)
                save_agriculture_data(updated_data)
                st.success("✅ تم تسجيل التقرير الزراعي بنجاح!")
                st.rerun()

    # قسم عرض ملخص أعمال الزراعة اليومية
    st.header("📊 ملخص أعمال الزراعة اليومية")
    current_day_data = load_agriculture_data()
    today_date_str = datetime.date.today().isoformat()
    daily_records = current_day_data[current_day_data["التاريخ"] == today_date_str]

    if not daily_records.empty:
        st.subheader("التقارير المسجلة اليوم:")
        st.dataframe(daily_records[['التاريخ', 'المسؤول_المسجل', 'المنطقة_المعنية', 'المهام_المنجزة', 'حالة_النباتات_العامة']].style.set_properties(**{'text-align': 'right', 'font-size': '14px'}), use_container_width=True, hide_index=True)

        st.subheader("ملاحظات واحتياجات خاصة (تحتاج متابعة):")
        attention_needed = daily_records[
            (daily_records["احتياجات_خاصة"].astype(str).str.strip() != "") |
            (daily_records["حالة_النباتات_العامة"].isin(["تحتاج اهتمام", "مشاكل ظاهرة"]))
        ]
        if not attention_needed.empty:
            for index, row in attention_needed.iterrows():
                st.warning(f"**منطقة: {row['المنطقة_المعنية']}** - المشرف: {row['المسؤول_المسجل']}")
                if row['حالة_النباتات_العامة'] in ["تحتاج اهتمام", "مشاكل ظاهرة"]:
                    st.error(f"**حالة النباتات:** {row['حالة_النباتات_العامة']}")
                if row['احتياجات_خاصة']:
                    st.info(f"**احتياجات/مشاكل:** {row['احتياجات_خاصة']}")
                st.markdown("---")
        else:
            st.success("🎉 لا توجد ملاحظات أو مشاكل خاصة في الزراعة اليوم.")
            
        st.subheader("الصور المرفوعة اليوم:")
        images_uploaded = daily_records[daily_records["مسار_الصورة"].astype(str).str.strip() != ""]
        if not images_uploaded.empty:
            for index, row in images_uploaded.iterrows():
                if os.path.exists(row['مسار_الصورة']):
                    st.image(row['مسار_الصورة'], caption=f"صورة من {row['المنطقة_المعنية']} - {row['التاريخ']}", width=250)
                else:
                    st.warning(f"مسار الصورة غير صالح لـ: {row['المنطقة_المعنية']}")
        else:
            st.info("لا توجد صور مرفوعة لأعمال الزراعة اليوم.")

    else:
        st.info("لا توجد تقارير زراعية مسجلة لهذا اليوم حتى الآن.")

# استدعاء الدالة لتشغيل الصفحة
run()
