---
title: Prismo                      # 标题
year: 2022                         # 年份（页面上的编号就是它）
summary: Transformable lamp        # 一句话类型，首页 tile 和列表里显示
group: selected                    # selected 或 archive
position: 8                        # 在所属组里排第几
discipline: ID                     # 旧分类，现在不显示，可忽略
legacy: https://kaizhang.io/prismo # 旧网站地址，仅备查
cover: prismo_cover.jpg            # 首页封面（32:25 裁切）
hover: prismo_hover.mp4            # 鼠标悬停时换成的图或循环视频
credits:                           # 显示在标题下方，有哪项写哪项，可整段删掉
  Course: SCI-6476 Transformable Design Methods
  Instructor: Chuck Hoberman
  Duration: 6 Weeks
  Team: Kai Zhang, Quincy Kuang, Danning Liang
  Thanks: Youtian Duan(Welding), Liu Yang(Assembly)
  Role:
    - "[1] Proposed the innovative concept of combining mirror and prismatic structures to create a transformable lighting solution."
    - "[2] Conducted research into both design directions and developed a Grasshopper C# script to streamline the design and simulation process for the team."
    - "[3] Defined the aesthetic and specifications of the final product."
    - "[4] Worked closely with two other team members to address the challenges in the actuation, lighting, and connection design."
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

# What will an "Inside-Out" kaleidoscope look like?

Prismo lamp is a modern interpretation of the classic prismatic structure, leveraging its periodic and space-filling properties to create a unique, kinetic aesthetic. {text-l}

[row 0.645 0.355]
### Initial Inspiration

I was first intrigued by the prismatic structure’s movement. The mesmerizing yet unexpected movement makes me wonder how will light bounces inside this structure. A whim suddenly hit me: Why don’t combine periscope and prismatic structure and make an "inside-out kaleidoscope", using prismatic transformation to amplify light?
|
![](prismo_02.mp4)
[/row]

![](prismo_03.jpg) wide-r

[row 0.24 0.76]
![](prismo_04.mp4)
|
[video audio] prismo_05.mp4
[/row]

[gallery grid4] prismo_06.jpg prismo_07.jpg prismo_08.jpg prismo_09.jpg

### Base Geometry

The first step was to identify the optimal base geometry. The geometry needed to be tessellatable, and we explored several options including the Truncated Rhombic Dodecahedron, the Rhombic Dodecahedron, and the Prismatic Polyhedron.\
We chose the basic Prismatic Polyhedron with 1 degree of freedom (DOF) for the following reasons: given our limited time and resources, a 1 DOF structure was easier to actuate, allowing us to focus more on design refinements rather than technical challenges; the 1 DOF structure was more straightforward for audiences to understand, as people tend to appreciate things they can easily grasp. {text-l}

![](prismo_10.jpg) half-l

We explored two Y-Shape Polyhedron-based designs: a polar tree and a tessellation structure. The latter was chosen for best highlighting movement through its smart, space-filling mechanics.

[gallery grid4] prismo_11.mp4 prismo_12.mp4 prismo_13.mp4 prismo_14.mp4

[row 0.375 0.625]
### Parametric Design

I wrote a C# grasshopper script to streamline the design and simulation process for 1 DOF prismatic structures, greatly improving our ability to iterate and refine the design in a timely manner.\
\
\
**[Click here to see how I improved the workflow in details](/transform) >>>**
|
![](prismo_15.mp4)
[/row]

![](prismo_16.jpg) | ![](prismo_17.jpg)

### Actuation


The lamp’s movement is driven by the actuation of its base parallelogram. By fixing one side of the parallelogram to the base, we were able to drive the whole structure by actuating the non-fixed side using a servo motor.

[gallery grid3] prismo_18.mp4 prismo_19.mp4 prismo_20.mp4

### Connection and Material

This was also one of the main challenges of realizing this product. There were three major factors: weight, reflectivity, and connection type:

[1] Since the whole structure is only driven by a single 35 kg servo motor, the main body of the top moving part has to be as light as possible.\
[2] The inside material should be reflective enough for light to bounce multiple times. We found out the more light gets bounced the better the kaleidoscope effect it gets.\
[3] The gap between each panel should be as small as possible to avoid light escape, and the connection should have as little friction as possible to ensure a smooth movement.

The acrylic mirror has the most reflective surface. However, hinges and fasteners are required for connecting laser cut mirror panel. There are mainly three drawbacks of using hinges and fasteners: 1. The assembly process, which requires fastening more than 1000 screws/rivets by hand, is extremely tedious and not flexible enough for maintenance and placing LED strip; 2. Hinge requires leaving huge gap between panels to avoid self-interference; 3. The lamp doesn’t look clean with this many fasteners exposed.\
Taken all consideration, we decided to 3D print the panel because we were able to integrate mechanical hinge into the individual panel.

[gallery grid3] prismo_21.jpg prismo_22.jpg prismo_23.jpg prismo_24.jpg prismo_25.jpg prismo_26.jpg prismo_27.jpg prismo_28.jpg prismo_29.jpg

[row 0.34 0.66]
### Panel and Base

The panels of the lamp are fabricated through SLS printing which resulted in a clean black matte finish. Given the short time frame, we didn’t fully optimize the panel but there is space for shrinking the edge and acquiring a sleeker look. The movement of the panels is enabled through mechanical hinges which are integrated into the panel designs.

The first panel, which is the fixed side of the base parallelogram, is integrated into the base. We spitted the base in halves to clamp the stand as well as to create space for placing the circuit board.
|
[gallery] prismo_30.png prismo_31.png
[/row]

[section] Fabrication

[gallery grid3] prismo_32.jpg prismo_33.jpg prismo_34.jpg prismo_35.jpg prismo_36.jpg prismo_37.jpg prismo_38.jpg prismo_39.jpg prismo_40.jpg

[video @1-5] prismo_41.mp4

![](prismo_42.jpg "Following studies and tests") @6-13 low

[section] Final Product

![](prismo_01.jpg) wide-l

![](prismo_43.jpg) | ![](prismo_44.jpg)

[row 0.625 0.375]
![](prismo_45.jpg)
|
![](prismo_46.jpg)
[/row]

[video half-l] prismo_47.mp4

[video half-r] prismo_48.mp4

[gallery grid3] prismo_49.jpg prismo_50.jpg prismo_51.jpg
