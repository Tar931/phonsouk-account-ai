import streamlit as st
import pandas as pd
import os
from datetime import datetime

# --- 1. ລະບົບ Login ---
def check_password():
    if "password_correct" not in st.session_state:
        st.markdown("### 🔒 ກະລຸນາໃສ່ລະຫັດຜ່ານ")
        pwd = st.text_input("ລະຫັດຜ່ານ:", type="password")
        if st.button("ເຂົ້າສູ່ລະບົບ"):
            if pwd == "1234":
                st.session_state["password_correct"] = True
                st.rerun()
            else:
                st.error("❌ ລະຫັດຜ່ານບໍ່ຖືກຕ້ອງ!")
        return False
    return True

if not check_password():
    st.stop()

# --- 2. ຕັ້ງຄ່າເວັບໄຊ ---
st.set_page_config(page_title="Phonsouk AI Secure", page_icon="🌸", layout="wide")
FILE_NAME = 'shop_database_v4.csv'

# ສ່ວນຫົວຂໍ້
st.markdown("""
    <div style="background-color:#1B4F72;padding:20px;border-radius:15px;text-align:center;">
        <h1 style="color:white;">🌸 ລະບົບບັນຊີ ປ້າພອນສຸກ + AI ວິເຄາະ</h1>
        <p style="color:#AED6F1;">ບ້ານໂພນສະຫວັນ | ລະບົບວາງແຜນການເງິນອັດສະລິຍະ</p>
    </div>
    """, unsafe_allow_html=True)

# --- 3. ສ່ວນປ້ອນຂໍ້ມູນ ---
st.subheader("📝 ປ້ອນລາຍການປະຈຳວັນ")
col1, col2 = st.columns(2)

with col1:
    st.markdown("#### 🟢 ຝ່າຍລາຍຮັບ")
    s1 = st.number_input("ຍອດຂາຍໜ້າຮ້ານ", min_value=0, step=5000)
    st.markdown(f"<div style='color:#2E7D32; background-color:#E8F5E9; padding:8px; border-radius:5px; font-weight:bold; font-size:20px;'>💰 {s1:,.0f} ກີບ</div>", unsafe_allow_html=True)
    
    s2 = st.number_input("ຄ່າວຽກຕັດຫຍິບ", min_value=0, step=5000)
    st.markdown(f"<div style='color:#2E7D32; background-color:#E8F5E9; padding:8px; border-radius:5px; font-weight:bold; font-size:20px;'>💰 {s2:,.0f} ກີບ</div>", unsafe_allow_html=True)
    
    s3 = st.number_input("ຂາຍເຄື່ອງ Online", min_value=0, step=5000)
    s4 = st.number_input("ຕູ້ກົດນ້ຳ/ຊັກຜ້າ", min_value=0, step=1000)

with col2:
    st.markdown("#### 🔴 ຝ່າຍລາຍຈ່າຍ")
    e1 = st.number_input("ຊື້ເຄື່ອງເຂົ້າຮ້ານ (Stock)", min_value=0, step=5000)
    st.markdown(f"<div style='color:#C62828; background-color:#FFEBEE; padding:8px; border-radius:5px; font-weight:bold; font-size:20px;'>💸 {e1:,.0f} ກີບ</div>", unsafe_allow_html=True)
    
    e2 = st.number_input("ຄ່ານ້ຳ + ຄ່າໄຟ", min_value=0, step=1000)
    e3 = st.number_input("ຄ່າກິນ/ໃຊ້ຈ່າຍໃນເຮືອນ", min_value=0, step=5000)
    st.markdown(f"<div style='color:#C62828; background-color:#FFEBEE; padding:8px; border-radius:5px; font-weight:bold; font-size:20px;'>💸 {e3:,.0f} ກີບ</div>", unsafe_allow_html=True)
    
    e4 = st.number_input("ລາຍຈ່າຍອື່ນໆ", min_value=0, step=1000)

