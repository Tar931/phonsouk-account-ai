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

# ໂຫຼດຂໍ້ມູນມາເພື່ອຄິດໄລ່ຍອດລວມສະສົມ
if os.path.exists(FILE_NAME):
    df = pd.read_csv(FILE_NAME)
    total_in_all = df['ລາຍຮັບທັງໝົດ'].sum() if not df.empty else 0
    total_ex_all = df['ລາຍຈ່າຍທັງໝົດ'].sum() if not df.empty else 0
else:
    total_in_all, total_ex_all = 0, 0

col_m1, col_m2, col_m3 = st.columns(3)
col_m1.metric("💰 ລາຍຮັບສະສົມ", f"{total_in_all:,.0f} ກີບ")
col_m2.metric("💸 ລາຍຈ່າຍສະສົມ", f"{total_ex_all:,.0f} ກີບ")
col_m3.metric("📈 ເຫຼືອເງິນສົດ", f"{(total_in_all - total_ex_all):,.0f} ກີບ")

# --- 2. ສ່ວນຊ່ອງປ້ອນຂໍ້ມູນ (ພາສາລາວຄົບຖ້ວນ) ---
st.write("---")
st.subheader("📝 ປ້ອນລາຍລະອຽດມື້ນີ້")
c1, c2 = st.columns(2)

with c1:
    st.success("🟢 ພາກສ່ວນ ລາຍຮັບ")
    i1 = st.number_input("1. ເງິນເດືອນ/ລາຍໄດ້ຫຼັກ", value=0, step=1000)
    i2 = st.number_input("2. ລາຍໄດ້ຈາກ YouTube/FB", value=0, step=1000)
    i3 = st.number_input("3. ຂາຍເຄື່ອງຍ່ອຍ", value=0, step=1000)
    i4 = st.number_input("4. ວຽກຫຍິບຜ້າ", value=0, step=1000)
    i5 = st.number_input("5. ເງິນຈາກຕູ້ກົດນ້ຳ", value=0, step=1000)
    i6 = st.number_input("6. ເງິນຈາກຕູ້ຊັກຜ້າ", value=0, step=1000)
    i7 = st.number_input("7. ຄ່າອາຫານ (ຮັບ)", value=0, step=1000)
    i8 = st.number_input("8. ລາຍຮັບອື່ນໆ", value=0, step=1000)

with c2:
    st.error("🔴 ພາກສ່ວນ ລາຍຈ່າຍ")
    e1 = st.number_input("1. ຄ່າກິນ/ອາຫານ", value=0, step=1000)
    e2 = st.number_input("2. ຄ່າເຊົ່າບ້ານ/ສະຖານທີ່", value=0, step=1000)
    e3 = st.number_input("3. ຄ່ານ້ຳ/ຄ່າໄຟ", value=0, step=1000)
    e4 = st.number_input("4. ຄ່ານ້ຳມັນ/ເດີນທາງ", value=0, step=1000)
    e5 = st.number_input("5. ຄ່າຮຽນ/ການສຶກສາ", value=0, step=1000)
    e6 = st.number_input("6. ຄ່າຢາ/ປິ່ນປົວ", value=0, step=1000)
    e7 = st.number_input("7. ຊື້ເຄື່ອງນຸ່ງ/ຂອງໃຊ້", value=0, step=1000)
    e8 = st.number_input("8. ໂທລະສັບ/ເນັດ/ບັນເທີງ", value=0, step=1000)
    e9 = st.number_input("9. ສ່ຽງໂຊກ/ຫວຍ", value=0, step=1000)
    e10 = st.number_input("10. ຄ່າສ້າງ/ສ້ອມເຮືອນ", value=0, step=1000)
    e11 = st.number_input("11. ຕົ້ນທຶນຊື້ເຄື່ອງເຂົ້າຮ້ານ", value=0, step=1000)

# --- 3. ປຸ່ມບັນທຶກ ແລະ ການຈັດການຂໍ້ມູນ ---
if st.button("💾 ບັນທຶກຂໍ້ມູນທັງໝົດ", use_container_width=True):
    t_in = float(i1+i2+i3+i4+i5+i6+i7+i8)
    t_ex = float(e1+e2+e3+e4+e5+e6+e7+e8+e9+e10+e11)
    bal = t_in - t_ex
    
    new_data = {
        'ວັນທີ': datetime.now().strftime("%d/%m/%Y %H:%M"),
        'ລາຍຮັບທັງໝົດ': t_in, 'ລາຍຈ່າຍທັງໝົດ': t_ex, 'ເຫຼືອສຸດທິ': bal,
        'ເງິນເດືອນ': i1, 'ລາຍໄດ້ເນັດ': i2, 'ຂາຍເຄື່ອງ': i3, 'ຫຍິບຜ້າ': i4,
        'ຕູ້ກົດນ້ຳ': i5, 'ຕູ້ຊັກຜ້າ': i6, 'ອາຫານຮັບ': i7, 'ຮັບອື່ນໆ': i8,
        'ຄ່າກິນ': e1, 'ຄ່າເຊົ່າ': e2, 'ນ້ຳໄຟ': e3, 'ເດີນທາງ': e4,
        'ການສຶກສາ': e5, 'ຄ່າຢາ': e6, 'ເຄື່ອງນຸ່ງ': e7, 'ເນັດບັນເທີງ': e8,
        'ຫວຍ': e9, 'ສ້າງເຮືອນ': e10, 'ທຶນຊື້ເຄື່ອງ': e11
    }
    
    df_new = pd.DataFrame([new_data])
    if not os.path.exists(FILE_NAME):
        df_new.to_csv(FILE_NAME, index=False, encoding='utf-8-sig')
    else:
        df_new.to_csv(FILE_NAME, mode='a', index=False, header=False, encoding='utf-8-sig')
    
    st.balloons()
    st.success(f"✅ ບັນທຶກສຳເລັດ! ຮັບ: {t_in:,.0f} | ຈ່າຍ: {t_ex:,.0f} | ເຫຼືອ: {bal:,.0f}")
    st.rerun()

# --- 4. ສະແດງຕາຕະລາງພາສາລາວ (ມີຈຸດຂັ້ນ) ---
st.write("---")
st.subheader("📊 ຕາຕະລາງປະຫວັດການເງິນ (Excel)")
if os.path.exists(FILE_NAME):
    df_display = pd.read_csv(FILE_NAME)
    if not df_display.empty:
        # ໃສ່ຈຸດຂັ້ນໃຫ້ທຸກຖັນທີ່ເປັນຕົວເລກ
        st.dataframe(df_display.style.format(thousands=",", precision=0), use_container_width=True)

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
