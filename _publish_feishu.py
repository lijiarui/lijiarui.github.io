#!/usr/bin/env python3
"""Pull articles from Feishu wiki/docx, download embedded images, write to posts/.

For each URL in ARTICLES:
1. Fetch markdown via lark-cli docs +fetch
2. Find <image token="..."/> references
3. Download each image to img/posts/<slug>/<token>.<ext>
4. Replace <image token="..."/> with ![alt](url)
5. Write posts/<slug>.md with frontmatter (the canonical source — no Hexo stub)

Run after this:
  python3 build.py    # picks up the new posts/*.md and publishes
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
    # (url, slug, date, category, [tags])
    # 历史已发布的（再跑会更新）
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
    # 2021 感恩节
    ("https://juzihudong.feishu.cn/wiki/D8FUwy0R9i4Kw1kFcFkcfEI9njd",
     "2021-11-25-juzibot-thanksgiving-2021", "2021-11-25", "thought",
     ["句子互动", "团队", "感恩节"]),
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


def make_description_from_md(text, n=150):
    plain = re.sub(r"!\[[^\]]*\]\([^)]+\)", "", text)
    plain = re.sub(r"```.*?```", "", plain, flags=re.S)
    plain = re.sub(r"`[^`]+`", "", plain)
    plain = re.sub(r"<[^>]+>", "", plain)
    plain = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", plain)
    plain = re.sub(r"[#>*_\-]", "", plain)
    plain = re.sub(r"\s+", " ", plain).strip()
    if len(plain) <= n:
        return plain
    cut = plain[:n]
    for sep in ["。", "！", "？", "；", "，"]:
        idx = cut.rfind(sep)
        if idx > n * 0.6:
            return cut[: idx + 1]
    return cut + "…"


def main():
    posts_dir = ROOT / "posts"
    posts_dir.mkdir(parents=True, exist_ok=True)

    published = 0
    for url, slug, date_short, category, tags in ARTICLES:
        print(f"\n=== {slug} ===")
        try:
            raw = fetch_markdown(url)
        except subprocess.SubprocessError as e:
            print(f"  ✗ fetch failed: {e}")
            continue

        # Extract title from first # line
        title_m = re.search(r"^#\s+(.+)", raw, re.M)
        title = title_m.group(1).strip() if title_m else slug

        # Download images and replace tokens with markdown image refs
        md_with_imgs, n_imgs = process_images(raw, slug)
        if n_imgs:
            print(f"  + downloaded {n_imgs} images → img/posts/{slug}/")

        body_md = clean_md(md_with_imgs)
        description = make_description_from_md(body_md)

        # Write to posts/<slug>.md (canonical source)
        tags_str = ", ".join(tags)
        frontmatter = (
            "---\n"
            f"title: {title}\n"
            f"date: {date_short}\n"
            f"category: {category}\n"
            f"tags: {tags_str}\n"
            f"slug: {slug}\n"
            f"description: {description}\n"
            "---\n\n"
        )
        out_md = posts_dir / f"{slug}.md"
        out_md.write_text(frontmatter + body_md + "\n", encoding="utf-8")
        print(f"  wrote posts/{slug}.md ({len(body_md):,} chars)")
        published += 1

    print(f"\n✓ published {published} articles to posts/")
    print("  next: python3 build.py")


if __name__ == "__main__":
    main()
