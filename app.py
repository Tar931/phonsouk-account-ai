import streamlit as st
import pandas as pd
import os
from datetime import datetime

# --- 1. ຕັ້ງຄ່າເວັບໄຊ ---
st.set_page_config(page_title="Phonsouk AI Business Advisor", page_icon="🤖", layout="wide")
FILE_NAME = 'shop_database_v4.csv'

# ສ່ວນຫົວຂໍ້ແບບທັນສະໄໝ
st.markdown("""
    <div style="background-color:#0E1117;padding:20px;border-radius:15px;text-align:center;border: 2px solid #00FFAA;">
        <h1 style="color:#00FFAA;">🤖 ລະບົບບັນຊີ + AI ອັດສະລິຍະ ປ້າພອນສຸກ</h1>
        <p style="color:#FFFFFF;">ວິເຄາະການເງິນລະດັບສູງ ບ້ານໂພນສະຫວັນ</p>
    </div>
    """, unsafe_allow_html=True)

# --- 2. ຟັງຊັນສະແດງຕົວເລກ (Input Monitor) ---
def input_monitor(label, amount, color):
    st.markdown(f"""
        <div style="border-left: 5px solid {color}; padding-left: 10px; margin-bottom: 10px;">
            <small style="color: gray;">{label}</small><br>
            <strong style="font-size: 20px; color: {color};">{amount:,.0f} ກີບ</strong>
        </div>
    """, unsafe_allow_html=True)

# --- 3. ສ່ວນປ້ອນຂໍ້ມູນ ---
st.write("### 📝 ບັນທຶກຂໍ້ມູນມື້ນີ້")
col1, col2 = st.columns(2)

with col1:
    st.markdown("#### 🟢 ຂາເຂົ້າ (Income)")
    s1 = st.number_input("ຍອດຂາຍໜ້າຮ້ານ", min_value=0, step=5000, key="n1")
    input_monitor("ກວດສອບຍອດຂາຍ:", s1, "#2E7D32")
    
    s2 = st.number_input("ວຽກຕັດຫຍິບ (Sewing)", min_value=0, step=5000, key="n2")
    input_monitor("ກວດສອບຄ່າຕັດຫຍິບ:", s2, "#2E7D32")
    
    s3 = st.number_input("ລາຍຮັບອື່ນໆ / Online", min_value=0, step=5000, key="n3")
    input_monitor("ກວດສອບລາຍຮັບອື່ນ:", s3, "#2E7D32")

with col2:
    st.markdown("#### 🔴 ຂາອອກ (Expense)")
    e1 = st.number_input("ຊື້ເຄື່ອງ Stock", min_value=0, step=5000, key="n4")
    input_monitor("ກວດສອບຄ່າ Stock:", e1, "#C62828")
    
    e2 = st.number_input("ຄ່າກິນ / ໃຊ້ຈ່າຍຄົວເຮືອນ", min_value=0, step=5000, key="n5")
    input_monitor("ກວດສອບຄ່າກິນ:", e2, "#C62828")
    
    e3 = st.number_input("ລາຍຈ່າຍອື່ນໆ", min_value=0, step=1000, key="n6")
    input_monitor("ກວດສອບຈ່າຍອື່ນ:", e3, "#C62828")

if st.button("🚀 ບັນທຶກ ແລະ ໃຫ້ AI ວິເຄາະ", use_container_width=True, type="primary"):
    total_in = s1 + s2 + s3
    total_out = e1 + e2 + e3
    new_entry = {
        'Date': datetime.now().strftime("%d-%m-%Y %H:%M"),
        'Month': datetime.now().strftime("%m-%Y"),
        'Sewing': s2, 'In': total_in, 'Out': total_out, 
        'Profit': total_in - total_out, 'Food': e2, 'Stock': e1
    }
    df_new = pd.DataFrame([new_entry])
    df_new.to_csv(FILE_NAME, mode='a', index=False, header=not os.path.exists(FILE_NAME))
    st.success("✅ ບັນທຶກສຳເລັດ! ກະລຸນາເບິ່ງຄຳແນະນຳ AI ທາງລຸ່ມ")

# --- 4. ສ່ວນສະໝອງ AI (Smart Analytics) ---
if os.path.exists(FILE_NAME):
    df = pd.read_csv(FILE_NAME)
    if not df.empty:
        st.markdown("---")
        st.header("🧠 ສະໝອງ AI ວິເຄາະການເງິນໃຫ້ປ້າ")
        
        last_row = df.iloc[-1]
        all_profit = df['Profit'].sum()
        avg_profit = df['Profit'].mean()
        
        ai_col1, ai_col2 = st.columns(2)
        
        with ai_col1:
            st.subheader("📊 ສະຖານະການເງິນ")
            if last_row['Profit'] > 0:
                st.write(f"✅ **ມື້ນີ້ກຳໄລ:** {last_row['Profit']:,.0f} ກີບ. ຖືວ່າປ້າເຮັດໄດ້ດີຫຼາຍ!")
            else:
                st.write(f"⚠️ **ມື້ນີ້ຂາດທຶນ:** {last_row['Profit']:,.0f} ກີບ. ປ້າລອງກວດເບິ່ງລາຍຈ່າຍຄືນເດີ້.")
            
            food_percent = (last_row['Food'] / last_row['In'] * 100) if last_row['In'] > 0 else 0
            if food_percent > 40:
                st.error(f"🚨 AI ເຕືອນ: ປ້າໃຊ້ເງິນຄ່າກິນສູງເຖິງ {food_percent:.1f}% ຂອງລາຍຮັບ. ລອງຫຼຸດເດີ້ປ້າ!")
            else:
                st.info("💡 ຄ່າໃຊ້ຈ່າຍໃນເຮືອນຢູ່ໃນເກນປົກກະຕິ.")

        with ai_col2:
            st.subheader("💡 ຄຳແນະນຳຈາກ AI")
            if last_row['Sewing'] > (last_row['In'] * 0.5):
                st.write("✨ ວຽກຕັດຫຍິບແມ່ນລາຍຮັບຫຼັກ. AI ແນະນຳໃຫ້ປ້າຊື້ເຂັມ ຫຼື ອຸປະກອນສຳຮອງໄວ້.")
            
            if all_profit > 1000000:
                st.write("💰 ປ້າມີເງິນເກັບສະສົມຫຼາຍແລ້ວ. AI ແນະນຳໃຫ້ແບ່ງ 20% ໄປຊື້ຄຳ ຫຼື ຝາກປະຈຳ.")
            else:
                st.write("📉 ໄລຍະນີ້ກຳໄລຍັງໜ້ອຍ. AI ແນະນຳໃຫ້ປ້າລອງໂພສຂາຍເຄື່ອງ Online ເພີ່ມ.")

        # ສະແດງຕາຕະລາງ
        st.markdown("---")
        st.subheader("📑 ປະຫວັດບັນຊີ (ມີຈຸດຄັ່ນທຸກຊ່ອງ)")
        df_show = df.copy()
        for col in ['Sewing', 'In', 'Out', 'Profit', 'Food', 'Stock']:
            df_show[col] = df_show[col].apply(lambda x: "{:,.0f}".format(float(x)))
        st.dataframe(df_show.tail(10), use_container_width=True)