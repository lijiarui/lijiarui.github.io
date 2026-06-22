---
title: 公司里 GitHub 讲得最好的，是个高三刚毕业的实习生
date: 2026-06-22
category: thought
tags: GitHub, 开源, AI Native, 实习生, 团队, Wechaty, 管培生
slug: 2026-06-22-highschool-intern-github
draft: false
description: 今天管培生例会，给全公司讲 GitHub 的是郭骐畅——高三刚毕业，来公司不到一个月。两周前他连 PR 是什么都不知道，跟 Claude 学会发 PR，今天就站上去讲了一堂。这篇把他讲的内容整理出来：不教命令行，只解决看懂项目、基本操作、开源生态三件事。Git 是时光机，GitHub 把它搬上云；怎么读懂一个仓库主页的六个位置；Commit、Branch、Pull Request 到底是什么，配一个真实被关掉的 PR 故事；30 秒判断一个开源项目靠不靠谱；大公司为什么把看家代码免费送出去。最后讲讲我为什么敢让一个 18 岁的人来讲、给他无限 token、让两个实习生赛马式开发——一个 AI Native 团队是什么样子。
---

今天的管培生例会，讲 GitHub 的是郭骐畅。他高三刚毕业，来公司不到一个月。

两周前，他连 PR 是什么都不知道。

那会儿我让他和另一个大一的同学徐赫铖一起重做官网，两个人赛马，各做一版。郭骐畅做完，想把改动给我，发来一句"我提交了"，附一个 GitHub 链接。那不叫发 PR。我回他：你问一下 Claude，什么叫发 PR，让它教你，或者让它直接帮你发也行。

第二天他就会了。又过几天，我让他把 GitHub 整个研究一遍，给全体管培生讲一堂——这帮人大多不写代码，市场、运营、产品都有。他做了一套 PPT、一份逐页讲稿，挂在公网上，自己站上去讲了十五分钟。

讲得比我预想的好。所以这篇我把他讲的整理出来，基本是他的原话和他的例子。一个刚成年的人怎么把 GitHub 讲清楚，本身就值得看。下面每一节配的图，都是他那套 PPT 的原页。

<img src="/img/posts/2026-06-22-highschool-intern-github/slides/slide-01.jpg" alt="郭骐畅的 GitHub 分享 PPT 封面页：GitHub，全世界一起盖楼的地方" class="full">

## 他上来就说，今天不教命令行

郭骐畅的开场是个段子。他说网上最火的那篇 GitHub 教程，两万字一百张图，从 `git init` 一路敲到 SSH 公钥，底下第一条高赞评论是：

> 看完后，我仿佛一个想点外卖，却注册成了骑手的人。

"我们不干这事。"他说，"你们不是来当骑手的。今天只解决三件事：看懂一个项目、会用基本操作、理解开源生态。命令行那套，等你真要用的时候，半天就会，不值得今天花时间。"

<img src="/img/posts/2026-06-22-highschool-intern-github/slides/slide-02.jpg" alt="PPT 开场页：今天不教你们敲命令。引用那条高赞评论——看完后，我仿佛一个想点外卖却注册成了骑手的人" class="full">

这个判断是对的。公司里九成的人用 GitHub，要的是看懂和判断，不是敲命令。

## 先说一个你可能不知道的事实：你的公司就是开源一员

他的第一张干货页，讲的是 Wechaty。

<img src="/img/posts/2026-06-22-highschool-intern-github/slides/slide-03.jpg" alt="PPT 页：你入职的公司，本身就是开源世界的一员。配 wechaty/wechaty 仓库实时截图，两万两千多颗 Star" class="full">

"你入职的这家公司，本身就是开源世界的一员。"他指着这张截图，"`wechaty/wechaty`，一个对话式 RPA 的开源 SDK，两万两千多颗星、被复制过两千八百多次。句子互动就是这个项目的核心维护者。"

Wechaty 是我写的。一套代码接入多个 IM 平台，换个配置就换一个；有人用 Python、Go、Java 写了各自的版本；核心贡献者来自腾讯、Google、百度，一群素不相识的人在为同一个项目写代码。郭骐畅讲到这里引了我一句原话：程序员一定要做开源，这是毋庸置疑的。然后他说，所以今天每个概念我都不拿网上的例子，全用我们自己的项目给你看。

<img src="/img/posts/2026-06-22-highschool-intern-github/slides/slide-04.jpg" alt="PPT 页：一套代码，六行起一个聊天机器人。左边是 Wechaty 真实代码，右边讲跨平台接入、多语言 SDK、全球协作" class="full">

