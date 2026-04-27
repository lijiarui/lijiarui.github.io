#!/usr/bin/env python3
"""自动化测试整站。

跑：python3 _test_site.py
检查：
- HTML 文件完整性（CSS link、topnav、sidebar、footer、双重转义、未渲染模板等）
- content.json 一致性（每篇 post 都有对应文件、search-index 同步）
- 所有 <img> 引用的本地路径都真实存在
- 所有 <a href="/..."> 内链都真实存在（除 fragment-only）
- LiveRe UID、必备 widget 全埋
- RSS feed.xml 格式正确，items > 0
- 关键页面布局完整（sidebar widget 全到、年度思考有内容、homepage feed 有 N 条）
- description meta 不为空
- 没有遗留占位符（YOUR_*）

退出码 0 = 全过；非 0 = 有失败。
"""
import json
import re
import sys
import xml.etree.ElementTree as ET
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).parent

issues = []
def fail(category, detail):
    issues.append((category, detail))


def all_html_files():
    """All HTML files in the site (excluding tags/ which are case-collision artifacts)."""
    out = []
    for pat in ["*.html", "blog/*.html", "slides/*.html", "slides/files/*/*.html",
                "claude/*.html", "yearly/*.html", "about/*.html",
                "thought/*.html", "chatbot/*.html", "presentation/*.html",
                "interview/*.html", "project/*.html", "reading/*.html",
                "saas/*.html", "microsoft/*.html"]:
        out.extend(ROOT.glob(pat))
    return out


def test_html_basics():
    """Per-page basic checks."""
    EXEMPT_NO_CSS = {"warn.html", "index-old.html"}
    for fp in all_html_files():
        rel = str(fp.relative_to(ROOT))
        html = fp.read_text(errors="ignore")

        if re.search(r"&amp;amp;", html):
            fail("DOUBLE-ESCAPE", f"{rel}: found &amp;amp;")
        if "post-content markdown-body" in html and "topnav" not in html:
            fail("NO-TOPNAV", rel)
        if "<body" in html and "/css/site.css" not in html and rel not in EXEMPT_NO_CSS:
            fail("NO-CSS", rel)
        if re.search(r"\{(?:title|date|cat|body)\}(?![a-z])", html):
            fail("UNRENDERED-TEMPLATE", rel)
        for ph in ["YOUR_LIVERE_UID", "YOUR_FORM_ID", "YOUR_REPO_ID"]:
            if ph in html:
                fail("PLACEHOLDER", f"{rel}: {ph}")


def test_post_pages_have_widgets():
    """Each post-detail page must have LiveRe + WeChat blocks + RSS link in head."""
    for fp in all_html_files():
        rel = str(fp.relative_to(ROOT))
        html = fp.read_text(errors="ignore")
        if "post-content markdown-body" not in html:
            continue
        # skip about + 404 + slide viewer (different layout)
        if rel.startswith("about/") or rel.startswith("404") or "slide-viewer-page" in html:
            continue
        if "lv-container" not in html and "livere-comment" not in html:
            fail("NO-LIVERE", rel)
        if "post-wechat" not in html:
            fail("NO-WECHAT-BLOCK", rel)
        if 'rel="alternate" type="application/rss+xml"' not in html:
            fail("NO-RSS-AUTODISCOVER", rel)


def test_local_images_exist():
    """All local /img or /images references in HTML must resolve to actual files.
    Whitelist: pre-existing legacy images that were never uploaded to Hexo repo."""
    KNOWN_LEGACY_MISSING = {
        "/img/2018/unit-3-1-3.jpeg",   # 2018 chatbot post, image never in repo
        "/img/2015/ainiangzi-5.jpg",   # 2015 project post, image never in repo
    }
    seen_missing = set()
    for fp in all_html_files():
        rel = str(fp.relative_to(ROOT))
        html = fp.read_text(errors="ignore")
        imgs = re.findall(r'src="(/(?:img|images|files)/[^"]+?)"', html)
        for img in imgs:
            clean = img.split("?")[0]
            if clean in KNOWN_LEGACY_MISSING:
                continue
            target = ROOT / clean.lstrip("/")
            if not target.exists() and clean not in seen_missing:
                seen_missing.add(clean)
                fail("MISSING-IMAGE", f"{rel} → {clean}")


