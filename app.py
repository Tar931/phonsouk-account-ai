import streamlit as st
import pandas as pd
import os
from datetime import datetime

# --- 1. ຕັ້ງຄ່າເວັບໄຊ ---
st.set_page_config(page_title="Phonsouk AI Business Planner", page_icon="📈", layout="wide")
FILE_NAME = 'shop_database_v4.csv'

st.markdown("""
    <div style="background-color:#002B36;padding:25px;border-radius:15px;text-align:center;border: 3px solid #268BD2;">
        <h1 style="color:#268BD2;">📈 AI ວາງແຜນການເງິນ & ອາຊີບ ປ້າພອນສຸກ</h1>
        <p style="color:#93A1A1;">ສະຫຼຸບລາຍອາທິດ, ລາຍເດືອນ, ລາຍປີ ແລະ ຊອກຫາຊ່ອງທາງປະຢັດ</p>
    </div>
    """, unsafe_allow_html=True)

# --- 2. ສ່ວນປ້ອນຂໍ້ມູນ ---
with st.expander("➕ ບັນທຶກລາຍຮັບ-ລາຍຈ່າຍ (ມື້ນີ້ຈ່າຍຫຍັງ ຮັບຫຍັງ)", expanded=True):
    col1, col2 = st.columns(2)
    with col1:
        s1 = st.number_input("ຍອດຂາຍ (ໜ້າຮ້ານ/Online)", min_value=0, step=5000, key="inc1")
        s2 = st.number_input("ຄ່າແຮງຕັດຫຍິບ (Sewing)", min_value=0, step=5000, key="inc2")
    with col2:
        e1 = st.number_input("ຄ່າເຄື່ອງ/Stock", min_value=0, step=5000, key="exp1")
        e2 = st.number_input("ຄ່າກິນ/ໃຊ້ໃນເຮືອນ", min_value=0, step=5000, key="exp2")
        e3 = st.number_input("ລາຍຈ່າຍອື່ນໆ", min_value=0, step=5000, key="exp3")

    if st.button("💾 ບັນທຶກ ແລະ ໃຫ້ AI ວິເຄາະທັນທີ", use_container_width=True, type="primary"):
        now = datetime.now()
        new_data = {
            'Date': now.strftime("%Y-%m-%d %H:%M"),
            'Day': now.strftime("%A"),
            'Week': now.isocalendar()[1],
            'Month': now.strftime("%m-%Y"),
            'Year': str(now.year), # ເກັບເປັນປີ
            'Income': s1 + s2,
            'Sewing': s2,
            'Expense': e1 + e2 + e3,
            'Food': e2,
            'Stock': e1,
            'Profit': (s1 + s2) - (e1 + e2 + e3)
        }
        df_new = pd.DataFrame([new_data])
        df_new.to_csv(FILE_NAME, mode='a', index=False, header=not os.path.exists(FILE_NAME))
        st.balloons()
        st.success("AI ໄດ້ບັນທຶກ ແລະ ເກັບຂໍ້ມູນໄວ້ໃນລາຍງານປະຈຳປີແລ້ວ!")

# --- 3. ສ່ວນລາຍງານ AI (Weekly/Monthly/Yearly) ---
if os.path.exists(FILE_NAME):
    df = pd.read_csv(FILE_NAME)
    df['Year'] = df['Year'].astype(str) # ເຮັດໃຫ້ປີເປັນຕົວໜັງສືເພື່ອຄົ້ນຫາງ່າຍ
    
    st.markdown("---")
    st.header("🧠 ສະຫຼຸບລາຍງານ ແລະ ແຜນອາຊີບ")
    
    # ປຸ່ມເລືອກເບິ່ງລາຍງານ
    report_type = st.segmented_control("ເລືອກໄລຍະເວລາທີ່ຕ້ອງການໃຫ້ AI ລາຍງານ:", ["ລາຍອາທິດ", "ລາຍເດືອນ", "ລາຍປີ"], default="ລາຍອາທິດ")
    
    now = datetime.now()
    if report_type == "ລາຍອາທິດ":
        summary = df[df['Week'] == now.isocalendar()[1]]
        text = "ອາທິດນີ້"
    elif report_type == "ລາຍເດືອນ":
        summary = df[df['Month'] == now.strftime("%m-%Y")]
        text = "ເດືອນນີ້"
    else:
        summary = df[df['Year'] == str(now.year)]
        text = f"ປີ {now.year}"

    # ສະແດງຕົວເລກລວມ
    c1, c2, c3 = st.columns(3)
    in_sum = summary['Income'].sum()
    out_sum = summary['Expense'].sum()
    pro_sum = in_sum - out_sum
    
    c1.metric(f"ລາຍຮັບ {text}", "{:,.0f} ກີບ".format(in_sum))
    c2.metric(f"ລາຍຈ່າຍ {text}", "{:,.0f} ກີບ".format(out_sum))
    c3.metric(f"ກຳໄລ {text}", "{:,.0f} ກີບ".format(pro_sum), delta=float(pro_sum))

    # --- 4. AI ວິເຄາະຊ່ອງທາງປະຢັດ ແລະ ວາງແຜນອາຊີບ ---
    st.markdown("### 💡 ຄຳແນະນຳຈາກ AI ສໍາລັບປ້າ")
    col_ai1, col_ai2 = st.columns(2)
    
    with col_ai1:
        st.write("**📍 ຊ່ອງທາງປະຢັດ:**")
        food_total = summary['Food'].sum()
        if food_total > (in_sum * 0.3) and in_sum > 0:
            st.error(f"ປ້າໃຊ້ເງິນຄ່າກິນໄປ {format(food_total, ',.0f')} ກີບ. AI ແນະນຳໃຫ້ປ້າລອງວາງແຜນຊື້ຂອງສົດເປັນອາທິດ ຈະປະຢັດໄດ້ຫຼາຍຂຶ້ນ!")
        else:
            st.success("ການໃຊ້ຈ່າຍຄົວເຮືອນຂອງປ້າຢູ່ໃນເກນທີ່ດີຫຼາຍ. ຮັກສາລະດັບນີ້ໄວ້ເດີ້!")

    with col_ai2:
        st.write("**📍 ແຜນວາງແຜນອາຊີບ:**")
        sewing_total = summary['Sewing'].sum()
        if sewing_total > 0:
            st.info(f"ລາຍໄດ້ຈາກການຕັດຫຍິບແມ່ນ {format(sewing_total, ',.0f')} ກີບ. ເພື່ອໃຫ້ເປັນມືອາຊີບ, ປ້າຄວນເກັບສະສົມກຳໄລ 10% ໄວ້ຊື້ຈັກເຍັບຜ້າລຸ້ນໃໝ່ໃນອະນາຄົດ.")
        else:
            st.warning("ຍັງບໍ່ມີລາຍຮັບຈາກການຕັດຫຍິບ. ປ້າລອງໂທຫາລູກຄ້າເກົ່າເພື່ອຖາມຂ່າວຄາວ ແລະ ຮັບງານໃໝ່ເບິ່ງເດີ້.")

    # ສະແດງປະຫວັດ
    with st.expander("📜 ເບິ່ງປະຫວັດການບັນທຶກທັງໝົດ"):
        st.dataframe(df.sort_values(by='Date', ascending=False), use_container_width=True)