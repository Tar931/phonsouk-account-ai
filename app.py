import streamlit as st
import pandas as pd
import os
from datetime import datetime, timedelta

# --- ຕັ້ງຄ່າໜ້າຈໍ ---
st.set_page_config(page_title="App ປ້າ", layout="wide")
FILE_NAME = 'phonsouk_final_database_v3.csv'

# ລົບ Header ແລະ ຂໍ້ຄວາມທີ່ປ້າບໍ່ມັກອອກໃຫ້ໝົດ
st.markdown("""
    <style>
    .block-container { padding-top: 0rem; }
    header {visibility: hidden;}
    footer {visibility: hidden;}
    .money-box { 
        background-color: #002B36; color: #00FFAA; padding: 15px; border-radius: 12px; 
        font-size: 24px; font-weight: bold; text-align: right; border: 2px solid #268BD2; margin-bottom: 10px;
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

# ຊ່ອງປ້ອນຂໍ້ມູນແບບມີຈຸດ
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
    i1_val = input_box("1. ເງິນເດືອນ", "i1")
    i2_val = input_box("2. ລາຍຮັບ Creator (FB/YouTube)", "i2")
    i3_val = input_box("3. ຂາຍຂອງຍ່ອຍ", "i3")
    i4_val = input_box("4. ຮັບຕັດຫຍິບ", "i4")
    i5_val = input_box("5. ຕູ້ກົດນ້ຳ", "i5")
    i6_val = input_box("6. ຕູ້ຊັກຜ້າ", "i6")

with c2:
    st.error("### 🔴 ລາຍຈ່າຍ")
    e1_val = input_box("1. ຄ່າອາຫານ & ເຄື່ອງບໍລິໂພກ", "e1")
    e2_val = input_box("2. ຄ່າເຊົ່າທີ່ຢູ່", "e2")
    e3_val = input_box("3. ຄ່ານ້ຳ-ຄ່າໄຟ-ເນັດ", "e3")
    e4_val = input_box("4. ຄ່າເດີນທາງ", "e4")
    e5_val = input_box("5. ຄ່າການສຶກສາ", "e5")
    e6_val = input_box("6. ຄ່າປິ່ນປົວ", "e6")
    e7_val = input_box("7. ຄ່າເສື້ອຜ້າ & ຂອງໃຊ້", "e7")
    e8_val = input_box("8. ຄ່າໂທລະສັບ & ບັນເທີງ", "e8")
    e9_val = input_box("9. ຄ່າຫວຍ/ລາງວັນ", "e9")
    e10_val = input_box("10. ຄ່າສ້າງເຮືອນ", "e10")

# --- ປຸ່ມບັນທຶກ (ນີ້ຄືສ່ວນທີ່ປ້າໃຫ້ເພີ່ມ) ---
st.write("")
submit = st.button("💾 ບັນທຶກຂໍ້ມູນ", use_container_width=True)

if submit:
    # ບວກ 7 ຊົ່ວໂມງເຂົ້າໄປຕົງໆເລີຍ ເພື່ອໃຫ້ເປັນເວລາລາວ
    now_lao = datetime.now() + timedelta(hours=7) 
    
    # ແປງຄ່າໃຫ້ເປັນຕົວເລກກ່ອນຄິດໄລ່
    i1, i2, i3, i4, i5, i6 = parse_num(i1_val), parse_num(i2_val), parse_num(i3_val), parse_num(i4_val), parse_num(i5_val), parse_num(i6_val)
    e1, e2, e3, e4, e5, e6, e7, e8, e9, e10 = parse_num(e1_val), parse_num(e2_val), parse_num(e3_val), parse_num(e4_val), parse_num(e5_val), parse_num(e6_val), parse_num(e7_val), parse_num(e8_val), parse_num(e9_val), parse_num(e10_val)
    
    t_in = i1+i2+i3+i4+i5+i6
    t_ex = e1+e2+e3+e4+e5+e6+e7+e8+e9+e10
    
    new_data = {
        'ວັນທີ': now_lao.strftime("%d/%m/%Y %H:%M"), 
        'ລາຍຮັບລວມ': t_in, 
        'ລາຍຈ່າຍລວມ': t_ex, 
        'ເຫຼືອເກັບ': t_in - t_ex,
        'ເງິນເດືອນ': i1, 'Creator': i2, 'ຂາຍຂອງ': i3, 'ຫຍິບຜ້າ': i4, 'ຕູ້້ກົດນ້ຳ': i5, 'ຕູ້ຊັກຜ້າ': i6,
        'ອາຫານ': e1, 'ຄ່າເຊົ່າ': e2, 'ນ້ຳໄຟ': e3, 'ເດີນທາງ': e4, 'ການສຶກສາ': e5, 'ຢາ': e6, 'ເສື້ອຜ້າ': e7, 'ບັນເທີງ': e8, 'ຫວຍ': e9, 'ສ້າງເຮືອນ': e10
    }
    
    # ບັນທຶກລົງ CSV (utf-8-sig ເພື່ອໃຫ້ Excel ອ່ານພາສາລາວອອກ)
    pd.DataFrame([new_data]).to_csv(FILE_NAME, mode='a', index=False, header=not os.path.exists(FILE_NAME), encoding='utf-8-sig')
    
    st.success(f"✅ ບັນທຶກແລ້ວ! ເວລາລາວປັດຈຸບັນ: {now_lao.strftime('%H:%M')}")
    st.rerun()

# --- ສະແດງຜົນລວມລຸ່ມສຸດ ---
st.markdown("---")
ti = parse_num(i1_val)+parse_num(i2_val)+parse_num(i3_val)+parse_num(i4_val)+parse_num(i5_val)+parse_num(i6_val)
te = parse_num(e1_val)+parse_num(e2_val)+parse_num(e3_val)+parse_num(e4_val)+parse_num(e5_val)+parse_num(e6_val)+parse_num(e7_val)+parse_num(e8_val)+parse_num(e9_val)+parse_num(e10_val)
bal = ti - te

ca, cb, cc = st.columns(3)
with ca: st.markdown(f'<div class="money-box">💰 ລາຍຮັບ: {format_num(ti)}</div>', unsafe_allow_html=True)
with cb: st.markdown(f'<div class="money-box">💸 ລາຍຈ່າຍ: {format_num(te)}</div>', unsafe_allow_html=True)
with cc: 
    col_bal = "#00FFAA" if bal >= 0 else "#FF5555"
    st.markdown(f'<div class="money-box" style="color:{col_bal}">📊 ສົມດຸນ: {format_num(bal)}</div>', unsafe_allow_html=True)

# ປະຫວັດ
if os.path.exists(FILE_NAME):
    with st.expander("📜 ເບິ່ງປະຫວັດການບັນທຶກ"):
        df = pd.read_csv(FILE_NAME)
        st.dataframe(df.tail(10), use_container_width=True)
