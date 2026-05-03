import streamlit as st
import pandas as pd
import os
from datetime import datetime, timedelta

# --- 1. ຕັ້ງຄ່າເບື້ອງຕົ້ນ ---
st.set_page_config(page_title="App ປ້າພອນສຸກ v6", layout="wide")
FILE_NAME = 'database_paphonsouk_v6.csv' # ປ່ຽນຊື່ໄຟລ໌ໃໝ່ເພື່ອລ້າງ Error ເກົ່າ

st.markdown("""
    <style>
    .stNumberInput input { font-size: 20px !important; font-weight: bold; color: #1B4F72 !important; }
    header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

st.title("🏦 ລະບົບບັນຊີ AI ປ້າພອນສຸກ")
st.write("### ປ້າພິມຕົວເລກລົງໄປເລີຍ ລະບົບຈະໃສ່ຈຸດໃຫ້ເອງ!")

# --- 2. ສ່ວນປ້ອນຂໍ້ມູນ (ແບບ Number Input 100%) ---
col1, col2 = st.columns(2)

with col1:
    st.success("### 🟢 ລາຍຮັບ")
    in1 = st.number_input("1. ເງິນເດືອນ", min_value=0, value=0, step=1000)
    in2 = st.number_input("2. ລາຍຮັບ Creator", min_value=0, value=0, step=1000)
    in3 = st.number_input("3. ຂາຍຂອງຍ່ອຍ", min_value=0, value=0, step=1000)
    in4 = st.number_input("4. ຮັບຕັດຫຍິບ", min_value=0, value=0, step=1000)

with col2:
    st.error("### 🔴 ລາຍຈ່າຍ")
    ex1 = st.number_input("1. ຄ່າອາຫານ/ຂອງໃຊ້", min_value=0, value=0, step=1000)
    ex2 = st.number_input("2. ຄ່າເຊົ່າບ້ານ/ນ້ຳໄຟ", min_value=0, value=0, step=1000)
    ex3 = st.number_input("3. ຄ່າຫວຍ/ສັງຄົມ", min_value=0, value=0, step=1000)
    ex4 = st.number_input("4. ຄ່າສ້າງເຮືອນ", min_value=0, value=0, step=1000)

# --- 3. ປຸ່ມບັນທຶກ ແລະ ການຄິດໄລ່ ---
st.markdown("---")
if st.button("💾 ບັນທຶກຂໍ້ມູນທັງໝົດ", use_container_width=True):
    # ຄິດໄລ່ແບບ Number 100% ປ້ອງກັນ Error ໃນຮູບ image_5fcb37.png
    t_in = float(in1 + in2 + in3 + in4)
    t_ex = float(ex1 + ex2 + ex3 + ex4)
    balance = t_in - t_ex
    
    now = datetime.now() + timedelta(hours=7)
    
    new_row = {
        'ວັນທີ': now.strftime("%d/%m/%Y %H:%M"),
        'ລາຍຮັບລວມ': t_in,
        'ລາຍຈ່າຍລວມ': t_ex,
        'ເຫຼືອເກັບ': balance
    }
    
    # ບັນທຶກລົງ CSV
    df_new = pd.DataFrame([new_row])
    df_new.to_csv(FILE_NAME, mode='a', index=False, header=not os.path.exists(FILE_NAME), encoding='utf-8-sig')
    
    st.balloons()
    st.success(f"✅ ບັນທຶກສຳເລັດ! ເຫຼືອເງິນເກັບ: {balance:,.0f} ກີບ")
    st.rerun()

# --- 4. ສະແດງປະຫວັດ ---
if os.path.exists(FILE_NAME):
    df = pd.read_csv(FILE_NAME)
    st.write("### 📊 ປະຫວັດການເງິນ")
    # ຈັດຮູບແບບຕົວເລກໃຫ້ມີຈຸດໃນຕະລາງ
    st.dataframe(df.tail(10).style.format("{:,.0f}", subset=['ລາຍຮັບລວມ', 'ລາຍຈ່າຍລວມ', 'ເຫຼືອເກັບ']), use_container_width=True)
