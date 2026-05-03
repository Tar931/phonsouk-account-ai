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

# --- ສ່ວນ AI Advisor (ເວີຊັນປັບປຸງໃໝ່: ປ້ອງກັນ Error) ---
st.divider()
st.write("### 🧠 AI ອັດສະລິຍະ: ວິເຄາະ & ວາງແຜນທຸລະກິດ")

if os.path.exists(FILE_NAME):
    try:
        df = pd.read_csv(FILE_NAME)
        # ກວດສອບວ່າໄຟລ໌ມີຂໍ້ມູນ ແລະ ມີຖັນທີ່ຕ້ອງການຫຼືບໍ່
        required_cols = ['ລາຍຮັບ', 'ລາຍຈ່າຍ', 'ເຫຼືອ']
        if not df.empty and all(col in df.columns for col in required_cols):
            
            # ຄິດໄລ່ຄ່າສະເລ່ຍ
            avg_income = pd.to_numeric(df['ລາຍຮັບ']).mean()
            avg_expense = pd.to_numeric(df['ລາຍຈ່າຍ']).mean()
            
            tab1, tab2, tab3 = st.tabs(["💰 ການເງິນ", "📈 ການຕະຫຼາດ", "🏢 ການບໍລິຫານ"])
            
            with tab1:
                st.info("#### ວິເຄາະການເງິນ")
                if avg_income > avg_expense:
                    st.write("✅ **ສະພາບຄ່ອງ:** ດີຫຼາຍ! ປ້າມີລາຍຮັບສະເລ່ຍສູງກວ່າລາຍຈ່າຍ.")
                    st.write(f"💡 **ແນະນຳ:** ຄວນແບ່ງເງິນ {avg_income * 0.2:,.0f} ກີບ (20%) ໄປຝາກປະຈຳ.")
                else:
                    st.warning("⚠️ **ຂໍ້ຄວນລະວັງ:** ລາຍຈ່າຍສະເລ່ຍສູງ! ໃຫ້ກວດສອບຕົ້ນທຶນຄືນໃໝ່.")

            with tab2:
                st.info("#### ວາງແຜນການຕະຫຼາດ")
                st.write("💡 **ກົນຍຸດ:** ປ້າຄວນໂພສວິດີໂອ 'ເບື້ອງຫຼັງການເຮັດວຽກ' ລົງ TikTok ຫຼື Facebook ມື້ລະ 1 ຄລິບ.")
                st.write("🚀 **ໂປຣໂມຊັນ:** ແນະນຳໃຫ້ເຮັດ 'ບັດສະສົມແຕ້ມ' ສຳລັບລູກຄ້າທີ່ມາໃຊ້ບໍລິການປະຈຳ.")

            with tab3:
                st.info("#### ການບໍລິຫານຈັດການ")
                st.write("⏳ **ການຈັດສັນເວລາ:** ແບ່ງເວລາ 1 ຊົ່ວໂມງຕໍ່ມື້ ເພື່ອກວດສອບສະຕັອກສິນຄ້າ.")
                st.write("📝 **ແຜນງານ:** ຄວນໃຊ້ AI ຊ່ວຍສະຫຼຸບບັນຊີທຸກໆທ້າຍອາທິດ.")
        else:
            st.warning("⚠️ ຍັງບໍ່ມີຂໍ້ມູນພຽງພໍໃຫ້ AI ວິເຄາະ. ກະລຸນາລອງ 'ບັນທຶກຂໍ້ມູນ' ໃໝ່ອີກ 1-2 ລາຍການກ່ອນເດີ້ເຈົ້າປ້າ.")
    except Exception as e:
        st.error("ພົບຂໍ້ຜິດພາດໃນການອ່ານຂໍ້ມູນ. ແນະນຳໃຫ້ລຶບໄຟລ໌ CSV ເກົ່າຖິ້ມ ແລ້ວເລີ່ມບັນທຶກໃໝ່.")
else:
    st.info("ຍັງບໍ່ມີຂໍ້ມູນໃຫ້ວິເຄາະໃນເວລານີ້.")
 
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
