#!/usr/bin/env python3
"""把所有现有 HTML 文章反向还原成 Markdown，写入 posts/。

用 content.json 的元数据 + 已渲染的 HTML 文件作为输入：
1. 从 HTML 抽 body
2. body HTML → Markdown（markdownify）
3. 拼 frontmatter（title, date, category, tags, description）
4. 写到 posts/<basename>.md

跑一次完成迁移。之后所有写作改 posts/*.md 即可。
"""
import json
import re
import sys
from html import unescape as _unescape
from pathlib import Path

from markdownify import markdownify as md_convert

ROOT = Path(__file__).parent
POSTS_DIR = ROOT / "posts"


def deep_unescape(s):
    if s is None:
        return s
    prev = None
    while prev != s:
        prev = s
        s = _unescape(s)
    return s


def extract_body(html):
    """Extract the markdown-body div content from a post HTML."""
    for pat in (
        r'<div class="post-content markdown-body">(.*?)</div>\s*<div class="post-tool">',
        r'<div class="post-content markdown-body">(.*?)</div>\s*<div class="post-tags">',
        r'<div class="post-content markdown-body">(.*?)</div>\s*<aside class="post-wechat">',
        r'<div class="post-content markdown-body">(.*?)</div>\s*</article>',
    ):
        m = re.search(pat, html, re.S)
        if m:
            return m.group(1).strip()
    return ""


def html_to_md(body_html):
    """Convert HTML body to Markdown."""
    md = md_convert(
        body_html,
        heading_style="ATX",
        bullets="-",
        strip=["script", "style"],
        code_language="",
        escape_asterisks=False,
        escape_underscores=False,
    )
    # Clean up extra whitespace
    md = re.sub(r"\n{3,}", "\n\n", md)
    md = re.sub(r"^[ \t]+\n", "\n", md, flags=re.M)
    return md.strip()


def make_description(body_html, max_len=150):
    """Generate SEO-friendly description from body."""
    text = re.sub(r"<[^>]+>", " ", body_html)
    text = deep_unescape(text)
    text = re.sub(r"\s+", " ", text).strip()
    if len(text) <= max_len:
        return text
    cut = text[:max_len]
    for sep in ["。", "！", "？", "；", "，"]:
        idx = cut.rfind(sep)
        if idx > max_len * 0.6:
            return cut[: idx + 1]
    return cut + "…"


def main():
    POSTS_DIR.mkdir(parents=True, exist_ok=True)

    data = json.loads((ROOT / "content.json").read_text())
    posts = data["posts"]
    print(f"Processing {len(posts)} posts from content.json")

    written = 0
    skipped = 0
    failed = []

    for p in posts:
        path = p["path"]
        fp = ROOT / path
        if not fp.exists():
            failed.append(f"{path} (file not found)")
            continue

        html = fp.read_text(errors="ignore")
        body = extract_body(html)
        if not body:
            failed.append(f"{path} (no body extractable)")
            continue

        # filename: basename of path, .html → .md
        slug = Path(path).stem
        category = p["categories"][0]["name"] if p.get("categories") else "thought"
        title = p["title"]
        date = p.get("date", "")[:10]
        tags = [t["name"] for t in p.get("tags", [])]

        # Auto-add 年度思考 tag if title matches pattern
        yearly_pat = re.compile(
            r"(写在\s*\d{4}\s*年的最后一天|写在\s*\d{4}\s*年的第一天|"
            r"\d{4}\s*年.*?(?:思想切片|思考切片)|"
            r"写在句子互动的\s*\d{4}\s*年)"
        )
        if yearly_pat.search(title) and "年度思考" not in tags:
            tags.insert(0, "年度思考")

        # Description: first 150 chars of body plain text
        description = make_description(body)

        # Convert body HTML to markdown
        try:
            body_md = html_to_md(body)
        except Exception as e:
            failed.append(f"{path} ({e})")
            continue

        # Compose frontmatter (escape colons / quotes minimally)
        def fm_value(v):
            v = str(v).replace('"', "'").replace("\n", " ")
            return v

        tags_str = ", ".join(tags)
        frontmatter = (
            "---\n"
            f"title: {fm_value(title)}\n"
            f"date: {date}\n"
            f"category: {category}\n"
            f"tags: {tags_str}\n"
            f"slug: {slug}\n"
            f"description: {fm_value(description)}\n"
            "---\n\n"
        )

        out_path = POSTS_DIR / f"{slug}.md"
        out_path.write_text(frontmatter + body_md + "\n", encoding="utf-8")
        written += 1

    print(f"\n✓ wrote {written} markdown files to posts/")
    if failed:
        print(f"\n✗ {len(failed)} failures:")
        for f in failed[:10]:
            print(f"  {f}")


if __name__ == "__main__":
    main()
