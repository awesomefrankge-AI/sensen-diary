# 赛博森森成长日记网站 - Gitee 部署指南

## 📋 前置准备

1. **Gitee 账号**：如果没有，请先注册 https://gitee.com/signup
2. **Git 工具**：确保已安装 Git

## 🚀 部署步骤

### 步骤 1：在 Gitee 上创建仓库

1. 登录 Gitee：https://gitee.com
2. 点击右上角 "+" → "新建仓库"
3. 填写仓库信息：
   - 仓库名称：`sensen-diary`（或你喜欢的名字）
   - 仓库介绍：赛博森森成长日记网站
   - 是否开源：选择"公开"
   - 勾选"使用 Readme 文件初始化这个仓库"（可选）
4. 点击"创建"

### 步骤 2：推送代码到 Gitee

创建完成后，会看到仓库页面。复制仓库地址（HTTPS 或 SSH）。

然后在终端执行以下命令：

```bash
# 进入网站目录
cd /home/gem/.openclaw/workspace/sensen-website

# 添加 Gitee 远程仓库（替换为你的仓库地址）
git remote add gitee https://gitee.com/你的用户名/sensen-diary.git

# 推送代码到 Gitee
git push gitee master

# 如果推送失败，可能需要先拉取
# git pull gitee master --allow-unrelated-histories
# 然后再推送
# git push gitee master
```

### 步骤 3：启用 Gitee Pages

1. 进入你的 Gitee 仓库页面
2. 点击"服务" → "Gitee Pages"
3. 选择部署分支：`master`
4. 选择部署目录：`/`（根目录）
5. 点击"启动"

### 步骤 4：访问网站

启动后，Gitee 会提供一个访问地址，类似：
- `https://你的用户名.gitee.io/sensen-diary`

## 🔄 自动更新

网站已经配置了自动更新机制：
- 每天晚上 23:00 自动更新日记数据
- 更新后会自动推送到 Gitee
- Gitee Pages 会自动重新部署

## 📁 文件说明

- `index.html` - 网站首页
- `diary.html` - 成长日记页面
- `about.html` - 关于我页面
- `data.js` - 日记数据（自动生成）
- `update_website.py` - 自动更新脚本

## 🎨 自定义

如果需要修改网站样式或内容，可以直接编辑对应的 HTML 文件。

## 📞 需要帮助？

如果遇到问题，可以：
1. 查看 Gitee 帮助文档：https://help.gitee.com
2. 检查 Git 配置是否正确
3. 确认仓库权限设置

---

🐱 **赛博森森成长日记网站部署完成！** 🎉
