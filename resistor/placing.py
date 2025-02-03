import gdstk
from calculations import calculate_resistors_parameters,simplify_ratio
from parameter import layer_numbers, drc_params, rnlplus_params
from calculations import assign_resistor_labels,calculate_metal_layer_coords



def create_resistor(start_x, start_y, length, width, layer_numbers, drc_params, rnlplus_params):
    # 校正电阻尺寸
    if width < rnlplus_params['DUMMY_Width_Min']:
        width = rnlplus_params['DUMMY_Width_Min']
        print('RPDUMMY宽度不能小于420nm')

    if length < rnlplus_params['DUMMY_Length_Min']:
        length = rnlplus_params['DUMMY_Length_Min']
        print('RPDUMMY长度不能小于350nm')

    # 创建RPDUMMY层电阻
    rp_dummy = gdstk.rectangle(
        (start_x, start_y),
        (start_x + length, start_y + width),
        layer=layer_numbers['RPDUMMY']
    )

    # 计算通孔
    contact_margin = drc_params['M1E2_Min_M1_CO_Spacing']
    contact_size = drc_params['COW1_Maxmin_CONT_Square']
    contact_spacing = rnlplus_params['CO_CO_Spacing']
    OD_CO_spacing = drc_params['COE1_Min_CONT_OD_Spacing']
    max_contacts_per_side = int((width - 2 * contact_margin + contact_spacing-2*OD_CO_spacing) / (contact_size + contact_spacing))
    start_y_for_contacts = (width - (
                max_contacts_per_side * contact_size + (max_contacts_per_side - 1) * contact_spacing)) / 2 + start_y

    # 创建通孔层CONT
    contacts_left = [
        gdstk.rectangle(
            (start_x - contact_size, start_y_for_contacts + i * (contact_size + contact_spacing)),
            (start_x, start_y_for_contacts + i * (contact_size + contact_spacing) + contact_size),
            layer=layer_numbers['CONT']
        ) for i in range(max_contacts_per_side)
    ]

    contacts_right = [
        gdstk.rectangle(
            (start_x + length, start_y_for_contacts + i * (contact_size + contact_spacing)),
            (start_x + length + contact_size,
             start_y_for_contacts + i * (contact_size + contact_spacing) + contact_size),
            layer=layer_numbers['CONT']
        ) for i in range(max_contacts_per_side)
    ]

    # 创建金属层METAL1
    metal1_left = gdstk.rectangle(
        (start_x - contact_size - contact_margin, start_y_for_contacts - contact_margin),
        (start_x + contact_margin, start_y_for_contacts + max_contacts_per_side * (
                contact_size + contact_spacing) - contact_spacing + contact_margin),
        layer=layer_numbers['METAL1']
    )

    metal1_right = gdstk.rectangle(
        (start_x + length - contact_margin, start_y_for_contacts - contact_margin),
        (start_x + length + contact_size + contact_margin, start_y_for_contacts + max_contacts_per_side * (
                contact_size + contact_spacing) - contact_spacing + contact_margin),
        layer=layer_numbers['METAL1']
    )



    # 创建Diff层和WELLBODY层
    diff_extension = drc_params['Min_Diff_DUMMY_Spacing']
    diff_layer = gdstk.rectangle(
        (start_x - diff_extension, start_y),
        (start_x + length + diff_extension, start_y + width),
        layer=layer_numbers['DIFF']
    )

    wellbody_layer = gdstk.rectangle(
        (start_x - diff_extension, start_y),
        (start_x + length + diff_extension, start_y + width),
        layer=layer_numbers['WELLBODY']
    )

    # 创建NIMP层
    nimp_spacing = rnlplus_params['Spacing_DIFF__NIMP_Width']
    nimp_layer = gdstk.rectangle(
        (start_x - diff_extension - nimp_spacing, start_y - nimp_spacing),
        (start_x + length + diff_extension + nimp_spacing, start_y + width + nimp_spacing),
        layer=layer_numbers['NIMP']
    )

    # 将所有图形添加到单元中
    resistor_cell = gdstk.Cell("RNLPLUS_RESISTOR")
    resistor_cell.add(rp_dummy, diff_layer, wellbody_layer, nimp_layer, *contacts_left, *contacts_right, metal1_left,
                      metal1_right)

    return resistor_cell


