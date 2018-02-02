---
title: Learn Rivescript
author: 李佳芮
avatar: /images/avatar.jpg
authorLink: 'https://www.botorange.com'
authorAbout: 'https://blog.botorange.com'
authorDesc: 一个现实的理想主义者
categories: chatbot
date: 2017-09-20 21:00 +0800
tags:
  - 聊天机器人
  - rivescript
keywords:
description: Study from rivescript and rivescript-js and write part of the doc as I prefered.  
photos:
  - /img/2017/learn-rivescript.png
---


Study from [rivescript](https://www.rivescript.com) and [rivescript-js](https://github.com/aichaos/rivescript-js) Write part of the doc as I prefered.    

Compare with Superscript, I prefer rivescript more for the following reason:
1. Doc is far more complete than superscript and has all kinds of examples.
2. Rivescript is more controllable than superscript. Superscript will do some random thing for more Intelligent.
3. Rivescript using Unicode to support Chinese wildcards and almost support all basic Chinese rules, which superscript cannot do.
4. Really simple, without MongoDB, while superscript has MongoDB built-in.

## Command

`+` Triggers

`-` Replies

`!` Definitions

`//` Comments

`%` Previous

`*` Conditionals

`^` Line Breaking

## Tags

### Tags has `<angled>` brackets

**Insert text in their place, or set a variable silently.**

#### `<@>`

#### `<star>`,` <star1>` - `<starN>`

These tags can not be used with `+ Trigger`

#### `<botstar>`, `<botstar1>` - `<botstarN>`

This tag is similar to `<star>`, but it captures wildcards present in a `% Previous` line. Here is an example:

```
+ i bought a new *
- Oh? What color is your new <star>?

+ (@colors)
% oh what color is your new *
- <star> is a pretty color for a <botstar>.
```

These tags can not be used with `+ Trigger`.

#### `<input>`, `<reply>`

The input and reply tags are used for showing previous messages sent by the user and the bot, respectively. The previous 9 messages and responses are stored, so you can use the tags `<input1>` through `<input9>`, or `<reply1>` through `<reply9>`to get a particular message or reply. `<input>` is an alias for `<input1>`, and `<reply>` is an alias for `<reply1>`.

```
// If the user repeats the bot's previous message
+ <reply>
- Don't repeat what I say.

// If the user keeps repeating themselves over and over.
+ <input1>
* <input1> == <input2> => That's the second time you've repeated yourself.
* <input1> == <input3> => If you repeat yourself again I'll stop talking.
* <input1> == <input4> => That's it. I'm not talking.{topic=sorry}
- Please don't repeat yourself.

// An example that uses both tags
+ why did you say that
- I said, "<reply>", because you said, "<input>".
```

#### `<id>`

This tag inserts the user's ID, which was passed in to the RiveScript interpreter when fetching a reply. With the interpreter shipped with the Perl RiveScript library, the `<id>` is, by default, `localuser`.

#### `<bot>`

The `<bot>` tag is used for retrieving a bot variable. It can also be used to set a bot variable.

```
+ what is your name
- You can call me <bot name>.

+ tell me about yourself
- I am <bot name>, a chatterbot written by <bot master>.

// Setting a bot variable dynamically
+ i hate you
- Aww! You've just ruined my day.<bot mood=depressed>
```

#### `<env>`

The `<env>` tag is used for retrieving global variables. It can also be used to set a global variable.

```
+ set debug mode (true|false)
* <id> == <bot master> => <env debug=<star>>Debug mode set to <star>.
- You're not my master.
```

#### `<get>`,`<set>`

#### `<add>`, `<sub>`, `<mult>`, `<div>`

```
+ give me 5 points
- <add points=5>You have been given 5 points. Your balance is: <get points>.
```

These tags can not be used with `+ Trigger`

#### `<@>`

equal to `{@ <star>}`

#### `<formal>`, `<sentence>`, `<uppercase>`, `<lowercase>`

#### `<call>`

### Tags have `{curly}`brackets 

**Modify the text around them.**

#### {random}

```
+ say something random
- This {random}message|sentence{/random} has a random word.
```

#### {weight}

```
+ greetings
- Hi there!{weight=20}
- Hello!{weight=25}
- Yos kyoco duckeb!
```

#### {@ <star>} / <@>

#### {topic}

#### {person}, <person>

#### {ok}

#### `\s` `\n`

## Line Breaking

```
+ tell me a poem
- Little Miss Muffit sat on her tuffet,\n
^ In a nonchalant sort of way.\n
^ With her forcefield around her,\n
^ The Spider, the bounder,\n
^ Is not in the picture today.
```

`\s`  space

`\n` line break

## Definitions

- ! local concat = newline | space | none （"file scoped"）
- ! version = 2.0
- ! var name = Tutorial
- ! global debug = true
- ! global depth = 50
- ! person i am = you are

## rivescript brain

start from `begin.rive`— contains some configuration settings for your bot's brain.

- const
- variables— bot variables
- Substitutions: *always lowercased*
- array
- global
- person

## Trigger

### catch-all wildcards

```
+ my name is *
- Nice to meet you, <star1>!

+ * told me to say *
- Why would <star1> tell you to say "<star2>"?
- Did you say "<star2>" after <star1> told you to?

+ i am * years old
- A lot of people are <star1> years old.
```

### special wildcards

- `#` only match a number
- `_` only match a word with no numbers or spaces

### Alternatives and Optionals

#### alternatives

```
+ what is your (home|office|cell) number
- You can reach me at: 1 (800) 555-1234.

+ i am (really|very|super) tired
- I'm sorry to hear that you are <star> tired.

+ i (like|love) the color *
- What a coincidence! I <star1> that color too!
- I also have a soft spot for the color <star2>!
- Really? I <star1> the color <star2> too!
- Oh I <star1> <star2> too!
```

#### optionals

```
+ how [are] you
- I'm great, you?

+ what is your (home|office|cell) [phone] number
- You can reach me at: 1 (800) 555-1234.

+ i have a [red|green|blue] car
- I bet you like your car a lot.
```

```
+ [*] the machine [*]
- How do you know about the machine!?
```

use `[*]` optionals to ignore parts of a message by putting it before or after your trigger instead of on both sides.

### Arrays in triggers

```
// Single word array items
! array colors = red blue green yellow

// Multiple word items
! array blues = light blue|dark blue|medium blue

// A lot of colors!
! array colors = red blue green yellow orange cyan fuchsia magenta
^ light red|dark red|light blue|dark blue|light yellow|dark yellow
^ light orange|dark orange|light cyan|dark cyan|light fuchsia
^ dark fuchsia|light magenta|dark magenta
^ black gray white silver
^ light gray|dark gray
```

```
+ what color is my (@colors) *
- Your <star2> is <star1>, silly!
- Do I look dumb to you? It's <star1>!

+ i am wearing a (@colors) shirt
- Do you really like <star>?
```

```
// Without parenthesis, the array doesn't go into a <star> tag.
+ what color is my @colors *
- I don't know what color your <star> is.
```

```
// Arrays in an optional
- i just bought a [@colors] *
- Is that your first <star>?
```

### priority triggers

Default: triggers with more words are tested first

This is useful to "hand tune" how well a trigger matches the user's message.

```
+ google *
- Google search: <a href="http://google.com/search?q=<star>">Click Here</a>

+ * perl script
- You need Perl to run a Perl script.
```

What if somebody asked the bot, "google write perl script"? They might expect the bot to provide them with a Google search link, but instead the bot replies talking about needing Perl. This is because "* perl script" has more words than "google *", and therefore would usually be a better match.

```
+ google *{weight=10}
- Google search: <a href="http://google.com/search?q=<star>">Click Here</a>

+ * perl script
- You need Perl to run a Perl script.
```

## Redirections

### use outside the reply

```
+ hello
- Hi there!
- Hey!
- Howdy!

+ hey
@ hello

+ hi
@ hello
```

### use inside the reply

`{@ <star>}` will redirect to `*` reply

```
+ * or something{weight=100}
- Or something. {@ <star>}
```

shortcut of `{@ <star>}`  is `<@>`

```
+ hello *
- {@ hello} <@>

+ hello
- Hi there!

+ are you a bot
- How did you know I'm a machine?
```

## % Previous

use `%` to make a short discussion

`% Previous` lines need to be lowercased just like triggers do.

```
+ knock knock
- Who's there?

+ *
% who is there
- <star> who?

+ *
% * who
- LOL! <star>! That's funny!
```



## Learning Things

`<set>` & `<get>`

```
+ my name is *
- <set name=<star>>It's nice to meet you, <get name>.

+ what is my name
- Your name is <get name>, silly!

+ i am # years old
- <set age=<star>>I will remember that you are <get age> years old.

+ how old am i
- You are <get age> years old.
```

retrieve variables from `begin.rive`

```
// The user can ask the bot its name too!
+ what is your name
- You can call me <bot name>.
- My name is <bot name>.

+ how old are you
- I am <bot age> years old.
```

The `<formal>` tag is a shortcut for `{formal}<star>{/formal}`

```
// Store the name with the correct casing
+ my name is *
- <set name=<formal>>Nice to meet you, <get name>!
```

## Writing Conditionals

```
+ what is my name
* <get name> == undefined => You never told me your name.
- Your name is <get name>, silly!
- Aren't you <get name>?
```

```
+ my name is *
* <formal>   == <bot name> => Wow, we have the same name!<set name=<formal>>
* <get name> == undefined  => <set name=<formal>>Nice to meet you!
- <set oldname=<get name>><set name=<formal>>
^ I thought your name was <get oldname>?
```

Constions:

```
==  equal to
eq  equal to (alias)
!=  not equal to
ne  not equal to (alias)
<>  not equal to (alias)
```

```
<   less than
<=  less than or equal to
>   greater than
>=  greater than or equal to
```

## Labeled sections 

begin with `>` and end with `<`

### Topic

```
+ i hate you
- You're really mean! I'm not talking again until you apologize.{topic=sorry}

> topic sorry

  // This will match if the word "sorry" exists ANYWHERE in their message
  + [*] sorry [*]
  - It's OK, I'll forgive you!{topic=random}

  + *
  - Nope, not until you apologize.
  - Say you're sorry!
  - Apologize!

< topic
```

Also, you can use `<set topic=random>` instead, but there is a small difference in how the two tags will behave:

The `<set>` tag can appear multiple times in a reply and each one is processed in order. The `{topic}` tag can only appear once (if there are multiple ones, the first one wins). So, they'll both do the same job, but `{topic}` is a little shorter to type.

### ??? 没看懂 The begin block

### Object Macros

