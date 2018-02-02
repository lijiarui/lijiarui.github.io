---
title: 产品分享|如何做一个用户喜欢的chatbot
author: 李佳芮
avatar: /images/avatar.jpg
authorLink: 'https://www.botorange.com'
authorAbout: 'https://blog.botorange.com'
authorDesc: 一个现实的理想主义者
categories: chatbot
date: 2017-03-30 11:10:36
tags: 
  - 产品
  - 聊天机器人
keywords:
description: chatbot和会话式交互已经不是一个新名词了，可以预见的是，随着技术的发展，聊天机器人即将会推动一场颠覆性的行业创新。
photos:
  - /img/2017/how-to-build-a-chatbot-cover.jpg
---

![如何做一个用户喜欢的chatbot-1](/img/2017/how-to-build-a-chatbot-cover.jpg)

chatbot行业的依然存在着大量的泡沫，但有一点我们不得不承认，未来新的会话式交互正在颠覆整个科技行业。chatbot和会话式交互已经不是一个新名词了，可以预见的是，随着技术的发展，聊天机器人即将会推动一场颠覆性的行业创新。所有的主流巨头公司都在为丰富多样的对话形式搭建底层框架。

去年发生了这些里程碑事件：
– Facebook Messenger 全面开放给开发者
– Apple iOS message apps 出现了
– Slack, Kik, Telegram, 和 Skype 开始支持机器人接入

同时，巨头还在积极为开发者搭建各类ai相关的工具
– Facebook 推出了 Wit.ai7
– Google 推出了 Cloud Natural Language API
– Microsoft 推出了 Bot Framework– IBM 推出了 Watson Conversation API

这些公司的入场预示着聊天机器人行业的一轮新的洗牌，这不禁让我想起，10年前，Apple 推出了app store，大量的app迅速涌入。然而只有很少的一部分有较高的用户留存。如今，bot的市场和当初的app是非常相似的。

产品希望从场景切入为C端用户提供服务，这样的bot应该是什么样子的呢？
首先，我们分析下bot面临的两个重大挑战

**1. 获取用户**

在和身边非技术同学的聊天中发现，90%的人都不知道chatbot是什么，这不禁让我想起了移动应用（app）刚刚出现的情景——当应用市场的雏形出现的时候，很多人经过很长时间才明白了什么是app。然而现在，如果你连Pokémon Go 是什么都不知道的话，大家可能会觉得你是个外星人了。

