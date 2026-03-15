# Gaussian Batch Calculation Tool | Gaussian 批量计算工具

An automated quantum chemistry calculation tool based on Gaussian software, supporting multiple calculation methods, BSSE correction, geometry optimization, frequency analysis, and email notifications.

基于 Gaussian 软件的批量量子化学计算自动化工具，支持多种计算方法、BSSE 矫正、几何优化和频率分析，并可通过邮件发送计算结果通知。

## Features | 功能特点

- 🔍 **Auto Discovery** | 自动发现：Automatically scan `.gjf` files in directories | 自动扫描目录中的 `.gjf` 文件
- ⚡ **Batch Processing** | 批量处理：Support batch geometry optimization and frequency analysis | 支持批量几何优化和频率分析
- 🎯 **Multi-Method** | 多方法：Support various quantum chemistry methods (CCSD(T), M062X, WB97XD, B3LYP, etc.) | 支持多种量子化学计算方法（CCSD(T)、M062X、WB97XD、B3LYP 等）
- 📊 **BSSE Correction** | BSSE 矫正：Automatic basis set superposition error correction | 自动进行基组叠加误差矫正计算
- 📧 **Email Notification** | 邮件通知：Automatically send email notifications with CSV results | 计算完成后自动发送邮件通知，附带 CSV 结果文件
- 📈 **Energy Extraction** | 能量提取：Automatically extract energy data and calculate binding energies | 自动从输出文件中提取能量数据并计算结合能
- ✅ **Imaginary Frequency Detection** | 虚频检测：Automatically detect imaginary frequencies in frequency calculations | 自动检测频率计算中的虚频

---

## System Requirements | 系统要求

- **OS**: Windows
- **Software**: 
  - Gaussian 16 (G16W)
  - Python 3.7+

---

## Installation | 安装步骤

### 1. Clone or Download Project | 克隆或下载项目

```bash
git clone <your-repository-url>
cd H2O
```

### 2. Create Virtual Environment (Recommended) | 创建虚拟环境（推荐）

```bash
python -m venv venv
```

### 3. Activate Virtual Environment | 激活虚拟环境

**Windows:**
```bash
.\venv\Scripts\activate
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

### 4. Install Dependencies | 安装依赖

```bash
pip install -r requirements.txt
```

### 5. Configure Environment Variables | 配置环境变量

Copy the environment variable template file:

复制环境变量模板文件：

```bash
cp .env.example .env
```

Edit the `.env` file and fill in your configuration:

编辑 `.env` 文件，填入你的配置：

```ini
# Email Configuration | 邮箱配置
FROM_EMAIL=your_qq_email@qq.com          # Your QQ email | 你的 QQ 邮箱
EMAIL_PASSWORD=your_auth_code            # Your email auth code | 你的邮箱授权码
TO_EMAIL=recipient@163.com               # Recipient email | 接收通知的邮箱

