import streamlit as st
import pandas as pd
import os
from datetime import datetime

# --- 1. ຕັ້ງຄ່າເວັບໄຊ ---
st.set_page_config(page_title="Phonsouk AI Ultimate Planner", page_icon="💰", layout="wide")
FILE_NAME = 'shop_database_vfinal.csv'

st.markdown("""
    <style>
    .main-header {background-color:#002B36; padding:20px; border-radius:15px; text-align:center; border: 2px solid #268BD2; color:white;}
    .income-section {background-color:#E8F5E9; padding:15px; border-radius:10px; border-left:5px solid #2E7D32;}
    .expense-section {background-color:#FFEBEE; padding:15px; border-radius:10px; border-left:5px solid #C62828;}
    </style>
    <div class="main-header">
        <h1>💰 ລະບົບບັນຊີ & AI ວາງແຜນຊີວິດ ປ້າພອນສຸກ</h1>
        <p>ລະບົບວິເຄາະການເງິນຄົບວົງຈອນ (ລາຍອາທິດ, ລາຍເດືອນ, ລາຍປີ)</p>
    </div>
    """, unsafe_allow_html=True)

# --- 2. ສ່ວນປ້ອນຂໍ້ມູນ (ຈັດກຸ່ມໃໝ່ໃຫ້ຄົບຕາມທີ່ປ້າຂໍ) ---
st.write("### 📝 ບັນທຶກລາຍຮັບ-ລາຍຈ່າຍມື້ນີ້")
with st.form("finance_form"):
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="income-section"><h4>🟢 ລາຍຮັບ (Income)</h4></div>', unsafe_allow_html=True)
        in1 = st.number_input("ເງິນເດືອນຈາກການທຳງານ", min_value=0, step=50000)
        in2 = st.number_input("ລາຍຮັບຈາກການເປັນ Creator", min_value=0, step=10000)
        in3 = st.number_input("ລາຍຮັບຈາກຂາຍຂອງຍ່ອຍ", min_value=0, step=5000)
        in4 = st.number_input("ລາຍຮັບຈາກຮັບຕັດຫຍິບ", min_value=0, step=5000)
        in5 = st.number_input("ລາຍຮັບຈາກຕູ້ກົດນ້ຳ", min_value=0, step=2000)
        in6 = st.number_input("ລາຍຮັບຈາກຕູ້ຊັກຜ້າ", min_value=0, step=5000)

    with col2:
        st.markdown('<div class="expense-section"><h4>🔴 ລາຍຈ່າຍ (Expense)</h4></div>', unsafe_allow_html=True)
        ex1 = st.number_input("ຄ່າອາຫານ ແລະ ເຄື່ອງບໍລິໂພກ", min_value=0, step=5000)
        ex2 = st.number_input("ຄ່າເຊົ່າທີ່ຢູ່", min_value=0, step=100000)
        ex3 = st.number_input("ຄ່າໄຟຟ້າ-ນໍ້າ-ອິນເຕີເນັດ", min_value=0, step=5000)
        ex4 = st.number_input("ຄ່າເດີນທາງ (ນໍ້າມັນ/ລົດຈ້າງ)", min_value=0, step=5000)
        ex5 = st.number_input("ຄ່າການສຶກສາລູກ", min_value=0, step=50000)
        ex6 = st.number_input("ຄ່າປິ່ນປົວ/ຢາພະຍາດ", min_value=0, step=5000)
        ex7 = st.number_input("ຄ່າເສື້ອຜ້າ ແລະ ຂອງໃຊ້ສ່ວນຕົວ", min_value=0, step=5000)
        ex8 = st.number_input("ຄ່າໂທລະສັບ ແລະ ບັນເທີງ", min_value=0, step=5000)
        ex9 = st.number_input("ຄ່າຜ່ອນຊຳລະໜີ້ (ລົດ ແລະ ອື່ນໆ)", min_value=0, step=50000)
        ex10 = st.number_input("ຄ່າຊື້ເຄື່ອງເຂົ້າຮ້ານ", min_value=0, step=10000)

    submit = st.form_submit_button("🚀 ບັນທຶກ ແລະ ໃຫ້ AI ວາງແຜນໃຫ້ປ້າ", use_container_width=True)

