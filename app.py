import streamlit as st
import pandas as pd
import requests # ຢ່າລືມ pip install requests
from datetime import datetime, timedelta

# ຕັ້ງຄ່າ URL ທີ່ໄດ້ຈາກ Google Apps Script
WEBHOOK_URL = "ເອົາ URL ທີ່ໄດ້ຈາກການ Deploy ມາໃສ່ບ່ອນນີ້"

# ... (ຟັງຊັນ input_box ແລະ format_num ໃຊ້ຂອງເກົ່າເຈົ້າໄດ້ເລີຍ) ...

if submit:
    now_lao = datetime.now() + timedelta(hours=7)
    v_i = [parse_num(i1_v), parse_num(i2_v), parse_num(i3_v), parse_num(i4_v), parse_num(i5_v), parse_num(i6_v), parse_num(i7_v)]
    v_e = [parse_num(e1_v), parse_num(e2_v), parse_num(e3_v), parse_num(e4_v), parse_num(e5_v), parse_num(e6_v), parse_num(e7_v), parse_num(e8_v), parse_num(e9_v), parse_num(e10_v), parse_num(e11_v)]
    t_in, t_ex = sum(v_i), sum(v_e)

    payload = {
        'date': now_lao.strftime("%d/%m/%Y %H:%M"),
        'total_in': t_in, 'total_ex': t_ex, 'balance': t_in - t_ex,
        'salary': v_i[0], 'creator': v_i[1], 'sale': v_i[2], 'sew': v_i[3], 'water': v_i[4], 'wash': v_i[5], 'other': v_i[6],
        'food': v_e[0], 'rent': v_e[1], 'bill': v_e[2], 'travel': v_e[3], 'study': v_e[4], 'med': v_e[5], 'cloth': v_e[6], 'ent': v_e[7], 'lottery': v_e[8], 'house': v_e[9], 'shop': v_e[10]
    }
    
    try:
        response = requests.post(WEBHOOK_URL, json=payload)
        if response.status_code == 200:
            st.success("✅ ບັນທຶກລົງ Google Sheets ສຳເລັດແລ້ວ!")
        else:
            st.error("❌ ບັນທຶກບໍ່ໄດ້")
    except Exception as e:
        st.error(f"Error: {e}")
