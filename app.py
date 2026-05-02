import streamlit as st
import pandas as pd
import os
from datetime import datetime

# --- 1. ຕັ້ງຄ່າເວັບໄຊ ---
st.set_page_config(page_title="Phonsouk Smart AI", page_icon="🏦", layout="wide")
FILE_NAME = 'phonsouk_final_database_v2.csv'

st.markdown("""
    <style>
    .money-box { 
        background-color: #002B36; color: #00FFAA; padding: 15px; border-radius: 12px; 
        font-size: 30px; font-weight: bold; text-align: right; border: 2px solid #268BD2; margin-bottom: 20px;
    }
    .ai-card { 
        background-color: #f8f9fa; padding: 25px; border-radius: 15px; border-left: 10px solid #268BD2; 
        box-shadow: 0 4px 10px rgba(0,0,0,0.05); color: #1B4F72; line-height: 1.6;
    }
    .stNumberInput input { font-size: 22px !important; font-weight: bold; }
    </style>
    <div style="background-color:#1B4F72; padding:20px; border-radius:15px; text-align:center; color:white; margin-bottom:25px;">
        <h1 style="margin:0;">🏦 ລະບົບ AI ທີ່ປຶກສາການເງິນ ປ້າພອນສຸກ</h1>
        <p style="margin:5px 0 0 0; opacity:0.9;">Professional Financial & Business Advisor</p>
    </div>
    """, unsafe_allow_html=True)

# --- 2. ສ່ວນປ້ອນຂໍ້ມູນ (ເນັ້ນຄວາມງ່າຍ ແລະ ຈຸດຕົວເລກ) ---
st.write("### 📝 ບັນທຶກລາຍຮັບ - ລາຍຈ່າຍ")

# ໃຊ້ Form ເພື່ອໃຫ້ລ້າງຂໍ້ມູນໄດ້ 100% ຫຼັງກົດ Save
with st.form("smart_form", clear_on_submit=True):
    c1, c2 = st.columns(2)
    
    with c1:
        st.markdown("### 🟢 ລາຍຮັບ (Income)")
        i1 = st.number_input("ເງິນເດືອນ", min_value=0, step=100000); st.markdown(f'<div class="money-box">{i1:,.0f} ກີບ</div>', unsafe_allow_html=True)
        i2 = st.number_input("ລາຍຮັບ Creator (FB/YouTube)", min_value=0, step=10000); st.markdown(f'<div class="money-box">{i2:,.0f} ກີບ</div>', unsafe_allow_html=True)
        i3 = st.number_input("ວຽກຕັດຫຍິບ & ສ້ອມແປງ", min_value=0, step=10000); st.markdown(f'<div class="money-box">{i3:,.0f} ກີບ</div>', unsafe_allow_html=True)

    with c2:
        st.markdown("### 🔴 ລາຍຈ່າຍ (Expense)")
        e1 = st.number_input("ຄ່າອາຫານ & ຂອງໃຊ້", min_value=0, step=10000); st.markdown(f'<div class="money-box">{e1:,.0f} ກີບ</div>', unsafe_allow_html=True)
        e2 = st.number_input("ຜ່ອນໜີ້ / ຄ່າງວດ", min_value=0, step=50000); st.markdown(f'<div class="money-box">{e2:,.0f} ກີບ</div>', unsafe_allow_html=True)
        e3 = st.number_input("ຕົ້ນທຶນຊື້ເຄື່ອງເຂົ້າຮ້ານ", min_value=0, step=10000); st.markdown(f'<div class="money-box">{e3:,.0f} ກີບ</div>', unsafe_allow_html=True)

    submit = st.form_submit_button("💾 ບັນທຶກຂໍ້ມູນ ແລະ ວິເຄາະທັນທີ", use_container_width=True)

    if submit:
        now = datetime.now()
        total_in = i1 + i2 + i3
        total_ex = e1 + e2 + e3
        new_data = {
            'ວັນທີ_ເວລາ': now.strftime("%d/%m/%Y %H:%M"),
            'Date': now.strftime("%Y-%m-%d"), 'Month': now.strftime("%m-%Y"),
            'Income': total_in, 'Expense': total_ex, 'Profit': total_in - total_ex,
            'Sewing': i3, 'Debt': e2, 'Creator': i2, 'Food': e1
        }
        pd.DataFrame([new_data]).to_csv(FILE_NAME, mode='a', index=False, header=not os.path.exists(FILE_NAME))
        st.balloons()
        st.rerun()

