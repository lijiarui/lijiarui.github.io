---
title: OpenAI 输给 Anthropic，不是输在产品，是输在组织
date: 2026-05-06
category: thought
tags: AI, Anthropic, OpenAI, To B, 企业 AI, Claude 永动机
slug: 2026-05-06-anthropic-won-enterprise
draft: false
description: 2026 年企业 LLM API 市场份额，Anthropic 32%，OpenAI 25%。财富 10 强里 8 家在用 Claude。OpenAI 输的不是产品，是被 ChatGPT 这个 C 端爆款训练出来的整套组织——工程师文化、迭代节奏、定价模型、销售组织都对不上企业市场。Anthropic 五年前选了反共识那条路。
---

**企业 AI，OpenAI 已经输了。** 不是输在产品，是输在组织——它整套打法都是按 C 端长出来的。

## 先说数字

2023 年底，OpenAI 在企业 LLM API 市场份额 50%。两年半之后，**Anthropic 32%，OpenAI 25%**（[Menlo Ventures 2025 中报](https://x.com/rohanpaul_ai/status/1984683421109481704)）——OpenAI 份额减半，第一名换人。

[Menlo 另一份数据](https://www.axios.com/2026/03/18/ai-enterprise-revenue-anthropic-openai)看 2026 年初的企业 LLM 总支出：**Anthropic 40%，OpenAI 27%**。

ARR 也反超了：[2026 年 4 月 Anthropic 300 亿，OpenAI 约 250 亿](https://medium.com/@david.j.sea/anthropic-just-passed-openai-in-revenue-here-is-why-it-matters-e3dd9bb04069)。年费超百万美元的企业客户超过 1000 家，**两个月翻一倍。财富 10 强有 8 家在用 Claude。**

营收来源也是反过来的——Anthropic **85% 来自企业**；OpenAI **约 60% 来自消费者**（[CNBC, 2026-01-10](https://www.cnbc.com/2026/01/10/anthropic-amodei-siblings-generative-ai.html)）。

## ChatGPT 成全了 OpenAI，也困住了 OpenAI

一个 2 个月内冲到 1 亿用户的消费品，会反过来**让整家公司练出一身 C 端肌肉**——发布节奏快、迭代激进、容忍度高、用户骂两句没事、产品出问题改一版就行。

这套打法在 C 端是优势，到了企业市场就**全成了负债**：

- 企业要的不是"上周更聪明了"，是"过去 12 个月行为一致"
- 企业不接受"偶尔幻觉"，金融、医疗、法务一次幻觉就是合规事故
- 企业采购周期 6-18 个月，要的是 5 年合作；C 端用户中位停留 < 2 周
- 企业要 SOC 2、HIPAA、数据驻留、审计日志；C 端用户根本不知道这些是什么

OpenAI 没法两边都赢——它整套**组织肌肉**（工程师文化、迭代节奏、定价模型、销售组织）都是被 ChatGPT 这个 C 端爆款训练出来的，做不了企业基础设施。

## 五年前的反共识

五年前，Amodei 兄妹带着一批资深研究员从 OpenAI 出来，创立 Anthropic。三条创立原则在当时都属于反共识：

1. **安全和盈利不冲突**——可以同时做
2. **真正的价值在企业市场**，不在 to C 病毒式产品
3. **稳步推进比鲁莽抢跑更能赢**

Anthropic 总裁 Daniela Amodei（CEO Dario 的妹妹）讲过他们当时离开 OpenAI 的想法：

> We really just felt more like we were running towards something than running away from something.
>
> 我们更像是朝着某个东西在跑，而不是从某个东西逃出来。

不是带情绪出走，是带着自己的产品方向离开。2022 年 11 月 ChatGPT 上线、两个月冲到 1 亿用户那一波，Anthropic 看着没跟。Daniela 给的理由：

> Anthropic, as an organization, is well suited to be a B2B company. We really care about things like reliability and security and safety. That's baked into our DNA.
>
> Anthropic 这个组织，本来就更适合做 B2B 公司。我们真的在意可靠性、安全、保密——这些写在 DNA 里。

这三个词的顺序不是随机的——reliability 排在最前，是 Anthropic 五年来反复回到的那个词。

Daniela 还讲过一条内部价值观：

> One of the values and the things that we talk about a lot internally is just how not to believe the hype.
>
> 我们内部一个很重要的价值观，就是不要相信 hype。我们从来不是为了博关注、博头条，是来真的做事的。

Anthropic 投资方 Bessemer Ventures 的合伙人 Sameer Dholakia，给的商业理由是：

> Enterprise customers don't churn the way consumers do.
>
> 企业客户不会像消费者那样说走就走。

C 端用户中位停留不到 2 周，企业一签就是几年。Anthropic 五年前赌的就是这条——前两年看着像放弃 C 端的大市场，今天 ARR 反超 OpenAI。

## Anthropic 选的是 reliability

Anthropic 官方使命的原话：

> We are an AI safety and research company that builds reliable, interpretable, and steerable AI systems.
>
> 我们是一家 AI 安全与研究公司，造的是可靠、可解释、可控的 AI 系统。

他们说自己是 "AI safety and research company"——但造的系统第一属性是 **reliable**，排在 interpretable、steerable 之前。

外界把他们记成"safety 公司"是因为公关声量集中在那儿——但他们卖给企业的核心价值，从来第一位都是 reliable。Daniela 在 CNBC 那段采访里也把顺序排得很清楚：reliability 第一，security 第二，safety 第三。

Anthropic 自己面向企业的话术开头就写：

> Enterprises cannot afford inconsistent AI behavior. Business environments demand repeatable and stable outputs.
>
> 企业容不得 AI 行为不一致。企业场景要的就是可重复、稳定的输出。

硅谷在吵泡沫、刷 benchmark、争谁家模型最聪明，Anthropic 把精力放在那些**很少上头条、却真正决定能不能上线**的问题上——AI 在最敏感的系统里，到底能不能被信任。

Daniela 在 Fast Company 那篇专访里（[2026-01-27](https://www.fastcompany.com/91480487/anthropic-cofounder-daniela-amodei-says-that-ai-entreprise-business-can-trust-will-transcend-the-hype-cycle)）：

> Trust is what unlocks deployment at scale.
>
> 信任，才是规模化部署的钥匙。

> In regulated industries, the question isn't just which model is smartest—it's which model you can actually rely on, and whether the company behind it will be a responsible long-term partner.
>
> 在受监管的行业里，问题不是哪个模型最聪明——是哪个你真能靠得住，以及它背后的公司是不是一个负责任的长期伙伴。

Daniela 紧接着补了一句：

> I think we are a good judge of what our models can do reliably and what they cannot do reliably.
>
> 我们对自己的模型能可靠做什么、不能可靠做什么，判断是准的。

Anthropic 把 Claude 定位成企业基础设施——一种会在医疗系统、保险平台、合规流水线里**连续跑几小时、有时几天**的软件，而不是消费品。

**OpenAI 比的是"最聪明"，Anthropic 比的是"最能放心连续跑一年"。** 客户买单时看的是后者——因为企业评估 AI 的问题变了：过去问"哪个模型最强"，现在问"哪个模型能让我有把握上线进我自己的系统"。

展开看是这 7 道关：

1. **可预测性**——一致、可重复的输出，不能"上周这么答这周那么答"
2. **数据安全与隐私**——内部文档、客户数据、专有信息不外泄
3. **治理与控制**——能划红线、能管住它说什么、能让它按公司规矩办事
4. **可审计与透明**——输出可追溯、可解释，有合规能用的日志
5. **集成**——能接进 CRM、知识库、内部 API、现有工作流
6. **可扩展**——数据量大、用户多、场景杂的时候照样跑得稳
7. **多模型策略**——企业不再押注一家，按场景选最合适的模型

Anthropic 这套打法每一条都对得上。**驱动 AI 采购的不再是模型性能，是模型在企业的真实约束里能不能跑稳。** Accenture、Deloitte 这些咨询大厂也在按这 7 条给客户挑供应商，Anthropic 正好是合身的那家。

## Do More With Less——用更少做更多

"Do more with less" 是 Anthropic 公司层面的价值观——别因为有钱就堆资源，先逼自己用更少的人、更少的钱、更少的算力把事做出来。亚马逊在领导力原则里有一条 Frugality（节俭），讲的是同一件事。

Daniela 在 [CNBC 的另一篇专访](https://www.cnbc.com/2026/01/03/anthropic-daniela-amodei-do-more-with-less-bet.html)里讲：

> Anthropic has always had a fraction of what our competitors have had in terms of compute and capital, and yet, pretty consistently, we've had the most powerful, most performant models for the majority of the past several years.
>
> Anthropic 一直只有竞争对手一小部分的算力和资本，但过去几年里，绝大多数时候我们都在最强最快的模型那一档。

这条价值观体现在好几个维度上，不只算力：

- **算力和资本**：OpenAI 押了 1.4 万亿美元的算力承诺，Anthropic 大约 1000 亿——只有 1/14。
- **基础设施**：OpenAI 重金自建大型园区 + 专属算力；Anthropic 不绑定一家，按成本、可用性、客户需求决定模型跑在哪儿。
- **训练**：把功夫下在更高质量的数据和 post-training 技术上，单位算力性能更高，而不是靠堆参数、堆训练量。
- **产品**：选择跑得起、容易上线的形态，让客户用得起、采用门槛低。

每一笔投入都在算"每美元算力换多少业务结果"。下一阶段拼的不是谁的预训练规模最大，是谁能把单位资源做出最大的能力。

## 这件事对做 To B 创业的人意味着什么

第一波生成式 AI 靠的是消费者兴奋感和病毒式传播。下一波则会在企业的采购流程、架构评审、合规审查里安静地完成——决定 AI 到底能不能真正嵌进有问责机制的组织里。

我有三个判断：

1. **基础设施化**——AI 正在变成像云计算一样"看不见的"企业基础设施，开始承重，开始进入关键工作流。
2. **生态竞争**——胜负不再只取决于模型本身，取决于和现有系统的集成程度。
3. **治理是第一差异点**——AI 治理会成为决定长期供应商关系的核心竞争因素，意义已经超出"合规"本身。

**对国内做 To B 的创业公司也一样。** 最容易踩的坑就是被国内大厂的 C 端 demo 故事带跑——比谁的多模态更炫、谁的 chat 体验更顺。客户付钱看的根本不是这些。

而且中国做 To B 的 AI 创业还多一层硬约束：拿不到美国大厂级别的资本和算力。能赢的路只有一条——"do more with less"，把每一块资源都换成具体的业务结果。

句子互动这两年走的就是这条路。不到 100 人的团队对着四个行业（在线教育、政企、消费品、金融）做 IM-native Agentic AI——不追多模态秀场，不追炫 demo，把每一块算力换成具体业务指标：营销转化、客服一次性解决率、续约率、合规审核通过率。一次幻觉、一次不一致、一次掉线，丢的都是真订单。我们卖的不是 demo 里那个最炫的回答，是连续跑一年都不出意外的那个回答。

为了真做到这件事，我们搭了一套 **Agent 质量保障体系**——AI 测试、批量验收、灰度发布、Badcase 反馈、回归测试、AI 质检 6 个模块串成闭环，覆盖上线前、上线中、上线后整条链路。每次 Agent 改动都跑全量回归，灰度发布按比例分流，线上 AI 客服和人工客服用同一套质检标准。Agent 上线不是赌博，是每一步都有据可依。

我自己每天的工作方式是 1 个人 + N 个 Agent，公司内部先把"每美元算力换多少业务结果"跑通。

Anthropic 在英文世界证明了一遍。中文世界也一样。

赢家不会是最聪明的那家，是最靠得住的那家——这也正是句子互动从做 Agent 第一天起，就一直坚持的事。

