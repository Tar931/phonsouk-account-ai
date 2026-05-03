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

# 1. ຟັງຊັນຈັດຮູບແບບຕົວເລກ (ໃຫ້ມີຈຸດ)
def format_num(v):
    if v == "" or v is None: return ""
    nums = "".join(filter(str.isdigit, str(v)))
    return "{:,}".format(int(nums)) if nums else ""

# 2. ຟັງຊັນແປງເປັນຕົວເລກແທ້ເພື່ອຄິດໄລ່
def parse_num(v):
    if v == "" or v is None: return 0
    nums = "".join(filter(str.isdigit, str(v)))
    return int(nums) if nums else 0

# 3. ຟັງຊັນຊ່ອງປ້ອນຂໍ້ມູນ (ອັນນີ້ແຫຼະທີ່ຈະເຮັດໃຫ້ມັນປ່ຽນ Real-time)
def input_box(label, key_name):
    # ຖ້າບໍ່ທັນມີຄ່າໃນລະບົບ ໃຫ້ຕັ້ງເປັນຄ່າຫວ່າງ
    if key_name not in st.session_state:
        st.session_state[key_name] = ""
    
    # ສ້າງຊ່ອງປ້ອນ
    val = st.text_input(label, value=st.session_state[key_name], key=f"input_{key_name}")
    
    # ຈັດຮູບແບບໃຫ້ມີຈຸດ
    formatted = format_num(val)
    
    # ຖ້າຄ່າທີ່ພິມປ່ຽນໄປ ໃຫ້ Update ແລະ Rerun ທັນທີ
    if formatted != st.session_state[key_name]:
        st.session_state[key_name] = formatted
        st.rerun()
    
    return formatted

# --- ສ່ວນຫົວຂໍ້ ---
st.markdown("### 💰 ລະບົບບ້ອນເລກແບບມີຈຸດ (Real-time)")
st.write("ປ້າພິມເລກລົງໄປ ແລ້ວກົດ Enter ຫຼື ກົດບ່ອນຫວ່າງ ມັນຈະໃສ່ຈຸດໃຫ້ທັນທີ!")

# --- ສ່ວນປ້ອນຂໍ້ມູນ ---
c1, c2 = st.columns(2)

with c1:
    st.success("### 🟢 ສ່ວນລາຍຮັບ")
    i1_v = input_box("1. ເງິນເດືອນ", "i1")
    i2_v = input_box("2. ລາຍຮັບ Creator (FB/YouTube)", "i2")
    i3_v = input_box("3. ຂາຍຂອງຍ່ອຍ", "i3")
    i4_v = input_box("4. ຮັບຕັດຫຍິບ", "i4")
    i5_v = input_box("5. ຕູ້ກົດນ້ຳ", "i5")
    i6_v = input_box("6. ຕູ້ຊັກຜ້າ", "i6")

with c2:
    st.error("### 🔴 ສ່ວນລາຍຈ່າຍ")
    e1_v = input_box("1. ຄ່າອາຫານ & ເຄື່ອງບໍລິໂພກ", "e1")
    e2_v = input_box("2. ຄ່າເຊົ່າທີ່ຢູ່", "e2")
    e3_v = input_box("3. ຄ່ານ້ຳ-ຄ່າໄຟ-ເນັດ", "e3")
    e4_v = input_box("4. ຄ່າເດີນທາງ", "e4")
    e5_v = input_box("5. ຄ່າການສຶກສາ", "e5")
    e6_v = input_box("6. ຄ່າປິ່ນປົວ", "e6")
    e7_v = input_box("7. ຄ່າເສື້ອຜ້າ & ຂອງໃຊ້", "e7")
    e8_v = input_box("8. ຄ່າໂທລະສັບ & ບັນເທີງ", "e8")
    e9_v = input_box("9. ຄ່າຫວຍ/ລາງວັນ", "e9")
    e10_v = input_box("10. ຄ່າສ້າງເຮືອນ", "e10")

submit = st.button("💾 ບັນທຶກຂໍ້ມູນທັງໝົດ", use_container_width=True)

# --- 4. ສ່ວນບັນທຶກຂໍ້ມູນ ---
if submit:
    now_lao = datetime.now() + timedelta(hours=7) 
    
    # ແປງທຸກຢ່າງເປັນຕົວເລກເພື່ອບວກກັນ
    v_i = [parse_num(i1_v), parse_num(i2_v), parse_num(i3_v), parse_num(i4_v), parse_num(i5_v), parse_num(i6_v)]
    v_e = [parse_num(e1_v), parse_num(e2_v), parse_num(e3_v), parse_num(e4_v), parse_num(e5_v), parse_num(e6_v), parse_num(e7_v), parse_num(e8_v), parse_num(e9_v), parse_num(e10_v)]
    
    t_in = sum(v_i)
    t_ex = sum(v_e)
    
    new_data = {
        'ວັນທີ': now_lao.strftime("%d/%m/%Y %H:%M"), 
        'ລາຍຮັບລວມ': t_in, 
        'ລາຍຈ່າຍລວມ': t_ex, 
        'ເຫຼືອເກັບ': t_in - t_ex,
        'ເງິນເດືອນ': v_i[0], 'Creator': v_i[1], 'ຂາຍຂອງ': v_i[2], 'ຫຍິບຜ້າ': v_i[3], 'ຕູ້້ກົດນ້ຳ': v_i[4], 'ຕູ້ຊັກຜ້າ': v_i[5],
        'ອາຫານ': v_e[0], 'ຄ່າເຊົ່າ': v_e[1], 'ນ້ຳໄຟ': v_e[2], 'ເດີນທາງ': v_e[3], 'ການສຶກສາ': v_e[4], 'ຢາ': v_e[5], 'ເສື້ອຜ້າ': v_e[6], 'ບັນເທີງ': v_e[7], 'ຫວຍ': v_e[8], 'ສ້າງເຮືອນ': v_e[9]
    }
    
    pd.DataFrame([new_data]).to_csv(FILE_NAME, mode='a', index=False, header=not os.path.exists(FILE_NAME), encoding='utf-8-sig')
    
    # ລ້າງຄ່າໃນຊ່ອງປ້ອນຫຼັງບັນທຶກ
    for k in ["i1","i2","i3","i4","i5","i6","e1","e2","e3","e4","e5","e6","e7","e8","e9","e10"]:
        st.session_state[k] = ""
        
    st.success(f"✅ ບັນທຶກແລ້ວ! ເວລາ: {now_lao.strftime('%H:%M')}")
    st.rerun()

# --- 5. ສ່ວນ AI ວິເຄາະ ແລະ ຕະລາງ ---
if os.path.exists(FILE_NAME):
    df = pd.read_csv(FILE_NAME)
    st.markdown("---")
    
    # ຕະລາງ Excel
    st.write("### 📅 ປະຫວັດການເງິນ (Excel)")
    st.dataframe(df.tail(10), use_container_width=True)

    # ປຸ່ມລົບຂໍ້ມູນ
    with st.expander("🛠️ ລ້າງຂໍ້ມູນທັງໝົດ"):
        pwd = st.text_input("ໃສ່ລະຫັດ 9999 ເພື່ອລົບ:", type="password")
        if st.button("🗑️ ຢືນຢັນລົບ"):
            if pwd == "9999":
                os.remove(FILE_NAME)
                st.rerun()
            else:
                st.error("ລະຫັດບໍ່ຖືກ!")