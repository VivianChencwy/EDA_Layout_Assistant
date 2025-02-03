import math
import random
import gdstk
from math import gcd, ceil, sqrt, exp
import networkx as nx
from heapq import heappop, heappush

# 计算最大公约数
def calculate_gcd(a, b):
    return gcd(a, b)

# 计算最简化单位电容值
def calculate_unit_cap_value(cap1, cap2):
    return calculate_gcd(cap1, cap2)

# 判断是否可以形成正方形阵列
def is_perfect_square(n):
    return int(sqrt(n)) ** 2 == n

# 生成可能的电容阵列
def generate_possible_arrays(total_caps):
    possible_arrays = []
    for cols in range(ceil(sqrt(total_caps)), 1, -1):
        rows = ceil(total_caps / cols)
        if rows * cols >= total_caps:
            dummy_caps = rows * cols - total_caps
            possible_arrays.append((rows, cols, dummy_caps))
    return possible_arrays

# 分配电容标签
def assign_labels_to_array(rows, cols, num_caps1, num_caps2):
    total_caps = num_caps1 + num_caps2
    structure = [[""] * cols for _ in range(rows)]
    remaining_caps1 = num_caps1
    remaining_caps2 = num_caps2

    for r in range(rows):
        count_a = remaining_caps1 // (rows - r)
        count_b = remaining_caps2 // (rows - r)
        remaining_caps1 -= count_a
        remaining_caps2 -= count_b
        row_labels = assign_labels_to_row(count_a, count_b, cols)
        structure[r] = row_labels if r % 2 == 0 else row_labels[::-1]

    return structure

# 排布每一行电容，使其尽量对称且分散
def assign_labels_to_row(count_a, count_b, length):
    row = [""] * length
    total_count = count_a + count_b
    total_half = total_count // 2

    major_num, minor_num = max(count_a, count_b), min(count_a, count_b)
    major_label = 'A' if count_a >= count_b else 'B'
    minor_label = 'B' if major_label == 'A' else 'A'

    use_ceil = False  # 交替使用int和ceil

    major_placed = minor_placed = 0
    position = total_half + 1  # 起始位置

    while major_placed < major_num // 2 or minor_placed < minor_num // 2:
        if major_placed < major_num // 2:
            repeat_value = ceil((major_num / 2) / (minor_num / 2 + 1)) if use_ceil else int(
                (major_num / 2) / (minor_num / 2 + 1))
            for _ in range(repeat_value):
                if major_placed < major_num // 2 and position <= length:
                    row[position - 1] = major_label
                    position += 1
                    major_placed += 1
        if minor_placed < minor_num // 2 and position <= length:
            row[position - 1] = minor_label
            position += 1
            minor_placed += 1
        use_ceil = not use_ceil  # 交替使用int和ceil

    # 分配剩余的电容
    for i in range(length):
        if row[i] == "":
            if major_placed < major_num:
                row[i] = major_label
                major_placed += 1
            else:
                row[i] = minor_label

    return row

# 随机替换部分数量少的电容为D
def replace_minor_with_d(structure, num_d, count_a, count_b):
    rows = len(structure)
    cols = len(structure[0])
    minor_label = 'A' if count_a < count_b else 'B'
    minor_positions = [(r, c) for r in range(rows) for c in range(cols) if structure[r][c] == minor_label]

    if len(minor_positions) < num_d:
        raise ValueError(f"Not enough '{minor_label}' capacitors to replace with 'D'.")

    selected_positions = random.sample(minor_positions, num_d)
    for r, c in selected_positions:
        structure[r][c] = 'D'

    return structure

# 计算质心
def calculate_centroid(structure, label):
    rows = len(structure)
    cols = len(structure[0])
    total_weight = sum((r + 1) * (c + 1) for r in range(rows) for c in range(cols) if structure[r][c] == label)
    count = sum(1 for r in range(rows) for c in range(cols) if structure[r][c] == label)
    return total_weight / count if count != 0 else 0

# 计算总质心差
def total_centroid_diff(structure):
    centroid_a = calculate_centroid(structure, 'A')
    centroid_b = calculate_centroid(structure, 'B')
    centroid_d = calculate_centroid(structure, 'D')
    centroid_ab_diff = abs(centroid_a - centroid_b)
    centroid_ad_diff = abs(centroid_a - centroid_d)
    centroid_bd_diff = abs(centroid_b - centroid_d)
    return centroid_ab_diff + centroid_ad_diff + centroid_bd_diff

