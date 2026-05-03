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

# --- ສ່ວນ AI Advisor ເວີຊັນສະຫຼາດ ແລະ ປອດໄພ (Daily/Weekly/Monthly/Yearly) ---
st.divider()
st.write("### 🧠 AI ສູນວິເຄາະ ແລະ ວາງແຜນທຸລະກິດອັດສະລິຍະ")

if os.path.exists(FILE_NAME):
    try:
        df = pd.read_csv(FILE_NAME)
        # ກວດສອບວ່າຖັນຂໍ້ມູນຄົບຫຼືບໍ່ ກ່ອນຈະຄິດໄລ່
        cols = df.columns.tolist()
        if not df.empty and 'ລາຍຮັບ' in cols and 'ລາຍຈ່າຍ' in cols:
            # ແປງວັນທີໃຫ້ລະບົບອ່ານໄດ້
            df['ວັນທີ'] = pd.to_datetime(df['ວັນທີ'], dayfirst=True, errors='coerce')
            
            # ຄິດໄລ່ຄ່າຕ່າງໆ
            total_in = pd.to_numeric(df['ລາຍຮັບ'], errors='coerce').sum()
            total_ex = pd.to_numeric(df['ລາຍຈ່າຍ'], errors='coerce').sum()
            net_profit = total_in - total_ex
            
            t1, t2, t3, t4 = st.tabs(["📅 ວິເຄາະໄລຍະເວລາ", "💰 ວາງແຜນການເງິນ", "📢 ການຕະຫຼາດ", "🛠 ການບໍລິຫານ"])
            
            with t1:
                st.info("#### 📊 ສະຫຼຸບຜົນການດຳເນີນງານ")
                c1, c2 = st.columns(2)
                c1.metric("ລາຍຮັບລວມທັງໝົດ", f"{total_in:,.0f} ₭")
                c2.metric("ກຳໄລສຸດທິ", f"{net_profit:,.0f} ₭")
                
                # ວິເຄາະລາຍເດືອນເບື້ອງຕົ້ນ
                avg_monthly = total_in / (len(df['ວັນທີ'].dt.month.unique()) if len(df) > 0 else 1)
                st.write(f"📈 **ຄາດການ:** ລາຍຮັບສະເລ່ຍຕໍ່ເດືອນຂອງປ້າແມ່ນ: **{avg_monthly:,.0f} ₭**")

            with t2:
                st.success("#### 💵 ກົນຍຸດການເງິນ")
                st.write(f"💡 **ແຜນອອມ:** ປ້າຄວນແບ່ງເກັບ 20% ເປັນເງິນ {total_in * 0.2:,.0f} ₭ ໄວ້ຂະຫຍາຍທຸລະກິດ.")
                if total_ex > total_in:
                    st.error("⚠️ ເຕືອນ: ລາຍຈ່າຍເກີນລາຍຮັບ! ຄວນກວດສອບຕົ້ນທຶນດ່ວນ.")

            with t3:
                st.warning("#### 📣 ການຕະຫຼາດ & ການຂາຍ")
                st.write("🎯 **ແຜນການ:** ເນັ້ນການເຮັດ Content 'ວຽກຝີມືປ້າພອນສຸກ' ລົງ Facebook Reels ທຸກໆມື້.")
                st.write("🎁 **ໂປຣ:** ເຮັດບັດສະສົມແຕ້ມ 10 ແຖມ 1 ສຳລັບລູກຄ້າທີ່ມາຮ້ານປະຈຳ.")

            with t4:
                st.error("#### ⚙️ ການບໍລິຫານ (Management)")
                st.write("⏳ **ບໍລິຫານເວລາ:** ແບ່ງເວລາ 15 ນາທີກ່ອນປິດຮ້ານ ເພື່ອສະຫຼຸບບັນຊີທຸກມື້.")
                st.write("🌟 **ການບໍລິການ:** ເນັ້ນຄວາມຈິງໃຈ ແລະ ແນະນຳສິນຄ້າທີ່ເໝາະກັບລູກຄ້າແທ້ໆ.")
        else:
            st.warning("⚠️ ຍັງຫາຂໍ້ມູນ 'ລາຍຮັບ' ບໍ່ເຫັນ. ກະລຸນາລອງ 'ບັນທຶກຂໍ້ມູນ' ໃໝ່ 1 ລາຍການກ່ອນເດີ້ເຈົ້າປ້າ.")
    except Exception as e:
        st.error("ພົບຂໍ້ຜິດພາດໃນການອ່ານຂໍ້ມູນ. ແນະນຳໃຫ້ລຶບໄຟລ໌ CSV ເກົ່າອອກ ແລ້ວເລີ່ມບັນທຶກໃໝ່.")
else:
    st.info("ຍັງບໍ່ມີຂໍ້ມູນໃນລະບົບ. ປ້າມີແຜນຈະຂາຍຫຍັງມື້ນີ້ ປ້ອນຂໍ້ມູນໄດ້ເລີຍ!")
 
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
