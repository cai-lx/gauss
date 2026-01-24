import os
import re
import subprocess
import time
import shutil
import csv
import math

# 配置参数
OPTIMIZATION_METHOD = "b3lyp/6-31g(d,p) em=gd3bj opt=maxcycle=100 freq"
AVAILABLE_METHODS = [
    "CCSD(T)/cc-pVTZ",
    "CCSD(T)/cc-pVDZ", 
    "M062X/def2TZVP em=gd3",#csv提取正常
    "WB97XD/6-311++G(2d,2p)",#含色散矫正
    "B3LYP/6-31G(d,p) em=gd3bj",
    "HF/6-31G(d)"
]
WAIT_TIME = 0.5  # 秒
ENERGY_CONVERSION_FACTOR = 2625.5  # Hartree to kJ/mol
GAUSSIAN_DIR = r"D:\1zmqy\Gauss\Gauss\G16W"

def find_gjf_files(root_dir):
    """查找所有.gjf文件"""
    gjf_files = []
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file.lower().endswith('.gjf'):
                gjf_files.append(os.path.join(root, file))
    return gjf_files

def find_optimized_gjf_files(root_dir):
    """查找已优化的.gjf文件"""
    optimized_files = []
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file.lower().endswith('_optimized.gjf'):
                optimized_files.append(os.path.join(root, file))
    return optimized_files

def extract_calculation_info(gjf_content):
    """从.gjf文件中提取计算信息"""
    lines = gjf_content.split('\n')
    for line in lines:
        line = line.strip()
        if line.startswith('#'):
            return line[1:].strip()
    return "Unknown"

def update_gjf_method(gjf_content, new_method):
    """更新.gjf文件中的计算方法，保留BSSE相关的counter关键词"""
    lines = gjf_content.split('\n')
    updated_lines = []
    route_section_found = False
    
    for i, line in enumerate(lines):
        if line.startswith('#'):
            # 提取原route line中的counter关键词（如果有）
            original_route = line[1:].strip()
            
            # 检查原route line中是否有counter关键词
            counter_match = re.search(r'counter=(\d+)', original_route)
            counter_keyword = ""
            if counter_match:
                counter_keyword = f" counter={counter_match.group(1)}"
            
            # 检查新方法中是否已经包含counter关键词
            new_method_has_counter = 'counter=' in new_method
            
            # 如果原route有counter而新方法没有，则添加counter
            if counter_match and not new_method_has_counter:
                updated_lines.append(f"# {new_method}{counter_keyword}")
            else:
                # 否则直接使用新方法（可能已经包含counter）
                updated_lines.append(f"# {new_method}")
            
            route_section_found = True
        else:
            updated_lines.append(line)
    
    if not route_section_found and len(lines) > 2:
        updated_lines.insert(1, f"# {new_method}")
    
    return '\n'.join(updated_lines)

def create_gaussian_script(gjf_path, new_method=None):
    """为Gaussian计算创建脚本"""
    with open(gjf_path, 'r', encoding='utf-8') as f:
        original_content = f.read()
    
    if new_method:
        gjf_content = update_gjf_method(original_content, new_method)
    else:
        gjf_content = original_content
    
    dir_path = os.path.dirname(gjf_path)
    base_name = os.path.splitext(os.path.basename(gjf_path))[0]
    
    if new_method:
        method_safe = new_method.replace('/', '_').replace(' ', '_').replace('(', '').replace(')', '').replace('=', '')
        new_gjf_name = f"{base_name}_{method_safe}.gjf"
    else:
        new_gjf_name = f"{base_name}_calc.gjf"
    
    new_gjf_path = os.path.join(dir_path, new_gjf_name)
    
    with open(new_gjf_path, 'w', encoding='utf-8', newline='\n') as f:
        f.write(gjf_content)
    
    if new_method:
        out_filename = f"{base_name}_{method_safe}.out"
    else:
        out_filename = f"{base_name}.out"
    
    output_path = os.path.join(dir_path, out_filename)
    
    return new_gjf_path, output_path

def setup_gaussian_environment():
    """设置Gaussian环境变量"""
    if not os.path.exists(GAUSSIAN_DIR):
        print(f"错误: Gaussian目录不存在: {GAUSSIAN_DIR}")
        return False
    
    os.environ['GAUSS_EXEDIR'] = GAUSSIAN_DIR
    os.environ['g16root'] = GAUSSIAN_DIR
    
    old_path = os.environ.get('PATH', '')
    if GAUSSIAN_DIR not in old_path:
        os.environ['PATH'] = f"{GAUSSIAN_DIR};{old_path}"
    
    return True

