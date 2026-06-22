# 🚀 独立站上线指南 — GitHub Pages

## 你需要准备
- 一个 GitHub 账号（没有的话去 github.com 注册，用 2191829064@qq.com 即可）
- 10 分钟时间

---

## 第一步：在 GitHub 创建仓库（3分钟）

1. 打开 https://github.com/new
2. 填写：
   - **Repository name**: `nexforge`（或你的品牌名）
   - **Description**: `Precision 3D Printing & CNC Prototyping Service`
   - **Public** ✅ 选 Public（GitHub Pages 免费）
   - **不要勾选** "Add a README file"
3. 点击 **Create repository**
4. 你会看到一页指令，**不要关掉**，等会要用

---

## 第二步：生成 Personal Access Token（2分钟）

因为 GitHub 不再支持密码登录 Git，需要用 Token：

1. 打开 https://github.com/settings/tokens
2. 点击 **Generate new token (classic)**
3. 勾选 `repo`（全部子项自动勾选）
4. 点击 **Generate token**
5. ⚠️ **立刻复制**那个 `ghp_xxxx` 开头的字符串（关掉页面就看不到了）

---

## 第三步：推送代码（2分钟）

回到 WorkBuddy，打开终端（或让我帮你执行），运行：

```bash
cd "C:\Users\马文彬\WorkBuddy\Claw\Claw\website"

# 替换 YOUR_USERNAME 为你的 GitHub 用户名
git remote add origin https://github.com/YOUR_USERNAME/nexforge.git

# 推送（会提示输入用户名和 Token）
git push -u origin master
```

弹窗输入：
- Username: 你的 GitHub 用户名
- Password: **刚才复制的 Token**（不是 GitHub 密码！）

---

## 第四步：开启 GitHub Pages（2分钟）

1. 打开 `https://github.com/YOUR_USERNAME/nexforge/settings/pages`
2. **Source**: Deploy from a branch
3. **Branch**: `master` / `/(root)`
4. 点击 **Save**
5. 等 1-2 分钟刷新，页面顶部会显示：
   > ✅ Your site is live at `https://YOUR_USERNAME.github.io/nexforge/`

---

## 第五步：绑定自定义域名（可选，有域名之后做）

1. 买个域名（推荐 Namesilo，`nexforge.com` ~$12/年）
2. 在 GitHub Pages 设置里填入域名
3. 在域名商后台添加 CNAME 记录指向 `YOUR_USERNAME.github.io`

---

## 验证

上线后，用手机打开 `https://YOUR_USERNAME.github.io/nexforge/`，应该看到完整网站。

---

## ⚠️ 如果你让我帮你做

告诉我你的 GitHub 用户名，我可以帮你完成：
- 设置 remote
- 推送代码
- （Token 还是需要你提供，我不会知道）

---

_准备好了告诉我你的 GitHub 用户名，我帮你一键推送。_
