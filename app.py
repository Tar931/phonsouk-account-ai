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

# --- 1. ສ່ວນປ້ອນຂໍ້ມູນ ---
c1, c2 = st.columns(2)

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

# --- ສ່ວນບັນທຶກ (Code ທີ່ປ້າໃຫ້ເພີ່ມ) ---
if submit:
    now_lao = datetime.now() + timedelta(hours=7) 
    
    # ແປງຄ່າຈາກຂໍ້ຄວາມທີ່ມີຈຸດ ໃຫ້ເປັນຕົວເລກແທ້ໆ
    v_i = [parse_num(i1_v), parse_num(i2_v), parse_num(i3_v), parse_num(i4_v), parse_num(i5_v), parse_num(i6_v)]
    v_e = [parse_num(e1_v), parse_num(e2_v), parse_num(e3_v), parse_num(e4_v), parse_num(e5_v), parse_num(e6_v), parse_num(e7_v), parse_num(e8_v), parse_num(e9_v), parse_num(e10_v)]
    
    t_in = sum(v_i)
    t_ex = sum(v_e)
    
    new_data = {
        'ວັນທີ': now_lao.strftime("%d/%m/%Y %H:%M"), 
        'ລາຍຮັບລວມ': t_in, 'ລາຍຈ່າຍລວມ': t_ex, 'ເຫຼືອເກັບ': t_in - t_ex,
        'ເງິນເດືອນ': v_i[0], 'Creator': v_i[1], 'ຂາຍຂອງ': v_i[2], 'ຫຍິບຜ້າ': v_i[3], 'ຕູ້້ກົດນ້ຳ': v_i[4], 'ຕູ້ຊັກຜ້າ': v_i[5],
        'ອາຫານ': v_e[0], 'ຄ່າເຊົ່າ': v_e[1], 'ນ້ຳໄຟ': v_e[2], 'ເດີນທາງ': v_e[3], 'ການສຶກສາ': v_e[4], 'ຢາ': v_e[5], 'ເສື້ອຜ້າ': v_e[6], 'ບັນເທີງ': v_e[7], 'ຫວຍ': v_e[8], 'ສ້າງເຮືອນ': v_e[9]
    }
    pd.DataFrame([new_data]).to_csv(FILE_NAME, mode='a', index=False, header=not os.path.exists(FILE_NAME), encoding='utf-8-sig')
    st.success(f"✅ ບັນທຶກແລ້ວ! ເວລາລາວ: {now_lao.strftime('%H:%M')}")
    st.rerun()

# --- ສ່ວນ AI ອັດສະລິຍະ ວິເຄາະຮອບດ້ານ (ວັນ/ທິດ/ເດືອນ/ປີ) ---
st.divider()
st.write("### 🧠 AI ສູນວິເຄາະ ແລະ ວາງແຜນທຸລະກິດອັດສະລິຍະ")

if os.path.exists(FILE_NAME):
    df = pd.read_csv(FILE_NAME)
    if not df.empty:
        # ແປງວັນທີໃຫ້ລະບົບເຂົ້າໃຈ
        df['ວັນທີ'] = pd.to_datetime(df['ວັນທີ'], dayfirst=True)
        
        # 1. ວິເຄາະສະຖິຕິພື້ນຖານ
        total_in = df['ລາຍຮັບ'].sum()
        total_ex = df['ລາຍຈ່າຍ'].sum()
        net_profit = df['ເຫຼືອ'].sum()
        
        # ສ້າງ Tab ສໍາລັບການວາງແຜນ
        t1, t2, t3, t4 = st.tabs(["📅 ວິເຄາະໄລຍະເວລາ", "💰 ວາງແຜນການເງິນ", "📢 ການຕະຫຼາດ", "🛠 ການບໍລິຫານ"])
        
        with t1:
            st.info("#### 📊 ສະຫຼຸບຜົນການດຳເນີນງານ")
            col_a, col_b = st.columns(2)
            # ວິເຄາະລາຍວັນ (ມື້ລ່າສຸດ)
            daily = df.iloc[-1]
            col_a.metric("ມື້ນີ້ (ລາຍຮັບ)", f"{daily['ລາຍຮັບ']:,.0f} ₭")
            
            # ວິເຄາະລາຍເດືອນ (ສະເລ່ຍ)
            monthly_avg = df.resample('M', on='ວັນທີ')['ລາຍຮັບ'].sum().mean()
            col_b.metric("ສະເລ່ຍລາຍຮັບ/ເດືອນ", f"{monthly_avg:,.0f} ₭")
            
            st.write(f"📈 **ພາບລວມລາຍປີ:** ຄາດການລາຍຮັບໝົດປີຈະຢູ່ທີ່: **{monthly_avg * 12:,.0f} ₭**")

        with t2:
            st.success("#### 💵 ກົນຍຸດການເງິນ (Financial Strategy)")
            savings_goal = net_profit * 0.3
            st.write(f"💡 **ແຜນການອອມ:** ປ້າຄວນແບ່ງເງິນເກັບ **30% ({savings_goal:,.0f} ₭)** ໄວ້ເປັນທຶນໝຸນວຽນສຸກເສີນ.")
            if total_ex > (total_in * 0.7):
                st.warning("⚠️ **ເຕືອນ:** ລາຍຈ່າຍສູງກວ່າ 70% ຂອງລາຍຮັບ. ແນະນຳໃຫ້ຫຼຸດຄ່າໃຊ້ຈ່າຍທີ່ບໍ່ຄົງທີ່ລົງ.")
            else:
                st.write("✅ **ສະພາບຄ່ອງ:** ດີຫຼາຍ! ປ້າມີກຳໄລເຫຼືອພຽງພໍສຳລັບການລົງທຶນເພີ່ມ.")

        with t3:
            st.warning("#### 📣 ແຜນການຕະຫຼາດ (Marketing Plan)")
            st.write("📌 **ກົນຍຸດການຂາຍ:** ໃຊ້ຫຼັກການ 'ປາກຕໍ່ປາກ' ບວກກັບການເຮັດ 'Facebook Reels' ສະແດງສິນຄ້າໃໝ່ທຸກໆວັນເສົາ.")
            st.write("🎁 **ໂປຣໂມຊັນ:** ແນະນຳໃຫ້ຈັດກິດຈະກຳ 'Happy Hour' ຫຼຸດລາຄາ 5-10% ໃນຊ່ວງມື້ທີ່ຍອດຂາຍຕ່ຳທີ່ສຸດ.")

        with t4:
            st.error("#### ⚙️ ການບໍລິຫານ & ການບໍລິການ (Management)")
            st.write("👥 **ການບໍລິການ:** ເນັ້ນການບໍລິການແບບ 'ຍິ້ມແຍ້ມແຈ່ມໃສ' ແລະ ມີຂອງຂວັນເລັກໆນ້ອຍໆໃຫ້ລູກຄ້າປະຈຳ.")
            st.write("🏗️ **ໂຄງສ້າງ:** ປ້າຄວນຈັດລຽງສິນຄ້າທີ່ຂາຍດີໄວ້ທາງໜ້າຮ້ານ ເພື່ອດຶງດູດສາຍຕາລູກຄ້າ.")
            
    else:
        st.warning("ກະລຸນາປ້ອນຂໍ້ມູນກ່ອນ ເພື່ອໃຫ້ AI ວິເຄາະ.")
 
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
