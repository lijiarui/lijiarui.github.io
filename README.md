# lijiarui.github.io

李佳芮的个人博客。GitHub Pages 静态站，2026 重构。

## 目录结构

```
.
├── index.html              # 首页（自动生成）
├── 404.html                # 404 页（手写）
├── blog/index.html         # 博客列表页（自动生成）
├── slides/index.html       # 分享 PPT 页（自动生成）
├── slides/files/<slug>/    # 上传 PPT 的预览页（自动生成）
├── claude/index.html       # Claude 永动机页（自动生成）
├── about/index.html        # 关于页（rewriter 改造）
├── thought/, chatbot/...   # 8 个分类目录，共 109 篇文章
├── files/slides/           # 你上传的 PPT/PDF + 可选 .md 描述
├── img/slides/             # 自动生成的 PPT 第一页封面图（缓存）
├── content.json            # 全站元数据（rewriter 与 build 都依赖）
├── search-index.json       # 站内搜索索引（自动生成）
├── css/site.css            # 全站样式
├── js/search.js            # 客户端搜索
├── images/avatar.jpg       # 站点头像
├── images/wechat-qr.jpg    # 公众号二维码
├── img/                    # 文章配图（按年份分目录）
├── _build_pages.py         # 生成首页 / 博客 / 分享 PPT / Claude / 搜索索引
├── _rewrite_posts.py       # 重写 109 篇文章详情页 + about 页
└── _publish_feishu.py      # 把飞书 wiki 文章拉下来转成博客（一次性脚本）
```

## 本地预览

```bash
python3 -m http.server 8080 --bind 127.0.0.1
open http://127.0.0.1:8080/
```

## 内容更新

**新增 / 编辑文章**：直接修改 `content.json` 的对应条目，再跑：

```bash
python3 _build_pages.py    # 重建首页 / 列表页 / 搜索索引
python3 _rewrite_posts.py  # 重建文章详情页（如有改动）
```

两个脚本都是幂等的，重复跑没事。

**改头像 / 公众号二维码**：替换 `images/avatar.jpg` / `images/wechat-qr.jpg`。如浏览器有缓存，把 `_build_pages.py` 和 `_rewrite_posts.py` 里的 `?v=2` 改成更大数字强刷一次即可。

**新增 PPT / PDF 分享**（最常用流程）：

1. 把文件丢到 `files/slides/` 目录，文件名建议格式：`YYYY-MM-DD-标题.pdf` 或 `YYYY-MM-DD-标题.pptx`
   - 例：`2025-04-27-juzibot-pitch.pdf`
   - 不带日期前缀也行，会用文件修改时间
2. **可选**：在同一目录建一个 `<同名>.md` 文件覆盖标题、加标签和描述：

   ```markdown
   ---
   title: 你想要的中文标题（覆盖文件名）
   tags: 创业, AI, 产品
   date: 2025-04-27
   ---

   一段描述。支持 **加粗**、[链接](https://...)、列表、引用、标题。
   会展示在详情页 PPT 预览上方。
   ```

3. 跑 `python3 _build_pages.py`
4. `/slides/` 列表自动多出一张卡——封面是 PPT 第一页（自动 qlmanage 抽取，缓存到 `img/slides/`），点进去是描述 + 在线预览
5. 首页"最近在写"也会按日期混入新上传的 PPT
6. **PDF 任何环境都能本地预览**（浏览器内置）
7. **PPT/PPTX 必须推到 GitHub 后才能预览**——走 Office Online viewer，需要公网 URL，本地 127.0.0.1 看不到（页面会显示提示）
8. 强烈建议导出为 PDF 上传——加载快、显示稳定、跨设备一致

**从飞书把文章发布为博客**：

1. 在 `_publish_feishu.py` 里编辑 `ARTICLES` 列表，添加：源 markdown 路径（先用 `lark-cli docs +fetch --doc <wiki url>` 拉下来）、slug、日期、分类、标签
2. 跑 `python3 _publish_feishu.py` → `python3 _rewrite_posts.py` → `python3 _build_pages.py`
3. 文章自动注册到 `content.json`，进 feed / search / 列表页

**改侧栏文案 / nav / 微信号**：改 `_build_pages.py` 和 `_rewrite_posts.py` 里 `sidebar()` / `topnav()` 这两个函数，跑一遍两个脚本。

## 评论系统：LiveRe（来必力）

**为什么选它**：免费、国内访问快、支持游客评论（无需登录）、自带邮件通知。
缺点：免费版评论区底部有"由 LiveRe 提供"小 footer，去不掉。

**当前状态**：已接入。UID = `AwCdtY6RULKUsR5ehN3E`（Site: RUI 的博客）。
106 篇文章详情页底部都已嵌入 LiveRe `<div id="lv-container" data-id="city" data-uid="...">`。

**LiveRe 管理后台**：

- 登录入口：https://www.livere.com/ （右上角"登录"，账号 `rui@juzi.bot`）
- 我的站点 / 我的设置：https://livere.com/myhome
- 评论管理（看 / 删 / 审核所有评论）：登录后导航到 "评论管理"
- 通知设置（开关邮件通知）：登录后导航到 "通知设置"
- 颜色 / 主题定制：登录后导航到 "外观设置 / 主题颜色"
- 站点配色已配为站点橙色 `#d26911`，详见 README "颜色"段落或 `css/site.css`

**剩余你要在 LiveRe 后台手动配置**：

1. **开"游客评论"**：基本设置 → 找"游客评论"/"匿名评论"开关 → 开启。这样访客填昵称+邮箱+网址就能发，不强制 SNS 登录
2. **开邮件通知**：通知设置 → 新评论邮件通知 → 收件箱填 `rui@juzi.bot`
3. **关键词过滤 / 先审后发**（推荐）：评论管理 → 开审核，避免被刷垃圾
4. **本地 127.0.0.1 看不到评论是正常的**——LiveRe referer 校验不过，必须推到 https://lijiarui.github.io 后才能真测试

**关于微信登录**：LiveRe 城市版不支持，2026 年也没有现成方案能给静态博客接微信 OAuth（备案 + 开放平台 + 公司主体 + 后端三件套缺一不可）。建议：博客评论用 LiveRe 游客模式覆盖基础互动，深度互动引到公众号文章评论。

**换 UID 流程**（如果哪天换站或重新申请）：

```bash
sed -i '' 's/AwCdtY6RULKUsR5ehN3E/新UID/g' _rewrite_posts.py
python3 _rewrite_posts.py
```

## 部署

GitHub Pages 自动从 `main` 分支根目录部署。本地确认无误后：

```bash
git add -A
git commit -m "update content"
git push origin main
```

几分钟内 https://lijiarui.github.io 生效。

## 历史

- 2012-2023：Hexo 静态生成，主题 JSimple
- 2026-04：完全重构，去掉 Hexo 主题，改成手写 CSS + Python 脚本生成
- 2026-04：评论从 Disqus 迁移到 LiveRe，新增搜索、PPT 上传预览、Claude 永动机栏目
- 旧首页备份在 `index-old.html`，旧文章备份在 `/tmp/posts-backup.tar.gz`（如未清理）

## 依赖

- Python 3 (built-in stdlib)
- `markdown` (pip3 install markdown) — 用于 `_publish_feishu.py` 把 Markdown 转 HTML
- macOS `qlmanage` (内置) — 用于自动抽取 PPT/PDF 第一页作封面
- `lark-cli` (npm install -g @larksuite/cli) — 用于拉飞书文档
