import streamlit as st
import pandas as pd
import os
from datetime import datetime, timedelta

# --- 1. ຕັ້ງຄ່າ AI ແບບພື້ນຖານ (ແກ້ບັນຫາ Error RequestOptions) ---
ai_error_msg = ""
try:
    import google.generativeai as genai
    
    # ກວດສອບວ່າປ້າໃສ່ Key ໃນ Secrets ແລ້ວຫຼືຍັງ
    if "GEMINI_API_KEY" in st.secrets:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        # ໃຊ້ gemini-pro ເພື່ອຄວາມສະຖຽນສູງສຸດໃນທຸກເວີຊັນຂອງ Library
        model = genai.GenerativeModel('gemini-pro')
        ai_ready = True
    else:
        ai_ready = False
        ai_error_msg = "ຫາ Key 'GEMINI_API_KEY' ບໍ່ເຫັນໃນ Settings/Secrets"
except Exception as e:
    ai_ready = False
    ai_error_msg = str(e)

# --- 2. ຕັ້ງຄ່າໜ້າຈໍ App ---
st.set_page_config(page_title="App ບັນຊີປ້າພອນສຸກ", layout="wide")
FILE_NAME = 'phonsouk_final_database_v3.csv'

# ຕົວນັບສຳລັບລ້າງຂໍ້ມູນໃນຊ່ອງ Input ຫຼັງບັນທຶກ
if 'clear_counter' not in st.session_state:
    st.session_state.clear_counter = 0

# --- 3. CSS ຕົບແຕ່ງ UI ໃຫ້ສວຍງາມ ---
st.markdown("""
<style>
    [data-testid="stMetricValue"] { color: #1B4F72 !important; font-size: 32px !important; font-weight: bold !important; }
    div[data-testid="stMetric"] { 
        background-color: #FFFFFF; 
        border: 2px solid #1B4F72; 
        padding: 15px; 
        border-radius: 10px; 
        box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
    }
    .ai-card { 
        background-color: #EBF5FB; 
        padding: 25px; 
        border-left: 10px solid #1B4F72; 
        border-radius: 10px; 
        color: #1B4F72; 
        font-size: 18px; 
        line-height: 1.8; 
    }
</style>
""", unsafe_allow_html=True)

# --- 4. ສ່ວນຫົວ Header ---
st.write("""
<div style="background-color: #1B4F72; padding: 25px; border-radius: 15px; text-align: center; color: white;">
    <h1 style="margin: 0;">🌸 ລະບົບບັນຊີ Super AI ປ້າພອນສຸກ </h1>
    <p style="margin: 5px 0;">ເບີໂທ: 020 99858310 | Line: Tarvan</p>
    <div style="font-size: 30px;">🌸 🇱🇦 🌸</div>
</div><br>
""", unsafe_allow_html=True)

# --- 5. ຟັງຊັນຊ່ວຍຈັດການຕົວເລກ ---
def parse_num(v):
    if not v: return 0
    nums = "".join(filter(str.isdigit, str(v)))
    return int(nums) if nums else 0

# --- 6. ສ່ວນການປ້ອນຂໍ້ມູນ ---
c1, c2 = st.columns(2)
with c1:
    st.success("### 🟢 ສ່ວນລາຍຮັບ")
    i1 = st.text_input("1. ເງິນເດືອນ", key=f"i1_{st.session_state.clear_counter}")
    i2 = st.text_input("2. ລາຍຮັບ Creator (FB/YT)", key=f"i2_{st.session_state.clear_counter}")
    i3 = st.text_input("3. ຂາຍຂອງຍ່ອຍ", key=f"i3_{st.session_state.clear_counter}")
    i4 = st.text_input("4. ຮັບຕັດຫຍິບ", key=f"i4_{st.session_state.clear_counter}")
    i5 = st.text_input("5. ຕູ້ກົດນ້ຳ/ຊັກຜ້າ", key=f"i5_{st.session_state.clear_counter}")

with c2:
    st.error("### 🔴 ສ່ວນລາຍຈ່າຍ")
    e1 = st.text_input("1. ຄ່າອາຫານ/ເຄື່ອງໃຊ້", key=f"e1_{st.session_state.clear_counter}")
    e2 = st.text_input("2. ຄ່າເຊົ່າ/ນ້ຳ-ໄຟ-ເນັດ", key=f"e2_{st.session_state.clear_counter}")
    e3 = st.text_input("3. ການສຶກສາລູກ", key=f"e3_{st.session_state.clear_counter}")
    e4 = st.text_input("4. ສ້າງເຮືອນ/ສ້ອມແປງ", key=f"e4_{st.session_state.clear_counter}")
    e5 = st.text_input("5. ຊື້ຂອງເຂົ້າຮ້ານ/ອື່ນໆ", key=f"e5_{st.session_state.clear_counter}")

