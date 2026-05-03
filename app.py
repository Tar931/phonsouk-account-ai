import streamlit as st
import pandas as pd
import os
from datetime import datetime, timedelta

st.set_page_config(page_title="App ບັນຊີຂອງປ້າ", layout="wide")
FILE_NAME = 'phonsouk_final_database_v3.csv'

st.markdown("""
<style>
    [data-testid="stMetricValue"] {
        color: #1B4F72 !important; 
        font-size: 35px !important;
        font-weight: bold !important;
    }
    [data-testid="stMetricLabel"] {
        color: #566573 !important;
        font-size: 18px !important;
    }
    div[data-testid="stMetric"] {
        background-color: #FFFFFF !important; 
        border: 2px solid #1B4F72 !important;
        padding: 15px !important;
        border-radius: 10px !important;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
    }
    .ai-card {
        background-color: #EBF5FB !important; 
        padding: 20px;
        border-left: 10px solid #1B4F72;
        border-radius: 10px;
        color: #1B4F72 !important;
        margin: 20px 0;
    }
    .ai-card h3, .ai-card p, .ai-card b {
        color: #1B4F72 !important;
    }

    /* ເຊື່ອງລູກສອນຂຶ້ນລົງຂອງ number_input */
    input[type=number]::-webkit-inner-spin-button,
    input[type=number]::-webkit-outer-spin-button {
        -webkit-appearance: none;
        margin: 0;
    }
    input[type=number] { -moz-appearance: textfield; }

    /* ຕົວເລກຢູ່ໃນ input ໃຫ້ໃຫຍ່ຂຶ້ນ */
    input[type=number] {
        font-size: 18px !important;
        font-weight: bold !important;
        color: #1B4F72 !important;
    }
</style>
""", unsafe_allow_html=True)

st.write("""
<div style="background-color: #1B4F72; padding: 25px; border-radius: 15px; border: 3px solid #F1C40F; text-align: center; color: white;">
    <h1 style="margin: 0;">🌸 ລະບົບບັນຊີ AI ປ້າພອນສຸກ </h1>
    <p style="margin: 10px 0;">ເບີໂທ: 020 99858310 | Line: Tarvan</p>
    <p style="margin: 0;">Facebook: ນາງພອນສຸກ ພັນທະຜອງ</p>
    <div style="font-size: 30px; margin-top: 10px;">🌸 🇱🇦 🌸</div>
</div>
<br>
""", unsafe_allow_html=True)

# --- ກຽມ session_state reset ---
ALL_KEYS = ["i1","i2","i3","i4","i5","i6","i7",
            "e1","e2","e3","e4","e5","e6","e7","e8","e9","e10","e11"]

if 'reset_counter' not in st.session_state:
    st.session_state['reset_counter'] = 0

# ✅ ໃຊ້ number_input ແທນ text_input
# - format="%d" → ສະແດງເປັນເລກເຕັມ, ບໍ່ມີທົດສະນິຍົມ
# - min_value=0 → ບໍ່ຕິດລົບ
# - step=1000 → ກົດລູກສອນເພີ່ມ/ຫຼຸດໄດ້ທີລະ 1,000
# - value=0 → ຄ່າເລີ່ມຕົ້ນ 0
# Streamlit's number_input ຈະ format ຈຸດ (,) ໃຫ້ອັດຕະໂນມັດ!

def num_input(label, key):
    rc = st.session_state['reset_counter']
    widget_key = f"n_{key}_{rc}"
    val = st.number_input(
        label,
        min_value=0,
        value=0,
        step=1000,
        format="%d",
        key=widget_key
    )
    return val

# --- 1. ສ່ວນປ້ອນຂໍ້ມູນ ---
c1, c2 = st.columns(2)
with c1:
    st.success("### 🟢 ສ່ວນລາຍຮັບ (ກີບ)")
    i1_v = num_input("1. ຮັບເງິນເດືອນ", "i1")
    i2_v = num_input("2. ລາຍຮັບ Creator (FB/YouTube)", "i2")
    i3_v = num_input("3. ລາຍຮັບຂາຍຂອງຍ່ອຍ", "i3")
    i4_v = num_input("4. ລາຍຮັບຕັດຫຍິບ", "i4")
    i5_v = num_input("5. ລາຍຮັບຕູ້ກົດນ້ຳ", "i5")
    i6_v = num_input("6. ລາຍຮັບຕູ້ຊັກຜ້າ", "i6")
    i7_v = num_input("7. ລາຍຮັບອື່ນໆ", "i7")

