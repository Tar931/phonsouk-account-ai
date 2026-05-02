import streamlit as st
import pandas as pd
import os
from datetime import datetime

# --- 1. ຕັ້ງຄ່າເວັບໄຊ ---
st.set_page_config(page_title="Phonsouk AI Advisor", page_icon="🤖", layout="wide")
FILE_NAME = 'phonsouk_final_database_v2.csv'

st.markdown("""
    <style>
    .money-box { 
        background-color: #002B36; 
        color: #00FFAA; 
        padding: 8px 15px; 
        border-radius: 8px; 
        font-size: 22px; 
        font-weight: bold; 
        text-align: right; 
        border: 2px solid #268BD2; 
        margin-top: -15px; 
        margin-bottom: 15px;
    }
    .ai-report { background-color: #F0F2F6; padding: 20px; border-radius: 15px; border-left: 10px solid #268BD2; color: #1B4F72; }
    </style>
    <div style="background-color:#1B4F72; padding:15px; border-radius:15px; text-align:center; color:white; margin-bottom:20px;">
        <h2 style="margin:0;">🤖 AI ອັດສະລິຍະ ວາງແຜນການເງິນ ປ້າພອນສຸກ</h2>
    </div>
    """, unsafe_allow_html=True)

# --- 2. ສ່ວນປ້ອນຂໍ້ມູນ (ແກ້ໄຂໃຫ້ເຊື່ອມຕໍ່ຈຸດຕົວເລກແລ້ວ) ---
with st.form("main_form"):
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("### 🟢 ລາຍຮັບ (6 ທາງ)")
        i1 = st.number_input("ເງິນເດືອນ", min_value=0, step=10000); st.markdown(f'<div class="money-box">{i1:,.0f} ກີບ</div>', unsafe_allow_html=True)
        i2 = st.number_input("ລາຍຮັບ Creator", min_value=0, step=10000); st.markdown(f'<div class="money-box">{i2:,.0f} ກີບ</div>', unsafe_allow_html=True)
        i3 = st.number_input("ຂາຍຂອງຍ່ອຍ", min_value=0, step=10000); st.markdown(f'<div class="money-box">{i3:,.0f} ກີບ</div>', unsafe_allow_html=True)
        i4 = st.number_input("ວຽກຕັດຫຍິບ", min_value=0, step=10000); st.markdown(f'<div class="money-box">{i4:,.0f} ກີບ</div>', unsafe_allow_html=True)
        i5 = st.number_input("ຕູ້ກົດນ້ຳ", min_value=0, step=10000); st.markdown(f'<div class="money-box">{i5:,.0f} ກີບ</div>', unsafe_allow_html=True)
        i6 = st.number_input("ຕູ້ຊັກຜ້າ", min_value=0, step=10000); st.markdown(f'<div class="money-box">{i6:,.0f} ກີບ</div>', unsafe_allow_html=True)
    with c2:
        st.markdown("### 🔴 ລາຍຈ່າຍ (10 ຢ່າງ)")
        e1 = st.number_input("ຄ່າອາຫານ/ເຄື່ອງໃຊ້", min_value=0, step=10000); st.markdown(f'<div class="money-box">{e1:,.0f} ກີບ</div>', unsafe_allow_html=True)
        e2 = st.number_input("ຄ່າເຊົ່າທີ່ຢູ່", min_value=0, step=10000); st.markdown(f'<div class="money-box">{e2:,.0f} ກີບ</div>', unsafe_allow_html=True)
        e3 = st.number_input("ໄຟຟ້າ-ນໍ້າ-ເນັດ", min_value=0, step=10000); st.markdown(f'<div class="money-box">{e3:,.0f} ກີບ</div>', unsafe_allow_html=True)
        e4 = st.number_input("ນ້ຳມັນ/ລົດຈ້າງ", min_value=0, step=10000); st.markdown(f'<div class="money-box">{e4:,.0f} ກີບ</div>', unsafe_allow_html=True)
        e5 = st.number_input("ຄ່າຮຽນລູກ", min_value=0, step=10000); st.markdown(f'<div class="money-box">{e5:,.0f} ກີບ</div>', unsafe_allow_html=True)
        e6 = st.number_input("ຄ່າຢາ/ປິ່ນປົວ", min_value=0, step=10000); st.markdown(f'<div class="money-box">{e6:,.0f} ກີບ</div>', unsafe_allow_html=True)
        e7 = st.number_input("ເສື້ອຜ້າ/ສ່ວນຕົວ", min_value=0, step=10000); st.markdown(f'<div class="money-box">{e7:,.0f} ກີບ</div>', unsafe_allow_html=True)
        e8 = st.number_input("ໂທລະສັບ/ບັນເທີງ", min_value=0, step=10000); st.markdown(f'<div class="money-box">{e8:,.0f} ກີບ</div>', unsafe_allow_html=True)
        e9 = st.number_input("ຜ່ອນໜີ້/ລົດ", min_value=0, step=10000); st.markdown(f'<div class="money-box">{e9:,.0f} ກີບ</div>', unsafe_allow_html=True)
        e10 = st.number_input("ຊື້ເຄື່ອງເຂົ້າຮ້ານ", min_value=0, step=10000); st.markdown(f'<div class="money-box">{e10:,.0f} ກີບ</div>', unsafe_allow_html=True)
    
    submit = st.form_submit_button("🚀 ບັນທຶກ ແລະ ໃຫ້ AI ວິເຄາະທັງໝົດ", use_container_width=True)

