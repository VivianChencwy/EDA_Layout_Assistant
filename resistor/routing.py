from calculations import assign_resistor_labels,calculate_resistors_parameters
from parameter import drc_params, rnlplus_params


def calculate_metal_layer_coords(start_x, start_y, res1, res2, rnlplus_params, drc_params, magnification,layout_style):
    # 假设 calculate_resistors_parameters 已经提供了正确的电阻宽度、长度和坐标
    width, length, coordinates = calculate_resistors_parameters(start_x, start_y, res1, res2, rnlplus_params, magnification,layout_style)

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
