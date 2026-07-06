# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

李佳芮的个人博客（rui.juzi.bot），纯静态站。**没有框架** — 用一组 Python 脚本读 `content.json` + `posts/*.md`，渲染成 HTML 直接 push 到 GitHub Pages。2026-04 从 Hexo 重构而来。详细作者向使用说明在 `README.md`。

## 发布红线（最重要，先读这条）

**只发布本次明确点名要发的那一篇文章。** 没点名的 `.md` 一律不发——哪怕它没标 `draft`、`build.py` 会把它一起渲染进 `content.json` / `feed.xml` / `index.html`，也要先拦住。作者被坑过：曾有一次 `git add -A` 误推了 4 篇文章（含 3 篇草稿）到公开网址，紧急撤回。红线是「**宁可漏发，不可误发**」。

操作纪律：

1. **永远不用 `git add -A`**。只显式 `git add` 点名那篇的 `posts/<slug>.md` + `img/posts/<slug>/`。云端构建后渲染 HTML 和聚合文件不需要 add——CI 会生成。
2. **push 的每个 commit 都会被 CI 全量 build 并上线**：凡是已提交且 `draft` 不为 true 的 `posts/*.md` 都会被发布。本地未跟踪的草稿不影响线上（CI 看不到），但绝不能把未点名的 `.md` add 进任何 commit。改共享组件（侧栏 / topnav / css / 构建脚本）的 commit 同样会全站生效，推前想清楚。
3. **推/提 PR 之前，先把"哪些文章会变上线"列成清单**，等到明确确认（"推 / yes"）才动。在 GitHub Actions / @claude 场景下，永远只**提 PR 交人审**，不直接 push 到默认分支。

## 核心命令

```bash
python3 build.py                            # 唯一构建命令，串四步（本地预览用，产物不用 commit）
python3 -m http.server 8080 --bind 127.0.0.1   # 本地预览
git add posts/<那篇>.md img/posts/<slug>/ && git commit -m '...' && git push   # 上线
```

**2026-07 起云端构建**：Pages 是 GitHub Actions 模式（`.github/workflows/pages.yml`），push master 后 CI 自动跑 `build.py` 并部署。**发布只需要推源文件**（`.md` + 图片），渲染 HTML / `content.json` / `feed.xml` / `search-index.json` / `sitemap.xml` 由 CI 生成，不需要也不应该再 add。仓库里现存的旧渲染产物会渐渐过时，无害。例外：PPT 封面图 `img/slides/<slug>.png` 靠 macOS qlmanage 生成，CI 上没有，上传新 slides 时要本地 build 一次并把封面图一起 commit。回滚整套云端构建：`gh api -X PUT repos/lijiarui/lijiarui.github.io/pages -f build_type=legacy`。

`build.py` 顺序执行（每一步失败就停）：

1. `_publish_posts.py` — 扫 `posts/*.md`，生成 hexo-format HTML stub 到 `<category>/<slug>.html`，并把条目写进 `content.json`
2. `_rewrite_posts.py` — 把所有文章详情页（旧 hexo + 新 md 都在一起）重新套上当前主题（topnav + sidebar + footer）
3. `_build_pages.py` — 重建 `index.html`、`blog/`、`slides/`、`claude/`、`yearly/`、`feed.xml`、`sitemap.xml`、`search-index.json`
4. `_redirect_legacy.py` — 把旧 Hexo 聚合页（`/page/N`、`/archives`、`/categories`、`/tags`）重写成 canonical + meta-refresh 跳转页

## 单一来源：content.json

`content.json` 是**站点元数据的真实源**。所有列表、搜索、feed、sitemap 都从它生成。

- 写新文章不要手动编辑 `content.json` —— `_publish_posts.py` 会自动 dedup-by-path 注册或更新条目
- 永远不要手编辑已渲染的文章 HTML（`chatbot/`、`thought/`、`interview/` 等目录下的 `.html`）—— 下次 `build.py` 会被覆盖。要改旧文章正文，改 `content.json` 里对应的 `text` 字段（不推荐，太麻烦），或者干脆把它改成 `posts/*.md` 重发
- 历史 109 篇 Hexo 文章已被 `_rewrite_posts.py` 改造过，逻辑统一

