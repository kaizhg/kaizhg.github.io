---
title: Inflatable Patterner
year: 2023
summary: "Grasshopper C# development"
context: Pneuhaus
group: selected
position: 4
discipline: CD
legacy: https://kaizhang.io/inflatable-generator
cover: inflatable-patterner_cover.jpg
hover: inflatable-patterner_hover.mp4
---

# How to procedurally generate DMF file for inflatable structures?

...
June 2023 - August 2023 at [Pneuhaus](https://www.pneu.haus/) under guidance of August Lekrecke.

Over the 8 weeks, I developed C# scripts in Grasshopper for generating production files for inflatable structures. This workflow accelerates entire design process, from form-finding, patterning, labeling, unrolling, and simulation, adaptable to various input topologies and pattern types. It uses the half-edge data structure to enhance performance and robustness.

![](inflatable-patterner_01.jpg "Inflatable Structure example 1: Cloud Lights by Pneuhaus")

## **Solution 1: Closed Boundaries (2D Input)**

Turn almost any flat doodle drawing into manufacturable inflatable.

![](inflatable-patterner_02.jpg "Some input tests") | ![](inflatable-patterner_03.mp4 "Developable Panels")

The grasshopper definition enables users to freely modify the patterning design for aesthetic, structural, and manufacturing purposes. The segmentation count, length, width, seam alignment, and other parameters can all be easily adjusted based on the needs.

[gallery grid4] inflatable-patterner_04.jpg "1. Draw input boundaries" inflatable-patterner_05.jpg "2. Extract skeleton" inflatable-patterner_06.jpg "3. Construct mountain" inflatable-patterner_07.jpg "4. Get contours" inflatable-patterner_08.jpg "5. Triangular remesh" inflatable-patterner_09.jpg "6. Add volumne" inflatable-patterner_10.jpg "7. Subdivide and simulate inflation" inflatable-patterner_11.jpg "8. Finalize pattern"

![](inflatable-patterner_12.mp4 "360 View of the final panels")

[gallery grid3] inflatable-patterner_13.jpg inflatable-patterner_14.jpg inflatable-patterner_15.jpg inflatable-patterner_16.jpg inflatable-patterner_17.jpg inflatable-patterner_18.jpg

![](inflatable-patterner_19.jpg "Inflatable Structure example 2: Grove by Pneuhaus<br>")

## **Solution 2: Line Networks (3D Input)**

Turn almost any 3D line networks into manufacturable inflatables with a smoother output profile.

[gallery grid4] inflatable-patterner_20.mp4 inflatable-patterner_21.mp4 inflatable-patterner_22.mp4 inflatable-patterner_23.mp4 inflatable-patterner_24.mp4 inflatable-patterner_25.mp4 inflatable-patterner_26.mp4 inflatable-patterner_27.mp4 inflatable-patterner_28.mp4 inflatable-patterner_29.mp4 inflatable-patterner_30.mp4 inflatable-patterner_31.mp4 inflatable-patterner_32.mp4 inflatable-patterner_33.mp4 inflatable-patterner_34.mp4 inflatable-patterner_35.mp4 inflatable-patterner_36.mp4 inflatable-patterner_37.mp4 inflatable-patterner_38.mp4 inflatable-patterner_39.mp4

### Adaptive to Design / Manufacturing needs:

The below animation demonstrates the adjustable nature of the complex strip's width (highlighted in blue), while the simple strip's patterning (shown in grey) also automatically adapts to the width change. This feature, specifically requested by my advisor, introduces greater flexibility in fine-tuning design and fabrication processes.

![](inflatable-patterner_40.mp4)

### Assembly Guide I: Group Search

The diagram and animation above show the general steps and the mapping between 3D geometry and 2D flattened pieces. The GIF on the right serves as a group dictionary that shows the overall assembly sequence.

[gallery grid4] inflatable-patterner_41.jpg "1. Draw connect lines" inflatable-patterner_42.jpg "2. Thicken lines(Using Mesh Fattener or Multipipe by Daniel Piker)" inflatable-patterner_43.jpg "3. Dispatch complex(vertex valence > 4) and simple regions" inflatable-patterner_44.jpg "4. Divide regions into panels. The panels will be reconstructed as patch mesh for unroll purpose."

![](inflatable-patterner_45.mp4)

### Assembly Guide II: Neighbor Search

The diagram and animation below show the neighbor relationship and the example file of the cutting and plotting profiles. This feature assists fabricator to quickly index the neighbor pieces

[row 0.6 0.4]
![](inflatable-patterner_46.mp4)
|
[gallery stack] inflatable-patterner_47.jpg inflatable-patterner_48.jpg
[/row]

### **If you are interested in my thinking process, please take a look at the log[ HERE](https://kaizhg.notion.site/2023-Summer-Pneuhaus-Intern-Log-f12c62426d6a49c2ad19600da80ba9c7?pvs=74).**

![](inflatable-patterner_49.jpg "One example of the closed planar boundaries geometry - a cloud bubble.<br>")

### Below is another example of the first logic: CLOUD Pillow\
You can check the process on my [How to Make (almost) Anything](https://fab.cba.mit.edu/classes/863.23/Harvard/people/Kai/index.html#week_2) site.

![](inflatable-patterner_50.jpg)

[gallery grid4] inflatable-patterner_51.jpg inflatable-patterner_52.jpg inflatable-patterner_53.jpg inflatable-patterner_54.jpg

### ↑ : Perfect machine cutting\
↓ : Terrible human sewing

[gallery grid4] inflatable-patterner_55.jpg inflatable-patterner_56.jpg inflatable-patterner_57.jpg inflatable-patterner_58.jpg

[row 0.5933 0.4067]
![](inflatable-patterner_59.jpg "bad sewing execution --- but demonstrated the idea!")
|
![](inflatable-patterner_60.jpg "could be a cute and useless handcuff")
[/row]