## Git 和 GitHub 是两回事

这是最容易混的两个词，他用两句话分清了：

**Git 是台时光机。** 给文字和代码做存档，每改一笔都记下来谁改的、什么时候、为什么，可以随时回看、回滚。

**GitHub 是把这台时光机搬上了云。** 让全世界在同一张蓝图上一起施工，谁改了什么、要不要采纳，全程留痕、能讨论、能撤回。

他还补了个冷知识：Git 是 Linux 之父 Linus 在 2005 年亲手写的，大概只花了十天。

<img src="/img/posts/2026-06-22-highschool-intern-github/slides/slide-05.jpg" alt="PPT 页：Git 是时光机，GitHub 是云上的工地。左右两栏分别解释 Git 和 GitHub" class="full">

## 怎么读懂一个项目主页

一个项目就是一个仓库，主页上信息很密。他对着 Wechaty 那张图，一个位置一个位置地指：

- **Star**（右上角）——人气和信任票，越高越被认可
- **Issues**——问题和需求区，相当于项目的客服台
- **Pull requests**——别人贡献代码的入口
- **License**——许可证，决定你能不能拿来商用
- **About**——那行标签，三十秒看懂它是干嘛的
- **README**——说明书，任何项目都先读它

<img src="/img/posts/2026-06-22-highschool-intern-github/slides/slide-07.jpg" alt="PPT 页：一个项目=一个仓库，这页全是信息。对着 Wechaty 仓库页逐个标注 Star、Issues、Pull requests、License、About、README" class="full">

"记住这六个位置，你打开任何一个陌生项目，都不会发懵。"

## Commit、Branch、Pull Request

三个高频词，他都给了一个生活里的对照。

**Commit，提交。** 每一次提交都带名字、时间和一句说明，像游戏的存档点，出了事能回到任意一刻。这就是版本控制。他翻出我们官网仓库这几天的提交记录，我和几个同学的名字都在里面；Wechaty 那个大项目，累计七千多次提交。

<img src="/img/posts/2026-06-22-highschool-intern-github/slides/slide-08.jpg" alt="PPT 页：每一次保存都带名字、时间和理由。配官网仓库这几天的真实提交记录" class="full">

**Branch，分支。** 想动大手术，不能在正在营业的主楼里砸墙——先开一个平行宇宙，在分支上安静地改，改好了再合并回主干。我们整版新官网上线走的就是这条线：拉一个 `stage-2` 分支做新版，做完一次性合回主干，用户全程无感。

<img src="/img/posts/2026-06-22-highschool-intern-github/slides/slide-09.jpg" alt="PPT 页：想动大手术？先开一个平行宇宙。用分支示意图讲 main 与 stage-2 的分叉与合并" class="full">

**Pull Request，合并请求。** 这是他花时间最多的一页。一句话：我改好了，请你看一眼再合并。流程五步——开分支、改、发 PR、别人 review、合并。

<img src="/img/posts/2026-06-22-highschool-intern-github/slides/slide-10.jpg" alt="PPT 页：我改好了，请你看一眼再合并。配官网仓库这几天的真实 PR 列表，CEO 和实习生的名字都在里面" class="full">

然后他放了一张图，是他自己的故事。

<img src="/img/posts/2026-06-22-highschool-intern-github/slides/slide-11.jpg" alt="PPT 页：不是每个 PR 都会合并，但好想法不会浪费。配 #9 号 PR 的真实页面，改动一千两百多行，最终被关闭" class="full">

"这是 #9 号 PR，我提的。一版把首页重做成 AI-native 的提案，改了一千两百多行。结果它被关掉了，没合并。"

他停了一下。"是不是白干了？不是。它提的那个方向——把 AI 当员工，而不是一堆功能——后来通过一连串新的 PR 真正上线了，成了今天的官网。所以 PR 是一场讨论，不是一道命令。提案被拒太正常了，但只要想法是好的，影响会留下来。别怕提。"

这话我没教他。一个刚工作的人，第一个大提案被关掉，能讲出这句，比讲对十个概念都难得。

## Star、Fork、Watch，还有 Issue 长什么样

剩下几个词他一句话带过：**Star** 是点赞收藏、给项目投票；**Fork** 是复制一份到自己名下随便改；**Watch** 是订阅，项目一更新就通知你。

Issue 他放了张真实的列表：

<img src="/img/posts/2026-06-22-highschool-intern-github/slides/slide-12.jpg" alt="PPT 页：Issue 是项目的客服台 + 需求池。配 Wechaty 真实 Issue 列表，并解释 Star、Fork、Watch" class="full">

