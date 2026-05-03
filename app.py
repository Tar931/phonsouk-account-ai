import streamlit as st
import pandas as pd
import os
from datetime import datetime, timedelta

# --- ຕັ້ງຄ່າໜ້າຈໍ ---
st.set_page_config(page_title="App ປ້າ", layout="wide")
FILE_NAME = 'phonsouk_final_database_v3.csv'

# Style ຕົບແຕ່ງ (ລົບຫົວຂໍ້ ແລະ ຂໍ້ຄວາມເກົ່າອອກໝົດແລ້ວ)
st.markdown("""
    <style>
    .block-container { padding-top: 1rem; }
    header {visibility: hidden;}
    footer {visibility: hidden;}
    .money-box { 
        background-color: #002B36; color: #00FFAA; padding: 15px; border-radius: 12px; 
        font-size: 24px; font-weight: bold; text-align: right; border: 2px solid #268BD2; margin-bottom: 10px;
    }
    .ai-card { 
        background-color: #f0f2f6; padding: 20px; border-radius: 15px; border-left: 10px solid #268BD2; 
        color: #1B4F72; margin-top: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# ຟັງຊັນຈັດຮູບແບບຕົວເລກ (ໃສ່ຈຸດ)
def format_num(v):
    if v == "" or v is None: return ""
    nums = "".join(filter(str.isdigit, str(v)))
    return "{:,}".format(int(nums)) if nums else ""

# ຟັງຊັນແປງເປັນຕົວເລກເພື່ອຄິດໄລ່
def parse_num(v):
    if v == "" or v is None: return 0
    nums = "".join(filter(str.isdigit, str(v)))
    return int(nums) if nums else 0

# ຊ່ອງປ້ອນຂໍ້ມູນແບບມີຈຸດ (Real-time)
def input_box(label, key):
    if key not in st.session_state: st.session_state[key] = ""
    val = st.text_input(label, value=st.session_state[key], key=f"k_{key}")
    new_val = format_num(val)
    if new_val != st.session_state[key]:
        st.session_state[key] = new_val
        st.rerun()
    return new_val

# --- ສ່ວນປ້ອນຂໍ້ມູນ ---
c1, c2 = st.columns(2)
with c1:
    st.success("### 🟢 ລາຍຮັບ")
    i1 = input_box("1. ເງິນເດືອນ", "i1")
    i2 = input_box("2. ລາຍຮັບ Creator (FB/YouTube)", "i2")
    i3 = input_box("3. ຂາຍຂອງຍ່ອຍ", "i3")
    i4 = input_box("4. ຮັບຕັດຫຍິບ", "i4")
    i5 = input_box("5. ຕູ້ກົດນ້ຳ", "i5")
    i6 = input_box("6. ຕູ້ຊັກຜ້າ", "i6")

with c2:
    st.error("### 🔴 ລາຍຈ່າຍ")
    e1 = input_box("1. ຄ່າອາຫານ & ເຄື່ອງບໍລິໂພກ", "e1")
    e2 = input_box("2. ຄ່າເຊົ່າທີ່ຢູ່", "e2")
    e3 = input_box("3. ຄ່ານ້ຳ-ຄ່າໄຟ-ເນັດ", "e3")
    e4 = input_box("4. ຄ່າເດີນທາງ", "e4")
    e5 = input_box("5. ຄ່າການສຶກສາ", "e5")
    e6 = input_box("6. ຄ່າປິ່ນປົວ", "e6")
    e7 = input_box("7. ຄ່າເສື້ອຜ້າ & ຂອງໃຊ້", "e7")
    e8 = input_box("8. ຄ່າໂທລະສັບ & ບັນເທີງ", "e8")
    e9 = input_box("9. ຄ່າຫວຍ/ລາງວັນ", "e9")
    e10 = input_box("10. ຄ່າສ້າງເຮືອນ", "e10")

# --- ສ່ວນບັນທຶກຂໍ້ມູນ (ລວມ Code ທີ່ປ້າເພີ່ມ) ---
st.write("")
if st.button("💾 ບັນທຶກຂໍ້ມູນ", use_container_width=True):
    # ບວກ 7 ຊົ່ວໂມງເປັນເວລາລາວ
    now_lao = datetime.now() + timedelta(hours=7) 
    
    # ແປງຄ່າຈາກຊ່ອງປ້ອນໃຫ້ເປັນຕົວເລກ
    n_i1, n_i2, n_i3, n_i4, n_i5, n_i6 = parse_num(i1), parse_num(i2), parse_num(i3), parse_num(i4), parse_num(i5), parse_num(i6)
    n_e1, n_e2, n_e3, n_e4, n_e5, n_e6, n_e7, n_e8, n_e9, n_e10 = parse_num(e1), parse_num(e2), parse_num(e3), parse_num(e4), parse_num(e5), parse_num(e6), parse_num(e7), parse_num(e8), parse_num(e9), parse_num(e10)
    
    t_in = n_i1 + n_i2 + n_i3 + n_i4 + n_i5 + n_i6
    t_ex = n_e1 + n_e2 + n_e3 + n_e4 + n_e5 + n_e6 + n_e7 + n_e8 + n_e9 + n_e10
    
    new_data = {
        'ວັນທີ': now_lao.strftime("%d/%m/%Y %H:%M"), 
        'ລາຍຮັບລວມ': t_in, 
        'ລາຍຈ່າຍລວມ': t_ex, 
        'ເຫຼືອເກັບ': t_in - t_ex,
        'ເງິນເດືອນ': n_i1, 'Creator': n_i2, 'ຂາຍຂອງ': n_i3, 'ຫຍິບຜ້າ': n_i4, 'ຕູ້້ກົດນ້ຳ': n_i5, 'ຕູ້ຊັກຜ້າ': n_i6,
        'ອາຫານ': n_e1, 'ຄ່າເຊົ່າ': n_e2, 'ນ້ຳໄຟ': n_e3, 'ເດີນທາງ': n_e4, 'ການສຶກສາ': n_e5, 'ຢາ': n_e6, 'ເສື້ອຜ້າ': n_e7, 'ບັນເທີງ': n_e8, 'ຫວຍ': n_e9, 'ສ້າງເຮືອນ': n_e10
    }
    
    # ບັນທຶກລົງ CSV
    pd.DataFrame([new_data]).to_csv(FILE_NAME, mode='a', index=False, header=not os.path.exists(FILE_NAME), encoding='utf-8-sig')
    st.success(f"✅ ບັນທຶກແລ້ວ! ເວລາລາວ: {now_lao.strftime('%H:%M')}")
    st.balloons()
    st.rerun()

# --- ສະແດງຜົນລວມ ---
st.markdown("---")
ti = parse_num(i1)+parse_num(i2)+parse_num(i3)+parse_num(i4)+parse_num(i5)+parse_num(i6)
te = parse_num(e1)+parse_num(e2)+parse_num(e3)+parse_num(e4)+parse_num(e5)+parse_num(e6)+parse_num(e7)+parse_num(e8)+parse_num(e9)+parse_num(e10)
bal = ti - te

ca, cb, cc = st.columns(3)
with ca: st.markdown(f'<div class="money-box">💰 ລາຍຮັບ<br>{format_num(ti)}</div>', unsafe_allow_html=True)
with cb: st.markdown(f'<div class="money-box">💸 ລາຍຈ່າຍ<br>{format_num(te)}</div>', unsafe_allow_html=True)
with cc: 
    color = "#00FFAA" if bal >= 0 else "#FF5555"
    st.markdown(f'<div class="money-box" style="color:{color}">📊 ສົມດຸນ<br>{format_num(bal)}</div>', unsafe_allow_html=True)

# --- ປະຫວັດ (Excel) ---
if os.path.exists(FILE_NAME):
    st.markdown("---")
    st.subheader("📅 ປະຫວັດການເງິນ (10 ລາຍການຫຼ້າສຸດ)")
    df = pd.read_csv(FILE_NAME)
    st.dataframe(df.tail(10), use_container_width=True)
