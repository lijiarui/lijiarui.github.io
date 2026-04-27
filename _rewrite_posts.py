#!/usr/bin/env python3
"""Rewrite each post HTML with the new site layout.

Reads existing post HTML, extracts the article body / title / tags / date,
then wraps them in the new layout (top nav + sidebar + footer).
"""
import json
import re
from collections import Counter
from html import escape
from html import unescape as _unescape


def unescape(s):
    """Unescape repeatedly until stable — handles previously double-escaped strings."""
    if s is None:
        return s
    prev = None
    while prev != s:
        prev = s
        s = _unescape(s)
    return s
from pathlib import Path

ROOT = Path(__file__).parent

CAT_LABEL = {
    "thought": "思考",
    "chatbot": "Chatbot",
    "presentation": "演讲",
    "interview": "访谈",
    "project": "项目",
    "reading": "读书",
    "saas": "SaaS",
    "microsoft": "Microsoft",
    "tech": "Tech",
}

POST_DIRS = ["chatbot", "interview", "microsoft", "presentation",
             "project", "reading", "saas", "thought"]

HEAD = """<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} · 李佳芮的博客</title>
<meta name="description" content="{desc}">
<link rel="stylesheet" href="/css/site.css">
<link rel="shortcut icon" href="/images/favicon.png">
</head>
<body>
"""

FOOT = """<footer class="site-foot"><div class="wrap">
<a href="https://github.com/lijiarui">GitHub</a>
<a href="https://juzibot.com">句子互动</a>
<a href="/blog/">博客</a>
<a href="/claude/">Claude 永动机</a>
<a href="/slides/">分享 PPT</a>
<a href="/yearly/">年度思考</a>
<a href="/about/">关于</a>
<div class="copyright">© Li Jiarui · 时间看得见</div>
</div></footer>
<script src="/js/search.js" defer></script>
</body></html>
"""


def topnav():
    items = [
        ("home", "/", "首页"),
        ("blog", "/blog/", "博客"),
        ("claude", "/claude/", "Claude 永动机"),
        ("slides", "/slides/", "分享 PPT"),
        ("yearly", "/yearly/", "年度思考"),
        ("about", "/about/", "关于"),
    ]
    links = "".join(f'<a href="{href}">{label}</a>' for _, href, label in items)
    links += '<a href="https://github.com/lijiarui" target="_blank" rel="noopener" class="nav-ext" title="GitHub">GitHub ↗</a>'
    return f"""<header class="topnav"><div class="wrap row">
<div class="brand"><a href="/">李佳芮</a><span class="tagline">时间看得见</span></div>
<nav>{links}</nav>
</div></header>
"""


def load_posts():
    data = json.loads((ROOT / "content.json").read_text())
    posts = data["posts"]
    for p in posts:
        cat = p["categories"][0]["name"] if p.get("categories") else "thought"
        p["_cat"] = cat
        p["_cat_label"] = CAT_LABEL.get(cat, cat.title())
        d = p.get("date", "")
        p["_date"] = d[:10]
        p["_year"] = d[:4]
    posts.sort(key=lambda p: p.get("date", ""), reverse=True)
    return posts


def sidebar(posts, slide_posts):
    """Compact sidebar for article pages — fewer widgets, tighter."""
    recent_html = "".join(
        f'<li><a href="/{escape(p["path"])}">{escape(p["title"])}</a></li>'
        for p in posts[:8]
    )
    cat_count = Counter(p["_cat"] for p in posts)
    cat_html = "".join(
        f'<li><a href="/blog/#{c}">{escape(CAT_LABEL.get(c, c))}</a>'
        f'<span class="count">{n}</span></li>'
        for c, n in cat_count.most_common()
    )
    year_count = Counter(p["_year"] for p in posts if p["_year"])
    year_html = "".join(
        f'<li><a href="/blog/#y{y}">{y}</a><span class="count">{n}</span></li>'
        for y, n in sorted(year_count.items(), reverse=True)
    )
    return f"""<aside class="sidebar">

<div class="widget">
  <h3>搜索</h3>
  <div class="search-box">
    <input type="search" id="search-input" placeholder="搜索文章关键词…" autocomplete="off">
    <ul class="search-results" id="search-results"></ul>
  </div>
</div>

<div class="widget">
  <div class="about-box">
    <img src="/images/avatar.jpg?v=2" alt="李佳芮" class="about-avatar">
    <p><strong>李佳芮</strong>，<a href="https://juzibot.com">句子互动</a> 创始人。</p>
    <p>创业、产品、读书，断断续续写了十年。</p>
  </div>
</div>

<div class="widget">
  <h3>微信</h3>
  <div class="wechat-box">
    <img src="/images/wechat-qr.jpg" alt="微信公众号" class="wechat-qr">
    <p class="wechat-cap">扫码关注公众号</p>
    <p class="wechat-id">个人微信 · <code>jiaruijuzi</code></p>
  </div>
</div>

<div class="widget">
  <h3>近期文章</h3>
  <ul>{recent_html}</ul>
</div>

<div class="widget">
  <h3>分类</h3>
  <ul>{cat_html}</ul>
</div>

<div class="widget">
  <h3>归档</h3>
  <ul>{year_html}</ul>
</div>

</aside>"""


