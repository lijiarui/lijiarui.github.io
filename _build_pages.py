#!/usr/bin/env python3
"""Generate index.html, blog/index.html, slides/index.html, claude/index.html
and search-index.json from content.json."""
import datetime
import json
import re
import subprocess
from collections import Counter
from html import escape
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

EXCERPT_LEN = 160

HEAD = """<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
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
<a href="/about/">关于</a>
<div class="copyright">© Li Jiarui · 时间看得见</div>
</div></footer>
<script src="/js/search.js" defer></script>
</body></html>
"""


def topnav(active):
    items = [
        ("home", "/", "首页"),
        ("blog", "/blog/", "博客"),
        ("claude", "/claude/", "Claude 永动机"),
        ("slides", "/slides/", "分享 PPT"),
        ("about", "/about/", "关于"),
    ]
    links = "".join(
        f'<a href="{href}" class="{ "active" if key==active else "" }">{label}</a>'
        for key, href, label in items
    )
    links += '<a href="https://github.com/lijiarui" target="_blank" rel="noopener" class="nav-ext" title="GitHub">GitHub ↗</a>'
    return f"""<header class="topnav"><div class="wrap row">
<div class="brand"><a href="/">李佳芮</a><span class="tagline">时间看得见</span></div>
<nav>{links}</nav>
</div></header>
"""


def make_excerpt(text, n=EXCERPT_LEN):
    text = re.sub(r"\s+", " ", text or "").strip()
    if len(text) <= n:
        return text
    cut = text[:n]
    for sep in ["。", "！", "？", "；", "，"]:
        idx = cut.rfind(sep)
        if idx > n * 0.6:
            return cut[: idx + 1]
    return cut + "…"


def extract_cover(post_path):
    """Pull the first /img/... image from the rendered post HTML."""
    fp = ROOT / post_path
    if not fp.exists():
        return None
    try:
        html = fp.read_text(errors="ignore")
    except Exception:
        return None
    m = re.search(r'src="(/img/[^"]+)"', html)
    if not m:
        return None
    img = m.group(1)
    if not (ROOT / img.lstrip("/")).exists():
        return None
    return img


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
        p["_month"] = d[:7]
        p["_excerpt"] = make_excerpt(p.get("text", ""))
        p["_tags"] = [t["name"] for t in p.get("tags", [])]
        p["_cover"] = extract_cover(p["path"]) if cat == "presentation" else None
        p["_uploaded"] = False
    posts.sort(key=lambda p: p.get("date", ""), reverse=True)
    return posts


SLIDE_DATE_RE = re.compile(r"^(\d{4}-\d{2}-\d{2})[-_ ](.+)$")


def slugify(s):
    s = re.sub(r"[^\w一-鿿-]+", "-", s)
    return re.sub(r"-+", "-", s).strip("-").lower()


def parse_md_sidecar(path):
    """Parse .md with YAML-ish frontmatter. Returns (meta_dict, body_text)."""
    if not path.exists():
        return {}, ""
    text = path.read_text(encoding="utf-8")
    if not text.lstrip().startswith("---"):
        return {}, text.strip()
    rest = text.lstrip()[3:]
    if "---" not in rest:
        return {}, text.strip()
    fm_text, body = rest.split("---", 1)
    meta = {}
    for line in fm_text.split("\n"):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if ":" in line:
            k, v = line.split(":", 1)
            meta[k.strip().lower()] = v.strip().strip('"').strip("'")
    return meta, body.strip()


def render_inline_md(text):
    text = escape(text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"`([^`]+)`", r"<code>\1</code>", text)
    text = re.sub(
        r"\[([^\]]+)\]\(([^)]+)\)",
        lambda m: f'<a href="{escape(m.group(2), quote=True)}">{m.group(1)}</a>',
        text,
    )
    return text