# 计算分散性
def dispersion_score(structure):
    def count_repeats(arr):
        return sum(arr[i] == arr[i + 1] for i in range(len(arr) - 1))

    rows = len(structure)
    cols = len(structure[0])
    total_repeats = sum(count_repeats(row) for row in structure) + sum(count_repeats([structure[r][c] for r in range(rows)]) for c in range(cols))
    max_repeats = (rows * (cols - 1)) + (cols * (rows - 1))
    return 1 - (total_repeats / max_repeats)

# 模拟退火算法
def simulated_annealing(structure, initial_temp, cooling_rate, weights):
    current_temp = initial_temp
    current_structure = structure
    best_structure = structure
    best_score = evaluate_structure(structure, weights)

    while current_temp > 1:
        new_structure = swap_elements(current_structure)
        new_score = evaluate_structure(new_structure, weights)
        if new_score > best_score:
            best_structure = new_structure
            best_score = new_score
        else:
            acceptance_prob = exp((new_score - best_score) / current_temp)
            if acceptance_prob > random.random():
                current_structure = new_structure
        current_temp *= cooling_rate

    return best_structure

# 交换两个随机元素的位置
def swap_elements(structure):
    rows = len(structure)
    cols = len(structure[0])
    r1, c1 = random.randint(0, rows - 1), random.randint(0, cols - 1)
    r2, c2 = random.randint(0, rows - 1), random.randint(0, cols - 1)
    new_structure = [row[:] for row in structure]
    new_structure[r1][c1], new_structure[r2][c2] = new_structure[r2][c2], new_structure[r1][c1]
    return new_structure

# 评估结构
def evaluate_structure(structure, weights):
    rows = len(structure)
    cols = len(structure[0])
    dummy_count = sum(row.count('D') for row in structure)
    aspect_ratio = max(rows, cols) / min(rows, cols)
    dispersion = dispersion_score(structure)
    centroid_diff = total_centroid_diff(structure)

    score = (weights['dummy'] * (1 / (1 + dummy_count))) + (weights['square'] * (1 / aspect_ratio)) + (weights['dispersion'] * dispersion) + (weights['centroid'] * (1 / (1 + centroid_diff)))
    return score

# 获取电容位置
def get_capacitor_positions(structure):
    positions = {'A': [], 'B': [], 'D': []}
    for r in range(len(structure)):
        for c in range(len(structure[0])):
            label = structure[r][c]
            positions[label].append((r, c))
    return positions

