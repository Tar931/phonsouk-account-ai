import streamlit as st
import pandas as pd
import os
from datetime import datetime, timedelta
from openai import OpenAI

# --- 1. ຕັ້ງຄ່າ DeepSeek AI ---
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
st.set_page_config(page_title="App ບັນຊີ Super AI ປ້າພອນສຸກ", layout="wide")
FILE_NAME = 'phonsouk_final_database_v3.csv'

if 'clear_counter' not in st.session_state:
    st.session_state.clear_counter = 0

# --- 3. CSS ຕົບແຕ່ງສີທີມໃຫມ່ (Dark Mode Blue-Purple Gradient) ---
st.markdown("""
<style>
    /* ພື້ນຫຼັງແອັບທັງໝົດ */
    .stApp {
        background-color: #050A18 !important;
        color: #FFFFFF !important;
    }
    
    /* ຕົບແຕ່ງກ່ອງ Metric (ກ່ອງຕົວເລກສະຫຼຸບ) */
    div[data-testid="stMetric"] {
        background: linear-gradient(135deg, #1A1F3C 0%, #0D1126 100%) !important;
        border: 1px solid #2E355E !important;
        border-radius: 20px !important;
        padding: 20px !important;
        box-shadow: 0 10px 20px rgba(0,0,0,0.4) !important;
    }
    
    /* ສີຕົວເລກ Metric ໃຫ້ເປັນສີ Gradient ຟ້າ-ມ່ວງ */
    div[data-testid="stMetricValue"] > div {
        background: linear-gradient(90deg, #BF5AF2 0%, #00EAFF 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 38px !important;
        font-weight: 800 !important;
    }
    
    div[data-testid="stMetricLabel"] > div {
        color: #A0AEC0 !important;
        font-size: 16px !important;
    }

    /* ຕົບແຕ່ງປຸ່ມ (Buttons) */
    .stButton > button {
        background: linear-gradient(90deg, #8A2BE2 0%, #BF5AF2 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 30px !important;
        padding: 12px 30px !important;
        font-weight: bold !important;
        width: 100% !important;
        box-shadow: 0 5px 15px rgba(138, 43, 226, 0.4) !important;
        transition: 0.3s !important;
    }
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 20px rgba(138, 43, 226, 0.6) !important;
    }

    /* ຕົບແຕ່ງຊ່ອງ Input */
    .stTextInput > div > div > input {
        background-color: #1A1F3C !important;
        color: white !important;
        border: 1px solid #2E355E !important;
        border-radius: 12px !important;
    }

    /* ຕົບແຕ່ງກ່ອງ AI CFO */
    .ai-card {
        background: linear-gradient(135deg, rgba(138, 43, 226, 0.15) 0%, rgba(0, 234, 255, 0.05) 100%) !important;
        border: 1px solid rgba(138, 43, 226, 0.4) !important;
        border-radius: 20px !important;
        padding: 25px !important;
        color: #E0E0E0 !important;
        line-height: 1.8 !important;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5) !important;
    }

    /* ຕົບແຕ່ງຕາຕະລາງ */
    .stDataFrame {
        background-color: #1A1F3C !important;
        border-radius: 15px !important;
    }

    /* ຫົວຂໍ້ Subheader */
    h3 {
        color: #00EAFF !important;
    }
</style>
""", unsafe_allow_html=True)

# --- 4. ສ່ວນຫົວ Header ---
st.write("""
<div style="background: linear-gradient(135deg, #1A1F3C 0%, #050A18 100%); padding: 30px; border-radius: 25px; border: 1px solid #2E355E; text-align: center; margin-bottom: 25px;">
    <h1 style="margin: 0; background: linear-gradient(90deg, #BF5AF2 0%, #00EAFF 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 40px;">🌸 ລະບົບບັນຊີ Super AI ປ້າພອນສຸກ</h1>
    <p style="color: #A0AEC0; font-size: 16px; margin-top: 10px;">ຈັດການການເງິນດ້ວຍລະບົບ DeepSeek AI ທັນສະໄໝ</p>
</div>
""", unsafe_allow_html=True)

