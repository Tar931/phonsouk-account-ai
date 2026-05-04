import streamlit as st
import pandas as pd
import os
from datetime import datetime, timedelta
from openai import OpenAI

# --- 1. ຕັ້ງຄ່າ DeepSeek AI (Smart Config) ---
ai_error_msg = ""
try:
    if "DEEPSEEK_API_KEY" in st.secrets:
        client = OpenAI(
            api_key=st.secrets["DEEPSEEK_API_KEY"],
            base_url="https://api.deepseek.com"
        )
        ai_ready = True
    else:
        ai_ready = False
        ai_error_msg = "ຫາ Key 'DEEPSEEK_API_KEY' ບໍ່ເຫັນໃນ Secrets"
except Exception as e:
    ai_ready = False
    ai_error_msg = str(e)

# --- 2. ຕັ້ງຄ່າໜ້າຈໍ ---
st.set_page_config(page_title="Super AI Account Pro - ປ້າພອນສຸກ", layout="wide")
FILE_NAME = 'phonsouk_final_database_v3.csv'

if 'clear_counter' not in st.session_state:
    st.session_state.clear_counter = 0

# --- 3. CSS ຕົບແຕ່ງ (Premium Dark Theme) ---
st.markdown("""
<style>
    .stApp { background-color: #050A18 !important; color: #FFFFFF !important; }
    
    /* ກ່ອງ Metric ໃຫ້ເບິ່ງມີມິຕິ */
    div[data-testid="stMetric"] {
        background: linear-gradient(135deg, #1A1F3C 0%, #0D1126 100%) !important;
        border: 1px solid #3498DB !important;
        border-radius: 20px !important;
        padding: 25px !important;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37) !important;
    }
    
    /* ຕົວເລກ Gradient */
    div[data-testid="stMetricValue"] > div {
        background: linear-gradient(90deg, #BF5AF2 0%, #00EAFF 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 42px !important;
        font-weight: 800 !important;
    }

    /* ປຸ່ມບັນທຶກ ແລະ ປຸ່ມ AI */
    .stButton > button {
        background: linear-gradient(90deg, #6C5CE7 0%, #A29BFE 100%) !important;
        color: white !important;
        border-radius: 50px !important;
        border: none !important;
        padding: 15px 30px !important;
        font-weight: bold !important;
        width: 100% !important;
        transition: 0.5s !important;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    .stButton > button:hover {
        transform: scale(1.02) !important;
        box-shadow: 0 0 20px rgba(108, 92, 231, 0.6) !important;
    }

    /* ກ່ອງ AI (ບົດວິເຄາະທີ່ສະຫຼາດ) */
    .ai-card {
        background: rgba(26, 31, 60, 0.8) !important;
        backdrop-filter: blur(10px);
        border: 1px solid #BF5AF2 !important;
        border-radius: 25px !important;
        padding: 35px !important;
        color: #F0F0F0 !important;
        line-height: 1.9 !important;
        font-size: 18px !important;
        box-shadow: 0 10px 50px rgba(0,0,0,0.5) !important;
    }
    
    .stTextInput input {
        background-color: #1A1F3C !important;
        color: white !important;
        border-radius: 15px !important;
        border: 1px solid #2E355E !important;
    }
</style>
""", unsafe_allow_html=True)

# --- 4. ສ່ວນຫົວ Header ---
st.write("""
<div style="background: linear-gradient(135deg, #1A1F3C 0%, #050A18 100%); padding: 40px; border-radius: 30px; border: 1px solid #3498DB; text-align: center; margin-bottom: 30px;">
    <h1 style="margin: 0; background: linear-gradient(90deg, #A29BFE 0%, #6C5CE7 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 50px; font-weight: 900;">🌸 Super AI Pro ປ້າພອນສຸກ</h1>
    <p style="color: #A0AEC0; font-size: 20px; margin-top: 15px;">ລະບົບວາງແຜນການເງິນອັດສະລິຍະ (DeepSeek Intelligent Core)</p>
</div>
""", unsafe_allow_html=True)

# --- Helpers ---
def parse_num(v):
    if not v: return 0
    nums = "".join(filter(str.isdigit, str(v)))
    return int(nums) if nums else 0

def format_num(v):
    if not v: return ""
    nums = "".join(filter(str.isdigit, str(v)))
    return "{:,}".format(int(nums)) if nums else ""

def input_box(label, base_key):
    actual_key = f"{base_key}_{st.session_state.clear_counter}"
    if actual_key not in st.session_state:
        st.session_state[actual_key] = ""
    return st.text_input(label, key=actual_key, on_change=lambda: None)

