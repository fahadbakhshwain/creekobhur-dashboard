import streamlit as st
import pandas as pd
import datetime
import os

# اسم الملف لحفظ بيانات دورات المياه
TOILETS_DATA_FILE = "toilets_data.csv"
# مجلد لحفظ صور دورات المياه
TOILETS_IMAGES_DIR = "toilet_images"

# التأكد من وجود مجلد حفظ الصور
if not os.path.exists(TOILETS_IMAGES_DIR):
    os.makedirs(TOILETS_IMAGES_DIR)

# دالة لتحميل بيانات دورات المياه
def load_toilets_data():
    if os.path.exists(TOILETS_DATA_FILE):
        try:
            return pd.read_csv(TOILETS_DATA_FILE)
        except pd.errors.EmptyDataError:
            return pd.DataFrame(columns=["التاريخ", "الوقت", "المسؤول", "رقم_المياه", "النوع", "مرات_التنظيف", "نواقص_مواد", "ملاحظات", "مسار_الصورة"])
    return pd.DataFrame(columns=["التاريخ", "الوقت", "المسؤول", "رقم_المياه", "النوع", "مرات_التنظيف", "نواقص_مواد", "ملاحظات", "مسار_الصورة"])

# دالة لحفظ بيانات دورات المياه
def save_toilets_data(df):
    df.to_csv(TOILETS_DATA_FILE, index=False)

def run():
    st.title("🚽 إدارة ومتابعة دورات المياه")
    st.info("هنا يمكنك تسجيل وتتبع حالة نظافة دورات المياه والنواقص ورفع الصور.")

    st.header("تسجيل حالة دورة مياه")
    with st.form("toilet_status_form", clear_on_submit=True):
        entry_date = st.date_input("تاريخ التسجيل:", datetime.date.today())
        entry_time = st.time_input("وقت التسجيل:", datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=3))).time()) # توقيت السعودية هو UTC+3

        # قائمة بالمشرفين المتاحين (يمكن أن تأتي من مكان مركزي مستقبلاً)
        supervisors = ["المشرف الأول", "المشرف الثاني", "المشرف الثالث", "العمالة العامة"]
        responsible_person = st.selectbox("المسؤول عن التنظيف:", supervisors, key="responsible_person_select")

        toilet_number = st.selectbox(
            "رقم دورة المياه:",
            ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14"],
            key="toilet_num_select"
        )
        toilet_type = st.radio("نوع دورة المياه:", ("رجال", "نساء", "خاص"), key="toilet_type_radio")
        
        # لا نطلب "عدد مرات التنظيف" هنا مباشرة، بل نسجل "عملية تنظيف" واحدة
        # يمكننا حساب الإجمالي لاحقاً من البيانات المسجلة.
        
        # اختيار النواقص
        missing_items_options = ["لا يوجد", "ديتول", "صابون", "مناديل", "أكياس نفايات", "معطر جو", "أخرى"]
        missing_items = st.multiselect("نواقص مواد النظافة:", missing_items_options, default=["لا يوجد"] if "لا يوجد" in missing_items_options else [])
        
        notes = st.text_area("ملاحظات إضافية:", key="toilet_notes_text")

        # رفع الصور
        uploaded_image = st.file_uploader("ارفع صورة لدورة المياه بعد التنظيف (اختياري):", type=["png", "jpg", "jpeg"], key="toilet_image_uploader")
        
        submitted = st.form_submit_button("تسجيل الحالة")
        if submitted:
            image_path = ""
            if uploaded_image is not None:
                # إنشاء اسم فريد للصورة لحفظها
                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                image_name = f"{toilet_number}_{toilet_type}_{timestamp}_{uploaded_image.name}"
                image_path = os.path.join(TOILETS_IMAGES_DIR, image_name)
                
                # حفظ الصورة
                with open(image_path, "wb") as f:
                    f.write(uploaded_image.getbuffer())
                st.success(f"تم حفظ الصورة: {image_name}")

            missing_items_str = ", ".join(missing_items) if missing_items and "لا يوجد" not in missing_items else "لا يوجد"
            
            # في كل مرة يتم التسجيل، نعتبرها "مرة تنظيف" واحدة
            new_entry = pd.DataFrame([{
                "التاريخ": entry_date.isoformat(),
                "الوقت": entry_time.strftime("%H:%M"),
                "المسؤول": responsible_person,
                "رقم_المياه": toilet_number,
                "النوع": toilet_type,
                "مرات_التنظيف": 1, # نسجل 1 لكل عملية تسجيل
                "نواقص_مواد": missing_items_str,
                "ملاحظات": notes,
                "مسار_الصورة": image_path
            }])
            
            all_data = load_toilets_data()
            if all_data.empty:
                updated_data = new_entry
            else:
                updated_data = pd.concat([all_data, new_entry], ignore_index=True)
            save_toilets_data(updated_data)
            st.success("✅ تم تسجيل حالة دورة المياه بنجاح!")
            st.rerun()

    st.header("📊 سجلات دورات المياه اليوم")
    current_day_data = load_toilets_data()
    today_date_str = datetime.date.today().isoformat()
    daily_records = current_day_data[current_day_data["التاريخ"] == today_date_str]

    if not daily_records.empty:
        # عرض السجلات في جدول
        st.dataframe(daily_records[['التاريخ', 'الوقت', 'المسؤول', 'رقم_المياه', 'النوع', 'نواقص_مواد', 'ملاحظات']].style.set_properties(**{'text-align': 'right', 'font-size': '14px'}), hide_index=True)
        
        # عرض الصور (بشكل اختياري في expender)
        if st.checkbox("عرض الصور المرفوعة لهذا اليوم"):
            for index, row in daily_records.iterrows():
                if row['مسار_الصورة'] and os.path.exists(row['مسار_الصورة']):
                    st.image(row['مسار_الصورة'], caption=f"صورة دورة مياه رقم {row['رقم_المياه']} ({row['النوع']}) - {row['الوقت']}", width=200)
                else:
                    st.markdown(f"**دورة مياه رقم {row['رقم_المياه']} ({row['النوع']}):** لا توجد صورة مرفوعة أو المسار غير صالح.")
        
        # ملخص سريع للنواقص
        st.subheader("💡 أبرز النواقص المبلغ عنها اليوم:")
        missing_today = daily_records[daily_records["نواقص_مواد"].str.contains("لا يوجد") == False]
        if not missing_today.empty:
            for index, row in missing_today.iterrows():
                st.warning(f"**رقم {row['رقم_المياه']} ({row['النوع']}) - {row['المسؤول']}:** نواقص في: {row['نواقص_مواد']}")
        else:
            st.success("🎉 لا توجد نواقص في مواد النظافة مبلغ عنها اليوم.")
            
    else:
        st.info("لا توجد بيانات تسجيل لدورات المياه لهذا اليوم حتى الآن.")


# استدعاء الدالة لتشغيل الصفحة
run()
