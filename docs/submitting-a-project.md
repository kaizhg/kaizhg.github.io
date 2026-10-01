# 投稿格式：怎么给网站加一个新项目

把一个文件夹丢进 `Website_Portfolio/asset/_inbox/`，告诉我一声，我导入、排版、给你看，你说上线就上线。
改已有项目也一样：建同名文件夹，只放要换的东西和一个 `project.md`，写清楚改哪里。

## 文件夹长这样

```
asset/_inbox/barnacle-lamp/
  project.md            项目信息 + 正文（下面有模板）
  cover.jpg             首页封面。会按 32:25 裁切，主体放中间
  hover.jpg             鼠标悬停时的第二张（可选，可以是 .gif）
  01.jpg                正文图，按出现顺序编号
  02.png                透明背景用 PNG
  03.gif                动图会自动转成循环视频
  04.mp4                视频
```

图片不用自己缩，但请 ≤ 2400px 长边、单张 ≤ 5 MB；视频 ≤ 1080p、尽量 ≤ 30 MB。
文件名只用小写字母、数字、横线。

## project.md 模板

```markdown
---
title: Barnacle Lamp
year: 2024
summary: Transformable lamp          # 一句话，首页 tile 和列表里显示
context: OPT Industries              # 可选，显示为 "@ OPT Industries"
group: selected                      # selected 或 archive
position: 3                          # 可选，在 Selected 里排第几
credits:                             # 可选，有哪项写哪项
  Course: Design Studio
  Instructor: Jane Doe
  Team: A, B, C
  Role: Hardware, firmware
  Thanks: Someone
---

# How to procedurally generate DMF files for inflatable structures?

开头这一段会放在标题右边，作为导语。两三句就够。

![](01.jpg)

一张图单独一行，排版自动。想指定大小，在图后面加一个词：

![](02.jpg) wide

可用的词：full（整宽）、wide、half、narrow。不写就是自动。

![](03.jpg) ![](04.jpg)

两张图写在同一行，就并排，底边会自动对齐。

caption: 图的说明文字，紧跟在图的下一行，鼠标悬停时显示。

## 小节标题

两个井号是小节标题，会显示成一行小字加分隔线。

> 一句引用式的大字，整页统一样式

[gallery cols=3] 05.jpg 06.jpg 07.jpg 08.jpg 09.jpg
[carousel] 10.jpg 11.jpg 12.jpg
[video] 13.mp4
[youtube] https://www.youtube.com/watch?v=xxxx
```

## 规则就这几条

- 图片默认靠左，段落会自动贴到旁边的图右侧。
- `[gallery]` 里图片比例不同时，自动按原网站那种"每行等高、整行铺满"排；比例相同就是整齐网格。`cols` 是每行最多几张。
- `[carousel]` 一次显示一张，自动播放，带左右箭头。
- 标题用 `#`，正文直接写，链接用 `[文字](网址)`。
- 不确定的就别写排版词，自动规则通常是对的，不对我再调。

## 之后的流程

1. 你：文件夹放好，在聊天里说"新项目 barnacle-lamp 放进 inbox 了"。
2. 我：导入、跑排版、在本地给你看截图或链接。
3. 你：看完说改哪里，或者直接说上线。
4. 我：推上去，两分钟后在 kaizhg.github.io 生效。
