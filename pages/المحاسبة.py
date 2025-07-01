import streamlit as st
import pandas as pd
import datetime
import os
import plotly.express as px # تم إضافة هذه المكتبة للرسوم البيانية

# اسم الملف لحفظ البيانات المالية
FINANCIAL_DATA_FILE = "financial_data.csv"

# دالة لتحميل البيانات المالية
def load_financial_data():
    # تعريف الأعمدة المتوقعة هنا لتكون متاحة دائماً
    expected_columns = [
        "التاريخ", "البند", "النوع", "القيمة", "الشاطئ", "ملاحظات", 
        "تم_التحقق_منه" 
    ]
    if os.path.exists(FINANCIAL_DATA_FILE):
        try:
            df = pd.read_csv(FINANCIAL_DATA_FILE)
            for col in expected_columns:
                if col not in df.columns:
                    df[col] = "" 
            return df[expected_columns]
        except pd.errors.EmptyDataError:
            return pd.DataFrame(columns=expected_columns)
    return pd.DataFrame(columns=expected_columns)

# دالة لحفظ البيانات المالية
def save_financial_data(df):
    df.to_csv(FINANCIAL_DATA_FILE, index=False)

def run():
    st.title("💵 إدارة المحاسبة")
    st.info("هنا يتم تسجيل ومتابعة الإيرادات، العهد، الرواتب، والمصروفات.")

    financial_categories = ["إيرادات", "عهد", "رواتب", "مصروفات"]
    beaches = ["كوكيان", "الشاطئ الصغير", "الشاطئ الكبير", "عام"] 

    st.header("تسجيل بند مالي جديد")
    with st.form("financial_entry_form", clear_on_submit=True):
        entry_date = st.date_input("تاريخ البند:", datetime.date.today())
        
        item_type = st.selectbox("نوع البند:", financial_categories, key="item_type_select")
        
        item_description = st.text_input("وصف البند (مثلاً: إيراد كاشير، مصروف نظافة):", key="item_description_input")
        value = st.number_input("القيمة (ريال سعودي):", min_value=0.0, step=0.01, format="%.2f", key="value_input")
        
        if item_type in ["إيرادات", "عهد"]:
            item_beach = st.selectbox("الشاطئ المعني:", beaches[:-1], key="item_beach_select")
        else:
            item_beach = st.selectbox("الشاطئ المعني (اختياري/عام):", beaches, index=len(beaches)-1, key="item_beach_select_other")

        notes = st.text_area("ملاحظات إضافية:", height=100, key="financial_notes_text")

        submitted = st.form_submit_button("تسجيل البند المالي")
        if submitted:
            if not item_description.strip() or value <= 0:
                st.error("الرجاء إدخال وصف وقيمة صحيحة للبند.")
            else:
                new_entry = pd.DataFrame([{
                    "التاريخ": entry_date.isoformat(),
                    "البند": item_description,
                    "النوع": item_type,
                    "القيمة": value,
                    "الشاطئ": item_beach,
                    "ملاحظات": notes,
                    "تم_التحقق_منه": "لا" 
                }])
                
                all_data = load_financial_data()
                if all_data.empty:
                    updated_data = new_entry
                else:
                    updated_data = pd.concat([all_data, new_entry], ignore_index=True)
                save_financial_data(updated_data)
                st.success("✅ تم تسجيل البند المالي بنجاح!")
                st.rerun()

    # قسم عرض الملخص المالي
    st.header("📊 ملخص مالي يومي")
    current_day_data = load_financial_data()
    today_date_str = datetime.date.today().isoformat()
    daily_records = current_day_data[current_day_data["التاريخ"] == today_date_str]

    if not daily_records.empty:
        # إجمالي الإيرادات والمصروفات لليوم
        total_income = daily_records[daily_records["النوع"] == "إيرادات"]["القيمة"].sum()
        total_expenses = daily_records[daily_records["النوع"] == "مصروفات"]["القيمة"].sum()
        total_salaries = daily_records[daily_records["النوع"] == "رواتب"]["القيمة"].sum()
        total_dues = daily_records[daily_records["النوع"] == "عهد"]["القيمة"].sum()

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("إجمالي الإيرادات اليوم", f"{total_income:.2f} ر.س", delta_color="normal")
        col2.metric("إجمالي المصروفات اليوم", f"{total_expenses:.2f} ر.س", delta_color="inverse")
        col3.metric("إجمالي الرواتب اليوم", f"{total_salaries:.2f} ر.س", delta_color="inverse")
        col4.metric("إجمالي العهد اليوم", f"{total_dues:.2f} ر.س", delta_color="normal")

        st.subheader("تفاصيل مالية حسب الشاطئ والنوع:")
        financial_summary_by_beach_type = daily_records.groupby(["الشاطئ", "النوع"])["القيمة"].sum().unstack(fill_value=0)
        if not financial_summary_by_beach_type.empty:
            st.dataframe(financial_summary_by_beach_type.style.set_properties(**{'text-align': 'right', 'font-size': '14px'}), use_container_width=True)
        else:
            st.info("لا توجد تفاصيل مالية مفلترة لهذا اليوم.")
        
        # --- الرسم البياني للمبيعات (الإيرادات) حسب الشاطئ ---
        st.subheader("📈 إيرادات الشواطئ اليوم")
        # فلترة الإيرادات فقط وتجميعها حسب الشاطئ
        daily_income_by_beach = daily_records[daily_records["النوع"] == "إيرادات"].groupby("الشاطئ")["القيمة"].sum().reset_index()
        
        if not daily_income_by_beach.empty:
            # التأكد من وجود الشواطئ الثلاثة الرئيسية حتى لو لم يكن بها إيرادات
            all_beaches_df = pd.DataFrame({"الشاطئ": ["كوكيان", "الشاطئ الصغير", "الشاطئ الكبير"], "القيمة": 0.0})
            daily_income_by_beach = pd.concat([daily_income_by_beach, all_beaches_df]).groupby("الشاطئ")["القيمة"].sum().reset_index()
            
            # فلترة "عام" إذا لم يكن شاطئاً
            daily_income_by_beach = daily_income_by_beach[daily_income_by_beach["الشاطئ"] != "عام"]

            fig = px.bar(
                daily_income_by_beach, 
                x="الشاطئ", 
                y="القيمة", 
                title="إجمالي الإيرادات حسب الشاطئ (اليوم)",
                labels={"الشاطئ": "اسم الشاطئ", "القيمة": "الإيرادات (ر.س)"},
                color_discrete_sequence=px.colors.qualitative.Pastel # لون جذاب
            )
            fig.update_layout(xaxis_title_font=dict(size=14), yaxis_title_font=dict(size=14))
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("لا توجد إيرادات مسجلة للشواطئ حتى الآن لعرض الرسم البياني.")

        st.subheader("جميع البنود المالية المسجلة اليوم:")
        st.dataframe(daily_records[['التاريخ', 'البند', 'النوع', 'القيمة', 'الشاطئ', 'ملاحظات', 'تم_التحقق_منه']].style.set_properties(**{'text-align': 'right', 'font-size': '14px'}), use_container_width=True, hide_index=True)

        st.subheader("تحديث حالة التحقق من البنود:")
        editable_financial_data = load_financial_data() 
        editable_financial_data_today = editable_financial_data[editable_financial_data["التاريخ"] == today_date_str].copy()

        if not editable_financial_data_today.empty:
            st.markdown("يمكنك تعديل حالة **'تم التحقق منه'** مباشرة في الجدول:")
            edited_df = st.data_editor(
                editable_financial_data_today,
                column_config={
                    "تم_التحقق_منه": st.column_config.CheckboxColumn("تم التحقق منه؟", default=False),
                    "التاريخ": st.column_config.Column("التاريخ", disabled=True),
                    "البند": st.column_config.Column("البند", disabled=True),
                    "النوع": st.column_config.Column("النوع", disabled=True),
                    "القيمة": st.column_config.Column("القيمة", disabled=True),
                    "الشاطئ": st.column_config.Column("الشاطئ", disabled=True),
                    "ملاحظات": st.column_config.Column("ملاحظات", disabled=True),
                },
                hide_index=True,
                use_container_width=True,
                num_rows="dynamic" 
            )

            if st.button("حفظ تحديثات التحقق", key="save_verification_updates"):
                all_financial_data_for_save = load_financial_data()
                # تم تصحيح هذا السطر: كان غير مكتمل
                updated_all_data = pd.concat([all_financial_data_for_save[all_financial_data_for_save["التاريخ"] != today_date_str], edited_df], ignore_index=True)
                save_financial_data(updated_all_data)
                st.success("✅ تم حفظ تحديثات التحقق بنجاح!")
                st.rerun()

        else:
            st.info("لا توجد بنود مالية اليوم يمكن التحقق منها.")

    else:
        st.info("لا توجد بنود مالية مسجلة لهذا اليوم حتى الآن.")

# استدعاء الدالة لتشغيل الصفحة
run()
   
      
        
             
