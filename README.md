# EDA Layout Assistant

This is an **automated layout generation tool for analog integrated circuit matching**, focusing on precise matching layout design for resistors and capacitors. Implemented with Python and the `gdstk` library, this tool optimizes device layouts to reduce process variations and improve circuit performance.

## Features

- **Automated Layout Generation**: Creates optimized resistor and capacitor layouts using matching rules and heuristic algorithms
- **Resistor Matching**: Supports interdigitated structures, symmetric arrangements, and user-defined parameters
- **Capacitor Matching**: Uses 2D arrays with simulated annealing algorithm for dispersion optimization
- **Layout Validation**: Tests mismatch rates under process variations through Monte Carlo simulations
- **EDA Integration**: Outputs GDSII files compatible with IC design workflows

## Core Module Usage Guide

### 1. Capacitor Array Generator (`capacitor/main.py`)

**Function**: Generates optimized layout for MIM capacitor arrays

**How to Run**:
```bash
cd capacitor
python main.py
```

**Parameter Configuration**:
```python
cap1 = 450  # First capacitor value (fF)
cap2 = 200  # Second capacitor value (fF)
initial_temp = 1000  # Simulated annealing initial temperature
cooling_rate = 0.99  # Cooling rate
weights = {'dummy': 1.0, 'square': 1.0, 'dispersion': 1.0, 'centroid': 1.0}  # Optimization weights
```

**Expected Results**:
- Automatically calculates optimal unit capacitor value and array dimensions
- Outputs optimized capacitor array layout matrix
- Generates `mim_cap_array.gds` file with complete layout information
- Displays array configuration scores and performance metrics
- Capacitors automatically connected through minimum spanning tree algorithm

**Output Example**:
```
Optimal unit capacitor value: 50
Number of unit capacitors for first capacitor value 450: 9
Number of unit capacitors for second capacitor value 200: 4
Optimal capacitor array:
A A B A
A D B A
B A A B
```
### 2. Resistor Array Generator (`resistor/main.py`)

**Function**: Generates precise layout for matching resistor arrays

**How to Run**:
```bash
cd resistor
python main.py
```

**Parameter Configuration**:
```python
res1 = 2500  # First resistor value (Ω)
res2 = 3000  # Second resistor value (Ω)
magnification = 2.0  # Magnification factor (relative to minimum area)
layout_style = 'symmetric'  # Layout style: 'symmetric' or 'even_segment'
start_x = 0  # Starting X coordinate
start_y = 0  # Starting Y coordinate
```

**Expected Results**:
- Automatically calculates optimal resistor geometric dimensions
- Generates resistor layout compliant with DRC rules
- Applies matching rules to ensure resistor symmetry
- Generates `resistor_array_cell.gds` file
- Automatically calculates and generates metal layer connections
- Supports multiple layout style options

**Output Example**:
```
GDS file saved to: resistor_array_cell.gds
Resistor array generated with matching R1 and R2 resistors
Layout style: symmetric
Magnification factor: 2.0x
```
### 3. GDS File Reader (`read_gds/main.py`)

**Function**: Reads existing GDS files and extracts vertex coordinates of all polygons

**How to Run**:
```bash
cd read_gds
python main.py
```

**Pre-configuration Required**:
Modify the file path in the code:
```python
gds_file_path = r"your_gds_file_path.gds"  # Replace with actual GDS file path
```

**Expected Results**:
- Reads specified GDS file
- Parses polygon objects in all cells
- Outputs complete vertex coordinate lists for each polygon
- Used for layout analysis, verification, or format conversion

**Output Example**:
```
Polygon 1 vertex coordinates: [(0.0, 0.0), (10.0, 0.0), (10.0, 5.0), (0.0, 5.0)]
Polygon 2 vertex coordinates: [(15.0, 0.0), (25.0, 0.0), (25.0, 5.0), (15.0, 5.0)]
...
```



## Technical Architecture

- **Python**: Core programming language
- **gdstk**: GDSII file generation and polygon drawing
- **Simulated Annealing**: Optimizes capacitor array dispersion
- **Monte Carlo Simulation**: Evaluates layout performance

## Matching Rules

- **Resistors**: Identical geometries, same material, aligned orientation, interdigitated arrays
- **Capacitors**: Square designs, same material, aligned centroids, cross-coupled arrays

## Workflow

1. Define resistor/capacitor values and layout preferences
2. Generate optimal matching layouts using heuristic algorithms
3. Output GDSII files for resistors (symmetric or even-segment) and capacitors (2D arrays)
4. Validate mismatch rates through Monte Carlo simulations

## Performance Results

- **Resistors**: Reduced average mismatch by 37.5% and standard deviation by 14.3% compared to Cadence Virtuoso standard layouts
- **Capacitors**: Improved standard deviation by 48.9%, but parasitic capacitance from manual routing increased average mismatch
- **Efficiency**: Significantly shortened design cycles compared to manual methods
