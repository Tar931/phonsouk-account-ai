import streamlit as st
import pandas as pd
import os
from datetime import datetime

# --- 1. ຕັ້ງຄ່າເວັບໄຊ ---
st.set_page_config(page_title="Phonsouk AI Super Pro", page_icon="💎", layout="wide")
FILE_NAME = 'shop_database_vfinal.csv'

st.markdown("""
    <style>
    .money-display { background-color: #002B36; color: #00FFAA; padding: 10px; border-radius: 8px; font-size: 24px; font-weight: bold; text-align: right; border: 1px solid #268BD2; margin-top: -15px; margin-bottom: 15px; }
    .label-text { font-size: 16px; font-weight: bold; color: #FFFFFF; }
    </style>
    <div style="background-color:#1B4F72; padding:20px; border-radius:15px; text-align:center; margin-bottom:20px;">
        <h1 style="color:white; margin:0;">💎 AI ຜູ້ຊ່ວຍວາງແຜນການເງິນ ປ້າພອນສຸກ</h1>
        <p style="color:#AED6F1; margin:0;">ສະຫຼຸບລາຍອາທິດ-ເດືອນ-ປີ ແລະ ວິເຄາະຊ່ອງທາງປະຢັດ (ມີຈຸດຄັ່ນທຸກບ່ອນ)</p>
    </div>
    """, unsafe_allow_html=True)

# --- 2. ຟັງຊັນສະແດງຕົວເລກມີຈຸດຄັ່ນ ---
def show_big_money(amount):
    st.markdown(f'<div class="money-display">{amount:,.0f} ກີບ</div>', unsafe_allow_html=True)

# --- 3. ສ່ວນປ້ອນຂໍ້ມູນ ---
with st.form("super_form"):
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🟢 ລາຍຮັບ (Income)")
        in1 = st.number_input("ເງິນເດືອນ", min_value=0, step=50000); show_big_money(in1)
        in2 = st.number_input("ລາຍຮັບ Creator", min_value=0, step=10000); show_big_money(in2)
        in3 = st.number_input("ຂາຍຂອງຍ່ອຍ", min_value=0, step=5000); show_big_money(in3)
        in4 = st.number_input("ວຽກຕັດຫຍິບ", min_value=0, step=5000); show_big_money(in4)
        in5 = st.number_input("ຕູ້ກົດນ້ຳ", min_value=0, step=2000); show_big_money(in5)
        in6 = st.number_input("ຕູ້ຊັກຜ້າ", min_value=0, step=5000); show_big_money(in6)

    with col2:
        st.subheader("🔴 ລາຍຈ່າຍ (Expense)")
        ex1 = st.number_input("ຄ່າອາຫານ/ເຄື່ອງໃຊ້", min_value=0, step=5000); show_big_money(ex1)
        ex2 = st.number_input("ຄ່າເຊົ່າທີ່ຢູ່", min_value=0, step=100000); show_big_money(ex2)
        ex3 = st.number_input("ໄຟຟ້າ-ນໍ້າ-ເນັດ", min_value=0, step=5000); show_big_money(ex3)
        ex4 = st.number_input("ນ້ຳມັນ/ລົດຈ້າງ", min_value=0, step=5000); show_big_money(ex4)
        ex5 = st.number_input("ຄ່າຮຽນລູກ", min_value=0, step=50000); show_big_money(ex5)
        ex6 = st.number_input("ຄ່າຢາ/ປິ່ນປົວ", min_value=0, step=5000); show_big_money(ex6)
        ex7 = st.number_input("ເສື້ອຜ້າ/ສ່ວນຕົວ", min_value=0, step=5000); show_big_money(ex7)
        ex8 = st.number_input("ໂທລະສັບ/ບັນເທີງ", min_value=0, step=5000); show_big_money(ex8)
        ex9 = st.number_input("ຜ່ອນໜີ້/ລົດ", min_value=0, step=50000); show_big_money(ex9)
        ex10 = st.number_input("ຊື້ເຄື່ອງເຂົ້າຮ້ານ", min_value=0, step=10000); show_big_money(ex10)

    btn = st.form_submit_button("🚀 ບັນທຶກ ແລະ ໃຫ້ AI ລາຍງານລາຍປີ", use_container_width=True)

