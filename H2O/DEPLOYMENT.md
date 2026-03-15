# Deployment Configuration Guide | 部署配置指南

This document contains configuration instructions for uploading the project to GitHub and deployment.

本文件包含将项目上传到 GitHub 及部署时的配置说明。

---

## 📋 Pre-upload Checklist | 上传前检查清单

### 1. Sensitive Information Handling ✅ | 敏感信息处理

- [x] Email accounts completely removed from code | 邮箱账号已从代码中完全移除
- [x] Auth codes completely removed from code | 授权码已从代码中完全移除
- [x] Configurations changed to read from environment variables | 配置改为从环境变量读取
- [x] `.env` file added to `.gitignore` | `.env` 文件已添加到 `.gitignore`
- [ ] Create `.env` file (for local use, do NOT upload) | 创建 `.env` 文件（本地使用，不要上传）

### 2. Required Configuration Files ✅ | 必需配置文件

The following files have been created and can be safely uploaded to GitHub:

以下文件已创建并可以安全上传到 GitHub：

- `README.md` - Project documentation | 项目说明文档
- `requirements.txt` - Python dependency list | Python 依赖列表
- `.env.example` - Environment variable template (placeholders only, no real credentials) | 环境变量模板（仅占位符，不含真实凭证）
- `.gitignore` - Git ignore rules | Git 忽略规则

### 3. Local Configuration Files (Do NOT Upload) ❌ | 本地配置文件（不要上传）

The following files are for local use only and **MUST NOT** be uploaded to GitHub:

以下文件仅在本地使用，**绝对不要**上传到 GitHub：

- `.env` - Contains real email accounts and auth codes | 包含真实的邮箱账号和授权码
- Any configuration files containing real credentials | 任何包含真实凭证的配置文件

---

## 🔧 Local Configuration Steps | 本地配置步骤

### Step 1: Create .env File | 创建 .env 文件

Create a `.env` file in the project root directory:

在项目根目录下创建 `.env` 文件：

```bash
# Windows (PowerShell)
ni .env

# Windows (CMD)
type nul > .env

# Linux/Mac
touch .env
```

### Step 2: Edit .env File | 编辑 .env 文件

Fill in your **real configuration** in the `.env` file:

在 `.env` 文件中填入你的**真实配置**：

```ini
# Email Configuration (MUST fill with real info) | 邮箱配置（必须填写真实信息）
FROM_EMAIL=your_qq_email@qq.com
EMAIL_PASSWORD=your_qq_email_auth_code
TO_EMAIL=recipient@163.com

# Gaussian Installation Directory | Gaussian 安装目录
GAUSSIAN_DIR=F:\Gauss\Gauss\G16W
```

⚠️ **Important**:
- `EMAIL_PASSWORD` is the auth code, NOT your QQ password
- All values must be replaced with real information for the program to work

⚠️ **重要**：
- `EMAIL_PASSWORD` 是授权码，不是 QQ 密码
- 所有值都必须替换为真实信息，程序才能正常运行

### Step 3: Get QQ Email Auth Code | 获取 QQ 邮箱授权码

1. Log in to QQ Mail web version | 登录 QQ 邮箱网页版
2. Go to "Settings" → "Accounts" | 进入"设置" → "账户"
3. Find "POP3/IMAP/SMTP/Exchange/CardDAV/CalDAV Service" | 找到"POP3/IMAP/SMTP/Exchange/CardDAV/CalDAV 服务"
4. Enable "POP3/SMTP Service" or "IMAP/SMTP Service" | 开启"POP3/SMTP 服务"或"IMAP/SMTP 服务"
5. Click "Generate Authorization Code" | 点击"生成授权码"
6. Follow prompts to send SMS verification | 按提示发送短信验证
7. Copy the generated auth code and fill it in the `EMAIL_PASSWORD` field of `.env` file | 复制生成的授权码，填入 `.env` 文件的 `EMAIL_PASSWORD` 字段

