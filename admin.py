import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Creek Obhur Admin", layout="wide")
st.title("🛠️ لوحة التحكم - Creek Obhur")

st.markdown("✉️ **الصق رسالة المديرة اليومية أدناه:**")

# حقل لصق الرسالة
message = st.text_area("📩 الرسالة", height=300)

if st.button("🔍 تحليل الرسالة"):
    lines = message.strip().split("\n")
    tasks = []

    for line in lines:
        line = line.strip()
        if line and not line.startswith("السلام") and not line.startswith("الله يعطيكم"):
            tasks.append([line])

    # تنظيف المهام المتكررة الخاصة بكشوفات الدوام
    cleaned_tasks = []
    skip_next = False
    for i, task in enumerate(tasks):
        t = task[0]
        if "كشوفات الدوام" in t:
            cleaned_tasks.append(["طباعة كشوفات دوام المنقذين + العمالة + الكاشيرات ووضعها في الأكشاك"])
            skip_next = True
        elif skip_next and ("المنقذين" in t or "العمالة" in t or "الكاشيرات" in t or "تنطبع" in t):
            continue
        else:
            cleaned_tasks.append([t])
            skip_next = False

    # تحويلها إلى DataFrame
    df = pd.DataFrame(cleaned_tasks, columns=["المهمة"])
    df.index = [f"مهمة {i+1}" for i in range(len(df))]

    # حفظ آخر جدول في ملف CSV
    df.to_csv("last_message.csv", index=False)

    st.success("✅ تم تحليل الرسالة وحفظ الجدول بنجاح")
    st.dataframe(df, use_container_width=True)
