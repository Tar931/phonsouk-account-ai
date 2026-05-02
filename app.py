import streamlit as st
import pandas as pd
import os
from datetime import datetime

# --- ຕັ້ງຄ່າໜ້າຈໍ ---
st.set_page_config(page_title="ບັນຊີຂອງປ້າ", page_icon="💰", layout="wide")
FILE_NAME = 'phonsouk_final_database_v3.csv'

# Style ຕົບແຕ່ງ (ປັບໃຫ້ເບິ່ງງ່າຍ)
st.markdown("""
    <style>
    .money-box { 
        background-color: #002B36; color: #00FFAA; padding: 15px; border-radius: 12px; 
        font-size: 28px; font-weight: bold; text-align: right; border: 2px solid #268BD2; margin-bottom: 20px;
    }
    .ai-card { 
        background-color: #ffffff; padding: 25px; border-radius: 20px; border-left: 15px solid #268BD2; 
        box-shadow: 0 4px 15px rgba(0,0,0,0.1); color: #1B4F72; margin-top: 20px; font-size: 18px;
    }
    /* ລົບ padding ສ່ວນເກີນອອກ */
    .block-container { padding-top: 2rem; }
    </style>
    """, unsafe_allow_html=True)

# ຟັງຊັນຈັດຮູບແບບຕົວເລກ (ໃສ່ຈຸດ)
def format_num(v):
    if v == "" or v is None: return ""
    nums = "".join(filter(str.isdigit, str(v)))
    return "{:,}".format(int(nums)) if nums else ""

# ຟັງຊັນແປງເປັນຕົວເລກ (ເພື່ອຄິດໄລ່)
def parse_num(v):
    if v == "" or v is None: return 0
    nums = "".join(filter(str.isdigit, str(v)))
    return int(nums) if nums else 0

# ຊ່ອງປ້ອນຂໍ້ມູນແບບມີຈຸດ Real-time
def input_box(label, key):
    if key not in st.session_state:
        st.session_state[key] = ""
    val = st.text_input(label, value=st.session_state[key], key=f"k_{key}")
    new_val = format_num(val)
    if new_val != st.session_state[key]:
        st.session_state[key] = new_val
        st.rerun()
    return new_val

def save_data(data_dict):
    df_new = pd.DataFrame([data_dict])
    if os.path.exists(FILE_NAME):
        df_existing = pd.read_csv(FILE_NAME)
        df_combined = pd.concat([df_existing, df_new], ignore_index=True)
    else:
        df_combined = df_new
    df_combined.to_csv(FILE_NAME, index=False, encoding='utf-8-sig')
    return True

# --- ສ່ວນການປ້ອນຂໍ້ມູນ ---
col1, col2 = st.columns(2)

with col1:
    st.success("### 🟢 ລາຍຮັບ")
    i1 = input_box("1. ເງິນເດືອນ", "i1")
    i2 = input_box("2. ລາຍຮັບ Creator (FB/YouTube)", "i2")
    i3 = input_box("3. ຂາຍຂອງຍ່ອຍ", "i3")
    i4 = input_box("4. ຮັບຕັດຫຍິບ", "i4")
    i5 = input_box("5. ຕູ້ກົດນ້ຳ", "i5")
    i6 = input_box("6. ຕູ້ຊັກຜ້າ", "i6")

with col2:
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

# --- ປຸ່ມບັນທຶກ ---
st.write("")
if st.button("💾 ບັນທຶກ", use_container_width=True):
    data = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "ເງິນເດືອນ": parse_num(i1),
        "ລາຍຮັບ Creator": parse_num(i2),
        "ຂາຍຂອງຍ່ອຍ": parse_num(i3),
        "ຮັບຕັດຫຍິບ": parse_num(i4),
        "ຕູ້ກົດນ້ຳ": parse_num(i5),
        "ຕູ້ຊັກຜ້າ": parse_num(i6),
        "ຄ່າອາຫານ": parse_num(e1),
        "ຄ່າເຊົ່າ": parse_num(e2),
        "ຄ່ານ້ຳ-ໄຟ-ເນັດ": parse_num(e3),
        "ຄ່າເດີນທາງ": parse_num(e4),
        "ຄ່າການສຶກສາ": parse_num(e5),
        "ຄ່າປິ່ນປົວ": parse_num(e6),
        "ຄ່າເສື້ອຜ້າ": parse_num(e7),
        "ຄ່າໂທລະສັບ": parse_num(e8),
        "ຄ່າຫວຍ": parse_num(e9),
        "ຄ່າສ້າງເຮືອນ": parse_num(e10),
    }
    if save_data(data):
        st.success("✅ ບັນທຶກສຳເລັດ!")
        st.balloons()

