import streamlit as st
import pandas as pd
import datetime
import os

# اسم الملف لحفظ بيانات الشواطئ
BEACHES_DATA_FILE = "beaches_status_data.csv"

# دالة لتحميل بيانات الشواطئ
def load_beaches_data():
    if os.path.exists(BEACHES_DATA_FILE):
        try:
            expected_columns = [
                "التاريخ", "اسم_المشرف", "اسم_الشاطئ", "حالة_الكاشير", 
                "عدد_المنقذين_المتواجدين", "المفروض_تواجدهم_منقذين", "حالة_ابراج_المراقبة",
                "حالة_الشاطئ_العامة", "موعد_الاخلاء", "موعد_فتح_السباحة", 
                "الحالة_الجوية_والإغلاق", "حالة_الشبك", "حالة_اجهزة_النداء", 
                "حالة_ادوات_السلامة", "حالة_الاسعافات_الاولية", "ملاحظات_عامة"
            ]
            df = pd.read_csv(BEACHES_DATA_FILE)
            for col in expected_columns:
                if col not in df.columns:
                    df[col] = ""
            return df[expected_columns]
        except pd.errors.EmptyDataError:
            return pd.DataFrame(columns=expected_columns)
    return pd.DataFrame(columns=expected_columns)

# دالة لحفظ بيانات الشواطئ
def save_beaches_data(df):
    df.to_csv(BEACHES_DATA_FILE, index=False)

