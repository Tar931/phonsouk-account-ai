import streamlit as st
import pandas as pd
import os
from datetime import datetime, timedelta
from openai import OpenAI

# --- 1. ຕັ້ງຄ່າ DeepSeek AI (ເພີ່ມຄວາມສະຫຼາດດ້ວຍ Expert Prompt) ---
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
st.set_page_config(page_title="Super AI Account - ປ້າພອນສຸກ", layout="wide")
FILE_NAME = 'phonsouk_final_database_v3.csv'

if 'clear_counter' not in st.session_state:
    st.session_state.clear_counter = 0

# --- 3. CSS ຕົບແຕ່ງ (Dark Mode Gradient ຟ້າ-ມ່ວງ ທີ່ປ້າເລືອກ) ---
st.markdown("""
<style>
    .stApp { background-color: #050A18 !important; color: #FFFFFF !important; }
    
    /* Metric Cards ຕົວເລກສະຫຼຸບ */
    div[data-testid="stMetric"] {
        background: linear-gradient(135deg, #1A1F3C 0%, #0D1126 100%) !important;
        border: 1px solid #2E355E !important;
        border-radius: 20px !important;
        padding: 20px !important;
        box-shadow: 0 10px 20px rgba(0,0,0,0.4) !important;
    }
    div[data-testid="stMetricValue"] > div {
        background: linear-gradient(90deg, #BF5AF2 0%, #00EAFF 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 38px !important;
        font-weight: 800 !important;
    }
    div[data-testid="stMetricLabel"] > div { color: #A0AEC0 !important; }

    /* ປຸ່ມກົດ (Buttons) */
    .stButton > button {
        background: linear-gradient(90deg, #8A2BE2 0%, #BF5AF2 100%) !important;
        color: white !important;
        border-radius: 30px !important;
        padding: 12px 30px !important;
        font-weight: bold !important;
        width: 100% !important;
        box-shadow: 0 5px 15px rgba(138, 43, 226, 0.4) !important;
    }

    /* ກ່ອງ AI (ບົດວິເຄາະອັດສະລິຍະ) */
    .ai-card {
        background: linear-gradient(135deg, rgba(138, 43, 226, 0.15) 0%, rgba(0, 234, 255, 0.05) 100%) !important;
        border: 1px solid rgba(138, 43, 226, 0.4) !important;
        border-radius: 20px !important;
        padding: 30px !important;
        color: #E0E0E0 !important;
        line-height: 1.8 !important;
    }
    
    .stTextInput input { background-color: #1A1F3C !important; color: white !important; border-radius: 12px !important; }
</style>
""", unsafe_allow_html=True)