def test_internal_links():
    """Internal /<path> links should point to existing files (or known directories).
    Skip index-old.html (legacy Hexo backup with stale Disqus/GA links)."""
    seen_missing = set()
    KNOWN_DIRS = {"/", "/blog/", "/slides/", "/claude/", "/yearly/", "/about/",
                  "/archives/", "/tags/", "/categories/"}
    SKIP_FILES = {"index-old.html"}
    KNOWN_LEGACY_BROKEN = {
        "/lijiarui-why-wuli-dream/",  # Hexo-era inline link in old post body
        "/README-en.md",              # 2018 wechaty post body link, file not in repo
    }
    for fp in all_html_files():
        rel = str(fp.relative_to(ROOT))
        if rel in SKIP_FILES:
            continue
        html = fp.read_text(errors="ignore")
        # only scan main content, skip nav/footer
        links = re.findall(r'href="(/[^"#]+?)(?:#[^"]*)?"', html)
        for link in links:
            if link in seen_missing:
                continue
            if link in KNOWN_DIRS or link in KNOWN_LEGACY_BROKEN:
                continue
            target = ROOT / link.lstrip("/")
            if link.endswith("/"):
                target = target / "index.html"
            if not target.exists():
                # try as directory
                dir_target = ROOT / link.lstrip("/") / "index.html"
                if dir_target.exists():
                    continue
                # try as raw file
                if (ROOT / link.lstrip("/")).exists():
                    continue
                # tags/categories paths: known to be Hexo-era, allow
                if link.startswith("/tags/") or link.startswith("/categories/") \
                        or link.startswith("/archives/"):
                    continue
                seen_missing.add(link)
                fail("BROKEN-INTERNAL-LINK", f"{rel} → {link}")


def test_content_json_consistency():
    """content.json paths should exist; each post should be in search index too."""
    cj = json.loads((ROOT / "content.json").read_text())
    sidx = json.loads((ROOT / "search-index.json").read_text())
    cj_paths = {p["path"] for p in cj["posts"]}
    sidx_paths = {e["p"].lstrip("/") for e in sidx}

    for p in cj["posts"]:
        if not (ROOT / p["path"]).exists():
            fail("CJ-MISSING-FILE", p["path"])
        if not p.get("description"):
            fail("CJ-NO-DESCRIPTION", p["path"])
        if not p.get("title"):
            fail("CJ-NO-TITLE", p["path"])
        if not p.get("date"):
            fail("CJ-NO-DATE", p["path"])

    if cj_paths != sidx_paths:
        only_cj = cj_paths - sidx_paths
        only_si = sidx_paths - cj_paths
        if only_cj:
            fail("SIDX-MISSING", f"in content.json but not search-index: {sorted(only_cj)[:3]}")
        if only_si:
            fail("CJ-MISSING", f"in search-index but not content.json: {sorted(only_si)[:3]}")


def test_rss_feed():
    """feed.xml exists, valid XML, has items."""
    feed = ROOT / "feed.xml"
    if not feed.exists():
        fail("NO-RSS", "feed.xml not generated")
        return
    try:
        tree = ET.parse(str(feed))
    except ET.ParseError as e:
        fail("RSS-INVALID-XML", str(e))
        return
    items = tree.findall(".//item")
    if not items:
        fail("RSS-NO-ITEMS", "feed has 0 items")
    elif len(items) < 5:
        fail("RSS-FEW-ITEMS", f"only {len(items)} items in feed")
    # Each item must have title, link, pubDate
    for i, item in enumerate(items[:5]):
        for tag in ("title", "link", "pubDate"):
            if item.find(tag) is None:
                fail("RSS-ITEM-MISSING-FIELD", f"item {i} missing <{tag}>")


def test_homepage_feed():
    """Homepage feed must contain top recent items including the latest PPT."""
    home = (ROOT / "index.html").read_text()
    feed_links = re.findall(r'class="entry-title"><a href="(/[^"]+)"', home)
    if len(feed_links) < 5:
        fail("HOMEPAGE-FEW-ENTRIES", f"only {len(feed_links)} feed items")
    # Top 8 should include the PKU slide (most recent activity)
    top_html = home.split("查看全部")[0] if "查看全部" in home else home
    if "重新发明组织" not in top_html and "ai-organization-pku" not in home:
        fail("HOMEPAGE-MISSING-PKU", "PKU slides not in homepage")


def test_yearly_page():
    """/yearly/ should have at least 10 entries."""
    p = ROOT / "yearly/index.html"
    if not p.exists():
        fail("NO-YEARLY", "yearly/index.html missing")
        return
    html = p.read_text()
    entries = len(re.findall(r"<li><time>", html))
    if entries < 10:
        fail("YEARLY-FEW-ENTRIES", f"only {entries} yearly entries (expected 10+)")


def test_sidebar_widgets():
    """Listing pages should have all sidebar widgets."""
    pages = ["index.html", "blog/index.html", "slides/index.html",
             "claude/index.html", "yearly/index.html"]
    expected = ["搜索", "近期文章", "微信", "分类", "归档", "订阅"]
    for p in pages:
        fp = ROOT / p
        if not fp.exists():
            fail("PAGE-MISSING", p)
            continue
        html = fp.read_text()
        for w in expected:
            if w not in html:
                fail("SIDEBAR-WIDGET-MISSING", f"{p} missing widget '{w}'")


