# Dorothy

# Warning!!!

#由于作者已经数个月没有更新他的代码了，所以该项目在目前最新的Nonebot上是无法正常运行的。其次，代码中的有关epd等字样的代码是我在调试一块外接显示屏时使用的厂家提供的第三方库，没有考虑到在一般情况下运行时的问题，总之是非常抱歉。

## 介绍

为了给日益变得无聊的群组带来一些生气而诞生的简单机器人。

>### 她能做什么？

~~伟大的计算机学者们一般称这种状态为*WIP(Work In Progress)*

#### 复读

当群友连续发送同一条信息超过3次时，Dorothy重复该信息，并且记录下来。

#### 复读榜

发送一个记录了哪些语句被复读了最多次的榜单。

#### 俄罗斯轮盘禁言赌

首次输入指令rr和参数1~5作为子弹数目，之后输入rr开始，如果Dorothy没有禁言资格则无法禁言。

#### 显示状态 (superuser)

发送status获取运行情况简报。

#### 天气查询

经典模块，接入了和风天气的API，返回当时天气和空气状况（如果有），范围为全球，南极洲也行（

#### 以图搜图

接入了SauceNAO的pixiv搜图API，发送”搜图“和一张图片搜索。

#### 一堆其他接口 (at me)

一言，嘴臭，彩虹屁狂夸，朋友圈文案，nbnhhsh。

## 关于

本项目的名称来源是我十分喜爱的一个赛博朋克风的文字游戏，*VA-11 Hall-A* 中的一名机器人角色 , Dorothy Haze ~~我甚至还给这游戏写过明日方舟云联动同人发到B站上去了（不建议看）~~。

十分感谢 [Richard Chien](https://github.com/richardchien) 大大和 [NoneBot2](https://github.com/nonebot/nonebot2)。

## 实现

本项目是利用了 *go-cqhttp* 项目和 *nonebot2* 和Jetbrains的Pycharm开发的，是在酷q离去后的选择。

python3.7以上才可以运行，需要的包除了nb-cli外还有就是ujson。

## 后记

2020/12
我还不是很熟悉版本管理以及开源协议等方面的知识，还在努力自学中。

---

<div align=center><img src="https://github.com/QingWen45/Dorothy/blob/master/images/Dorothy.png"/></div>


心血来潮给项目画了个像素画，绘于2020年12月6日。




