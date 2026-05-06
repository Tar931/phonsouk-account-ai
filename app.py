import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from openai import OpenAI  
from streamlit_gsheets import GSheetsConnection 

# --- 1. ຕັ້ງຄ່າ AI ---
st.set_page_config(page_title="App ບັນຊີຂອງປ້າພອນສຸກ", layout="wide")

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

# --- 2. ຕັ້ງຄ່າເຊື່ອມຕໍ່ Google Sheets ---
conn = st.connection("gsheets", type=GSheetsConnection)

# 🔴🔴 ປ່ຽນ Link ລຸ່ມນີ້ເປັນ Link ຂອງ Google Sheets ຂອງເຈົ້າເອງ (ເອົາມາຈາກ Browser) 🔴🔴
"SHEET_URL = "https://docs.google.com/spreadsheets/d/1XyZabcd1234/edit"" 

if 'clear_counter' not in st.session_state:
    st.session_state.clear_counter = 0

# ກຳນົດຫົວຂໍ້ຖັນຂອງຕະລາງ
COLUMNS = ['ວັນທີ', 'ລາຍຮັບລວມ', 'ລາຍຈ່າຍລວມ', 'ເຫຼືອເກັບ', 'ເງິນເດືອນ', 'Creator', 'ຂາຍຂອງ', 'ຫຍິບຜ້າ', 'ຕູ້ກົດນ້ຳ', 'ຕູ້ຊັກຜ້າ', 'ຮັບອື່ນໆ', 'ອາຫານ', 'ຄ່າເຊົ່າ', 'ນ້ຳໄຟ', 'ເດີນທາງ', 'ການສຶກສາ', 'ຢາ', 'ເສື້ອຜ້າ', 'ບັນເທີງ', 'ຫວຍ', 'ສ້າງເຮືອນ', 'ຊື້ຂອງເຂົ້າຮ້ານ']

# --- 3. CSS ຕົບແຕ່ງ UI ---
st.markdown("""
<style>
    .stApp { background-color: #050A18 !important; color: #FFFFFF !important; }
    div[data-testid="stMetric"] { background: linear-gradient(135deg, #1A1F3C 0%, #0D1126 100%) !important; border: 1px solid #2E355E !important; border-radius: 20px !important; padding: 20px !important; box-shadow: 0 10px 20px rgba(0,0,0,0.4) !important; }
    div[data-testid="stMetricValue"] > div { background: linear-gradient(90deg, #BF5AF2 0%, #00EAFF 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 38px !important; font-weight: 800 !important; }
    div[data-testid="stMetricLabel"] > div { color: #A0AEC0 !important; font-size: 16px !important; }
    .stButton > button { background: linear-gradient(90deg, #8A2BE2 0%, #BF5AF2 100%) !important; color: white !important; border: none !important; border-radius: 30px !important; padding: 12px 30px !important; font-weight: bold !important; box-shadow: 0 5px 15px rgba(138, 43, 226, 0.4) !important; }
    .stTextInput > div > div > input { background-color: #1A1F3C !important; color: white !important; border: 1px solid #2E355E !important; border-radius: 12px !important; }
    .ai-card { background: linear-gradient(135deg, rgba(138, 43, 226, 0.15) 0%, rgba(0, 234, 255, 0.05) 100%) !important; border: 1px solid rgba(138, 43, 226, 0.4) !important; border-radius: 20px !important; padding: 25px !important; color: #E0E0E0 !important; line-height: 1.8 !important; margin: 20px 0; }
    .stDataFrame { background-color: #1A1F3C !important; border-radius: 15px !important; }
</style>
""", unsafe_allow_html=True)

# --- ຫົວຂໍ້ ---
header_text = """
<div style="background: linear-gradient(135deg, #1A1F3C 0%, #050A18 100%); padding: 30px; border-radius: 25px; border: 1px solid #2E355E; text-align: center; margin-bottom: 25px;">
    <h1 style="margin: 0; background: linear-gradient(90deg, #BF5AF2 0%, #00EAFF 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 40px;">🌸 ລະບົບບັນຊີ Super AI ປ້າພອນສຸກ </h1>
    <p style="color: #A0AEC0; font-size: 16px; margin-top: 10px;">🟢 ເຊື່ອມຕໍ່ຖານຂໍ້ມູນ Google Sheets ສຳເລັດແລ້ວ 🟢</p>
    <p style="color: #636E72; font-size: 14px; margin-bottom: 0;">ເບີໂທ: 020 99858310 | Line: Tarvan</p>
</div>
"""
st.write(header_text, unsafe_allow_html=True)

