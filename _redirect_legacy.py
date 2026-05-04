#!/usr/bin/env python3
"""把旧 Hexo 主题留下来的聚合页（/page/N、/archives、/categories、/tags）全部改写成
SEO 友好的轻量跳转页：canonical 指向新站点的对应位置，meta-refresh + JS 双保险。

Google 看到 canonical + 0 秒 refresh 会按 soft 301 处理，几周内把权重合并到新地址。
不加 noindex —— noindex 只会让旧 URL 被丢弃，不会把权重转移到新页。
"""
from __future__ import annotations

from html import escape
from pathlib import Path

ROOT = Path(__file__).parent
SITE = "https://rui.juzi.bot"

# 新站只有这几个分类有锚点过滤
CANONICAL_CATS = {"thought", "chatbot", "interview", "project", "reading", "saas", "microsoft"}

REDIRECT_TMPL = """<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<title>{title} · 李佳芮</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="{desc}">
<link rel="canonical" href="{target}">
<meta http-equiv="refresh" content="0; url={target}">
<meta property="og:title" content="{title} · 李佳芮">
<meta property="og:url" content="{target}">
<meta property="og:type" content="website">
<script>location.replace({target_js});</script>
<style>body{{font:14px/1.7 -apple-system,BlinkMacSystemFont,"PingFang SC",sans-serif;max-width:560px;margin:80px auto;padding:0 20px;color:#222}}a{{color:#c0392b}}</style>
</head>
<body>
<p>这个页面已经搬到 <a href="{target}">{display}</a>。如果没有自动跳转，请点击链接。</p>
</body>
</html>
"""


def write_redirect(rel_path: Path, target_path: str, title: str, display: str, desc: str = "") -> None:
    """rel_path: 相对仓库根的路径（带 index.html）。target_path: 站内路径，如 /blog/ 或 /blog/#thought。"""
    target = SITE + target_path
    if not desc:
        desc = f"页面已迁移到 {display}"
    out = REDIRECT_TMPL.format(
        title=escape(title),
        desc=escape(desc),
        target=escape(target),
        target_js='"' + target.replace('"', '\\"') + '"',
        display=escape(display),
    )
    full = ROOT / rel_path
    full.parent.mkdir(parents=True, exist_ok=True)
    full.write_text(out, encoding="utf-8")


def redirect_blog_paginations() -> int:
    """/page/2/ ... /page/N/ → /blog/"""
    n = 0
    page_dir = ROOT / "page"
    if not page_dir.is_dir():
        return 0
    for sub in sorted(page_dir.iterdir()):
        if sub.is_dir() and sub.name.isdigit():
            write_redirect(
                Path("page") / sub.name / "index.html",
                "/blog/",
                f"博客 第 {sub.name} 页",
                "博客全部文章",
                "李佳芮的博客全部文章已合并到一个页面，按时间倒序，可按分类筛选。",
            )
            n += 1
    return n


