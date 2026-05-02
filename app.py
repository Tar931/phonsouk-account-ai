import streamlit as st
import pandas as pd
import os
from datetime import datetime

# --- 1. ການຕັ້ງຄ່າພື້ນຖານ ---
st.set_page_config(page_title="Phonsouk Pro Advisor", page_icon="🏦", layout="wide")
FILE_NAME = 'phonsouk_final_database_v2.csv'

st.markdown("""
    <style>
    .money-box { 
        background-color: #002B36; color: #00FFAA; padding: 12px 20px; border-radius: 12px; 
        font-size: 28px; font-weight: bold; text-align: right; border: 2px solid #268BD2; margin-bottom: 25px;
    }
    .ai-card { 
        background-color: #ffffff; padding: 25px; border-radius: 20px; border-left: 15px solid #268BD2; 
        box-shadow: 0 4px 15px rgba(0,0,0,0.1); color: #1B4F72; margin-top: 20px;
    }
    .stNumberInput input { font-size: 20px !important; }
    </style>
    <div style="background-color:#1B4F72; padding:20px; border-radius:15px; text-align:center; color:white; margin-bottom:25px;">
        <h1 style="margin:0;">🏦 ລະບົບວິເຄາະການເງິນມືອາຊີບ ສື່ສານໂດຍ AI</h1>
        <p style="margin:5px 0 0 0; opacity:0.8;">ຈັດການລາຍຮັບ-ລາຍຈ່າຍ ສຳລັບປ້າພອນສຸກ</p>
    </div>
    """, unsafe_allow_html=True)

# --- 2. ສ່ວນປ້ອນຂໍ້ມູນ (ເນັ້ນຈຸດຕົວເລກ ແລະ ໃຊ້ງານງ່າຍ) ---
st.write("### 📝 ບັນທຶກລາຍວັນ")

with st.form("pro_form", clear_on_submit=True):
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🟢 ສ່ວນລາຍຮັບ")
        in_1 = st.number_input("ເງິນເດືອນ", min_value=0, step=50000)
        st.markdown(f'<div class="money-box">{in_1:,.0f} ກີບ</div>', unsafe_allow_html=True)
        
        in_2 = st.number_input("ລາຍຮັບຈາກ Creator (YouTube/FB)", min_value=0, step=10000)
        st.markdown(f'<div class="money-box">{in_2:,.0f} ກີບ</div>', unsafe_allow_html=True)
        
        in_3 = st.number_input("ວຽກຕັດຫຍິບ & ສ້ອມແປງ", min_value=0, step=10000)
        st.markdown(f'<div class="money-box">{in_3:,.0f} ກີບ</div>', unsafe_allow_html=True)

    with col2:
        st.markdown("### 🔴 ສ່ວນລາຍຈ່າຍ")
        ex_1 = st.number_input("ຄ່າອາຫານ ແລະ ເຄື່ອງໃຊ້ໃນເຮືອນ", min_value=0, step=10000)
        st.markdown(f'<div class="money-box">{ex_1:,.0f} ກີບ</div>', unsafe_allow_html=True)
        
        ex_2 = st.number_input("ຜ່ອນໜີ້ສິນ / ຄ່າງວດລົດ", min_value=0, step=50000)
        st.markdown(f'<div class="money-box">{ex_2:,.0f} ກີບ</div>', unsafe_allow_html=True)
        
        ex_3 = st.number_input("ຕົ້ນທຶນຊື້ເຄື່ອງເຂົ້າຮ້ານ", min_value=0, step=10000)
        st.markdown(f'<div class="money-box">{ex_3:,.0f} ກີບ</div>', unsafe_allow_html=True)

    submit = st.form_submit_button("🚀 ບັນທຶກຂໍ້ມູນທັງໝົດ", use_container_width=True)

    if submit:
        now = datetime.now()
        total_in = in_1 + in_2 + in_3
        total_ex = ex_1 + ex_2 + ex_3
        new_data = {
            'ວັນທີ_ເວລາ': now.strftime("%d/%m/%Y %H:%M"),
            'Date': now.strftime("%Y-%m-%d"),
            'Income': total_in, 'Expense': total_ex, 'Profit': total_in - total_ex,
            'Sewing': in_3, 'Debt': ex_2, 'Store': ex_3, 'Creator': in_2
        }
        pd.DataFrame([new_data]).to_csv(FILE_NAME, mode='a', index=False, header=not os.path.exists(FILE_NAME))
        st.success("✅ ບັນທຶກສຳເລັດ ແລະ ລ້າງໜ້າຈໍແລ້ວ!")
        st.rerun()

