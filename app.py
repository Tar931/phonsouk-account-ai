import streamlit as st
import pandas as pd
import os
from datetime import datetime

# --- 1. ຕັ້ງຄ່າໜ້າຈໍ ---
st.set_page_config(page_title="Phonsouk Super Smart AI", page_icon="💰", layout="wide")
FILE_NAME = 'phonsouk_final_database_v3.csv'

# Style ຕົບແຕ່ງ (ປັບໃຫ້ກ່ອງຕົວເລກເຫັນແຈ້ງຂຶ້ນ)
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
    .stNumberInput input { font-size: 20px !important; }
    </style>
    <div style="background-color:#1B4F72; padding:20px; border-radius:15px; text-align:center; color:white; margin-bottom:25px;">
        <h1 style="margin:0;">🏦 ລະບົບ AI ທີ່ປຶກສາການເງິນສະຫຼາດສຸດ (ປ້າພອນສຸກ)</h1>
    </div>
    """, unsafe_allow_html=True)

import streamlit as st

# --- 1. ສູດລັບເຮັດໃຫ້ຕົວເລກມີຈຸດ (Format Function) ---
def format_money(value):
    if not value: return "0"
    # ລຶບຈຸດ ແລະ ຕົວອັກສອນທີ່ບໍ່ແມ່ນເລກອອກກ່ອນ
    clean = "".join(filter(str.isdigit, str(value)))
    if clean == "": return "0"
    # ແປງເປັນຕົວເລກແລ້ວໃສ່ຈຸດຄືນ
    return "{:,}".format(int(clean))

st.set_page_config(page_title="ບັນຊີຂອງປ້າ - ມີຈຸດ", layout="wide")

st.write("# 💰 ລະບົບປ້ອນເລກແບບມີຈຸດ (Real-time)")
st.info("💡 ເຄັດລັບ: ພິມຕົວເລກແລ້ວກົດ Enter ຫຼື ກົດບ່ອນວ່າງ ຕົວເລກຈະມີຈຸດຂຶ້ນມາທັນທີ!")

with st.form("account_form"):
    col1, col2 = st.columns(2)
    
    with col1:
        st.success("### 🟢 ສ່ວນລາຍຮັບ")
        # ໃຊ້ text_input ເພື່ອໃຫ້ພິມຈຸດໄດ້
        i1 = st.text_input("1. ເງິນເດືອນ", value="0")
        i1 = format_money(i1) # ສັ່ງໃຫ້ມັນໃສ່ຈຸດ
        
        i2 = st.text_input("2. ລາຍຮັບ Creator (FB/YouTube)", value="0")
        i2 = format_money(i2)
        
        i3 = st.text_input("3. ຂາຍຂອງຍ່ອຍ", value="0")
        i3 = format_money(i3)
        
        i4 = st.text_input("4. ຮັບຕັດຫຍິບ", value="0")
        i4 = format_money(i4)
        
        i5 = st.text_input("5. ຕູ້ກົດນ້ຳ", value="0")
        i5 = format_money(i5)
        
        i6 = st.text_input("6. ຕູ້ຊັກຜ້າ", value="0")
        i6 = format_money(i6)

    with col2:
        st.error("### 🔴 ສ່ວນລາຍຈ່າຍ")
        e1 = st.text_input("1. ຄ່າອາຫານ & ເຄື່ອງບໍລິໂພກ", value="0")
        e1 = format_money(e1)
        
        e2 = st.text_input("2. ຄ່າເຊົ່າທີ່ຢູ່", value="0")
        e2 = format_money(e2)
        
        e3 = st.text_input("3. ຄ່ານ້ຳ-ຄ່າໄຟ-ເນັດ", value="0")
        e3 = format_money(e3)
        
        e4 = st.text_input("4. ຄ່າເດີນທາງ", value="0")
        e4 = format_money(e4)
        
        e5 = st.text_input("5. ຄ່າການສຶກສາ", value="0")
        e5 = format_money(e5)
        
        e6 = st.text_input("6. ຄ່າປິ່ນປົວ", value="0")
        e6 = format_money(e6)
        
        e7 = st.text_input("7. ຄ່າເສື້ອຜ້າ & ຂອງໃຊ້", value="0")
        e7 = format_money(e7)
        
        e8 = st.text_input("8. ຄ່າໂທລະສັບ & ບັນເທີງ", value="0")
        e8 = format_money(e8)
        
        e9 = st.text_input("9. ຄ່າຫວຍ/ລາງວັນ", value="0")
        e9 = format_money(e9)
        
        e10 = st.text_input("10. ຄ່າສ້າງເຮືອນ", value="0")
        e10 = format_money(e10)

    # ປຸ່ມບັນທຶກ
    submit = st.form_submit_button("💾 ບັນທຶກຂໍ້ມູນທັງໝົດ", use_container_width=True)

if submit:
    st.balloons()
    st.success("✅ ບັນທຶກຂໍ້ມູນຮຽບຮ້ອຍແລ້ວ!")

# 3. ສ່ວນການຈັດການຂໍ້ມູນຫຼັງກົດປຸ່ມ
if submit:
    total_income = i1 + i2 + i3 + i4 + i5 + i6
    total_expense = e1 + e2 + e3 + e4 + e5 + e6 + e7 + e8 + e9 + e10
    balance = total_income - total_expense
    
    st.success("✅ ບັນທຶກສຳເລັດແລ້ວ!")
    st.metric("ລາຍຮັບທັງໝົດ", f"{total_income:,.0f} ກີບ")
    st.metric("ລາຍຈ່າຍທັງໝົດ", f"{total_expense:,.0f} ກີບ")
    st.metric("ເງິນຄົງເຫຼືອ", f"{balance:,.0f} ກີບ")

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