但是即使你‘了解’chatbot，也很难找到bot应用进行体验。Product Hunt(https://www.producthunt.com/) 和 Botlist(https://botlist.co/) 可以帮开发者导一些流量，他们是类似于豌豆荚或者应用宝这样的应用商店，我们也可以称他们为bot store，虽然这些store 可以帮助开发者带来一些用户，而bot真正的流量来源还是主流的社交平台。Slack, Kik, Telegram 和 Skype 都拥有各自的bot store。Facebook Messenger  甚至会在搜索联系人的时候推荐一些bot。虽然我们并不清楚Messenger 是按照什么规则推荐bot的，但是可以确认的一点是，那些足够幸运的，可以在Facebook中搜索到的bot 通过messenger的巨大流量迅速获取到了大量的用户。

下图是一些当前主流的bot store截图：
![如何做一个用户喜欢的chatbot-2](/img/2017/how-to-build-a-chatbot-botlist.png)

![如何做一个用户喜欢的chatbot-3](/img/2017/how-to-build-a-chatbot-product-hunt.png)


我有一种的直觉，在未来的bot 应用中，群消息机器人将会改变行业的规则（虽然Messenger现在还不支持，但是从国内社群运营的概念已经火了几年了，而且，社群运营中真正和chatbot相关的非营销类的场景还没有被挖掘出来）。

毕竟，老用户的推荐是获取新用户最好的方式，如果在一个群聊中开启了一个机器人，之前不了解这个bot的人会立刻和他产生互动，迅速实现飞速的用户增长。

恩，所以我在此给我自己打个广告。。我是专门做微信群自动化运营的服务提供商。
åç
**2. 用户留存**

和获取用户同样具有挑战的是如何在产品中留住用户。用户回来继续使用bot并积极参与是有原因的。开发者可以通过定期发推送来召回用户，而最好的方式还是应该还是bot的产品本身，究竟有哪些核心功能能吸引他们回来，常见的方式有签到，月/周的订阅等。

按理说，与app相比，bot用户的获取成本相对较低。只需要发送一条消息就体验bot产品了，这远比让用户从app store上下载一个app要容易的多。当然，这同样存在另外一个问题，很多用户可能只是好奇的来体验一下，他们用过一次之后就不会再回来了。

那么，什么样的bot可以克服这些问题呢？

**1. 游戏类bot**

“再来一次我就可以完成了。。。” ‘使人上瘾的bot’ 会持续吸引用户的注意力并让用户想要的更多。这些bot自称有极高的用户活跃度，当然，也应该是这样的。

Trivia Blast

![如何做一个用户喜欢的chatbot-4](/img/2017/how-to-build-a-chatbot-trivia-blast.png)

Trivia Blast(https://www.facebook.com/triviablast1/) 是一个非常有意思，快速提问问题的机器人，他提供各种各样的问题，答对以后会得分升级，问题类别包括音乐、科学、体育、历史、电影等等。这个bot有用一个全球积分榜，你可以看到你的好友、以及你同一个城市、同一个国家甚至全世界的人的排名，并和他们进行分数比拼。由于Trivia Blast 是一个智力游戏，所以即使你长时间沉溺在这个游戏中也不会有很深的负罪感。

Swelly

![如何做一个用户喜欢的chatbot-5](/img/2017/how-to-build-a-chatbot-swelly.png)

Swelly(https://www.facebook.com/swell.bot) 是另外一个一旦你玩起来就会上瘾的bot，Swelly 通过直接向用户提问来帮助用户做一些日常的决定。你可以为别人的选择投票，比如’我应该用什么头像呢？’ 或者’我今天应该穿什么鞋？’ 你可以发表你自己的问题或者只是帮助其他人做决定。我不得不说，随机帮助一些人做决定是一件很酷的事情。

**2. 习惯养成类bot**

习惯养成类bot 的核心功能就是召回用户。

Joy

![如何做一个用户喜欢的chatbot-6](/img/2017/how-to-build-a-chatbot-joy.png)

Joy(http://www.hellojoy.ai/) 追踪你的心情并让你的心智更加健康。他会每天或者每周对你进行检查并告诉你现在的感受。Joy会记录你所有的想法并会生成情绪报告，如果检测到你的情绪低落，它甚至会提供一些减压的互动。我很喜欢这个bot，未来也许他会在日常生活中让你随时心情愉悦。

**3. 效率类bot**

现阶段，这类bot一般都在在slack team 中提高团队的协作能力，也有一小部分是面向普通用户的，比如下面这个应用。

Sourcing Bot

![如何做一个用户喜欢的chatbot-7](/img/2017/how-to-build-a-chatbot-trivia-blast-sourcing-bot.png)

[Source Bot](https://www.facebook.com/itoutsourcingbot/) 帮助用户迅速找到需要的开发者和团队，使用bot向用户收集信息，他们现在有合作的276家外包公司提供服务。

写在最后：

在botlist上我们可以看到bot的分类有很多，包括分析工具、交流、设计、开发工具、教育、娱乐、文件管理、视频、游戏、健康、新闻、市场、旅游、运动、购物。。。。。等等，而每个bot的访问量并不是很多，平均在100-300之间，几个很有名的bot也不过是10k左右，面向用户场景的bot设计仍然有很大挑战，但是我相信，这是一个正在增长的市场，当你找到很好的场景并不断打磨你的bot产品，你就会做出一个用户喜欢的chatbot。

最后，祝所有做chatbot的产品经理们找到场景，切入痛点，实现产品从0到1 ^-^。

本文内容纯属原创，转载请注明，图片都是我用sketch一点点拼的，内容也是一点点码的，所以不要直接盗取我的内容啦。
