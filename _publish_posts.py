#!/usr/bin/env python3
"""Scan posts/*.md and publish them as blog posts.

Each .md file should have YAML frontmatter:
  ---
  title: 标题
  date: 2026-04-27
  category: thought
  tags: 创业, AI
  ---

  正文 markdown 内容...

The script:
1. Generates a Hexo-format HTML stub at <category>/<slug>.html
2. Registers / updates the entry in content.json (dedup by path)

Then run `_rewrite_posts.py` to convert to new layout, then `_build_pages.py`
to rebuild listings. Or just run `build.py` to chain all three.
"""
import json
import re
from html import escape
from pathlib import Path

import markdown as md_lib

ROOT = Path(__file__).parent
POSTS_DIR = ROOT / "posts"

VALID_CATEGORIES = {"thought", "reading", "chatbot", "project", "saas",
                    "interview", "microsoft", "presentation"}

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


def parse_frontmatter(text):
    if not text.lstrip().startswith("---"):
        return {}, text.strip()
    rest = text.lstrip()[3:]
    if "---" not in rest:
        return {}, text.strip()
    fm, body = rest.split("---", 1)
    meta = {}
    for line in fm.split("\n"):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if ":" in line:
            k, v = line.split(":", 1)
            meta[k.strip().lower()] = v.strip().strip('"').strip("'")
    return meta, body.strip()


def md_to_plain_text(md_body):
    text = re.sub(r"```.*?```", "", md_body, flags=re.S)
    text = re.sub(r"`[^`]+`", "", text)
    text = re.sub(r"!\[[^\]]*\]\([^)]+\)", "", text)
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    text = re.sub(r"[#>*_\-]", "", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def slugify_title(s):
    s = re.sub(r"[^\w一-鿿-]+", "-", s)
    return re.sub(r"-+", "-", s).strip("-").lower() or "post"


def main():
    if not POSTS_DIR.exists():
        print(f"posts/ directory not found at {POSTS_DIR}")
        return

    cj_path = ROOT / "content.json"
    data = json.loads(cj_path.read_text())
    existing_paths = {p["path"]: i for i, p in enumerate(data["posts"])}

    converter = md_lib.Markdown(extensions=["extra", "sane_lists"])

    published = 0
    skipped = 0
    md_files = sorted(POSTS_DIR.glob("*.md"))

    for fp in md_files:
        if fp.name == "TEMPLATE.md" or fp.name.startswith("_"):
            skipped += 1
            continue
        text = fp.read_text(encoding="utf-8")
        meta, body_md = parse_frontmatter(text)

        # Required fields
        title = meta.get("title")
        date = meta.get("date")
        category = meta.get("category", "thought").lower()

        if not title:
            print(f"  ✗ {fp.name}: missing title in frontmatter, skipped")
            skipped += 1
            continue
        if category not in VALID_CATEGORIES:
            print(f"  ✗ {fp.name}: invalid category '{category}' "
                  f"(must be one of {sorted(VALID_CATEGORIES)}), skipped")
            skipped += 1
            continue

        # Date: from frontmatter or filename prefix YYYY-MM-DD
        if not date:
            m = re.match(r"^(\d{4}-\d{2}-\d{2})", fp.stem)
            if m:
                date = m.group(1)
            else:
                print(f"  ✗ {fp.name}: missing date in frontmatter and filename, skipped")
                skipped += 1
                continue

        date_short = date[:10]
        date_iso = f"{date_short}T10:00:00.000Z"

        # Slug: explicit frontmatter slug = canonical filename stem.
        # If no slug, derive from filename (with date prefix logic for new posts).
        explicit_slug = meta.get("slug")
        if explicit_slug:
            # Treat as canonical full stem — no date prefix munging
            slug = explicit_slug
            path = f"{category}/{slug}.html"
        else:
            # Filename-based: if filename already has date prefix (any digit count for m/d), use as-is
            stem = fp.stem
            if re.match(r"^\d{4}-\d{1,2}-\d{1,2}([-_].+)?$", stem):
                slug = stem
                path = f"{category}/{stem}.html"
            else:
                slug = slugify_title(stem)
                path = f"{category}/{date_short}-{slug}.html"

        # Tags
        tags = []
        if meta.get("tags"):
            tags = [t.strip() for t in re.split(r"[,，]", meta["tags"]) if t.strip()]

        body_html = converter.convert(body_md)
        converter.reset()
        plain = md_to_plain_text(body_md)

        # Description (SEO): from frontmatter, or auto-generate from body
        description = meta.get("description") or ""
        if not description:
            description = plain[:150].replace("\n", " ").strip()
            if len(plain) > 150:
                description = description.rstrip() + "…"

        tags_html = "\n".join(
            f'    <a href="/tags/{escape(t)}/">{escape(t)}</a>' for t in tags
        )

        html = HEXO_TEMPLATE.format(
            title=escape(title),
            date_short=escape(date_short),
            word_count=len(plain),
            body_html=body_html,
            tags_html=tags_html,
        )

        out_path = ROOT / path
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(html, encoding="utf-8")

        # content.json entry
        post_entry = {
            "title": title,
            "slug": slug,
            "date": date_iso,
            "updated": date_iso,
            "comments": True,
            "path": path,
            "link": "",
            "permalink": f"https://rui.juzi.bot/{path}",
            "excerpt": "",
            "description": description,
            "text": plain,
            "categories": [{
                "name": category,
                "slug": category,
                "permalink": f"https://rui.juzi.bot/categories/{category}/",
            }],
            "tags": [{
                "name": t,
                "slug": t,
                "permalink": f"https://rui.juzi.bot/tags/{t}/",
            } for t in tags],
            "keywords": [{
                "name": category,
                "slug": category,
                "permalink": f"https://rui.juzi.bot/categories/{category}/",
            }],
        }

        if path in existing_paths:
            data["posts"][existing_paths[path]] = post_entry
        else:
            data["posts"].insert(0, post_entry)
            existing_paths[path] = 0
        published += 1

    cj_path.write_text(json.dumps(data, ensure_ascii=False, separators=(",", ":")))
    print(f"\nprocessed {published} posts ({skipped} skipped)")
    if published:
        print("now run: python3 _rewrite_posts.py && python3 _build_pages.py")
        print("(or just: python3 build.py)")


if __name__ == "__main__":
    main()
