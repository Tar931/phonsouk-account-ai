# --- 1. ສ່ວນປ້ອນຂໍ້ມູນ ---
c1, c2 = st.columns(2)

c1, c2 = st.columns(2)
with c1:
    st.success("### 🟢 ສ່ວນລາຍຮັບ")
    i1_v = input_box("1. ລາຍຮັບເງິນເດືອນ", "i1")
    i2_v = input_box("2. ລາຍຮັບເງີນ Creator ແລະ ນ້ອງສາວຢູ່ໄທ (FB/YouTube)", "i2")
    i3_v = input_box("3. ລາຍຮັບເງີນຈາກການຂາຍຂອງຍ່ອຍ", "i3")
    i4_v = input_box("4. ລາຍຮັບເງີນຈາກຕັດຫຍິບ", "i4")
    i5_v = input_box("5. ລາຍຮັບເງີນຈາກຕູ້ກົດນ້ຳ", "i5")
    i6_v = input_box("6. ລາຍຮັບເງີນຈາກຕູ້ຊັກຜ້າ", "i6")
    i7_v = input_box("7. ລາຍຮັບເງີນຈາກຍາມບໍລິສັດ", "i7")
    i8_v = input_box("8. ລາຍຮັບເງີນເສີມອື່ນໆ", "i8")

    	
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
    e11_v = input_box("11. ຄ່າຊື້ສິນຄ້າເຂົ້າຮ້ານເພື່ອຂາຍ", "e11")

submit = st.button("💾 ບັນທຶກຂໍ້ມູນທັງໝົດ", use_container_width=True)

# --- ສ່ວນບັນທຶກ (Code ທີ່ປ້າໃຫ້ເພີ່ມ) ---
if submit:
    now_lao = datetime.now() + timedelta(hours=7) 
    
    # ແປງຄ່າຈາກຂໍ້ຄວາມທີ່ມີຈຸດ ໃຫ້ເປັນຕົວເລກແທ້ໆ
    v_i = [parse_num(i1_v), parse_num(i2_v), parse_num(i3_v), parse_num(i4_v), parse_num(i5_v), parse_num(i6_v)]
    v_e = [parse_num(e1_v), parse_num(e2_v), parse_num(e3_v), parse_num(e4_v), parse_num(e5_v), parse_num(e6_v), parse_num(e7_v), parse_num(e8_v), parse_num(e9_v), parse_num(e10_v)]
    
    t_in = sum(v_i)
    t_ex = sum(v_e)
    
    new_data = {
        'ວັນທີ': now_lao.strftime("%d/%m/%Y %H:%M"), 
        'ລາຍຮັບລວມ': t_in, 'ລາຍຈ່າຍລວມ': t_ex, 'ເຫຼືອເກັບ': t_in - t_ex,
        'ເງິນເດືອນ': v_i[0], 'Creator': v_i[1], 'ຂາຍຂອງ': v_i[2], 'ຫຍິບຜ້າ': v_i[3], 'ຕູ້້ກົດນ້ຳ': v_i[4], 'ຕູ້ຊັກຜ້າ': v_i[5],
        'ອາຫານ': v_e[0], 'ຄ່າເຊົ່າ': v_e[1], 'ນ້ຳໄຟ': v_e[2], 'ເດີນທາງ': v_e[3], 'ການສຶກສາ': v_e[4], 'ຢາ': v_e[5], 'ເສື້ອຜ້າ': v_e[6], 'ບັນເທີງ': v_e[7], 'ຫວຍ': v_e[8], 'ສ້າງເຮືອນ': v_e[9]
    }
    pd.DataFrame([new_data]).to_csv(FILE_NAME, mode='a', index=False, header=not os.path.exists(FILE_NAME), encoding='utf-8-sig')
    st.success(f"✅ ບັນທຶກແລ້ວ! ເວລາລາວ: {now_lao.strftime('%H:%M')}")
    st.rerun()