# --- 4. ສ່ວນຫົວ Header ---
st.write("""
<div style="background: linear-gradient(135deg, #1A1F3C 0%, #050A18 100%); padding: 35px; border-radius: 25px; border: 1px solid #2E355E; text-align: center; margin-bottom: 25px;">
    <h1 style="margin: 0; background: linear-gradient(90deg, #BF5AF2 0%, #00EAFF 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 40px;">🌸 ລະບົບບັນຊີ Super AI ປ້າພອນສຸກ</h1>
    <p style="color: #A0AEC0; font-size: 18px; margin-top: 10px;">ທີ່ປຶກສາການເງິນອັດສະລິຍະ (DeepSeek Intelligent Core)</p>
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
    return st.text_input(label, key=actual_key)

# --- 5. ສ່ວນປ້ອນຂໍ້ມູນ (ລາຍຮັບ 7 / ລາຍຈ່າຍ 11) ---
c1, c2 = st.columns(2)
with c1:
    st.markdown("#### <span style='color: #00EAFF;'>🟢 ລາຍຮັບ (Income)</span>", unsafe_allow_html=True)
    i1 = input_box("1. ຮັບເງິນເດືອນ", "i1"); i2 = input_box("2. Creator (FB/YT)", "i2"); i3 = input_box("3. ຂາຍຂອງຍ່ອຍ", "i3")
    i4 = input_box("4. ຮັບຕັດຫຍິບ", "i4"); i5 = input_box("5. ຕູ້ກົດນ້ຳ", "i5"); i6 = input_box("6. ຕູ້ຊັກຜ້າ", "i6"); i7 = input_box("7. ອື່ນໆ", "i7")

with c2:
    st.markdown("#### <span style='color: #FF00E6;'>🔴 ລາຍຈ່າຍ (Expenses)</span>", unsafe_allow_html=True)
    e1 = input_box("1. ອາຫານ & ບໍລິໂພກ", "e1"); e2 = input_box("2. ຄ່າເຊົ່າທີ່ຢູ່", "e2"); e3 = input_box("3. ນ້ຳ-ໄຟ-ເນັດ", "e3")
    e4 = input_box("4. ຄ່າເດີນທາງ", "e4"); e5 = input_box("5. ການສຶກສາ", "e5"); e6 = input_box("6. ຄ່າປິ່ນປົວ", "e6")
    e7 = input_box("7. ຄ່າເສື້ອຜ້າ", "e7"); e8 = input_box("8. ບັນເທີງ", "e8"); e9 = input_box("9. ຫວຍ", "e9")
    e10 = input_box("10. ສ້າງເຮືອນ", "e10"); e11 = input_box("11. ຊື້ຂອງເຂົ້າຮ້ານ", "e11")

st.write("<br>", unsafe_allow_html=True)

# --- 6. ປຸ່ມບັນທຶກ ພ້ອມລະບົບຢືນຢັນ "ຕົກລົງ" ---
if st.button("🚀 ປະມວນຜົນ ແລະ ບັນທຶກຂໍ້ມູນ"):
    v_i = [parse_num(i1), parse_num(i2), parse_num(i3), parse_num(i4), parse_num(i5), parse_num(i6), parse_num(i7)]
    v_e = [parse_num(e1), parse_num(e2), parse_num(e3), parse_num(e4), parse_num(e5), parse_num(e6), parse_num(e7), parse_num(e8), parse_num(e9), parse_num(e10), parse_num(e11)]
    t_in, t_ex = sum(v_i), sum(v_e)
    
    if t_in == 0 and t_ex == 0:
        st.warning("⚠️ ກະລຸນາປ້ອນຂໍ້ມູນກ່ອນ!")
    else:
        st.warning(f"📋 **ກວດສອບກ່ອນບັນທຶກ:** ລາຍຮັບ: {t_in:,.0f} | ລາຍຈ່າຍ: {t_ex:,.0f}")
        if st.button("✅ ຕົກລົງ, ບັນທຶກເລີຍ!"):
            now_lao = datetime.now() + timedelta(hours=7) 
            new_data = {
                'ວັນທີ': now_lao.strftime("%d/%m/%Y %H:%M"), 
                'ລາຍຮັບລວມ': t_in, 'ລາຍຈ່າຍລວມ': t_ex, 'ເຫຼືອເກັບ': t_in - t_ex,
                'ເງິນເດືອນ': v_i[0], 'Creator': v_i[1], 'ຂາຍຂອງ': v_i[2], 'ຫຍິບຜ້າ': v_i[3], 'ຕູ້ກົດນ້ຳ': v_i[4], 'ຕູ້ຊັກຜ້າ': v_i[5], 'ຮັບອື່ນໆ': v_i[6],
                'ອາຫານ': v_e[0], 'ຄ່າເຊົ່າ': v_e[1], 'ນ້ຳໄຟ': v_e[2], 'ເດີນທາງ': v_e[3], 'ການສຶກສາ': v_e[4], 'ຢາ': v_e[5], 'ເສື້ອຜ້າ': v_e[6], 'ບັນເທີງ': v_e[7], 'ຫວຍ': v_e[8], 'ສ້າງເຮືອນ': v_e[9], 'ຊື້ຂອງເຂົ້າຮ້ານ': v_e[10]
            }
            pd.DataFrame([new_data]).to_csv(FILE_NAME, mode='a', index=False, header=not os.path.exists(FILE_NAME), encoding='utf-8-sig')
            st.session_state.clear_counter += 1
            st.rerun()

# --- 7. ລາຍງານ (ມື້ນີ້, ອາທິດນີ້, ເດືອນນີ້, ປີນີ້) ---
if os.path.exists(FILE_NAME):
    df = pd.read_csv(FILE_NAME)
    st.markdown("---")
    
    option = st.radio("ເລືອກໄລຍະເວລາລາຍງານ:", ["ມື້ນີ້", "ອາທິດນີ້", "ເດືອນນີ້", "ປີນີ້"], horizontal=True)
    df['Date_Obj'] = pd.to_datetime(df['ວັນທີ'], format="%d/%m/%Y %H:%M")
    now = datetime.now()
    
    if option == "ມື້ນີ້": filtered_df = df[df['Date_Obj'].dt.date == now.date()]
    elif option == "ອາທິດນີ້": filtered_df = df[df['Date_Obj'].dt.isocalendar().week == now.isocalendar()[1]]
    elif option == "ເດືອນນີ້": filtered_df = df[df['Date_Obj'].dt.month == now.month]
    else: filtered_df = df[df['Date_Obj'].dt.year == now.year]

    if not filtered_df.empty:
        t_in_sum, t_ex_sum = filtered_df['ລາຍຮັບລວມ'].sum(), filtered_df['ລາຍຈ່າຍລວມ'].sum()
        profit = t_in_sum - t_ex_sum
        
        c1, c2, c3 = st.columns(3)
        c1.metric(f"ລາຍຮັບ {option}", f"{t_in_sum:,.0f} ກີບ")
        c2.metric(f"ລາຍຈ່າຍ {option}", f"{t_ex_sum:,.0f} ກີບ")
        c3.metric(f"ເຫຼືອເກັບສຸດທິ", f"{profit:,.0f} ກີບ")

        if ai_ready:
            st.write("<br>", unsafe_allow_html=True)
            if st.button("🧠 ເປີດໃຊ້ທີ່ປຶກສາ AI DeepSeek (ວິເຄາະຂັ້ນສູງ)"):
                with st.spinner("🤖 AI ກຳລັງວິເຄາະຖານຂໍ້ມູນ..."):
                    try:
                        response = client.chat.completions.create(
                            model="deepseek-chat",
                            messages=[
                                {"role": "system", "content": "ເຈົ້າຄື CFO ທີ່ປຶກສາການເງິນມືອາຊີບ. ວິເຄາະຕົວເລກຂອງປ້າພອນສຸກຢ່າງລະອຽດ. ຕອບເປັນພາສາລາວ ແບ່ງເປັນ: ສະຫຼຸບ, ຈຸດຄວນລະວັງ, ແລະ ໄອເດຍເພີ່ມເງິນ."},
                                {"role": "user", "content": f"ຂໍ້ມູນ {option}: ຮັບ {t_in_sum:,.0f}, ຈ່າຍ {t_ex_sum:,.0f}, ເຫຼືອ {profit:,.0f}. ວິເຄາະໃຫ້ສະຫຼາດທີ່ສຸດ."},
                            ]
                        )
                        st.markdown(f'<div class="ai-card"><h3>🧠 ບົດວິເຄາະອັດສະລິຍະ</h3>{response.choices[0].message.content}</div>', unsafe_allow_html=True)
                    except Exception as e: st.error(f"Error AI: {e}")

    # --- 8. ຕາຕະລາງປະຫວັດ ---
    st.markdown("---")
    st.write("### 📅 ປະຫວັດການບັນທຶກ (10 ລາຍການຫຼ້າສຸດ)")
    view_df = df.drop(columns=['Date_Obj'], errors='ignore')
    num_cols = view_df.select_dtypes(include=['number']).columns.tolist()
    st.dataframe(view_df.tail(10).style.format(subset=num_cols, formatter="{:,.0f}"), use_container_width=True)

    with st.expander("🛠️ ຈັດການຖານຂໍ້ມູນ"):
        if st.text_input("ລະຫັດຢືນຢັນ", type="password") == "9999":
            if st.button("🗑️ ລຶບຂໍ້ມູນທັງໝົດ"):
                os.remove(FILE_NAME); st.rerun()
