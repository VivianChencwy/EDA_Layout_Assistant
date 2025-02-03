from math import gcd,ceil

def calculate_resistor_size(target_resistance, magnification, ohms_per_square, min_width, min_length):
    # 直接使用float进行计算
    width = round(min_width, 2)
    length = round((target_resistance / ohms_per_square) * width, 2)

    # 如果理论长度小于最小长度，则需要增加宽度
    if length < min_length:
        length = round(min_length, 2)
        width = round((ohms_per_square * length) / target_resistance, 2)
    width *= round(magnification, 2)
    length *= round(magnification, 2)
    area = round(width * length, 2)
    actual_resistance = round(ohms_per_square * length / width, 2)
    #print(f"Width: {width}, Length: {length}, Area: {area}, Actual Resistance: {actual_resistance}")
    return width, length, area, actual_resistance

from math import gcd


def simplify_ratio(res1, res2, layout_style):
    # 计算最大公约数
    greatest_common_divisor = gcd(res1, res2)
    # 除以最大公约数简化比例
    res1_num = res1 // greatest_common_divisor
    res2_num = res2 // greatest_common_divisor
    basic_resistance = res1 / res1_num


    #下下策，懒狗不想写两遍布线Modify
    if (res1_num % 2==1):
        temp_num=res1_num
        res1_num=res2_num
        res2_num=temp_num
        temp_res=res1
        res1=res2
        res2=temp_res




    if layout_style == 'symmetric':
        # 对称式，如果都是奇数，则将他们都*2，以保证对称性
        if res1_num % 2 == 1 and res2_num % 2 == 1:
            res1_num = res1_num * 2
            res2_num = res2_num * 2
            basic_resistance = basic_resistance / 2

    elif layout_style == 'symmetric_even':
        # 对称偶数式，确保两者都是偶数
        if res1_num % 2 == 1 or res2_num % 2 == 1:
            res1_num = res1_num * 2
            res2_num = res2_num * 2
            basic_resistance = basic_resistance / 2

    print(f"Resistor 1: {res1_num}, Resistor 2: {res2_num}, Basic Resistance: {basic_resistance}")

    return res1_num, res2_num, basic_resistance


def calculate_resistors_parameters(start_x, start_y, res1, res2, rnlplus_params, magnification,layout_style):
    res1_num, res2_num, basic_resistance = simplify_ratio(res1, res2,layout_style)
    width, length, area, actual_resistance = calculate_resistor_size(
        basic_resistance,magnification,
        rnlplus_params['Ohm/Sq'],
        rnlplus_params['DUMMY_Width_Min'],
        rnlplus_params['DUMMY_Length_Min']
    )

    # 计算所有电阻的坐标
    coordinates = []
    current_y = start_y
    for _ in range(res1_num + res2_num):
        coordinates.append((start_x, current_y))
        current_y += width + rnlplus_params['Min_Segment_Spacing']

    return width, length, coordinates