if st.button("💾 ບັນທຶກຂໍ້ມູນທັງໝົດ", use_container_width=True):
    now_lao = datetime.now() + timedelta(hours=7)
    t_in = sum([parse_num(i1), parse_num(i2), parse_num(i3), parse_num(i4), parse_num(i5)])
    t_ex = sum([parse_num(e1), parse_num(e2), parse_num(e3), parse_num(e4), parse_num(e5)])
    
    if t_in > 0 or t_ex > 0:
        new_data = {
            'ວັນທີ': now_lao.strftime("%d/%m/%Y %H:%M"),
            'ລາຍຮັບລວມ': t_in,
            'ລາຍຈ່າຍລວມ': t_ex,
            'ເຫຼືອເກັບ': t_in - t_ex
        }
        pd.DataFrame([new_data]).to_csv(FILE_NAME, mode='a', index=False, header=not os.path.exists(FILE_NAME), encoding='utf-8-sig')
        st.session_state.clear_counter += 1
        st.success("✅ ບັນທຶກສຳເລັດແລ້ວ!")
        st.rerun()

# --- 7. ສະຫຼຸບຜົນ ແລະ ທີ່ປຶກສາ AI ---
if os.path.exists(FILE_NAME):
    df = pd.read_csv(FILE_NAME)
    st.markdown("---")
    st.subheader("📊 ສະຫຼຸບຜົນການເງິນທັງໝົດ")
    
    t_in = df['ລາຍຮັບລວມ'].sum()
    t_ex = df['ລາຍຈ່າຍລວມ'].sum()
    profit = t_in - t_ex
    
    c1, c2, c3 = st.columns(3)
    c1.metric("ລາຍຮັບສະສົມ", f"{t_in:,.0f} ກີບ")
    c2.metric("ລາຍຈ່າຍສະສົມ", f"{t_ex:,.0f} ກີບ")
    c3.metric("ເຫຼືອເກັບ/ກຳໄລ", f"{profit:,.0f} ກີບ")

    # ສ່ວນ AI ວິເຄາະ
    if ai_ready:
        if st.button("✨ ໃຫ້ AI ວິເຄາະບັນຊີໃຫ້ປ້າ", use_container_width=True):
            with st.spinner("🤖 AI ກຳລັງວິເຄາະຕົວເລກໃຫ້ປ້າ..."):
                try:
                    # ໃຊ້ຄຳສັ່ງແບບພື້ນຖານທີ່ສຸດ (ຕັດ RequestOptions ທີ່ເຮັດໃຫ້ Error ອອກ)
                    prompt = f"""
                    ເຈົ້າຄື CFO ທີ່ປຶກສາການເງິນຂອງປ້າພອນສຸກ. 
                    ຕົວເລກບັນຊີ: ລາຍຮັບ {t_in:,.0f} ກີບ, ລາຍຈ່າຍ {t_ex:,.0f} ກີບ, ກຳໄລ {profit:,.0f} ກີບ.
                    ຈົ່ງແນະນຳເປັນພາສາລາວ 3 ຂໍ້ສັ້ນໆ: ສະຫຼຸບພາບລວມ, ວິທີເພີ່ມລາຍຮັບ, ແລະ ຈຸດທີ່ຄວນປະຢັດ.
                    """
                    response = model.generate_content(prompt)
                    st.markdown(f'<div class="ai-card"><h3>🤖 ບົດວິເຄາະຈາກ AI</h3>{response.text}</div>', unsafe_allow_html=True)
                except Exception as ai_e:
                    st.error(f"AI ຕິດບັນຫາດ້ານເທັກນິກ: {ai_e}")
    else:
        st.warning(f"⚠️ AI ຍັງບໍ່ພ້ອມ: {ai_error_msg}")

    # ສະແດງປະຫວັດ 5 ລາຍການຫຼ້າສຸດ
    st.write("### 📅 ປະຫວັດການບັນທຶກ (5 ລາຍການຫຼ້າສຸດ)")
    st.table(df.tail(5))

    # ສ່ວນລຶບຂໍ້ມູນ
    with st.expander("🛠️ ຕັ້ງຄ່າ/ລົບຂໍ້ມູນ"):
        pwd = st.text_input("ໃສ່ລະຫັດ 9999 ເພື່ອລົບ:", type="password")
        if st.button("🗑️ ຢືນຢັນລົບຂໍ້ມູນທັງໝົດ"):
            if pwd == "9999" and os.path.exists(FILE_NAME):
                os.remove(FILE_NAME)
                st.success("ລົບຂໍ້ມູນແລ້ວ! ກະລຸນາ Refresh ໜ້າຈໍ.")
                st.rerun()