# Gaussian Configuration | Gaussian 配置
GAUSSIAN_DIR=F:\Gauss\Gauss\G16W         # Gaussian installation path | Gaussian 安装路径
```

⚠️ **Important**: The `EMAIL_PASSWORD` is your email authorization code, NOT your login password. See [QUICKSTART.md](QUICKSTART.md) for details.

⚠️ **重要**：`EMAIL_PASSWORD` 是你的邮箱授权码，不是登录密码。详见 [QUICKSTART.md](QUICKSTART.md)。

---

## Configuration Guide | 配置说明

### Calculation Method Configuration | 计算方法配置

Modify the `AVAILABLE_METHODS` list in `email_gaussian_runner.py` to select calculation methods:

在 `email_gaussian_runner.py` 中修改 `AVAILABLE_METHODS` 列表来选择要使用的计算方法：

```python
AVAILABLE_METHODS = [
    "M062X/def2TZVP em=gd3 SCRF=(SMD,solvent=water)",
    "WB97XD/6-311++G(2d,2p)",
    "B3LYP/6-31G(d,p) em=gd3bj",
]
```

### BSSE Correction Configuration | BSSE 矫正配置

Enable or disable BSSE correction:

启用或禁用 BSSE 矫正：

```python
USE_BSSE = True  # True=enable, False=disable | True=启用，False=禁用
```

### Geometry Optimization Method | 几何优化方法

Set the method for optimization and frequency calculation:

设置优化和频率计算的方法：

```python
OPTIMIZATION_METHOD = "b3lyp/6-31g(d,p) em=gd3bj Opt=(VeryTight, MaxCycles=200) freq SCRF=(SMD,solvent=water)"
```

---

## Usage | 使用方法

### Basic Usage | 基本使用

After ensuring all environment variables and Gaussian paths are correctly configured, run the main script:

确保已正确配置所有环境变量和 Gaussian 路径后，直接运行主脚本：

```bash
python email_gaussian_runner.py
```

### Workflow | 工作流程

1. **Auto Scan** | 自动扫描：Automatically scan all `.gjf` files in current directory and subdirectories | 程序会自动扫描当前目录及其子目录中的所有 `.gjf` 文件
2. **Geometry Optimization** | 几何优化：Perform geometry optimization and frequency analysis on selected files | 对选定的文件进行几何优化和频率分析
3. **Imaginary Frequency Detection** | 虚频检测：Automatically detect if imaginary frequencies exist | 自动检测是否存在虚频
4. **Multi-Method Calculation** | 多方法计算：Perform single-point energy calculations using multiple methods on structures without imaginary frequencies | 对无虚频的结构进行多种方法的单点能计算
5. **BSSE Correction** | BSSE 矫正：If enabled, automatically perform BSSE correction calculations | 如启用，自动进行 BSSE 矫正计算
6. **Energy Extraction** | 能量提取：Extract energy data from output files and calculate binding energies | 从输出文件中提取能量数据并计算结合能
7. **Result Saving** | 结果保存：Save energy data to CSV files | 将能量数据保存到 CSV 文件
8. **Email Notification** | 邮件通知：Send calculation results to specified email | 发送计算结果到指定邮箱

### Filename Convention | 文件名规则

The program identifies monomers, dimers, trimers, etc., based on numbers in filenames:

程序根据文件名中的数字来识别单体、二聚体、三聚体等：

- `H2O_1.gjf` - Monomer | 单体
- `H2O_2.gjf` - Dimer | 二聚体
- `H2O_3.gjf` - Trimer | 三聚体

For polymers (n>1), the program automatically performs BSSE correction.

对于多聚体（n>1），程序会自动进行 BSSE 矫正。

---

## Output Files | 输出文件

The program generates the following files after execution:

程序运行后会生成以下文件：

- `*_optimized.gjf` - Optimized geometry files | 优化后的几何结构文件
- `*_opt_freq.gjf` - Optimization and frequency calculation input files | 优化和频率计算的输入文件
- `*.out` - Gaussian output files | Gaussian 输出文件
- `energies_and_binding.csv` or `energies_and_binding_bsse.csv` - Energy and binding energy data | 能量和结合能数据

### CSV File Format | CSV 文件格式

| Method | Filename | N-mer | Total Energy (kJ/mol) | Binding Energy (kJ/mol) | Is_BSSE |
|--------|----------|-------|----------------------|------------------------|---------|
| M062X_def2TZVP | H2O_1 | 1 | -12345.67 | - | No |
| M062X_def2TZVP | H2O_2_bsse | 2 | -24691.34 | -15.23 | Yes |

---

## Email Notification | 邮件通知

The program automatically sends email notifications after calculation completion, including:

程序会在计算完成后自动发送邮件通知，包含：

- Calculation completion status | 计算完成状态
- Calculation time | 计算时间
- Log summary | 日志摘要
- CSV result file attachment | CSV 结果文件附件

### Email Provider SMTP Configuration | 邮箱服务商 SMTP配置

Currently supported email providers:

目前支持的邮箱服务商：

- **QQ Mail**: smtp.qq.com:465 (SSL)

To add other email providers, modify the `SMTP_CONFIGS` dictionary in the code.

如需添加其他邮箱服务商，可在代码中修改 `SMTP_CONFIGS` 字典。

---

## Directory Structure | 目录结构

```
H2O/
├── email_gaussian_runner.py      # Main script | 主程序
├── README.md                     # Documentation | 说明文档
├── QUICKSTART.md                 # Quick start guide | 快速开始指南
├── DEPLOYMENT.md                 # Deployment guide | 部署指南
├── UPLOAD_GUIDE.md               # Upload guide | 上传指南
├── DOCS_INDEX.md                 # Documentation index | 文档索引
├── PROJECT_SUMMARY.md            # Project summary | 项目总结
├── LICENSE                       # MIT License | MIT 许可证
├── requirements.txt              # Python dependencies | Python 依赖
├── .env                          # Environment config (create manually) | 环境变量配置（需手动创建）
├── .env.example                  # Environment template | 环境变量模板
├── .gitignore                    # Git ignore rules | Git 忽略规则
└── [Your .gjf files]/            # Place .gjf files here | 放置需要计算的.gjf 文件
```

---

## FAQ | 常见问题

### 1. Gaussian Installation Directory Not Found | Gaussian 找不到安装目录

Ensure `GAUSSIAN_DIR` is correctly set in the `.env` file, pointing to the Gaussian 16 installation directory.

确保在 `.env` 文件中正确设置了 `GAUSSIAN_DIR` 变量，指向 Gaussian 16 的安装目录。

### 2. Email Sending Failed | 邮件发送失败

- Check if email account and auth code are correct | 检查邮箱账号和授权码是否正确
- QQ Mail requires auth code, not password | QQ 邮箱需要使用授权码而非密码
- Ensure SMTP service is enabled for the email | 确保邮箱已开启 SMTP 服务

### 3. Calculation Timeout | 计算超时

The program has a default timeout of 100000 seconds. To adjust, modify the `timeout` variable in the code.

程序默认设置了 100000 秒的超时时间。如果需要调整，可修改代码中的 `timeout` 变量。

### 4. Cannot Extract Energy Values | 无法提取能量值

Ensure Gaussian calculation completed normally and output files contain "SCF Done" or other energy keywords.

确保 Gaussian 计算正常完成，输出文件中包含 "SCF Done" 或其他能量关键词。

---

## Security Notice | 安全提示

⚠️ **IMPORTANT**: Do NOT upload files containing sensitive information (such as `.env`, source code with email and auth code) to public code repositories.

⚠️ **重要**：请勿将包含敏感信息的文件（如 `.env`、包含邮箱和授权码的源代码）上传到公开代码仓库。

It is recommended to use environment variables or configuration files to manage sensitive information and add these files to `.gitignore`.

建议使用环境变量或配置文件来管理敏感信息，并将这些文件添加到 `.gitignore` 中。

---

## License | 许可证

This project is for academic research and teaching purposes only.

本项目仅供学术研究和教学使用。

---

## Acknowledgements | 致谢

- Gaussian Software: Gaussian 16, Revision C.01
- Thanks to all researchers who contributed to this tool | 感谢所有为此工具做出贡献的研究人员

---

## Contact | 联系方式

For questions or suggestions, please contact the author via email.

如有问题或建议，欢迎通过邮件联系作者。