# 检查路径是否跨越其他电容
def is_valid_path(path, structure, label, cap_width, cap_height, metal_dummy_spacing):
    for (x, y) in path:
        row = int(y // (cap_height + 2 * metal_dummy_spacing))
        col = int(x // (cap_width + 2 * metal_dummy_spacing))
        if structure[row][col] != label and structure[row][col] != 'D':
            return False
    return True

# 生成曼哈顿路径
def manhattan_path(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    path = []
    if x1 == x2 or y1 == y2:
        path = [(x1, y1), (x2, y2)]
    else:
        path = [(x1, y1), (x1, y2), (x2, y2)]
    return path

# 生成电容连接
def generate_connections(structure, cap_width, cap_height, metal_dummy_spacing):
    positions = get_capacitor_positions(structure)
    connections = {'A': [], 'B': [], 'D': []}

    for label in ['A', 'B', 'D']:
        if len(positions[label]) > 1:
            graph = nx.Graph()
            for i in range(len(positions[label])):
                for j in range(i + 1, len(positions[label])):
                    p1 = positions[label][i]
                    p2 = positions[label][j]
                    distance = abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])
                    graph.add_edge(p1, p2, weight=distance)
            mst = nx.minimum_spanning_tree(graph)

            for (p1, p2) in mst.edges():
                path = manhattan_path((p1[1] * (cap_width + 2 * metal_dummy_spacing) + cap_width / 2, p1[0] * (cap_height + 2 * metal_dummy_spacing) + cap_height / 2),
                                      (p2[1] * (cap_width + 2 * metal_dummy_spacing) + cap_width / 2, p2[0] * (cap_height + 2 * metal_dummy_spacing) + cap_height / 2))
                if is_valid_path(path, structure, label, cap_width, cap_height, metal_dummy_spacing):
                    connections[label].append((p1, p2))

    return connections

# 创建 MIM 电容阵列
def create_mim_capacitor_array(structure, connections, cap_width=10, cap_height=10):
    # Define the layers
    layers = {
        'METAL5': 33,
        'METAL6': 38,
        'VIA56': 39,
        'CTM5': 67,
        'CTMDUMMY': 131,
        'CTMDUMMY_dr4': (131, 20),
        'TEXT': 59,
    }

    # Define the used parameters
    mimcap_params = {
        'VIA_VIA_Spacing': 2,
        'VIA_Width': 0.36,
        'Metal_Dif': 0.4,
        'Metal_DUMMY_Spacing': 2,
        'Line_Width': 0.28  # 新增
    }

    # Create a new GDSII library
    lib = gdstk.Library()

    # Create a cell for the MIM capacitor array
    cell = lib.new_cell('MIM_CAP_ARRAY')

    rows = len(structure)
    cols = len(structure[0])

    for r in range(rows):
        for c in range(cols):
            x_offset = c * (cap_width + 2 * mimcap_params['Metal_DUMMY_Spacing'])
            y_offset = r * (cap_height + 2 * mimcap_params['Metal_DUMMY_Spacing'])

            # Define the coordinates for the METAL6 layer (previously METAL5)
            metal6_coords = [
                (x_offset, y_offset),
                (x_offset + cap_width, y_offset),
                (x_offset + cap_width, y_offset + cap_height),
                (x_offset, y_offset + cap_height)
            ]

            # Create the METAL6 layer polygon (previously METAL5)
            metal6 = gdstk.Polygon(metal6_coords, layer=layers['METAL6'])

            # Define the coordinates for the METAL5 layer (previously METAL6)
            metal5_coords = [
                (x_offset - mimcap_params['Metal_Dif'], y_offset - mimcap_params['Metal_Dif']),
                (x_offset + cap_width + mimcap_params['Metal_Dif'], y_offset - mimcap_params['Metal_Dif']),
                (x_offset + cap_width + mimcap_params['Metal_Dif'], y_offset + cap_height + mimcap_params['Metal_Dif']),
                (x_offset - mimcap_params['Metal_Dif'], y_offset + cap_height + mimcap_params['Metal_Dif'])
            ]
            metal5 = gdstk.Polygon(metal5_coords, layer=layers['METAL5'])

            # Create the VIA56 layer (arranged in a grid)
            vias = []
            via_spacing = mimcap_params['VIA_VIA_Spacing']
            via_width = mimcap_params['VIA_Width']
            num_vias_x = int(cap_width / (via_width + via_spacing))
            num_vias_y = int(cap_height / (via_width + via_spacing))

            # Calculate offsets to center the vias
            x_via_offset = x_offset + (cap_width - (num_vias_x * (via_width + via_spacing) - via_spacing)) / 2
            y_via_offset = y_offset + (cap_height - (num_vias_y * (via_width + via_spacing) - via_spacing)) / 2

            for i in range(num_vias_x):
                for j in range(num_vias_y):
                    x = x_via_offset + i * (via_width + via_spacing)
                    y = y_via_offset + j * (via_width + via_spacing)
                    if x + via_width <= x_offset + cap_width and y + via_width <= y_offset + cap_height:
                        via_coords = [
                            (x, y),
                            (x + via_width, y),
                            (x + via_width, y + via_width),
                            (x, y + via_width)
                        ]
                        via56 = gdstk.Polygon(via_coords, layer=layers['VIA56'])
                        vias.append(via56)

            # CTM5 layer coincides with METAL6, using layer 67 and datatype 5
            ctm5 = gdstk.Polygon(metal6_coords, layer=layers['CTM5'], datatype=5)

            # CTMDUMMY layer centered on CTM5, with spacing
            ctmdummy_coords = [
                (x_offset - mimcap_params['Metal_DUMMY_Spacing'], y_offset - mimcap_params['Metal_DUMMY_Spacing']),
                (x_offset + cap_width + mimcap_params['Metal_DUMMY_Spacing'], y_offset - mimcap_params['Metal_DUMMY_Spacing']),
                (x_offset + cap_width + mimcap_params['Metal_DUMMY_Spacing'], y_offset + cap_height + mimcap_params['Metal_DUMMY_Spacing']),
                (x_offset - mimcap_params['Metal_DUMMY_Spacing'], y_offset + cap_height + mimcap_params['Metal_DUMMY_Spacing'])
            ]
            ctmdummy = gdstk.Polygon(ctmdummy_coords, layer=layers['CTMDUMMY'])

            # CTMDUMMY_dr4 layer coincides with CTMDUMMY
            ctmdummy_dr4 = gdstk.Polygon(ctmdummy_coords, layer=layers['CTMDUMMY_dr4'][0], datatype=layers['CTMDUMMY_dr4'][1])

            # Add text label to the center of the capacitor
            label = structure[r][c]
            text_polygons = gdstk.text(label, size=10, position=(x_offset, y_offset), layer=layers['TEXT'])

            # Add all elements to the cell
            cell.add(metal6, metal5, *vias, ctm5, ctmdummy, ctmdummy_dr4, *text_polygons)

    # Add connections
    for label in connections:
        for (p1, p2) in connections[label]:
            x1, y1 = p1[1] * (cap_width + 2 * mimcap_params['Metal_DUMMY_Spacing']) + cap_width / 2, p1[0] * (cap_height + 2 * mimcap_params['Metal_DUMMY_Spacing']) + cap_height / 2
            x2, y2 = p2[1] * (cap_width + 2 * mimcap_params['Metal_DUMMY_Spacing']) + cap_width / 2, p2[0] * (cap_height + 2 * mimcap_params['Metal_DUMMY_Spacing']) + cap_height / 2

            path = manhattan_path((x1, y1), (x2, y2))
            if is_valid_path(path, structure, label, cap_width, cap_height, mimcap_params['Metal_DUMMY_Spacing']):
                flexpath = gdstk.FlexPath(path, width=mimcap_params['Line_Width'], layer=layers['METAL5'])
                cell.add(flexpath)
            else:
                # Handle rerouting
                for new_path in reroute_path(p1, p2, structure, label, cap_width, cap_height, metal_dummy_spacing):
                    if is_valid_path(new_path, structure, label, cap_width, cap_height, metal_dummy_spacing):
                        flexpath = gdstk.FlexPath(new_path, width=mimcap_params['Line_Width'], layer=layers['METAL5'])
                        cell.add(flexpath)

    # Save the library to a GDSII file
    lib.write_gds('mim_cap_array.gds')

    print("MIM capacitor array layout with connections saved to 'mim_cap_array.gds'")

# 重新规划路径以绕过非同组电容
def reroute_path(p1, p2, structure, label, cap_width, cap_height, metal_dummy_spacing):
    x1, y1 = p1[1] * (cap_width + 2 * metal_dummy_spacing) + cap_width / 2, p1[0] * (cap_height + 2 * metal_dummy_spacing) + cap_height / 2
    x2, y2 = p2[1] * (cap_width + 2 * metal_dummy_spacing) + cap_width / 2, p2[0] * (cap_height + 2 * metal_dummy_spacing) + cap_height / 2

    rerouted_paths = []

    # Try vertical then horizontal
    rerouted_paths.append([(x1, y1), (x1, y2), (x2, y2)])

    # Try horizontal then vertical
    rerouted_paths.append([(x1, y1), (x2, y1), (x2, y2)])

    return rerouted_paths

# 创建 MIM 电容
def create_mim_capacitor(cap1, cap2, initial_temp=1000, cooling_rate=0.95, weights=None):
    if weights is None:
        weights = {'dummy': 1.0, 'square': 1.0, 'dispersion': 1.0, 'centroid': 1.0}

    unit_cap_value = calculate_unit_cap_value(cap1, cap2)
    num_caps1 = cap1 // unit_cap_value
    num_caps2 = cap2 // unit_cap_value
    total_caps = num_caps1 + num_caps2

    best_structure = None
    best_score = float('-inf')
    possible_arrays = generate_possible_arrays(total_caps)

    for rows, cols, dummy_caps in possible_arrays:
        structure = assign_labels_to_array(rows, cols, num_caps1, num_caps2)
        structure = replace_minor_with_d(structure, dummy_caps, num_caps1, num_caps2)  # 替换数量少的电容为D
        optimized_structure = simulated_annealing(structure, initial_temp, cooling_rate, weights)
        score = evaluate_structure(optimized_structure, weights)

        print("电容阵列:")
        for row in optimized_structure:
            print(" ".join(row))
        print(f"行数: {rows}, 列数: {cols}")
        print(f"dummy 数: {dummy_caps}")
        print(f"得分: {score}\n")

        if score > best_score:
            best_score = score
            best_structure = optimized_structure

    # 输出结果
    print(f"最优单位电容值: {unit_cap_value}")
    print(f"第一个电容值 {cap1} 的匹配单元电容数: {num_caps1}")
    print(f"第二个电容值 {cap2} 的匹配单元电容数: {num_caps2}")
    print("最优的电容阵列:")

    for row in best_structure:
        print(" ".join(row))

    # 生成最优电容阵列的 GDS 文件
    connections = generate_connections(best_structure, cap_width=10, cap_height=10, metal_dummy_spacing=2)
    create_mim_capacitor_array(best_structure, connections)

if __name__ == "__main__":
    cap1 = 450  # 第一个电容值
    cap2 = 200  # 第二个电容值
    initial_temp = 1000
    cooling_rate = 0.99
    weights = {'dummy': 1.0, 'square': 1.0, 'dispersion': 1.0, 'centroid': 1.0}
    create_mim_capacitor(cap1, cap2, initial_temp, cooling_rate, weights)
