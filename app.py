import streamlit as st
import pandas as pd

st.set_page_config(page_title="نظام إدارة الواجهة البحرية", layout="wide")

st.title("📋 نظام إدارة الواجهة البحرية – Creek Obhur")

st.markdown("يرجى لصق رسالة المهام اليومية أدناه 👇")

# إدخال الرسالة
message = st.text_area("📩 لصق الرسالة هنا:", height=300)

if st.button("🔍 تحليل الرسالة"):
    lines = message.strip().split("\n")
    tasks = []

    for line in lines:
        line = line.strip()
        if line and not line.startswith("السلام") and not line.startswith("الله يعطيكم"):
            tasks.append([line])

    # تجميع كشوفات الدوام
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

    # عرض النتائج
    df = pd.DataFrame(cleaned_tasks, columns=["المهمة"])
    df.index = [f"مهمة {i+1}" for i in range(len(df))]
    st.dataframe(df, use_container_width=True)
