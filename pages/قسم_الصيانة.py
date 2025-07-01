import streamlit as st
import pandas as pd
import datetime
import os

# اسم الملف لحفظ بيانات مشاكل الصيانة
MAINTENANCE_DATA_FILE = "maintenance_issues.csv"
# مجلد لحفظ صور مشاكل الصيانة
MAINTENANCE_IMAGES_DIR = "maintenance_images"

# التأكد من وجود مجلد حفظ الصور
if not os.path.exists(MAINTENANCE_IMAGES_DIR):
    os.makedirs(MAINTENANCE_IMAGES_DIR)

# دالة لتحميل بيانات مشاكل الصيانة
def load_maintenance_issues():
    if os.path.exists(MAINTENANCE_DATA_FILE):
        try:
            return pd.read_csv(MAINTENANCE_DATA_FILE)
        except pd.errors.EmptyDataError:
            return pd.DataFrame(columns=["التاريخ", "الوقت", "المبلغ_عنه", "الموقع", "وصف_المشكلة", "الحالة", "ملاحظات_إدارية", "مسار_الصورة"])
    return pd.DataFrame(columns=["التاريخ", "الوقت", "المبلغ_عنه", "الموقع", "وصف_المشكلة", "الحالة", "ملاحظات_إدارية", "مسار_الصورة"])

# دالة لحفظ بيانات مشاكل الصيانة
def save_maintenance_issues(df):
    df.to_csv(MAINTENANCE_DATA_FILE, index=False)

