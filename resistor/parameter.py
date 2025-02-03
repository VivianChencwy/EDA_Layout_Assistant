# parameter.py
layer_numbers = {
    'NWELL': 2,
    'DIFF': 3,
    'PIMP': 7,
    'NIMP': 8,
    'POLY1': 13,
    'CONT': 15,
    'METAL1': 16,
    'VIA12': 17,
    'METAL2': 18,
    'VIA23': 27,
    'METAL3': 28,
    'VIA34': 29,
    'METAL4': 31,
    'VIA45': 32,
    'METAL5': 33,
    'METAL6': 38,
    'WELLBODY': 103,
    'RPDUMMY': 54,
    'IP': 113
}

# DRC参数
drc_params = {
    'COW1_Maxmin_CONT_Square': 0.22,  # 通孔大小
    'COE1_Min_CONT_OD_Spacing': 0.1,
    'COE2_Min_CONT_PD_Spacing': 0.1,
    'MXS2_Min_CONT_M1_Spacing': 0.6,
    'M1E2_Min_M1_CO_Spacing': 0.06,  # 金属到通孔的距离
    'Min_Diff_DUMMY_Spacing': 0.32,  # diff到rpdummy
    'M1S1_Min_M1_M1_Spacing': 0.23,
    'MARGIN_PO_OD_Distance': 0.22,
    'SLITPOE2_Min_Imp_PO_Spacing': 0.13,
    'Spacing_DIFF__NIMP_Width': 0.18,
    'COC1_Min_CO_PO_Spacing': 0.16,
    'M1W1_Min_METAL1_Width': 0.29,
    'Margin_Guarding__body_elngth': 0.3,
    'Margin_Min_Pimp_Nimp_Spacing': 0.08,
    'M1E2_Min_CONT_M1_Spacing': 0.005
}

# 针对此电阻的一些参数
rnlplus_params={
    'CO_CO_Spacing': 0.25,
    'Spacing_DIFF__NIMP_Width': 0.35,
    'DUMMY_Width_Min': 0.42,
    'DUMMY_Length_Min': 0.35,
    'Min_Segment_Spacing': 0.28,
    'Ohm/Sq': 6.82,
}
