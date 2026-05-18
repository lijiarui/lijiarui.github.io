---
title: 为什么我认为 Anthropic 已经完胜 OpenAI
date: 2026-05-05
category: thought
tags: AI, Anthropic, OpenAI, To B, 战略
slug: 2026-05-05-anthropic-beats-openai
draft: true
description: 在 C 端 OpenAI 没输，ChatGPT 周活 9.1 亿。但在决定 AI 长期格局的那条赛道——企业把 AI 塞进核心系统——Anthropic 已经完胜。Menlo Ventures 最新数据，Anthropic 占 40% 企业 LLM 支出，OpenAI 从 2023 年的 50% 跌到 27%；编程市场 54% vs 21%。这件事对做 to B 的人意味着什么。
---

先把前提挑清楚——

C 端，OpenAI 没输。ChatGPT 周活 9.1 亿，是 Claude 的几倍。

我说的"完胜"，是另一条赛道——**企业把 AI 塞进核心系统**那条。这条上 Anthropic 已经赢了，赢得不只是领先，是反转。

## 一组让我下决心写这篇的数字

Menlo Ventures 2025 年那份《State of Generative AI in the Enterprise》，最新数据：

| 指标 | 2023 | 2025 末 |
|---|---|---|
| Anthropic 占企业 LLM 支出 | **12%** | **40%** |
| OpenAI 占企业 LLM 支出 | **50%** | **27%** |
| 编程市场（Claude Code 出来之后） | — | Anthropic **54%** vs OpenAI **21%** |

两年时间，OpenAI 在企业市场的份额掉了**接近一半**。同期 Anthropic 翻了三倍多。这是我能找到的、关于 AI 公司格局的所有数字里**最干净的一组反转**。

企业 LLM 支出不是小生意。Menlo 那份报告里 2025 年企业生成式 AI 总投入 **370 亿美元**，一年翻三倍。

收入侧 Anthropic 给的曲线更夸张：

- 2023 年底 ARR：**8700 万美元**
- 2024 年底 ARR：**10 亿美元**
- 2025 年底 ARR：**90 亿美元以上**

三年 100 倍。估值 **1830 亿美元**，新一轮在谈。

## "完胜"的判定标准是什么

OpenAI 收入仍然比 Anthropic 高（2025 年约 130 亿，2026 预计 290 亿），周活更碾压。但收入结构是反的——

- **Anthropic 的钱：85% 来自企业**
- **OpenAI 的钱：60% 还来自消费者**（企业占比 40%，在追，但还没追上）

为什么我把企业市场看得比 C 端更重要？因为 AI 真正改变世界的方式，不是被 9 亿人闲聊用，是被几万家企业**塞进核心流程**。

闲聊会换。明天 Gemini 3 出来更好玩，9 亿人里有 3 亿迁过去，OpenAI 的护城河就掉一截。

但 Banner Health 的 22000 名医生用上 Claude 辅助工作流之后，**85% 反馈速度更快、准确度更高**——这种东西不会换。它要重新过 IT 评审、合规审查、HIPAA 复检，至少半年。Novo Nordisk 把临床文档周期从 12 周以上压到几分钟，Travelers 把 Claude 接给 1 万员工，Snowflake 签了 2 亿美元的联合开发——这些都是**几年走不动的合同**。

Bessemer 的合伙人 Sameer Dholakia 一句话点透：

> Enterprise customers don't churn the way consumers do.

C 端的胜利每周都在重新发生一次。企业的胜利发生一次，再发生一次的概率就很低。

## Daniela 那两句话，把 Anthropic 的差异化讲透了

2026 年 1 月 10 日，Daniela Amodei 对 CNBC：

> Anthropic, as an organization, is well suited to be a B2B company. **We really care about things like reliability and security and safety.** That's baked into our DNA.

注意她列的顺序——**reliability 在前，security 和 safety 在后**。

外界把 Anthropic 记成"safety 公司"，是因为他们的 PR 资源都花在那里。但 Anthropic 总裁亲口讲的话，第一个词是 reliability。

两周后 Fast Company 那篇专访（1 月 27 日），她把这件事讲得更直白：

> Trust is what unlocks deployment at scale. In regulated industries, the question isn't just which model is smartest—**it's which model you can actually rely on**, and whether the company behind it will be a responsible long-term partner.

**最聪明 ≠ 最能用。**

做 to B 的人都懂这个区别。我们[句子互动](/thought/2026-05-04-anthropic-ic-juzibot.html)做的是 IM 渠道、客服、销售转化、合规审核——一次幻觉，一次回答不一致，丢的都是真订单。客户买的不是 demo 里那个最炫的回答，是连续跑一年都不出意外的那个回答。

OpenAI 这两年憋的力气是 GPT-5、Sora、ChatGPT Health——都在追"最聪明"。Anthropic 这两年憋的力气是 Claude Code、Cowork、HIPAA-ready 部署——都在追"最能用"。两年下来，Menlo 那张表就是结果。

## Anthropic 不是 safety 信仰公司，是企业可靠合作伙伴

这件事 2026 年 2 月看得最清楚——

2 月 25 日，Anthropic **改了 RSP**（Responsible Scaling Policy）。原来 2023 年定的最硬一条——"如果不能保证风险被 mitigate 就不发布模型"——改成 nonbinding 框架。CSO Jared Kaplan 对 TIME 说：