def run():
    st.title("🏖️ إدارة الشواطئ")
    st.info("هنا يتم تسجيل ومتابعة حالة الشواطئ الثلاثة بشكل يومي.")

    # المشرفون المسؤولون (يمكن تعديلهم)
    beach_supervisors = ["المشرف الأول", "المشرف الثاني", "المشرف الثالث"]

    # أسماء الشواطئ
    beaches = ["كوكيان", "الشاطئ الصغير", "الشاطئ الكبير"]

    st.header("تسجيل حالة الشاطئ اليومية")
    with st.form("beach_status_form", clear_on_submit=True):
        entry_date = st.date_input("تاريخ التسجيل:", datetime.date.today())
        responsible_supervisor = st.selectbox("المشرف المسؤول عن الشاطئ:", beach_supervisors, key="beach_supervisor_select")
        
        selected_beach = st.selectbox("اختر الشاطئ:", beaches, key="selected_beach_select")

        st.subheader(f"تفاصيل حالة {selected_beach}:")
        
        col1, col2 = st.columns(2)
        with col1:
            cashier_status = st.selectbox("حالة الكاشير:", ["يعمل", "متعطل", "بطيء", "تحت الصيانة"], key="cashier_status_select")
            num_lifeguards_present = st.number_input("عدد المنقذين المتواجدين:", min_value=0, step=1, key="lifeguards_present_input")
            watchtower_status = st.selectbox("حالة أبراج المراقبة:", ["تعمل", "تحتاج صيانة", "معطلة"], key="watchtower_status_select")
            beach_general_status = st.selectbox("حالة الشاطئ العامة (نظافة):", ["نظيف جداً", "نظيف", "متوسط", "متسخ"], key="beach_general_status_select")
            net_status = st.selectbox("حالة الشبك (الأسوار البحرية):", ["سليم", "ممزق جزئياً", "ممزق كلياً", "يحتاج إصلاح"], key="net_status_select")

        with col2:
            num_lifeguards_expected = st.number_input("العدد المفروض تواجده من المنقذين:", min_value=0, step=1, key="lifeguards_expected_input")
            evacuation_time = st.time_input("موعد الإخلاء المتوقع من الشاطئ:", datetime.time(18, 0), key="evacuation_time_input") # 6 PM
            swimming_open_time = st.time_input("موعد فتح السباحة:", datetime.time(8, 0), key="swimming_open_time_input") # 8 AM
            
            weather_condition = st.selectbox(
                "الحالة الجوية:", 
                ["صافي وجيد للسباحة", "رياح قوية (تحذير)", "أمطار خفيفة", "أمطار غزيرة (إغلاق)", "عواصف (إغلاق)"], 
                key="weather_condition_select"
            )
            # زر راديو لتحديد ما إذا كان الشاطئ مغلقاً بسبب الجو
            is_beach_closed = st.radio("هل الشاطئ مغلق بسبب الظروف الجوية؟", ("نعم", "لا"), key="beach_closed_radio")
            if is_beach_closed == "نعم":
                st.warning("تم إغلاق الشاطئ بسبب الظروف الجوية.")

            loudspeaker_status = st.selectbox("حالة أجهزة النداء:", ["تعمل", "متعطلة جزئياً", "متعطلة كلياً"], key="loudspeaker_status_select")
            safety_tools_status = st.selectbox("حالة أدوات السلامة (الطوافات، الخ):", ["متوفرة وكاملة", "يوجد نقص بسيط", "يوجد نقص كبير", "غير متوفرة"], key="safety_tools_status_select")
            first_aid_status = st.selectbox("حالة الإسعافات الأولية (المحتويات):", ["متوفرة وكاملة", "يوجد نقص بسيط", "يوجد نقص كبير", "غير متوفرة"], key="first_aid_status_select")

        general_notes = st.text_area("ملاحظات إضافية حول الشاطئ اليوم:", height=100, key="beach_notes_text")

        submitted = st.form_submit_button("تسجيل حالة الشاطئ")
        if submitted:
            if not responsible_supervisor.strip():
                st.error("الرجاء اختيار المشرف المسؤول.")
            else:
                new_entry = pd.DataFrame([{
                    "التاريخ": entry_date.isoformat(),
                    "اسم_المشرف": responsible_supervisor,
                    "اسم_الشاطئ": selected_beach,
                    "حالة_الكاشير": cashier_status,
                    "عدد_المنقذين_المتواجدين": num_lifeguards_present,
                    "المفروض_تواجدهم_منقذين": num_lifeguards_expected,
                    "حالة_ابراج_المراقبة": watchtower_status,
                    "حالة_الشاطئ_العامة": beach_general_status,
                    "موعد_الاخلاء": evacuation_time.strftime("%H:%M"),
                    "موعد_فتح_السباحة": swimming_open_time.strftime("%H:%M"),
                    "الحالة_الجوية_والإغلاق": f"{weather_condition} ({'مغلق' if is_beach_closed == 'نعم' else 'مفتوح'})",
                    "حالة_الشبك": net_status,
                    "حالة_اجهزة_النداء": loudspeaker_status,
                    "حالة_ادوات_السلامة": safety_tools_status,
                    "حالة_الاسعافات_الاولية": first_aid_status,
                    "ملاحظات_عامة": general_notes
                }])
                
                all_data = load_beaches_data()
                if all_data.empty:
                    updated_data = new_entry
                else:
                    updated_data = pd.concat([all_data, new_entry], ignore_index=True)
                save_beaches_data(updated_data)
                st.success(f"✅ تم تسجيل حالة شاطئ {selected_beach} بنجاح!")
                st.rerun()

    # قسم عرض ملخص حالة الشواطئ اليومية
    st.header("📊 ملخص حالة الشواطئ اليومية")
    current_day_data = load_beaches_data()
    today_date_str = datetime.date.today().isoformat()
    daily_records = current_day_data[current_day_data["التاريخ"] == today_date_str]

    if not daily_records.empty:
        st.subheader("حالة كل شاطئ:")
        for beach in beaches:
            beach_data = daily_records[daily_records["اسم_الشاطئ"] == beach].iloc[-1:] # نأخذ آخر إدخال لهذا الشاطئ اليوم
            if not beach_data.empty:
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.markdown(f"#### {beach}")
                    current_status = beach_data['حالة_الشاطئ_العامة'].iloc[0]
                    if "متسخ" in current_status: st.error(f"الحالة: {current_status}")
                    elif "متوسط" in current_status: st.warning(f"الحالة: {current_status}")
                    else: st.success(f"الحالة: {current_status}")
                    
                    st.metric(label="منقذون", value=f"{beach_data['عدد_المنقذين_المتواجدين'].iloc[0]} من {beach_data['المفروض_تواجدهم_منقذين'].iloc[0]}")
                    
                with col2:
                    st.write(f"**حالة الكاشير:** {beach_data['حالة_الكاشير'].iloc[0]}")
                    st.write(f"**أبراج المراقبة:** {beach_data['حالة_ابراج_المراقبة'].iloc[0]}")
                    st.write(f"**أجهزة النداء:** {beach_data['حالة_اجهزة_النداء'].iloc[0]}")
                    
                with col3:
                    st.write(f"**حالة الشبك:** {beach_data['حالة_الشبك'].iloc[0]}")
                    st.write(f"**أدوات السلامة:** {beach_data['حالة_ادوات_السلامة'].iloc[0]}")
                    st.write(f"**الإسعافات الأولية:** {beach_data['حالة_الاسعافات_الاولية'].iloc[0]}")
                    
                st.write(f"**الحالة الجوية:** {beach_data['الحالة_الجوية_والإغلاق'].iloc[0]}")
                st.write(f"**موعد الفتح:** {beach_data['موعد_فتح_السباحة'].iloc[0]} - **الإخلاء:** {beach_data['موعد_الاخلاء'].iloc[0]}")
                if beach_data['ملاحظات_عامة'].iloc[0]:
                    st.info(f"**ملاحظات:** {beach_data['ملاحظات_عامة'].iloc[0]}")
                st.markdown("---") # فاصل بين الشواطئ
            else:
                st.info(f"لا توجد بيانات مسجلة لشاطئ {beach} لهذا اليوم.")
        
        st.subheader("جميع سجلات الشواطئ لليوم:")
        st.dataframe(daily_records.style.set_properties(**{'text-align': 'right', 'font-size': '14px'}), use_container_width=True, hide_index=True)

    else:
        st.info("لا توجد بيانات مسجلة للشواطئ لهذا اليوم حتى الآن.")

# استدعاء الدالة لتشغيل الصفحة
run()