"这是项目的客服台加需求池。你看，什么都有：官方公告、用户报 bug、有人提问、甚至有企业来谈采购。发现问题、提需求，都从开一条 Issue 开始。"

## 30 秒判断一个项目靠不靠谱

这是他讲的最实用的一段。以后搜到一个项目，看五个地方：

1. **Star 多不多**
2. **最近还在不在更新**（看最后一次提交日期）
3. **Issue 有没有人回**
4. **License 是什么**
5. **有没有现成的 Releases 能直接下**

<img src="/img/posts/2026-06-22-highschool-intern-github/slides/slide-13.jpg" alt="PPT 页：看五个地方，30 秒判断一个项目——Star、最近更新、Issue 响应、License、Releases" class="full">

"其实大多数人用 GitHub 的日常就一条线：搜项目、点 Releases、下载。你会判断，就已经赢过一大半人了。"

## 大公司为什么把看家代码免费送出去

最后他拔了一下视野，讲开源的逻辑。

"因为这是一门生意。把自己业务的配套品做成免费的——软件不要钱了，价值就流向它们真正握着的东西：数据、算力、平台标准。Google 送 TensorFlow、Meta 送 Llama，顺带还白嫖了全世界的人才和口碑。"

他引了 2023 年 Google 那份内部备忘录里的一句：我们没有护城河，开源正在吃掉我们的午餐。

<img src="/img/posts/2026-06-22-highschool-intern-github/slides/slide-15.jpg" alt="PPT 页：大公司为什么把看家代码免费送出去？讲开源作为生意的逻辑，和 MIT / Apache / GPL 三种许可证" class="full">

许可证他给了三句话记忆法：**MIT** 最宽松、**Apache** 多一层专利保护（Wechaty 用的就是它）、**GPL** 最严，你改了对外发布就得连源码一起开源。

## 散会就能做的五件事

他没让大家光听。结尾给了五个动作：

1. 注册，把 profile 填好，头像加一句简介——这是你的技术名片
2. 给 `wechaty/wechaty` 点个 Star
3. Follow 我和身边的同事
4. 去官网仓库提一条 Issue，发现哪儿有小毛病就记下来
5. 试着开个分支、提个小 PR，哪怕只改一个错别字

<img src="/img/posts/2026-06-22-highschool-intern-github/slides/slide-14.jpg" alt="PPT 页：散会后你今天就能做的 5 件事——完善 profile、给 wechaty 点 Star、Follow、提 Issue、提一个小 PR" class="full">

"第五件，是你从看客变成参与者的那一步。"

## 我为什么敢让一个高三生来讲

回到开头。两周前不知道 PR 是什么的人，今天给全公司讲了一堂 GitHub。中间发生了什么，我觉得值得说一下，因为这就是我现在带团队的方式。

我没有派人手把手教他。我做了三件事：给他一个真任务（重做官网），给他无限的 token，让他和另一个实习生赛马——同一个需求，两个人各做一版，谁的好上谁的。剩下的，他自己跟 Claude 一点点磨出来。从不会发 PR，到能给非技术同事把 PR 讲明白，他用了不到两周。

这事换三年前做不到。三年前一个高三毕业生想上手，得先啃命令行、配环境、被一堆术语劝退，光入门就够耗掉他的热情。现在工具变了，挡在"想做"和"做出来"之间的那堵墙，基本被 AI 推平了。剩下的门槛不是会不会写代码，是想不想做、敢不敢提。

所以我招人也跟着变了。我现在更看重的，是一个人面对一个不会的东西，会不会自己去问、去试、去交付，而不是他简历上已经会什么。郭骐畅这套讲稿里我最喜欢的，恰恰是那句不在技术点上的话：**PR 被拒太正常了，别怕提。**

他在讲稿最后引了我一句话，是我在一次访谈里说的：**加入字节最好的时间是 2016 年，加入句子互动最好的时间是今天。**这句话现在更想送给来面试的年轻人。GitHub 不是程序员的专利，开源也不是大神和老外的事——华人一直在这个舞台上，Vue 的尤雨溪、出圈的 DeepSeek，还有就在你身边的 Wechaty。

<img src="/img/posts/2026-06-22-highschool-intern-github/slides/slide-16.jpg" alt="PPT 收尾页：华人也在世界开源的舞台上，列尤雨溪、DeepSeek、Wechaty。引用——加入字节最好的时间是 2016 年，加入句子互动最好的时间是今天" class="full">

郭骐畅今年 18 岁。他和这个舞台之间，本来只隔一个账号。
