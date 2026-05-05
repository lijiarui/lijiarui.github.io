---
title: OpenAI 输给 Anthropic，不是输在产品，是输在基因
date: 2026-05-06
category: thought
tags: AI, Anthropic, OpenAI, To B, 企业 AI
slug: 2026-05-06-anthropic-won-enterprise
draft: false
description: 2026 年企业 LLM API 市场份额，Anthropic 32%，OpenAI 25%。代码生成市场 Anthropic 拿到 42-54%，OpenAI 21%。财富 10 强里 8 家在用 Claude。这不是单点失利，是 OpenAI 的消费品基因和企业 AI 这门生意根本不匹配——而 Anthropic 五年前就把 reliable 排在 safe 前面。
---

**企业 AI，OpenAI 已经输了。** 不是输在某条产品线，是整家公司就不是按企业市场长出来的。

## 先说数字

2023 年底，OpenAI 在企业 LLM API 市场份额 50%。两年半之后，**Anthropic 32%，OpenAI 25%**（[Menlo Ventures 2025 中报](https://x.com/rohanpaul_ai/status/1984683421109481704)）。一进一出，七十五个百分点的位置互换。

[Menlo 的另一份数据](https://www.axios.com/2026/03/18/ai-enterprise-revenue-anthropic-openai)看 2026 年初企业 LLM 总支出：

- **Anthropic 40%**
- **OpenAI 27%**

代码生成是企业掏钱最痛快的那个场景：

- **Claude 42%–54%**
- **OpenAI 21%**

ARR 也反超了：[2026 年 4 月 Anthropic 300 亿，OpenAI 约 250 亿](https://medium.com/@david.j.sea/anthropic-just-passed-openai-in-revenue-here-is-why-it-matters-e3dd9bb04069)。年费超百万美元的企业客户超过 1000 家，**两个月翻一倍。财富 10 强有 8 家在用 Claude。**

CNBC 那组数字也值得放进来——Anthropic 营收 **85% 来自企业**；OpenAI 反过来，**约 60% 来自消费者**（[CNBC, 2026-01-10](https://www.cnbc.com/2026/01/10/anthropic-amodei-siblings-generative-ai.html)）。

## 成全 OpenAI 的，也是困住它的

ChatGPT 把 OpenAI 抬起来，也把它焊在了 C 端。

一个 2 个月内冲到 1 亿用户的消费品，会反过来**塑造整家公司的肌肉**——发布节奏快、迭代激进、容忍度高、用户骂两句没事、产品出问题改一版就行。

这套打法在 C 端是优势，到了企业市场全是负债：

- 企业要的不是"上周更聪明了"，是"过去 12 个月行为一致"
- 企业不接受"偶尔幻觉"，金融、医疗、法务一次幻觉就是合规事故
- 企业采购周期 6-18 个月，要的是 5 年合作；C 端用户中位停留 < 2 周
- 企业要 SOC 2、HIPAA、数据驻留、审计日志；C 端用户根本不知道这些是什么

OpenAI 没法两边都赢。工程师文化、迭代节奏、定价模型、销售组织——全是按"消费品 + 开发者 API"长出来的肌肉。这套肌肉做不了企业基础设施。

## 五年前的反共识

五年前，Amodei 兄妹带着一批资深研究员从 OpenAI 出来，创立 Anthropic。三条创立原则在当时都属于反共识：

1. **安全和盈利不冲突**——可以同时做
2. **真正的价值在企业市场**，不在 to C 病毒式产品
3. **稳步推进比鲁莽抢跑更能赢**

Anthropic 总裁 Daniela Amodei（CEO Dario 的妹妹）讲过他们离开 OpenAI 时是什么感觉：

> We really just felt more like we were running towards something than running away from something.
>
> （我们更像是朝着某个东西在跑，而不是从某个东西逃出来。）

不是带情绪出走，是带着自己的产品方向离开。2022 年 11 月 ChatGPT 上线、两个月冲到 1 亿用户那一波，Anthropic 看着没跟。Daniela 的解释直接：

> Anthropic, as an organization, is well suited to be a B2B company. We really care about things like reliability and security and safety. That's baked into our DNA.
>
> （Anthropic 这个组织，本来就更适合做 B2B 公司。我们真的在意可靠性、安全、保密——这些写在 DNA 里。）

她反复强调内部一条价值观：

> One of the values and the things that we talk about a lot internally is just how not to believe the hype.
>
> （我们内部一个很重要的价值观，就是不要相信 hype。我们从来不是为了博关注、博头条，是来真的做事的。）

Anthropic 投资方 Bessemer Ventures 的合伙人 Sameer Dholakia，给的商业理由是：

> Enterprise customers don't churn the way consumers do.
>
> （企业客户不会像消费者那样说走就走。）

C 端用户中位停留不到 2 周，企业一签就是几年。这不是事后总结的优势，是 Anthropic 创立第一天就赌的方向——前两年看起来像放弃了大市场，第三年开始变成护城河。

## Anthropic 选对了第一性的尺子

Anthropic 官方使命的原话：

> We are an AI safety and research company that builds reliable, interpretable, and steerable AI systems.
>
> （我们是一家 AI 安全与研究公司，造的是可靠、可解释、可控的 AI 系统。）

他们说自己是 "AI safety and research company"——但造的系统第一属性是 **reliable**，排在 interpretable、steerable 之前。

外界把他们记成"safety 公司"是因为公关声量集中在那儿——但他们卖给企业的核心价值，从来都是 reliable。Daniela 在 CNBC 那段采访里也把顺序排得很清楚：reliability 第一，security 第二，safety 第三。

Anthropic 自己面向企业的话术开头就写：

> Enterprises cannot afford inconsistent AI behavior. Business environments demand repeatable and stable outputs.
>
> （企业容不得 AI 行为不一致。企业场景要的就是可重复、稳定的输出。）

硅谷在吵泡沫、刷 benchmark、争谁家模型最聪明，Anthropic 把精力放在那些**很少上头条、却真正决定能不能上线**的问题上——这套 AI 在最敏感的系统里，能不能被信任。

Daniela 在 Fast Company 那篇专访里讲得更直接（[2026-01-27](https://www.fastcompany.com/91480487/anthropic-cofounder-daniela-amodei-says-that-ai-entreprise-business-can-trust-will-transcend-the-hype-cycle)）：

> Trust is what unlocks deployment at scale.
>
> （信任，才是规模化部署的钥匙。）

> In regulated industries, the question isn't just which model is smartest—it's which model you can actually rely on, and whether the company behind it will be a responsible long-term partner.
>
> （在受监管的行业里，问题不是哪个模型最聪明——是哪个你真能靠得住，以及它背后的公司是不是一个负责任的长期伙伴。）

Daniela 紧接着的一句，是企业 CIO 最想听的：

> I think we are a good judge of what our models can do reliably and what they cannot do reliably.
>
> （我们对自己的模型能可靠做什么、不能可靠做什么，判断是准的。）

Anthropic 把 Claude 定位成企业基础设施——一种会在医疗系统、保险平台、合规流水线里**连续跑几小时、有时几天**的软件，而不是消费品。

**OpenAI 一直拿"最聪明"那把尺子比，Anthropic 拿的是"最能放心连续跑一年"那把尺子。** 客户买单时用的是后者。

**评估问题已经换了**——过去企业问"哪个模型最强"，现在问"哪个模型能让我有把握上线进我自己的系统"。

后一个问题展开来，是企业 AI 采购真正在过的 7 道关（[techresearchonline 的整理](https://techresearchonline.com/blog/anthropics-rise-enterprise-ai-shift-2026/)）：

1. **可预测性**——一致、可重复的输出，不能"上周这么答这周那么答"
2. **数据安全与隐私**——内部文档、客户数据、专有信息不外泄
3. **治理与控制**——能划红线、能管住它说什么、能让它按公司规矩办事
4. **可审计与透明**——输出可追溯、可解释，有合规能用的日志
5. **集成**——能接进 CRM、知识库、内部 API、现有工作流
6. **可扩展**——数据量大、用户多、场景杂的时候照样跑得稳
7. **多模型策略**——企业不再押注一家，按场景选最合适的模型

Anthropic 在治理、可预测性、企业就绪度上的位置正好对得上这 7 条。**驱动 AI 采购的不再是模型性能，是模型在企业的真实约束里能不能跑稳。** Accenture、Deloitte 这些咨询大厂的生态体系，也在把客户往满足这些条件的方案上引——这条路径上 Anthropic 天然占便宜。

## Do More With Less——不打消耗战

Anthropic 还做对了一件事：不去和对手打算力消耗战。

Daniela 在 CNBC 的另一篇专访里反复回到一句话（[2026-01-03](https://www.cnbc.com/2026/01/03/anthropic-daniela-amodei-do-more-with-less-bet.html)）：

> Anthropic has always had a fraction of what our competitors have had in terms of compute and capital, and yet, pretty consistently, we've had the most powerful, most performant models for the majority of the past several years.
>
> （Anthropic 一直只有竞争对手一小部分的算力和资本，但过去几年里，绝大多数时候我们都在最强最快的模型那一档。）

"Do more with less" 不是口号，是 Anthropic 内部每一个决策的标准——指针都拨在"每美元算力换多少业务结果"上。OpenAI 押 bespoke 园区 + 专属算力，Anthropic 则保留弹性，按成本、可用性、客户需求决定模型跑在哪里，把内部精力压在算法效率和单位算力性能上。

**这件事对中国 AI 创业更关键。**

中国 AI 创业公司拿不到美国大厂级别的资本和算力。要么硬刚做"中国版 OpenAI"——这条路成本结构本身就不利；要么走 Anthropic 这种路——把每一块算力都换成最大的业务结果。

句子互动从第一天起走的就是第二条。50 多人的团队对着四个行业（在线教育、政企、消费品、金融）做 IM-native Agentic AI——不追多模态秀场，不追炫 demo，把每一块算力换成具体业务指标：营销转化、客服一次性解决率、续约率、合规审核通过率。我自己每天的工作方式是 1 个人 + N 个 Agent，公司内部先把"每美元算力换多少业务结果"跑通——"do more with less" 不是事后总结的话术，是组织日常的样子。

## 这件事对做 To B 的人意味着什么

第一波生成式 AI 靠的是消费者兴奋感和病毒式传播。下一波则会在企业的采购流程、架构评审、合规审查里安静地完成——决定 AI 到底能不能真正嵌进有问责机制的组织里。

下一波的胜负，我自己看的是三条线：

1. **基础设施化**——AI 正在变成像云计算一样"看不见的"企业基础设施，开始承重，开始进入关键工作流。
2. **生态竞争**——胜负不再只取决于模型本身，取决于和现有系统的集成程度。
3. **治理是第一差异点**——AI 治理会成为决定长期供应商关系的核心竞争因素，意义已经超出"合规"本身。

**这三条在国内同样成立。** 国内做 To B AI 的同行最容易踩的坑，就是被国内大厂的 C 端 demo 故事带跑——比谁的多模态更炫、谁的 chat 体验更顺。客户付钱的时候用的不是这把尺子。

句子互动这两年也在反复回到这件事——客户跑的是营销、客服、销售转化、合规审核。一次幻觉、一次不一致、一次掉线，丢的都是真订单。我们卖的不是 demo 里那个最炫的回答，是连续跑一年都不出意外的那个回答。

Anthropic 在英文世界证明了一遍。中文世界也一样。

赢家不会是最聪明的那家，是最靠得住的那家。