# --- 5. ປ້ອນຂໍ້ມູນ ---
c1, c2 = st.columns(2)
with c1:
    st.markdown("### <span style='color: #00EAFF;'>💰 ລາຍຮັບ (Income)</span>", unsafe_allow_html=True)
    i1 = input_box("💵 ເງິນເດືອນ", "i1")
    i2 = input_box("📱 Creator (FB/YT)", "i2")
    i3 = input_box("🛍️ ຂາຍຂອງຍ່ອຍ", "i3")
    i4 = input_box("🧵 ຕັດຫຍິບ", "i4")
    i5 = input_box("💧 ຕູ້ກົດນ້ຳ", "i5")
    i6 = input_box("🧺 ຕູ້ຊັກຜ້າ", "i6")
    i7 = input_box("➕ ອື່ນໆ", "i7")

with c2:
    st.markdown("### <span style='color: #FF7675;'>💸 ລາຍຈ່າຍ (Expenses)</span>", unsafe_allow_html=True)
    e1 = input_box("🍱 ອາຫານ & ເຄື່ອງໃຊ້", "e1")
    e2 = input_box("🏠 ຄ່າເຊົ່າ & ທີ່ຢູ່", "e2")
    e3 = input_box("🔌 ນ້ຳ-ໄຟ-ເນັດ", "e3")
    e4 = input_box("🚗 ເດີນທາງ", "e4")
    e5 = input_box("🎓 ການສຶກສາ", "e5")
    e6 = input_box("💊 ຄ່າປິ່ນປົວ", "e6")
    e7 = input_box("👕 ເສື້ອຜ້າ", "e7")
    e8 = input_box("🍿 ບັນເທີງ", "e8")
    e9 = input_box("🎰 ຫວຍ", "e9")
    e10 = input_box("🏗️ ສ້າງເຮືອນ", "e10")
    e11 = input_box("📦 ຊື້ຂອງເຂົ້າຮ້ານ", "e11")

st.write("<br>", unsafe_allow_html=True)

# --- 6. ປຸ່ມຢືນຢັນການບັນທຶກ ---
if st.button("🚀 ປະມວນຜົນ ແລະ ບັນທຶກຂໍ້ມູນ"):
    v_i = [parse_num(i1), parse_num(i2), parse_num(i3), parse_num(i4), parse_num(i5), parse_num(i6), parse_num(i7)]
    v_e = [parse_num(e1), parse_num(e2), parse_num(e3), parse_num(e4), parse_num(e5), parse_num(e6), parse_num(e7), parse_num(e8), parse_num(e9), parse_num(e10), parse_num(e11)]
    t_in, t_ex = sum(v_i), sum(v_e)
    
    if t_in == 0 and t_ex == 0:
        st.warning("⚠️ ກະລຸນາປ້ອນຂໍ້ມູນກ່ອນ!")
    else:
        st.info(f"📊 **ກວດສອບ:** ຮັບ {t_in:,.0f} | ຈ່າຍ {t_ex:,.0f} | ເຫຼືອ {t_in-t_ex:,.0f}")
        if st.button("✅ ຢືນຢັນ 'ຕົກລົງ' ບັນທຶກ"):
            now_lao = datetime.now() + timedelta(hours=7) 
            new_data = {
                'ວັນທີ': now_lao.strftime("%d/%m/%Y %H:%M"), 
                'ລາຍຮັບລວມ': t_in, 'ລາຍຈ່າຍລວມ': t_ex, 'ເຫຼືອເກັບ': t_in - t_ex,
                'ເງິນເດືອນ': v_i[0], 'Creator': v_i[1], 'ຂາຍຂອງ': v_i[2], 'ຫຍິບຜ້າ': v_i[3], 'ຕູ້ກົດນ້ຳ': v_i[4], 'ຕູ້ຊັກຜ້າ': v_i[5], 'ຮັບອື່ນໆ': v_i[6],
                'ອາຫານ': v_e[0], 'ຄ່າເຊົ່າ': v_e[1], 'ນ້ຳໄຟ': v_e[2], 'ເດີນທາງ': v_e[3], 'ການສຶກສາ': v_e[4], 'ຢາ': v_e[5], 'ເສື້ອຜ້າ': v_e[6], 'ບັນເທີງ': v_e[7], 'ຫວຍ': v_e[8], 'ສ້າງເຮືອນ': v_e[9], 'ຊື້ຂອງເຂົ້າຮ້ານ': v_e[10]
            }
            pd.DataFrame([new_data]).to_csv(FILE_NAME, mode='a', index=False, header=not os.path.exists(FILE_NAME), encoding='utf-8-sig')
            st.session_state.clear_counter += 1
            st.success("✨ ລະບົບໄດ້ບັນທຶກ ແລະ ອັບເດດຖານຂໍ້ມູນແລ້ວ!")
            st.rerun()

