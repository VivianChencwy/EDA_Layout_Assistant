import gdstk
from parameter import layer_numbers, drc_params, rnlplus_params
from placing import draw_resistor_array
from calculations import assign_resistor_labels
from routing import calculate_metal_layer_coords
from calculations import calculate_resistor_size


res1 = 2500
res2 = 3000
magnification = 2.0 # 放大倍数（相对于最小面积）
start_x = 0
start_y = 0
layout_style = 'symmetric'

def main():

    # 分配标签
    #labels_for_r1, labels_for_r2 = assign_resistor_labels(res1, res2)


    # 使用示例
    resistor_array_cell = draw_resistor_array(
        start_x,
        start_y,
        res1=res1,
        res2=res2,
        layer_numbers=layer_numbers,
        drc_params=drc_params, # drc参数
        rnlplus_params=rnlplus_params, # 针对该电阻的一些参数
        magnification=magnification, # 放大倍数（相对于最小面积）
        layout_style = layout_style
    )

    calculate_metal_layer_coords(0, 0, res1, res2, rnlplus_params, drc_params, magnification,layout_style)

    # 创建库并将电阻单元添加到库中
    library = gdstk.Library()
    library.add(resistor_array_cell)

    # 保存GDS文件
    gds_filename = "resistor_array_cell.gds"
    library.write_gds(gds_filename)
    print(f"GDS文件已保存到: {gds_filename}")

if __name__ == "__main__":
    main()