def assign_resistor_labels(res1, res2, layout_style):
    res1_num, res2_num, _ = simplify_ratio(res1, res2, layout_style)
    total_res = res1_num + res2_num

    labels_for_r1, labels_for_r2 = [], []

    # Check for odd resistor in symmetric layout
    odd_res=0
    odd_in_middle = None
    if layout_style == 'symmetric' and (res1_num % 2 == 1 or res2_num % 2 == 1):
        if res1_num % 2 == 1:
            odd_in_middle = ('R1', total_res // 2 + 1)
            res1_num -= 1  # Adjust for the odd one out
        else:
            odd_in_middle = ('R2', total_res // 2 + 1)
            res2_num -= 1  # Adjust for the odd one out
        total_res -= 1
        odd_res = 1

    # Assign labels for the rest
    major_num, minor_num = max(res1_num, res2_num), min(res1_num, res2_num)
    major_label = 'R1' if res1_num >= res2_num else 'R2'
    minor_label = 'R2' if major_label == 'R1' else 'R1'

    # 对电阻总数 / 2，找到对称轴
    total_res_half = (res1_num + res2_num) // 2
    repeat_value = int((major_num / 2) / (minor_num / 2 + 1)) # 数量较多的电阻的重复值
    if repeat_value == 0:
        repeat_value = 1
    # print("repeat_value:", repeat_value)

    # 初始化标号列表
    labels_for_r1, labels_for_r2 = [], []
    # 在对称轴右边的排列
    major_placed = minor_placed = 0
    position = total_res_half + 1 +odd_res # 从对称轴右侧第一个位置开始

    while major_placed < major_num // 2 or minor_placed < minor_num // 2:
        for _ in range(repeat_value):
            if major_placed < major_num // 2:
                if major_label == 'R1':
                    labels_for_r1.append(position)
                else:
                    labels_for_r2.append(position)
                position += 1
                major_placed += 1
        if minor_placed < minor_num // 2:
            if minor_label == 'R1':
                labels_for_r1.append(position)
            else:
                labels_for_r2.append(position)
            position += 1
            minor_placed += 1

    # 对称轴左边的排列
    labels_for_r1_left = [total_res_half * 2 - x + 1+odd_res for x in labels_for_r1 if x > total_res_half]
    labels_for_r2_left = [total_res_half * 2 - x + 1+odd_res for x in labels_for_r2 if x > total_res_half]
    # print("labels_for_r1_left:", labels_for_r1_left, "labels_for_r2_left:", labels_for_r2_left)
    labels_for_r1 = labels_for_r1_left + [x for x in labels_for_r1 if x > total_res_half]
    labels_for_r2 = labels_for_r2_left + [x for x in labels_for_r2 if x > total_res_half]

    # If there's an odd resistor in the middle, add it to the correct list
    if odd_in_middle:
        if odd_in_middle[0] == 'R1':
            labels_for_r1.append(odd_in_middle[1])
        else:
            labels_for_r2.append(odd_in_middle[1])

    labels_for_r1.sort()
    labels_for_r2.sort()
    print("Resistor1 labels:", labels_for_r1, "Resistor2 labels:", labels_for_r2)

    return labels_for_r1, labels_for_r2

def calculate_metal_layer_coords(start_x, start_y, res1, res2, rnlplus_params, drc_params, magnification,layout_style):
    # 假设 calculate_resistors_parameters 已经提供了正确的电阻宽度、长度和坐标
    width, length, coordinates = calculate_resistors_parameters(start_x, start_y, res1, res2, rnlplus_params, magnification,layout_style)
    print("width:",width,"length:",length,"coordinates:",coordinates)
    # 设计规则参数
    contact_margin = drc_params['M1E2_Min_M1_CO_Spacing']
    contact_size = drc_params['COW1_Maxmin_CONT_Square']
    contact_spacing = rnlplus_params['CO_CO_Spacing']
    OD_CO_spacing = drc_params['COE1_Min_CONT_OD_Spacing']

    metal_coords = []

    for coord_x, coord_y in coordinates:
        # 计算每侧通孔的最大数量
        max_contacts_per_side = int((width - 2 * contact_margin + contact_spacing - 2 * OD_CO_spacing) / (contact_size + contact_spacing))
        # 计算通孔的y坐标起始位置
        start_y_for_contacts = coord_y + (width - (max_contacts_per_side * contact_size + (max_contacts_per_side - 1) * contact_spacing)) / 2

        # 金属层x坐标范围
        metal_x_start = coord_x - contact_size - contact_margin
        metal_x_end = coord_x + length + contact_size + contact_margin
        # 金属层y坐标范围
        metal_y_start = start_y_for_contacts - contact_margin
        metal_y_end = start_y_for_contacts + max_contacts_per_side * contact_size + (max_contacts_per_side - 1) * contact_spacing + contact_margin

        metal_coords.append({
            "left": {
                "top_left": (metal_x_start, metal_y_start),
                "bottom_right": (coord_x, metal_y_end)
            },
            "right": {
                "top_left": (coord_x + length, metal_y_start),
                "bottom_right": (metal_x_end, metal_y_end)
            }
        })

    labels_for_r1, labels_for_r2 = assign_resistor_labels(res1, res2,layout_style)

    r1_metal_coords = [metal_coords[i - 1] for i in labels_for_r1]
    r2_metal_coords = [metal_coords[i - 1] for i in labels_for_r2]

    return r1_metal_coords, r2_metal_coords


