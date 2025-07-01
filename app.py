import streamlit as st

# إعداد الصفحة
st.set_page_config(
    page_title="Creek Obhur - نظام إدارة الواجهة البحرية",
    page_icon="🏖️",
    layout="wide"
)

# --- مسار الشعار (نفس المسار الذي استخدمناه للسايدبار) ---
LOGO_PATH = "logo.jpg" # <--- تأكد أن هذا المسار صحيح تماماً لملفك logo.jpg

# --- إضافة الشعار في الواجهة الرئيسية فوق في اليمين ---
# سنستخدم عمودين: واحد للمحتوى الرئيسي (العنوان) وواحد للشعار في اليمين
main_col, logo_col = st.columns([0.7, 0.3]) # 0.7 للعناوين، 0.3 للشعار (يمكن تعديل النسب)

with main_col:
    # عنوان الصفحة الرئيسي
    st.markdown("## 🏖️ نظام إدارة الواجهة البحرية - Creek Obhur")
    st.markdown("### 👇 اختر القسم الذي تريد الدخول إليه:")

with logo_col:
    # عرض الشعار في العمود الأيمن
    # يمكن التحكم في عرض الصورة هنا مباشرة
    st.image(LOGO_PATH, width=150) # <--- يمكنك تعديل الـ width حسب حجم اللوجو المناسب

# --- إضافة الشعار إلى الشريط الجانبي (يبقى كما هو) ---
st.sidebar.image(LOGO_PATH, use_column_width=True) 
st.sidebar.markdown("---") 


# مربعات الأقسام
col1, col2, col3 = st.columns(3) 

with col1:
    if st.button("📋 المهام اليومية", use_container_width=True):
        st.switch_page("pages/المهام_اليومية.py")

    if st.button("🚽 دورات المياه", use_container_width=True):
        st.switch_page("pages/دورات_المياه.py")

    if st.button("🌴 الشواطئ", use_container_width=True):
        st.switch_page("pages/الشواطئ.py")

    if st.button("📦 المستودع", use_container_width=True):
        st.switch_page("pages/المستودع.py")

with col2:
    if st.button("🧑‍🤝‍🧑 الموظفين", use_container_width=True):
        st.switch_page("pages/الموظفين.py")

    if st.button("🏢 الإدارة", use_container_width=True):
        st.switch_page("pages/الإدارة.py")

    if st.button("🛡️ الشركة الأمنية", use_container_width=True):
        st.switch_page("pages/الشركة_الامنية.py")

    if st.button("🚌 السائقون والباصات", use_container_width=True):
        st.switch_page("pages/السائقون.py")

with col3:
    if st.button("🔧 قسم الصيانة", use_container_width=True):
        st.switch_page("pages/قسم_الصيانة.py")

    if st.button("🌳 قسم الزراعة", use_container_width=True):
        st.switch_page("pages/قسم_الزراعة.py")
        
    if st.button("💵 المحاسبة", use_container_width=True):
        st.switch_page("pages/المحاسبة.py")
        
    if st.button("👥 الموارد البشرية", use_container_width=True):
        st.switch_page("pages/الموارد_البشرية.py")
        
    if st.button("👩‍💼 مساعدة المديرة", use_container_width=True):
        st.switch_page("pages/مساعدة_المديرة.py")

    if st.button("📊 التقارير الشاملة", use_container_width=True):
        st.switch_page("pages/التقارير_الشاملة.py")
        
# ملاحظة
st.markdown("---")
st.info("🛠️ هذا النظام تحت التطوير - يرجى إبلاغ الإدارة بأي ملاحظات.")
  