def render_md(text):
    if not text or not text.strip():
        return ""
    blocks = re.split(r"\n\s*\n", text.strip())
    html = []
    for block in blocks:
        block = block.strip()
        if not block:
            continue
        m = re.match(r"^(#{1,6})\s+(.+)", block)
        if m:
            level = min(len(m.group(1)) + 1, 6)
            html.append(f"<h{level}>{render_inline_md(m.group(2))}</h{level}>")
            continue
        if block.startswith(">"):
            inner_lines = [re.sub(r"^>\s?", "", l) for l in block.split("\n")]
            inner = "<br>".join(render_inline_md(l) for l in inner_lines)
            html.append(f"<blockquote>{inner}</blockquote>")
            continue
        if re.match(r"^[-*]\s", block):
            items = re.split(r"\n(?=[-*]\s)", block)
            lis_parts = []
            for i in items:
                if not i.strip():
                    continue
                cleaned = re.sub(r"^[-*]\s+", "", i.strip())
                lis_parts.append(f"<li>{render_inline_md(cleaned)}</li>")
            html.append(f"<ul>{''.join(lis_parts)}</ul>")
            continue
        if re.match(r"^\d+\.\s", block):
            items = re.split(r"\n(?=\d+\.\s)", block)
            lis_parts = []
            for i in items:
                if not i.strip():
                    continue
                cleaned = re.sub(r"^\d+\.\s+", "", i.strip())
                lis_parts.append(f"<li>{render_inline_md(cleaned)}</li>")
            html.append(f"<ol>{''.join(lis_parts)}</ol>")
            continue
        rendered = render_inline_md(block).replace("\n", "<br>")
        html.append(f"<p>{rendered}</p>")
    return "\n".join(html)


def generate_cover(src_path, slug):
    """Use qlmanage to extract first-page thumbnail. Returns URL path or None."""
    out_dir = ROOT / "img" / "slides"
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / f"{slug}.png"
    if target.exists() and target.stat().st_mtime > src_path.stat().st_mtime:
        return f"/img/slides/{slug}.png"
    try:
        subprocess.run(
            ["qlmanage", "-t", "-s", "1200", "-o", str(out_dir), str(src_path)],
            capture_output=True, timeout=60, check=False,
        )
    except (subprocess.SubprocessError, FileNotFoundError):
        return None
    tmp = out_dir / f"{src_path.name}.png"
    if tmp.exists():
        if target.exists():
            target.unlink()
        tmp.rename(target)
        return f"/img/slides/{slug}.png"
    return None


def scan_uploaded_slides():
    """Scan files/slides/ for .pdf/.pptx/.ppt and return slide records.

    Each slide can have an optional sidecar .md with YAML frontmatter:
      ---
      title: 自定义标题
      tags: 标签1, 标签2
      date: 2025-04-27
      ---
      Markdown 描述正文（多段、支持加粗/链接/列表）
    """
    folder = ROOT / "files" / "slides"
    if not folder.exists():
        return []
    out = []
    for fp in sorted(folder.iterdir()):
        if fp.is_dir() or fp.name.startswith(".") or fp.suffix.lower() == ".md":
            continue
        ext = fp.suffix.lower()
        if ext not in (".pdf", ".pptx", ".ppt"):
            continue
        stem = fp.stem
        slug = slugify(stem) or "slide"

        # Default title and date from filename
        m = SLIDE_DATE_RE.match(stem)
        if m:
            date = m.group(1)
            title = m.group(2).replace("-", " ").replace("_", " ").strip()
        else:
            mtime = datetime.date.fromtimestamp(fp.stat().st_mtime)
            date = mtime.isoformat()
            title = stem.replace("-", " ").replace("_", " ").strip()

        # Sidecar metadata override
        meta, body_md = parse_md_sidecar(folder / f"{stem}.md")
        if meta.get("title"):
            title = meta["title"]
        if meta.get("date"):
            date = meta["date"]
        tags = []
        if meta.get("tags"):
            tags = [t.strip() for t in re.split(r"[,，]", meta["tags"]) if t.strip()]

        cover_url = generate_cover(fp, slug)
        desc_html = render_md(body_md) if body_md else ""
        excerpt = make_excerpt(body_md, 160) if body_md else ""

        out.append({
            "title": title,
            "_cat": "presentation",
            "_cat_label": "演讲",
            "_date": date,
            "_year": date[:4],
            "_tags": tags,
            "_cover": cover_url,
            "_uploaded": True,
            "_source_file": "/files/slides/" + fp.name,
            "_format": ext.lstrip("."),
            "_slug": slug,
            "_description_md": body_md,
            "_description_html": desc_html,
            "_excerpt": excerpt,
            "path": f"slides/files/{slug}/index.html",
        })
    return out


