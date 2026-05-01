# lijiarui.github.io

李佳芮的个人博客。这份 README 是给我自己看的——下次回来不知道东西放哪、怎么发的，翻这里。

---

## 我要做什么？

### 1. 写一篇新博客

**步骤**：

1. 在 `posts/` 文件夹新建一个 `.md` 文件（参考 `posts/TEMPLATE.md`）
2. 文件名格式：`YYYY-MM-DD-英文-slug.md`
3. 文件开头加 frontmatter，正文用 Markdown：

   ```markdown
   ---
   title: 你想要的中文标题
   date: 2026-04-27
   category: thought
   tags: 创业, AI, 思考
   ---

   正文从这里开始，支持完整 Markdown。
   ```

4. 跑：
   ```bash
   python3 build.py
   ```
5. 看一眼本地 http://127.0.0.1:8080/
6. 推到线上：`git add -A && git commit -m '新文章' && git push`

**`category` 可选值**（决定文章放哪个分区）：
- `thought` — 思考（最常用）
- `reading` — 读书笔记
- `chatbot` — Chatbot 相关
- `project` — 项目记录
- `saas` — SaaS 相关
- `interview` — 访谈
- `microsoft` — 微软相关
- `presentation` — 演讲（一般用 `files/slides/` 上传 PPT 而不是这个）

**自动逻辑**：
- 标题里有 `写在 XX 年的最后一天`、`XX 年思想切片`、`写在句子互动的 XX 年` 的，会自动打 `年度思考` 标签，并出现在 `/yearly/` 页面
- 文章会自动进首页"最近在写"feed、`/blog/` 列表页和站内搜索

---

### 2. 上传一份 PPT 或 PDF 分享

**步骤**：

1. 把 `.pdf` 或 `.pptx` 文件丢到 `files/slides/`
2. 文件名建议：`YYYY-MM-DD-标题.pdf`（例：`2025-04-27-juzibot-pitch.pdf`）
3. **可选**：在同一目录建一个同名 `.md` 文件，写自定义标题、标签和描述：

   ```markdown
   ---
   title: 你想要的标题（覆盖文件名）
   tags: 创业, AI, 演讲
   ---

   一段描述。会出现在详情页 PPT 预览上方。支持 Markdown。
   ```

4. 跑 `python3 build.py`
5. `/slides/` 列表自动多出一张卡，封面是 PPT 第一页（自动从 macOS qlmanage 抽取）
6. 推到线上：`git add -A && git commit -m '新分享' && git push`

**注意**：
- **PDF** 在本地 + 线上都能预览
- **PPT/PPTX** 必须推到 GitHub 后才能预览（Office Online viewer 需要公网 URL）
- 强烈建议导出 PDF 上传——加载快、显示稳一致

---

### 3. 从飞书把现成文档拉过来发

如果文章已经写在飞书 wiki/docx 里：

1. 编辑 `_publish_feishu.py` 的 `ARTICLES` 列表，加一行：
   ```python
   ("https://juzihudong.feishu.cn/wiki/<token>",
    "2026-04-27-my-slug", "2026-04-27", "thought", ["年度思考", "标签2"]),
   ```
2. 跑：
   ```bash
   python3 _publish_feishu.py    # 拉 markdown + 自动下载图片到 img/posts/<slug>/
   python3 build.py              # 重建整站
   ```
3. 推到线上

图片处理：脚本会自动找飞书的 `<image token="..."/>` 标签，调 `lark-cli docs +media-download` 下载，按格式存到 `img/posts/<slug>/<token>.<ext>`，并替换正文里的引用。**图片不会遗漏**。

---

## 目录速查（我自己写内容时去哪改）

| 我要 | 改这里 |
|---|---|
| 写新博客 | `posts/<date>-<slug>.md` |
| 上传 PPT/PDF | `files/slides/<date>-<title>.<pdf\|pptx>` |
| 给 PPT 加描述 | `files/slides/<同名>.md` |
| 从飞书拉文章 | 编辑 `_publish_feishu.py` 的 `ARTICLES` 列表 |
| 改头像 | 替换 `images/avatar.jpg`（再把 `?v=2` 在脚本里改成 `?v=3` 强刷缓存） |
| 改公众号二维码 | 替换 `images/wechat-qr.jpg` |
| 改侧栏简介 | `_build_pages.py` 的 `sidebar()` 函数（搜 `about-box`） |
| 改顶栏链接 | `_build_pages.py` 和 `_rewrite_posts.py` 的 `topnav()` 函数 |
| 改全站颜色 | `css/site.css` 顶部的 `:root { --accent: ... }` |
| 改 LiveRe UID | `_rewrite_posts.py` 里搜 `livere-comment client-id` 全局替换 |