# --- ຟັງຊັນຊ່ວຍ (Helpers) ---
def format_num(v):
    if not v: return ""
    nums = "".join(filter(str.isdigit, str(v)))
    return "{:,}".format(int(nums)) if nums else ""

def parse_num(v):
    if not v: return 0
    nums = "".join(filter(str.isdigit, str(v)))
    return int(nums) if nums else 0

def update_val(key):
    st.session_state[key] = format_num(st.session_state[key])

def input_box(label, base_key):
    actual_key = f"{base_key}_{st.session_state.clear_counter}"
    if actual_key not in st.session_state:
        st.session_state[actual_key] = ""
    return st.text_input(label, key=actual_key, on_change=update_val, args=(actual_key,))

# --- 5. ສ່ວນປ້ອນຂໍ້ມູນ ---
c1, c2 = st.columns(2)
with c1:
    st.markdown("#### <span style='color: #00EAFF;'>🟢 ສ່ວນລາຍຮັບ</span>", unsafe_allow_html=True)
    i1_v = input_box("1. ຮັບເງິນເດືອນ", "i1")
    i2_v = input_box("2. ລາຍຮັບ Creator (FB/YT)", "i2")
    i3_v = input_box("3. ລາຍຮັບຂາຍຂອງຍ່ອຍ", "i3")
    i4_v = input_box("4. ລາຍຮັບຕັດຫຍິບ", "i4")
    i5_v = input_box("5. ລາຍຮັບຕູ້ກົດນ້ຳ/ຊັກຜ້າ", "i5")
    i6_v = input_box("6. ລາຍຮັບອື່ນໆ", "i6")

with c2:
    st.markdown("#### <span style='color: #FF00E6;'>🔴 ສ່ວນລາຍຈ່າຍ</span>", unsafe_allow_html=True)
    e1_v = input_box("1. ຄ່າອາຫານ & ບໍລິໂພກ", "e1")
    e2_v = input_box("2. ຄ່ານ້ຳ-ໄຟ-ເນັດ-ຄ່າເຊົ່າ", "e2")
    e3_v = input_box("3. ການສຶກສາ/ປິ່ນປົວ", "e3")
    e4_v = input_box("4. ສ້າງເຮືອນ/ສ້ອມແປງ", "e4")
    e5_v = input_box("5. ຊື້ຂອງເຂົ້າຮ້ານ/ອື່ນໆ", "e5")

st.write("<br>", unsafe_allow_html=True)
if st.button("💾 ບັນທຶກຂໍ້ມູນທັງໝົດ"):
    now_lao = datetime.now() + timedelta(hours=7) 
    v_i = [parse_num(i1_v), parse_num(i2_v), parse_num(i3_v), parse_num(i4_v), parse_num(i5_v), parse_num(i6_v)]
    v_e = [parse_num(e1_v), parse_num(e2_v), parse_num(e3_v), parse_num(e4_v), parse_num(e5_v)]
    t_in, t_ex = sum(v_i), sum(v_e)
    
    if t_in > 0 or t_ex > 0:
        new_data = {
            'ວັນທີ': now_lao.strftime("%d/%m/%Y %H:%M"), 
            'ລາຍຮັບລວມ': t_in, 'ລາຍຈ່າຍລວມ': t_ex, 'ເຫຼືອເກັບ': t_in - t_ex,
            'ເງິນເດືອນ': v_i[0], 'Creator': v_i[1], 'ຂາຍຂອງ': v_i[2], 'ຫຍິບຜ້າ': v_i[3], 'ຕູ້ກົດນ້ຳ': v_i[4],
            'ອາຫານ': v_e[0], 'ຄ່າເຊົ່າ_ນ້ຳໄຟ': v_e[1], 'ການສຶກສາ': v_e[2], 'ສ້າງເຮືອນ': v_e[3], 'ຊື້ຂອງເຂົ້າຮ້ານ': v_e[4]
        }
        pd.DataFrame([new_data]).to_csv(FILE_NAME, mode='a', index=False, header=not os.path.exists(FILE_NAME), encoding='utf-8-sig')
        st.session_state.clear_counter += 1
        st.success("✅ ບັນທຶກສຳເລັດແລ້ວ!")
        st.rerun()

