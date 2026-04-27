#!/usr/bin/env python3
"""一键发布：扫 posts/ + files/slides/，重建整站。

工作流：
  1. 编辑 posts/<your-post>.md（或 files/slides/ 加 PPT/PDF）
  2. 跑：python3 build.py
  3. git commit + push（如果想推到线上）

这个脚本会顺序执行：
  - _publish_posts.py    将 posts/*.md 转成博客 + 注册到 content.json
  - _rewrite_posts.py    把所有文章详情页渲染成新主题（旧 hexo + 新 md 都会处理）
  - _build_pages.py      重建首页/博客列表/分享 PPT/Claude 永动机/搜索索引
"""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent

steps = [
    ("发布 posts/*.md 博客", "_publish_posts.py"),
    ("渲染所有文章详情页", "_rewrite_posts.py"),
    ("重建列表页 + 搜索", "_build_pages.py"),
]

for label, script in steps:
    print(f"\n=== {label}（{script}）===")
    result = subprocess.run(
        [sys.executable, str(ROOT / script)],
        cwd=ROOT,
    )
    if result.returncode != 0:
        print(f"\n✗ {script} 失败，停止。")
        sys.exit(result.returncode)

print("\n✓ 全部完成。本地预览：http://127.0.0.1:8080/")
print("  推到线上：git add -A && git commit -m '...' && git push")