with c2:
    st.error("### 🔴 ສ່ວນລາຍຈ່າຍ (ກີບ)")
    e1_v = num_input("1. ຄ່າອາຫານ & ເຄື່ອງບໍລິໂພກ", "e1")
    e2_v = num_input("2. ຄ່າເຊົ່າທີ່ຢູ່", "e2")
    e3_v = num_input("3. ຄ່ານ້ຳ-ຄ່າໄຟ-ເນັດ", "e3")
    e4_v = num_input("4. ຄ່າເດີນທາງ", "e4")
    e5_v = num_input("5. ຄ່າການສຶກສາ", "e5")
    e6_v = num_input("6. ຄ່າປິ່ນປົວ", "e6")
    e7_v = num_input("7. ຄ່າເສື້ອຜ້າ & ຂອງໃຊ້", "e7")
    e8_v = num_input("8. ຄ່າໂທລະສັບ & ບັນເທີງ", "e8")
    e9_v = num_input("9. ຄ່າຫວຍ/ລາງວັນ", "e9")
    e10_v = num_input("10. ຄ່າສ້າງເຮືອນ", "e10")
    e11_v = num_input("11. ຄ່າຊື້ສິນຄ້າເຂົ້າຮ້ານ", "e11")

# ສະແດງຜົນລວມກ່ອນກົດບັນທຶກ
t_in_preview  = i1_v+i2_v+i3_v+i4_v+i5_v+i6_v+i7_v
t_ex_preview  = e1_v+e2_v+e3_v+e4_v+e5_v+e6_v+e7_v+e8_v+e9_v+e10_v+e11_v
profit_preview = t_in_preview - t_ex_preview

pc1, pc2, pc3 = st.columns(3)
pc1.metric("💰 ລາຍຮັບລວມ (preview)", f"{t_in_preview:,} ກີບ")
pc2.metric("💸 ລາຍຈ່າຍລວມ (preview)", f"{t_ex_preview:,} ກີບ")
pc3.metric("📊 ກຳໄລ (preview)", f"{profit_preview:,} ກີບ")

submit = st.button("💾 ບັນທຶກຂໍ້ມູນທັງໝົດ", use_container_width=True)

# --- 2. ບັນທຶກຂໍ້ມູນ ---
if submit:
    now_lao = datetime.now() + timedelta(hours=7)

    v_i = [i1_v, i2_v, i3_v, i4_v, i5_v, i6_v, i7_v]
    v_e = [e1_v, e2_v, e3_v, e4_v, e5_v, e6_v, e7_v, e8_v, e9_v, e10_v, e11_v]
    t_in = sum(v_i)
    t_ex = sum(v_e)

    new_data = {
        'ວັນທີ': now_lao.strftime("%d/%m/%Y %H:%M"),
        'ລາຍຮັບລວມ': t_in, 'ລາຍຈ່າຍລວມ': t_ex, 'ເຫຼືອເກັບ': t_in - t_ex,
        'ເງິນເດືອນ': v_i[0], 'Creator': v_i[1], 'ຂາຍຂອງ': v_i[2], 'ຫຍິບຜ້າ': v_i[3],
        'ຕູ້ກົດນ້ຳ': v_i[4], 'ຕູ້ຊັກຜ້າ': v_i[5], 'ຮັບອື່ນໆ': v_i[6],
        'ອາຫານ': v_e[0], 'ຄ່າເຊົ່າ': v_e[1], 'ນ້ຳໄຟ': v_e[2], 'ເດີນທາງ': v_e[3],
        'ການສຶກສາ': v_e[4], 'ຢາ': v_e[5], 'ເສື້ອຜ້າ': v_e[6], 'ບັນເທີງ': v_e[7],
        'ຫວຍ': v_e[8], 'ສ້າງເຮືອນ': v_e[9], 'ຊື້ຂອງເຂົ້າຮ້ານ': v_e[10]
    }

    pd.DataFrame([new_data]).to_csv(
        FILE_NAME, mode='a', index=False,
        header=not os.path.exists(FILE_NAME), encoding='utf-8-sig'
    )

    # ✅ ລ້າງໂດຍເພີ່ມ reset_counter → widget ທັງໝົດ reset ກັບ 0
    st.session_state['reset_counter'] += 1
    st.success(f"✅ ບັນທຶກແລ້ວ! ເວລາລາວ: {now_lao.strftime('%H:%M')}")
    st.rerun()

