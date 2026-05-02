import streamlit as st
import pandas as pd
import os
from datetime import datetime

# --- 1. ຕັ້ງຄ່າເວັບໄຊ ແລະ Style (ມືອາຊີບ) ---
st.set_page_config(page_title="Phonsouk Professional AI", page_icon="🏦", layout="wide")
FILE_NAME = 'phonsouk_final_database_v2.csv'

# ໃຊ້ Session State ເພື່ອລ້າງຂໍ້ມູນຫຼັງ Save
if 'reset_val' not in st.session_state:
    st.session_state.reset_val = 0

st.markdown("""
    <style>
    .money-box { 
        background-color: #002B36; color: #00FFAA; padding: 10px 15px; border-radius: 10px; 
        font-size: 24px; font-weight: bold; text-align: right; border: 2px solid #268BD2; margin-bottom: 20px;
    }
    .ai-card { background-color: #FFFFFF; padding: 25px; border-radius: 20px; border-left: 12px solid #268BD2; 
               box-shadow: 0 4px 6px rgba(0,0,0,0.1); color: #1B4F72; }
    .stNumberInput > div > div > input { font-size: 20px !important; font-weight: bold !important; }
    </style>
    <div style="background-color:#1B4F72; padding:20px; border-radius:15px; text-align:center; color:white; margin-bottom:25px;">
        <h1 style="margin:0;">🏦 ລະບົບທີ່ປຶກສາການເງິນອັດສະລິຍະ (Professional Version)</h1>
        <p style="margin:0; opacity:0.8;">ສຳລັບ: ປ້າພອນສຸກ | ວາງແຜນ, ວິເຄາະ, ແລະ ເຕີບໂຕ</p>
    </div>
    """, unsafe_allow_html=True)

# --- 2. ສ່ວນປ້ອນຂໍ້ມູນ (ມີລະບົບ Auto-Clear) ---
st.write("### 📝 ບັນທຶກລາຍຮັບ - ລາຍຈ່າຍ")
with st.form("finance_form", clear_on_submit=True):
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("### 🟢 ລາຍຮັບ")
        i1 = st.number_input("ເງິນເດືອນ", min_value=0, step=10000)
        i2 = st.number_input("ລາຍຮັບ Creator", min_value=0, step=10000)
        i3 = st.number_input("ຂາຍຂອງຍ່ອຍ", min_value=0, step=10000)
        i4 = st.number_input("ວຽກຕັດຫຍິບ", min_value=0, step=10000)
        i5 = st.number_input("ຕູ້ກົດນ້ຳ", min_value=0, step=10000)
        i6 = st.number_input("ຕູ້ຊັກຜ້າ", min_value=0, step=10000)

    with c2:
        st.markdown("### 🔴 ລາຍຈ່າຍ")
        e1 = st.number_input("ຄ່າອາຫານ/ເຄື່ອງໃຊ້", min_value=0, step=10000)
        e2 = st.number_input("ຄ່າເຊົ່າທີ່ຢູ່", min_value=0, step=10000)
        e3 = st.number_input("ໄຟຟ້າ-ນໍ້າ-ເນັດ", min_value=0, step=10000)
        e4 = st.number_input("ນ້ຳມັນ/ລົດຈ້າງ", min_value=0, step=10000)
        e5 = st.number_input("ຄ່າຮຽນລູກ", min_value=0, step=10000)
        e9 = st.number_input("ຜ່ອນໜີ້/ລົດ", min_value=0, step=10000)
        e10 = st.number_input("ຊື້ເຄື່ອງເຂົ້າຮ້ານ", min_value=0, step=10000)

    submitted = st.form_submit_button("🚀 ບັນທຶກ ແລະ ລ້າງຂໍ້ມູນ", use_container_width=True)
    
    if submitted:
        now = datetime.now()
        total_in = i1+i2+i3+i4+i5+i6
        total_ex = e1+e2+e3+e4+e5+e9+e10
        new_entry = {
            'ວັນທີ_ເວລາ': now.strftime("%d/%m/%Y %H:%M"),
            'Date': now.strftime("%Y-%m-%d"), 'Week': now.isocalendar()[1], 'Month': now.strftime("%m-%Y"), 'Year': str(now.year),
            'Income': total_in, 'Expense': total_ex, 'Profit': total_in - total_ex,
            'Food': e1, 'Debt': e9, 'Sewing': i4, 'Vending': i5+i6, 'Store': e10
        }
        pd.DataFrame([new_entry]).to_csv(FILE_NAME, mode='a', index=False, header=not os.path.exists(FILE_NAME))
        st.balloons()
        st.rerun()

