import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from openai import OpenAI  
from streamlit_gsheets import GSheetsConnection 

# --- 1. ຕັ້ງຄ່າ AI & Google Sheets ---
st.set_page_config(page_title="App ບັນຊີປ້າພອນສຸກ", layout="wide")

try:
    client = OpenAI(api_key=st.secrets["DEEPSEEK_API_KEY"], base_url="https://api.deepseek.com")
    ai_ready = True
except:
    ai_ready = False

conn = st.connection("gsheets", type=GSheetsConnection)
# 🔴 ໃສ່ ID ຕະລາງຂອງເຈົ້າທີ່ນີ້ (ລະຫັດຍາວໆໃນ Link) 🔴
SHEET_ID = "1XyZ123" 

if 'clear_counter' not in st.session_state: st.session_state.clear_counter = 0

COLUMNS = ['ວັນທີ', 'ລາຍຮັບລວມ', 'ລາຍຈ່າຍລວມ', 'ເຫຼືອເກັບ', 'ເງິນເດືອນ', 'Creator', 'ຂາຍຂອງ', 'ຫຍິບຜ້າ', 'ຕູ້ກົດນ້ຳ', 'ຕູ້ຊັກຜ້າ', 'ຮັບອື່ນໆ', 'ອາຫານ', 'ຄ່າເຊົ່າ', 'ນ້ຳໄຟ', 'ເດີນທາງ', 'ການສຶກສາ', 'ຢາ', 'ເສື້ອຜ້າ', 'ບັນເທີງ', 'ຫວຍ', 'ສ້າງເຮືອນ', 'ຊື້ຂອງເຂົ້າຮ້ານ']

# --- 2. CSS ຕົບແຕ່ງ UI ---
st.markdown("""<style>
    .stApp { background-color: #050A18 !important; color: #FFFFFF !important; }
    .ai-card { background: linear-gradient(135deg, rgba(138, 43, 226, 0.15) 0%, rgba(0, 234, 255, 0.05) 100%) !important; border: 1px solid rgba(138, 43, 226, 0.4) !important; border-radius: 20px !important; padding: 25px !important; }
    div[data-testid="stMetricValue"] > div { color: #00EAFF !important; font-size: 38px !important; }
</style>""", unsafe_allow_html=True)

# --- 3. ຟັງຊັນຈັດການຂໍ້ມູນ ---
def format_num(v): return "{:,}".format(int("".join(filter(str.isdigit, str(v))))) if v else ""
def parse_num(v): return int("".join(filter(str.isdigit, str(v)))) if v else 0
def input_box(label, base_key):
    k = f"{base_key}_{st.session_state.clear_counter}"
    if k not in st.session_state: st.session_state[k] = ""
    return st.text_input(label, key=k, on_change=lambda: st.session_state.update({k: format_num(st.session_state[k])}))

# --- 4. ສ່ວນປ້ອນຂໍ້ມູນ ---
c1, c2 = st.columns(2)
with c1:
    st.markdown("#### 🟢 ສ່ວນລາຍຮັບ")
    inputs_i = [input_box(l, f"i{i+1}") for i, l in enumerate(["ຮັບເງິນເດືອນ", "Creator", "ຂາຍຂອງຍ່ອຍ", "ຫຍິບຜ້າ", "ຕູ້ກົດນ້ຳ", "ຕູ້ຊັກຜ້າ", "ຮັບອື່ນໆ"])]
with c2:
    st.markdown("#### 🔴 ສ່ວນລາຍຈ່າຍ")
    inputs_e = [input_box(l, f"e{i+1}") for i, l in enumerate(["ອາຫານ", "ຄ່າເຊົ່າ", "ນ້ຳໄຟ", "ເດີນທາງ", "ການສຶກສາ", "ຢາ", "ເສື້ອຜ້າ", "ບັນເທີງ", "ຫວຍ", "ສ້າງເຮືອນ", "ຊື້ຂອງເຂົ້າຮ້ານ"])]

# --- 5. ບັນທຶກຂໍ້ມູນ ---
if st.button("💾 ບັນທຶກຂໍ້ມູນທັງໝົດ"):
    v_i = [parse_num(x) for x in inputs_i]
    v_e = [parse_num(x) for x in inputs_e]
    t_in, t_ex = sum(v_i), sum(v_e)
    
    new_data = pd.DataFrame([{**{'ວັນທີ': (datetime.now()+timedelta(hours=7)).strftime("%d/%m/%Y %H:%M"), 'ລາຍຮັບລວມ': t_in, 'ລາຍຈ່າຍລວມ': t_ex, 'ເຫຼືອເກັບ': t_in - t_ex}, **dict(zip(COLUMNS[4:], v_i + v_e)) }])
    
    try:
        existing_df = conn.read(spreadsheet=SHEET_ID, worksheet="Sheet1")
        conn.update(spreadsheet=SHEET_ID, worksheet="Sheet1", data=pd.concat([existing_df, new_data], ignore_index=True))
        st.session_state.clear_counter += 1
        st.success("✅ ບັນທຶກສຳເລັດ!")
        st.rerun()
    except Exception as e:
        st.error(f"ຜິດພາດ: {e}")

# --- 6. ສະແດງຜົນ Dashboard ---
try:
    df = conn.read(spreadsheet=SHEET_ID, worksheet="Sheet1")
    df['Date_Obj'] = pd.to_datetime(df['ວັນທີ'], format='mixed', dayfirst=True)
    
    st.write("### 📈 Dashboard ສະຫຼຸບຕົວເລກ")
    opt = st.radio("ໄລຍະເວລາ:", ["ມື້ນີ້", "ເດືອນນີ້"], horizontal=True)
    now = datetime.now() + timedelta(hours=7)
    
    f_df = df[df['Date_Obj'].dt.month == now.month] if opt == "ເດືອນນີ້" else df[df['Date_Obj'].dt.date == now.date()]
    
    if not f_df.empty:
        t_in, t_ex = f_df['ລາຍຮັບລວມ'].sum(), f_df['ລາຍຈ່າຍລວມ'].sum()
        c1, c2, c3 = st.columns(3)
        c1.metric("ລາຍຮັບ", f"{t_in:,.0f}")
        c2.metric("ລາຍຈ່າຍ", f"{t_ex:,.0f}")
        c3.metric("ກຳໄລ", f"{t_in - t_ex:,.0f}")

        if ai_ready and st.button("✨ ເປີດໃຊ້ DeepSeek AI"):
            resp = client.chat.completions.create(model="deepseek-chat", messages=[{"role": "user", "content": f"ວິເຄາະ: ຮັບ {t_in}, ຈ່າຍ {t_ex}, ເຫຼືອ {t_in-t_ex}"}])
            st.markdown(f'<div class="ai-card">{resp.choices[0].message.content}</div>', unsafe_allow_html=True)

    st.write("### 📅 ປະຫວັດການເງິນ")
    st.dataframe(df.tail(10))
    
    if st.text_input("ລະຫັດລົບຂໍ້ມູນ (9999)", type="password") == "9999":
        if st.button("🗑️ ລ້າງຂໍ້ມູນ"):
            conn.update(spreadsheet=SHEET_ID, worksheet="Sheet1", data=pd.DataFrame(columns=COLUMNS))
            st.rerun()
except:
    st.info("ຍັງບໍ່ມີຂໍ້ມູນ ຫຼື ເຊື່ອມຕໍ່ບໍ່ໄດ້")
