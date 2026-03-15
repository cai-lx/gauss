# 🚀 Quick Start Guide | 快速开始指南

Get up and running in 5 minutes!

5 分钟快速配置！

---

## Step 1: Create Environment File (2 min) | 创建环境变量文件（2 分钟）

Create a `.env` file in the project root directory:

在项目根目录创建 `.env` 文件：

```bash
# Windows PowerShell
New-Item -Path ".env" -ItemType File

# Or create directly in Notepad and save as .env
# 或者在记事本中直接创建并保存为 .env
```

---

## Step 2: Get and Configure Email Auth Code (3 min) | 获取并填写邮箱授权码（3 分钟）

### 1. Log in to QQ Mail | 登录 QQ 邮箱
https://mail.qq.com

### 2. Go to Settings | 进入设置
Click "Settings" → "Accounts" tab at the top

点击顶部"设置" → "账户"标签

### 3. Enable SMTP Service | 开启 SMTP 服务
Find "POP3/IMAP/SMTP/Exchange/CardDAV/CalDAV Service" section  
Ensure "IMAP/SMTP Service" is enabled (shows green)

找到"POP3/IMAP/SMTP/Exchange/CardDAV/CalDAV 服务"区域  
确保"IMAP/SMTP 服务"已开启（显示绿色）

### 4. Generate Auth Code | 生成授权码
Click "Generate Authorization Code"  
Follow prompts to send SMS verification  
Copy the received auth code

点击"生成授权码"  
按提示发送短信验证  
复制收到的授权码

### 5. Edit .env File | 编辑 .env 文件

Fill in the following information:

填入以下信息：

```ini
# Email Configuration (MUST replace with your real info) | 邮箱配置（必须替换为你的真实信息）
FROM_EMAIL=your_qq_email@qq.com              # Your QQ email | 你的 QQ 邮箱
EMAIL_PASSWORD=your_auth_code                # Your auth code (NOT your QQ password) | 你的授权码（不是 QQ 密码）
TO_EMAIL=recipient@163.com                   # Notification recipient email | 接收通知的邮箱

# Gaussian Installation Directory | Gaussian 安装目录
GAUSSIAN_DIR=F:\Gauss\Gauss\G16W             # Modify based on your actual installation path | 根据你的实际安装位置修改
```

⚠️ **Important Note** | 重要提示：
- `EMAIL_PASSWORD` should be the **auth code**, NOT your QQ login password
- The auth code needs to be generated separately, one auth code per email account
- If you forget the auth code, you can regenerate it

⚠️ **重要提示**：
- `EMAIL_PASSWORD` 填的是**授权码**，不是你的 QQ 登录密码
- 授权码需要单独生成，每个邮箱账号对应一个授权码
- 如果忘记授权码，可以重新生成

---

## Step 3: Prepare Calculation Files | 准备计算文件

Place your `.gjf` files in the project directory or subdirectories.

将你的 `.gjf` 文件放入项目目录或子目录中。

Filename convention examples:

文件名规则示例：
- `H2O_1.gjf` - Monomer water molecule | 单体水分子
- `H2O_2.gjf` - Dimer | 二聚体
- `H2O_3.gjf` - Trimer | 三聚体

---

## Step 4: Run Program (1 min) | 运行程序（1 分钟）

Open Command Prompt or PowerShell, navigate to the project directory:

打开命令提示符或 PowerShell，进入项目目录：

```bash
cd d:\desk\科研\分子动力学\高斯\H2O
python email_gaussian_runner.py
```

Then follow the prompts!

然后按照提示操作即可！

---

## Complete Configuration Guide | 完整配置说明

### Calculation Method Configuration | 计算方法配置

Edit the `AVAILABLE_METHODS` list in `email_gaussian_runner.py`:

编辑 `email_gaussian_runner.py` 文件中的 `AVAILABLE_METHODS` 列表：

```python
AVAILABLE_METHODS = [
    "M062X/def2TZVP em=gd3 SCRF=(SMD,solvent=water)",  # Recommended for aqueous solution | 推荐的水溶液方法
    "WB97XD/6-311++G(2d,2p)",                          # With dispersion correction | 含色散矫正
    "B3LYP/6-31G(d,p) em=gd3bj",                       # Common functional | 常用泛函
]
```

Comment out methods you don't want, or add new methods.

注释掉不想要的方法，或添加新的方法。

### BSSE Correction Switch | BSSE 矫正开关

```python
USE_BSSE = True  # True=enable BSSE correction | False=disable
```

### Geometry Optimization Method | 几何优化方法

```python
OPTIMIZATION_METHOD = "b3lyp/6-31g(d,p) em=gd3bj Opt=(VeryTight, MaxCycles=200) freq SCRF=(SMD,solvent=water)"
```

---

## Expected Output | 预期输出

After running, the program will generate the following files in the current directory:

程序运行后会在当前目录生成以下文件：

```
H2O/
├── energies_and_binding_bsse.csv     # Energy and binding energy results | 能量和结合能结果
├── M062X_def2TZVP_em_gd3_SCRF_SMD_solvent_water/  # Calculation method folder | 计算方法文件夹
│   ├── H2O_1_M062X_def2TZVP.out      # Calculation output file | 计算输出文件
│   └── H2O_1_M062X_def2TZVP.gjf      # Calculation input file | 计算输入文件
├── H2O_1_optimized.gjf               # Optimized structure | 优化后的结构
└── ...other files | ...其他文件
```

### Email Notification Example | 邮件通知示例

After calculation completes, you'll receive an email containing:

计算完成后，你会收到一封邮件，包含：
- ✅ Calculation completion status | 计算完成状态
- 📅 Calculation time | 计算时间
- 📝 Log summary | 日志摘要
- 📊 CSV result attachment | CSV 结果附件

---

## FAQ Quick Reference | 常见问题速查

### ❓ How to skip calculation for certain files? | 如何跳过某些文件的计算？

When the program runs, it will list all found files. Choose "2" to manually select file numbers to process.

程序运行时会列出所有找到的文件，选择"2"手动选择要处理的文件编号。

### ❓ What if calculation stops midway? | 计算中途停止怎么办？

Check:
检查：
1. Is Gaussian installed correctly? | Gaussian 是否正确安装
2. Is the path in `.env` file correct? | `.env` 文件中的路径是否正确
3. Is there enough disk space? | 是否有足够的磁盘空间

### ❓ Email sending failed? | 邮件发送失败？

Check:
检查：
1. Are the email and auth code in `.env` file correct? | `.env` 文件中的邮箱账号和授权码是否正确
2. Is SMTP service enabled for the email? | 邮箱是否开启了 SMTP 服务
3. Is the network connection normal? | 网络连接是否正常

### ❓ How to view detailed error messages? | 如何查看详细的错误信息？

The program automatically prints detailed logs during execution. Observe the console output carefully.

程序运行时会自动打印详细日志，注意观察控制台输出。

---

## Next Steps | 下一步

After completing the basic configuration, you can:

完成基本配置后，你可以：

1. 📖 Read [`README.md`](README.md) for detailed features | 阅读 [`README.md`](README.md) 了解详细功能
2. 🔧 Check [`DEPLOYMENT.md`](DEPLOYMENT.md) to learn how to upload to GitHub | 查看 [`DEPLOYMENT.md`](DEPLOYMENT.md) 学习如何上传到 GitHub
3. 📊 Analyze generated CSV files to view calculation results | 分析生成的 CSV 文件查看计算结果

---

**Happy calculating!** 🎉

**祝你计算顺利！** 🎉

For any issues, please refer to project documentation or contact the author.

如有问题，请查阅项目文档或联系作者。