# --- 3. ການວິເຄາະ AI ແບບມືອາຊີບ ---
if os.path.exists(FILE_NAME):
    df = pd.read_csv(FILE_NAME)
    st.markdown("---")
    period = st.radio("📊 ເລືອກໄລຍະວິເຄາະ:", ["ມື້ນີ້", "ລາຍອາທິດ", "ລາຍເດືອນ", "ລາຍປີ"], horizontal=True)
    
    now = datetime.now()
    if period == "ມື້ນີ້": data = df[df['Date'] == now.strftime("%Y-%m-%d")]; t = "ມື້ນີ້"
    elif period == "ລາຍອາທິດ": data = df[df['Week'] == now.isocalendar()[1]]; t = "ອາທິດນີ້"
    elif period == "ລາຍເດືອນ": data = df[df['Month'] == now.strftime("%m-%Y")]; t = "ເດືອນນີ້"
    else: data = df[df['Year'] == str(now.year)]; t = f"ປີ {now.year}"

    if not data.empty:
        c1, c2, c3 = st.columns(3)
        in_sum, ex_sum = data['Income'].sum(), data['Expense'].sum()
        profit = in_sum - ex_sum
        c1.metric(f"ລາຍຮັບ {t}", f"{in_sum:,.0f} ກີບ")
        c2.metric(f"ລາຍຈ່າຍ {t}", f"{ex_sum:,.0f} ກີບ")
        c3.metric(f"ກຳໄລຕົວຈິງ {t}", f"{profit:,.0f} ກີບ", delta=f"{profit:,.0f}")

        # --- AI Professional Analysis Section ---
        st.markdown(f'<div class="ai-card"><h2>💡 AI Professional Insight ({t})</h2>', unsafe_allow_html=True)
        col_a, col_b = st.columns(2)
        
        with col_a:
            st.write("### 📈 ວິເຄາະກະແສເງິນ")
            if profit > 0:
                st.success(f"✅ ປ້າພອນສຸກມີເງິນເຫຼືອເກັບ {profit:,.0f} ກີບ. ແນະນຳໃຫ້ແບ່ງ 20% ເຂົ້າບັນຊີເງິນທ້ອນສຸກເສີນ.")
            else:
                st.error("⚠️ ຕອນນີ້ລາຍຈ່າຍສູງກວ່າລາຍຮັບ! ຄວນກວດສອບລາຍຈ່າຍທີ່ບໍ່ຈຳເປັນທັນທີ.")
            
            debt_val = data['Debt'].sum() if 'Debt' in data.columns else 0
            if debt_val > 0:
                st.warning(f"💳 ພາລະໜີ້ສິນ: {debt_val:,.0f} ກີບ ({ (debt_val/in_sum)*100 if in_sum>0 else 0:.1f}% ຂອງລາຍຮັບ). ພະຍາຍາມບໍ່ໃຫ້ເກີນ 30%.")

        with col_b:
            st.write("### 🏠 ວິເຄາະທຸລະກິດ & ອາຊີບ")
            sewing = data['Sewing'].sum() if 'Sewing' in data.columns else 0
            vending = data['Vending'].sum() if 'Vending' in data.columns else 0
            st.info(f"🧵 ງານຫຍິບຜ້າສ້າງລາຍໄດ້ໃຫ້ປ້າ {sewing:,.0f} ກີບ. ເປັນອາຊີບທີ່ໝັ້ນຄົງດີຫຼາຍ.")
            st.info(f"💧 ຕູ້ກົດນ້ຳ/ຊັກຜ້າ ສ້າງ Passive Income: {vending:,.0f} ກີບ. ຄວນຮັກສາຄວາມສະອາດຕູ້ເປັນປະຈຳ.")
        
        st.markdown('</div>', unsafe_allow_html=True)

    # ຕະລາງ Excel
    st.markdown("### 📅 ປະຫວັດການບັນທຶກ (Excel Format)")
    display_df = df.copy()
    for col in ['Income', 'Expense', 'Profit']:
        if col in display_df.columns: display_df[col] = display_df[col].apply(lambda x: f"{x:,.0f}")
    st.dataframe(display_df[['ວັນທີ_ເວລາ', 'Income', 'Expense', 'Profit']].tail(10), use_container_width=True)

    # --- 4. ປຸ່ມ Reset ແບບໃສ່ລະຫັດ (Security Lock) ---
    st.markdown("---")
    with st.expander("🛠️ ການຕັ້ງຄ່າລະບົບ (ລົບຂໍ້ມູນ)"):
        st.write("⚠️ ຄຳເຕືອນ: ການລົບຂໍ້ມູນຈະບໍ່ສາມາດກູ້ຄືນໄດ້.")
        pwd = st.text_input("ກະລຸນາໃສ່ລະຫັດຜ່ານເພື່ອລົບ (ລະຫັດແມ່ນ 9999):", type="password")
        if st.button("🗑️ ຢືນຢັນລ້າງຂໍ້ມູນທັງໝົດ"):
            if pwd == "9999":
                os.remove(FILE_NAME)
                st.success("ລ້າງຂໍ້ມູນສຳເລັດແລ້ວ! ປ້າເລີ່ມບັນທຶກໃໝ່ໄດ້ເລີຍ.")
                st.rerun()
            else:
                st.error("ລະຫັດຜ່ານບໍ່ຖືກຕ້ອງ! ບໍ່ສາມາດລົບໄດ້.")