if submit:
    now = datetime.now()
    total_in = i1+i2+i3+i4+i5+i6
    total_ex = e1+e2+e3+e4+e5+e6+e7+e8+e9+e10
    new_entry = {
        'Date': now.strftime("%Y-%m-%d"), 'Week': now.isocalendar()[1], 'Month': now.strftime("%m-%Y"), 'Year': str(now.year),
        'Income': total_in, 'Expense': total_ex, 'Profit': total_in - total_ex,
        'Food': e1, 'Bills': e3, 'Debt': e9, 'Sewing': i4, 'Creator': i2
    }
    pd.DataFrame([new_entry]).to_csv(FILE_NAME, mode='a', index=False, header=not os.path.exists(FILE_NAME))
    st.balloons(); st.rerun()

# --- 3. ສ່ວນ AI ວິເຄາະ (ຮັກສາໄວ້ຄືເກົ່າ 100% ຕາມຄຳສັ່ງປ້າ) ---
if os.path.exists(FILE_NAME):
    df = pd.read_csv(FILE_NAME)
    st.markdown("---")
    period = st.radio("📊 ເລືອກໄລຍະເວລາລາຍງານ:", ["ມື້ນີ້", "ລາຍອາທິດ", "ລາຍເດືອນ", "ລາຍປີ"], horizontal=True)
    
    now = datetime.now()
    if period == "ມື້ນີ້": data = df[df['Date'] == now.strftime("%Y-%m-%d")]; t = "ມື້ນີ້"
    elif period == "ລາຍອາທິດ": data = df[df['Week'] == now.isocalendar()[1]]; t = "ອາທິດນີ້"
    elif period == "ລາຍເດືອນ": data = df[df['Month'] == now.strftime("%m-%Y")]; t = "ເດືອນນີ້"
    else: data = df[df['Year'] == str(now.year)]; t = f"ປີ {now.year}"

    if not data.empty:
        c1, c2, c3 = st.columns(3)
        in_sum, ex_sum = data['Income'].sum(), data['Expense'].sum()
        c1.metric(f"ລາຍຮັບ {t}", "{:,.0f} ກີບ".format(in_sum))
        c2.metric(f"ລາຍຈ່າຍ {t}", "{:,.0f} ກີບ".format(ex_sum))
        c3.metric(f"ກຳໄລ {t}", "{:,.0f} ກີບ".format(in_sum - ex_sum))

        st.markdown(f'<div class="ai-report"><h3>💡 AI Advisor ວິເຄາະ{t}:</h3>', unsafe_allow_html=True)
        food_sum = data['Food'].sum()
        if food_sum > 0: st.write(f"📌 **ຊ່ອງທາງປະຢັດ:** ປ້າຈ່າຍຄ່າອາຫານ {food_sum:,.0f} ກີບ. ລອງເບິ່ງວ່າຫຼຸດບ່ອນໃດໄດ້ແດ່ເດີ້.")
        sewing_sum = data['Sewing'].sum()
        if sewing_sum > 0: st.write(f"🚀 **ແຜນອາຊີບ:** ລາຍໄດ້ຫຍິບຜ້າ {sewing_sum:,.0f} ກີບ. ປ້າເຮັດ Content Creator ສອນຫຍິບຜ້າມາແຮງແນ່ນອນ!")
        st.markdown('</div>', unsafe_allow_html=True)