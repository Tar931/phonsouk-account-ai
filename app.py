import streamlit as st
import pandas as pd
import os
from datetime import datetime, timedelta

# --- 1. ຕັ້ງຄ່າເບື້ອງຕົ້ນ ---
st.set_page_config(page_title="App ປ້າພອນສຸກ v5", layout="wide")
FILE_NAME = 'phonsouk_final_database_v3.csv'

# CSS ຕົບແຕ່ງ (ເນັ້ນຕົວເລກໃຫຍ່ໆ ອ່ານງ່າຍ)
st.markdown("""
    <style>
    .block-container { padding-top: 1rem; }
    header {visibility: hidden;}
    .stNumberInput input { font-size: 22px !important; font-weight: bold; color: #1B4F72 !important; }
    .ai-card { background-color: #f0f2f6; padding: 20px; border-radius: 15px; border-left: 10px solid #268BD2; }
    </style>
    """, unsafe_allow_html=True)

st.markdown(f'<div style="background-color:#1B4F72; padding:20px; border-radius:15px; text-align:center; color:white;"><h1>🏦 ລະບົບບັນຊີ AI ປ້າພອນສຸກ (ໃສ່ຈຸດອັດຕະໂນມັດ)</h1></div>', unsafe_allow_html=True)

# --- 2. ສ່ວນປ້ອນຂໍ້ມູນ (ແບບໃໝ່ ໃສ່ຈຸດໃຫ້ເລີຍ) ---
st.write("### 💰 ບ້ອນຕົວເລກລົງໃນຊ່ອງ (ລະບົບຈະຄັ່ນຈຸດໃຫ້ເອງ)")

c1, c2 = st.columns(2)

with c1:
    st.success("### 🟢 ລາຍຮັບ")
    i1 = st.number_input("1. ເງິນເດືອນ", min_value=0, step=1000, format="%d")
    i2 = st.number_input("2. ລາຍຮັບ Creator", min_value=0, step=1000, format="%d")
    i3 = st.number_input("3. ຂາຍຂອງຍ່ອຍ", min_value=0, step=1000, format="%d")
    i4 = st.number_input("4. ຮັບຕັດຫຍິບ", min_value=0, step=1000, format="%d")
    i5 = st.number_input("5. ຕູ້ກົດນ້ຳ", min_value=0, step=1000, format="%d")
    i6 = st.number_input("6. ຕູ້ຊັກຜ້າ", min_value=0, step=1000, format="%d")

with c2:
    st.error("### 🔴 ລາຍຈ່າຍ")
    e1 = st.number_input("1. ຄ່າອາຫານ & ຂອງໃຊ້", min_value=0, step=1000, format="%d")
    e2 = st.number_input("2. ຄ່າເຊົ່າທີ່ຢູ່", min_value=0, step=1000, format="%d")
    e3 = st.number_input("3. ຄ່ານ້ຳ-ໄຟ-ເນັດ", min_value=0, step=1000, format="%d")
    e4 = st.number_input("4. ຄ່າເດີນທາງ", min_value=0, step=1000, format="%d")
    e9 = st.number_input("9. ຄ່າຫວຍ/ລາງວັນ", min_value=0, step=1000, format="%d")
    e10 = st.number_input("10. ຄ່າສ້າງເຮືອນ", min_value=0, step=1000, format="%d")

# --- 3. ການບັນທຶກ ---
st.markdown("---")
if st.button("💾 ບັນທຶກລົງຖານຂໍ້ມູນ", use_container_width=True):
    now_lao = datetime.now() + timedelta(hours=7)
    t_in = i1 + i2 + i3 + i4 + i5 + i6
    t_ex = e1 + e2 + e3 + e4 + e9 + e10
    
    new_data = {
        'ວັນທີ': now_lao.strftime("%d/%m/%Y %H:%M"),
        'ລາຍຮັບລວມ': t_in,
        'ລາຍຈ່າຍລວມ': t_ex,
        'ເຫຼືອເກັບ': t_in - t_ex
    }
    
    pd.DataFrame([new_data]).to_csv(FILE_NAME, mode='a', index=False, header=not os.path.exists(FILE_NAME), encoding='utf-8-sig')
    st.balloons() # ສະແດງຄວາມດີໃຈ
    st.success("✅ ບັນທຶກສຳເລັດແລ້ວເດີ້ປ້າ!")
    st.rerun()

# --- 4. ສ່ວນ AI ວິເຄາະ ---
if os.path.exists(FILE_NAME):
    df = pd.read_csv(FILE_NAME)
    st.write("### 📊 ປະຫວັດການເງິນຫຼ້າສຸດ")
    # ສະແດງຕະລາງແບບມີຈຸດ
    st.dataframe(df.tail(10).style.format("{:,.0f}", subset=['ລາຍຮັບລວມ', 'ລາຍຈ່າຍລວມ', 'ເຫຼືອເກັບ']), use_container_width=True)
    
    st.markdown(f"""
    <div class="ai-card">
        <h3>🤖 AI ທີ່ປຶກສາສ່ວນຕົວ</h3>
        <p>ສະບາຍດີປ້າພອນສຸກ! ຕອນນີ້ປ້າມີເງິນເຫຼືອເກັບສະສົມທັງໝົດ <b>{df['ເຫຼືອເກັບ'].sum():,.0f}</b> ກີບແລ້ວເດີ້.</p>
        <p>💡 <b>ຄຳແນະນຳ:</b> ຖ້າເຫັນວ່າລາຍຮັບຈາກ "ຕູ້ຊັກຜ້າ" ສູງຂຶ້ນ, ປ້າອາດຈະພິຈາລະນາເພີ່ມຕູ້ໃໝ່ໄດ້ໃນເດືອນໜ້າ!</p>
    </div>
    """, unsafe_allow_html=True)
