import streamlit as st
import pandas as pd
import os
from datetime import datetime, timedelta
from openai import OpenAI  # DeepSeek ໃຊ້ລະບົບດຽວກັບ OpenAI

# --- 1. ຕັ້ງຄ່າ DeepSeek AI ---
ai_error_msg = ""
try:
    if "DEEPSEEK_API_KEY" in st.secrets:
        # ເຊື່ອມຕໍ່ຫາ DeepSeek API
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
st.set_page_config(page_title="App ບັນຊີຂອງປ້າພອນສຸກ", layout="wide")
FILE_NAME = 'phonsouk_final_database_v3.csv'

if 'clear_counter' not in st.session_state:
    st.session_state.clear_counter = 0

# --- 3. CSS ຕົບແຕ່ງ UI ---
st.markdown("""
<style>
    [data-testid="stMetricValue"] { color: #1B4F72 !important; font-size: 35px !important; font-weight: bold !important; }
    [data-testid="stMetricLabel"] { color: #566573 !important; font-size: 18px !important; }
    div[data-testid="stMetric"] { background-color: #FFFFFF !important; border: 2px solid #1B4F72 !important; padding: 15px !important; border-radius: 10px !important; box-shadow: 2px 2px 10px rgba(0,0,0,0.1); }
    .ai-card { background-color: #EBF5FB !important; padding: 25px; border-left: 10px solid #1B4F72; border-radius: 10px; color: #1B4F72 !important; margin: 20px 0; line-height: 1.8; }
</style>
""", unsafe_allow_html=True)

