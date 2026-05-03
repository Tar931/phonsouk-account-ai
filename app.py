import streamlit as st
import pandas as pd
import os
from datetime import datetime, timedelta

# --- ຕັ້ງຄ່າໜ້າຈໍ ---
st.set_page_config(page_title="App ບັນຊີຂອງປ້າ", layout="wide")
FILE_NAME = 'phonsouk_final_database_v3.csv'

# CSS ຕົບແຕ່ງ
st.markdown("""
    <style>
    .block-container { padding-top: 1rem; }
    header {visibility: hidden;}
    footer {visibility: hidden;}
    .ai-card { 
        background-color: #f0f2f6; padding: 20px; border-radius: 15px; border-left: 10px solid #268BD2; 
        color: #1B4F72; margin-top: 10px; line-height: 1.6;
    }
    </style>
    """, unsafe_allow_html=True)

# 1. ຟັງຊັນຈັດຮູບແບບຕົວເລກ (ໃສ່ຈຸດ)
def format_with_commas(v):
    nums = "".join(filter(str.isdigit, str(v)))
    if nums:
        return "{:,}".format(int(nums))
    return ""

# 2. ຟັງຊັນແປງເປັນຕົວເລກ (ຄິດໄລ່)
def to_int(v):
    nums = "".join(filter(str.isdigit, str(v)))
    return int(nums) if nums else 0

# 3. ຟັງຊັນຈັດການເມື່ອມີການປ່ຽນແປງຂໍ້ມູນ (Callback)
def on_change_callback(key):
    raw_value = st.session_state[f"raw_{key}"]
    st.session_state[key] = format_with_commas(raw_value)

# ຟັງຊັນສ້າງຊ່ອງປ້ອນ
def make_input(label, key):
    if key not in st.session_state:
        st.session_state[key] = ""
    return st.text_input(label, value=st.session_state[key], key=f"raw_{key}", on_change=on_change_callback, args=(key,))

# --- ສ່ວນຫົວຂໍ້ ---
st.markdown(f'<div style="background-color:#1B4F72; padding:15px; border-radius:10px; text-align:center; color:white;"><h2>🏦 ລະບົບ AI ທີ່ປຶກສາການເງິນສະຫຼາດສຸດ (ປ້າພອນສຸກ)</h2></div>', unsafe_allow_html=True)
st.markdown("### 💰 ລະບົບບ້ອນເລກແບບມີຈຸດ (Real-time)")
st.write("ປ້າພິມເລກລົງໄປ ແລ້ວກົດ **Enter** ຫຼື **ກົດບ່ອນຫວ່າງ** ມັນຈະໃສ່ຈຸດໃຫ້ທັນທີ!")

# --- ສ່ວນປ້ອນຂໍ້ມູນ ---
c1, c2 = st.columns(2)

with c1:
    st.success("### 🟢 ສ່ວນລາຍຮັບ")
    i1 = make_input("1. ເງິນເດືອນ", "i1")
    i2 = make_input("2. ລາຍຮັບ Creator (FB/YouTube)", "i2")
    i3 = make_input("3. ຂາຍຂອງຍ່ອຍ", "i3")
    i4 = make_input("4. ຮັບຕັດຫຍິບ", "i4")
    i5 = make_input("5. ຕູ້ກົດນ້ຳ", "i5")
    i6 = make_input("6. ຕູ້ຊັກຜ້າ", "i6")

with c2:
    st.error("### 🔴 ສ່ວນລາຍຈ່າຍ")
    e1 = make_input("1. ຄ່າອາຫານ & ເຄື່ອງບໍລິໂພກ", "e1")
    e2 = make_input("2. ຄ່າເຊົ່າທີ່ຢູ່", "e2")
    e3 = make_input("3. ຄ່ານ້ຳ-ຄ່າໄຟ-ເນັດ", "e3")
    e4 = make_input("4. ຄ່າເດີນທາງ", "e4")
    e5 = make_input("5. ຄ່າການສຶກສາ", "e5")
    e6 = make_input("6. ຄ່າປິ່ນປົວ", "e6")
    e7 = make_input("7. ຄ່າເສື້ອຜ້າ & ຂອງໃຊ້", "e7")
    e8 = make_input("8. ຄ່າໂທລະສັບ & ບັນເທີງ", "e8")
    e9 = make_input("9. ຄ່າຫວຍ/ລາງວັນ", "e9")
    e10 = make_input("10. ຄ່າສ້າງເຮືອນ", "e10")

st.markdown("---")
if st.button("💾 ບັນທຶກຂໍ້ມູນທັງໝົດ", use_container_width=True):
    now_lao = datetime.now() + timedelta(hours=7)
    
    # ດຶງຄ່າ ແລະ ແປງເປັນຕົວເລກ
    in_vals = [to_int(st.session_state.get(k, "")) for k in ["i1","i2","i3","i4","i5","i6"]]
    ex_vals = [to_int(st.session_state.get(k, "")) for k in ["e1","e2","e3","e4","e5","e6","e7","e8","e9","e10"]]
    
    sum_in = sum(in_vals)
    sum_ex = sum(ex_vals)
    
    new_row = {
        'ວັນທີ': now_lao.strftime("%d/%m/%Y %H:%M"),
        'ລາຍຮັບລວມ': sum_in, 'ລາຍຈ່າຍລວມ': sum_ex, 'ເຫຼືອເກັບ': sum_in - sum_ex,
        'ເງິນເດືອນ': in_vals[0], 'Creator': in_vals[1], 'ຂາຍຂອງ': in_vals[2], 'ຫຍິບຜ້າ': in_vals[3], 'ຕູ້້ກົດນ້ຳ': in_vals[4], 'ຕູ້ຊັກຜ້າ': in_vals[5],
        'ອາຫານ': ex_vals[0], 'ຄ່າເຊົ່າ': ex_vals[1], 'ນ້ຳໄຟ': ex_vals[2], 'ເດີນທາງ': ex_vals[3], 'ການສຶກສາ': ex_vals[4], 'ຢາ': ex_vals[5], 'ເສື້ອຜ້າ': ex_vals[6], 'ບັນເທີງ': ex_vals[7], 'ຫວຍ': ex_vals[8], 'ສ້າງເຮືອນ': ex_vals[9]
    }
    
    pd.DataFrame([new_row]).to_csv(FILE_NAME, mode='a', index=False, header=not os.path.exists(FILE_NAME), encoding='utf-8-sig')
    
    # Reset ຄ່າ
    for k in ["i1","i2","i3","i4","i5","i6","e1","e2","e3","e4","e5","e6","e7","e8","e9","e10"]:
        st.session_state[k] = ""
        st.session_state[f"raw_{k}"] = ""
        
    st.success("✅ ບັນທຶກຂໍ້ມູນສຳເລັດແລ້ວ!")
    st.rerun()

# --- ສ່ວນສະແດງຜົນ ---
if os.path.exists(FILE_NAME):
    df = pd.read_csv(FILE_NAME)
    st.write("### 📅 ປະຫວັດການເງິນ (Excel)")
    st.dataframe(df.tail(10), use_container_width=True)

    with st.expander("🛠️ ລ້າງຂໍ້ມູນທັງໝົດ"):
        pwd = st.text_input("ໃສ່ລະຫັດ 9999 ເພື່ອລົບ:", type="password")
        if st.button("🗑️ ຢືນຢັນລົບ"):
            if pwd == "9999":
                os.remove(FILE_NAME)
                st.rerun()
            else:
                st.error("ລະຫັດບໍ່ຖືກ!")