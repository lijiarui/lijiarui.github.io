---
title: 我有 10 个 Skill，最常用的那个我从没打过 /
date: 2026-05-03
category: thought
tags: Claude 永动机, Claude Code, Skill, Agent
slug: 2026-05-03-claude-code-skills
draft: true
description: 上一篇我说"一个 Agent 的本质，就是一组编排好的 skill"。这篇接着回答：skill 到底怎么用？我花了一下午把自己的 Claude Code 重新搭了一遍，拆出 10 个按需加载的 skill，发现一件反直觉的事——好 skill 你从来不需要打 /。
---

[上一篇](/thought/2026-04-28-return-to-code.html)我说，"一个 Agent 的本质，就是一组编排好的 skill"。

那 skill 到底怎么用？我之前一直没搞明白。今天花了一下午把自己的 Claude Code 重新搭了一遍，发现一件反直觉的事：

**好 skill，你从来不需要打 /。**

## 我之前搞错了

我以前以为 skill 就是"给 Claude Code 加几个 / 命令"。所以我写了三个：

- `/rename`：按文件内容自动改名
- `/sync-memory`：把 claude.ai 网页端的 memory 同步过来
- `/create-feishu-doc`：以我身份在飞书云盘创建文档

写完觉得很爽。

直到我去翻所有会话历史——Claude Code 把每条会话都存成 JSONL，正好能扫。`/rename` 调过 0 次。`/sync-memory` 调过 0 次。`/create-feishu-doc` 调过 8 次，**但没有一次是我打 / 触发的**，全是我跟 Claude 说"帮我把这个内容存到飞书"，它自己找出来用的。

**我没用 / 的那个，反而是我用得最多的。**

## Skill 不是命令，是 Agent 的函数

去翻 Claude Code 官方文档，发现写 skill 的关键不在步骤本身，在这条 description：

> 当用户做 X、说 Y、给了 Z 类型的链接时，使用本 skill。
>
> <span class="cite">—— [Claude Code Skills 官方文档](https://docs.claude.com/en/docs/claude-code/skills)（英文原文 example：*Use when the user asks what changed, wants a commit message, or asks to review their diff.*）</span>

Claude 看到符合的场景就自己拉这个 skill 出来用。打 / 是兜底——好的 skill 描述清楚，Claude 该自己出来。

这一下懂了。Skill 不是命令面板里的快捷方式。**Skill 是 Agent 的函数**——Agent 决定什么时候调用，调用之后按 skill 里写的步骤执行。

我以前的比喻"一个 Agent 的本质就是一组编排好的 skill"——是对的，但我没真正用对。我把 skill 当**手动调用的工具**用，而不是**Agent 自动调度的函数**用。

## 我新搭的 10 个 skill

按这个思路重新搭。

**Claude 自己会自动调的 5 个**——给 Agent 扩展能力：

- `read-wechat`：抓微信公众号文章。WebFetch 默认 UA 会被微信拦成"环境异常"，这个 skill 用微信内置浏览器 UA 绕过。我发个 mp.weixin.qq.com 链接，Claude 自己就调
- `read-feishu-doc`：拉飞书文档/Bitable/Wiki，走 lark-cli。我发个飞书链接，Claude 自己就调
- `juzibot-context`：句子互动业务/产品/客户的完整背景。讨论业务时 Claude 自己加载
- `claude-code-docs-fresh`：问 Claude Code 相关问题前先抓官方文档。Claude Code 每两周一更，Claude 训练数据永远是旧的。我问过几次 hooks 现在支持什么，它一本正经地编了不存在的字段，我才加这个
- `free-port`：起本地服务前先 `lsof` 找个没被占用的端口。我自己两个服务在 8787 撞过一次，Claude 写 server 又默认写 8787

**只能我手动 / 触发的 5 个**——有副作用，必须我点头：

- `/create-feishu-doc`：创建飞书文档。但**我从不打这个 /**，我说"存到飞书"它自己出来
- `/rename`：批量改文件名
- `/sync-memory`：同步 memory
- `/pg-review`：按 Paul Graham 朴素直白审我写的中文文案
- `/lark-data-overview`：拉数据先给规范概览（样本 + 字段说明 + 可疑值），不直接出结论

最后这个是我反复栽过的坑——Claude 拉到数据喜欢直接写结论，我每次得手动喊停。把它写成 skill，下次它自己走流程。

## 一个意外收获：CLAUDE.md 应该越短越好

我一直以为 CLAUDE.md 是越详细越好。错了。

CLAUDE.md 是**常驻 prompt**——每次会话每次对话每次都在烧 token。skill 是**按需加载**——不用就只占一行 description。

我把 CLAUDE.md 里"句子互动公司业务上下文"那 200 字搬进了 `juzibot-context` skill。讨论业务时它自动加载，不讨论时常驻 prompt 里没这段。

判断准则我现在用一句话：

> **事实/约束**（命名规范、写作风格、工具偏好）→ CLAUDE.md
>
> **步骤/SOP/可复用流程**（怎么读公众号、怎么发飞书文档、怎么审 deck）→ skill
>
> **长背景**（业务、客户、行业）→ skill（按需加载）

## 三条规则

这一下午踩坑出来的规则：

**1. 想让 Claude 自动用，description 写"什么时候触发"，不写"做什么"。** 写"当用户发来 mp.weixin.qq.com 链接时使用"，比写"抓微信公众号文章"管用得多。

**2. 有副作用的，加 `disable-model-invocation: true`。** 改文件、写文档、调外部 API 的——必须人点头。这个 flag 还有第二个作用：description 不进 Claude 的常驻 context，省 token。

**3. CLAUDE.md 里超过 200 字的章节，考虑搬进 skill。** 你不是每次会话都需要它，按需加载更便宜。

## 回到 1+N

[上一篇](/thought/2026-05-03-ai-era-competitiveness.html)我说，1+N 这个组织单元里 "1" 应该 keep 不可替代的 20%，"N" 接走 80%。

skill 就是把那 80% **显式**写下来。每个 skill 是一段 SOP，告诉 Agent：什么时候触发、怎么干、用什么工具、做完放哪。

我以前写组织 SOP 是给团队看的——给人念的。现在写 skill 是给 Agent 跑的——能直接执行的。

**组织设计从"画组织架构图"变成"编排 skill"，这件事我之前是当口号说的。直到今天把自己的 Claude Code 重搭一遍，才第一次具体感觉到这话什么意思。**

写在 2026 年 5 月，从我这一台 Mac 开始。