# --- 6. ສະແດງຜົນ Dashboard & AI ວິເຄາະ ---
if os.path.exists(FILE_NAME):
    df = pd.read_csv(FILE_NAME)
    st.markdown("---")
    
    option = st.radio("ໄລຍະເວລາ:", ["ມື້ນີ້", "ອາທິດນີ້", "ເດືອນນີ້", "ທັງໝົດ"], horizontal=True)
    df['Date_Obj'] = pd.to_datetime(df['ວັນທີ'], format="%d/%m/%Y %H:%M")
    now = datetime.now()
    if option == "ມື້ນີ້": filtered_df = df[df['Date_Obj'].dt.date == now.date()]
    elif option == "ອາທິດນີ້": filtered_df = df[df['Date_Obj'].dt.isocalendar().week == now.isocalendar()[1]]
    elif option == "ເດືອນນີ້": filtered_df = df[df['Date_Obj'].dt.month == now.month]
    else: filtered_df = df

    if not filtered_df.empty:
        t_in, t_ex = filtered_df['ລາຍຮັບລວມ'].sum(), filtered_df['ລາຍຈ່າຍລວມ'].sum()
        profit = t_in - t_ex
        
        c1, c2, c3 = st.columns(3)
        c1.metric(f"ລາຍຮັບ {option}", f"{t_in:,.0f} ກີບ")
        c2.metric(f"ລາຍຈ່າຍ {option}", f"{t_ex:,.0f} ກີບ")
        c3.metric(f"ເຫຼືອເກັບສຸດທິ", f"{profit:,.0f} ກີບ")

        if ai_ready:
            st.write("<br>", unsafe_allow_html=True)
            if st.button("✨ ໃຫ້ DeepSeek AI ວິເຄາະ ແລະ ວາງແຜນການເງິນ"):
                with st.spinner("🤖 DeepSeek ກຳລັງວິເຄາະຕົວເລກ..."):
                    try:
                        response = client.chat.completions.create(
                            model="deepseek-chat",
                            messages=[
                                {"role": "system", "content": "ເຈົ້າຄື CFO ທີ່ປຶກສາການເງິນຂອງປ້າພອນສຸກ. ຕອບເປັນພາສາລາວ."},
                                {"role": "user", "content": f"ວິເຄາະບັນຊີ: ຮັບ {t_in}, ຈ່າຍ {t_ex}, ເຫຼືອ {profit}. ແນະນຳ 3 ຫົວຂໍ້: ສະຫຼຸບ, ວິທີເພີ່ມເງິນ, ຈຸດທີ່ຄວນລະວັງ."},
                            ]
                        )
                        st.markdown(f'<div class="ai-card"><h3>🤖 ບົດວິເຄາະຈາກ DeepSeek AI</h3>{response.choices[0].message.content}</div>', unsafe_allow_html=True)
                    except Exception as e:
                        st.error(f"Error AI: {e}")

    # --- 7. ຕາຕະລາງປະຫວັດ ---
    st.markdown("---")
    st.write("### 📅 ປະຫວັດການເງິນແບບລະອຽດ")
    view_df = df.drop(columns=['Date_Obj'], errors='ignore')
    num_cols = view_df.select_dtypes(include=['number']).columns.tolist()
    st.dataframe(view_df.tail(10).style.format(subset=num_cols, formatter="{:,.0f}"), use_container_width=True)

    with st.expander("🛠️ ຈັດການຖານຂໍ້ມູນ"):
        if st.text_input("ລະຫັດຢືນຢັນ", type="password") == "9999":
            if st.button("🗑️ ລຶບຂໍ້ມູນທັງໝົດ"):
                os.remove(FILE_NAME)
                st.rerun()
