#!/usr/bin/env python3
"""Pull articles from Feishu wiki/docx, download embedded images, and publish.

For each URL in ARTICLES:
1. Fetch markdown via lark-cli docs +fetch
2. Find <image token="..."/> references
3. Download each image to img/posts/<slug>/<token>.<ext>
4. Replace <image token="..."/> with <img src="...">
5. Generate Hexo-stub HTML at <category>/<date>-<slug>.html
6. Register / update entry in content.json (dedup by path)

Run after this:
  python3 _rewrite_posts.py && python3 _build_pages.py
or just:
  python3 build.py
"""
import json
import re
import subprocess
import sys
from html import escape
from pathlib import Path

import markdown as md_lib

ROOT = Path(__file__).parent

# Each: (url, slug, date, category, [tags...])
ARTICLES = [
    ("https://juzihudong.feishu.cn/wiki/CfI9wD3Jti4F0rk3uCGcwqK2nJb",
     "2025-12-31-last-day-of-2025", "2025-12-31", "thought", ["年度思考", "总结"]),
    ("https://juzihudong.feishu.cn/wiki/JODGwBjJSi4jEYkpjKTcBoqxnsd",
     "2025-12-31-2025-thought-slices", "2025-12-31", "thought", ["年度思考", "思考切片"]),
    ("https://juzihudong.feishu.cn/wiki/OjFwwUr6mi2moWkpkz7c7WO7nee",
     "2026-01-31-juzibot-2026", "2026-01-31", "thought", ["年度思考", "句子互动", "创业"]),
    ("https://juzihudong.feishu.cn/wiki/LDwewTWDFiPyVAkIHjGcahhUn7g",
     "2024-12-31-last-day-of-2024", "2024-12-31", "thought", ["年度思考", "总结"]),
    ("https://juzihudong.feishu.cn/wiki/HsIbw5RfPigkfsk3AJScHqRbnkf",
     "2024-12-31-2024-thought-slices", "2024-12-31", "thought", ["年度思考", "思考切片"]),
    ("https://juzihudong.feishu.cn/docx/IXVUdiYp1obWVXxKfjOcQl9Bn4e",
     "2025-01-31-juzibot-2025", "2025-01-31", "thought", ["年度思考", "句子互动", "创业"]),
    ("https://juzihudong.feishu.cn/docx/LhL7d4T05oWB6ixAQKLcAIr8nMe",
     "2024-01-31-juzibot-2024", "2024-01-31", "thought", ["年度思考", "句子互动", "创业"]),
    ("https://juzihudong.feishu.cn/wiki/ABYEwZaFdiCaeVkll4nc8BWhnLg",
     "2023-12-31-last-day-of-2023", "2023-12-31", "thought", ["年度思考", "总结"]),
    ("https://juzihudong.feishu.cn/wiki/PZJaw0cK7iuTglkyc76cnxg9nge",
     "2023-12-31-2023-thought-slices", "2023-12-31", "thought", ["年度思考", "思考切片", "创业"]),
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


def fetch_markdown(url):
    r = subprocess.run(
        ["lark-cli", "docs", "+fetch", "--doc", url, "--format", "pretty"],
        capture_output=True, text=True, timeout=60,
    )
    text = r.stdout
    # Strip the WARN line if present
    text = re.sub(r"^\[lark-cli\][^\n]*\n", "", text)
    return text


def download_image(token, target_dir):
    """Download image by token into target_dir as <token>.<ext> (auto-detected).
    Returns (path_str, ext) or (None, None) on failure."""
    target_dir.mkdir(parents=True, exist_ok=True)
    # Existing? check any file matching this token stem
    for existing in target_dir.glob(f"{token}.*"):
        return str(existing), existing.suffix
    # Run lark-cli with cwd=target_dir, relative output ./TOKEN
    r = subprocess.run(
        ["lark-cli", "docs", "+media-download",
         "--token", token, "--output", f"./{token}"],
        capture_output=True, text=True, cwd=target_dir, timeout=120,
    )
    # Output JSON has saved_path
    m = re.search(r'"saved_path"\s*:\s*"([^"]+)"', r.stdout)
    if not m:
        return None, None
    saved = Path(m.group(1))
    return str(saved), saved.suffix


def process_images(md_text, slug):
    """Replace <image token="X" .../> with <img src="/img/posts/<slug>/X.ext"> after downloading."""
    target_dir = ROOT / "img" / "posts" / slug
    tokens = re.findall(r'<image token="([^"]+)"[^/]*/>', md_text)
    if not tokens:
        return md_text, 0
    downloaded = 0
    for tok in tokens:
        path, ext = download_image(tok, target_dir)
        if path and ext:
            downloaded += 1
            web_path = f"/img/posts/{slug}/{tok}{ext}"
            # Replace ALL forms of <image token="tok" ... />
            md_text = re.sub(
                rf'<image token="{re.escape(tok)}"[^/]*/>',
                f'![]({web_path})',
                md_text,
            )
        else:
            print(f"    ✗ failed to download image token {tok}")
    return md_text, downloaded


def clean_md(text):
    """Strip first # title line; collapse extra leading whitespace."""
    lines = text.split("\n")
    out = []
    seen_title = False
    for line in lines:
        if not seen_title and re.match(r"^#\s+", line):
            seen_title = True
            continue
        out.append(line)
    return "\n".join(out).strip()


def md_to_plain_text(md_body):
    text = re.sub(r"```.*?```", "", md_body, flags=re.S)
    text = re.sub(r"`[^`]+`", "", text)
    text = re.sub(r"!\[[^\]]*\]\([^)]+\)", "", text)
    text = re.sub(r"<[^>]+>", "", text)
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    text = re.sub(r"[#>*_\-]", "", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def main():
    cj_path = ROOT / "content.json"
    data = json.loads(cj_path.read_text())
    existing_paths = {p["path"]: i for i, p in enumerate(data["posts"])}

    converter = md_lib.Markdown(extensions=["extra", "sane_lists"])

    published = 0
    for url, slug, date_short, category, tags in ARTICLES:
        print(f"\n=== {slug} ===")
        try:
            raw = fetch_markdown(url)
        except subprocess.SubprocessError as e:
            print(f"  ✗ fetch failed: {e}")
            continue

        # Extract title from first # line if present
        title_m = re.search(r"^#\s+(.+)", raw, re.M)
        title = title_m.group(1).strip() if title_m else slug

        # Download images and replace
        md_with_imgs, n_imgs = process_images(raw, slug)
        if n_imgs:
            print(f"  + downloaded {n_imgs} images")

        body_md = clean_md(md_with_imgs)
        body_html = converter.convert(body_md)
        converter.reset()
        plain = md_to_plain_text(body_md)

        path = f"{category}/{slug}.html"
        date_iso = f"{date_short}T10:00:00.000Z"

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
        print(f"  wrote {path} ({len(html):,} bytes)")

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
            print(f"  ↻ updated content.json entry")
        else:
            data["posts"].insert(0, post_entry)
            existing_paths[path] = 0
            print(f"  + new content.json entry")
        published += 1

    # Also tag historical "年度思考" posts already in content.json
    yearly_pattern = re.compile(
        r"(写在\s*\d{4}\s*年的最后一天|写在\s*\d{4}\s*年的第一天|"
        r"\d{4}\s*年.*?(?:思想切片|思考切片)|"
        r"写在句子互动的\s*\d{4}\s*年)"
    )
    tagged_count = 0
    for p in data["posts"]:
        title = p.get("title", "")
        if yearly_pattern.search(title):
            existing = {t["name"] for t in p.get("tags", [])}
            if "年度思考" not in existing:
                p.setdefault("tags", []).insert(0, {
                    "name": "年度思考",
                    "slug": "年度思考",
                    "permalink": "https://rui.juzi.bot/tags/%E5%B9%B4%E5%BA%A6%E6%80%9D%E8%80%83/",
                })
                tagged_count += 1
                print(f"  + tagged 年度思考: {title}")

    cj_path.write_text(json.dumps(data, ensure_ascii=False, separators=(",", ":")))
    print(f"\npublished {published} articles, retro-tagged {tagged_count} historical")


if __name__ == "__main__":
    main()
