---
title: Large Language Objects
year: 2023
summary: Physical interface design for LLMs
context: MIT HAN Lab
group: selected
position: 3
discipline: IX
legacy: https://kaizhang.io/large-language-objects
cover: large-language-objects_cover.jpg
hover: large-language-objects_hover.jpg
hero: large-language-objects_hero.jpg
---

# **Engaging with Large Language Models through Tangible Experiences:**

[section] Part I: AIncense

![](large-language-objects_01.jpg)

### ▲\
Harnessing the power of traditional rituals for the emerging technologies.\
▼

![](large-language-objects_02.jpg)

### AIncense is a praying device powered by ChatGPT, designed to amplify self-motivation through psychological suggestion.

AIncense integrates the comprehensive capabilities of ChatGPT to revolutionize and expand our perception of religious authority. This innovative platform empowers users to foster a routine of self-empowerment and inspiration. Whether making a wish, confessing, or navigating daily life, AIncense provides a unique space for personal reflection and growth.

[row 0.6917 0.3083]
![](large-language-objects_03.jpg)
|
![](large-language-objects_04.jpg)
[/row]

![](large-language-objects_05.jpg) wide-l

[youtube] https://www.youtube.com/watch?v=9Aasryk0lOA

[row]
### AIncense 2.0 (Locally deployed LLM)

In Fall 2024, I had a chance to revisit this project, and made a hardware design that truly enables this interaction. With the support from MIT HAN Lab, I was able to make a smart incense that locally communicates with Large Language. Please click the following links to see detail for the 2nd Iteration:

### **[>>> Overview](https://fab.cba.mit.edu/classes/863.23/Harvard/people/Kai/index.html#final)**\
**[>>> Process Documentation](https://fab.cba.mit.edu/classes/863.23/Harvard/people/Kai/index.html#final_tracking)**
|
![](large-language-objects_06.jpg)
[/row]

[gallery grid3] large-language-objects_07.jpg large-language-objects_08.jpg

![](large-language-objects_09.jpg) wide-r

![](large-language-objects_10.jpg "Incense PCB Iterations") half-l

### Part II: MIT HAN Lab Local Voice Assistant

[row 0.645 0.355]
![](large-language-objects_11.mp4)
|
### A modular design for edge computing

This device envisions how modularity works for edge computing hardware. The base computing module is powered by Nvidia Jetson Orin Nano, while the top module could be easily changed according to the need. Here presents a speakerphone module as example.\
\
The client and technical support for this project is MIT HAN Lab, founded by Professor Song Han. HAN lab stands at the forefront of cutting-edge research, encompassing a wide spectrum of topics from LLM and genAI to TinyML and hardware design.
[/row]

[row]
### Technology

This voice assistant and TinyChat computer uses the TinyChatEngine software from MIT HAN Lab. It runs Meta's latest LLaMA-2 model at 30 tokens / second on NVIDIA Jetson Orin Nano and can easily support different models and hardware. For more details on the software side please visit MIT HAN Lab. All of Tinychat computer's hardware are custom designed except the keys. We wanted to craft the most compact interface for portability and personalization
|
![](large-language-objects_12.jpg)
[/row]

[row 0.535 0.465]
![](large-language-objects_13.jpg)
|
### Design Decision:\
Off-the-shelf speaker module

Some design decisions were made as we (Spatial Dynamics, a local industrial design consultancy studio who commissioned me for this project) only had one week to deliver the prototype.

For instance, we disassembled an existing speakerphone product from Amazon, and integrated the speakerphone unit into our design. Although using existing component raised certain limitations, this saved us quiet a lot time from building the hardware from scratch.
[/row]

[row]
![](large-language-objects_14.jpg)
|
![](large-language-objects_15.jpg)
[/row]

Due to time constraint, we decided to use SLS / FDM print for the prototypes, and use an external usb-c cable to power and communicate with the speakerphone unit.

[section] Part III: Tiny Chat Computer

...
For: MIT HAN Lab\
Project team: Quincy Kuang, Lingdong Huang, Kai Zhang, MIT HAN Lab {credits}

[row 0.61 0.39]
![](large-language-objects_16.jpg)
|
### Private personal computing

This integration enables powerful technologies to operate locally, fortifying the safeguarding of personal privacy. "TinyChat" emerges as a pioneering project to explore this very concept. We crafted the TinyChat computer with a design reminiscent of classic computers, both as a tribute to the original idea of a "personal computer" and as a reminder of their historical aesthetics. This raises an interesting query: as AI software evolves, might it also transform the physical form of computers themselves?
[/row]

![](large-language-objects_17.jpg)

[row 0.315 0.685]
All of TinyChat computer's hardware are custom designed except the keys. We wanted to craft the most compact interface for portability, personalization, and of course, the ultimate retro look.
|
![](large-language-objects_18.jpg)
[/row]

[video audio] large-language-objects_19.mp4
