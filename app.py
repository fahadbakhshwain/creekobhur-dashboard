import streamlit as st

# إعداد الصفحة
st.set_page_config(
    page_title="Creek Obhur - نظام إدارة الواجهة البحرية",
    page_icon="🏖️",
    layout="wide"
)

# --- إضافة الشعار إلى الشريط الجانبي ---
# تأكد أن المسار هنا صحيح تماماً بناءً على مكان رفعك للشعار في GitHub
# بما أنك رفعت ملف الشعار logo.jpg في الدليل الرئيسي، فالمسار سيكون كالتالي:
LOGO_PATH = "logo.jpg" # <--- تأكد أن هذا المسار صحيح تماماً
                        # يجب أن يكون اسم الملف مطابقاً لحالة الأحرف (logo.jpg وليس Logo.jpg مثلاً)

st.sidebar.image(LOGO_PATH, use_column_width=True) # use_column_width=True يضبط العرض ليناسب العمود

# إضافة مسافة أو خط فاصل بعد اللوجو (اختياري)
st.sidebar.markdown("---") 

# عنوان الصفحة الرئيسي
st.markdown("## 🏖️ نظام إدارة الواجهة البحرية - Creek Obhur")
st.markdown("### 👇 اختر القسم الذي تريد الدخول إليه:")

# مربعات الأقسام
# سنستخدم 3 أعمدة بدلاً من 2 ليكون هناك مجال لأزرار أكثر في كل سطر
col1, col2, col3 = st.columns(3) # <--- تم التغيير هنا إلى 3 أعمدة

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

with col3: # <--- هذا العمود الجديد للأزرار المتبقية
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

    if st.button("📊 التقارير الشاملة", use_container_width=True): # زر التقارير الشاملة
        st.switch_page("pages/التقارير_الشاملة.py")
        
    # إذا كان هناك زر الطوارئ وتريد إضافته
    # if st.button("🚨 الطوارئ", use_container_width=True):
    #     st.switch_page("pages/الطوارئ.py")

# ملاحظة
st.markdown("---")
st.info("🛠️ هذا النظام تحت التطوير - يرجى إبلاغ الإدارة بأي ملاحظات.")
 