def redirect_archives() -> int:
    """/archives/ + /archives/page/N/ + /archives/YYYY/ + /archives/YYYY/MM/ + /archives/YYYY/page/N/"""
    n = 0
    arch = ROOT / "archives"
    if not arch.is_dir():
        return 0

    # /archives/index.html
    if (arch / "index.html").exists():
        write_redirect(
            Path("archives/index.html"),
            "/blog/",
            "归档",
            "博客全部文章",
            "归档已合并到博客列表，按年份和分类筛选。",
        )
        n += 1

    # /archives/page/N/index.html
    page = arch / "page"
    if page.is_dir():
        for sub in sorted(page.iterdir()):
            if sub.is_dir() and sub.name.isdigit():
                write_redirect(
                    Path("archives/page") / sub.name / "index.html",
                    "/blog/",
                    f"归档 第 {sub.name} 页",
                    "博客全部文章",
                )
                n += 1

    # /archives/YYYY/...
    for year_dir in sorted(arch.iterdir()):
        if not year_dir.is_dir() or not (year_dir.name.isdigit() and len(year_dir.name) == 4):
            continue
        year = year_dir.name
        # /archives/YYYY/index.html → /blog/#yYYYY
        if (year_dir / "index.html").exists():
            write_redirect(
                Path("archives") / year / "index.html",
                f"/blog/#y{year}",
                f"{year} 年文章归档",
                f"{year} 年博客文章",
            )
            n += 1
        # /archives/YYYY/page/N/
        ypage = year_dir / "page"
        if ypage.is_dir():
            for sub in sorted(ypage.iterdir()):
                if sub.is_dir() and sub.name.isdigit():
                    write_redirect(
                        Path("archives") / year / "page" / sub.name / "index.html",
                        f"/blog/#y{year}",
                        f"{year} 年文章归档 第 {sub.name} 页",
                        f"{year} 年博客文章",
                    )
                    n += 1
        # /archives/YYYY/MM/index.html
        for month_dir in sorted(year_dir.iterdir()):
            if month_dir.is_dir() and month_dir.name.isdigit() and len(month_dir.name) == 2:
                if (month_dir / "index.html").exists():
                    write_redirect(
                        Path("archives") / year / month_dir.name / "index.html",
                        f"/blog/#y{year}",
                        f"{year} 年 {int(month_dir.name)} 月文章归档",
                        f"{year} 年博客文章",
                    )
                    n += 1
    return n


def redirect_categories() -> int:
    """/categories/<cat>/ + /categories/<cat>/page/N/"""
    n = 0
    cats = ROOT / "categories"
    if not cats.is_dir():
        return 0
    for cat_dir in sorted(cats.iterdir()):
        if not cat_dir.is_dir():
            continue
        cat = cat_dir.name
        anchor = f"#{cat}" if cat in CANONICAL_CATS else ""
        target = f"/blog/{anchor}"
        # /categories/<cat>/index.html
        if (cat_dir / "index.html").exists():
            write_redirect(
                Path("categories") / cat / "index.html",
                target,
                f"分类：{cat}",
                "博客分类",
            )
            n += 1
        # /categories/<cat>/page/N/
        cpage = cat_dir / "page"
        if cpage.is_dir():
            for sub in sorted(cpage.iterdir()):
                if sub.is_dir() and sub.name.isdigit():
                    write_redirect(
                        Path("categories") / cat / "page" / sub.name / "index.html",
                        target,
                        f"分类：{cat} 第 {sub.name} 页",
                        "博客分类",
                    )
                    n += 1
    return n


def redirect_tags() -> int:
    """/tags/<tag>/ —— 新站没有标签页，全部回 /blog/。tag 名是中文，URL 编码由浏览器处理。"""
    n = 0
    tags = ROOT / "tags"
    if not tags.is_dir():
        return 0
    for tag_dir in sorted(tags.iterdir()):
        if not tag_dir.is_dir():
            continue
        tag = tag_dir.name
        if (tag_dir / "index.html").exists():
            write_redirect(
                Path("tags") / tag / "index.html",
                "/blog/",
                f"标签：{tag}",
                "博客全部文章",
                f"标签 “{tag}” 的文章已合并回博客列表。",
            )
            n += 1
        tpage = tag_dir / "page"
        if tpage.is_dir():
            for sub in sorted(tpage.iterdir()):
                if sub.is_dir() and sub.name.isdigit():
                    write_redirect(
                        Path("tags") / tag / "page" / sub.name / "index.html",
                        "/blog/",
                        f"标签：{tag} 第 {sub.name} 页",
                        "博客全部文章",
                    )
                    n += 1
    return n


def main() -> None:
    counts = {
        "page": redirect_blog_paginations(),
        "archives": redirect_archives(),
        "categories": redirect_categories(),
        "tags": redirect_tags(),
    }
    total = sum(counts.values())
    print(f"✓ 改写 {total} 个旧聚合页为跳转页")
    for k, v in counts.items():
        print(f"  - {k}: {v}")


if __name__ == "__main__":
    main()
