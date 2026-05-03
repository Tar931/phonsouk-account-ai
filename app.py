import streamlit as st
import pandas as pd
import os
from datetime import datetime, timedelta

# --- ຕັ້ງຄ່າໜ້າຈໍ ---
st.set_page_config(page_title="App ບັນຊີຂອງປ້າ", layout="wide")
FILE_NAME = 'phonsouk_final_database_v3.csv'

# --- ຫົວຂໍ້ແບບປອດໄພ 100% ---
header_text = """
<div style="background-color: #1B4F72; padding: 25px; border-radius: 15px; border: 3px solid #F1C40F; text-align: center; color: white;">
    <h1 style="margin: 0;">🌸 ລະບົບບັນຊີ AI ປ້າພອນສຸກ </h1>
    <p style="margin: 10px 0;">ເບີໂທ: 020 99858310 | Line: Tarvan</p>
    <p style="margin: 0;">Facebook: ນາງພອນສຸກ ພັນທະຜອງ</p>
    <div style="font-size: 30px; margin-top: 10px;">🌸 🇱🇦 🌸</div>
</div>
<br>
"""
st.write(header_text, unsafe_allow_html=True)


# 1. ຟັງຊັນຈັດຮູບແບບຕົວເລກ (ໃຫ້ມີຈຸດຄືເກົ່າ)
def format_num(v):
    if v == "" or v is None: return ""
    nums = "".join(filter(str.isdigit, str(v)))
    return "{:,}".format(int(nums)) if nums else ""

# 2. ຟັງຊັນແປງເປັນຕົວເລກເພື່ອຄິດໄລ່ (ປ້ອງກັນ Error ຕາມຮູບ image_78df7d.png)
def parse_num(v):
    if v == "" or v is None: return 0
    nums = "".join(filter(str.isdigit, str(v)))
    return int(nums) if nums else 0

# 3. ຟັງຊັນສ້າງຊ່ອງປ້ອນຂໍ້ມູນແບບ Real-time (ອັນນີ້ຈະເຮັດໃຫ້ມັນໃສ່ຈຸດທັນທີ)
def input_box(label, key):
    if key not in st.session_state: st.session_state[key] = ""
    val = st.text_input(label, value=st.session_state[key], key=f"k_{key}")
    new_val = format_num(val)
    if new_val != st.session_state[key]:
        st.session_state[key] = new_val
        st.rerun()
    return new_val

# --- 1. ສ່ວນຂອງຊ່ອງປ້ອນຂໍ້ມູນ (ຕ້ອງຕັ້ງຊື່ i ແລະ e ແບບນີ້ AI ຈຶ່ງຈະເຫັນ) ---
st.write("### 💰 ປ້ອນລາຍຮັບ-ລາຍຈ່າຍ")
col1, col2 = st.columns(2)

with col1:
    st.success("🟢 ສ່ວນລາຍຮັບ")
    i1 = st.number_input("1. ລາຍຮັບເງິນເດືອນ", value=0, step=1000)
    i2 = st.number_input("2. ລາຍຮັບ Creator", value=0, step=1000)
    i3 = st.number_input("3. ຂາຍຂອງ", value=0, step=1000)
    i4 = st.number_input("4. ຫຍິບຜ້າ", value=0, step=1000)
    i5 = st.number_input("5. ຕູ້ກົດນ້ຳ", value=0, step=1000)
    i6 = st.number_input("6. ຕູ້ຊັກຜ້າ", value=0, step=1000)
    i7 = st.number_input("7. ອາຫານ(ຮັບ)", value=0, step=1000)
    i8 = st.number_input("8. ລາຍຮັບອື່ນໆ", value=0, step=1000)

with col2:
    st.error("🔴 ສ່ວນລາຍຈ່າຍ")
    e1 = st.number_input("1. ຄ່າອາຫານ", value=0, step=1000)
    e2 = st.number_input("2. ຄ່າເຊົ່າ", value=0, step=1000)
    e3 = st.number_input("3. ນ້ຳໄຟ", value=0, step=1000)
    e4 = st.number_input("4. ເດີນທາງ", value=0, step=1000)
    e5 = st.number_input("5. ການສຶກສາ", value=0, step=1000)
    e6 = st.number_input("6. ຢາ", value=0, step=1000)
    e7 = st.number_input("7. ເສື້ອຜ້າ", value=0, step=1000)
    e8 = st.number_input("8. ຄ່າໂທລະສັບ & ບັນເທີງ", value=0, step=1000)
    e9 = st.number_input("9. ຄ່າຫວຍ/ລາງວັນ", value=0, step=1000)
    e10 = st.number_input("10. ຄ່າສ້າງເຮືອນ", value=0, step=1000)
    e11 = st.number_input("11. ຄ່າຊື້ສິນຄ້າເຂົ້າຮ້ານ", value=0, step=1000)

# --- 2. ສ່ວນປຸ່ມບັນທຶກ ແລະ ສະແດງຜົນແບບມີຈຸດ (,) ---
if st.button("💾 ບັນທຶກຂໍ້ມູນທັງໝົດ", use_container_width=True):
    # ຄິດໄລ່ຍອດລວມ
    total_in = float(i1 + i2 + i3 + i4 + i5 + i6 + i7 + i8)
    total_ex = float(e1 + e2 + e3 + e4 + e5 + e6 + e7 + e8 + e9 + e10 + e11)
    balance = total_in - total_ex
    
    # ສະແດງຍອດລວມແບບມີຈຸດຂັ້ນ (,) ໃຫ້ເຫັນທັນທີ
    st.info(f"📊 ສະຫຼຸບຕອນນີ້: ຮັບ {total_in:,.0f} | ຈ່າຍ {total_ex:,.0f} | ເຫຼືອ {balance:,.0f} ກີບ")
    
    # ບັນທຶກລົງ CSV
    new_entry = {
        'ວັນທີ': datetime.now().strftime("%d/%m/%Y %H:%M"),
        'ລາຍຮັບລວມ': total_in, 'ລາຍຈ່າຍລວມ': total_ex, 'ເຫຼືອກັບ': balance,
        'ເງິນເດືອນ': i1, 'ອາຫານ': e1, 'ສ້າງເຮືອນ': e10 # (ຕື່ມໃຫ້ຄົບຕາມ Columns ຂອງປ້າ)
    }
    
    df_new = pd.DataFrame([new_entry])
    if not os.path.exists(FILE_NAME):
        df_new.to_csv(FILE_NAME, index=False, encoding='utf-8-sig')
    else:
        df_new.to_csv(FILE_NAME, mode='a', index=False, header=False, encoding='utf-8-sig')
    
    st.success("✅ ບັນທຶກຂໍ້ມູນຮຽບຮ້ອຍແລ້ວ!")
    st.rerun()

# --- 3. ສ່ວນຕາຕະລາງ Excel ໃຫ້ມີຈຸດທັງໝົດ ---
if os.path.exists(FILE_NAME):
    df_show = pd.read_csv(FILE_NAME)
    if not df_show.empty:
        st.write("### 📊 ປະຫວັດການເງິນ (ແບບມີຈຸດຂັ້ນ)")
        # ບັງຄັບໃຫ້ທຸກຖັນຕົວເລກມີຈຸດຂັ້ນອັດຕະໂນມັດ
        st.dataframe(df_show.style.format(thousands=",", precision=0), use_container_width=True)

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
 
# --- ຕະລາງ Excel ແລະ ປຸ່ມລົບ (Code ທີ່ປ້າໃຫ້ເພີ່ມ) ---
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