# --- 7. Dashboard & AI Intelligence ---
if os.path.exists(FILE_NAME):
    df = pd.read_csv(FILE_NAME)
    st.markdown("---")
    
    option = st.radio("ຄັດກອງຂໍ້ມູນ:", ["ທັງໝົດ", "ເດືອນນີ້", "ອາທິດນີ້", "ມື້ນີ້"], horizontal=True)
    df['Date_Obj'] = pd.to_datetime(df['ວັນທີ'], format="%d/%m/%Y %H:%M")
    now = datetime.now()
    if option == "ມື້ນີ້": f_df = df[df['Date_Obj'].dt.date == now.date()]
    elif option == "ອາທິດນີ້": f_df = df[df['Date_Obj'].dt.isocalendar().week == now.isocalendar()[1]]
    elif option == "ເດືອນນີ້": f_df = df[df['Date_Obj'].dt.month == now.month]
    else: f_df = df

    if not f_df.empty:
        t_in_sum, t_ex_sum = f_df['ລາຍຮັບລວມ'].sum(), f_df['ລາຍຈ່າຍລວມ'].sum()
        profit = t_in_sum - t_ex_sum
        
        col1, col2, col3 = st.columns(3)
        col1.metric("ລາຍຮັບລວມ", f"{t_in_sum:,.0f} ກີບ")
        col2.metric("ລາຍຈ່າຍລວມ", f"{t_ex_sum:,.0f} ກີບ")
        col3.metric("ເຫຼືອເກັບສຸດທິ", f"{profit:,.0f} ກີບ")

        if ai_ready:
            st.write("<br>", unsafe_allow_html=True)
            if st.button("🤖 ເປີດໃຊ້ງານທີ່ປຶກສາ AI DeepSeek (ວິເຄາະຂັ້ນສູງ)"):
                with st.spinner("🧠 AI ກຳລັງປະມວນຜົນຖານຂໍ້ມູນຂະໜາດໃຫຍ່..."):
                    try:
                        # --- ສັ່ງໃຫ້ AI ສະຫຼາດທີ່ສຸດດ້ວຍ Advanced Prompt ---
                        response = client.chat.completions.create(
                            model="deepseek-chat",
                            messages=[
                                {"role": "system", "content": """ເຈົ້າຄືທີ່ປຶກສາການເງິນລະດັບໂລກ ແລະ CFO ມືອາຊີບ. 
                                ພາລະກິດ: ວິເຄາະຕົວເລກຂອງປ້າພອນສຸກ ໃຫ້ລະອຽດ, ຊອກຫາຈຸດບົກຜ່ອງ, ແລະ ວາງແຜນການເຕີບໂຕ.
                                ວິທີຕອບ: ໃຊ້ພາສາລາວທີ່ສຸພາບ, ອ່ານງ່າຍ, ແຕ່ມີຂໍ້ມູນແໜ້ນ. 
                                ໃຫ້ແບ່ງເປັນ 4 ພາກ: 
                                1. 📈 ສະຫຼຸບສຸຂະພາບການເງິນ (ດີ ຫຼື ຄວນລະວັງ). 
                                2. 🔍 ຈຸດທີ່ຄວນປະຢັດ (ວິເຄາະຈາກລາຍຈ່າຍທີ່ປ້ານຳເຂົ້າ). 
                                3. 💡 ກົນຍຸດເພີ່ມລາຍຮັບ (ຈາກ Creator, ຕູ້ກົດນ້ຳ, ຫຼື ຕັດຫຍິບ). 
                                4. 🎯 ເປົ້າໝາຍໃນອະນາຄົດ (ການສ້າງເຮືອນ ແລະ ການອອມ)."""},
                                {"role": "user", "content": f"ຂໍ້ມູນບັນຊີ {option}: ລາຍຮັບ {t_in_sum:,.0f} ກີບ, ລາຍຈ່າຍ {t_ex_sum:,.0f} ກີບ, ເຫຼືອ {profit:,.0f} ກີບ. ລາຍຈ່າຍສ່ວນໃຫຍ່ແມ່ນມາຈາກຊ່ອງທາງທີ່ປ້ານຳເຂົ້າ."},
                            ]
                        )
                        st.markdown(f'<div class="ai-card"><h3>🧠 ບົດວິເຄາະອັດສະລິຍະ ຈາກ DeepSeek Pro</h3>{response.choices[0].message.content}</div>', unsafe_allow_html=True)
                    except Exception as e: st.error(f"Error AI: {e}")

    # --- 8. History & Management ---
    st.markdown("---")
    st.write("### 📅 ປະຫວັດການບັນທຶກ (Detailed Logs)")
    view_df = df.drop(columns=['Date_Obj'], errors='ignore')
    num_cols = view_df.select_dtypes(include=['number']).columns.tolist()
    st.dataframe(view_df.tail(15).style.format(subset=num_cols, formatter="{:,.0f}"), use_container_width=True)

    with st.expander("🛠️ ການຈັດການລະບົບຂັ້ນສູງ"):
        if st.text_input("ລະຫັດຄວາມປອດໄພ", type="password") == "9999":
            if st.button("🗑️ ລ້າງຖານຂໍ້ມູນທັງໝົດ"):
                os.remove(FILE_NAME)
                st.rerun()
