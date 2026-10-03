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
credits:                           # 显示在标题下方，有哪项写哪项，可整段删掉
  Tools: Rhino, Grasshopper (C#), TetGen
  Reference: Carbon Design Engine
  Status: Design tool, 2025 – ongoing
  Role:
    - Built the whole pipeline alone: point seeding, tetrahedralization, surface extraction, cell typing, and strut generation.
    - Designed the cell-transition scheme that lets one part carry several lattice types without seams.
    - Modeled the application studies: bicycle saddle, VR headset gasket, headphone earpads.
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

# What if a cushion could be grown to fit the body that sits on it?

Lattice++ is a lattice generation system I built inside Grasshopper, taking Carbon's Design Engine as the reference. Give it any closed geometry and it fills the volume with a conformal lattice: tetrahedral, hexahedral, or Voronoi cells, at a chosen density and strut thickness. Density, thickness, and even the cell type can change gradually across one part. It is a design tool, not yet a simulation tool. But the shapes it makes are the shapes that could one day be tuned to a person's own pressure map.

[section] The tool

![](lattice_19_slide-tool-goal.jpg "Any closed geometry in; struts, nodes, and a printable mesh out.") wide-c

![](lattice_18_slide-seven-types.jpg "Seven cell families on the same torus: tetrahedral, rhombic, icosahedral, Voronoi, kagome, star, Kelvin.") full

### How it works

Four problems had to be solved for the tool to work on an arbitrary shape. Seeding points at a controllable density, and filling the volume with well-shaped tetrahedra, are both handled by TetGen, called from a C# component. The outer faces of the tetrahedral mesh are extracted so the lattice follows the input surface exactly. Cell types are assigned per vertex rather than per cell, so a transition happens inside a cell, not between cells.

![](lattice_15_tetgen-workflow.jpg "TetGen inside Grasshopper: the tetrahedralization step, before and after refinement.") | ![](lattice_20_slide-tetgen-wip.jpg "An early tetrahedralization: usable, but with a few small and distorted cells near the boundary.")

![](lattice_23_slide-transition-cell.jpg "Each vertex of a tetrahedron carries a cell type, or a mix of types. The cell between them blends.") wide-l

### Three gradients

Density follows the point seeding, so it can thin out where a part needs to be light and tighten where it needs support. Strut thickness is a per-edge value and can follow any field. Cell type is the unusual one: because types live on vertices, a part can go from a stiff Kelvin cell to a soft Voronoi cell continuously.

[gallery grid5] lattice_07_ring-a.png "Same ring, five lattices." lattice_08_ring-b.png lattice_09_ring-c.png lattice_10_ring-d.png lattice_11_ring-e.png

![](lattice_12_hex-cell-morph.mp4) small-l

One hexagonal unit cell, morphing between types. The transition is what lets zones meet without a seam. {text-r low}

![](lattice_25_slide-zone-icosa-tetra.jpg "Zone transition: icosahedral to tetrahedral.") | ![](lattice_26_slide-zone-voronoi.jpg "Zone transition: Voronoi.")

![](lattice_24_slide-zones-wip.jpg "Assigning cell types per node in a custom script, next to the brute-force zoning a native component gives.") wide-c

![](lattice_22_slide-hex-torus.jpg "Hexahedral grid on a torus.") | ![](lattice_21_slide-hex-cells.jpg "Hex cells built by extrusion, grid, or loft, with the same star cell inside.")

[section] Studies

A saddle, a headset gasket, and a pair of earpads: three places where a body meets a product and a single foam density is always a compromise.

[gallery grid3] lattice_03_saddle-front.jpg "Saddle, front." lattice_01_saddle-side.jpg "Saddle, side." lattice_05_saddle-bottom.jpg "Saddle, bottom."

[gallery grid3] lattice_04_saddle-front-frame.jpg "With the rails." lattice_02_saddle-side-frame.jpg lattice_06_saddle-bottom-frame.jpg

![](lattice_27_slide-vr-gasket.jpg "VR headset gasket: icosahedral where it bears on the face, tetrahedral where it only needs to hold shape.") full

![](lattice_28_slide-gasket-variants.jpg "The same gasket in Voronoi, BCC, and icosahedral + tetrahedral.") | ![](lattice_29_slide-gasket-heatmap.jpg "Lattice only on the underside, where pressure concentrates, keeping the outside clean.")

![](lattice_30_slide-headphones.jpg "Earpads in Kelvin and Voronoi cells.") wide-l

![](lattice_31_slide-earpad-surfaces.jpg "Printed surface, fabric over print, or exposed mesh.") | ![](lattice_32_slide-micro-texture.jpg "A micro texture on the inner wall, sized to the frequencies it should damp.")

![](lattice_17_headphones-zelda.jpg "Because the lattice is generated, a pattern or a logo can be written into its skin.") | ![](lattice_14_zelda-pattern.jpg)

![](lattice_13_g-regions.jpg "Regions of a lattice carrying a letterform.") wide-c

[section] What it is not, yet

![](lattice_16_comfort-map.jpg "Softer to stiffer, mapped onto the head. The data is illustrative.") half-l

The tool generates; it does not simulate. There is no stiffness model behind the gradients yet, so the choice of where to soften and where to stiffen is still the designer's. The next step is obvious: take a pressure map from a real body, in a saddle, a headset, or a pair of earpads, and let it drive density and cell type directly. Then a cushion would be generated for one person, rather than for an average of everyone. {text-r low}