# --- ຟັງຊັນຊ່ວຍຈັດການຕົວເລກ ---
def format_num(v):
    if v == "" or v is None: return ""
    nums = "".join(filter(str.isdigit, str(v)))
    return "{:,}".format(int(nums)) if nums else ""

def parse_num(v):
    if v == "" or v is None: return 0
    nums = "".join(filter(str.isdigit, str(v)))
    return int(nums) if nums else 0

def update_val(key):
    st.session_state[key] = format_num(st.session_state[key])

def input_box(label, base_key):
    actual_key = f"{base_key}_{st.session_state.clear_counter}"
    if actual_key not in st.session_state:
        st.session_state[actual_key] = ""
    return st.text_input(label, key=actual_key, on_change=update_val, args=(actual_key,))

# --- 4. ສ່ວນປ້ອນຂໍ້ມູນ ---
c1, c2 = st.columns(2)
with c1:
    st.markdown("#### <span style='color: #00EAFF;'>🟢 ສ່ວນລາຍຮັບ</span>", unsafe_allow_html=True)
    i1_v = input_box("1. ຮັບເງິນເດືອນ", "i1")
    i2_v = input_box("2. ລາຍຮັບ Creator (FB/YouTube)", "i2")
    i3_v = input_box("3. ລາຍຮັບຂາຍຂອງຍ່ອຍ", "i3")
    i4_v = input_box("4. ລາຍຮັບຕັດຫຍິບ", "i4")
    i5_v = input_box("5. ລາຍຮັບຕູ້ກົດນ້ຳ", "i5")
    i6_v = input_box("6. ລາຍຮັບຕູ້ຊັກຜ້າ", "i6")
    i7_v = input_box("7. ລາຍຮັບອື່ນໆ", "i7")

with c2:
    st.markdown("#### <span style='color: #FF00E6;'>🔴 ສ່ວນລາຍຈ່າຍ</span>", unsafe_allow_html=True)
    e1_v = input_box("1. ຄ່າອາຫານ & ເຄື່ອງບໍລິໂພກ", "e1")
    e2_v = input_box("2. ຄ່າເຊົ່າທີ່ຢູ່", "e2")
    e3_v = input_box("3. ຄ່ານ້ຳ-ຄ່າໄຟ-ເນັດ", "e3")
    e4_v = input_box("4. ຄ່າເດີນທາງ", "e4")
    e5_v = input_box("5. ຄ່າການສຶກສາ", "e5")
    e6_v = input_box("6. ຄ່າປິ່ນປົວ", "e6")
    e7_v = input_box("7. ຄ່າເສື້ອຜ້າ & ຂອງໃຊ້", "e7")
    e8_v = input_box("8. ຄ່າໂທລະສັບ & ບັນເທີງ", "e8")
    e9_v = input_box("9. ຄ່າຫວຍ/ລາງວັນ", "e9")
    e10_v = input_box("10. ຄ່າສ້າງເຮືອນ", "e10")
    e11_v = input_box("11. ຄ່າຊື້ສິນຄ້າເຂົ້າຮ້ານ", "e11")

submit = st.button("💾 ບັນທຶກຂໍ້ມູນລົງ Google Sheets", use_container_width=True)

# ----------------------------------------------------
# ດຶງຂໍ້ມູນຈາກ Google Sheets ເພື່ອກຽມອັບເດດ ແລະ ສະແດງຜົນ
# ----------------------------------------------------
df = pd.DataFrame(columns=COLUMNS) # ສ້າງຕະລາງເປົ່າໄວ້ກ່ອນກັນ Error
try:
    if "ປ່ຽນເປັນ" not in SHEET_URL:
        df = conn.read(spreadsheet=SHEET_URL, worksheet="Sheet1", ttl=0)
        # ຖ້າ Sheet ວ່າງເປົ່າ ໃຫ້ສ້າງຕະລາງທີ່ມີຫົວຂໍ້
        if df.empty or len(df.columns) < 5:
            df = pd.DataFrame(columns=COLUMNS)
    else:
        st.error("⚠️ ກະລຸນາເອົາ Link ຂອງ Google Sheets ໄປໃສ່ໃນແຖວທີ 28 ກ່ອນ!")