def run_gaussian_calculation(gjf_path, new_method=None):
    """运行单个Gaussian计算"""
    input_gjf, output_path = create_gaussian_script(gjf_path, new_method)
    work_dir = os.path.dirname(input_gjf)
    
    try:
        gaussian_path = r"D:\1zmqy\Gauss\Gauss\G16W\g16.exe"
        
        if not os.path.exists(gaussian_path):
            print(f"错误: Gaussian可执行文件不存在!")
            return False, output_path
        
        cmd = f'"{gaussian_path}" "{input_gjf}" "{output_path}"'
        
        env = os.environ.copy()
        env['GAUSS_EXEDIR'] = GAUSSIAN_DIR
        env['g16root'] = GAUSSIAN_DIR
        old_path = env.get('PATH', '')
        env['PATH'] = f"{GAUSSIAN_DIR};{old_path}"
        
        start_time = time.time()
        process = subprocess.Popen(
            cmd,
            shell=True,
            cwd=work_dir,
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        timeout = 100000
        try:
            stdout, stderr = process.communicate(timeout=timeout)
            
            if process.returncode == 0:
                elapsed_time = time.time() - start_time
                print(f"计算成功完成! 耗时: {elapsed_time:.2f}秒")
                
                if os.path.exists(output_path):
                    print(f"输出文件已生成: {output_path}")
                    return True, output_path
                else:
                    print(f"警告: 输出文件未生成: {output_path}")
                    return False, output_path
            else:
                print(f"计算失败，返回码: {process.returncode}")
                if stderr:
                    print(f"标准错误: {stderr}")
                return False, output_path
                
        except subprocess.TimeoutExpired:
            print(f"计算超时 (超过{timeout}秒)")
            process.kill()
            return False, output_path
            
    except Exception as e:
        print(f"执行计算时出错: {str(e)}")
        return False, output_path

def extract_optimized_geometry_from_out(out_file_path):
    """从优化输出文件中提取最终优化的几何结构"""
    with open(out_file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    lines = content.split('\n')
    coord_start_idx = -1
    
    for i in range(len(lines)-1, -1, -1):
        if 'Input orientation:' in lines[i] or 'Standard orientation:' in lines[i]:
            coord_start_idx = i
            break
    
    if coord_start_idx == -1:
        print("未能在输出文件中找到坐标信息")
        return None
    
    atom_coords = []
    for i in range(coord_start_idx + 5, len(lines)):
        line = lines[i].strip()
        
        if not line:
            continue
        elif 'Distance matrix' in line or 'Rotational constants' in line:
            break
        elif '--' in line or '------------' in line:
            continue
        else:
            parts = line.split()
            if len(parts) >= 5:
                try:
                    atom_num = int(parts[1])
                    x = float(parts[3])
                    y = float(parts[4])
                    z = float(parts[5])
                    atom_coords.append((atom_num, x, y, z))
                except (ValueError, IndexError):
                    continue
    
    if not atom_coords:
        print("未能解析到原子坐标")
        return None
    
    gjf_path = out_file_path.replace('.out', '.gjf')
    if not os.path.exists(gjf_path):
        print(f"找不到对应的.gjf文件: {gjf_path}")
        return None
    
    with open(gjf_path, 'r', encoding='utf-8') as f:
        original_lines = f.readlines()
    
    route_section = []
    title_section = []
    charge_multiplicity = []
    after_molecule = []
    
    section = "route"
    for line in original_lines:
        stripped = line.strip()
        
        if section == "route" and stripped:
            route_section.append(line.rstrip())
        elif section == "route" and not stripped:
            section = "title"
            title_section.append(line.rstrip())
        elif section == "title" and len(title_section) < 2:
            title_section.append(line.rstrip())
        elif section == "title" and not stripped:
            section = "charge_mult"
            charge_multiplicity.append(line.rstrip())
        elif section == "charge_mult" and len(charge_multiplicity) == 1:
            charge_multiplicity.append(line.rstrip())
        elif section == "charge_mult" and not stripped:
            section = "molecule"
        elif section == "molecule":
            if not stripped:
                section = "after_molecule"
                after_molecule.append(line.rstrip())
        elif section == "after_molecule":
            after_molecule.append(line.rstrip())
    
    new_gjf_content = []
    new_gjf_content.extend(route_section)
    new_gjf_content.extend(title_section)
    new_gjf_content.extend(charge_multiplicity)
    
    atomic_symbols = {
        1: 'H', 2: 'He', 3: 'Li', 4: 'Be', 5: 'B', 6: 'C', 7: 'N', 8: 'O',
        9: 'F', 10: 'Ne', 11: 'Na', 12: 'Mg', 13: 'Al', 14: 'Si', 15: 'P',
        16: 'S', 17: 'Cl', 18: 'Ar', 19: 'K', 20: 'Ca', 21: 'Sc', 22: 'Ti',
        23: 'V', 24: 'Cr', 25: 'Mn', 26: 'Fe', 27: 'Co', 28: 'Ni', 29: 'Cu',
        30: 'Zn', 31: 'Ga', 32: 'Ge', 33: 'As', 34: 'Se', 35: 'Br', 36: 'Kr'
    }
    
    for atom_num, x, y, z in atom_coords:
        element_symbol = atomic_symbols.get(atom_num, 'X')
        new_gjf_content.append(f"{element_symbol}                  {x:>12.8f}    {y:>12.8f}    {z:>12.8f}")
    
    new_gjf_content.append("")
    new_gjf_content.extend(after_molecule[1:])
    gjf_content = '\n'.join(new_gjf_content)
    gjf_content += '\n\n'
    
    return gjf_content

def has_imaginary_frequency(out_file_path):
    """检查输出文件中是否有虚频"""
    with open(out_file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    lines = content.split('\n')
    freq_section = False
    
    for line in lines:
        if 'Frequencies --' in line:
            freq_section = True
            freq_values = re.findall(r'-?\d+\.\d+', line)
            for freq_val in freq_values:
                if float(freq_val) < 0:
                    return True, float(freq_val)
        elif freq_section and ('Frequencies --' not in line) and (not line.strip().startswith(' ')):
            freq_section = False
    
    return False, None

def run_optimization_and_check_freq(gjf_path):
    """执行几何优化和频率计算，并检查虚频"""
    print(f"正在进行几何优化和频率计算: {os.path.basename(gjf_path)}")
    
    with open(gjf_path, 'r', encoding='utf-8') as f:
        original_content = f.read()
    
    opt_freq_content = update_gjf_method(original_content, OPTIMIZATION_METHOD)
    
    dir_path = os.path.dirname(gjf_path)
    base_name = os.path.splitext(os.path.basename(gjf_path))[0]
    opt_gjf_name = f"{base_name}_opt_freq.gjf"
    opt_gjf_path = os.path.join(dir_path, opt_gjf_name)
    
    with open(opt_gjf_path, 'w', encoding='utf-8', newline='\n') as f:
        f.write(opt_freq_content)
    
    success, output_path = run_gaussian_calculation(opt_gjf_path, None)
    
    if not success:
        print(f"优化和频率计算失败: {gjf_path}")
        return False, None, None
    
    has_imag_freq, imag_freq_value = has_imaginary_frequency(output_path)
    
    if has_imag_freq:
        print(f"发现虚频: {gjf_path}, 虚频值: {imag_freq_value} cm-1")
        return True, output_path, imag_freq_value
    else:
        print(f"无虚频: {gjf_path}, 可继续后续计算")
        optimized_gjf_content = extract_optimized_geometry_from_out(output_path)
        if optimized_gjf_content:
            optimized_gjf_path = os.path.join(dir_path, f"{base_name}_optimized.gjf")
            with open(optimized_gjf_path, 'w', encoding='utf-8') as f:
                f.write(optimized_gjf_content)
            print(f"已保存优化后的几何结构: {optimized_gjf_path}")
            return False, optimized_gjf_path, None
        else:
            print(f"无法提取优化后的几何结构: {gjf_path}")
            return False, None, None

def extract_number_from_filename(filename):
    """从文件名中提取数字部分"""
    basename = os.path.basename(filename)
    # 提取第一个下划线后的数字
    match = re.search(r'_(\d+)', basename)
    if match:
        return int(match.group(1))
    return 1

def calculate_distance(coord1, coord2):
    """计算两个坐标之间的距离"""
    x1, y1, z1 = coord1
    x2, y2, z2 = coord2
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2 + (z2 - z1)**2)

def cluster_atoms(coordinates, n_fragments):
    """根据原子之间的距离将原子聚类为片段"""
    n_atoms = len(coordinates)
    
    # 初始化每个原子为一个单独的片段
    fragments = [[i] for i in range(n_atoms)]
    
    # 计算所有原子对之间的距离
    distances = []
    for i in range(n_atoms):
        for j in range(i+1, n_atoms):
            dist = calculate_distance(coordinates[i], coordinates[j])
            distances.append((dist, i, j))
    
    # 按距离排序
    distances.sort(key=lambda x: x[0])
    
    # 合并距离最近的原子，直到达到目标片段数
    while len(fragments) > n_fragments:
        if not distances:
            break
        
        # 找到最小距离且在不同片段中的原子对
        for dist, i, j in distances:
            # 查找i和j所在的片段
            frag_i = next((f for f in fragments if i in f), None)
            frag_j = next((f for f in fragments if j in f), None)
            
            if frag_i and frag_j and frag_i != frag_j:
                # 合并片段
                merged_frag = frag_i + frag_j
                fragments.remove(frag_i)
                fragments.remove(frag_j)
                fragments.append(merged_frag)
                break
        
        # 重新计算距离（简化处理：移除已处理的最近距离）
        if distances:
            distances.pop(0)
    
    # 为每个原子分配片段编号
    atom_fragments = [0] * n_atoms
    for frag_idx, frag in enumerate(fragments):
        for atom_idx in frag:
            atom_fragments[atom_idx] = frag_idx + 1
    
    return atom_fragments

def convert_to_bsse_format(gjf_content, n_mer):
    """将普通GJF文件转换为BSSE矫正格式"""
    lines = gjf_content.strip().split('\n')
    
    # 解析原文件
    route_line = None
    title_line = None
    charge_mult_line = None
    coord_start = None
    
    for i, line in enumerate(lines):
        if line.startswith('#') and route_line is None:
            route_line = line
        elif route_line is not None and title_line is None and line.strip() == '':
            continue
        elif route_line is not None and title_line is None:
            title_line = line
        elif title_line is not None and charge_mult_line is None and line.strip() == '':
            continue
        elif title_line is not None and charge_mult_line is None:
            charge_mult_line = line
            coord_start = i + 1
            break
    
    # 提取原子坐标和元素
    atoms = []
    coordinates = []
    for i in range(coord_start, len(lines)):
        line = lines[i].strip()
        if not line:
            break
        parts = line.split()
        if len(parts) >= 4:
            atom = parts[0]
            x = float(parts[1])
            y = float(parts[2])
            z = float(parts[3])
            atoms.append(atom)
            coordinates.append((x, y, z))
    
    # 如果是单体，不需要BSSE矫正
    if n_mer == 1:
        return gjf_content
    
    # 聚类原子到片段
    atom_fragments = cluster_atoms(coordinates, n_mer)
    
    # 构建新的BSSE格式内容
    new_lines = []
    
    # 修改计算级别行，添加counter参数
    if route_line:
        route_text = route_line[1:].strip()  # 去掉开头的#
        # 检查是否已经有counter关键词
        if 'counter=' not in route_text:
            route_text = route_text.rstrip()
            route_text += f' counter={n_mer}'
        else:
            # 如果已有counter，确保它是正确的
            # 移除旧的counter并添加新的
            route_text = re.sub(r'counter=\d+', f'counter={n_mer}', route_text)
        
        new_lines.append(f"# {route_text}")
    else:
        # 如果没有route line，创建一个默认的
        new_lines.append(f"# def2tzvp em=gd3 m062x counter={n_mer}")
    
    new_lines.append('')
    new_lines.append(title_line if title_line else 'Title Card Required')
    new_lines.append('')
    
    # 构建新的电荷与自旋多重度行
    if n_mer == 2:
        new_charge_mult = '0 1 0 1 0 1'  # 二聚体：整体 + 2个单体
    elif n_mer == 3:
        new_charge_mult = '0 1 0 1 0 1 0 1'  # 三聚体：整体 + 3个单体
    else:
        # 对于更多聚体，扩展模式
        groups = ['0 1'] * (n_mer + 1)
        new_charge_mult = ' '.join(groups)
    
    new_lines.append(new_charge_mult)
    
    # 添加原子坐标，包含片段标签
    for i, (atom, coord, frag) in enumerate(zip(atoms, coordinates, atom_fragments)):
        x, y, z = coord
        if n_mer > 1:
            # 移除原子标签中可能已有的括号
            clean_atom = re.sub(r'\(.*?\)', '', atom).strip()
            new_line = f"{clean_atom}(Fragment={frag})     {x:>12.8f}    {y:>12.8f}    {z:>12.8f}"
        else:
            new_line = f"{atom}                  {x:>12.8f}    {y:>12.8f}    {z:>12.8f}"
        new_lines.append(new_line)
    
    # 添加两个换行符
    new_lines.append('')
    new_lines.append('')
    
    return '\n'.join(new_lines)

def create_bsse_gjf_file(gjf_path, n_mer):
    """创建BSSE矫正的GJF文件"""
    with open(gjf_path, 'r', encoding='utf-8') as f:
        original_content = f.read()
    
    bsse_content = convert_to_bsse_format(original_content, n_mer)
    
    # 保存新的GJF文件
    dir_path = os.path.dirname(gjf_path)
    base_name = os.path.splitext(os.path.basename(gjf_path))[0]
    
    # 移除可能存在的_optimized后缀
    if base_name.endswith('_optimized'):
        base_name = base_name[:-10]
    
    bsse_gjf_name = f"{base_name}_bsse.gjf"
    bsse_gjf_path = os.path.join(dir_path, bsse_gjf_name)
    
    with open(bsse_gjf_path, 'w', encoding='utf-8', newline='\n') as f:
        f.write(bsse_content)
    
    print(f"已创建BSSE矫正文件: {bsse_gjf_path}")
    return bsse_gjf_path

def perform_method_calculations(gjf_path, methods_list, use_bsse=False):
    """对给定的.gjf文件执行多种方法的计算"""
    print(f"开始对 {os.path.basename(gjf_path)} 执行多种方法计算")
    
    base_name = os.path.splitext(os.path.basename(gjf_path))[0]
    
    for method in methods_list:
        method_folder = os.path.join(os.path.dirname(gjf_path), method.replace('/', '_').replace(' ', '_').replace('=', ''))
        os.makedirs(method_folder, exist_ok=True)
        
        print(f"执行计算方法: {method}")
        
        # 如果需要BSSE矫正，创建相应的GJF文件
        if use_bsse:
            # 提取文件名中的数字
            n_mer = extract_number_from_filename(gjf_path)
            if n_mer > 1:  # 只有多聚体需要BSSE矫正
                bsse_gjf_path = create_bsse_gjf_file(gjf_path, n_mer)
                # 对BSSE文件进行计算
                success, output_path = run_gaussian_calculation(bsse_gjf_path, method)
                
                if success and output_path:
                    method_safe = method.replace('/', '_').replace(' ', '_').replace('(', '').replace(')', '').replace('=', '')
                    new_output_path = os.path.join(method_folder, f"{base_name}_bsse_{method_safe}.out")
                    shutil.move(output_path, new_output_path)
                    print(f"BSSE输出文件已保存至: {new_output_path}")
                    
                    temp_gjf = output_path.replace('.out', '.gjf')
                    if os.path.exists(temp_gjf):
                        new_gjf_path = os.path.join(method_folder, f"{base_name}_bsse_{method_safe}.gjf")
                        shutil.move(temp_gjf, new_gjf_path)
                elif output_path and os.path.exists(output_path):
                    # 如果失败但输出文件存在，也尝试移动
                    method_safe = method.replace('/', '_').replace(' ', '_').replace('(', '').replace(')', '').replace('=', '')
                    new_output_path = os.path.join(method_folder, f"{base_name}_bsse_{method_safe}.out")
                    shutil.move(output_path, new_output_path)
                    print(f"BSSE输出文件已保存至: {new_output_path}")
            else:
                print(f"单体 (n=1) 不需要BSSE矫正，跳过BSSE计算")
                success, output_path = run_gaussian_calculation(gjf_path, method)
                
                if success and output_path:
                    method_safe = method.replace('/', '_').replace(' ', '_').replace('(', '').replace(')', '').replace('=', '')
                    new_output_path = os.path.join(method_folder, f"{base_name}_{method_safe}.out")
                    shutil.move(output_path, new_output_path)
                    print(f"输出文件已保存至: {new_output_path}")
                    
                    temp_gjf = output_path.replace('.out', '.gjf')
                    if os.path.exists(temp_gjf):
                        new_gjf_path = os.path.join(method_folder, f"{base_name}_{method_safe}.gjf")
                        shutil.move(temp_gjf, new_gjf_path)
        else:
            # 不进行BSSE矫正，正常计算
            success, output_path = run_gaussian_calculation(gjf_path, method)
            
            if success and output_path:
                method_safe = method.replace('/', '_').replace(' ', '_').replace('(', '').replace(')', '').replace('=', '')
                new_output_path = os.path.join(method_folder, f"{base_name}_{method_safe}.out")
                shutil.move(output_path, new_output_path)
                print(f"输出文件已保存至: {new_output_path}")
                
                temp_gjf = output_path.replace('.out', '.gjf')
                if os.path.exists(temp_gjf):
                    new_gjf_path = os.path.join(method_folder, f"{base_name}_{method_safe}.gjf")
                    shutil.move(temp_gjf, new_gjf_path)
            elif output_path and os.path.exists(output_path):
                # 如果失败但输出文件存在，也尝试移动
                method_safe = method.replace('/', '_').replace(' ', '_').replace('(', '').replace(')', '').replace('=', '')
                new_output_path = os.path.join(method_folder, f"{base_name}_{method_safe}.out")
                shutil.move(output_path, new_output_path)
                print(f"输出文件已保存至: {new_output_path}")
        
        if not success:
            print(f"计算失败: {method}")

def extract_energy_from_out_file(out_file_path, is_bsse=False):
    """从.out文件中提取最终能量值并转换为kJ/mol"""
    with open(out_file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 如果是BSSE计算，需要提取Counterpoise corrected energy
    if is_bsse:
        # 查找Counterpoise corrected energy
        cp_match = re.search(r'Counterpoise corrected energy\s*=\s*(-?\d+\.\d+)', content)
        if cp_match:
            hartree_energy = float(cp_match.group(1))
            print(f"从BSSE计算中提取Counterpoise corrected energy: {hartree_energy} Hartree")
            return hartree_energy * ENERGY_CONVERSION_FACTOR
        
        # 如果找不到Counterpoise corrected energy，尝试查找最后一个SCF Done
        print(f"警告: 在BSSE计算中未找到Counterpoise corrected energy，尝试提取最后一个SCF能量")
    
    # 普通能量提取
    scf_match = re.search(r'SCF Done:.*E\(.*?\)\s*=\s*(-?\d+\.\d+)', content)
    if scf_match:
        hartree_energy = float(scf_match.group(1))
        return hartree_energy * ENERGY_CONVERSION_FACTOR
    
    cbsqb3_match = re.search(r'CBS-QB3 \(0 K\):\s+(-?\d+\.\d+)', content)
    if cbsqb3_match:
        hartree_energy = float(cbsqb3_match.group(1))
        return hartree_energy * ENERGY_CONVERSION_FACTOR
    
    ccsdt_match = re.search(r'E\(.*?CCSD\(T\).*?\)\s*=\s*(-?\d+\.\d+)', content)
    if ccsdt_match:
        hartree_energy = float(ccsdt_match.group(1))
        return hartree_energy * ENERGY_CONVERSION_FACTOR
    
    mp2_match = re.search(r'E\(.*?MP2.*?\)\s*=\s*(-?\d+\.\d+)', content)
    if mp2_match:
        hartree_energy = float(mp2_match.group(1))
        return hartree_energy * ENERGY_CONVERSION_FACTOR
    
    last_energy_match = re.findall(r'E\(.*?\)\s*=\s*(-?\d+\.\d+)', content)
    if last_energy_match:
        hartree_energy = float(last_energy_match[-1])
        return hartree_energy * ENERGY_CONVERSION_FACTOR
    
    print(f"警告: 无法从 {out_file_path} 中提取能量值")
    return None

def extract_bsse_binding_energy(out_file_path):
    """从BSSE计算输出文件中提取矫正后的结合能（单位：kcal/mol）"""
    with open(out_file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 查找矫正后的结合能（以kcal/mol为单位）
    # 格式示例：complexation energy =      -3.85 kcal/mole (corrected)
    corrected_match = re.search(r'complexation energy\s*=\s*(-?\d+\.\d+)\s*kcal/mole\s*\(corrected\)', content)
    if corrected_match:
        kcal_energy = float(corrected_match.group(1))
        # 转换为kJ/mol
        return kcal_energy * 4.184  # 1 kcal = 4.184 kJ
    
    # 如果找不到矫正后的结合能，尝试计算
    # 提取Counterpoise corrected energy（复合物总能量）
    cp_match = re.search(r'Counterpoise corrected energy\s*=\s*(-?\d+\.\d+)', content)
    if cp_match:
        complex_energy = float(cp_match.group(1))
        
        # 提取片段能量和
        sum_frag_match = re.search(r'sum of fragments\s*=\s*(-?\d+\.\d+)', content)
        if sum_frag_match:
            fragments_sum = float(sum_frag_match.group(1))
            # 计算结合能（Hartree为单位）
            binding_energy_hartree = complex_energy - fragments_sum
            # 转换为kJ/mol
            return binding_energy_hartree * ENERGY_CONVERSION_FACTOR
    
    return None

def calculate_binding_energies(energy_data):
    """计算结合能"""
    binding_energies = {}
    
    # 找到每个方法的单体能量
    monomer_energies = {}
    for method, energies in energy_data.items():
        for filename, n, energy, is_bsse, binding_energy in energies:
            if n == 1 and not is_bsse:  # 使用非BSSE的单体能量
                monomer_energies[method] = energy
                break
    
    # 计算每个多聚体的结合能
    for method, energies in energy_data.items():
        if method in monomer_energies:
            monomer_energy = monomer_energies[method]
            for filename, n, energy, is_bsse, binding_energy in energies:
                if n > 1:
                    # 如果已经有提取的BSSE结合能，使用它
                    if is_bsse and binding_energy is not None:
                        calc_binding = binding_energy
                    else:
                        # 否则计算结合能
                        calc_binding = energy - n * monomer_energy
                    
                    if method not in binding_energies:
                        binding_energies[method] = []
                    binding_energies[method].append((filename, n, calc_binding, is_bsse))
    
    return binding_energies

def save_energies_to_csv(energy_data, binding_energies, output_csv_path):
    """将能量数据保存到CSV文件"""
    import os
    file_exists = os.path.isfile(output_csv_path)
    
    with open(output_csv_path, 'a', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        if not file_exists:
            writer.writerow(['Method', 'Filename', 'N-mer', 'Total Energy (kJ/mol)', 'Binding Energy (kJ/mol)', 'Is_BSSE'])
        
        for method, energies in energy_data.items():
            for filename, n, energy, is_bsse, binding_energy in energies:
                # 查找对应的结合能
                found_binding_energy = None
                if method in binding_energies:
                    for bf, bn, be, bis_bsse in binding_energies[method]:
                        if bf == filename and bn == n and bis_bsse == is_bsse:
                            found_binding_energy = be
                            break
                
                writer.writerow([method, filename, n, energy, found_binding_energy, 'Yes' if is_bsse else 'No'])
    
    print(f"能量数据已{'追加' if file_exists else '保存'}到: {output_csv_path}")

def process_optimized_files_and_calculate_energies(root_dir, methods_list, use_bsse=False):
    """处理现有的优化文件并计算能量"""
    print("正在查找已优化的文件...")
    optimized_files = find_optimized_gjf_files(root_dir)
    
    if not optimized_files:
        print("未找到任何已优化的文件 (*_optimized.gjf)")
        return
    
    print(f"找到 {len(optimized_files)} 个已优化的文件:")
    for opt_file in optimized_files:
        print(f"  - {os.path.basename(opt_file)}")
    
    for opt_file in optimized_files:
        perform_method_calculations(opt_file, methods_list, use_bsse)
    
    energy_data = {}
    for method in methods_list:
        method_folder = os.path.join(root_dir, method.replace('/', '_').replace(' ', '_').replace('=', ''))
        if not os.path.exists(method_folder):
            continue
        
        for out_file in os.listdir(method_folder):
            if out_file.endswith('.out'):
                out_path = os.path.join(method_folder, out_file)
                
                # 判断是否是BSSE计算
                is_bsse = '_bsse' in out_file
                
                # 提取能量
                energy = extract_energy_from_out_file(out_path, is_bsse)
                
                if energy is not None:
                    n_mer = extract_number_from_filename(out_file)
                    base_name = os.path.splitext(out_file)[0]
                    
                    # 对于BSSE计算，尝试提取矫正后的结合能
                    binding_energy = None
                    if is_bsse:
                        binding_energy = extract_bsse_binding_energy(out_path)
                        if binding_energy is not None:
                            print(f"从BSSE输出中提取矫正结合能: {binding_energy:.4f} kJ/mol")
                    
                    if method not in energy_data:
                        energy_data[method] = []
                    energy_data[method].append((base_name, n_mer, energy, is_bsse, binding_energy))
    
    binding_energies = calculate_binding_energies(energy_data)
    
    csv_name = "energies_and_binding_bsse.csv" if use_bsse else "energies_and_binding.csv"
    csv_path = os.path.join(root_dir, csv_name)
    save_energies_to_csv(energy_data, binding_energies, csv_path)

def main():
    """主函数"""
    print("=" * 60)
    print("Gaussian 批量计算工具 (包含BSSE矫正功能)")
    print("=" * 60)
    
    print("\n正在设置Gaussian环境变量...")
    if not setup_gaussian_environment():
        return
    
    root_dir = os.path.dirname(os.path.abspath(__file__))
    
    process_existing = input("\n是否处理当前目录下已有的优化文件(*_optimized.gjf)? (y/N): ")
    
    if process_existing.lower() == 'y':
        print("\n可用于后续计算的方法:")
        for i, method in enumerate(AVAILABLE_METHODS):
            print(f"  {i+1}. {method}")
        
        selected_methods = []
        while True:
            try:
                choice_input = input(f"\n请选择要用于后续计算的方法 (输入序号，多个用逗号分隔，或输入0表示全部): ")
                choices = [int(x.strip()) for x in choice_input.split(',')]
                
                if len(choices) == 1 and choices[0] == 0:
                    selected_methods = AVAILABLE_METHODS
                    break
                else:
                    for choice in choices:
                        if 1 <= choice <= len(AVAILABLE_METHODS):
                            selected_methods.append(AVAILABLE_METHODS[choice-1])
                        else:
                            print(f"序号 {choice} 超出范围")
                    break
            except ValueError:
                print("请输入有效的数字或数字序列（用逗号分隔）")
        
        if not selected_methods:
            print("没有选择任何方法!")
            return
        
        print(f"\n选择的方法: {selected_methods}")
        
        # 询问是否使用BSSE矫正
        use_bsse = input("\n是否进行BSSE矫正计算? (y/N): ")
        use_bsse = use_bsse.lower() == 'y'
        
        if use_bsse:
            print("将进行BSSE矫正计算")
        else:
            print("将进行普通计算（无BSSE矫正）")
        
        process_optimized_files_and_calculate_energies(root_dir, selected_methods, use_bsse)
        return
    
    use_current_dir = input(f"\n是否在当前目录 ({root_dir}) 中搜索.gjf文件? (y/N): ")
    if use_current_dir.lower() != 'y':
        custom_dir = input("请输入要搜索的目录路径: ")
        if os.path.exists(custom_dir):
            root_dir = custom_dir
        else:
            print(f"目录不存在: {custom_dir}")
            return
    
    print(f"\n正在搜索 {root_dir} 中的 .gjf 文件...")
    gjf_files = find_gjf_files(root_dir)
    
    if not gjf_files:
        print("未找到任何 .gjf 文件!")
        return
    
    print(f"找到 {len(gjf_files)} 个 .gjf 文件:")
    for i, gjf_file in enumerate(gjf_files):
        rel_path = os.path.relpath(gjf_file, root_dir)
        with open(gjf_file, 'r', encoding='utf-8') as f:
            content = f.read()
            method_info = extract_calculation_info(content)
        n_mer = extract_number_from_filename(gjf_file)
        print(f"  {i+1}. {rel_path} (当前方法: {method_info}, N-mer: {n_mer})")
    
    print("\n可用于后续计算的方法:")
    for i, method in enumerate(AVAILABLE_METHODS):
        print(f"  {i+1}. {method}")
    
    selected_methods = []
    while True:
        try:
            choice_input = input(f"\n请选择要用于后续计算的方法 (输入序号，多个用逗号分隔，或输入0表示全部): ")
            choices = [int(x.strip()) for x in choice_input.split(',')]
            
            if len(choices) == 1 and choices[0] == 0:
                selected_methods = AVAILABLE_METHODS
                break
            else:
                for choice in choices:
                    if 1 <= choice <= len(AVAILABLE_METHODS):
                        selected_methods.append(AVAILABLE_METHODS[choice-1])
                    else:
                        print(f"序号 {choice} 超出范围")
                break
        except ValueError:
            print("请输入有效的数字或数字序列（用逗号分隔）")
    
    if not selected_methods:
        print("没有选择任何方法!")
        return
    
    print(f"\n选择的方法: {selected_methods}")
    
    # 询问是否使用BSSE矫正
    use_bsse = input("\n是否进行BSSE矫正计算? (y/N): ")
    use_bsse = use_bsse.lower() == 'y'
    
    if use_bsse:
        print("将进行BSSE矫正计算")
    else:
        print("将进行普通计算（无BSSE矫正）")
    
    print("\n选择要处理的文件:")
    print("  1. 处理所有文件")
    print("  2. 选择特定文件")
    
    file_choice = input("请选择 (1-2): ")
    
    files_to_process = []
    if file_choice == "1":
        files_to_process = gjf_files
    else:
        file_numbers = input("请输入要处理的文件编号 (用逗号分隔，例如: 1,3,5): ")
        try:
            indices = [int(x.strip()) - 1 for x in file_numbers.split(",")]
            for idx in indices:
                if 0 <= idx < len(gjf_files):
                    files_to_process.append(gjf_files[idx])
                else:
                    print(f"忽略无效编号: {idx+1}")
        except ValueError:
            print("输入格式错误，将处理所有文件")
            files_to_process = gjf_files
    
    if not files_to_process:
        print("没有选择任何文件!")
        return
    
    confirm = input(f"\n确定要对 {len(files_to_process)} 个文件执行几何优化和频率分析吗? (y/N): ")
    if confirm.lower() != 'y':
        print("操作已取消。")
        return
    
    print("\n开始批量几何优化和频率分析...")
    
    files_with_imag_freq = []
    files_without_imag_freq = []
    
    for i, gjf_file in enumerate(files_to_process):
        print(f"\n{'='*60}")
        print(f"[{i+1}/{len(files_to_process)}] 正在处理: {os.path.relpath(gjf_file, root_dir)}")
        
        has_imag_freq, result_path, imag_freq_value = run_optimization_and_check_freq(gjf_file)
        
        if has_imag_freq:
            files_with_imag_freq.append((gjf_file, imag_freq_value))
        elif result_path:
            files_without_imag_freq.append(result_path)
        
        if i < len(files_to_process) - 1:
            delay = 5
            print(f"等待{delay}秒后继续...")
            time.sleep(delay)
    
    print(f"\n{'='*60}")
    print(f"几何优化和频率分析完成!")
    
    if files_with_imag_freq:
        print(f"\n发现虚频的文件 ({len(files_with_imag_freq)} 个):")
        for file_path, freq_value in files_with_imag_freq:
            print(f"  - {os.path.basename(file_path)}, 虚频值: {freq_value} cm-1")
    else:
        print("\n没有发现虚频的文件")
    
    if files_without_imag_freq:
        print(f"\n对 {len(files_without_imag_freq)} 个无虚频的文件执行多种方法计算...")
        
        for optimized_gjf in files_without_imag_freq:
            perform_method_calculations(optimized_gjf, selected_methods, use_bsse)
        
        energy_data = {}
        for method in selected_methods:
            method_folder = os.path.join(root_dir, method.replace('/', '_').replace(' ', '_').replace('=', ''))
            if not os.path.exists(method_folder):
                continue
            
            for out_file in os.listdir(method_folder):
                if out_file.endswith('.out'):
                    out_path = os.path.join(method_folder, out_file)
                    
                    # 判断是否是BSSE计算
                    is_bsse = '_bsse' in out_file
                    
                    # 提取能量
                    energy = extract_energy_from_out_file(out_path, is_bsse)
                    
                    if energy is not None:
                        n_mer = extract_number_from_filename(out_file)
                        base_name = os.path.splitext(out_file)[0]
                        
                        # 对于BSSE计算，尝试提取矫正后的结合能
                        binding_energy = None
                        if is_bsse:
                            binding_energy = extract_bsse_binding_energy(out_path)
                            if binding_energy is not None:
                                print(f"从BSSE输出中提取矫正结合能: {binding_energy:.4f} kJ/mol")
                        
                        if method not in energy_data:
                            energy_data[method] = []
                        energy_data[method].append((base_name, n_mer, energy, is_bsse, binding_energy))
        
        binding_energies = calculate_binding_energies(energy_data)
        
        csv_name = "energies_and_binding_bsse.csv" if use_bsse else "energies_and_binding.csv"
        csv_path = os.path.join(root_dir, csv_name)
        save_energies_to_csv(energy_data, binding_energies, csv_path)
        
    else:
        print("\n没有无虚频的文件需要进一步计算")
    
    print(f"\n程序执行完毕!")

if __name__ == "__main__":
    main()