if st.button("💾 ກົດບັນທຶກຂໍ້ມູນ", use_container_width=True, type="primary"):
    total_in = s1 + s2 + s3 + s4
    total_out = e1 + e2 + e3 + e4
    new_entry = {
        'Date': datetime.now().strftime("%d-%m-%Y %H:%M"),
        'Month': datetime.now().strftime("%m-%Y"),
        'Sewing': s2, 'In': total_in, 'Out': total_out, 
        'Profit': total_in - total_out, 'Food': e3, 'Stock': e1
    }
    df_new = pd.DataFrame([new_entry])
    df_new.to_csv(FILE_NAME, mode='a', index=False, header=not os.path.exists(FILE_NAME))
    st.balloons(); st.success("✅ ບັນທຶກສຳເລັດແລ້ວ!"); st.rerun()

st.markdown("---")

# --- 4. ສ່ວນ AI ວິເຄາະ ແລະ ສະແດງຜົນ ---
if os.path.exists(FILE_NAME):
    df = pd.read_csv(FILE_NAME)
    if not df.empty:
        # --- ສ່ວນ AI ວິເຄາະ (ເພີ່ມຄືນໃຫ້ແລ້ວ) ---
        st.header("🤖 ລະບົບ AI ວິເຄາະ ແລະ ແນະນຳການເງິນ")
        ai_col1, ai_col2 = st.columns(2)
        
        with ai_col1:
            st.markdown("### 📊 ສຸຂະພາບການເງິນ")
            last_profit = df['Profit'].iloc[-1]
            total_in = df['In'].sum()
            total_food = df['Food'].sum()
            food_ratio = (total_food / total_in * 100) if total_in > 0 else 0
            
            if last_profit > 0:
                st.success(f"📈 ມື້ຫຼ້າສຸດປ້າໄດ້ກຳໄລ: **{last_profit:,.0f} ກີບ**. ຖືວ່າການຄ້າຂາຍໄປໄດ້ດີ!")
            else:
                st.warning(f"📉 ມື້ນີ້ລາຍຈ່າຍຫຼາຍກວ່າລາຍຮັບ: **{last_profit:,.0f} ກີບ**. ລອງກວດເບິ່ງຄືນເດີ້ປ້າ.")
            
            if food_ratio > 30:
                st.error(f"⚠️ AI ເຕືອນ: ຄ່າກິນ/ໃຊ້ຈ່າຍ ສູງເຖິງ **{food_ratio:.1f}%**. ລອງຫຼຸດລາຍຈ່າຍສ່ວນນີ້ເພື່ອເພີ່ມເງິນເກັບ.")
            else:
                st.info("✅ ປ້າບໍລິຫານຄ່າໃຊ້ຈ່າຍໃນເຮືອນໄດ້ດີຫຼາຍ!")

        with ai_col2:
            st.markdown("### 💡 ແຜນຊອກຫາເງິນເພີ່ມ")
            avg_sewing = df['Sewing'].mean()
            if avg_sewing > 100000:
                st.write("✨ **AI ແນະນຳ:** ວຽກຕັດຫຍິບສ້າງລາຍໄດ້ດີ. ປ້າລອງຕິດປ້າຍ 'ຮັບແປງຊຸດດ່ວນ' ຢູ່ໜ້າບ້ານໂພນສະຫວັນ ເພື່ອຫາລູກຄ້າໃໝ່.")
            st.write("✨ **ແຜນອອມເງິນ:** AI ແນະນຳໃຫ້ປ້າແບ່ງກຳໄລ 10% ຂອງທຸກມື້ ເຂົ້າບັນຊີເງິນຝາກ ເພື່ອເປັນທຶນຂະຫຍາຍຮ້ານໃນອະນາຄົດ.")

        st.markdown("---")
        # ຕາຕະລາງ
        st.subheader("📊 ປະຫວັດການບັນທຶກ (ມີຈຸດຄັ່ນທຸກຊ່ອງ)")
        df_show = df.copy()
        for col in ['Sewing', 'In', 'Out', 'Profit', 'Food', 'Stock']:
            df_show[col] = df_show[col].apply(lambda x: "{:,.0f}".format(float(x)))
        st.dataframe(df_show.tail(15), use_container_width=True)
        
        if st.button("⚠️ ລຶບແຖວລ່າສຸດ"):
            df.drop(df.index[-1]).to_csv(FILE_NAME, index=False); st.rerun()