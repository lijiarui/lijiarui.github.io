---
title: 你的标题
date: 2026-04-27
category: thought
tags: 标签1, 标签2, 标签3
---

正文从这里开始。

支持完整 Markdown：

## 二级标题

正文段落，可以 **加粗**、*斜体*、`代码`、[链接](https://juzibot.com)。

### 三级标题

- 列表项一
- 列表项二
- 列表项三

> 引用一段话。

```python
# 代码块
print("Hello")
```

----

## 写作约定

- **文件名**：`YYYY-MM-DD-英文-slug.md`，例：`2026-04-27-juzibot-roadmap.md`
- **frontmatter**：
  - `title` 必填，中文也行
  - `date` 必填，`YYYY-MM-DD` 格式
  - `category` 必填，从这几个选一个：`thought`、`reading`、`chatbot`、`project`、`saas`、`interview`
  - `tags` 选填，逗号分隔
- 写完保存，跑 `python3 build.py`，自动发布
