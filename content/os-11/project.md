---
title: Operating System 1.1        # 标题
year: 2024                         # 年份（页面上的编号就是它）
summary: Interactive installation  # 一句话类型，首页 tile 和列表里显示
group: selected                    # selected 或 archive
position: 2                        # 在所属组里排第几
discipline: IX                     # 旧分类，现在不显示，可忽略
legacy: https://kaizhang.io/os-11  # 旧网站地址，仅备查
cover: os-11_cover.jpg             # 首页封面（32:25 裁切）
hover: os-11_hover.jpg             # 鼠标悬停时换成的图或循环视频
hero: os-11_hero.jpg               # 项目页顶部大图；没有这行就用封面；inline = 顶部不放大图
credits_notes:                     # 不属于固定栏目的 credits 文字，一行一条
  - Harvard Graduate School of Design,
  - "Master in Design Studies: Open Project"
  - Operating System_1.1
  - Sarah Oppenheimer Instructor
  - Claire GlassTA
  - Team members (in the alphabetic order）
  - Alexia Asgari, Selin Dursun, Skye Gao, Danning Liang, Quincy Kuang, Kai Zhang
---

<!-- 使用说明（这段不会显示在网站上，可以删）
段落之间空一行。可以直接改：文字、图片文件名、先后顺序。_sheet.jpg 里有全部图片的缩略图和文件名。

  # 一句话                 整页大字 statement
  ## 标题 / ### 小标题      正文里的标题，后面的段落跟它一组
  [section] 文字           小字分节标签 + 分隔线
  ![](文件名)               一张图；后面加一个词指定宽度：full / wide-l / wide-r / half-l / half-r / narrow-l / narrow-r
                           再加 stagger = 比旁边那张往下错开；什么都不加 = 自动排
  ![](文件名 "说明")        图的说明文字（鼠标悬停显示）
  [![](文件名)](网址)       可点击的图
  ![](a.jpg) | ![](b.jpg)  两张并排，底边自动对齐
  [gallery cols=3] a b c   多图组，每行最多 3 张；[gallery carousel] = 轮播；[gallery stack] = 一张一行
  [video] 文件.mp4          带播放条的视频；![](文件.mp4) = 循环小动画
  [row 0.4 0.6] ... [/row] 多列，数字是列宽比例，列和列之间单独一行写 |
  段落末尾 {text-l}         文字固定在左栏（{text-r} 右栏）
  用 HTML 注释包起来         暂时隐藏，文件照留（和这段说明一样的写法）

不想管排版就把排版词删掉，自动规则会排。完整说明：docs/submitting-a-project.md
-->

## OS1.1: Architectural Knob

OS 1.1 harnesses the built infrastructure to extend our sensory registers. We have collaboratively designed an operating system: a lighting network linked by air. As mechanical wooden inputs are touched and turned, lighting outputs change and fluctuate. Manipulation of the physical apparatus directs sensory phenomena along new pathways.

![](os-11_01.jpg)

[video audio half-l] os-11_02.mp4

[video audio half-r] os-11_03.mp4

# With the "architectural knob" added, any column could be a control switch.

[gallery grid4 cols=3] os-11_04.jpg os-11_05.jpg os-11_06.jpg os-11_07.jpg os-11_08.jpg

### How does it work?

CNC wood + Hose clamp + Steel balls + DIY RGB Optical encoder

[row 0.375 0.625]
![](os-11_09.jpg "Exploded View")
|
![](os-11_10.jpg "Section view: One L-shape vinyl archway is first clamped on the column. Then the piece is clamped to the archway.")
[/row]

[gallery carousel] os-11_11.jpg os-11_12.jpg os-11_13.jpg

[video] os-11_14.mp4

[section] OS1.2: Universal through-hole, disassemble, optical rotary encoder

![](os-11_15.jpg) full

![](os-11_16.jpg) half-l

![](os-11_17.jpg) half-r stagger

[video audio] os-11_18.mp4
