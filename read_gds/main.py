import gdstk

gds_file_path = r"D:\Users\vivian\Desktop\gdstk_2024\try2\rnlplus_resistor.gds"
library = gdstk.read_gds(gds_file_path)

# 获取所有单元
all_cells = library.cells

# 用来存储所有多边形顶点的列表
all_polygons_vertices = []

# 遍历所有单元中的所有多边形，并收集它们的顶点坐标
for cell in all_cells:
    for polygon in cell.polygons:
        vertices = polygon.points  # 获取多边形的顶点坐标
        all_polygons_vertices.append(vertices)  # 将顶点坐标添加到列表中

# 储存完成后，输出所有多边形的坐标
for i, vertices in enumerate(all_polygons_vertices):
    print(f"矩形{i+1}的顶点坐标: {vertices}")