## 写一篇新文章

在 `posts/` 新建 `YYYY-MM-DD-slug.md`（参考 `posts/TEMPLATE.md`）：

```markdown
---
title: 中文标题
date: 2026-04-27
category: thought
tags: 创业, AI
draft: false       # 可选；true 则跳过发布并清理已渲染产物
slug: 自定义slug    # 可选；指定 canonical 文件名 stem，覆盖 date-prefix 逻辑
description: 自定义 SEO 摘要  # 可选；不填则取正文前 150 字
---
正文 Markdown。
```

**`category` 必须是这八个之一**（写在 `_publish_posts.py:VALID_CATEGORIES`）：`thought` / `reading` / `chatbot` / `project` / `saas` / `interview` / `microsoft` / `presentation`。其它值会被脚本拒绝。

**自动逻辑**：
- 标题包含 `写在 XX 年的最后一天` / `XX 年思想切片` / `写在句子互动的 XX 年`，会自动打 `年度思考` 标签并出现在 `/yearly/`
- frontmatter 没填 `date` 时从文件名 `YYYY-MM-DD-` 前缀提取
- `draft: true` 会从 `content.json` 删掉旧条目并清理已渲染 HTML，避免列表 404

## 上传 PPT/PDF 分享

把 `.pdf` 或 `.pptx` 丢到 `files/slides/`（建议命名 `YYYY-MM-DD-标题.<ext>`），可选放一份**同名** `.md` 写描述/标签 frontmatter。`build.py` 会调 macOS `qlmanage` 抽 PPT 第一页做封面。**PPT/PPTX 必须 push 到 GitHub 后线上才能预览**（Office Online viewer 需要公网 URL），强烈建议导出 PDF 上传。

## 飞书拉文章

如果原文写在飞书里，编辑 `_publish_feishu.py` 的 `ARTICLES` 列表加一行（url, slug, date, category, tags），再跑：

```bash
python3 _publish_feishu.py    # lark-cli 拉 markdown + 自动下载图片到 img/posts/<slug>/
python3 build.py
```

脚本会自动找 `<image token="..."/>`，调 `lark-cli docs +media-download` 下载并替换正文引用。需要 `lark-cli` 已登录（见 workspace `CLAUDE.md`）。

## 改站点全局元素去哪改

| 改什么 | 在哪改 |
|---|---|
| 顶栏 / 侧栏 / footer | `_build_pages.py` 和 `_rewrite_posts.py` 的 `topnav()` / `sidebar()` 函数（注意：要同时改两个文件） |
| `<head>` SEO meta / 统计 beacon | 同上，`HEAD` 常量 |
| 全站颜色 / 主题色 | `css/site.css` 顶部的 `:root { --accent: ... }` |
| LiveRe 评论 UID | `_rewrite_posts.py` 里搜 `livere-comment client-id` |
| 网站颜色橙 `#d26911` | 是站点品牌色，不要随便改 |

**坑**：百度统计 JS 里有 `{` `}`，写在 Python `.format()` 模板里必须转义成 `{{` `}}`，否则 `KeyError`。

## 不要乱碰

- `index-old.html` —— 旧首页备份，回滚用
- `tags/` —— Hexo 时代遗留的 case-collision 目录，macOS 上 git 总显示 `M`，忽略即可
- `search.xml`、旧的 `archives/`、`categories/`、`tags/` —— Hexo 时代产物，已被 `_redirect_legacy.py` 改写为跳转页，不要手编辑
- `.env*` / 任何 token / LiveRe 账密 —— 仓库不放敏感信息

## 依赖

- Python 3（系统自带）+ `pip3 install markdown`
- macOS `qlmanage`（PPT 封面）
- `lark-cli`（拉飞书文档；已在 workspace 全局配置）

没有 Node 工具链、没有打包器、没有 lint / test。改完肉眼起 http server 看效果就是测试。