except Exception as e:
    st.error(f"❌ ບໍ່ສາມາດເຊື່ອມຕໍ່ Google Sheets ໄດ້. Error: {e}")

# ເມື່ອກົດປຸ່ມບັນທຶກ
if submit:
    now_lao = datetime.now() + timedelta(hours=7) 
    v_i = [parse_num(i1_v), parse_num(i2_v), parse_num(i3_v), parse_num(i4_v), parse_num(i5_v), parse_num(i6_v), parse_num(i7_v)]
    v_e = [parse_num(e1_v), parse_num(e2_v), parse_num(e3_v), parse_num(e4_v), parse_num(e5_v), parse_num(e6_v), parse_num(e7_v), parse_num(e8_v), parse_num(e9_v), parse_num(e10_v), parse_num(e11_v)]
    t_in, t_ex = sum(v_i), sum(v_e)
    
    if t_in == 0 and t_ex == 0:
        st.warning("⚠️ ກະລຸນາປ້ອນຂໍ້ມູນກ່ອນບັນທຶກ!")
    elif "ປ່ຽນເປັນ" in SHEET_URL:
        st.error("⚠️ ຍັງບໍ່ໄດ້ປ່ຽນ Link Google Sheets ໃນແຖວທີ 28 ຂອງໂຄ້ດ!")
    else:
        new_data = {
            'ວັນທີ': now_lao.strftime("%d/%m/%Y %H:%M"), 
            'ລາຍຮັບລວມ': t_in, 'ລາຍຈ່າຍລວມ': t_ex, 'ເຫຼືອເກັບ': t_in - t_ex,
            'ເງິນເດືອນ': v_i[0], 'Creator': v_i[1], 'ຂາຍຂອງ': v_i[2], 'ຫຍິບຜ້າ': v_i[3], 'ຕູ້ກົດນ້ຳ': v_i[4], 'ຕູ້ຊັກຜ້າ': v_i[5], 'ຮັບອື່ນໆ': v_i[6],
            'ອາຫານ': v_e[0], 'ຄ່າເຊົ່າ': v_e[1], 'ນ້ຳໄຟ': v_e[2], 'ເດີນທາງ': v_e[3], 'ການສຶກສາ': v_e[4], 'ຢາ': v_e[5], 'ເສື້ອຜ້າ': v_e[6], 'ບັນເທີງ': v_e[7], 'ຫວຍ': v_e[8], 'ສ້າງເຮືອນ': v_e[9], 'ຊື້ຂອງເຂົ້າຮ້ານ': v_e[10]
        }
        
        new_df = pd.DataFrame([new_data])
        updated_df = pd.concat([df, new_df], ignore_index=True)
        
        with st.spinner("⏳ ກຳລັງສົ່ງຂໍ້ມູນລົງ Google Sheets..."):
            conn.update(spreadsheet=SHEET_URL, worksheet="Sheet1", data=updated_df)
            st.cache_data.clear()
            
        st.session_state.clear_counter += 1
        st.success(f"✅ ບັນທຶກສຳເລັດ! ຂໍ້ມູນຖືກສົ່ງໄປ Google Sheets ແລ້ວ.")
        st.rerun() 