# --- 3. ສ່ວນ AI Advisor ແບບມືອາຊີບ ---
if os.path.exists(FILE_NAME):
    df = pd.read_csv(FILE_NAME)
    st.markdown("---")
    
    st.markdown("### 📊 ບົດວິເຄາະຈາກ AI ມືອາຊີບ")
    
    # ຄຳນວນຕົວເລກລວມ
    total_income = df['Income'].sum()
    total_expense = df['Expense'].sum()
    net_profit = total_income - total_expense
    
    c1, c2, c3 = st.columns(3)
    c1.metric("ລາຍຮັບສະສົມ", f"{total_income:,.0f} ກີບ")
    c2.metric("ລາຍຈ່າຍສະສົມ", f"{total_expense:,.0f} ກີບ")
    c3.metric("ກຳໄລສຸດທິ", f"{net_profit:,.0f} ກີບ", delta=f"{net_profit:,.0f}")

    st.markdown(f"""
    <div class="ai-card">
        <h2>💡 AI Professional Advisor Insights</h2>
        <hr>
        <p><b>📈 ວິເຄາະກະແສເງິນສົດ:</b> ຕອນນີ້ປ້າມີກຳໄລເຫຼືອເກັບ <b>{net_profit:,.0f} ກີບ</b>. 
        ແນະນຳໃຫ້ແບ່ງ 20% ເກັບເປັນເງິນສຳຮອງສຸກເສີນ ແລະ 10% ສຳລັບບຳລຸງຮັກສາຈັກຫຍິບຜ້າ.</p>
        
        <p><b>🧵 ດ້ານທຸລະກິດ:</b> ລາຍໄດ້ຈາກງານຫຍິບຜ້າສະສົມແມ່ນ <b>{df['Sewing'].sum():,.0f} ກີບ</b>. 
        ຫາກລາຍໄດ້ສ່ວນນີ້ເພີ່ມຂຶ້ນ 15% ໃນເດືອນໜ້າ ປ້າຈະສາມາດປິດງວດໜີ້ໄດ້ໄວຂຶ້ນ.</p>
        
        <p><b>⚠️ ຈຸດທີ່ຄວນລະວັງ:</b> ພາລະໜີ້ສິນຕອນນີ້ກວມເອົາ <b>{(df['Debt'].sum()/total_income)*100 if total_income > 0 else 0:.1f}%</b> ຂອງລາຍຮັບ. 
        ພະຍາຍາມຄຸມບໍ່ໃຫ້ເກີນ 40% ເພື່ອຄວາມຄ່ອງຕົວທາງການເງິນ.</p>
        
        <p><b>🚀 ຊ່ອງທາງເພີ່ມລາຍໄດ້:</b> AI ພົບວ່າລາຍໄດ້ຈາກ Creator ມີທ່າອ່ຽງດີ. ປ້າຄວນເຮັດຄລິບສອນຫຍິບຜ້າແບບງ່າຍໆ 
        ເພື່ອດຶງດູດລູກຄ້າໃໝ່ເຂົ້າຮ້ານຫຍິບຜ້າໄປໃນຕົວ.</p>
    </div>
    """, unsafe_allow_html=True)

    # ຕະລາງປະຫວັດ
    st.write("### 📅 ປະຫວັດການບັນທຶກ (Excel)")
    display_df = df.copy()
    for col in ['Income', 'Expense', 'Profit']:
        display_df[col] = display_df[col].apply(lambda x: f"{x:,.0f}")
    st.dataframe(display_df[['ວັນທີ_ເວລາ', 'Income', 'Expense', 'Profit']].tail(10), use_container_width=True)

    # --- 4. ປຸ່ມລົບຂໍ້ມູນ (ໃສ່ລະຫັດຜ່ານ) ---
    st.markdown("---")
    with st.expander("🛠️ ການຕັ້ງຄ່າຂັ້ນສູງ (ລົບຂໍ້ມູນ)"):
        st.warning("⚠️ ການກົດລົບຂໍ້ມູນຈະເຮັດໃຫ້ຂໍ້ມູນທັງໝົດຫາຍໄປຖາວອນ!")
        pwd = st.text_input("ກະລຸນາໃສ່ລະຫັດຜ່ານເພື່ອຢືນຢັນ (ລະຫັດແມ່ນ 9999):", type="password")
        if st.button("🗑️ ລ້າງຂໍ້ມູນທັງໝົດ"):
            if pwd == "9999":
                os.remove(FILE_NAME)
                st.success("ລົບຂໍ້ມູນທັງໝົດຮຽບຮ້ອຍແລ້ວ!")
                st.rerun()
            else:
                st.error("❌ ລະຫັດຜ່ານບໍ່ຖືກຕ້ອງ! ບໍ່ສາມາດລົບຂໍ້ມູນໄດ້.")