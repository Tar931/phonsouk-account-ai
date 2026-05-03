import streamlit as st
import pandas as pd
import os
from datetime import datetime, timedelta

# --- 1. ຕັ້ງຄ່າໜ້າຈໍ ---
st.set_page_config(page_title="App ປ້າພອນສຸກ v4", layout="wide")
FILE_NAME = 'phonsouk_final_database_v3.csv'

# CSS ຕົບແຕ່ງ (ລົບ Header ແລະ ປັບແຕ່ງສີ)
st.markdown("""
    <style>
    .block-container { padding-top: 1rem; }
    header {visibility: hidden;}
    footer {visibility: hidden;}
    .stNumberInput div div input { font-size: 20px !important; font-weight: bold; color: #1B4F72; }
    .ai-card { background-color: #f0f2f6; padding: 20px; border-radius: 15px; border-left: 10px solid #268BD2; }
    </style>
    """, unsafe_allow_html=True)

st.markdown(f'<div style="background-color:#1B4F72; padding:15px; border-radius:10px; text-align:center; color:white;"><h2>🏦 ລະບົບບັນຊີ AI (ປ້າພອນສຸກ)</h2></div>', unsafe_allow_html=True)
st.write("### 💰 ບ້ອນຕົວເລກ (ລະບົບຈະໃສ່ຈຸດໃຫ້ອັດຕະໂນມັດ)")

# --- 2. ສ້າງສ່ວນປ້ອນຂໍ້ມູນ (ໃຊ້ number_input ເພື່ອໃຫ້ມີຈຸດອັດຕະໂນມັດ) ---
c1, c2 = st.columns(2)

with c1:
    st.success("### 🟢 ສ່ວນລາຍຮັບ")
    i1 = st.number_input("1. ເງິນເດືອນ", min_value=0, step=1000, format="%d")
    i2 = st.number_input("2. ລາຍຮັບ Creator (FB/YouTube)", min_value=0, step=1000, format="%d")
    i3 = st.number_input("3. ຂາຍຂອງຍ່ອຍ", min_value=0, step=1000, format="%d")
    i4 = st.number_input("4. ຮັບຕັດຫຍິບ", min_value=0, step=1000, format="%d")
    i5 = st.number_input("5. ຕູ້ກົດນ້ຳ", min_value=0, step=1000, format="%d")
    i6 = st.number_input("6. ຕູ້ຊັກຜ້າ", min_value=0, step=1000, format="%d")

with c2:
    st.error("### 🔴 ສ່ວນລາຍຈ່າຍ")
    e1 = st.number_input("1. ຄ່າອາຫານ & ເຄື່ອງບໍລິໂພກ", min_value=0, step=1000, format="%d")
    e2 = st.number_input("2. ຄ່າເຊົ່າທີ່ຢູ່", min_value=0, step=1000, format="%d")
    e3 = st.number_input("3. ຄ່ານ້ຳ-ຄ່າໄຟ-ເນັດ", min_value=0, step=1000, format="%d")
    e4 = st.number_input("4. ຄ່າເດີນທາງ", min_value=0, step=1000, format="%d")
    e5 = st.number_input("5. ຄ່າການສຶກສາ", min_value=0, step=1000, format="%d")
    e9 = st.number_input("9. ຄ່າຫວຍ/ລາງວັນ", min_value=0, step=1000, format="%d")
    e10 = st.number_input("10. ຄ່າສ້າງເຮືອນ", min_value=0, step=1000, format="%d")

# --- 3. ປຸ່ມບັນທຶກ ແລະ ການຄິດໄລ່ ---
st.markdown("---")
if st.button("💾 ບັນທຶກຂໍ້ມູນທັງໝົດ", use_container_width=True):
    now_lao = datetime.now() + timedelta(hours=7)
    
    t_in = i1 + i2 + i3 + i4 + i5 + i6
    t_ex = e1 + e2 + e3 + e4 + e5 + e9 + e10
    
    new_data = {
        'ວັນທີ': now_lao.strftime("%d/%m/%Y %H:%M"),
        'ລາຍຮັບລວມ': t_in,
        'ລາຍຈ່າຍລວມ': t_ex,
        'ເຫຼືອເກັບ': t_in - t_ex
    }
    
    # ບັນທຶກລົງ CSV
    pd.DataFrame([new_data]).to_csv(FILE_NAME, mode='a', index=False, header=not os.path.exists(FILE_NAME), encoding='utf-8-sig')
    st.success("✅ ບັນທຶກສຳເລັດແລ້ວ!")
    st.rerun()

# --- 4. ສ່ວນສະແດງຜົນ AI ---
if os.path.exists(FILE_NAME):
    df = pd.read_csv(FILE_NAME)
    st.write("### 📊 ປະຫວັດການເງິນ")
    st.dataframe(df.tail(10), use_container_width=True)
    
    st.markdown(f"""
    <div class="ai-card">
        <h3>🤖 AI ວິເຄາະໃຫ້ປ້າ</h3>
        <p>ສະບາຍດີປ້າພອນສຸກ! ຕອນນີ້ປ້າມີລາຍຮັບລວມທັງໝົດ <b>{df['ລາຍຮັບລວມ'].sum():,.0f}</b> ກີບ.</p>
        <p>ຢ່າລືມກວດເບິ່ງລາຍຈ່າຍຄ່າຫວຍເດີ້ ຖ້າມັນຫຼາຍເກີນໄປ AI ແນະນຳໃຫ້ເພີ່ມງົບໄປໃສ່ການສ້າງເຮືອນແທນ!</p>
    </div>
    """, unsafe_allow_html=True)