# --- 3. ສ່ວນສະແດງຜົນ ແລະ AI Advisor ມືອາຊີບ ---
if os.path.exists(FILE_NAME):
    df = pd.read_csv(FILE_NAME)
    st.markdown("---")
    
    # ບົດສະຫຼຸບຕົວເລກ
    t_in, t_ex = df['Income'].sum(), df['Expense'].sum()
    profit = t_in - t_ex
    
    col_a, col_b, col_c = st.columns(3)
    col_a.metric("ລາຍຮັບທັງໝົດ", f"{t_in:,.0f} ກີບ")
    col_b.metric("ລາຍຈ່າຍທັງໝົດ", f"{t_ex:,.0f} ກີບ")
    col_c.metric("ກຳໄລສຸດທິ", f"{profit:,.0f} ກີບ", delta=f"{profit:,.0f}")

    # AI Professional Insight (ແກ້ໄຂໃຫ້ອ່ານງ່າຍ ບໍ່ມີ Code ປົນ)
    st.markdown('<div class="ai-card">', unsafe_allow_html=True)
    st.subheader("💡 AI Professional Advisor Insights")
    
    # ວິເຄາະ 1: ກະແສເງິນ
    if profit > 0:
        st.write(f"✅ **ການເງິນດີ:** ປ້າມີເງິນເຫຼືອເກັບ **{profit:,.0f} ກີບ**. ຫຼານແນະນຳໃຫ້ແບ່ງ 20% ໄປທ້ອນເພື່ອໄວ້ໃຊ້ຍາມສຸກເສີນ ແລະ ອີກ 10% ແມ່ນເອົາໄວ້ພັດທະນາຮ້ານຫຍິບຜ້າ.")
    else:
        st.write("⚠️ **ຄຳເຕືອນ:** ລາຍຈ່າຍຕອນນີ້ສູງກວ່າລາຍຮັບ. ປ້າຄວນກວດສອບຄ່າອາຫານ ຫຼື ຄ່າໃຊ້ຈ່າຍຟຸມເຟືອຍອື່ນໆ.")

    # ວິເຄາະ 2: ທຸລະກິດ
    sewing_total = df['Sewing'].sum()
    st.write(f"🧵 **ດ້ານທຸລະກິດ:** ວຽກຕັດຫຍິບສ້າງລາຍໄດ້ໃຫ້ປ້າແລ້ວ **{sewing_total:,.0f} ກີບ**. ນີ້ຄືອາຊີບທີ່ໝັ້ນຄົງ ຄວນຮັກສາຄຸນນະພາບເພື່ອໃຫ້ລູກຄ້າບອກຕໍ່.")

    # ວິເຄາະ 3: ໜີ້ສິນ
    debt_total = df['Debt'].sum()
    debt_ratio = (debt_total / t_in * 100) if t_in > 0 else 0
    st.write(f"💳 **ພາລະໜີ້ສິນ:** ປ້າຈ່າຍຄ່າງວດໄປແລ້ວ **{debt_total:,.0f} ກີບ** (ຄິດເປັນ {debt_ratio:.1f}% ຂອງລາຍຮັບ). ພະຍາຍາມຄຸມບໍ່ໃຫ້ເກີນ 40% ຈະເຮັດໃຫ້ປ້າບໍ່ເຄັ່ງຄຽດ.")

    # ວິເຄາະ 4: ຊ່ອງທາງເພີ່ມລາຍໄດ້
    st.write(f"🚀 **ຊ່ອງທາງລວຍ:** ລາຍໄດ້ຈາກ Creator (**{df['Creator'].sum():,.0f} ກີບ**) ມີໂອກາດເຕີບໂຕ. ປ້າລອງເຮັດຄລິບ 'ເຄັດລັບການເລືອກຜ້າ' ຫຼື 'ວິທີແປງໂສ້ງແບບງ່າຍໆ' ຈະຊ່ວຍດຶງຄົນເຂົ້າເບິ່ງຫຼາຍຂຶ້ນ!")
    
    st.markdown('</div>', unsafe_allow_html=True)

    # ຕະລາງປະຫວັດ
    st.write("### 📅 ປະຫວັດການບັນທຶກ (Excel)")
    display_df = df.copy()
    for col in ['Income', 'Expense', 'Profit']:
        display_df[col] = display_df[col].apply(lambda x: f"{x:,.0f}")
    st.dataframe(display_df[['ວັນທີ_ເວລາ', 'Income', 'Expense', 'Profit']].tail(10), use_container_width=True)

    # --- 4. ປຸ່ມລົບຂໍ້ມູນ (ໃສ່ລະຫັດຜ່ານ 9999) ---
    st.markdown("---")
    with st.expander("🛠️ ຕັ້ງຄ່າຂັ້ນສູງ (ລົບຂໍ້ມູນ)"):
        st.warning("⚠️ ຄຳເຕືອນ: ການລົບຂໍ້ມູນຈະບໍ່ສາມາດກູ້ຄືນໄດ້.")
        pwd = st.text_input("ໃສ່ລະຫັດຜ່ານ 9999 ເພື່ອຢືນຢັນການລົບ:", type="password")
        if st.button("🗑️ ຢືນຢັນລ້າງຂໍ້ມູນທັງໝົດ"):
            if pwd == "9999":
                if os.path.exists(FILE_NAME): os.remove(FILE_NAME)
                st.success("ລົບຂໍ້ມູນແລ້ວ!")
                st.rerun()
            else:
                st.error("ລະຫັດຜ່ານບໍ່ຖືກຕ້ອງ!")