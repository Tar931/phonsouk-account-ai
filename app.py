import streamlit as st
import pandas as pd
import os
from datetime import datetime, timedelta

# --- ຕັ້ງຄ່າໜ້າຈໍ ---
st.set_page_config(page_title="App ປ້າພອນສຸກ v8", layout="wide")
# ໃຊ້ຊື່ໄຟລ໌ໃໝ່ທັງໝົດເພື່ອບໍ່ໃຫ້ມັນຕີກັບຂອງເກົ່າ
DB_FILE = 'data_clean_v8.csv'

st.title("🏦 ລະບົບບັນຊີ AI ປ້າພອນສຸກ (ເວີຊັນລ້າງ Error)")

# --- ໃຊ້ number_input ເທົ່ານັ້ນ (ໃສ່ຈຸດໃຫ້ເອງ) ---
st.warning("💡 ປ້າພິມຕົວເລກລົງໄປເລີຍ ມັນຈະໃສ່ຈຸດໃຫ້ອັດຕະໂນມັດ!")

c1, c2 = st.columns(2)
with c1:
    st.success("### 🟢 ລາຍຮັບ")
    i1 = st.number_input("1. ເງິນເດືອນ", min_value=0, step=1000)
    i2 = st.number_input("2. ລາຍຮັບ Creator", min_value=0, step=1000)
with c2:
    st.error("### 🔴 ລາຍຈ່າຍ")
    e1 = st.number_input("1. ຄ່າອາຫານ", min_value=0, step=1000)
    e2 = st.number_input("2. ຄ່າຫວຍ", min_value=0, step=1000)

# --- ປຸ່ມບັນທຶກ (ໃຊ້ສູດຄິດໄລ່ແບບປ້ອງກັນ Error) ---
if st.button("💾 ບັນທຶກຂໍ້ມູນ", use_container_width=True):
    total_in = float(i1 + i2)
    total_ex = float(e1 + e2)
    diff = total_in - total_ex
    
    new_data = {'ວັນທີ': (datetime.now() + timedelta(hours=7)).strftime("%d/%m/%Y %H:%M"),
                'ລາຍຮັບ': total_in, 'ລາຍຈ່າຍ': total_ex, 'ເຫຼືອ': diff}
    
    df_new = pd.DataFrame([new_data])
    df_new.to_csv(DB_FILE, mode='a', index=False, header=not os.path.exists(DB_FILE), encoding='utf-8-sig')
    st.balloons()
    st.success(f"ບັນທຶກແລ້ວ! ເຫຼືອ: {diff:,.0f}")
    st.rerun()

if os.path.exists(DB_FILE):
    st.write("### 📊 ປະຫວັດ")
    st.dataframe(pd.read_csv(DB_FILE).tail(10))