if submit:
        # ບວກ 7 ຊົ່ວໂມງເຂົ້າໄປຕົງໆເລີຍ ເພື່ອໃຫ້ເປັນເວລາລາວ
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
        pd.DataFrame([new_data]).to_csv(FILE_NAME, mode='a', index=False, header=not os.path.exists(FILE_NAME))
        st.success(f"✅ ບັນທຶກແລ້ວ! ເວລາລາວປັດຈຸບັນ: {now_lao.strftime('%H:%M')}")
        st.rerun()
# --- ສ່ວນ AI ວິເຄາະແບບມືອາຊີບ (ທຸກໄລຍະ) ---
if os.path.exists(FILE_NAME):
    df = pd.read_csv(FILE_NAME)
    st.markdown("---")
    
    # 1. ປຸ່ມໃຫ້ປ້າເລືອກເບິ່ງໄລຍະເວລາ
    st.subheader("📊 ເລືອກໄລຍະເວລາທີ່ປ້າຢາກໃຫ້ AI ວິເຄາະ")
    option = st.radio("ເບິ່ງລາຍງານ:", ["ມື້ນີ້", "ອາທິດນີ້", "ເດືອນນີ້", "ປີນີ້"], horizontal=True)

    # 2. ຈັດການຂໍ້ມູນຕາມໄລຍະເວລາທີ່ເລືອກ
    df['Date_Obj'] = pd.to_datetime(df['ວັນທີ'], format="%d/%m/%Y %H:%M")
    now = datetime.now()
    
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

    # 3. ສະແດງຕົວເລກສະຫຼຸບ
    if not filtered_df.empty:
        t_in = filtered_df['ລາຍຮັບລວມ'].sum()
        t_ex = filtered_df['ລາຍຈ່າຍລວມ'].sum()
        profit = t_in - t_ex
        
        c1, c2, c3 = st.columns(3)
        c1.metric(f"ລາຍຮັບ {text_time}", f"{t_in:,.0f} ກີບ")
        c2.metric(f"ລາຍຈ່າຍ {text_time}", f"{t_ex:,.0f} ກີບ")
        c3.metric(f"ກຳໄລ {text_time}", f"{profit:,.0f} ກີບ")

        # 4. ບົດວິເຄາະ AI ແບບເຈາະຈຶກ
        st.markdown(f"""
        <div class="ai-card">
            <h3>🤖 AI Professional Advisor ({text_time})</h3>
            <p>✅ <b>ສະຫຼຸບການເງິນ:</b> {text_time} ປ້າມີກຳໄລສຸດທິ <b>{profit:,.0f} ກີບ</b>.</p>
            <p>📈 <b>ວິເຄາະຊ່ອງທາງລາຍໄດ້:</b> ລາຍຮັບຈາກການຫຍິບຜ້າ ແລະ ຕູ້ຢອດຫຼຽນເປັນລາຍໄດ້ທີ່ໝັ້ນຄົງທີ່ສຸດ.</p>
            <p>⚠️ <b>ຂໍ້ຄວນລະວັງ:</b> ຖ້າລາຍຈ່າຍຄ່າຫວຍ ຫຼື ຄ່າບັນເທີງສູງເກີນ 10% ຂອງລາຍຮັບ, AI ແນະນຳໃຫ້ປ້າປັບຫຼຸດລົງເພື່ອເອົາໄປໃສ່ຄ່າສ້າງເຮືອນແທນ.</p>
            <p>🚀 <b>ຄຳແນະນຳມືອາຊີບ:</b> ໃນໄລຍະ {text_time}, ປ້າຄວນແບ່ງກຳໄລ 5% ໄປບຳລຸງຮັກສາຕູ້ຊັກຜ້າ ແລະ ຕູ້ກົດນ້ຳ ເພື່ອໃຫ້ມັນສ້າງເງິນໃຫ້ປ້າໄດ້ຍາວໆ.</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.info(f"ຍັງບໍ່ມີຂໍ້ມູນ {text_time} ເດີ້ປ້າ!")

 # ຕະລາງ Excel
    st.write("### 📅 ປະຫວັດການເງິນ (Excel)")
    st.dataframe(df.tail(10), use_container_width=True)

    # --- ປຸ່ມລົບ (Password Lock) ---
    with st.expander("🛠️ ລ້າງຂໍ້ມູນທັງໝົດ"):
        pwd = st.text_input("ໃສ່ລະຫັດ 9999 ເພື່ອລົບ:", type="password")
        if st.button("🗑️ ຢືນຢັນລົບ"):
            if pwd == "9999":
                os.remove(FILE_NAME)
                st.rerun()
            else:
                st.error("ລະຫັດບໍ່ຖືກ!")