### Step 4: Verify Configuration | 验证配置

Run the following command to test if the configuration is correct:

运行以下命令测试配置是否正确：

```bash
python email_gaussian_runner.py
```

If the program starts normally, the configuration is successful!

如果程序能正常启动，说明配置成功！

---

## 🚀 Upload to GitHub | 上传到 GitHub

### Method 1: Using Git Command Line | 方法 1: 使用 Git 命令行

```bash
# Initialize Git repository (if not already) | 初始化 Git 仓库（如果还没有）
git init

# Add all files | 添加所有文件
git add .

# Check if sensitive files are excluded | 检查是否有敏感文件被排除
git status

# Confirm .env is NOT in the list | 确认 .env 不在列表中

# Commit changes | 提交更改
git commit -m "Initial commit: Gaussian batch calculation tool"

# Link remote repository (replace with your repo URL) | 关联远程仓库（替换为你的仓库地址）
git remote add origin https://github.com/yourusername/your-repo-name.git

# Push to GitHub | 推送到 GitHub
git push -u origin main
```

### Method 2: Using GitHub Desktop | 方法 2: 使用 GitHub Desktop

1. Open GitHub Desktop | 打开 GitHub Desktop
2. Click "File" → "Add local repository" | 点击 "File" → "Add local repository"
3. Select the project folder | 选择项目文件夹
4. Fill in summary information | 填写摘要信息
5. Click "Commit to main" | 点击 "Commit to main"
6. Click "Publish repository" to upload to GitHub | 点击 "Publish repository" 上传到 GitHub

### Method 3: Manual Upload | 方法 3: 手动上传

1. Visit GitHub website | 访问 GitHub 网站
2. Create a new repository | 创建新的仓库
3. Click "uploading an existing file" | 点击 "uploading an existing file"
4. Drag and drop files to browser | 拖拽文件到浏览器
5. Fill in commit information and upload | 填写提交信息并上传

⚠️ **Note**: Before manual upload, ensure you have created a `.gitignore` file to avoid accidentally uploading sensitive files.

⚠️ **注意**: 手动上传前请确保已经创建了 `.gitignore` 文件，避免误传敏感文件。

---

## 🔒 Security Check | 安全检查

Be sure to confirm the following before uploading:

上传前务必确认以下内容：

### 1. Check if .gitignore is Working | 检查 .gitignore 是否生效

```bash
# View which files will be ignored | 查看哪些文件会被忽略
git check-ignore -a

# Or view the list of files to be committed | 或者查看将要提交的文件列表
git status
```

Ensure the following files **DO NOT** appear in the commit list:

确保以下文件**不会**出现在提交列表中：
- `.env`
- Any files containing passwords or keys | 任何包含密码、密钥的文件

### 2. Check for Sensitive Information in Code | 检查代码中的敏感信息

```bash
# Search for possible sensitive information | 搜索可能的敏感信息
grep -r "password" --include="*.py" .
grep -r "auth" --include="*.py" .
grep -r "token" --include="*.py" .
```

You should only find placeholders in `.env.example`, not real credentials anywhere.

应该只在 `.env.example` 中找到占位符，不应该在任何地方找到真实的凭证。

### 3. Use Git History Scanning Tools | 使用 Git 历史扫描工具

Install git-secrets or other tools to scan Git history:

安装 git-secrets 或其他工具扫描 Git 历史：

```bash
# Install git-secrets (Git required) | 安装 git-secrets（需要先安装 Git）
git clone https://github.com/awslabs/git-secrets.git
cd git-secrets
sudo make install

# Scan current repository | 扫描当前仓库
git secrets --scan
```

---

## 📝 Update Repository URL in README | 更新 README 中的仓库地址

After uploading to GitHub, remember to update the repository URL in `README.md`:

上传到 GitHub 后，记得更新 `README.md` 中的仓库地址：

