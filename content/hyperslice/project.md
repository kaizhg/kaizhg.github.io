---
title: HyperSlice                  # 标题
year: 2023                         # 年份（页面上的编号就是它）
summary: Image-interpolation-based 3D modeling workflow # 一句话类型，首页 tile 和列表里显示
group: selected                    # selected 或 archive
position: 6                        # 在所属组里排第几
discipline: CD                     # 旧分类，现在不显示，可忽略
legacy: https://kaizhang.io/hyperslice # 旧网站地址，仅备查
cover: hyperslice_cover.jpg        # 首页封面（32:25 裁切）
hover: hyperslice_hover.mp4        # 鼠标悬停时换成的图或循环视频
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

![](hyperslice_02.jpg) narrow-l

This project aims to integrate AI 2D-interpolation techniques into the 3D design process. It involves retrieving geometric sections from a specified slicing axis, and using an interpolation model to explore the latent space between the cross sections. {beside-r}

[gallery grid4] hyperslice_03.jpg hyperslice_04.jpg hyperslice_05.mp4 hyperslice_06.mp4

### Image Interpolation Matrix

By utilizing an M by N image matrix (M: total cross section count, N: interpolation in each layer), it empowers user to parametrically blend geometries using a customized curve. This approach enhances control and facilitates seamless integration of diverse geometries.

![](hyperslice_07.jpg) full

![](hyperslice_08.mp4) | ![](hyperslice_09.mp4)

### It's also possible to get cross-sections from a non-linear axis, and stack them back together to build a sub-form.

[gallery grid4 cols=4] hyperslice_10.mp4 "1. Input Geometry" hyperslice_11.mp4 "2. Non-linear Slicing Axis" hyperslice_12.mp4 "3. Cross-section" hyperslice_13.mp4 "4. Output Geometry"