# --- 3. ສ່ວນສະແດງຜົນ ---
if os.path.exists(FILE_NAME):
    df = pd.read_csv(FILE_NAME)
    st.markdown("---")

    st.subheader("📊 ເລືອກໄລຍະເວລາທີ່ປ້າຢາກໃຫ້ AI ວິເຄາະ")
    option = st.radio("ເບິ່ງລາຍງານ:", ["ມື້ນີ້", "ອາທິດນີ້", "ເດືອນນີ້", "ປີນີ້"], horizontal=True)

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

    if not filtered_df.empty:
        t_in  = filtered_df['ລາຍຮັບລວມ'].sum()
        t_ex  = filtered_df['ລາຍຈ່າຍລວມ'].sum()
        profit = t_in - t_ex

        c1, c2, c3 = st.columns(3)
        c1.metric(f"ລາຍຮັບ {text_time}", f"{t_in:,.0f} ກີບ")
        c2.metric(f"ລາຍຈ່າຍ {text_time}", f"{t_ex:,.0f} ກີບ")
        c3.metric(f"ກຳໄລ {text_time}", f"{profit:,.0f} ກີບ")

        st.markdown(f"""
        <div class="ai-card">
            <h3>🤖 AI Professional Advisor ({text_time})</h3>
            <p>✅ <b>ສະຫຼຸບການເງິນ:</b> {text_time} ປ້າມີກຳໄລສຸດທິ <b>{profit:,.0f} ກີບ</b>.</p>
            <p>📈 <b>ວິເຄາະຊ່ອງທາງລາຍໄດ້:</b> ລາຍຮັບຈາກການຫຍິບຜ້າ ແລະ ຕູ້ຢອດຫຼຽນເປັນລາຍໄດ້ທີ່ໝັ້ນຄົງທີ່ສຸດ.</p>
            <p>⚠️ <b>ຂໍ້ຄວນລະວັງ:</b> ຖ້າລາຍຈ່າຍຄ່າຫວຍ ຫຼື ຄ່າບັນເທີງສູງເກີນ 10% ຂອງລາຍຮັບ, AI ແນະນຳໃຫ້ປ້າປັບຫຼຸດລົງ.</p>
            <p>🚀 <b>ຄຳແນະນຳ:</b> ແບ່ງກຳໄລ 5% ໄປບຳລຸງຮັກສາຕູ້ຊັກຜ້າ ແລະ ຕູ້ກົດນ້ຳ ເພື່ອໃຫ້ສ້າງລາຍໄດ້ໄດ້ຍາວໆ.</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.info(f"ຍັງບໍ່ມີຂໍ້ມູນ {text_time} ເດີ້ປ້າ!")

    st.markdown("---")
    st.write("### 📅 ປະຫວັດການເງິນ (10 ລາຍການຫຼ້າສຸດ)")
    st.dataframe(
        df.tail(10).style.format(
            subset=['ລາຍຮັບລວມ', 'ລາຍຈ່າຍລວມ', 'ເຫຼືອເກັບ'],
            formatter="{:,.0f}"
        ),
        use_container_width=True
    )

    with st.expander("🛠️ ລ້າງຂໍ້ມູນທັງໝົດ"):
        st.warning("ຄຳເຕືອນ: ການລົບຂໍ້ມູນຈະບໍ່ສາມາດກູ້ຄືນໄດ້!")
        pwd = st.text_input("ໃສ່ລະຫັດ 9999 ເພື່ອລົບ:", type="password")
        if st.button("🗑️ ຢືນຢັນລົບ"):
            if pwd == "9999":
                if os.path.exists(FILE_NAME):
                    os.remove(FILE_NAME)
                    st.success("ລົບຂໍ້ມູນຮຽບຮ້ອຍແລ້ວ!")
                    st.rerun()
            else:
                st.error("ລະຫັດບໍ່ຖືກ!")
