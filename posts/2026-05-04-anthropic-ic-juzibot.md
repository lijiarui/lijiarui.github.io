---
title: 六个 CTO 去 Anthropic 当工程师——国内的技术人，可以来句子互动
date: 2026-05-04
category: thought
tags: 招聘, AI, Agent, 组织, 句子互动
slug: 2026-05-04-anthropic-ic-juzibot
draft: true
description: 过去 16 个月，Workday、Instagram、Box、You.com、Super.com、Adept 的 CTO 陆续从管理岗下来，去 Anthropic 做一线工程师。这事真正的解释不是杠杆，是 Anthropic 的文化——CEO 把 40% 时间花在文化上，工程师和研究员不分，"该做这事的人很可能就是你"。国内没有 Anthropic，但这种文化国内做得到的地方不多，句子互动是其中一个。
---

过去 16 个月，硅谷在发生一件怪事——

- 2025 年 1 月，Adept AI 的 CTO 去 Anthropic 做工程师
- 2025 年 7 月，Super.com 的 CTO 去 Anthropic 做工程师
- 2025 年 12 月，Box 的 CTO 去 Anthropic 做工程师
- 2026 年 1 月，Instagram 联合创始人兼前 CTO Mike Krieger 转入 Anthropic Labs，做工程师
- 2026 年 3 月，You.com 联合创始人兼 CTO 去 Anthropic 做工程师
- 2026 年 4 月，Workday 的 CTO Peter Bailis 去 Anthropic 做工程师

不是去当 VP，不是去当架构师，是真的回到一线写代码、自己提交 PR、不带团队那种。

百亿美元公司的 CTO，放弃几千万年薪和几百人团队，回去当一个一线工程师。

## 杠杆是表象，文化是底层

官方理由都是"AGI 来了，我想坐在前排看"。这话不假，但不够。

更深一层，是 Anthropic 这家公司的文化。这才是 CTO 们愿意降级来这里的原因。

几件具体的事：

- **Dario Amodei 自己说过，他每天 40% 的时间不花在产品决策上，花在公司文化上。**他相信文化是公司能不能"步调一致"的底层，比某一个具体产品决策重要得多。
- **公司官网首句**：engineers do research, researchers do engineering——这里没有"研究员"和"工程师"的隔离，更没有"决策者"和"执行者"的二分。每个人都既写代码又想问题。
- **内部反复说的一句话**：If something needs to be done, the right person to do it is probably you. 一件事必须有人做，那个该做的人很可能就是你。没有"这不是我职责范围内"。
- **每个候选人都过一轮文化面试**，不论你是研究员还是行政。文化对齐是硬门槛，比技术筛得还严。
- **不讲 corpo speak。**Dario 自己讲，公司里"赋能"、"协同"、"对齐"这种话越少越好。直接说真话，包括说"我不知道"。

所以 CTO 们真正放弃的不是 title。是"我每天一半精力花在政治、汇报、跨团队协调上"那种生活。来 Anthropic，他们不需要再为了"对齐组织"花时间。一个人 + 一个强模型，走到底。

杠杆是这件事的结果。**文化是它的前提。**

## 国内技术人看完这篇，会有个尴尬的问题

**那我能去哪？**

国内没有 Anthropic 这种量级的前沿模型实验室。这是事实，没必要绕。

但 Anthropic 真正吸引人的那几件事——CEO 在第一线、研究和工程不分、低 ego、做事的人就是你——这些是文化，不是只有前沿模型实验室才有。

我没法说句子互动是"中国的 Anthropic"，我们不做模型，规模也差几个数量级。但有几件事，我们走的方向是同一个：

## 我们和 Anthropic 哪几点像

**1. 上手干，不评价。**

说实话，我们文化的源头不是 Anthropic，是亚马逊。去年公司年会的主题就是 **Dive Deep, Rise High**——越想看清楚一件事，越得自己钻到细节里去。亚马逊 14 条领导力原则里有一条就叫 Dive Deep：所有层级的人都要 stay connected to the details，没有"这事我大概知道、具体让 XX 讲"那一套。

Anthropic 那句"engineers do research, researchers do engineering"是同一件事的另一种说法。每个人都既动手又想问题，没有"评价者"和"执行者"的二分。

我自己每天的工作是 [1 个我 + N 个 Agent](/thought/2026-05-03-ai-era-competitiveness.html)——脑子想，顺手让 Claude 干，我 review，一次能并行十几条线。一个十年没碰代码的 CEO，被 Claude Opus 4.5 [拉回来天天写代码](/thought/2026-04-28-return-to-code.html)。AI 让 dive deep 的成本降到几乎为零——以前我看不懂的东西，让 Claude 解释一下就能看懂。所以这条文化在 AI 时代反而更能跑得动了。

