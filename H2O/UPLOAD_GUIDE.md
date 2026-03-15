# 📤 GitHub Upload Guide | GitHub 上传指南

## One Sentence Summary | 一句话总结

**Except for the `.env` file, all other files can be safely uploaded to GitHub.**

**除了 `.env` 文件，其他所有文件都可以安全上传到 GitHub。**

---

## ✅ Files That CAN Be Uploaded | 可以上传的文件列表

The following files **MUST be uploaded** - they contain NO sensitive information:

以下文件**必须上传**，它们不包含任何敏感信息：

```
✅ email_gaussian_runner.py    # Main program (all sensitive info removed) | 主程序（已移除所有敏感信息）
✅ README.md                    # Project documentation | 项目说明文档
✅ QUICKSTART.md                # Quick start guide | 快速开始指南
✅ DEPLOYMENT.md                # Deployment configuration guide | 部署配置指南
✅ DOCS_INDEX.md                # Documentation index | 文档索引
✅ PROJECT_SUMMARY.md           # Project summary | 项目总结
✅ UPLOAD_GUIDE.md              # Upload guide (this file) | 上传指南（本文档）
✅ LICENSE                      # MIT License | MIT 许可证
✅ requirements.txt             # Python dependencies | Python 依赖说明
✅ .env.example                 # Configuration template (placeholders only) | 配置模板（仅占位符）
✅ .gitignore                   # Git ignore rules | Git 忽略规则
```

---

## ❌ Files That CANNOT Be Uploaded | 不要上传的文件列表

The following file **MUST NOT be uploaded** - it contains your real email and auth code:

以下文件**绝对不要上传**，包含你的真实邮箱和授权码：

```
❌ .env                        # Your real email configuration (most important!) | 你的真实邮箱配置（最重要！）
```

⚠️ **Note**: `.gitignore` has already excluded the `.env` file, so when you run `git add .`, it won't be included.

⚠️ **注意**：`.gitignore` 已经自动排除了 `.env` 文件，所以你执行 `git add .` 时不会包含它。

---

## 🚀 Upload Steps | 上传步骤

### 1. Create .env File (Local Use Only) | 创建 .env 文件（本地使用）

```bash
# Execute in project directory | 在项目目录执行
copy .env.example .env
```

Edit the `.env` file and fill in your real information:

编辑 `.env` 文件，填入你的真实信息：
```ini
FROM_EMAIL=your_qq_email@qq.com          # Your QQ email | 你的 QQ 邮箱
EMAIL_PASSWORD=your_auth_code            # Your QQ email auth code | 你的 QQ 邮箱授权码
TO_EMAIL=recipient@example.com           # Recipient email | 接收通知的邮箱
GAUSSIAN_DIR=F:\Gauss\Gauss\G16W         # Gaussian installation path | Gaussian 安装路径
```

### 2. Test the Program | 测试程序

```bash
python email_gaussian_runner.py
```

Ensure the program runs successfully.

确保程序能正常运行。

### 3. Upload to GitHub | 上传到 GitHub

```bash
# Initialize Git | 初始化 Git
git init

# Add all files (.env will be automatically excluded) | 添加所有文件（.env 会被自动排除）
git add .

# Check file list (confirm no .env) | 检查文件列表（确认没有 .env）
git status

# Commit | 提交
git commit -m "Initial commit"

# Link remote repository (replace with your repo URL) | 关联远程仓库（替换为你的仓库地址）
git remote add origin https://github.com/YOUR_USERNAME/H2O.git

# Push | 推送
git push -u origin main
```

---

## 🔍 How to Confirm .env Was NOT Uploaded | 如何确认 .env 没有被上传

Execute the following command:

执行以下命令：

```bash
git status
```

You should see output like this:

你应该看到类似这样的输出：

```
Changes to be committed:
  (use "git rm --cached <file>..." to unstage)
        new file:   .env.example
        new file:   .gitignore
        new file:   README.md
        ...other files...

Untracked files:
  (use "git add <file>..." to include in what will be committed)
        .env          <-- This is in Untracked area, won't be committed | 这个在 Untracked 区域，不会被提交
```

If `.env` appears in the "Changes to be committed" area, execute:

如果 `.env` 出现在 "Changes to be committed" 区域，执行：

```bash
git rm --cached .env
git commit -m "Remove .env from tracking"
```

---

## 🎯 Quick Reference | 快速记忆

| File Type | Can Upload? | Reason |
|-----------|-------------|--------|
| Code Files (.py) | ✅ Yes | All sensitive info removed | 已移除所有敏感信息 |
| Documentation Files (.md) | ✅ Yes | No sensitive information | 不包含敏感信息 |
| Configuration Files (.env) | ❌ No | Contains real email and auth code | 包含真实邮箱和授权码 |
| Configuration Templates (.env.example) | ✅ Yes | Placeholders only, no real info | 只有占位符，无真实信息 |

---

## ⚠️ What If I Accidentally Uploaded .env? | 如果不小心上传了 .env 怎么办？

Immediately execute the following steps:

立即执行以下步骤：

1. **Remove from Git history** | 从 Git 历史中删除：
   ```bash
   git rm --cached .env
   git commit -m "Remove .env"
   ```

2. **Force push to GitHub** | 强制推送到 GitHub：
   ```bash
   git push --force
   ```

3. **Change the leaked auth code** | 更改泄露的授权码：
   - Log in to QQ Mail | 登录 QQ 邮箱
   - Regenerate auth code | 重新生成授权码
   - Update local `.env` file | 更新本地的 `.env` 文件

---

## 📞 FAQ | 常见问题

**Q: Can I upload .env to a private repository?**  
**Q: 我可以把 .env 上传到私有仓库吗？**

A: Not recommended. Even for private repositories, avoid uploading sensitive information. Always use environment variables.  
A: 不建议。即使是私有仓库，也应该避免上传敏感信息。始终使用环境变量管理配置。

**Q: What is .env.example?**  
**Q: .env.example 是什么？**

A: It's a template file containing only placeholders (e.g., `your_qq_email@qq.com`), no real information, safe to share.  
A: 这是一个模板文件，只包含占位符（如 `your_qq_email@qq.com`），不含真实信息，可以安全分享。

**Q: How to verify there's no sensitive info in the code?**  
**Q: 如何验证代码中没有敏感信息？**

A: Execute the following command to search:  
A: 执行以下命令搜索：
```bash
grep -r "@qq.com" --include="*.py" .
grep -r "password" --include="*.py" .
```
You should only see example text in comments or `.env.example`.  
应该只在注释或 `.env.example` 中看到示例文本。

---

**Remember: Protect your email and auth code, security first!** 🔐

**记住：保护好自己的邮箱和授权码，安全第一！** 🔐