def extract_post(html):
    """Parse the body, title, date, tags from either legacy or new HTML."""
    body = ""
    # try patterns: legacy (post-tool follows), new (post-tags or post-wechat follow), fallback (article close)
    for pat in (
        r'<div class="post-content markdown-body">(.*?)</div>\s*<div class="post-tool">',
        r'<div class="post-content markdown-body">(.*?)</div>\s*<div class="post-tags">',
        r'<div class="post-content markdown-body">(.*?)</div>\s*<aside class="post-wechat">',
        r'<div class="post-content markdown-body">(.*?)</div>\s*</article>',
    ):
        m = re.search(pat, html, re.S)
        if m:
            body = m.group(1).strip()
            break

    # Title: legacy h2, or new h1 — unescape entities so we don't double-escape later
    title_m = re.search(r'<h2 class="post-title">(.*?)</h2>', html, re.S)
    if not title_m:
        title_m = re.search(r'<h1 class="post-title-h1">(.*?)</h1>', html, re.S)
    title = unescape(title_m.group(1).strip()) if title_m else ""

    # Date: legacy span, or new <time>
    date_m = re.search(r'<span title="最后编辑于[^"]*">([^<]+)</span>', html)
    if not date_m:
        date_m = re.search(r'<div class="post-byline">\s*<time>([^<]+)</time>', html)
    date = unescape(date_m.group(1).strip()) if date_m else ""

    # Tags: legacy /tags/ links, or new .post-tag spans
    tags = re.findall(r'<a href="/tags/[^"]*/?">([^<]+)</a>', html)
    if not tags:
        tags = [t.lstrip("#") for t in re.findall(r'<span class="post-tag">([^<]+)</span>', html)]
    tags = [unescape(t) for t in tags]

    # Word count: legacy "本文共计N个字", or new "全文 N 字"
    word_m = re.search(r'本文共计(\d+)个字', html)
    if not word_m:
        word_m = re.search(r'全文\s*(\d+)\s*字', html)
    word_count = word_m.group(1) if word_m else None

    return {
        "title": title,
        "date": date,
        "tags": tags,
        "word_count": word_count,
        "body": body,
    }


def neighbors(posts, current_path):
    paths = [p["path"] for p in posts]
    try:
        i = paths.index(current_path)
    except ValueError:
        return None, None
    # posts sorted desc by date — index 0 is newest
    newer = posts[i - 1] if i > 0 else None
    older = posts[i + 1] if i < len(posts) - 1 else None
    return newer, older


