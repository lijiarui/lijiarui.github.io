---
title: 给 Claude Code 装上眼睛 - 聊聊 code intelligence plugin
date: 2026-05-03
category: thought
tags: Claude 永动机, Claude Code, LSP, 工具
slug: 2026-05-03-claude-code-lsp
description: Claude Code 文档里有一条 tip：装 code intelligence plugin。我点进去看了下，底下是 LSP——VS Code、Neovim 用了十年的代码智能基建。之前 Claude 改完 TypeScript 自信地说"完成了"，我跑 tsc 红线一片；装上再做一遍，过了。LSP 不是给 Claude 加新功能，是给它装上眼睛。
---

Claude Code 的[官方文档](https://code.claude.com/docs/en/common-workflows)在 "Find relevant code" 那节末尾埋了一条 tip：

> 为你的语言安装 code intelligence plugin，让 Claude 拥有精确的"跳转到定义"和"查找引用"导航能力。

我点开 code intelligence plugin 那个链接看了下。底下是 LSP——VS Code、Neovim、JetBrains 用了十年的那套代码智能基建。

那就试一下。

让 Claude 改一个 TypeScript 函数加个参数，调用方都跟着改。

**不装 LSP**：它说"完成了"。我跑 tsc，红线一片——漏了一个用 `import { foo as bar }` 别名调用的文件。这种事发生过很多次。

**装了 `typescript-lsp`**：再做一遍，过了。

差别在哪？为了搞明白，我把整条链路从头捋了一遍。这篇是捋完的笔记。

## 这事其实要装两样东西

我一开始没搞清楚的就是这件——以为 `/plugin install typescript-lsp@claude-plugins-official` 跑一下就完事，结果跑起来什么也没多。

要装的是两样：

1. **Claude Code 这边的插件**（让 Claude 学会说 LSP 这套行话）
2. **你机器上的 language server**（在另一边接话的程序）

少一个都不行。下面分别说。

## 第一样：code intelligence plugin

Claude Code 的插件系统里有一类专门叫 **code intelligence**——给 Claude 提供"理解代码语义"的能力。

默认的 Claude Code 只会 Read 文件 + grep 文本，对代码的理解停留在字符串层面：不知道一个变量真实的类型，不知道一个函数被谁调用过，不知道改完编译挂没挂。code intelligence plugin 补的就是这块。

按语言分，官方市场 `claude-plugins-official` 里都有：

| 语言 | 插件名 |
|---|---|
| TypeScript / JavaScript | `typescript-lsp` |
| Python | `pyright-lsp` |
| Go | `gopls-lsp` |
| Rust | `rust-analyzer-lsp` |
| Java | `jdtls-lsp` |

在 Claude Code 里直接装：

```
/plugin install typescript-lsp@claude-plugins-official
/reload-plugins
```

**装一次到处用。** 插件存在 `~/.claude/plugins/`，所有项目共享，不用每个项目装一次。如果哪个项目不想用，去那个项目的 `.claude/settings.json` 里单独关掉。

## 第二样：language server 二进制

这一步是我之前漏掉的——以为插件自带就行。不是。

插件**只是适配器**，让 Claude 会说 LSP 这套协议；但跟谁说？得另一个程序在那边接着。这个程序就是 **language server**，你得自己装。

不同语言对应不同的 server：

| 插件 | 你要装的二进制 |
|---|---|
| `typescript-lsp` | `typescript-language-server` |
| `pyright-lsp` | `pyright` |
| `gopls-lsp` | `gopls` |
| `rust-analyzer-lsp` | `rust-analyzer` |
| `jdtls-lsp` | `jdtls` |

TypeScript 的装法：

```bash
npm i -g typescript typescript-language-server
```

验证一下装好了：

```bash
which typescript-language-server
# /opt/homebrew/bin/typescript-language-server
```

两边接上，Claude 才真的多了眼睛。

## language server 到底是什么

一个常驻后台的程序，干一件事：理解你项目里的代码。

跑起来之后它做这些：把所有源文件读一遍，建一棵抽象语法树，在内存里维护一张**符号表**——哪个文件定义了哪个 class / function / variable，类型是什么，被谁引用过。你改文件，它增量更新这张表。别人（编辑器、Claude）问它问题，它从这张表里查答案。

它**不是编译器**——它不生成可执行代码。`tsc` 是编译器，`typescript-language-server` 是常驻的查询服务。底层都依赖 TypeScript 那套解析和类型推导，目的不同。

打个比方。把项目想成一座图书馆。`tsc` 是把书印出来给读者拿走的印刷工。`typescript-language-server` 是常驻图书馆的资深管理员——记得每本书在哪、每个引用在哪、谁引用了谁，你问什么他张口就答。VS Code、Claude Code 这些编辑器，是来图书馆的读者，通过统一提问方式（LSP 协议）跟管理员对话。

Claude 之前没有管理员，自己满架子翻书。现在有了。

## 顺便说一句 LSP

"语言服务器"这个东西能成立，靠的是微软 2016 年定的 **LSP 协议**（Language Server Protocol）。

在它之前，每个 IDE 要支持每种语言，都得自己实现一遍跳定义、查引用、补全、类型检查。N 种 IDE × M 种语言，重复 N×M 次。LSP 的做法是把"编辑器"和"语言服务器"拆开，让它变成 N+M：每种语言出一个 server，所有编辑器通过同一套协议调用。

VS Code、Neovim、JetBrains、Sublime——背后都是这套。十年下来主流语言的 language server 都很成熟。Claude Code 的 code intelligence 插件，就是把 Claude 也接进了这套体系，复用这十年的基建。

## Claude 怎么用 LSP

装好之后 Claude 用 LSP 有两种方式，你都不用打命令：

**一种是自动用——改完之后看到诊断**。每次 Edit / Write 一个文件，Claude 立刻拿到该文件的真实诊断：类型错误、未定义符号、import 拼错、未使用变量、语法错误。红线在它眼皮底下，它自己会修。**"改完编译挂了你来修"这种来回打的轮次大幅减少。**

**另一种是按需用——Claude 自己判断要不要调**。让它给一个函数加参数、调用方都跟改？它会调 `find references` 拿到所有真实调用点。让它读一段不熟的代码？它会调 `hover` 看类型。让它做重命名？它会按符号改而不是全文替换。

第一种是 Claude Code 自动塞给 Claude 的，第二种是 Claude 根据当前任务自己判断要不要调。

## grep 派变成 LSP 派

具体能力上的差别：

| 操作 | 不装 | 装了 |
|---|---|---|
| 跳定义 | grep，会漏 re-export、泛型 | LSP 一步到位 |
| 查引用 | grep 字符串，会误报（注释里、字符串里） | 按语义匹配 |
| 改名重构 | 全文替换，容易改错同名变量 | 按符号改，作用域内安全 |
| 看接口实现 | grep `implements Foo` | LSP 直接列 |
| 类型 / 签名 | 模型脑补 | LSP 给确定答案 |

跨文件改动尤其明显。grep 派的 Claude 经常漏改一个 re-export 文件，编译挂了才发现。

还有一个隐性收益：**上下文窗口更省**。不装的时候 Claude 为了搞清楚一个符号常常要 Read 整个文件，甚至几个文件。装了之后大量"是什么 / 在哪里 / 谁用它"的问题由 LSP 直接回答，不再把无关代码塞进上下文。长会话、大代码库下区别尤其明显。

## 一个具体场景

让 Claude 给一个 TS 函数加参数，调用方都跟着改。

不装：grep 函数名 → 漏掉 `import { foo as bar }` 的别名调用 → tsc 报错 → 再修 → 来回 2-3 轮。

装了：LSP find references → 拿到所有真实调用点（别名、re-export 都有） → 一次改完。

## 什么时候不装

- 单文件脚本、写完就扔的玩具——overhead 大于收益
- 项目语言没有对应 LSP（纯 shell、纯 SQL）
- language server 二进制本身有成本（rust-analyzer 几百 MB，jdtls 启动慢）

我大部分时间在用 Claude Code 做飞书数据拉取 + 战略分析，代码是给自己用的小工具。这种情况：**TypeScript / Python 项目装一下值，纯 CLI 脚本可以不装。**

## 一句话

**LSP 不是给 Claude 加新功能，是给它装上眼睛。**

之前它靠 grep 看世界，现在它接上了编译器。

写在 2026 年 5 月，重新读 Claude Code 文档的那个下午。
