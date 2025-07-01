import streamlit as st
import pandas as pd
import datetime
import os

# --- الدوال المساعدة لتحميل البيانات (يمكن أن نربطها بملفات CSV أخرى مستقبلاً) ---

# دالة لتحميل بيانات نظافة دورات المياه (افتراضية حالياً)
def load_toilet_cleaning_data():
    # في البروتوتايب، نستخدم بيانات وهمية. لاحقاً يمكن قراءتها من ملف CSV.
    data = {
        "رقم_المياه": ["3", "2", "1", "4"],
        "النوع": ["نساء", "رجال", "رجال", "نساء"],
        "مرات_التنظيف_اليوم": [1, 4, 2, 3],
        "نواقص_مواد": ["لا يوجد", "لا يوجد", "ديتول، صابون، مناديل", "مناديل"]
    }
    df = pd.DataFrame(data)
    # يمكننا فلترة لليوم الحالي إذا أردنا
    # df['التاريخ'] = pd.to_datetime(df['التاريخ'])
    # df = df[df['التاريخ'].dt.date == datetime.date.today()]
    return df

# دالة لتحميل المهام الإدارية المعلقة (افتراضية حالياً)
def load_admin_tasks():
    # بيانات وهمية للمهام الإدارية
    tasks = [
        {"المهمة": "مراجعة كشوفات الدوام للمنقذين والعمالة والكاشيرات.", "الحالة": "معلقة", "الموعد_النهائي": "2025-07-03"},
        {"المهمة": "متابعة حل مشكلة الكاشير الصغير واستبدال الطابعات.", "الحالة": "معلقة", "الموعد_النهائي": "2025-07-02"},
        {"المهمة": "التأكد من إغلاق أبواب الكاشيرات يومياً وتصويرها.", "الحالة": "مستمرة", "الموعد_النهائي": "يومي"},
        {"المهمة": "مراجعة تقرير نظافة البرج والإشراف عليه.", "الحالة": "معلقة", "الموعد_النهائي": "2025-07-01"}
    ]
    return pd.DataFrame(tasks)

# --- الكود الرئيسي لصفحة الإدارة ---

def run():
    st.title("🏢 لوحة تحكم الإدارة")
    st.info("هنا يتم عرض ملخص للإنجازات والمهام الإدارية المعلقة.")

    # --- قسم لوحة الإنجازات/الملخص (الكروت - Cards) ---
    st.header("ملخص الأداء والإنجازات اليومية")

    # جلب البيانات الوهمية
    toilet_data = load_toilet_cleaning_data()

    # إنشاء كروت بناءً على البيانات
    col1, col2, col3 = st.columns(3)

    with col1:
        st.subheader("دورات المياه - نساء")
        toilet_women = toilet_data[toilet_data["النوع"] == "نساء"]
        total_cleaning_women = toilet_women["مرات_التنظيف_اليوم"].sum()
        st.metric(label="إجمالي مرات التنظيف (نساء)", value=f"{total_cleaning_women} مرة")
        if not toilet_women[toilet_women["نواقص_مواد"] != "لا يوجد"].empty:
            st.warning("يوجد نواقص في مواد نظافة دورات المياه (نساء).")

    with col2:
        st.subheader("دورات المياه - رجال")
        toilet_men = toilet_data[toilet_data["النوع"] == "رجال"]
        total_cleaning_men = toilet_men["مرات_التنظيف_اليوم"].sum()
        st.metric(label="إجمالي مرات التنظيف (رجال)", value=f"{total_cleaning_men} مرة")
        if not toilet_men[toilet_men["نواقص_مواد"] != "لا يوجد"].empty:
            st.warning("يوجد نواقص في مواد نظافة دورات المياه (رجال).")

    with col3:
        st.subheader("نواقص مواد النظافة")
        missing_items = toilet_data[toilet_data["نواقص_مواد"] != "لا يوجد"]
        if not missing_items.empty:
            st.error(f"يوجد نواقص في {len(missing_items)} دورة مياه.")
            for index, row in missing_items.iterrows():
                st.write(f"- مياه رقم {row['رقم_المياه']} ({row['النوع']}): {row['نواقص_مواد']}")
        else:
            st.success("لا توجد نواقص في مواد النظافة حالياً.")

    st.markdown("---") # خط فاصل

    # --- قسم المهام الإدارية المعلقة ---
    st.header("المهام الإدارية المعلقة")

    admin_tasks = load_admin_tasks()

    if not admin_tasks.empty:
        # عرض المهام في جدول أو في بطاقات فردية حسب الرغبة
        # لعرضها كبطاقات منفصلة لكل مهمة
        for index, task in admin_tasks.iterrows():
            st.markdown(f"**المهمة:** {task['المهمة']}")
            st.markdown(f"**الحالة:** <span style='color: {'red' if task['الحالة'] == 'معلقة' else 'orange'}; font-weight:bold;'>{task['الحالة']}</span>", unsafe_allow_html=True)
            if pd.notna(task['الموعد_النهائي']): # تحقق مما إذا كان الموعد النهائي موجوداً
                st.markdown(f"**الموعد النهائي:** {task['الموعد_النهائي']}")
            st.markdown("---") # خط فاصل بين المهام
    else:
        st.info("لا توجد مهام إدارية معلقة حالياً.")


# استدعاء الدالة لتشغيل الصفحة
run()
