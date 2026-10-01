# 项目内容怎么改：`content/` 文件夹

网站的全部内容都在 `site/content/` 里，一个项目一个文件夹，名字就是网址里的 slug：

```
content/prismo/
  project.md          这个项目的全部文字和排版
  prismo_cover.jpg    首页封面（按 32:25 裁切，主体放中间）
  prismo_hover.mp4    鼠标悬停时的第二张（图或循环视频，可选）
  prismo_hero.jpg     项目页顶部大图（可选，不写就用封面）
  prismo_01.jpg       正文媒体，按出现顺序编号
  prismo_02.png       透明背景用 PNG
  prismo_07.mp4       视频（同名 .jpg 是它的封面帧）
  _sheet.jpg          所有文件的缩略图一览，带文件名，方便我们对话时指图
```

**改文字**：直接改 `project.md`，存盘。
**换图 / 加图**：把文件放进文件夹（名字照编号规则，或者随便起名也行，只要 md 里写对），在 md 里引用。
**新项目**：复制一个文件夹改名，改 `project.md`，放图。
**删项目**：删文件夹。
**边改边看**：双击 `Website_Portfolio/编辑网站.command`（或在 site 目录里跑 `npm run edit`），它会打开 http://127.0.0.1:4321 ，之后每次存盘 `project.md`，浏览器两三秒内自动刷新；写法有错会在那个窗口里用红字告诉你是哪一行。关掉窗口就退出。
改满意了告诉我一声，我看一眼、上线。

图片 ≤ 2400px 长边、≤ 5 MB；视频 ≤ 1080p、尽量 ≤ 30 MB。文件名只用小写字母、数字、横线、下划线。

## project.md 怎么写

```markdown
---
title: Prismo
year: 2022
summary: Transformable lamp        # 一句话，首页 tile 和列表显示
context: Harvard GSD               # 可选，显示为 "@ Harvard GSD"
group: selected                    # selected 或 archive
position: 8                        # 在所属组里排第几
cover: prismo_cover.jpg
hover: prismo_hover.mp4
hero: prismo_hero.jpg              # 可选；写 inline 表示顶部不放大图
link: https://example.com          # 可选，顶部大图点击跳转
credits:                           # 可选，有哪项写哪项，会显示在标题下方
  Course: SCI-6476 Transformable Design Methods
  Instructor: Chuck Hoberman
  Team: A, B, C
  Role:
    - Proposed the concept
    - Wrote the Grasshopper C# tool
---

# What will an "Inside-Out" kaleidoscope look like?

一个井号是 statement，整页大字，全站样式统一。

开头这一段会放在标题右边，作为导语。

![](prismo_01.jpg)

一张图单独一行，排版自动。想指定位置，在图后面加一个词：

![](prismo_02.jpg) half-l

![](prismo_03.jpg "图的说明，鼠标悬停时显示") wide-r

[![](prismo_04.jpg)](https://example.com) | ![](prismo_05.jpg)

图外面套一层 `[ ](网址)` 就是可点击的图。

两张图用 ` | ` 隔开写在同一行，就并排，底边自动对齐。

## 小节标题

两个井号是正文里的标题，三个井号小一级。标题后面的段落属于同一块，会一起排。

段落之间空一行。想在段落里强制换行，在行尾放一个反斜杠 \
像这样。

[section] Fabrication

`[section]` 是一行小字标签加分隔线，用来分章节。

[gallery cols=3] prismo_06.jpg prismo_07.jpg prismo_08.jpg prismo_09.jpg "这张有说明" prismo_10.jpg
[gallery carousel] prismo_11.jpg prismo_12.jpg prismo_13.jpg
[video] prismo_14.mp4
[youtube start=7] https://www.youtube.com/watch?v=kxqCKvFvQow
![](prismo_15.mp4)

[row 0.4 0.6]
### 左边是一段文字
右边是图。`[row]` 里每一列用单独一行 `|` 隔开，数字是列宽比例，不写就均分。
|
![](prismo_16.jpg)
[/row]
```

## 排版词（都可选）

| 写法 | 效果 |
|---|---|
| `full` | 整宽 |
| `wide-l` `wide-r` `wide-c` | 三分之二宽，靠左 / 右 / 居中 |
| `half-l` `half-r` | 一半宽 |
| `narrow-l` `narrow-r` | 五分之二宽 |
| `small-l` `small-r` | 三分之一宽 |
| 后面再加 `stagger` | 比旁边那张往下错开一截 |
| `@3-7` | 精确指定占第 3 到第 7 列（页面分 12 列），想放哪就放哪 |
| 两张并排的单图 | 自动等高、底边对齐（形状差太多的除外） |
| 段落末尾 `{text-r low}` | 文字和旁边的图底边对齐 |
| 点任何图 | 放大查看，← → 翻页，Esc 关闭（自动有） |
| `w=320` | 把图限制在 320px 宽（logo 之类的小图用） |

**自由拼贴 `[cluster]`**：照片在纵向上交错，像贴在墙上。每张写列范围 `@a-b`，`y=` 是从顶部往下的格数（一格 ≈ 半个列宽），不写就是 0；高度按照片比例自动算。

```markdown
[cluster]
![](a.jpg) @1-5
![](b.jpg) @6-10 y=3
![](c.jpg) @1-5 y=9
[/cluster]
```
（A 在左上，B 在右边、比 A 低三格，C 在 A 下面、和 B 的下半段并排。）

**开场两栏 `[row 0.65 0.35 spread]`**：左栏第一块（logo）贴顶、其余文字贴到右栏图片的底边，右栏放图。用在项目页开头，标题下面。
| 段落末尾加 `{text-l}` 或 `{text-r}` | 文字固定在左 / 右栏 |
| `[gallery]` 后加 `cols=N` | 每行最多几张；比例不同的图自动按等高行排，相同的排网格 |
| `[gallery stack]` | 一张一行、整宽 |
| `[gallery carousel]` | 轮播 |
| `![](x.mp4)` | 循环播放的小动画（GIF 请先转 mp4，或直接给我 GIF 我来转） |
| `[video]` | 带播放条的视频；`[video audio]` 表示有声音 |

暂时不想显示的内容，用 `<!-- 这里 -->` 包起来就会被跳过，文件还留着。

不确定就什么都不写。自动规则：图靠左，段落贴到图旁边，连续三张照片自动成一组，连续四张白底图自动两列。

## 文件夹之外

- 顺序：改 `position`。Selected 和 Archive 各自从 1 数。
- 关于页、首页那句话、Life band 的词：还是找我改，它们不在 content 里。
- 不要动 `src/` 里的 json，那是从 md 生成的，下次生成会覆盖。