if btn:
    now = datetime.now()
    total_in = in1+in2+in3+in4+in5+in6
    total_ex = ex1+ex2+ex3+ex4+ex5+ex6+ex7+ex8+ex9+ex10
    new_entry = {
        'Date': now.strftime("%Y-%m-%d %H:%M"), 'Week': now.isocalendar()[1], 'Month': now.strftime("%m-%Y"), 'Year': str(now.year),
        'Income': total_in, 'Expense': total_ex, 'Profit': total_in - total_ex, 'Food': ex1, 'Debt': ex9, 'Sewing': in4
    }
    pd.DataFrame([new_entry]).to_csv(FILE_NAME, mode='a', index=False, header=not os.path.exists(FILE_NAME))
    st.balloons(); st.success("AI ບັນທຶກແລ້ວ!")

# --- 4. ສ່ວນ AI ລາຍງານ ແລະ ວາງແຜນ ---
if os.path.exists(FILE_NAME):
    df = pd.read_csv(FILE_NAME)
    st.markdown("---")
    report = st.radio("📊 ເລືອກໄລຍະເວລາລາຍງານ:", ["ລາຍອາທິດ", "ລາຍເດືອນ", "ລາຍປີ"], horizontal=True)
    
    now = datetime.now()
    if report == "ລາຍອາທິດ": data = df[df['Week'] == now.isocalendar()[1]]; t = "ອາທິດນີ້"
    elif report == "ລາຍເດືອນ": data = df[df['Month'] == now.strftime("%m-%Y")]; t = "ເດືອນນີ້"
    else: data = df[df['Year'] == str(now.year)]; t = f"ປີ {now.year}"

    c1, c2, c3 = st.columns(3)
    c1.metric(f"ລາຍຮັບ {t}", "{:,.0f} ກີບ".format(data['Income'].sum()))
    c2.metric(f"ລາຍຈ່າຍ {t}", "{:,.0f} ກີບ".format(data['Expense'].sum()))
    c3.metric(f"ກຳໄລ {t}", "{:,.0f} ກີບ".format(data['Profit'].sum()))

    st.markdown("### 🧠 AI ວິເຄາະຫາຊ່ອງທາງປະຢັດ & ວາງແຜນອາຊີບ")
    col_ai1, col_ai2 = st.columns(2)
    with col_ai1:
        st.info("**💡 ຊ່ອງທາງປະຢັດ:**")
        food_sum = data['Food'].sum()
        if food_sum > 0: st.write(f"📌 {t} ປ້າຈ່າຍຄ່າກິນ {food_sum:,.0f} ກີບ. AI ແນະນຳໃຫ້ປ້າກວດເບິ່ງວ່າສາມາດຫຼຸດລາຍຈ່າຍທີ່ບໍ່ຈຳເປັນໄດ້ບໍ່.")
        if data['Debt'].sum() > 0: st.warning(f"📌 ປ້າມີພາລະໜີ້ສິນ {data['Debt'].sum():,.0f} ກີບ. ຄວນແບ່ງກຳໄລ 20% ໄປທະຍອຍໂປ້ໜີ້ເດີ້.")

    with col_ai2:
        st.success("**🚀 ແຜນວາງແຜນອາຊີບ:**")
        sewing_val = data['Sewing'].sum()
        st.write(f"✨ ລາຍໄດ້ຕັດຫຍິບ {t} ແມ່ນ {sewing_val:,.0f} ກີບ.")
        st.write("AI ແນະນຳ: ໃນຖານະ Creator ແລະ ຊ່າງຫຍິບ, ປ້າຄວນ 'ຖ່າຍວິດີໂອຕອນຫຍິບຜ້າ' ລົງ Facebook/TikTok ເພື່ອຫາລູກຄ້າ ແລະ ສ້າງລາຍໄດ້ 2 ທາງພ້ອມກັນ!")

    with st.expander("📜 ເບິ່ງປະຫວັດທັງໝົດ (ມີຈຸດຄັ່ນ)"):
        st.dataframe(df.sort_values(by='Date', ascending=False), use_container_width=True)