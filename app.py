import streamlit as st
import pandas as pd
import os
from datetime import datetime

# --- 1. ຕັ້ງຄ່າເວັບໄຊ ແລະ Style ---
st.set_page_config(page_title="Phonsouk Professional AI", page_icon="🏦", layout="wide")
FILE_NAME = 'phonsouk_final_database_v2.csv'

st.markdown("""
    <style>
    .money-box { 
        background-color: #002B36; color: #00FFAA; padding: 10px 15px; border-radius: 10px; 
        font-size: 24px; font-weight: bold; text-align: right; border: 2px solid #268BD2; margin-bottom: 20px;
    }
    .ai-card { background-color: #FFFFFF; padding: 25px; border-radius: 20px; border-left: 12px solid #268BD2; 
               box-shadow: 0 4px 6px rgba(0,0,0,0.1); color: #1B4F72; }
    </style>
    <div style="background-color:#1B4F72; padding:20px; border-radius:15px; text-align:center; color:white; margin-bottom:25px;">
        <h1 style="margin:0;">🏦 ລະບົບທີ່ປຶກສາການເງິນ (Version ປ້າພອນສຸກ)</h1>
    </div>
    """, unsafe_allow_html=True)

# --- 2. ສ່ວນປ້ອນຂໍ້ມູນ (ເອົາຈຸດຕົວເລກ Real-time ກັບຄືນມາ) ---
st.write("### 📝 ບັນທຶກລາຍຮັບ - ລາຍຈ່າຍ")

# ໃຊ້ Form ເພື່ອໃຫ້ລ້າງຂໍ້ມູນໄດ້ງ່າຍ
with st.form("my_form", clear_on_submit=True):
    c1, c2 = st.columns(2)
    
    with c1:
        st.markdown("### 🟢 ລາຍຮັບ")
        i1 = st.number_input("ເງິນເດືອນ", min_value=0, step=10000); st.markdown(f'<div class="money-box">{i1:,.0f}</div>', unsafe_allow_html=True)
        i2 = st.number_input("ລາຍຮັບ Creator", min_value=0, step=10000); st.markdown(f'<div class="money-box">{i2:,.0f}</div>', unsafe_allow_html=True)
        i3 = st.number_input("ຂາຍຂອງຍ່ອຍ", min_value=0, step=10000); st.markdown(f'<div class="money-box">{i3:,.0f}</div>', unsafe_allow_html=True)
        i4 = st.number_input("ວຽກຕັດຫຍິບ", min_value=0, step=10000); st.markdown(f'<div class="money-box">{i4:,.0f}</div>', unsafe_allow_html=True)
        i5 = st.number_input("ຕູ້ກົດນ້ຳ", min_value=0, step=10000); st.markdown(f'<div class="money-box">{i5:,.0f}</div>', unsafe_allow_html=True)
        i6 = st.number_input("ຕູ້ຊັກຜ້າ", min_value=0, step=10000); st.markdown(f'<div class="money-box">{i6:,.0f}</div>', unsafe_allow_html=True)

    with c2:
        st.markdown("### 🔴 ລາຍຈ່າຍ")
        e1 = st.number_input("ຄ່າອາຫານ/ເຄື່ອງໃຊ້", min_value=0, step=10000); st.markdown(f'<div class="money-box">{e1:,.0f}</div>', unsafe_allow_html=True)
        e3 = st.number_input("ໄຟຟ້າ-ນໍ້າ-ເນັດ", min_value=0, step=10000); st.markdown(f'<div class="money-box">{e3:,.0f}</div>', unsafe_allow_html=True)
        e9 = st.number_input("ຜ່ອນໜີ້/ລົດ", min_value=0, step=10000); st.markdown(f'<div class="money-box">{e9:,.0f}</div>', unsafe_allow_html=True)
        e10 = st.number_input("ຊື້ເຄື່ອງເຂົ້າຮ້ານ", min_value=0, step=10000); st.markdown(f'<div class="money-box">{e10:,.0f}</div>', unsafe_allow_html=True)

    submitted = st.form_submit_button("🚀 ບັນທຶກ ແລະ ລ້າງຂໍ້ມູນອອກ", use_container_width=True)

    if submitted:
        now = datetime.now()
        total_in = i1+i2+i3+i4+i5+i6
        total_ex = e1+e3+e9+e10
        new_entry = {
            'ວັນທີ_ເວລາ': now.strftime("%d/%m/%Y %H:%M"),
            'Date': now.strftime("%Y-%m-%d"), 'Week': now.isocalendar()[1], 'Month': now.strftime("%m-%Y"), 'Year': str(now.year),
            'Income': total_in, 'Expense': total_ex, 'Profit': total_in - total_ex,
            'Food': e1, 'Debt': e9, 'Sewing': i4, 'Vending': i5+i6
        }
        pd.DataFrame([new_entry]).to_csv(FILE_NAME, mode='a', index=False, header=not os.path.exists(FILE_NAME))
        st.success("ບັນທຶກ ແລະ ລ້າງຂໍ້ມູນຮຽບຮ້ອຍ!")
        st.rerun()