# --- ຫົວຂໍ້ ---
header_text = """
<div style="background-color: #1B4F72; padding: 25px; border-radius: 15px; border: 3px solid #F1C40F; text-align: center; color: white;">
    <h1 style="margin: 0;">🌸 ລະບົບບັນຊີ Super AI ປ້າພອນສຸກ </h1>
    <p style="margin: 10px 0;">ເບີໂທ: 020 99858310 | Line: Tarvan</p>
    <div style="font-size: 30px; margin-top: 10px;">🌸 🇱🇦 🌸</div>
</div><br>
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
    st.success("### 🟢 ສ່ວນລາຍຮັບ")
    i1_v = input_box("1. ຮັບເງິນເດືອນ", "i1")
    i2_v = input_box("2. ລາຍຮັບ Creator (FB/YouTube)", "i2")
    i3_v = input_box("3. ລາຍຮັບຂາຍຂອງຍ່ອຍ", "i3")
    i4_v = input_box("4. ລາຍຮັບຕັດຫຍິບ", "i4")
    i5_v = input_box("5. ລາຍຮັບຕູ້ກົດນ້ຳ", "i5")
    i6_v = input_box("6. ລາຍຮັບຕູ້ຊັກຜ້າ", "i6")
    i7_v = input_box("7. ລາຍຮັບອື່ນໆ", "i7")

with c2:
    st.error("### 🔴 ສ່ວນລາຍຈ່າຍ")
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

submit = st.button("💾 ບັນທຶກຂໍ້ມູນທັງໝົດ", use_container_width=True)

if submit:
    now_lao = datetime.now() + timedelta(hours=7) 
    v_i = [parse_num(i1_v), parse_num(i2_v), parse_num(i3_v), parse_num(i4_v), parse_num(i5_v), parse_num(i6_v), parse_num(i7_v)]
    v_e = [parse_num(e1_v), parse_num(e2_v), parse_num(e3_v), parse_num(e4_v), parse_num(e5_v), parse_num(e6_v), parse_num(e7_v), parse_num(e8_v), parse_num(e9_v), parse_num(e10_v), parse_num(e11_v)]
    t_in, t_ex = sum(v_i), sum(v_e)
    
    if t_in == 0 and t_ex == 0:
        st.warning("⚠️ ກະລຸນາປ້ອນຂໍ້ມູນກ່ອນບັນທຶກ!")
    else:
        new_data = {
            'ວັນທີ': now_lao.strftime("%d/%m/%Y %H:%M"), 
            'ລາຍຮັບລວມ': t_in, 'ລາຍຈ່າຍລວມ': t_ex, 'ເຫຼືອເກັບ': t_in - t_ex,
            'ເງິນເດືອນ': v_i[0], 'Creator': v_i[1], 'ຂາຍຂອງ': v_i[2], 'ຫຍິບຜ້າ': v_i[3], 'ຕູ້ກົດນ້ຳ': v_i[4], 'ຕູ້ຊັກຜ້າ': v_i[5], 'ຮັບອື່ນໆ': v_i[6],
            'ອາຫານ': v_e[0], 'ຄ່າເຊົ່າ': v_e[1], 'ນ້ຳໄຟ': v_e[2], 'ເດີນທາງ': v_e[3], 'ການສຶກສາ': v_e[4], 'ຢາ': v_e[5], 'ເສື້ອຜ້າ': v_e[6], 'ບັນເທີງ': v_e[7], 'ຫວຍ': v_e[8], 'ສ້າງເຮືອນ': v_e[9], 'ຊື້ຂອງເຂົ້າຮ້ານ': v_e[10]
        }
        pd.DataFrame([new_data]).to_csv(FILE_NAME, mode='a', index=False, header=not os.path.exists(FILE_NAME), encoding='utf-8-sig')
        st.session_state.clear_counter += 1
        st.success(f"✅ ບັນທຶກແລ້ວ!")
        st.rerun() 

# --- 5. ສະແດງຜົນ ແລະ AI ວິເຄາະ ---
if os.path.exists(FILE_NAME):
    df = pd.read_csv(FILE_NAME)
    st.markdown("---")
    st.subheader("📊 ເບິ່ງສະຫຼຸບ ແລະ ໃຫ້ AI ວິເຄາະ")
    option = st.radio("ເລືອກໄລຍະເວລາ:", ["ມື້ນີ້", "ອາທິດນີ້", "ເດືອນນີ້", "ປີນີ້"], horizontal=True)

    df['Date_Obj'] = pd.to_datetime(df['ວັນທີ'], format="%d/%m/%Y %H:%M")
    now = datetime.now()
    
    if option == "ມື້ນີ້": filtered_df, text_time = df[df['Date_Obj'].dt.date == now.date()], "ຂອງມື້ນີ້"
    elif option == "ອາທິດນີ້": filtered_df, text_time = df[df['Date_Obj'].dt.isocalendar().week == now.isocalendar()[1]], "ຂອງອາທິດນີ້"
    elif option == "ເດືອນນີ້": filtered_df, text_time = df[df['Date_Obj'].dt.month == now.month], "ຂອງເດືອນນີ້"
    else: filtered_df, text_time = df[df['Date_Obj'].dt.year == now.year], "ຂອງປີນີ້"

    if not filtered_df.empty:
        t_in, t_ex = filtered_df['ລາຍຮັບລວມ'].sum(), filtered_df['ລາຍຈ່າຍລວມ'].sum()
        profit = t_in - t_ex
        
        c1, c2, c3 = st.columns(3)
        c1.metric(f"ລາຍຮັບ {text_time}", f"{t_in:,.0f} ກີບ")
        c2.metric(f"ລາຍຈ່າຍ {text_time}", f"{t_ex:,.0f} ກີບ")
        c3.metric(f"ກຳໄລ {text_time}", f"{profit:,.0f} ກີບ")

        if not ai_ready:
            st.error(f"🔍 ລະບົບ AI ຍັງບໍ່ພ້ອມ: {ai_error_msg}")
        else:
            if st.button("✨ ໃຫ້ DeepSeek AI ຊ່ວຍວິເຄາະບັນຊີ", use_container_width=True):
                with st.spinner("🤖 DeepSeek ກຳລັງວິເຄາະຕົວເລກໃຫ້ປ້າ..."):
                    try:
                        response = client.chat.completions.create(
                            model="deepseek-chat",
                            messages=[
                                {"role": "system", "content": "ເຈົ້າຄື CFO ທີ່ປຶກສາການເງິນຂອງປ້າພອນສຸກ. ຕອບເປັນພາສາລາວສັ້ນໆ ອ່ານງ່າຍ."},
                                {"role": "user", "content": f"ວິເຄາະບັນຊີ: ຮັບ {t_in}, ຈ່າຍ {t_ex}, ເຫຼືອ {profit}. ແນະນຳ 3 ຫົວຂໍ້: ສະຫຼຸບ, ວິທີເພີ່ມລາຍຮັບ, ວິທີປະຢັດ."},
                            ]
                        )
                        st.markdown(f'<div class="ai-card"><h3>🤖 ຜົນວິເຄາະຈາກ DeepSeek</h3>{response.choices[0].message.content}</div>', unsafe_allow_html=True)
                    except Exception as e:
                        st.error(f"Error AI: {e}")

    # --- 6. ຕາຕະລາງປະຫວັດແບບລະອຽດ ---
    st.markdown("---")
    st.write("### 📅 ປະຫວັດການເງິນ (10 ລາຍການຫຼ້າສຸດ)")
    display_df = df.drop(columns=['Date_Obj'], errors='ignore')
    num_cols = display_df.select_dtypes(include=['number']).columns.tolist()
    st.dataframe(display_df.tail(10).style.format(subset=num_cols, formatter="{:,.0f}"), use_container_width=True)

    # --- ສ່ວນລົບຂໍ້ມູນ ---
    with st.expander("🛠️ ລ້າງຂໍ້ມູນ"):
        if st.text_input("ລະຫັດ 9999", type="password") == "9999":
            if st.button("🗑️ ຢືນຢັນລົບ"):
                os.remove(FILE_NAME)
                st.rerun()
