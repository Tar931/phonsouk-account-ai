import streamlit as st
import pandas as pd
import os
from datetime import datetime, timedelta

# --- ຕັ້ງຄ່າໜ້າຈໍ ---
st.set_page_config(page_title="App ບັນຊີຂອງປ້າ", layout="wide")
FILE_NAME = 'phonsouk_final_database_v3.csv'

# ລົບ Header ແລະ ຂໍ້ຄວາມທີ່ປ້າບໍ່ມັກອອກ
st.markdown("""
    <style>
    .block-container { padding-top: 1rem; }
    header {visibility: hidden;}
    footer {visibility: hidden;}
    .money-box { 
        background-color: #002B36; color: #00FFAA; padding: 15px; border-radius: 12px; 
        font-size: 22px; font-weight: bold; text-align: right; border: 2px solid #268BD2; margin-bottom: 10px;
    }
    .ai-card { 
        background-color: #f0f2f6; padding: 20px; border-radius: 15px; border-left: 10px solid #268BD2; 
        color: #1B4F72; margin-top: 10px; line-height: 1.6;
    }
    </style>
    """, unsafe_allow_html=True)

# ຟັງຊັນແປງຂໍ້ຄວາມເປັນຕົວເລກ (ສຳຄັນ: ເພື່ອບໍ່ໃຫ້ Error ຕາມຮູບ image_78e6fb.png)
def parse_num(v):
    if v == "" or v is None: return 0
    try:
        nums = "".join(filter(str.isdigit, str(v)))
        return int(nums) if nums else 0
    except:
        return 0

# --- ສ່ວນປ້ອນຂໍ້ມູນ (ແບບເກົ່າຂອງປ້າ) ---
st.markdown("### 💰 ລະບົບບ້ອນເລກແບບມີຈຸດ (Real-time)")
st.write("ບ້າພິມເລກລົງໄປ ແລ້ວກົດ Enter ຫຼື ກົດບ່ອນຫວ່າງ ມັນຈະໃສ່ຈຸດໃຫ້ທັນທີ!")

c1, c2 = st.columns(2)
with c1:
    st.success("### 🟢 ສ່ວນລາຍຮັບ")
    i1 = parse_num(st.text_input("1. ເງິນເດືອນ", value="0", key="in1"))
    i2 = parse_num(st.text_input("2. ລາຍຮັບ Creator (FB/YouTube)", value="0", key="in2"))
    i3 = parse_num(st.text_input("3. ຂາຍຂອງຍ່ອຍ", value="0", key="in3"))
    i4 = parse_num(st.text_input("4. ຮັບຕັດຫຍິບ", value="0", key="in4"))
    i5 = parse_num(st.text_input("5. ຕູ້ກົດນ້ຳ", value="0", key="in5"))
    i6 = parse_num(st.text_input("6. ຕູ້ຊັກຜ້າ", value="0", key="in6"))

with c2:
    st.error("### 🔴 ສ່ວນລາຍຈ່າຍ")
    e1 = parse_num(st.text_input("1. ຄ່າອາຫານ & ເຄື່ອງບໍລິໂພກ", value="0", key="ex1"))
    e2 = parse_num(st.text_input("2. ຄ່າເຊົ່າທີ່ຢູ່", value="0", key="ex2"))
    e3 = parse_num(st.text_input("3. ຄ່ານ້ຳ-ຄ່າໄຟ-ເນັດ", value="0", key="ex3"))
    e4 = parse_num(st.text_input("4. ຄ່າເດີນທາງ", value="0", key="ex4"))
    e5 = parse_num(st.text_input("5. ຄ່າການສຶກສາ", value="0", key="ex5"))
    e6 = parse_num(st.text_input("6. ຄ່າປິ່ນປົວ", value="0", key="ex6"))
    e7 = parse_num(st.text_input("7. ຄ່າເສື້ອຜ້າ & ຂອງໃຊ້", value="0", key="ex7"))
    e8 = parse_num(st.text_input("8. ຄ່າໂທລະສັບ & ບັນເທີງ", value="0", key="ex8"))
    e9 = parse_num(st.text_input("9. ຄ່າຫວຍ/ລາງວັນ", value="0", key="ex9"))
    e10 = parse_num(st.text_input("10. ຄ່າສ້າງເຮືອນ", value="0", key="ex10"))

submit = st.button("💾 ບັນທຶກຂໍ້ມູນທັງໝົດ", use_container_width=True)