def build_post_page(post_meta, parsed, side_html, newer, older):
    title = parsed["title"] or post_meta["title"]
    date = parsed["date"] or post_meta["_date"]
    cat = post_meta["_cat_label"]
    body = parsed["body"]

    tags_html = ""
    if parsed["tags"]:
        tags_html = '<div class="post-tags">' + "".join(
            f'<span class="post-tag">#{escape(t)}</span>' for t in parsed["tags"]
        ) + '</div>'

    wechat_block = """<aside class="post-wechat">
  <img src="/images/wechat-qr.jpg" alt="李佳芮的公众号" class="post-wechat-qr">
  <div class="post-wechat-text">
    <h4>欢迎扫码关注</h4>
    <p>不定期更新 · 创业、产品、读书</p>
    <p class="post-wechat-id">个人微信 · <code>jiaruijuzi</code></p>
  </div>
</aside>"""

    comments_block = """<section class="post-comments">
  <h3>评论</h3>
  <livere-comment client-id="AwCdtY6RULKUsR5ehN3E"></livere-comment>
  <script type="module" src="https://www.livere.org/livere-widget.js"></script>
  <noscript>请启用 JavaScript 查看评论</noscript>
</section>"""

    word_html = ""
    if parsed["word_count"]:
        word_html = f' · 全文 {parsed["word_count"]} 字'

    nav_html = ""
    if newer or older:
        n_html = (
            f'<a class="prev" href="/{escape(newer["path"])}">← {escape(newer["title"])}</a>'
            if newer else '<span class="prev"></span>'
        )
        o_html = (
            f'<a class="next" href="/{escape(older["path"])}">{escape(older["title"])} →</a>'
            if older else '<span class="next"></span>'
        )
        nav_html = f'<nav class="post-nav">{n_html}{o_html}</nav>'

    body_html = f"""{topnav()}

<div class="wrap">
<div class="cols">
<main class="post-main">
<article class="post-article">
  <header class="post-head">
    <div class="post-cat-line">
      <a href="/blog/#{post_meta['_cat']}" class="post-cat">{escape(cat)}</a>
    </div>
    <h1 class="post-title-h1">{escape(title)}</h1>
    <div class="post-byline">
      <time>{escape(date)}</time>{word_html}
    </div>
  </header>
  <div class="post-content markdown-body">
{body}
  </div>
  {tags_html}
  {wechat_block}
</article>
{comments_block}
{nav_html}
</main>
{side_html}
</div>
</div>

{FOOT}"""

    # SEO description: prefer explicit description from content.json (set via posts/*.md frontmatter)
    desc = post_meta.get("description") or ""
    if not desc:
        desc = re.sub(r"<[^>]+>", "", body)[:150].replace("\n", " ").strip()
        desc = unescape(desc)
    head = HEAD.format(title=escape(title), desc=escape(desc))
    return head + body_html


def build_page(parsed, side_html, page_meta):
    """Build a static page (about, links, etc) — no comment form, no wechat block."""
    title = parsed["title"] or page_meta.get("title", "")
    body = parsed["body"]

    body_html = f"""{topnav()}

<div class="wrap">
<div class="cols">
<main class="post-main">
<article class="post-article">
  <header class="post-head">
    <h1 class="post-title-h1">{escape(title)}</h1>
  </header>
  <div class="post-content markdown-body">
{body}
  </div>
</article>
</main>
{side_html}
</div>
</div>

{FOOT}"""

    desc = re.sub(r"<[^>]+>", "", body)[:120].replace("\n", " ").strip()
    desc = unescape(desc)
    head = HEAD.format(title=escape(title), desc=escape(desc))
    return head + body_html


def main():
    posts = load_posts()
    blog_posts = [p for p in posts if p["_cat"] != "presentation"]
    slide_posts = [p for p in posts if p["_cat"] == "presentation"]

    side_html = sidebar(blog_posts, slide_posts)

    rewritten = 0
    skipped = 0
    failed = []

    for p in posts:
        fp = ROOT / p["path"]
        if not fp.exists():
            skipped += 1
            continue
        original = fp.read_text(errors="ignore")
        if 'class="post-content markdown-body"' not in original:
            skipped += 1
            continue
        parsed = extract_post(original)
        if not parsed["body"]:
            failed.append(p["path"])
            continue
        newer, older = neighbors(posts, p["path"])
        new_html = build_post_page(p, parsed, side_html, newer, older)
        fp.write_text(new_html, encoding="utf-8")
        rewritten += 1

    # ---- Standalone pages (about, links, help) ----
    data = json.loads((ROOT / "content.json").read_text())
    for page in data.get("pages", []):
        path = page.get("path", "")
        if path not in ("about/index.html",):  # only about for now
            continue
        fp = ROOT / path
        if not fp.exists():
            continue
        original = fp.read_text(errors="ignore")
        if 'class="post-content markdown-body"' not in original:
            continue
        parsed = extract_post(original)
        if not parsed["body"]:
            failed.append(path)
            continue
        new_html = build_page(parsed, side_html, page)
        fp.write_text(new_html, encoding="utf-8")
        print(f"rewrote page {path}")

    print(f"rewrote {rewritten} posts, skipped {skipped}")
    if failed:
        print(f"failed ({len(failed)}):")
        for f in failed[:10]:
            print(f"  {f}")


if __name__ == "__main__":
    main()
