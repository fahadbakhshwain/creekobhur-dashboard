import streamlit as st
import pandas as pd
import datetime
import os

# اسم الملف لحفظ بيانات المستودع
WAREHOUSE_DATA_FILE = "warehouse_inventory_data.csv"

# دالة لتحميل بيانات المستودع
def load_warehouse_data():
    if os.path.exists(WAREHOUSE_DATA_FILE):
        try:
            expected_columns = [
                "التاريخ", "وقت_التسجيل", "المسؤول", "نوع_العملية", 
                "الصنف", "الكمية", "الوحدة", "المورد", "ملاحظات"
            ]
            df = pd.read_csv(WAREHOUSE_DATA_FILE)
            for col in expected_columns:
                if col not in df.columns:
                    df[col] = "" 
            return df[expected_columns]
        except pd.errors.EmptyDataError:
            return pd.DataFrame(columns=expected_columns)
    return pd.DataFrame(columns=expected_columns)

# دالة لحفظ بيانات المستودع
def save_warehouse_data(df):
    df.to_csv(WAREHOUSE_DATA_FILE, index=False)

def run():
    st.title("📦 إدارة المستودع")
    st.info("هنا يتم تسجيل ومتابعة حركة المخزون من المواد المستوردة.")

    warehouse_personnel = ["أمين المستودع", "المشرف الأول", "المشرف الثاني"]
    item_types = ["مواد نظافة", "مناديل", "مياه", "قرطاسية", "أخرى"]
    units = ["كرتون", "حبة", "لتر", "كجم", "عبوة"]
    suppliers = ["مورد 1", "مورد 2", "مورد 3", "غير محدد"]

    st.header("تسجيل حركة مخزون جديدة (وارد/صادر)")
    with st.form("warehouse_entry_form", clear_on_submit=True):
        entry_date = st.date_input("تاريخ العملية:", datetime.date.today())
        entry_time = st.time_input("وقت التسجيل:", datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=3))).time())
        responsible_person = st.selectbox("المسؤول عن العملية:", warehouse_personnel, key="responsible_person_select")
        
        operation_type = st.radio("نوع العملية:", ["وارد (استلام)", "صادر (صرف/نقص)"], key="operation_type_radio")

        item_category = st.selectbox("الصنف:", item_types, key="item_category_select")
        item_name = st.text_input("اسم المادة (مثال: ديتول، مناديل وجه 500):", key="item_name_input")
        quantity = st.number_input("الكمية:", min_value=0.0, step=0.1, format="%.2f", key="quantity_input")
        unit = st.selectbox("الوحدة:", units, key="unit_select")
        
        if operation_type == "وارد (استلام)":
            supplier = st.selectbox("المورد:", suppliers, key="supplier_select")
        else:
            supplier = "---" # لا يوجد مورد في عملية الصرف

        notes = st.text_area("ملاحظات إضافية:", height=100, key="warehouse_notes_text")

        submitted = st.form_submit_button("تسجيل حركة المخزون")
        if submitted:
            if not item_name.strip() or quantity <= 0:
                st.error("الرجاء إدخال اسم المادة وكمية صحيحة.")
            else:
                new_entry = pd.DataFrame([{
                    "التاريخ": entry_date.isoformat(),
                    "وقت_التسجيل": entry_time.strftime("%H:%M"),
                    "المسؤول": responsible_person,
                    "نوع_العملية": operation_type,
                    "الصنف": item_category,
                    "اسم_المادة": item_name, # إضافة هذا العمود للحفظ
                    "الكمية": quantity,
                    "الوحدة": unit,
                    "المورد": supplier,
                    "ملاحظات": notes
                }])
                
                all_data = load_warehouse_data()
                if all_data.empty:
                    updated_data = new_entry
                else:
                    updated_data = pd.concat([all_data, new_entry], ignore_index=True)
                save_warehouse_data(updated_data)
                st.success("✅ تم تسجيل حركة المخزون بنجاح!")
                st.rerun()

    # قسم عرض ملخص المخزون اليومي
    st.header("📊 ملخص حركة المخزون اليومي")
    current_day_data = load_warehouse_data()
    today_date_str = datetime.date.today().isoformat()
    daily_records = current_day_data[current_day_data["التاريخ"] == today_date_str]

    if not daily_records.empty:
        st.subheader("إجمالي الوارد والصادر اليوم:")
        total_in = daily_records[daily_records["نوع_العملية"] == "وارد (استلام)"]["الكمية"].sum()
        total_out = daily_records[daily_records["نوع_العملية"] == "صادر (صرف/نقص)"]["الكمية"].sum()
        
        col1, col2 = st.columns(2)
        col1.metric("إجمالي الوارد اليوم", f"{total_in:.2f}")
        col2.metric("إجمالي الصادر اليوم", f"{total_out:.2f}")

        st.subheader("تفاصيل حركة المخزون حسب الصنف:")
        # تلخيص الكميات حسب الصنف ونوع العملية
        inventory_summary = daily_records.groupby(["الصنف", "نوع_العملية"])["الكمية"].sum().unstack(fill_value=0)
        st.dataframe(inventory_summary.style.set_properties(**{'text-align': 'right', 'font-size': '14px'}), use_container_width=True)
        
        st.subheader("جميع حركات المخزون المسجلة اليوم:")
        st.dataframe(daily_records.style.set_properties(**{'text-align': 'right', 'font-size': '14px'}), use_container_width=True, hide_index=True)

        st.subheader("🔴 الإبلاغ عن نقص أو ملاحظات هامة:")
        # عرض فقط البنود التي تحتوي على ملاحظات أو هي من نوع "صادر" مع ملاحظات
        # هذا الجزء يعتمد على الملاحظات المدخلة
        critical_notes = daily_records[(daily_records["نوع_العملية"] == "صادر (صرف/نقص)") | (daily_records["ملاحظات"].str.strip() != "")]
        if not critical_notes.empty:
            for index, row in critical_notes.iterrows():
                st.warning(f"**صنف: {row['اسم_المادة']}** ({row['نوع_العملية']}) - ملاحظات: {row['ملاحظات']}")
                if row['نوع_العملية'] == "صادر (صرف/نقص)":
                    st.error(f"تم صرف/تسجيل نقص بكمية: {row['الكمية']} {row['الوحدة']}")
                st.markdown("---")
        else:
            st.info("لا توجد بلاغات نقص أو ملاحظات هامة اليوم.")


    else:
        st.info("لا توجد حركات مخزون مسجلة لهذا اليوم حتى الآن.")

# استدعاء الدالة لتشغيل الصفحة
run()
