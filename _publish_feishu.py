#!/usr/bin/env python3
"""Convert Feishu markdown articles to Hexo-format HTML stubs and register
them in content.json so _rewrite_posts.py and _build_pages.py pick them up.
"""
import json
import re
from html import escape
from pathlib import Path

import markdown as md_lib

ROOT = Path(__file__).parent

# (source_md_path, slug, date, category, tags)
ARTICLES = [
    {
        "src": "/tmp/feishu-articles/CfI9wD3Jti4F0rk3uCGcwqK2nJb.md",
        "slug": "2025-12-31-last-day-of-2025",
        "title": "写在 2025 年的最后一天",
        "date": "2025-12-31T23:59:00.000Z",
        "category": "thought",
        "tags": ["总结", "思考"],
    },
    {
        "src": "/tmp/feishu-articles/JODGwBjJSi4jEYkpjKTcBoqxnsd.md",
        "slug": "2025-12-31-2025-thought-slices",
        "title": "2025 年思想切片",
        "date": "2025-12-31T23:00:00.000Z",
        "category": "thought",
        "tags": ["思考", "思考切片"],
    },
    {
        "src": "/tmp/feishu-articles/OjFwwUr6mi2moWkpkz7c7WO7nee.md",
        "slug": "2026-01-31-juzibot-2026",
        "title": "写在句子互动的 2026 年",
        "date": "2026-01-31T10:00:00.000Z",
        "category": "thought",
        "tags": ["句子互动", "创业", "计划"],
    },
]

HEXO_TEMPLATE = """<!DOCTYPE HTML>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<title>{title} - 李佳芮de博客</title>
<link rel="stylesheet" href="/css/site.css">
</head>
<body>
<article class="post" itemscope itemtype="http://schema.org/BlogPosting">
  <div class="post-header">
    <div class="post-author clearfix">
      <p>
        <span class="label">作者</span>
        <a href="/" target="_blank">李佳芮</a>
        <span title="最后编辑于&nbsp;{date_short}">{date_short}</span>
      </p>
    </div>
    <h2 class="post-title">{title}</h2>
    <div class="post-meta">本文共计{word_count}个字</div>
  </div>
  <div class="post-content markdown-body">
{body_html}
  </div>
  <div class="post-tags">标签：
{tags_html}
  </div>
</article>
</body>
</html>
"""


def clean_md(text):
    """Strip lark-cli WARN line + first # title line. Return body markdown."""
    lines = text.split("\n")
    out = []
    seen_title = False
    for line in lines:
        if "[lark-cli]" in line and "WARN" in line:
            continue
        if not seen_title and re.match(r"^#\s+", line):
            seen_title = True
            continue
        out.append(line)
    return "\n".join(out).strip()


def md_to_plain_text(md_body):
    """Strip markdown syntax to get plain text for excerpt + word count."""
    text = re.sub(r"```.*?```", "", md_body, flags=re.S)
    text = re.sub(r"`[^`]+`", "", text)
    text = re.sub(r"!\[[^\]]*\]\([^)]+\)", "", text)
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    text = re.sub(r"[#>*_\-]", "", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def make_excerpt(text, n=160):
    if len(text) <= n:
        return text
    cut = text[:n]
    for sep in ["。", "！", "？", "；", "，"]:
        idx = cut.rfind(sep)
        if idx > n * 0.6:
            return cut[: idx + 1]
    return cut + "…"


def main():
    cj_path = ROOT / "content.json"
    data = json.loads(cj_path.read_text())

    existing_paths = {p["path"] for p in data["posts"]}

    converter = md_lib.Markdown(extensions=["extra", "sane_lists"])

    added = 0
    for art in ARTICLES:
        src_path = Path(art["src"])
        if not src_path.exists():
            print(f"  SKIP missing source: {src_path}")
            continue
        raw = src_path.read_text(encoding="utf-8")
        body_md = clean_md(raw)
        body_html = converter.convert(body_md)
        converter.reset()
        plain = md_to_plain_text(body_md)

        path = f"{art['category']}/{art['slug']}.html"

        # Tag <a> links matching legacy Hexo format (rewriter parses these)
        tags_html = "\n".join(
            f'    <a href="/tags/{escape(t)}/">{escape(t)}</a>' for t in art["tags"]
        )

        date_short = art["date"][:10]
        html = HEXO_TEMPLATE.format(
            title=escape(art["title"]),
            date_short=escape(date_short),
            word_count=len(plain),
            body_html=body_html,
            tags_html=tags_html,
        )

        out_path = ROOT / path
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(html, encoding="utf-8")
        print(f"  wrote {path} ({len(html):,} bytes)")

        # Register in content.json (skip if already exists)
        if path in existing_paths:
            print(f"    already in content.json — skipping registration")
            continue

        post_entry = {
            "title": art["title"],
            "slug": art["slug"],
            "date": art["date"],
            "updated": art["date"],
            "comments": True,
            "path": path,
            "link": "",
            "permalink": f"https://rui.juzi.bot/{path}",
            "excerpt": "",
            "text": plain,
            "categories": [{
                "name": art["category"],
                "slug": art["category"],
                "permalink": f"https://rui.juzi.bot/categories/{art['category']}/",
            }],
            "tags": [{
                "name": t,
                "slug": t,
                "permalink": f"https://rui.juzi.bot/tags/{t}/",
            } for t in art["tags"]],
            "keywords": [{
                "name": art["category"],
                "slug": art["category"],
                "permalink": f"https://rui.juzi.bot/categories/{art['category']}/",
            }],
        }
        data["posts"].insert(0, post_entry)
        added += 1

    cj_path.write_text(json.dumps(data, ensure_ascii=False, separators=(",", ":")))
    print(f"added {added} posts to content.json")
    print(f"now run: python3 _rewrite_posts.py && python3 _build_pages.py")


if __name__ == "__main__":
    main()
