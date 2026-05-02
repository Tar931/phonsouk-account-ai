import streamlit as st
import pandas as pd
import os
from datetime import datetime

# --- 1. ຕັ້ງຄ່າເວັບໄຊ ---
st.set_page_config(page_title="Phonsouk AI Fixed", page_icon="💎", layout="wide")
# ປ່ຽນຊື່ໄຟລ໌ໃໝ່ເພື່ອປ້ອງກັນ Error ຈາກຂໍ້ມູນເກົ່າ
FILE_NAME = 'phonsouk_smart_data_v1.csv'

st.markdown("""
    <style>
    .money-box { background-color: #002B36; color: #00FFAA; padding: 12px; border-radius: 10px; font-size: 26px; font-weight: bold; text-align: right; border: 2px solid #268BD2; margin-bottom: 20px; }
    </style>
    <div style="background-color:#1B4F72; padding:25px; border-radius:15px; text-align:center; margin-bottom:20px;">
        <h1 style="color:white; margin:0;">💎 AI ວາງແຜນການເງິນ ປ້າພອນສຸກ (ເວີຊັນແກ້ໄຂ)</h1>
        <p style="color:#AED6F1; margin:0;">ກວດສອບຈຸດຕົວເລກໄດ້ທັນທີ ແລະ ວິເຄາະລາຍປີ</p>
    </div>
    """, unsafe_allow_html=True)

def show_big_num(val):
    st.markdown(f'<div class="money-box">{val:,.0f} ກີບ</div>', unsafe_allow_html=True)

# --- 2. ສ່ວນປ້ອນຂໍ້ມູນ ---
with st.form("main_form"):
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("🟢 ລາຍຮັບ (Income)")
        i1 = st.number_input("ເງິນເດືອນ", min_value=0, step=50000); show_big_num(i1)
        i2 = st.number_input("ລາຍຮັບ Creator", min_value=0, step=10000); show_big_num(i2)
        i3 = st.number_input("ຂາຍຂອງຍ່ອຍ", min_value=0, step=5000); show_big_num(i3)
        i4 = st.number_input("ວຽກຕັດຫຍິບ", min_value=0, step=5000); show_big_num(i4)
        i5 = st.number_input("ຕູ້ກົດນ້ຳ", min_value=0, step=2000); show_big_num(i5)
        i6 = st.number_input("ຕູ້ຊັກຜ້າ", min_value=0, step=5000); show_big_num(i6)
    with c2:
        st.subheader("🔴 ລາຍຈ່າຍ (Expense)")
        e1 = st.number_input("ຄ່າອາຫານ/ເຄື່ອງໃຊ້", min_value=0, step=5000); show_big_num(e1)
        e2 = st.number_input("ຄ່າເຊົ່າ (ຖ້າບໍ່ມີໃສ່ 0)", min_value=0, step=100000); show_big_num(e2)
        e3 = st.number_input("ໄຟຟ້າ-ນໍ້າ-ເນັດ", min_value=0, step=5000); show_big_num(e3)
        e4 = st.number_input("ນ້ຳມັນ/ລົດຈ້າງ", min_value=0, step=5000); show_big_num(e4)
        e5 = st.number_input("ຄ່າຮຽນລູກ", min_value=0, step=50000); show_big_num(e5)
        e6 = st.number_input("ຄ່າຢາ/ປິ່ນປົວ", min_value=0, step=5000); show_big_num(e6)
        e7 = st.number_input("ເສື້ອຜ້າ/ສ່ວນຕົວ", min_value=0, step=5000); show_big_num(e7)
        e8 = st.number_input("ໂທລະສັບ/ບັນເທີງ", min_value=0, step=5000); show_big_num(e8)
        e9 = st.number_input("ຜ່ອນໜີ້/ລົດ", min_value=0, step=50000); show_big_num(e9)
        e10 = st.number_input("ຊື້ເຄື່ອງເຂົ້າຮ້ານ", min_value=0, step=10000); show_big_num(e10)
    
    submit = st.form_submit_button("🚀 ບັນທຶກຂໍ້ມູນທັງໝົດ", use_container_width=True)

if submit:
    now = datetime.now()
    total_in = i1+i2+i3+i4+i5+i6
    total_ex = e1+e2+e3+e4+e5+e6+e7+e8+e9+e10
    new_data = {
        'Date': now.strftime("%Y-%m-%d %H:%M"), 'Week': now.isocalendar()[1], 'Month': now.strftime("%m-%Y"), 'Year': str(now.year),
        'Total_In': total_in, 'Total_Ex': total_ex, 'Profit': total_in - total_ex, 'Food': e1, 'Sewing': i4, 'Debt': e9
    }
    pd.DataFrame([new_data]).to_csv(FILE_NAME, mode='a', index=False, header=not os.path.exists(FILE_NAME))
    st.balloons(); st.rerun()

# --- 3. ສ່ວນ AI ລາຍງານ ---
if os.path.exists(FILE_NAME):
    df = pd.read_csv(FILE_NAME)
    st.markdown("---")
    report = st.radio("📊 ເລືອກໄລຍະເວລາ:", ["ລາຍອາທິດ", "ລາຍເດືອນ", "ລາຍປີ"], horizontal=True)
    
    now = datetime.now()
    if report == "ລາຍອາທິດ": data = df[df['Week'] == now.isocalendar()[1]]; t = "ອາທິດນີ້"
    elif report == "ລາຍເດືອນ": data = df[df['Month'] == now.strftime("%m-%Y")]; t = "ເດືອນນີ້"
    else: data = df[df['Year'] == str(now.year)]; t = f"ປີ {now.year}"

    if not data.empty:
        c1, c2, c3 = st.columns(3)
        c1.metric(f"ລາຍຮັບ {t}", "{:,.0f} ກີບ".format(data['Total_In'].sum()))
        c2.metric(f"ລາຍຈ່າຍ {t}", "{:,.0f} ກີບ".format(data['Total_Ex'].sum()))
        c3.metric(f"ກຳໄລ {t}", "{:,.0f} ກີບ".format(data['Profit'].sum()))

        st.markdown("### 🧠 AI ວິເຄາະ ແລະ ວາງແຜນ")
        ai_col1, ai_col2 = st.columns(2)
        with ai_col1:
            st.info(f"💡 **ຊ່ອງທາງປະຢັດ:** ປີນີ້ປ້າຈ່າຍຄ່າອາຫານໄປແລ້ວ {data['Food'].sum():,.0f} ກີບ. ຖ້າຫຼຸດໄດ້ 10% ປ້າຈະມີເງິນເກັບເພີ່ມຂຶ້ນທັນທີ!")
        with ai_col2:
            st.success(f"🚀 **ແຜນອາຊີບ:** ລາຍໄດ້ຈາກການຕັດຫຍິບແມ່ນ {data['Sewing'].sum():,.0f} ກີບ. AI ແນະນຳໃຫ້ປ້າເຮັດຄລິບ Creator ສອນຫຍິບຜ້າງ່າຍໆ ເພື່ອຫາລາຍໄດ້ຕື່ມເດີ້!")
    
    with st.expander("📜 ປະຫວັດທັງໝົດ"):
        st.dataframe(df.sort_values(by='Date', ascending=False), use_container_width=True)