def draw_resistor_array(start_x, start_y, res1, res2, layer_numbers, drc_params, rnlplus_params, magnification,layout_style):
    width, length, coordinates = calculate_resistors_parameters(start_x, start_y, res1, res2, rnlplus_params, magnification,layout_style)
    r1_metal_coords, r2_metal_coords = calculate_metal_layer_coords(start_x, start_y, res1, res2, rnlplus_params, drc_params, magnification,layout_style)
    resistor_array_cell = gdstk.Cell("RESISTOR_ARRAY")
    r1_num,r2_num,basic_resistance=simplify_ratio(res1, res2, layout_style)

    for coord_x, coord_y in coordinates:
        resistor_cell = create_resistor(coord_x, coord_y, length, width, layer_numbers, drc_params, rnlplus_params)
        resistor_array_cell.add(*resistor_cell.get_polygons())

    wire_width = 0.34 #！！！！！待修改
    metal_layer = layer_numbers["METAL1"]
    shift_distance = wire_width+drc_params['M1S1_Min_M1_M1_Spacing'] # 待调整

    r1_modify=0
    r2_modify=0
    if (layout_style == "symmetric"):
        if(r1_num % 2==1):
            r1_modify=1
        elif(r2_num % 2==1):
            r2_modify=1



    def create_wiring_line(start, end, layer, shift=0):
        # Shift the wiring accordingly
        start = (start[0] , start[1])
        end = (start[0] , end[1])
        #print(f"Creating wiring line from {start} to {end}")
        vertices = [(start[0]+shift , start[1]), (start[0]+shift + wire_width, start[1]), (end[0]+shift + wire_width, end[1]),(end[0]+shift, end[1])]
        #print(vertices)
        return gdstk.Polygon(vertices, layer=layer)

    def connect_wire_to_cont(start, end, layer, shift=0):

        # Shift the wiring accordingly
        start = (start[0] , start[1])
        end = (start[0] , end[1])
        #print(f"Creating wiring line from {start} to {end}")
        vertices = [(start[0]+shift+wire_width , start[1]), (start[0], start[1]), (end[0], end[1]),(end[0]+shift+wire_width, end[1])]
        #print(vertices)
        return gdstk.Polygon(vertices, layer=layer)

    # Connect Resistor1 metals alternating between left and right
    for i in range(len(r1_metal_coords) - 1):
        if i % 2 == 0:  # Even index, connect left metals
            start = r1_metal_coords[i]['left']['top_left']
            end = r1_metal_coords[i + 1]['left']['bottom_right']
            wiring_line = create_wiring_line(start, end, metal_layer, -shift_distance)
        else:  # Odd index, connect right metals
            start = r1_metal_coords[i]['right']['top_left']
            end = r1_metal_coords[i + 1]['right']['bottom_right']
            wiring_line = create_wiring_line(start, end, metal_layer, -shift_distance-0.06)
        resistor_array_cell.add(wiring_line)

    for i in range(len(r1_metal_coords)):

        start = r1_metal_coords[i]['left']['top_left']
        end = r1_metal_coords[i]['left']['bottom_right']
        connecting_line_left = connect_wire_to_cont(start, end, metal_layer, -shift_distance)

        if (i != 0 and i != len(r1_metal_coords) - 1):
            start = r1_metal_coords[i]['right']['top_left']
            end = r1_metal_coords[i]['right']['bottom_right']
            connecting_line_right = connect_wire_to_cont(start, end, metal_layer, -shift_distance - 0.06)
            resistor_array_cell.add(connecting_line_right)
        resistor_array_cell.add(connecting_line_left)

    # Connect Resistor2 metals alternating between left and right
    for i in range(0, len(r2_metal_coords) -1):  # Start from the second Resistor2
        if i % 2 == 1:  # Odd index, connect left metals
            start = r2_metal_coords[i]['left']['top_left']
            end = r2_metal_coords[i + 1]['left']['bottom_right']
            wiring_line = create_wiring_line(start, end, metal_layer, shift_distance+0.05)
        else:  # Even index (not used based on provided logic)

            start = r2_metal_coords[i]['right']['top_left']
            end = r2_metal_coords[i + 1]['right']['bottom_right']
            wiring_line = create_wiring_line(start, end, metal_layer, shift_distance)
        resistor_array_cell.add(wiring_line)


    for i in range(len(r2_metal_coords)):
        if(i!=len(r2_metal_coords)-r2_modify):#！！！！
            start = r2_metal_coords[i]['right']['top_left']
            end = r2_metal_coords[i]['right']['bottom_right']
            connecting_line_right = connect_wire_to_cont(start, end, metal_layer, shift_distance)
        if(i!=0 and i!=len(r2_metal_coords)-1+r2_modify):#！！！！！
            start = r2_metal_coords[i]['left']['top_left']
            end = r2_metal_coords[i]['left']['bottom_right']
            connecting_line_left = connect_wire_to_cont(start, end, metal_layer, shift_distance)
            resistor_array_cell.add(connecting_line_left)
            #print(start,end)
        resistor_array_cell.add(connecting_line_right)


    return resistor_array_cell
