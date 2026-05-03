import streamlit as st
import pandas as pd
import os
from datetime import datetime, timedelta

# --- 1. ຕັ້ງຄ່າເບື້ອງຕົ້ນ ---
st.set_page_config(page_title="ບັນຊີປ້າພອນສຸກ v7", layout="wide")
# ປ່ຽນຊື່ໄຟລ໌ເກັບຂໍ້ມູນໃໝ່ ເພື່ອໃຫ້ລະບົບເລີ່ມຕົ້ນໃໝ່ແບບບໍ່ມີ Error
FILE_NAME = 'phonsouk_account_v7.csv'

st.markdown("""
    <style>
    .stNumberInput input { font-size: 22px !important; font-weight: bold; color: #1B4F72 !important; }
    header {visibility: hidden;}
    .reportview-container { background-color: #f0f2f6; }
    </style>
    """, unsafe_allow_html=True)

st.title("🏦 ລະບົບບັນຊີ AI ປ້າພອນສຸກ (ເວີຊັນປັບປຸງ)")

# --- 2. ສ່ວນປ້ອນຂໍ້ມູນ (ບັງຄັບໃຫ້ເປັນຕົວເລກ 100%) ---
st.info("💡 ພິມຕົວເລກລົງໄປເລີຍ ລະບົບຈະໃສ່ຈຸດຄັ່ນໃຫ້ເອງອັດຕະໂນມັດ!")

c1, c2 = st.columns(2)

with c1:
    st.success("### 🟢 ລາຍຮັບ")
    i1 = st.number_input("1. ເງິນເດືອນ", min_value=0, step=1000)
    i2 = st.number_input("2. ລາຍຮັບ Creator", min_value=0, step=1000)
    i3 = st.number_input("3. ຂາຍຂອງຍ່ອຍ", min_value=0, step=1000)

with c2:
    st.error("### 🔴 ລາຍຈ່າຍ")
    e1 = st.number_input("1. ຄ່າອາຫານ/ຂອງໃຊ້", min_value=0, step=1000)
    e2 = st.number_input("2. ຄ່າເຊົ່າບ້ານ/ນ້ຳໄຟ", min_value=0, step=1000)
    e3 = st.number_input("3. ຄ່າຫວຍ/ສັງຄົມ", min_value=0, step=1000)

# --- 3. ການບັນທຶກ ແລະ ຄິດໄລ່ (ໃຊ້ສູດທີ່ບໍ່ມີທາງ Error) ---
st.markdown("---")
if st.button("💾 ບັນທຶກຂໍ້ມູນ", use_container_width=True):
    # ແປງຄ່າໃຫ້ເປັນຕົວເລກແນ່ນອນ (float) ກ່ອນຄິດໄລ່
    total_in = float(i1 + i2 + i3)
    total_ex = float(e1 + e2 + e3)
    net_balance = total_in - total_ex
    
    current_time = (datetime.now() + timedelta(hours=7)).strftime("%d/%m/%Y %H:%M")
    
    new_data = {
        'ວັນທີ': current_time,
        'ລາຍຮັບລວມ': total_in,
        'ລາຍຈ່າຍລວມ': total_ex,
        'ເຫຼືອເກັບ': net_balance
    }
    
    # ບັນທຶກລົງ CSV
    df_new = pd.DataFrame([new_data])
    df_new.to_csv(FILE_NAME, mode='a', index=False, header=not os.path.exists(FILE_NAME), encoding='utf-8-sig')
    
    st.balloons()
    st.success(f"✅ ບັນທຶກແລ້ວ! ເງິນເຫຼືອເກັບຮອບນີ້: {net_balance:,.0f} ກີບ")
    st.rerun()

# --- 4. ສະແດງປະຫວັດ ---
if os.path.exists(FILE_NAME):
    df = pd.read_csv(FILE_NAME)
    st.write("### 📊 ປະຫວັດການເງິນຫຼ້າສຸດ")
    st.dataframe(df.tail(10).style.format("{:,.0f}", subset=['ລາຍຮັບລວມ', 'ລາຍຈ່າຍລວມ', 'ເຫຼືອເກັບ']), use_container_width=True)