if submit:
    now = datetime.now()
    total_in = in1+in2+in3+in4+in5+in6
    total_ex = ex1+ex2+ex3+ex4+ex5+ex6+ex7+ex8+ex9+ex10
    new_data = {
        'Date': now.strftime("%Y-%m-%d %H:%M"),
        'Week': now.isocalendar()[1],
        'Month': now.strftime("%m-%Y"),
        'Year': str(now.year),
        'Total_In': total_in, 'Total_Ex': total_ex, 'Profit': total_in - total_ex,
        'Salary': in1, 'Creator': in2, 'Retail': in3, 'Sewing': in4, 'Water_Machine': in5, 'Laundry': in6,
        'Food': ex1, 'Rent': ex2, 'Utilities': ex3, 'Travel': ex4, 'Education': ex5, 'Medical': ex6, 'Personal': ex7, 'Entertainment': ex8, 'Debt': ex9, 'Stock': ex10
    }
    pd.DataFrame([new_data]).to_csv(FILE_NAME, mode='a', index=False, header=not os.path.exists(FILE_NAME))
    st.balloons(); st.success("AI ບັນທຶກຮຽບຮ້ອຍແລ້ວ!")

# --- 3. ສ່ວນ AI ລາຍງານ ແລະ ວາງແຜນ (Weekly/Monthly/Yearly) ---
if os.path.exists(FILE_NAME):
    df = pd.read_csv(FILE_NAME)
    st.markdown("---")
    report_type = st.radio("📊 ເບິ່ງລາຍງານ AI:", ["ລາຍອາທິດ", "ລາຍເດືອນ", "ລາຍປີ"], horizontal=True)
    
    now = datetime.now()
    if report_type == "ລາຍອາທິດ": summary = df[df['Week'] == now.isocalendar()[1]]; label = "ອາທິດນີ້"
    elif report_type == "ລາຍເດືອນ": summary = df[df['Month'] == now.strftime("%m-%Y")]; label = "ເດືອນນີ້"
    else: summary = df[df['Year'] == str(now.year)]; label = f"ປີ {now.year}"

    c1, c2, c3 = st.columns(3)
    c1.metric(f"ລາຍຮັບ {label}", "{:,.0f} ກີບ".format(summary['Total_In'].sum()))
    c2.metric(f"ລາຍຈ່າຍ {label}", "{:,.0f} ກີບ".format(summary['Total_Ex'].sum()))
    c3.metric(f"ກຳໄລ {label}", "{:,.0f} ກີບ".format(summary['Profit'].sum()))

    # --- 4. ສະໝອງ AI ວິເຄາະຫາຊ່ອງທາງປະຢັດ ---
    st.markdown("### 🧠 AI Analysis: ຊ່ອງທາງປະຢັດ & ແຜນວຽກມືອາຊີບ")
    col_ai1, col_ai2 = st.columns(2)

    with col_ai1:
        st.info("**💡 ຊ່ອງທາງປະຢັດຂອງປ້າ:**")
        if summary['Food'].sum() > (summary['Total_In'].sum() * 0.4):
            st.warning("⚠️ AI ກວດພົບ: ຄ່າອາຫານສູງເກີນໄປ! ລອງຫຼຸດການກິນນອກບ້ານເດີ້ປ້າ.")
        if summary['Debt'].sum() > 0:
            st.write(f"📌 ປ້າມີພາລະໜີ້ສິນ {summary['Debt'].sum():,.0f} ກີບ. AI ແນະນຳໃຫ້ປ້າຈ່າຍໃຫ້ຕົງເວລາເພື່ອຫຼີກລ່ຽງດອກເບ້ຍເພີ່ມ.")
        if summary['Utilities'].sum() > 500000:
            st.write("📌 ຄ່າໄຟ-ນໍ້າ ສູງ! ກວດເບິ່ງວ່າປິດຕູ້ກົດນໍ້າ ຫຼື ຈັກຊັກຜ້າຕອນບໍ່ມີຄົນໃຊ້ຫຼືບໍ່.")

    with col_ai2:
        st.success("**🚀 ແຜນວາງແຜນອາຊີບ:**")
        sources = {'ຕັດຫຍິບ': summary['Sewing'].sum(), 'Creator': summary['Creator'].sum(), 'ຕູ້ກົດນໍ້າ/ຊັກຜ້າ': summary['Water_Machine'].sum() + summary['Laundry'].sum()}
        best_source = max(sources, key=sources.get)
        st.write(f"✨ ວຽກທີ່ເຮັດເງິນໃຫ້ປ້າຫຼາຍທີ່ສຸດຄື: **{best_source}**")
        st.write(f"AI ແນະນຳ: ປ້າຄວນແບ່ງເວລາ 70% ໃຫ້ກັບວຽກ {best_source} ເພາະເປັນບໍ່ເງິນຫຼັກຂອງປີນີ້!")

    with st.expander("📜 ເບິ່ງປະຫວັດລະອຽດທັງໝົດ"):
        st.dataframe(df.sort_values(by='Date', ascending=False), use_container_width=True)