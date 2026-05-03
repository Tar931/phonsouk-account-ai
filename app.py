import streamlit as st
import pandas as pd
import os
from datetime import datetime, timedelta

# --- 1. ຕັ້ງຄ່າເບື້ອງຕົ້ນ ---
st.set_page_config(page_title="App ປ້າພອນສຸກ v3", layout="wide")
FILE_NAME = 'phonsouk_final_database_v3.csv'

# CSS ຕົບແຕ່ງໃຫ້ສວຍງາມ
st.markdown("""
    <style>
    .block-container { padding-top: 1rem; }
    header {visibility: hidden;}
    .ai-card { 
        background-color: #f0f2f6; padding: 20px; border-radius: 15px; border-left: 10px solid #268BD2; 
        color: #1B4F72; margin-top: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# ຟັງຊັນຈັດການຕົວເລກ
def format_num(v):
    nums = "".join(filter(str.isdigit, str(v)))
    return "{:,}".format(int(nums)) if nums else ""

def parse_num(v):
    nums = "".join(filter(str.isdigit, str(v)))
    return int(nums) if nums else 0

# ຟັງຊັນ Callback ເວລາປ້າພິມ (ນີ້ຄືຈຸດແກ້ໄຂໃຫ້ມັນປ່ຽນ Real-time)
def handle_change(key):
    st.session_state[key] = format_num(st.session_state[f"raw_{key}"])

# --- 2. ສ້າງຊ່ອງປ້ອນຂໍ້ມູນ ---
st.markdown(f'<div style="background-color:#1B4F72; padding:15px; border-radius:10px; text-align:center; color:white;"><h2>🏦 ລະບົບ AI ທີ່ປຶກສາການເງິນ (ປ້າພອນສຸກ)</h2></div>', unsafe_allow_html=True)
st.write("### 💰 ບ້ອນເລກແບບມີຈຸດ (ກົດ Enter ເພື່ອໃສ່ຈຸດ)")

in_keys = ["in1", "in2", "in3", "in4", "in5", "in6"]
ex_keys = ["ex1", "ex2", "ex3", "ex4", "ex5", "ex6", "ex7", "ex8", "ex9", "ex10"]
labels_in = ["1. ເງິນເດືອນ", "2. ລາຍຮັບ Creator", "3. ຂາຍຂອງຍ່ອຍ", "4. ຮັບຕັດຫຍິບ", "5. ຕູ້ກົດນ້ຳ", "6. ຕູ້ຊັກຜ້າ"]
labels_ex = ["1. ຄ່າອາຫານ", "2. ຄ່າເຊົ່າທີ່ຢູ່", "3. ຄ່ານ້ຳ-ໄຟ-ເນັດ", "4. ຄ່າເດີນທາງ", "5. ຄ່າການສຶກສາ", "6. ຄ່າປິ່ນປົວ", "7. ຄ່າເສື້ອຜ້າ", "8. ຄ່າບັນເທີງ", "9. ຄ່າຫວຍ", "10. ຄ່າສ້າງເຮືອນ"]

c1, c2 = st.columns(2)

with c1:
    st.success("### 🟢 ລາຍຮັບ")
    for k, lb in zip(in_keys, labels_in):
        if k not in st.session_state: st.session_state[k] = ""
        st.text_input(lb, value=st.session_state[k], key=f"raw_{k}", on_change=handle_change, args=(k,))

with c2:
    st.error("### 🔴 ລາຍຈ່າຍ")
    for k, lb in zip(ex_keys, labels_ex):
        if k not in st.session_state: st.session_state[k] = ""
        st.text_input(lb, value=st.session_state[k], key=f"raw_{k}", on_change=handle_change, args=(k,))

# --- 3. ປຸ່ມບັນທຶກ ---
st.write("")
if st.button("💾 ບັນທຶກຂໍ້ມູນທັງໝົດ", use_container_width=True):
    now_lao = datetime.now() + timedelta(hours=7)
    
    # ດຶງຄ່າຈາກ session_state ມາຄິດໄລ່
    v_in = [parse_num(st.session_state.get(k, "0")) for k in in_keys]
    v_ex = [parse_num(st.session_state.get(k, "0")) for k in ex_keys]
    
    t_in, t_ex = sum(v_in), sum(v_ex)
    
    new_row = {
        'ວັນທີ': now_lao.strftime("%d/%m/%Y %H:%M"),
        'ລາຍຮັບລວມ': t_in, 'ລາຍຈ່າຍລວມ': t_ex, 'ເຫຼືອເກັບ': t_in - t_ex,
        'ເງິນເດືອນ': v_in[0], 'Creator': v_in[1], 'ຂາຍຂອງ': v_in[2], 'ຫຍິບຜ້າ': v_in[3], 'ຕູ້້ກົດນ້ຳ': v_in[4], 'ຕູ້ຊັກຜ້າ': v_in[5],
        'ອາຫານ': v_ex[0], 'ຄ່າເຊົ່າ': v_ex[1], 'ນ້ຳໄຟ': v_ex[2], 'ເດີນທາງ': v_ex[3], 'ການສຶກສາ': v_ex[4], 'ຢາ': v_ex[5], 'ເສື້ອຜ້າ': v_ex[6], 'ບັນເທີງ': v_ex[7], 'ຫວຍ': v_ex[8], 'ສ້າງເຮືອນ': v_ex[9]
    }
    
    pd.DataFrame([new_row]).to_csv(FILE_NAME, mode='a', index=False, header=not os.path.exists(FILE_NAME), encoding='utf-8-sig')
    
    # ລ້າງຂໍ້ມູນຫຼັງບັນທຶກ
    for k in in_keys + ex_keys: 
        st.session_state[k] = ""
        st.session_state[f"raw_{k}"] = ""
        
    st.success("✅ ບັນທຶກ ແລະ ລ້າງຊ່ອງປ້ອນໃຫ້ແລ້ວເດີ້ປ້າ!")
    st.rerun()

# --- 4. ສ່ວນ AI ວິເຄາະ ແລະ ປະຫວັດ ---
if os.path.exists(FILE_NAME):
    df = pd.read_csv(FILE_NAME)
    st.markdown("---")
    
    # AI Summary
    total_in = df['ລາຍຮັບລວມ'].sum()
    total_ex = df['ລາຍຈ່າຍລວມ'].sum()
    st.markdown(f"""
    <div class="ai-card">
        <h3>🤖 AI ວິເຄາະພາບລວມ</h3>
        <p>ປ້າມີລາຍຮັບສະສົມທັງໝົດ <b>{total_in:,.0f}</b> ກີບ ແລະ ລາຍຈ່າຍ <b>{total_ex:,.0f}</b> ກີບ.</p>
        <p>ເຫຼືອເກັບສຸດທິ: <b>{(total_in - total_ex):,.0f}</b> ກີບ.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.write("### 📅 ປະຫວັດ 5 ລາຍການຫຼ້າສຸດ")
    st.dataframe(df.tail(5), use_container_width=True)

    # ປຸ່ມລົບ
    with st.expander("🛠️ ຈັດການຂໍ້ມູນ"):
        if st.button("🗑️ ລົບຂໍ້ມູນທັງໝົດ (ລະຫັດ 9999)"):
            st.warning("ຟັງຊັນນີ້ກຳລັງລໍຖ້າການຢືນຢັນ...")