**2. 工程师和"做产品的人"不分。**

Anthropic 那句"engineers do research, researchers do engineering"——我们这边在发生类似的事。PM、运营、销售、交付都被 Claude 拉回到了一线。挡在他们和代码之间的那层过路费没了。每个工种都在被[重新写一遍](/thought/2026-05-03-claude-code-skills.html)。

**3. 一件事得做，做的人就是你。**

Anthropic 招聘页反复出现的一句话：

> If something urgently needs to be done, the right person to do it is probably you.

这是默认假设的反转。大公司的默认是"这事归别人，除非有人指派给我"——所以你看到问题，默认它不是你的事。Anthropic 的默认反过来：你看到一件事必须有人做，那个人很可能就是你。要么你做，要么你想清楚为什么不该是你。

落到日常：一个 bug 被发现的标准流程不是"提 ticket → 走 backlog → 等排期"，是"看到的人写个 fix → 找熟的人 pair → 当天 deploy"。新员工第一周看到文档不对就自己改，不问"这归谁"。

它和 Amazon 的 Ownership（"never say that's not my job"）+ Bias for Action 是同一件事——**降低协调成本**。CTO 在大公司一半精力花在"让 X 同意 / 找 Y 协调"上，来 Anthropic 这层全没了。

我们也信这条。近百号人，没"对接 BD"、"协调资源"、"等汇报"那套话术。看到流程不对，自己改一个版本试试，一周内部真跑起来再讨论。两款产品——句子秒回管 IM 渠道接入和聚合，句子秒懂是给业务人员用的 Agent 工厂——自己内部用得最深，不然凭什么相信它能帮客户。

**4. 使命具体到能拿来吵。**

Anthropic 官方使命的原话是：

> We build **reliable**, interpretable, and steerable AI systems.

注意第一个词是 **reliable**，不是 safe。外界把他们记成"safety 公司"是因为公关资源都花那儿了——但他们 **85% 的营收来自企业**。企业不容忍 AI 行为不稳定。Anthropic 实际卖给客户的核心价值，从来都是"可靠"。

（顺带一提，Anthropic 自己 2026 年 2 月 [改了 RSP](https://time.com/7380854/exclusive-anthropic-drops-flagship-safety-pledge/)——把"如果不能保证风险被 mitigate 就不发布模型"的硬承诺改成了 nonbinding 框架。"safety-first"的标签今天比 2023 年松动了不少。reliability 反而是越来越硬的那条。）

我们和这条对齐。**做 To B 的人都知道，不靠谱的 AI 等于没用。**客户跑的是营销、客服、销售转化、合规审核——一次幻觉、一次回答不一致、一次掉线，客户丢的是真订单、真客户、真合规风险。"靠谱稳定"对我们不是加分项，是底线。

这个使命具体到能拿来 disagree——一个产品决策做不做、一个客户接不接、一次 demo 要不要用激进模型，都能用这把尺子量。空话产生不了拒绝；具体使命才会。

不像的地方我也讲清楚：我们不做模型，给不到 Anthropic 那种股权回报，办公室也不在 SF。但你想做的"离前沿最近、不被管理稀释、文化驱动"那件事，国内能给到的地方不多，我们是其中一个。

## "AI 不会替代程序员，程序员会替代所有人"

这是 [Naval 那句话](/thought/2026-04-28-return-to-code.html)。我引过一次，再引一次——

> AI won't replace programmers, but rather make it easier for programmers to replace everyone else.

过去能写代码的人是 0.1%。Agent 把这个数字推到 1-3%——几十倍。

放大几十倍的不是"会写代码的人"，是**会用代码 + AI 把自己的判断力、品味、设计感放大成产品的人。**

如果你被 Anthropic 那种文化打动过——
如果你已经被 Claude / Cursor / Codex 喂出过一次"原来一个人可以干这么多事"的体感——
如果你想找一个不用为 title 和管理稀释操心、能直接上手跑的地方——

**来句子互动。**

进来第一天，你就被丢进 1+N。

## 怎么联系

- 直接加我微信：`jiaruijuzi`（备注"Anthropic"我就知道你是从这篇来的）
- 邮箱：rui@juzi.bot
- 公司主页和具体岗位：[juzibot.com](https://juzibot.com)

写在 2026 年 5 月。这一栏我还会继续记。