> 我们觉得，停下来对谁都没好处。

CNN、TIME 把这件事定性为"Anthropic 在竞争压力下放弃旗舰安全承诺"。看着像是品牌崩塌。

但客户没跑。Travelers、Snowflake、Banner Health、Eli Lilly——续约的续约，扩签的扩签。

因为**客户买的从来不是 safety 招牌，是 reliability**。Safety 招牌是让 reliability 更可信的工具，不是终极目的。两者目标一致：你这个 AI 放进我系统跑一年，能不能不出事。

讽刺的是同一时间——

2024 年中 OpenAI superalignment 团队解散、Ilya 离开、Jan Leike 离开。那波之后**OpenAI 的企业份额掉得最快**。不是因为客户突然变成了"安全主义者"，是因为客户读懂了一个信号：**这家公司说改就改的东西太多了**。

Anthropic 改 RSP 没掉份额，OpenAI 拆 superalignment 掉了份额。区别在哪？区别在 Anthropic 改的是**自己单方面的承诺**，OpenAI 拆的是**对客户而言的可靠性信号**。

reliability 这个词在企业市场比想象中更具体。

## 五角大楼那一仗，显示真正的护城河是什么

2026 年 2 月 28 日，CBS 独家。

五角大楼给 Anthropic 周五晚上的最后通牒——红线松，不松就 6 个月内停用。Anthropic 两条红线：**不用于大规模监控**、**不用于自主武器**。

Hegseth（防长）说他们"想夺取一票否决权"。Trump 直接喊"他们在让美国人命处于危险中"。

Dario Amodei 在专访里两句话顶回去：

> 只要符合我们的红线，我们仍然有兴趣和他们合作。
>
> ...可靠性还没到那一步（The reliability is not there yet）。

第一句留谈判门，第二句拿"可靠性"当挡箭牌。

我看这件事最深的地方不是红线本身，是**Amodei 这一仗的底气从哪来**。

一家两年前的 startup 敢和美国国防部+总统硬刚——因为它知道自己背后站着 Travelers 1 万员工、Banner Health 22000 医生、Snowflake 2 亿美元、Eli Lilly、Sanofi、Novo Nordisk、Stanford。这些客户**今年不会跑、明年不会跑、后年大概率也不会跑**。

一家以 to C 收入为主的公司在和国防部对峙时不会有这种底气。因为它的用户群是想看 demo 的人，明天可以换 ChatGPT、换 Gemini。

**B 端客户的 churn 成本越高，你越不容易被踢出去。** Amodei 那句"我们不会在红线上让步"——本质上是这件事的派生品。

## 给做 to B 的人的几条收尾

OpenAI 没输。它在 C 端赢得彻底，9 亿人的心智仍然写着"AI = ChatGPT"。

但 AI 嵌入世界的方式不是被 9 亿人闲聊，是被几万家企业塞进核心流程。后者这条线，**胜负已定**。

对做 to B 的人，这件事的几条直接含义：

**1. 不要追最炫的 demo。** 客户买的不是 demo 那个回答。是同样的回答跑 365 天不出意外。这两件事在工程上是不同的难度等级。

**2. reliability、safety、合规——是一回事，不是三回事。** 它们都在回答一个问题：你这个 AI 放进我系统，明年我会不会因为它丢工作。你哪个角度切都行，但不能只切其中一个。

**3. 客户的 churn 成本是你最大的护城河。** 比你的模型 benchmark 重要。比你的估值重要。让客户离不开你的，不是你多聪明，是切换你的成本有多高。

**4. 别相信 hype。** 这是 Daniela 在 CNBC 那一段我最喜欢的一句话——"我们内部反复讲，不要相信 hype。我们不是为了博关注、博头条，我们是来真的做事的。" 这话听上去像鸡汤，做 to B 的人听一遍就懂——做 hype 拿不到企业续约，做 hype 拿不到 HIPAA 认证，做 hype 拿不到五角大楼对峙的底气。

OpenAI 这两年是被 hype 推着跑。Anthropic 这两年在拒绝被 hype 推着跑。

两年下来，Menlo 那张表就是答案。

---

**注释 / 数据来源**

- Menlo Ventures, *2025: The State of Generative AI in the Enterprise*：企业 LLM 支出 $37B、Anthropic 40% / OpenAI 27% / Google 20%、编程市场 Anthropic 54% vs OpenAI 21%
- CNBC, *Anthropic's Amodei siblings may hold the key to generative AI*（2026-01-10）：85% B2B、$183B 估值、ChatGPT 9 亿周活
- Fast Company / Yahoo, *Daniela Amodei says trusted enterprise AI will transcend the hype cycle*（2026-01-27）："Trust is what unlocks deployment at scale"、收入曲线、Banner Health 85%、Novo Nordisk 12 周→几分钟
- TIME, *Exclusive: Anthropic Drops Flagship Safety Pledge*（2026-02）：Jared Kaplan 关于 RSP 变更的访谈
- CBS News, *Anthropic CEO says he's sticking to AI "red lines" despite clash with Pentagon*（2026-02-28）
- Sacra / SaaStr：OpenAI ARR、企业占比、ChatGPT 周活

数据是 2026 年 5 月初的截面。再过一两个季度看不一定还成立。
