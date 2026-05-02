import streamlit as st
import pandas as pd
import os
from datetime import datetime

# --- 1. ຕັ້ງຄ່າເວັບໄຊ ---
st.set_page_config(page_title="Phonsouk Super AI", page_icon="🤖", layout="wide")
FILE_NAME = 'phonsouk_final_database_v2.csv'

st.markdown("""
    <style>
    .money-box { background-color: #002B36; color: #00FFAA; padding: 10px; border-radius: 8px; font-size: 24px; font-weight: bold; text-align: right; border: 2px solid #268BD2; margin-bottom: 15px; }
    .ai-report { background-color: #F0F2F6; padding: 20px; border-radius: 15px; border-left: 10px solid #268BD2; }
    </style>
    <div style="background-color:#1B4F72; padding:20px; border-radius:15px; text-align:center; color:white;">
        <h1>🤖 AI ອັດສະລິຍະ ວາງແຜນການເງິນ ປ້າພອນສຸກ</h1>
        <p>ວິເຄາະລາຍວັນ, ລາຍອາທິດ, ລາຍເດືອນ, ແລະ ລາຍປີ ແບບມືອາຊີບ</p>
    </div>
    """, unsafe_allow_html=True)

def display_money(val):
    st.markdown(f'<div class="money-box">{val:,.0f} ກີບ</div>', unsafe_allow_html=True)

# --- 2. ສ່ວນປ້ອນຂໍ້ມູນ ---
st.write("### 📝 ບັນທຶກລາຍຮັບ-ລາຍຈ່າຍມື້ນີ້")
with st.form("ultimate_form"):
    c1, c2 = st.columns(2)
    with c1:
        st.info("🟢 ລາຍຮັບ (6 ຊ່ອງທາງ)")
        i1 = st.number_input("ເງິນເດືອນ", min_value=0, step=50000); display_money(i1)
        i2 = st.number_input("ລາຍຮັບ Creator", min_value=0, step=10000); display_money(i2)
        i3 = st.number_input("ຂາຍຂອງຍ່ອຍ", min_value=0, step=5000); display_money(i3)
        i4 = st.number_input("ວຽກຕັດຫຍິບ", min_value=0, step=5000); display_money(i4)
        i5 = st.number_input("ຕູ້ກົດນ້ຳ", min_value=0, step=2000); display_money(i5)
        i6 = st.number_input("ຕູ້ຊັກຜ້າ", min_value=0, step=5000); display_money(i6)
    with c2:
        st.warning("🔴 ລາຍຈ່າຍ (10 ຢ່າງ)")
        e1 = st.number_input("ຄ່າອາຫານ/ເຄື່ອງໃຊ້", min_value=0, step=5000); display_money(e1)
        e2 = st.number_input("ຄ່າເຊົ່າທີ່ຢູ່", min_value=0, step=100000); display_money(e2)
        e3 = st.number_input("ໄຟຟ້າ-ນໍ້າ-ເນັດ", min_value=0, step=5000); display_money(e3)
        e4 = st.number_input("ນ້ຳມັນ/ລົດຈ້າງ", min_value=0, step=5000); display_money(e4)
        e5 = st.number_input("ຄ່າຮຽນລູກ", min_value=0, step=50000); display_money(e5)
        e6 = st.number_input("ຄ່າຢາ/ປິ່ນປົວ", min_value=0, step=5000); display_money(e6)
        e7 = st.number_input("ເສື້ອຜ້າ/ສ່ວນຕົວ", min_value=0, step=5000); display_money(e7)
        e8 = st.number_input("ໂທລະສັບ/ບັນເທີງ", min_value=0, step=5000); display_money(e8)
        e9 = st.number_input("ຜ່ອນໜີ້/ລົດ", min_value=0, step=50000); display_money(e9)
        e10 = st.number_input("ຊື້ເຄື່ອງເຂົ້າຮ້ານ", min_value=0, step=10000); display_money(e10)
    
    submit = st.form_submit_button("🚀 ບັນທຶກ ແລະ ໃຫ້ AI ວິເຄາະທັງໝົດ", use_container_width=True)