def sidebar(posts, slide_posts):
    recent = posts[:6]
    recent_html = "".join(
        f'<li><a href="/{escape(p["path"])}">{escape(p["title"])}</a></li>'
        for p in recent
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

    slides_recent = slide_posts[:5]
    slides_html = "".join(
        f'<li><a href="/{escape(p["path"])}">{escape(p["title"])}</a></li>'
        for p in slides_recent
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
    <p>十年前我是程序员，这个博客是自己写的。后来做公司，代码不写了，更新也停了。</p>
    <p>最近又能写起来——这次没自己动手，AI 干的。</p>
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
  <h3>分享 PPT</h3>
  <ul>{slides_html}</ul>
</div>

<div class="widget">
  <h3>分类</h3>
  <ul>{cat_html}</ul>
</div>

<div class="widget">
  <h3>归档</h3>
  <ul>{year_html}</ul>
</div>

<div class="widget">
  <h3>外站</h3>
  <ul>
    <li><a href="https://github.com/lijiarui">GitHub</a></li>
    <li><a href="https://github.com/wechaty/wechaty">Wechaty</a></li>
    <li><a href="https://juzibot.com">句子互动</a></li>
  </ul>
</div>

</aside>"""


def write(path, html):
    full = ROOT / path
    full.parent.mkdir(parents=True, exist_ok=True)
    full.write_text(html, encoding="utf-8")
    print(f"wrote {path} ({len(html):,} bytes)")


def entry_html(p):
    return f"""<article class="entry">
  <h2 class="entry-title"><a href="/{escape(p['path'])}">{escape(p['title'])}</a></h2>
  <div class="entry-meta">{escape(p['_date'])}<span class="cat">{escape(p['_cat_label'])}</span></div>
  <div class="entry-excerpt"><p>{escape(p['_excerpt'])}</p></div>
  <div class="entry-more"><a href="/{escape(p['path'])}">继续读 →</a></div>
</article>"""


def build_index(posts, uploaded_slides):
    blog_posts = [p for p in posts if p["_cat"] != "presentation"]
    slide_posts_all = [p for p in posts if p["_cat"] == "presentation"] + uploaded_slides

    # Feed mixes blog + uploaded slides (NOT historical Hexo presentations — those are 2015-2021 archive)
    feed_source = blog_posts + uploaded_slides
    feed_source.sort(key=lambda p: p["_date"], reverse=True)
    feed_posts = feed_source[:8]

    feed_html = "\n".join(entry_html(p) for p in feed_posts)
    side_html = sidebar(blog_posts, slide_posts_all)

    first_year = blog_posts[-1]["_year"] if blog_posts else ""
    last_year = blog_posts[0]["_year"] if blog_posts else ""
    slide_first = slide_posts_all[-1]["_year"] if slide_posts_all else ""

    home_cards = f"""<div class="home-cards">
  <a class="home-card" href="/blog/">
    <div class="hc-num">{len(blog_posts)}</div>
    <div class="hc-meta">
      <h3>博客</h3>
      <p>创业、产品、读书 · {first_year}–{last_year}</p>
    </div>
    <span class="hc-arrow">→</span>
  </a>
  <a class="home-card" href="/claude/">
    <div class="hc-num hc-num-text">∞</div>
    <div class="hc-meta">
      <h3>Claude 永动机</h3>
      <p>用 AI 跑长任务的实践笔记 · 正在搬运</p>
    </div>
    <span class="hc-arrow">→</span>
  </a>
  <a class="home-card" href="/slides/">
    <div class="hc-num">{len(slide_posts_all)}</div>
    <div class="hc-meta">
      <h3>分享 PPT</h3>
      <p>过往演讲与分享 · {slide_first} 起</p>
    </div>
    <span class="hc-arrow">→</span>
  </a>
</div>"""

    body = f"""{topnav("home")}

<div class="wrap">
{home_cards}

<div class="cols">
<main class="feed">
<div class="feed-head"><h2>最近在写</h2><a href="/blog/" class="feed-more">全部 →</a></div>
{feed_html}
<p style="text-align:center;margin-top:32px;"><a href="/blog/" style="color:var(--accent);font-size:14px;">查看全部 {len(blog_posts)} 篇 →</a></p>
</main>
{side_html}
</div>
</div>

{FOOT}"""

    head = HEAD.format(
        title="李佳芮的博客 · 时间看得见",
        desc="句子互动创始人李佳芮的个人博客：创业、产品、读书",
    )
    write("index.html", head + body)


def build_blog(posts):
    blog_posts = [p for p in posts if p["_cat"] != "presentation"]
    slide_posts = [p for p in posts if p["_cat"] == "presentation"]

    cats = sorted({p["_cat"] for p in blog_posts},
                  key=lambda c: -sum(1 for p in blog_posts if p["_cat"] == c))
    filter_html = '<a href="#" class="active" data-cat="all">全部</a>' + "".join(
        f'<a href="#{c}" data-cat="{c}">{escape(CAT_LABEL.get(c, c))}</a>' for c in cats
    )

    items_html = "\n".join(
        f'<li data-cat="{p["_cat"]}" data-year="{p["_year"]}">'
        f'<time>{escape(p["_date"])}</time>'
        f'<a href="/{escape(p["path"])}">{escape(p["title"])}</a>'
        f'<span class="cat">{escape(p["_cat_label"])}</span>'
        '</li>'
        for p in blog_posts
    )

    side_html = sidebar(blog_posts, slide_posts)

    body = f"""{topnav("blog")}

<div class="wrap">
<div class="page-intro">
  <h1>博客</h1>
  <p>共 {len(blog_posts)} 篇，{blog_posts[-1]["_year"]} – {blog_posts[0]["_year"]}。按时间倒序。</p>
</div>

<div class="cols">
<main>
<div class="filter-bar" id="filter">{filter_html}</div>
<ul class="post-list" id="posts">
{items_html}
</ul>
</main>
{side_html}
</div>
</div>

<script>
(function() {{
  var bar = document.getElementById('filter');
  var list = document.getElementById('posts');
  function applyCat(cat) {{
    bar.querySelectorAll('a').forEach(function(x) {{ x.classList.toggle('active', x.getAttribute('data-cat') === cat); }});
    list.querySelectorAll('li').forEach(function(li) {{
      li.style.display = (cat === 'all' || li.getAttribute('data-cat') === cat) ? '' : 'none';
    }});
  }}
  bar.addEventListener('click', function(e) {{
    var a = e.target.closest('a'); if (!a) return;
    e.preventDefault();
    applyCat(a.getAttribute('data-cat'));
  }});
  if (location.hash) {{
    var h = location.hash.slice(1);
    if (h.startsWith('y')) {{
      var y = h.slice(1);
      list.querySelectorAll('li').forEach(function(li) {{
        li.style.display = li.getAttribute('data-year') === y ? '' : 'none';
      }});
    }} else {{
      applyCat(h);
    }}
  }}
}})();
</script>

{FOOT}"""

    head = HEAD.format(title="博客 · 李佳芮", desc="李佳芮博客文章列表")
    write("blog/index.html", head + body)


def build_slides(posts, uploaded):
    historical = [p for p in posts if p["_cat"] == "presentation"]
    slide_posts = sorted(historical + uploaded, key=lambda p: p["_date"], reverse=True)
    blog_posts = [p for p in posts if p["_cat"] != "presentation"]

    def card(p):
        is_upload = p.get("_uploaded")
        if p.get("_cover"):
            cover_html = (
                f'<div class="ppt-cover">'
                f'<img src="{escape(p["_cover"])}" alt="" loading="lazy">'
                f'</div>'
            )
        elif is_upload:
            fmt = p.get("_format", "pdf").upper()
            cover_html = (
                '<div class="ppt-cover ppt-cover-fallback ppt-cover-upload">'
                f'<span class="ppt-cover-fmt">{escape(fmt)}</span>'
                '</div>'
            )
        else:
            initial = escape(p["title"][0]) if p["title"] else ""
            cover_html = f'<div class="ppt-cover ppt-cover-fallback"><span>{initial}</span></div>'
        tags_html = ""
        tags = list(p.get("_tags", []))
        if is_upload:
            tags = ["可预览"] + tags
        if tags:
            tags_html = '<div class="ppt-tags">' + "".join(
                f'<span class="ppt-tag">#{escape(t)}</span>' for t in tags[:6]
            ) + "</div>"
        return (
            '<li class="ppt-card">'
            + '<a class="ppt-card-link" href="/' + escape(p["path"]) + '">'
            + cover_html
            + '<div class="ppt-body">'
            + f'<h3>{escape(p["title"])}</h3>'
            + f'<div class="ppt-meta"><time>{escape(p["_date"])}</time></div>'
            + tags_html
            + '</div>'
            + '</a>'
            + '</li>'
        )

    cards_html = "\n".join(card(p) for p in slide_posts)
    side_html = sidebar(blog_posts, slide_posts)

    upload_count = len(uploaded)
    intro_extra = f"，新上传 {upload_count} 份可在线预览" if upload_count else ""

    body = f"""{topnav("slides")}

<div class="wrap">
<div class="page-intro">
  <h1>分享 PPT</h1>
  <p>过去做过的 PPT 分享，多数和 Chatbot、Wechaty、开源、创业相关。共 {len(slide_posts)} 份{intro_extra}。</p>
</div>

<div class="cols">
<main>
<ul class="ppt-grid">
{cards_html}
</ul>
</main>
{side_html}
</div>
</div>

{FOOT}"""

    head = HEAD.format(title="分享 PPT · 李佳芮", desc="李佳芮 PPT 分享合集")
    write("slides/index.html", head + body)

    # Build viewer pages for each uploaded slide
    for u in uploaded:
        build_slide_viewer(u, blog_posts, slide_posts)


def build_slide_viewer(u, blog_posts, slide_posts):
    """Build /slides/files/<slug>/index.html with embedded PDF/PPTX preview."""
    src = u["_source_file"]
    title = u["title"]
    fmt = u["_format"]

    if fmt == "pdf":
        viewer_html = (
            f'<iframe class="slide-viewer slide-viewer-pdf" src="{escape(src)}#view=FitH&toolbar=0" '
            f'title="{escape(title)}" allowfullscreen></iframe>'
        )
    else:
        viewer_html = (
            '<div class="slide-viewer slide-viewer-ppt" id="ppt-viewer-host">'
            '<div class="slide-viewer-msg">PPT 预览需要公网 URL（Office Online viewer 限制），'
            '本地预览看不到，请推到 GitHub Pages 后访问。</div>'
            '<noscript>需要 JavaScript 才能预览 PPT。</noscript>'
            '</div>'
            '<script>'
            '(function(){'
            'var host=location.hostname;'
            'if(host&&host!=="localhost"&&host!=="127.0.0.1"){'
            'var enc=encodeURIComponent(location.origin+' + json.dumps(src) + ');'
            'var u="https://view.officeapps.live.com/op/embed.aspx?src="+enc;'
            'document.getElementById("ppt-viewer-host").innerHTML='
            '\'<iframe class="slide-viewer slide-viewer-ppt" src="\'+u+\'" allowfullscreen></iframe>\';'
            '}'
            '})();'
            '</script>'
        )

    side_html = sidebar(blog_posts, [p for p in slide_posts if p["_cat"] == "presentation"])

    desc_html = ""
    if u.get("_description_html"):
        desc_html = f'<div class="slide-description">{u["_description_html"]}</div>'

    tags_html = ""
    if u.get("_tags"):
        tags_html = '<div class="slide-tags">' + "".join(
            f'<span class="slide-tag">#{escape(t)}</span>' for t in u["_tags"]
        ) + '</div>'

    body = f"""{topnav("slides")}

<div class="wrap-wide">
<div class="slide-viewer-page">
  <div class="slide-viewer-head">
    <div>
      <a href="/slides/" class="slide-back">← 返回所有分享</a>
      <h1>{escape(title)}</h1>
      <div class="slide-meta"><time>{escape(u["_date"])}</time> · {fmt.upper()}</div>
      {tags_html}
    </div>
  </div>
  {desc_html}
  {viewer_html}
</div>
</div>

{FOOT}"""

    head = HEAD.format(title=f"{escape(title)} · 分享 PPT", desc=f"{escape(title)} – PPT 在线预览")
    write(u["path"], head + body)


def build_claude(posts):
    blog_posts = [p for p in posts if p["_cat"] != "presentation"]
    slide_posts = [p for p in posts if p["_cat"] == "presentation"]
    side_html = sidebar(blog_posts, slide_posts)

    body = f"""{topnav("claude")}

<div class="wrap">
<div class="page-intro">
  <h1>Claude 永动机</h1>
  <p>用 Claude Code 跑长任务、做小工具、自动化日常工作的实践笔记。</p>
  <p>这一栏在持续填充。</p>
</div>

<div class="cols">
<main>
  <article class="entry">
    <h2 class="entry-title">关于这个栏目</h2>
    <div class="entry-excerpt">
      <p>这是给 Claude Code 单独留的位置。我会把跑过的有意思的任务、写过的小工具、踩过的坑、用过的 Prompt 模式都放在这里——每条都是一个能复现的实验。</p>
      <p>暂时是空的，内容会陆续搬上来。</p>
    </div>
  </article>

  <article class="entry">
    <h2 class="entry-title">计划放进来的内容</h2>
    <div class="entry-excerpt">
      <p>· 长任务：让 Claude 一次跑几十分钟到几小时的工作流</p>
      <p>· 数据：从飞书拉数据、跑分析、产出文档的固定 Pipeline</p>
      <p>· 自动化：邮件、日历、PR review 的小钩子</p>
      <p>· Prompt：那些救过我命的 system prompt 与 skill</p>
      <p>· 翻车：失败的实验和原因</p>
    </div>
  </article>
</main>
{side_html}
</div>
</div>

{FOOT}"""

    head = HEAD.format(
        title="Claude 永动机 · 李佳芮",
        desc="用 Claude Code 跑长任务的实践与笔记",
    )
    write("claude/index.html", head + body)


def build_search_index(posts):
    """Lightweight client-side search: title + 280-char snippet for matching."""
    idx = []
    for p in posts:
        snippet = re.sub(r"\s+", " ", p.get("text", "") or "").strip()[:280]
        idx.append({
            "t": p["title"],
            "p": "/" + p["path"],
            "d": p["_date"],
            "c": p["_cat_label"],
            "s": snippet,
        })
    out = ROOT / "search-index.json"
    out.write_text(json.dumps(idx, ensure_ascii=False), encoding="utf-8")
    print(f"wrote search-index.json ({len(idx)} posts, {out.stat().st_size:,} bytes)")


def main():
    posts = load_posts()
    print(f"loaded {len(posts)} posts")
    uploaded = scan_uploaded_slides()
    print(f"  + {len(uploaded)} uploaded slides")
    build_index(posts, uploaded)
    build_blog(posts)
    build_slides(posts, uploaded)
    build_claude(posts)
    build_search_index(posts)


if __name__ == "__main__":
    main()