```markdown
## Installation Steps | 安装步骤

### 1. Clone or Download Project | 克隆或下载项目

```bash
git clone https://github.com/YOUR_USERNAME/H2O.git
cd H2O
```
```

---

## 🛡️ Security Best Practices | 安全最佳实践

### 1. Never Commit Sensitive Information | 永远不要提交敏感信息

- API keys | API 密钥
- Database passwords | 数据库密码
- Email auth codes | 邮箱授权码
- Private key files | 私钥文件
- Personal identifiable information | 个人身份信息

### 2. Use Environment Variables for Configuration | 使用环境变量管理配置

Follow this project's approach using `.env.example` + environment variables:

参考本项目的方法，使用 `.env.example` + 环境变量的方式：

```python
# ✅ Good practice | 好的做法
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

# ❌ Bad practice | 不好的做法
EMAIL_PASSWORD = "mlcmmlystydvdjdf"
```

### 3. Regularly Update Dependencies | 定期更新依赖

If using third-party libraries, regularly check and update dependency versions:

如果使用第三方库，定期检查并更新依赖版本：

```bash
pip list --outdated
pip install --upgrade package_name
```

### 4. Enable Two-Factor Authentication | 启用双因素认证

Enable two-factor authentication (2FA) for your GitHub account to improve security.

为你的 GitHub 账号启用双因素认证（2FA）以提高安全性。

---

## 🆘 FAQ | 常见问题

### Q1: What if I accidentally commit sensitive files? | Q1: 不小心提交了敏感文件怎么办？

**Immediately take the following measures:** | **立即采取以下措施：**

1. **Delete sensitive files** (if still in workspace) | **删除敏感文件**（如果还在工作区）

2. **Completely remove from Git history** | **从 Git 历史中彻底删除**：

   ```bash
   # Using BFG Repo-Cleaner (recommended) | 使用 BFG Repo-Cleaner（推荐）
   java -jar bfg.jar --delete-files .env .

   # Or using git filter-branch | 或使用 git filter-branch
   git filter-branch --force --index-filter \
     'git rm --cached --ignore-unmatch .env' \
     --prune-empty --tag-name-filter cat -- --all
   ```

3. **Force push to GitHub** | **强制推送到 GitHub**：

   ```bash
   git push --force --all
   ```

4. **Change leaked credentials** (such as email auth code) | **更改泄露的凭证**（如邮箱授权码）

### Q2: .env file not working? | Q2: .env 文件没有生效？

Check the following points:

检查以下几点：

1. Filename must be `.env` (not `.env.txt`) | 文件名必须是 `.env`（不是 `.env.txt`）
2. File encoding must be UTF-8 | 文件编码为 UTF-8
3. One variable per line, format as `KEY=value` | 每行一个变量，格式为 `KEY=value`
4. No spaces or quotes (unless value contains spaces) | 不要有空格或引号（除非值中包含空格）

### Q3: How to verify if environment variables are loaded correctly? | Q3: 如何验证环境变量是否正确加载？

Add debug output in Python:

在 Python 中添加调试输出：

```python
import os
print(f"FROM_EMAIL: {os.getenv('FROM_EMAIL')}")
print(f"EMAIL_PASSWORD: {'Set' if os.getenv('EMAIL_PASSWORD') else 'Not set'}")
print(f"TO_EMAIL: {os.getenv('TO_EMAIL')}")
```

---

## 📞 Getting Help | 获取帮助

If you encounter problems during configuration:

如果在配置过程中遇到问题：

1. Check `README.md` for detailed instructions | 查看 `README.md` 中的详细说明
2. Check examples in `.env.example` file | 检查 `.env.example` 文件中的示例
3. Check the project's Issues page | 查阅项目的 Issue 页面
4. Contact project maintainers | 联系项目维护者

---

**Final Reminder**: Protect your sensitive information, code securely! 🔐

**最后提醒**: 保护好自己的敏感信息，安全 coding！🔐
