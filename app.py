import streamlit as st
import pandas as pd
import os
from datetime import datetime

# --- 1. ຕັ້ງຄ່າເວັບໄຊ ---
st.set_page_config(page_title="Phonsouk AI", page_icon="🌸", layout="wide")
FILE_NAME = 'shop_database_v4.csv'

# ສ່ວນຫົວຂໍ້
st.markdown("""
    <div style="background-color:#1B4F72;padding:20px;border-radius:15px;text-align:center;">
        <h1 style="color:white;">🌸 ລະບົບບັນຊີ ປ້າພອນສຸກ</h1>
        <p style="color:#AED6F1;">ບ້ານໂພນສະຫວັນ | ກວດສອບຈຸດຕົວເລກໃຫ້ລະອຽດກ່ອນບັນທຶກ</p>
    </div>
    """, unsafe_allow_html=True)

# --- 2. ຟັງຊັນຊ່ວຍສະແດງຕົວເລກມີຈຸດຄັ່ນ ---
def show_lao_currency(label, amount, color_bg, color_text):
    st.markdown(f"""
        <div style="background-color:{color_bg}; padding:10px; border-radius:10px; border: 2px solid {color_text}; margin-bottom:20px;">
            <p style="margin:0; color:{color_text}; font-size:16px;">{label}</p>
            <h2 style="margin:0; color:{color_text};">{amount:,.0f} ກີບ</h2>
        </div>
    """, unsafe_allow_html=True)

# --- 3. ສ່ວນປ້ອນຂໍ້ມູນ ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("🟢 ລາຍຮັບ")
    s1 = st.number_input("ຍອດຂາຍໜ້າຮ້ານ", min_value=0, step=5000, key="s1")
    show_lao_currency("ກວດສອບຍອດຂາຍ:", s1, "#E8F5E9", "#2E7D32")
    
    s2 = st.number_input("ຄ່າວຽກຕັດຫຍິບ", min_value=0, step=5000, key="s2")
    show_lao_currency("ກວດສອບຄ່າຕັດຫຍິບ:", s2, "#E8F5E9", "#2E7D32")
    
    s3 = st.number_input("ຂາຍເຄື່ອງ Online / ອື່ນໆ", min_value=0, step=5000, key="s3")
    show_lao_currency("ກວດສອບຍອດ Online:", s3, "#E8F5E9", "#2E7D32")

with col2:
    st.subheader("🔴 ລາຍຈ່າຍ")
    e1 = st.number_input("ຊື້ເຄື່ອງເຂົ້າຮ້ານ (Stock)", min_value=0, step=5000, key="e1")
    show_lao_currency("ກວດສອບຄ່າເຄື່ອງ:", e1, "#FFEBEE", "#C62828")
    
    e2 = st.number_input("ຄ່າກິນ / ໃຊ້ຈ່າຍໃນເຮືອນ", min_value=0, step=5000, key="e2")
    show_lao_currency("ກວດສອບຄ່າກິນ:", e2, "#FFEBEE", "#C62828")
    
    e3 = st.number_input("ລາຍຈ່າຍອື່ນໆ", min_value=0, step=1000, key="e3")
    show_lao_currency("ກວດສອບລາຍຈ່າຍອື່ນ:", e3, "#FFEBEE", "#C62828")

if st.button("💾 ບັນທຶກຂໍ້ມູນທັງໝົດ", use_container_width=True, type="primary"):
    total_in = s1 + s2 + s3
    total_out = e1 + e2 + e3
    new_entry = {
        'Date': datetime.now().strftime("%d-%m-%Y %H:%M"),
        'Sewing': s2, 'In': total_in, 'Out': total_out, 
        'Profit': total_in - total_out, 'Food': e2
    }
    df_new = pd.DataFrame([new_entry])
    df_new.to_csv(FILE_NAME, mode='a', index=False, header=not os.path.exists(FILE_NAME))
    st.balloons(); st.success("ບັນທຶກແລ້ວ!"); st.rerun()

# --- 4. ຕາຕະລາງປະຫວັດ ---
if os.path.exists(FILE_NAME):
    st.markdown("---")
    st.subheader("📊 ປະຫວັດການບັນທຶກ (ມີຈຸດຄັ່ນທຸກຊ່ອງ)")
    df = pd.read_csv(FILE_NAME)
    df_display = df.copy()
    for col in ['Sewing', 'In', 'Out', 'Profit', 'Food']:
        df_display[col] = df_display[col].apply(lambda x: "{:,.0f}".format(float(x)))
    st.dataframe(df_display.tail(10), use_container_width=True)