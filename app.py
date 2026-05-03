import streamlit as st
import pandas as pd
import os
from datetime import datetime, timedelta

# --- 1. ຕັ້ງຄ່າໜ້າຈໍ ---
st.set_page_config(page_title="App ບັນຊີປ້າພອນສຸກ", layout="wide")
FILE_NAME = 'database_paphonsouk.csv'

# CSS ຕົບແຕ່ງໃຫ້ຕົວເລກໃຫຍ່ ອ່ານງ່າຍ
st.markdown("""
    <style>
    .stNumberInput input { font-size: 20px !important; font-weight: bold; color: #1B4F72 !important; }
    div[data-testid="stNotification"] { font-size: 18px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🏦 ລະບົບບັນຊີ AI ປ້າພອນສຸກ (ເວີຊັນແກ້ໄຂ Error)")
st.info("💡 ວິທີໃຊ້: ພິມຕົວເລກລົງໄປເລີຍ ລະບົບຈະໃສ່ຈຸດຄັ່ນໃຫ້ເອງອັດຕະໂນມັດ!")

# --- 2. ສ່ວນປ້ອນຂໍ້ມູນ (ໃຊ້ number_input ເພື່ອປ້ອງກັນ Error) ---
col1, col2 = st.columns(2)

with col1:
    st.success("### 🟢 ລາຍຮັບ")
    in1 = st.number_input("ເງິນເດືອນ", min_value=0, step=10000, value=0)
    in2 = st.number_input("ລາຍຮັບ Creator", min_value=0, step=10000, value=0)
    in3 = st.number_input("ຂາຍຂອງຍ່ອຍ", min_value=0, step=10000, value=0)
    in4 = st.number_input("ຮັບຕັດຫຍິບ", min_value=0, step=10000, value=0)

with col2:
    st.error("### 🔴 ລາຍຈ່າຍ")
    ex1 = st.number_input("ຄ່າອາຫານ/ຂອງໃຊ້", min_value=0, step=10000, value=0)
    ex2 = st.number_input("ຄ່າເຊົ່າບ້ານ", min_value=0, step=10000, value=0)
    ex3 = st.number_input("ຄ່ານ້ຳ-ໄຟ-ເນັດ", min_value=0, step=10000, value=0)
    ex4 = st.number_input("ຄ່າຫວຍ/ສັງຄົມ", min_value=0, step=10000, value=0)

# --- 3. ປຸ່ມບັນທຶກ ---
st.markdown("---")
if st.button("💾 ບັນທຶກຂໍ້ມູນ", use_container_width=True):
    # ຄິດໄລ່ແບບຕົວເລກແທ້ໆ (ຈະບໍ່ Error ແບບໃນຮູບອີກ)
    total_income = in1 + in2 + in3 + in4
    total_expense = ex1 + ex2 + ex3 + ex4
    balance = total_income - total_expense
    
    now = datetime.now() + timedelta(hours=7)
    
    new_data = {
        'ວັນທີ': now.strftime("%d/%m/%Y %H:%M"),
        'ລາຍຮັບລວມ': total_income,
        'ລາຍຈ່າຍລວມ': total_expense,
        'ເຫຼືອເກັບ': balance
    }
    
    # ບັນທຶກລົງ CSV
    df_new = pd.DataFrame([new_data])
    df_new.to_csv(FILE_NAME, mode='a', index=False, header=not os.path.exists(FILE_NAME), encoding='utf-8-sig')
    
    st.balloons()
    st.success(f"✅ ບັນທຶກແລ້ວ! ລາຍຮັບ: {total_income:,.0f} | ລາຍຈ່າຍ: {total_expense:,.0f} | ເຫຼືອ: {balance:,.0f}")
    st.rerun()

# --- 4. ສະແດງປະຫວັດ ---
if os.path.exists(FILE_NAME):
    df = pd.read_csv(FILE_NAME)
    st.write("### 📊 ປະຫວັດ 5 ລາຍການຫຼ້າສຸດ")
    st.table(df.tail(5))
