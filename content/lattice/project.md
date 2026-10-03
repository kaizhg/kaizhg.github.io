---
title: Lattice++                   # 标题
year: 2025                         # 年份（页面上的编号就是它）
summary: Conformal lattice generator for Grasshopper # 一句话类型，首页 tile 和列表里显示
group: selected                    # selected 或 archive
position: 1                        # 在所属组里排第几
discipline: CD                     # 旧分类，现在不显示，可忽略
cover: lattice_cover.jpg           # 首页封面（32:25 裁切）
hover: lattice_hover.jpg           # 鼠标悬停时换成的图或循环视频
hero: lattice_03_saddle-front.jpg  # 项目页顶部大图；没有这行就用封面；inline = 顶部不放大图
password: bounce                   # 访问密码：页面内容会用它加密，删掉这行就不加锁
credits:                           # 显示在标题下方，有哪项写哪项，可整段删掉
  Tools: Rhino, Grasshopper, Custom Python Script, TetGen
  Role:
    - Built the whole pipeline alone: point seeding, tetrahedralization, surface extraction, cell typing, and strut generation.
    - Designed the cell-transition scheme that lets one part carry several lattice types without seams.
    - Modeled the application studies: bicycle saddle and headphone earpads.
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

# What if the parts that touch the body were grown to fit it?

Lattice++ is a lattice generation system I built inside Grasshopper, taking Carbon's Design Engine as the reference. Give it any closed geometry and it fills the volume with a conformal lattice: tetrahedral, hexahedral, or Voronoi cells, at a chosen density and strut thickness. Density, thickness, and even the cell type can change gradually across one part. It is a design tool, not yet a simulation tool. But the shapes it makes are the shapes that could one day be tuned to a person's own pressure map.

[section] The tool

![](lattice_19_slide-tool-goal.jpg "Any closed geometry in; struts, nodes, and a printable mesh out.") | ![](lattice_18_slide-seven-types.jpg "Seven cell families on the same torus: tetrahedral, rhombic, icosahedral, Voronoi, kagome, star, Kelvin.")

### How it works

The tool builds on two kinds of grid. **The hexahedral grid** is the simple one: a cube, extruded, gridded, or lofted through the volume, with the same unit cell repeated inside and the cells at the boundary cut to the shape. It is regular and predictable, but it only approximates the surface.

![](lattice_22_slide-hex-torus.jpg "Hexahedral grid on a torus.") | ![](lattice_21_slide-hex-cells.jpg "Hex cells built by extrusion, grid, or loft, with the same star cell inside.")

**The tetrahedral grid** is what makes the lattice conformal. Points are seeded at a controllable density, and TetGen, called from a C# component, fills the volume with well-shaped tetrahedra. The outer faces of that mesh are extracted, so the lattice follows the input surface exactly. {text-l}

![](lattice_20_slide-tetgen-wip.jpg "An early tetrahedralization: usable, but with a few small and distorted cells near the boundary.") | ![](lattice_15_tetgen-workflow.jpg "TetGen inside Grasshopper: the tetrahedralization step, before and after refinement.")

Cell types are assigned per vertex rather than per cell, so a transition happens inside a cell, not between cells. That is what lets one part carry several lattice types without a seam. {text-l}

![](lattice_23_slide-transition-cell.jpg "Each vertex of a tetrahedron carries a cell type, or a mix of types. The cell between them blends.") | ![](lattice_24_slide-zones-wip.jpg "Assigning cell types per node in a custom script, next to the brute-force zoning a native component gives.")

![](lattice_25_slide-zone-icosa-tetra.jpg "Zone transition: icosahedral to tetrahedral.") | ![](lattice_26_slide-zone-voronoi.jpg "Zone transition: Voronoi.")

### Three gradients

Density follows the point seeding, so it can thin out where a part needs to be light and tighten where it needs support. Strut thickness is a per-edge value and can follow any field. Cell type is the unusual one: because types live on vertices, a part can go from a stiff Kelvin cell to a soft Voronoi cell continuously.

[section] Studies

A saddle and a pair of earpads: two places where a body meets a product and a single foam density is always a compromise. {text-l}

![](lattice_04_saddle-front-frame.jpg "Saddle on its rails. Hover to see the lattice alone.") half-l hover=lattice_03_saddle-front.jpg

![](lattice_06_saddle-bottom-frame.jpg "From below: the lattice opens up where nothing bears on it.") half-r stagger hover=lattice_05_saddle-bottom.jpg

### Earpads

An earpad has to be soft against the head, breathable, and still hold its shape around the driver. One lattice can do all three if it is allowed to change across the pad. {text-l}

![](lattice_30_slide-headphones.jpg "Kelvin and Voronoi earpads on the same headphone.") wide-r

The skin of a generated lattice is a design surface in its own right. Its pattern can be drawn from a key visual element or an IP: this earpad takes the Sheikah emblem from The Legend of Zelda: Breath of the Wild as its motif. {text-l}

![](lattice_14_zelda-pattern.jpg "The Sheikah emblem, redrawn as a lattice pattern.") | ![](lattice_17_headphones-zelda.jpg "The pattern carried on the earpad.")

[row]
[gallery carousel every=3] lattice_07_ring-a.png "Lattice surface skin, design 1 of 5" lattice_08_ring-b.png "Lattice surface skin, design 2 of 5" lattice_09_ring-c.png "Lattice surface skin, design 3 of 5" lattice_10_ring-d.png "Lattice surface skin, design 4 of 5" lattice_11_ring-e.png "Lattice surface skin, design 5 of 5"
|
![](lattice_31_slide-earpad-surfaces.jpg "Printed surface, fabric over print, or exposed mesh.")
[/row]

[section] What it is not, yet

[row @1-9]
![](lattice_16_comfort-map.jpg "Softer to stiffer, mapped onto the head. The data is illustrative.")
|
![](lattice_12_hex-cell-morph.mp4 "One hexahedral unit cell, morphing between types.")
[/row]

Whether the grid is hexahedral or tetrahedral, every unit cell is a parameter: its type, its size, and its strut thickness can be tuned to human-factors data, pressure, heat, fit. The Grasshopper workflow does not simulate yet; it designs. The data has to come from somewhere else, and that is exactly where a close collaboration with a human-factors team would begin: their measurements in, a cushion generated for one person out. {text-l}
