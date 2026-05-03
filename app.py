import streamlit as st
import pandas as pd
import os
from datetime import datetime, timedelta

# --- ຫົວຂໍ້ ແລະ ຂໍ້ມູນຕິດຕໍ່ (ແບບປ້ອງກັນການຫຼຸດ 100%) ---
header_html = """
<div style="background-color: #1B4F72; padding: 30px; border-radius: 20px; border: 3px solid #F1C40F; text-align: center; color: white; font-family: 'Arial';">
    <h1 style="margin: 0; font-size: 35px;">🌸 ລະບົບບັນຊີ AI ປ້າພອນສຸກ ₭</h1>
    <p style="font-size: 18px; color: #D5D8DC; margin-top: 10px;">ລະບົບບັນທຶກການເງິນ ແລະ ວິເຄາະດ້ວຍ AI (ເວີຊັນເມືອງລາວ)</p>
    
    <hr style="border: 0.5px solid #F1C40F; width: 80%; margin: 20px auto;">
    
    <div style="background-color: rgba(255, 255, 255, 0.1); padding: 15px; border-radius: 10px; display: inline-block; text-align: left;">
        <h4 style="margin: 0 0 10px 0; color: #F1C40F;">📞 ຂໍ້ມູນຕິດຕໍ່ຜູ້ເດູແລ:</h4>
        <p style="margin: 5px 0; font-size: 18px; color: white;"><b>ເບີໂທ:</b> 020 99858310</p>
        <p style="margin: 5px 0; font-size: 18px; color: white;"><b>Line ID:</b> Tarvan</p>
        <p style="margin: 5px 0; font-size: 18px; color: white;"><b>Facebook:</b> ນາງພອນສຸກ ພັນທະຜອງ</p>
    </div>
    
    <div style="margin-top: 15px;">
        <span style="font-size: 40px;">🌸</span>
        <span style="font-size: 30px; vertical-align: middle; margin: 0 15px;">🇱🇦</span>
        <span style="font-size: 40px;">🌸</span>
    </div>
</div>
<br>
"""
# ສັ່ງໃຫ້ມັນສະແດງຜົນ (ຫ້າມລືມແຖວນີ້ເດີ້ປ້າ)
st.markdown(header_html, unsafe_allow_html=True)

# ຟັງຊັນແປງເປັນຕົວເລກ
def parse_num(v):
    if v == "" or v is None: return 0
    nums = "".join(filter(str.isdigit, str(v)))
    return int(nums) if nums else 0

# --- 1. ສ່ວນປ້ອນຂໍ້ມູນ ---
c1, c2 = st.columns(2)

with c1:
    st.success("### 🟢 ລາຍຮັບ")
    i1 = parse_num(st.text_input("1. ເງິນເດືອນ", key="in1"))
    i2 = parse_num(st.text_input("2. ລາຍຮັບ Creator (FB/YouTube)", key="in2"))
    i3 = parse_num(st.text_input("3. ຂາຍຂອງຍ່ອຍ", key="in3"))
    i4 = parse_num(st.text_input("4. ຮັບຕັດຫຍິບ", key="in4"))
    i5 = parse_num(st.text_input("5. ຕູ້ກົດນ້ຳ", key="in5"))
    i6 = parse_num(st.text_input("6. ຕູ້ຊັກຜ້າ", key="in6"))

with c2:
    st.error("### 🔴 ລາຍຈ່າຍ")
    e1 = parse_num(st.text_input("1. ຄ່າອາຫານ & ເຄື່ອງບໍລິໂພກ", key="ex1"))
    e2 = parse_num(st.text_input("2. ຄ່າເຊົ່າທີ່ຢູ່", key="ex2"))
    e3 = parse_num(st.text_input("3. ຄ່ານ້ຳ-ຄ່າໄຟ-ເນັດ", key="ex3"))
    e4 = parse_num(st.text_input("4. ຄ່າເດີນທາງ", key="ex4"))
    e5 = parse_num(st.text_input("5. ຄ່າການສຶກສາ", key="ex5"))
    e6 = parse_num(st.text_input("6. ຄ່າປິ່ນປົວ", key="ex6"))
    e7 = parse_num(st.text_input("7. ຄ່າເສື້ອຜ້າ & ຂອງໃຊ້", key="ex7"))
    e8 = parse_num(st.text_input("8. ຄ່າໂທລະສັບ & ບັນເທີງ", key="ex8"))
    e9 = parse_num(st.text_input("9. ຄ່າຫວຍ/ລາງວັນ", key="ex9"))
    e10 = parse_num(st.text_input("10. ຄ່າສ້າງເຮືອນ", key="ex10"))

submit = st.button("💾 ບັນທຶກຂໍ້ມູນທັງໝົດ", use_container_width=True)

# --- 2. ສ່ວນບັນທຶກຂໍ້ມູນ (ທີ່ປ້າບອກໃຫ້ເພີ່ມ) ---
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
    pd.DataFrame([new_data]).to_csv(FILE_NAME, mode='a', index=False, header=not os.path.exists(FILE_NAME), encoding='utf-8-sig')
    st.success(f"✅ ບັນທຶກແລ້ວ! ເວລາລາວປັດຈຸບັນ: {now_lao.strftime('%H:%M')}")
    st.rerun()

# --- 3. ສ່ວນ AI ວິເຄາະ ແລະ ສະແດງຜົນ ---
if os.path.exists(FILE_NAME):
    df = pd.read_csv(FILE_NAME)
    st.markdown("---")
    
    # ເລືອກໄລຍະເວລາ
    st.subheader("📊 ເລືອກໄລຍະເວລາທີ່ປ້າຢາກໃຫ້ AI ວິເຄາະ")
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
            <p>⚠️ <b>ຂໍ້ຄວນລະວັງ:</b> ຖ້າລາຍຈ່າຍຄ່າຫວຍ ຫຼື ຄ່າບັນເທີງສູງເກີນ 10% ຂອງລາຍຮັບ, AI ແນະນຳໃຫ້ປ້າປັບຫຼຸດລົງເພື່ອເອົາໄປໃສ່ຄ່າສ້າງເຮືອນແທນ.</p>
            <p>🚀 <b>ຄຳແນະນຳມືອາຊີບ:</b> ໃນໄລຍະ {text_time}, ປ້າຄວນແບ່ງກຳໄລ 5% ໄປບຳລຸງຮັກສາຕູ້ຊັກຜ້າ ແລະ ຕູ້ກົດນ້ຳ ເພື່ອໃຫ້ມັນສ້າງເງິນໃຫ້ປ້າໄດ້ຍາວໆ.</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.info(f"ຍັງບໍ່ມີຂໍ້ມູນ {text_time} ເດີ້ປ້າ!")

    # --- 4. ຕະລາງ Excel ແລະ ປຸ່ມລົບ (Password Lock) ທີ່ປ້າຫາກໍ່ສົ່ງມາໃຫ້ ---
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