## 工作流命令速查

```bash
# 唯一需要记住的命令：
python3 build.py

# 它会顺序跑：
# 1. _publish_posts.py     发布 posts/*.md
# 2. _rewrite_posts.py     渲染所有文章详情页
# 3. _build_pages.py       重建首页/列表/搜索/年度思考

# 本地预览：
python3 -m http.server 8080 --bind 127.0.0.1
open http://127.0.0.1:8080/

# 推到线上：
git add -A && git commit -m '...' && git push
```

---

## 评论系统（LiveRe）

**当前状态**：已接入。UID 写在 `_rewrite_posts.py` 的 `livere-comment client-id` 那一行；登录账号见个人密码管理器。

**LiveRe 后台**：
- 登录入口：https://www.livere.com/
- 我的设置：https://livere.com/myhome
- 评论管理：登录后导航到"评论管理"
- 通知设置：登录后导航到"通知设置"
- 配色：站点橙色 `#d26911`，已配好

**已配置开关**（如果要改）：
- 游客评论：必须开（不强制 SNS 登录，访客填昵称+邮箱+网址即可）
- 邮件通知：开
- 关键词过滤 / 先审后发：建议开

**关于微信登录**：LiveRe 城市版不支持。要做的话需要备案 + 微信开放平台 + 公司主体 + 自架后端。投入太大，现状是博客评论用 LiveRe 游客模式覆盖基础互动，深度互动引到公众号文章评论。

---

## 站点统计（Umami + 百度统计）

**当前状态**：双埋点，两个 beacon 都在所有页面 head 里 `defer` 加载，不阻塞页面、无 cookie 弹窗。

### Umami Cloud（海外 + 部分国内）

- **登录**：https://cloud.umami.is
- **Website**：`rui.juzi.bot`
- **看数据**：登录 → 选对应站点 → Realtime / Overview / Sessions / Pages / Sources

**为什么用**：免费、隐私友好、无 cookie、报表 UI 干净。
**局限**：CDN 在海外，国内访问偶尔失败，国内用户数据会丢一部分。

### 百度统计（国内全覆盖）

- **登录**：https://tongji.baidu.com
- **网站**：`rui.juzi.bot`
- **看数据**：登录 → 实时访客 / 来源分析 / 搜索词 / 地域

**为什么用**：国内访问 100% 通；**百度搜索关键词数据是独家**——读者从百度搜什么进来，只有这里能看。

### Beacon 写在哪

两个统计的 `<script>` 都写在 `_build_pages.py` 和 `_rewrite_posts.py` 的 `HEAD` 常量里（搜 `cloud.umami.is` 和 `hm.baidu.com`）。具体 Website ID / Hash 看代码，不在这里列。

要改 ID / Hash：

1. 同时改两个文件的 `HEAD`
2. 跑 `python3 build.py`
3. push

**坑**：百度 JS 里有 `{` `}`（函数体），在 Python `.format()` 模板里必须转义成 `{{` `}}`，不然会报 `KeyError`。

**账号 / 密码**：登录账号、API key 等敏感信息**不放仓库**——存个人密码管理器。

### 为什么没做自定义大屏

试过一版 `/dashboard/` 自定义大屏，后来撤了——Umami 和百度自带的后台已经把 UV/PV/来源/页面/地域/设备/实时全给了，再做一份是重复造轮子。要自定义大屏可以拿 Umami API Key 调 REST API，但目前没必要。

---

## 小心，这些东西不要乱碰

- **`content.json`** 是博客元数据的来源，构建脚本依赖它。新文章会被脚本自动加进去，但不要手改（除非确定）
- **`tags/`** 目录是历史 Hexo 时代的产物，case-collision 在 macOS 上 git 总会显示 `M`，忽略即可
- **旧首页备份在 `index-old.html`**，回滚用
- **历史 109 篇文章的 HTML 文件**已经被 `_rewrite_posts.py` 改造过，不要再手编辑——改了下次构建会被覆盖。要永久改某篇旧文章，改 `content.json` 里对应的 `text` 字段（不推荐，太麻烦）

---

## 依赖

- Python 3（系统自带）
- `markdown`（一次性安装：`pip3 install markdown`）
- macOS `qlmanage`（系统自带，用于从 PPT 第一页抽封面）
- `lark-cli`（一次性安装：`npm install -g @larksuite/cli`，用于拉飞书文档）

---

## 历史

- 2012-2023：Hexo 静态生成，主题 JSimple
- 2026-04：完全重构——去掉 Hexo 主题，改成手写 CSS + Python 脚本生成 + LiveRe 评论 + PPT 上传预览 + 站内搜索 + 年度思考栏目
