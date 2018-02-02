---
title: ChatBot Framework-Wechaty
author: 李佳芮
avatar: /images/avatar.jpg
authorLink: 'https://www.botorange.com'
authorAbout: 'https://blog.botorange.com'
authorDesc: 一个现实的理想主义者
categories: project
date: 2016-10-01 14:26:08
tags:
  - wechaty
keywords:
description: Wechaty is a easy to use ChatBot Framework which can help you write the worlds smallest chatbot. Maybe you are very interesting in ChatBot industory, or you just want to get your own wechat personal account robot, Wechaty will always be your friend.
photos:
  - /img/2016/wechaty-logo.png
---
![Wechaty Logo][wechaty-logo-image]

Hello, ChatBot Developers!

Wechaty is a easy to use **ChatBot Framework** which can help you write **the worlds smallest chatbot**. Maybe you are very interesting in ChatBot industory, or you just want to get your own wechat personal account robot, Wechaty will always be your friend.

Visit Wechaty Github: <https://github.com/chatie/wechaty>
Visit Wechaty Blog: <http://blog.chatie.io/>

In this video, I will show you how to getting started with Wechaty through a 10 minutes live coding tutorial, with Wechaty Docker Runtime. (Event Node.js Party #18, Beijing)

For visiters come from China who can not visit YouTube.com, this video is also hosted on YouKu.com & Tencent Video

<div class="video-container" style="
    position: relative;
    padding-bottom:56.25%;
    padding-top:30px;
    height:0;
    overflow:hidden;
">
<iframe width="560" height="315" src="https://www.youtube.com/embed/IUDuxHaV9bQ?start=85" frameborder="0" allowfullscreen="" style="
    position: absolute;
    top:0;
    left:0;
    width:100%;
    height:100%;
"></iframe></div>

* [Getting Started with Wechaty @ YouKu](http://v.youku.com/v_show/id_XMTkyNDgzMjY5Ng==.html)
* [Getting Started with Wechaty @ Tencent](https://v.qq.com/x/page/b0363p9kg3q.html)

Learn more about how to use Wechaty: <https://github.com/wechaty/wechaty/wiki/GettingStarted>

Code in the video:

```typescript

import {Wechaty, Room} from 'wechaty'

const bot = Wechaty.instance()

bot
.on('scan', (url, code)=>{
    let loginUrl = url.replace('qrcode', 'l')
    require('qrcode-terminal').generate(loginUrl)
    console.log(url)
})

.on('login', user=>{
    console.log(`${user} login`)
})

.on('friend', async function (contact, request){
    if(request){
        await request.accept()
        console.log(`Contact: ${contact.name()} send request ${request.hello}`)
    }
})

.on('message', async function(m){
    const contact = m.from()
    const content = m.content()
    const room = m.room()

    if(room){
        console.log(`Room: ${room.topic()} Contact: ${contact.name()} Content: ${content}`)
    } else{
        console.log(`Contact: ${contact.name()} Content: ${content}`)
    }

    if(m.self()){
        return
    }

    if(/hello/.test(content)){
        m.say("hello how are you")
    }

    if(/room/.test(content)){
        let keyroom = await Room.find({topic: "test"})
        if(keyroom){
            await keyroom.add(contact)
            await keyroom.say("welcome!", contact)
        }
    }

    if(/out/.test(content)){
        let keyroom = await Room.find({topic: "test"})
        if(keyroom){
            await keyroom.say("Remove from the room", contact)
            await keyroom.del(contact)
        }
    }
})

.init()

```

docker command:    

```
docker run -ti --volume="$(pwd)":/bot --rm zixia/wechaty mybot.ts
```
[Click here to get the repo](https://github.com/lijiarui/Getting-Started-with-Wechaty---Live-Coding-Tutorial "Click here to get the repo")

[wechaty-logo-image]: https://raw.githubusercontent.com/Chatie/wechaty/master/docs/images/wechaty-logo-en.png