# --- 5. ສະແດງຜົນ ແລະ AI ວິເຄາະ ---
if not df.empty:
    st.markdown("---")
    st.subheader("📈 Dashboard ສະຫຼຸບຕົວເລກ")
    option = st.radio("ເລືອກໄລຍະເວລາລາຍງານ:", ["ມື້ນີ້", "ອາທິດນີ້", "ເດືອນນີ້", "ປີນີ້"], horizontal=True)

    df['Date_Obj'] = pd.to_datetime(df['ວັນທີ'], format='mixed', dayfirst=True, errors='coerce')
    df_clean = df.dropna(subset=['Date_Obj']) 

    now = datetime.now() + timedelta(hours=7)
    
    if option == "ມື້ນີ້": filtered_df, text_time = df_clean[df_clean['Date_Obj'].dt.date == now.date()], "ຂອງມື້ນີ້"
    elif option == "ອາທິດນີ້": filtered_df, text_time = df_clean[df_clean['Date_Obj'].dt.isocalendar().week == now.isocalendar()[1]], "ຂອງອາທິດນີ້"
    elif option == "ເດືອນນີ້": filtered_df, text_time = df_clean[df_clean['Date_Obj'].dt.month == now.month], "ຂອງເດືອນນີ້"
    else: filtered_df, text_time = df_clean[df_clean['Date_Obj'].dt.year == now.year], "ຂອງປີນີ້"

    if not filtered_df.empty:
        t_in = pd.to_numeric(filtered_df['ລາຍຮັບລວມ'], errors='coerce').sum()
        t_ex = pd.to_numeric(filtered_df['ລາຍຈ່າຍລວມ'], errors='coerce').sum()
        profit = t_in - t_ex
        
        c1, c2, c3 = st.columns(3)
        c1.metric(f"ລາຍຮັບ {text_time}", f"{t_in:,.0f} ກີບ")
        c2.metric(f"ລາຍຈ່າຍ {text_time}", f"{t_ex:,.0f} ກີບ")
        c3.metric(f"ເຫຼືອເກັບ/ກຳໄລ", f"{profit:,.0f} ກີບ")

        if not ai_ready:
            st.error(f"🔍 ລະບົບ AI ຍັງບໍ່ພ້ອມ: {ai_error_msg}")
        else:
            st.write("<br>", unsafe_allow_html=True)
            if st.button("✨ ເປີດໃຊ້ທີ່ປຶກສາ DeepSeek AI", use_container_width=True):
                with st.spinner("🤖 DeepSeek ກຳລັງວິເຄາະຕົວເລກໃຫ້ປ້າ..."):
                    try:
                        response = client.chat.completions.create(
                            model="deepseek-chat",
                            messages=[
                                {"role": "system", "content": "ເຈົ້າຄື CFO ທີ່ປຶກສາການເງິນຂອງປ້າພອນສຸກ. ຕອບເປັນພາສາລາວສັ້ນໆ ອ່ານງ່າຍ."},
                                {"role": "user", "content": f"ວິເຄາະບັນຊີ: ຮັບ {t_in}, ຈ່າຍ {t_ex}, ເຫຼືອ {profit}. ແນະນຳ 3 ຫົວຂໍ້: ສະຫຼຸບ, ວິທີເພີ່ມລາຍຮັບ, ວິທີປະຢັດ."},
                            ]
                        )
                        st.markdown(f'<div class="ai-card"><h3>🤖 ບົດວິເຄາະຈາກ DeepSeek AI</h3>{response.choices[0].message.content}</div>', unsafe_allow_html=True)
                    except Exception as e:
                        st.error(f"Error AI: {e}")

    # --- 6. ຕາຕະລາງປະຫວັດແບບລະອຽດ ---
    st.markdown("---")
    st.write("### 📅 ປະຫວັດການເງິນ (10 ລາຍການຫຼ້າສຸດຈາກ Google Sheets)")
    display_df = df.drop(columns=['Date_Obj'], errors='ignore')
    
    for col in COLUMNS[1:]: 
        display_df[col] = pd.to_numeric(display_df[col], errors='coerce')
        
    st.dataframe(display_df.tail(10).style.format(subset=COLUMNS[1:], formatter="{:,.0f}"), use_container_width=True)

    # --- ສ່ວນລົບຂໍ້ມູນ ---
    with st.expander("🛠️ ຈັດການຖານຂໍ້ມູນ (ລ້າງຂໍ້ມູນໃນ Sheet)"):
        if st.text_input("ໃສ່ລະຫັດ 9999 ເພື່ອຢືນຢັນ", type="password") == "9999":
            if st.button("🗑️ ຢືນຢັນລ້າງຂໍ້ມູນທັງໝົດໃນ Google Sheets"):
                empty_df = pd.DataFrame(columns=COLUMNS)
                try:
                    conn.update(spreadsheet=SHEET_URL, worksheet="Sheet1", data=empty_df)
                    st.cache_data.clear()
                    st.success("ລ້າງຂໍ້ມູນສຳເລັດແລ້ວ!")
                    st.rerun()
                except Exception as e:
                    st.error(f"ເກີດຂໍ້ຜິດພາດ: {e}")