# --- 3. ການວິເຄາະ AI ແລະ ຕະລາງ (ຄືເກົ່າ 100%) ---
if os.path.exists(FILE_NAME):
    df = pd.read_csv(FILE_NAME)
    st.markdown("---")
    period = st.radio("📊 ເລືອກໄລຍະວິເຄາະ:", ["ມື້ນີ້", "ລາຍອາທິດ", "ລາຍເດືອນ", "ລາຍປີ"], horizontal=True)
    
    now = datetime.now()
    if period == "ມື້ນີ້": data = df[df['Date'] == now.strftime("%Y-%m-%d")]; t = "ມື້ນີ້"
    elif period == "ລາຍອາທິດ": data = df[df['Week'] == now.isocalendar()[1]]; t = "ອາທິດນີ້"
    elif period == "ລາຍເດືອນ": data = df[df['Month'] == now.strftime("%m-%Y")]; t = "ເດືອນນີ້"
    else: data = df[df['Year'] == str(now.year)]; t = f"ປີ {now.year}"

    if not data.empty:
        c1, c2, c3 = st.columns(3)
        in_sum, ex_sum = data['Income'].sum(), data['Expense'].sum()
        profit = in_sum - ex_sum
        c1.metric(f"ລາຍຮັບ {t}", f"{in_sum:,.0f} ກີບ")
        c2.metric(f"ລາຍຈ່າຍ {t}", f"{ex_sum:,.0f} ກີບ")
        c3.metric(f"ກຳໄລ {t}", f"{profit:,.0f} ກີບ")

        st.markdown(f'<div class="ai-card"><h3>💡 AI Professional Insight ({t})</h3>', unsafe_allow_html=True)
        st.write(f"📌 **ວິເຄາະ:** ປ້າມີລາຍໄດ້ຈາກງານຫຍິບຜ້າ {data['Sewing'].sum() if 'Sewing' in data.columns else 0:,.0f} ກີບ ແລະ ຕູ້ຢອດຫຼຽນ {data['Vending'].sum() if 'Vending' in data.columns else 0:,.0f} ກີບ.")
        if profit < 0: st.warning("⚠️ ເດືອນນີ້ລາຍຈ່າຍເກີນລາຍຮັບ! ປ້າຄວນກວດສອບຄ່າອາຫານ ແລະ ໜີ້ສິນຄືນ.")
        st.markdown('</div>', unsafe_allow_html=True)

    # ຕະລາງ Excel
    st.markdown("### 📅 ປະຫວັດ (Excel Format)")
    display_df = df.copy()
    for col in ['Income', 'Expense', 'Profit']:
        if col in display_df.columns: display_df[col] = display_df[col].apply(lambda x: f"{x:,.0f}")
    st.dataframe(display_df[['ວັນທີ_ເວລາ', 'Income', 'Expense', 'Profit']].tail(10), use_container_width=True)

    # ປຸ່ມ Reset (Password: 9999)
    with st.expander("🛠️ ລ້າງຂໍ້ມູນ (Security Lock)"):
        pwd = st.text_input("ໃສ່ລະຫັດ 9999 ເພື່ອລົບ:", type="password")
        if st.button("🗑️ ຢືນຢັນລົບທັງໝົດ"):
            if pwd == "9999":
                os.remove(FILE_NAME)
                st.rerun()