def run():
    st.title("🔧 إدارة قسم الصيانة")
    st.info("هنا يتم تسجيل مشاكل الصيانة، متابعة حالتها، ورفع الصور.")

    st.header("تسجيل مشكلة صيانة جديدة")
    with st.form("new_maintenance_issue_form", clear_on_submit=True):
        issue_date = st.date_input("تاريخ البلاغ:", datetime.date.today())
        issue_time = st.time_input("وقت البلاغ:", datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=3))).time())

        # يمكن تحديد قائمة المواقع من قائمة مركزية
        locations = ["شاطئ كوكيان", "دورات المياه رقم 1", "الكاشيرات الرئيسية", "مركز المراقبة", "المستودع", "أخرى"]
        location = st.selectbox("الموقع المتأثر:", locations, key="issue_location")
        
        reported_by = st.text_input("اسم المبلغ عن المشكلة:", key="reported_by_name")
        
        issue_description = st.text_area("وصف المشكلة التي تحتاج إصلاح:", height=150, key="issue_desc")
        
        # حالة المشكلة (سيتم تحديثها لاحقاً بواسطة الإدارة أو فريق الصيانة)
        # في هذه المرحلة، يمكن للمشرف تسجيلها كـ "جديد"
        issue_status = st.selectbox("حالة المشكلة الأولية:", ["جديد", "قيد المراجعة", "تم الحل"], index=0, key="issue_status_select")

        # رفع الصور
        uploaded_image = st.file_uploader("ارفع صورة للمشكلة (اختياري):", type=["png", "jpg", "jpeg"], key="issue_image_uploader")
        
        submitted = st.form_submit_button("تسجيل بلاغ الصيانة")
        if submitted:
            if issue_description.strip() == "" or reported_by.strip() == "":
                st.error("الرجاء إدخال اسم المبلغ ووصف المشكلة.")
            else:
                image_path = ""
                if uploaded_image is not None:
                    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                    image_name = f"maintenance_{location.replace(' ', '_')}_{timestamp}_{uploaded_image.name}"
                    image_path = os.path.join(MAINTENANCE_IMAGES_DIR, image_name)
                    with open(image_path, "wb") as f:
                        f.write(uploaded_image.getbuffer())
                    st.success(f"تم حفظ الصورة: {image_name}")

                new_issue = pd.DataFrame([{
                    "التاريخ": issue_date.isoformat(),
                    "الوقت": issue_time.strftime("%H:%M"),
                    "المبلغ_عنه": reported_by,
                    "الموقع": location,
                    "وصف_المشكلة": issue_description,
                    "الحالة": issue_status,
                    "ملاحظات_إدارية": "", # ستُملأ بواسطة الإدارة لاحقاً
                    "مسار_الصورة": image_path
                }])
                
                all_issues = load_maintenance_issues()
                if all_issues.empty:
                    updated_issues = new_issue
                else:
                    updated_issues = pd.concat([all_issues, new_issue], ignore_index=True)
                save_maintenance_issues(updated_issues)
                st.success("✅ تم تسجيل بلاغ الصيانة بنجاح!")
                st.rerun()

    st.header("📈 سجلات مشاكل الصيانة")
    
    all_issues_data = load_maintenance_issues()

    if not all_issues_data.empty:
        st.subheader("فلترة مشاكل الصيانة:")
        filter_status = st.selectbox("الحالة:", ["الكل", "جديد", "قيد المراجعة", "تم الحل"], key="maintenance_filter_status")
        filter_location = st.selectbox("الموقع:", ["الكل"] + all_issues_data["الموقع"].unique().tolist(), key="maintenance_filter_location")
        
        filtered_issues = all_issues_data.copy()
        if filter_status != "الكل":
            filtered_issues = filtered_issues[filtered_issues["الحالة"] == filter_status]
        if filter_location != "الكل":
            filtered_issues = filtered_issues[filtered_issues["الموقع"] == filter_location]

        if not filtered_issues.empty:
            st.dataframe(filtered_issues[['التاريخ', 'الوقت', 'المبلغ_عنه', 'الموقع', 'وصف_المشكلة', 'الحالة']].style.set_properties(**{'text-align': 'right', 'font-size': '14px'}), hide_index=True)
            
            # عرض تفاصيل المشكلة (الوصف الكامل والصور) عند اختيارها
            st.subheader("تفاصيل المشكلة المحددة:")
            # استخدم مفتاح فريد لـ selectbox هنا
            selected_issue_id = st.selectbox(
                "اختر مشكلة لعرض التفاصيل:",
                options=[f"{row['الموقع']} - {row['وصف_المشكلة'][:50]}..." for index, row in filtered_issues.iterrows()],
                key="selected_issue_details"
            )
            
            if selected_issue_id:
                # العثور على الصف المطابق للمشكلة المختارة
                selected_row = filtered_issues.loc[filtered_issues.apply(lambda row: f"{row['الموقع']} - {row['وصف_المشكلة'][:50]}..." == selected_issue_id, axis=1)].iloc[0]
                
                st.markdown(f"**التاريخ والوقت:** {selected_row['التاريخ']} - {selected_row['الوقت']}")
                st.markdown(f"**الموقع:** {selected_row['الموقع']}")
                st.markdown(f"**المبلغ عنه:** {selected_row['المبلغ_عنه']}")
                st.markdown(f"**الحالة:** <span style='color: {'red' if selected_row['الحالة'] == 'جديد' else 'orange' if selected_row['الحالة'] == 'قيد المراجعة' else 'green'}; font-weight:bold;'>{selected_row['الحالة']}</span>", unsafe_allow_html=True)
                st.markdown(f"**وصف المشكلة:** {selected_row['وصف_المشكلة']}")
                if selected_row['ملاحظات_إدارية']:
                    st.markdown(f"**ملاحظات إدارية:** {selected_row['ملاحظات_إدارية']}")
                
                if selected_row['مسار_الصورة'] and os.path.exists(selected_row['مسار_الصورة']):
                    st.image(selected_row['مسار_الصورة'], caption=f"صورة المشكلة في {selected_row['الموقع']}", width=400)
                else:
                    st.info("لا توجد صورة مرفوعة لهذه المشكلة.")
        else:
            st.info("لا توجد مشاكل صيانة مطابقة لمعايير الفلترة.")
    else:
        st.info("لا توجد بلاغات صيانة مسجلة حتى الآن.")

# استدعاء الدالة لتشغيل الصفحة
run()