def test_seo_meta():
    """Every public page should have og:title, og:description, canonical."""
    REQUIRED = [
        ('property="og:title"', "OG-TITLE"),
        ('property="og:description"', "OG-DESC"),
        ('property="og:type"', "OG-TYPE"),
        ('property="og:url"', "OG-URL"),
        ('property="og:image"', "OG-IMAGE"),
        ('rel="canonical"', "CANONICAL"),
        ('name="twitter:card"', "TWITTER-CARD"),
    ]
    EXEMPT = {"warn.html", "index-old.html"}
    for fp in all_html_files():
        rel = str(fp.relative_to(ROOT))
        if rel in EXEMPT:
            continue
        html = fp.read_text(errors="ignore")
        for needle, code in REQUIRED:
            if needle not in html:
                fail(f"SEO-{code}", rel)


def test_jsonld_structured_data():
    """Article pages should have JSON-LD BlogPosting structured data."""
    for fp in all_html_files():
        rel = str(fp.relative_to(ROOT))
        html = fp.read_text(errors="ignore")
        if "post-content markdown-body" not in html:
            continue
        if rel.startswith("about/") or "slide-viewer-page" in html:
            continue
        if 'application/ld+json' not in html:
            fail("JSONLD-MISSING", rel)
        elif '"BlogPosting"' not in html:
            fail("JSONLD-WRONG-TYPE", rel)


def test_sitemap():
    """sitemap.xml should exist with reasonable URL count."""
    sm = ROOT / "sitemap.xml"
    if not sm.exists():
        fail("NO-SITEMAP", "sitemap.xml not generated")
        return
    try:
        tree = ET.parse(str(sm))
    except ET.ParseError as e:
        fail("SITEMAP-INVALID-XML", str(e))
        return
    # XML namespace handling
    ns = "{http://www.sitemaps.org/schemas/sitemap/0.9}"
    urls = tree.findall(f"{ns}url")
    if len(urls) < 50:
        fail("SITEMAP-FEW-URLS", f"only {len(urls)} URLs (expected 100+)")


def test_robots_txt():
    """robots.txt should exist and reference sitemap."""
    r = ROOT / "robots.txt"
    if not r.exists():
        fail("NO-ROBOTS", "robots.txt not generated")
        return
    txt = r.read_text()
    if "Sitemap:" not in txt:
        fail("ROBOTS-NO-SITEMAP", "robots.txt missing Sitemap: directive")
    if "User-agent:" not in txt:
        fail("ROBOTS-NO-UA", "robots.txt missing User-agent: directive")


def test_specific_artifacts():
    """Spot-check specific things that should be present."""
    home = (ROOT / "index.html").read_text()
    if "AwCdtY6RULKUsR5ehN3E" not in (ROOT / "thought/2026-01-31-juzibot-2026.html").read_text():
        fail("LIVERE-UID-MISSING", "thought/2026-01-31-juzibot-2026.html has no LiveRe UID")
    if "/feed.xml" not in home:
        fail("HOMEPAGE-NO-RSS-LINK", "homepage doesn't link to /feed.xml")
    # PKU slide page has the contact card
    pku = ROOT / "slides/files/2026-04-25-ai-organization-pku/index.html"
    if pku.exists():
        html = pku.read_text()
        if "contact-card" not in html:
            fail("PKU-NO-CONTACT-CARD", "PKU slide page missing contact card")
        if "jiaruijuzi" not in html:
            fail("PKU-NO-WECHAT-ID", "PKU slide page missing personal WeChat")


def main():
    print("Running automated site QA...\n")

    tests = [
        ("HTML basics", test_html_basics),
        ("Post pages widgets", test_post_pages_have_widgets),
        ("Local images exist", test_local_images_exist),
        ("Internal links", test_internal_links),
        ("content.json consistency", test_content_json_consistency),
        ("RSS feed", test_rss_feed),
        ("Sitemap", test_sitemap),
        ("robots.txt", test_robots_txt),
        ("SEO meta tags", test_seo_meta),
        ("JSON-LD structured data", test_jsonld_structured_data),
        ("Homepage feed", test_homepage_feed),
        ("Yearly page", test_yearly_page),
        ("Sidebar widgets", test_sidebar_widgets),
        ("Specific artifacts", test_specific_artifacts),
    ]

    for name, fn in tests:
        before = len(issues)
        fn()
        added = len(issues) - before
        marker = "✓" if added == 0 else "✗"
        print(f"  {marker} {name}: {len(issues) - before} issues")

    print()
    if issues:
        cat_counts = Counter(c for c, _ in issues)
        print(f"Found {len(issues)} issues across {len(cat_counts)} categories:")
        for cat in cat_counts:
            cat_issues = [d for c, d in issues if c == cat]
            print(f"\n  [{cat}] {len(cat_issues)}:")
            for d in cat_issues[:5]:
                print(f"    {d}")
            if len(cat_issues) > 5:
                print(f"    ... +{len(cat_issues) - 5} more")
        sys.exit(1)
    else:
        print("✅ All tests passed.")


if __name__ == "__main__":
    main()