if submit:
    now = datetime.now()
    total_in = i1+i2+i3+i4+i5+i6
    total_ex = e1+e2+e3+e4+e5+e6+e7+e8+e9+e10
    new_entry = {
        'Date': now.strftime("%Y-%m-%d"), 'Week': now.isocalendar()[1], 'Month': now.strftime("%m-%Y"), 'Year': str(now.year),
        'Income': total_in, 'Expense': total_ex, 'Profit': total_in - total_ex,
        'Food': e1, 'Rent': e2, 'Bills': e3, 'Debt': e9, 'Sewing': i4, 'Creator': i2
    }
    pd.DataFrame([new_entry]).to_csv(FILE_NAME, mode='a', index=False, header=not os.path.exists(FILE_NAME))
    st.balloons(); st.rerun()

# --- 3. ສ່ວນ AI ວິເຄາະລາຍວັນ-ທິດ-ເດືອນ-ປີ ---
if os.path.exists(FILE_NAME):
    df = pd.read_csv(FILE_NAME)
    st.markdown("---")
    st.header("🧠 ສູນວິເຄາະ AI ອັດສະລິຍະ")
    
    period = st.radio("ເລືອກໄລຍະເວລາທີ່ຕ້ອງການໃຫ້ AI ລາຍງານ:", ["ມື້ນີ້", "ລາຍອາທິດ", "ລາຍເດືອນ", "ລາຍປີ"], horizontal=True)
    
    now = datetime.now()
    if period == "ມື້ນີ້": data = df[df['Date'] == now.strftime("%Y-%m-%d")]; t = "ມື້ນີ້"
    elif period == "ລາຍອາທິດ": data = df[df['Week'] == now.isocalendar()[1]]; t = "ອາທິດນີ້"
    elif period == "ລາຍເດືອນ": data = df[df['Month'] == now.strftime("%m-%Y")]; t = "ເດືອນນີ້"
    else: data = df[df['Year'] == str(now.year)]; t = f"ປີ {now.year}"

    if not data.empty:
        c1, c2, c3 = st.columns(3)
        in_sum, ex_sum = data['Income'].sum(), data['Expense'].sum()
        c1.metric(f"ລາຍຮັບ {t}", "{:,.0f} ກີບ".format(in_sum))
        c2.metric(f"ລາຍຈ່າຍ {t}", "{:,.0f} ກີບ".format(ex_sum))
        c3.metric(f"ກຳໄລ {t}", "{:,.0f} ກີບ".format(in_sum - ex_sum))

        st.markdown(f'<div class="ai-report"><h3>💡 AI ວາງແຜນ ແລະ ແນະນຳສຳລັບ {t}:</h3>', unsafe_allow_html=True)
        
        # ວິເຄາະຊ່ອງທາງປະຢັດ
        food_val, bills_val = data['Food'].sum(), data['Bills'].sum()
        if food_val > (in_sum * 0.3):
            st.write(f"⚠️ **ຊ່ອງທາງປະຢັດ:** ປ້າຈ່າຍຄ່າອາຫານສູງ ({food_val:,.0f} ກີບ). ລອງປະຢັດບ່ອນນີ້ເພື່ອເພີ່ມເງິນເກັບເດີ້.")
        if bills_val > 500000:
            st.write(f"⚠️ **ຊ່ອງທາງປະຢັດ:** ຄ່າໄຟ-ນໍ້າ ສູງເກີນໄປ! ກວດເບິ່ງເຄື່ອງໃຊ້ໄຟຟ້າໃນຮ້ານຄືນໃໝ່.")

        # ວາງແຜນອາຊີບ
        sewing_val, creator_val = data['Sewing'].sum(), data['Creator'].sum()
        st.write(f"🚀 **ແຜນອາຊີບ:** {t} ປ້າມີລາຍໄດ້ຈາກຕັດຫຍິບ {sewing_val:,.0f} ກີບ ແລະ Creator {creator_val:,.0f} ກີບ.")
        if sewing_val > creator_val:
            st.write("✨ AI ແນະນຳ: ວຽກຫຍິບຜ້າມາແຮງ! ປ້າຄວນຖ່າຍຄລິບຕອນຫຍິບລົງເປັນ Creator ພ້ອມກັນເພື່ອເພີ່ມຍອດຂາຍ.")
        else:
            st.write("✨ AI ແນະນຳ: ວຽກ Creator ໄປໄດ້ດີ! ປ້າລອງໂຄສະນາຮັບງານຕັດຫຍິບຜ່ານຄລິບຕື່ມອີກເດີ້.")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with st.expander("📜 ເບິ່ງປະຫວັດການບັນທຶກ (ມີຈຸດຄັ່ນ)"):
        st.dataframe(df.sort_values(by='Date', ascending=False), use_container_width=True)