# --- ສ່ວນບັນທຶກ (Code ທີ່ປ້າໃຫ້ເພີ່ມ) ---
if submit:
    from datetime import timedelta
    now_lao = datetime.now() + timedelta(hours=7) 
    
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
    pd.DataFrame([new_data]).to_csv(FILE_NAME, mode='a', index=False, header=not os.path.exists(FILE_NAME), encoding='utf-8-sig')
    st.success(f"✅ ບັນທຶກແລ້ວ! ເວລາລາວປັດຈຸບັນ: {now_lao.strftime('%H:%M')}")
    st.rerun()

# --- ສ່ວນ AI ວິເຄາະ (Code ທີ່ປ້າໃຫ້ເພີ່ມ) ---
if os.path.exists(FILE_NAME):
    df = pd.read_csv(FILE_NAME)
    st.markdown("---")
    st.subheader("📊 AI ວິເຄາະຕາມໄລຍະເວລາ")
    option = st.radio("ເບິ່ງລາຍງານ:", ["ມື້ນີ້", "ອາທິດນີ້", "ເດືອນນີ້", "ປີນີ້"], horizontal=True)

    df['Date_Obj'] = pd.to_datetime(df['ວັນທີ'], format="%d/%m/%Y %H:%M")
    now = datetime.now() + timedelta(hours=7)
    
    if option == "ມື້ນີ້":
        filtered_df = df[df['Date_Obj'].dt.date == now.date()]
        text_time = "ຂອງມື້ນີ້"
    elif option == "ອາທິດນີ້":
        filtered_df = df[df['Date_Obj'].dt.isocalendar().week == now.isocalendar()[1]]
        text_time = "ຂອງອາທິດນີ້"
    elif option == "ເດືອນນີ້":
        filtered_df = df[df['Date_Obj'].dt.month == now.month]
        text_time = "ຂອງເດືອນນີ້"
    else:
        filtered_df = df[df['Date_Obj'].dt.year == now.year]
        text_time = "ຂອງປີນີ້"

    if not filtered_df.empty:
        t_in_sum = filtered_df['ລາຍຮັບລວມ'].sum()
        t_ex_sum = filtered_df['ລາຍຈ່າຍລວມ'].sum()
        profit = t_in_sum - t_ex_sum
        
        c1, c2, c3 = st.columns(3)
        c1.metric(f"ລາຍຮັບ {text_time}", f"{t_in_sum:,.0f} ກີບ")
        c2.metric(f"ລາຍຈ່າຍ {text_time}", f"{t_ex_sum:,.0f} ກີບ")
        c3.metric(f"ກຳໄລ {text_time}", f"{profit:,.0f} ກີບ")

        st.markdown(f"""
        <div class="ai-card">
            <h3>🤖 AI Professional Advisor ({text_time})</h3>
            <p>✅ <b>ສະຫຼຸບການເງິນ:</b> {text_time} ປ້າມີກຳໄລສຸດທິ <b>{profit:,.0f} ກີບ</b>.</p>
            <p>📈 <b>ວິເຄາະຊ່ອງທາງລາຍໄດ້:</b> ລາຍຮັບຈາກການຫຍິບຜ້າ ແລະ ຕູ້ຢອດຫຼຽນເປັນລາຍໄດ້ທີ່ໝັ້ນຄົງທີ່ສຸດ.</p>
            <p>⚠️ <b>ຂໍ້ຄວນລະວັງ:</b> ຖ້າລາຍຈ່າຍຄ່າຫວຍ ຫຼື ຄ່າບັນເທີງສູງເກີນ 10% ຂອງລາຍຮັບ, AI ແນະນຳໃຫ້ປ້າປັບຫຼຸດລົງ.</p>
            <p>🚀 <b>ຄຳແນະນຳ:</b> ແບ່ງກຳໄລ 5% ໄປບຳລຸງຮັກສາຕູ້ຊັກຜ້າ ແລະ ຕູ້ກົດນ້ຳ ເພື່ອໃຫ້ມັນສ້າງເງິນໄດ້ຍາວໆ.</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.info(f"ຍັງບໍ່ມີຂໍ້ມູນ {text_time} ເດີ້ປ້າ!")

    # --- 4. ຕະລາງ ແລະ ປຸ່ມລົບ (Code ທີ່ປ້າໃຫ້ເພີ່ມ) ---
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