import streamlit as st
import pandas as pd
import os
from datetime import datetime, timedelta

# --- 1. ຕັ້ງຄ່າເບື້ອງຕົ້ນ ---
st.set_page_config(page_title="ລະບົບບັນຊີປ້າພອນສຸກ v9", layout="wide")
DB_FILE = 'phonsouk_final_database.csv'

# CSS ຕົບແຕ່ງ (ຕົວເລກໃຫຍ່, ປ່ຽນສີໃຫ້ອ່ານງ່າຍ)
st.markdown("""
    <style>
    .stNumberInput input { font-size: 20px !important; font-weight: bold; color: #1B4F72 !important; }
    header {visibility: hidden;}
    .ai-card { background-color: #f8f9fa; padding: 20px; border-radius: 15px; border-left: 10px solid #28a745; margin-bottom: 25px; box-shadow: 2px 2px 10px rgba(0,0,0,0.1); }
    .total-card { background-color: #1B4F72; color: white; padding: 15px; border-radius: 10px; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="total-card"><h1>🏦 ລະບົບບັນຊີ AI ປ້າພອນສຸກ (Full Version)</h1></div>', unsafe_allow_html=True)

# --- 2. ສ່ວນປ້ອນຂໍ້ມູນ (ໃສ່ຈຸດອັດຕະໂນມັດ 100%) ---
st.write("### 💰 ບ້ອນຕົວເລກ (ລະບົບຈະຄັ່ນຈຸດໃຫ້ເອງ)")

col1, col2 = st.columns(2)

with col1:
    st.success("### 🟢 ລາຍຮັບ")
    i1 = st.number_input("1. ເງິນເດືອນ", min_value=0, step=10000)
    i2 = st.number_input("2. ລາຍຮັບ Creator (FB/YouTube)", min_value=0, step=10000)
    i3 = st.number_input("3. ຂາຍຂອງຍ່ອຍ", min_value=0, step=10000)
    i4 = st.number_input("4. ຮັບຕັດຫຍິບ", min_value=0, step=10000)
    i5 = st.number_input("5. ຕູ້ກົດນ້ຳ", min_value=0, step=10000)
    i6 = st.number_input("6. ຕູ້ຊັກຜ້າ", min_value=0, step=10000)

with col2:
    st.error("### 🔴 ລາຍຈ່າຍ")
    e1 = st.number_input("1. ຄ່າອາຫານ & ຂອງໃຊ້", min_value=0, step=10000)
    e2 = st.number_input("2. ຄ່າເຊົ່າທີ່ຢູ່", min_value=0, step=10000)
    e3 = st.number_input("3. ຄ່ານ້ຳ-ໄຟ-ເນັດ", min_value=0, step=10000)
    e4 = st.number_input("4. ຄ່າເດີນທາງ/ນ້ຳມັນ", min_value=0, step=10000)
    e5 = st.number_input("5. ຄ່າການສຶກສາ", min_value=0, step=10000)
    e6 = st.number_input("6. ຄ່າປິ່ນປົວ/ຢາ", min_value=0, step=10000)
    e7 = st.number_input("7. ຄ່າເສື້ອຜ້າ/ເຄື່ອງນຸ່ງ", min_value=0, step=10000)
    e8 = st.number_input("8. ຄ່າບັນເທີງ/ທ່ອງທ່ຽວ", min_value=0, step=10000)
    e9 = st.number_input("9. ຄ່າຫວຍ/ລາງວັນ/ສັງຄົມ", min_value=0, step=10000)
    e10 = st.number_input("10. ຄ່າສ້າງເຮືອນ", min_value=0, step=10000)

# --- 3. ປຸ່ມບັນທຶກ ແລະ ການຄິດໄລ່ ---
st.markdown("---")
if st.button("💾 ບັນທຶກຂໍ້ມູນ ແລະ ຄິດໄລ່", use_container_width=True):
    total_in = float(i1 + i2 + i3 + i4 + i5 + i6)
    total_ex = float(e1 + e2 + e3 + e4 + e5 + e6 + e7 + e8 + e9 + e10)
    balance = total_in - total_ex
    
    current_time = (datetime.now() + timedelta(hours=7)).strftime("%d/%m/%Y %H:%M")
    
    new_data = {
        'ວັນທີ': current_time,
        'ລາຍຮັບລວມ': total_in,
        'ລາຍຈ່າຍລວມ': total_ex,
        'ເຫຼືອເກັບ': balance
    }
    
    # ບັນທຶກລົງ CSV
    df_new = pd.DataFrame([new_data])
    df_new.to_csv(DB_FILE, mode='a', index=False, header=not os.path.exists(DB_FILE), encoding='utf-8-sig')
    
    st.balloons()
    st.success(f"✅ ບັນທຶກແລ້ວ! ລາຍຮັບ: {total_in:,.0f} | ລາຍຈ່າຍ: {total_ex:,.0f} | ເຫຼືອເກັບ: {balance:,.0f} ກີບ")
    st.rerun()

# --- 4. ສ່ວນສະແດງຜົນ ແລະ Excel ---
if os.path.exists(DB_FILE):
    df = pd.read_csv(DB_FILE)
    
    # AI Summary
    total_all_saved = df['ເຫຼືອເກັບ'].sum()
    st.markdown(f"""
    <div class="ai-card">
        <h3>🤖 AI ທີ່ປຶກສາ (ປ້າພອນສຸກ)</h3>
        <p>ຍິນດີດ້ວຍເຈົ້າປ້າ! ຕອນນີ້ປ້າມີເງິນເກັບສະສົມທັງໝົດ <b>{total_all_saved:,.0f}</b> ກີບ.</p>
        <p>💡 <b>ຄຳແນະນຳ:</b> ຖ້າເດືອນນີ້ລາຍຈ່າຍຄ່າສ້າງເຮືອນສູງ, ລອງຫຼຸດຄ່າຫວຍລົງເດີ້ປ້າ ເພື່ອໃຫ້ເຮືອນແລ້ວໄວໆ!</p>
    </div>
    """, unsafe_allow_html=True)

    # ປຸ່ມ Download Excel
    st.write("### 📂 ຈັດການຂໍ້ມູນ")
    col_dl1, col_dl2 = st.columns(2)
    
    with col_dl1:
        # ແປງເປັນ Excel
        csv = df.to_csv(index=False).encode('utf-8-sig')
        st.download_button(
            label="📥 ດາວໂຫຼດຂໍ້ມູນເປັນ Excel (.csv)",
            data=csv,
            file_name=f'paphonsouk_account_{datetime.now().strftime("%Y%m%d")}.csv',
            mime='text/csv',
            use_container_width=True
        )

    with col_dl2:
        if st.button("🗑️ ລ້າງປະຫວັດທັງໝົດ (Reset)", use_container_width=True):
            if os.path.exists(DB_FILE):
                os.remove(DB_FILE)
                st.warning("ລ້າງຂໍ້ມູນທັງໝົດແລ້ວ!")
                st.rerun()

    # ຕະລາງສະແດງຜົນ
    st.write("### 📊 ປະຫວັດ 10 ລາຍການຫຼ້າສຸດ")
    st.dataframe(df.tail(10).style.format("{:,.0f}", subset=['ລາຍຮັບລວມ', 'ລາຍຈ່າຍລວມ', 'ເຫຼືອເກັບ']), use_container_width=True)
