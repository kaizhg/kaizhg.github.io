---
title: See/Saw
year: 2023
summary: 1D balancing game and controller
group: selected
position: 7
discipline: IX
legacy: https://kaizhang.io/seesaw
cover: seesaw_cover.jpg
hover: seesaw_hover.jpg
hero: seesaw_hero.jpg
credits:
  Course: Interaction Intelligence, Spring 2023
  Instructor: Marcelo Coelho
  Duration: 4 Weeks
  Team: Kai Zhang, Tatiana Estrina
---

## How to make a simple '1D' game that encourages physical collaborations?

See Saw is a one-dimensional game that encourages collaboration between two players who share a single controller. As they slide along the rail, the players must maintain balance and overcome growing challenges. The project involves both software and hardware development. The game is coded within the p5js environment and receives data from Arduino via a serial port. This page will concentrate on the hardware design process.

![](seesaw_hero.jpg) full

![](seesaw_01.jpg) half-l

![](seesaw_02.jpg) half-r stagger

[section] How to play

[gallery grid3] seesaw_03.jpg "Each player controls one block. Tilt the handle to move." seesaw_04.jpg "The size represents weight. The heavier the longer." seesaw_05.jpg "Similar to a see-saw, it tilts! Try to balance it."

[gallery grid3] seesaw_06.jpg "1/3:The block bounces back when it hits another block" seesaw_07.jpg "2/3:The block bounces back when it hits another block" seesaw_08.jpg "3/3:The block bounces back when it hits another block"

[section] Controller development

![](seesaw_09.png "Iteration Process") full

[row 0.705 0.295]
![](seesaw_10.jpg)
|
### First iteration: see-saw

The initial controller simply merged a conventional game controller with a see-saw. While the interaction was natural, it failed to foster collaboration---players only use their individual controllers to play the game.
[/row]

[row 0.3 0.7]
### Second iteration: cross

To promote physical interaction, we combined two see-saws into a cross-shaped controller. This distinctive design encourages players to engage with each other's bodies, adding an extra element of fun. However, the basic cardboard prototype restricts independent movement for players.
|
![](seesaw_11.jpg)
[/row]

[row]
[video audio] seesaw_12.mp4
|
[video audio] seesaw_13.mp4
[/row]

### Third and fourth iteration: free rotation

The solution to the movement problem was to introduce an extra degree of freedom. The third prototype effectively used a rod and a slightly larger hole, but it lacked a polished look and feel. To elevate the user experience, I added two bearings on each handle, resulting in smoother rotation and a premium feel. You can clearly tell the difference when you grab it in your hands.

![](seesaw_14.jpg) half-r

Thanks to the cross-shaped design, the electronic components are straightforward, requiring only one joystick and an Arduino board. The joystick's X value corresponds to Player 1's acceleration, while the Y value corresponds to Player 2's acceleration.

![](seesaw_15.jpg) wide-l

[youtube start=7] https://www.youtube.com/watch?v=kxqCKvFvQow

![](seesaw_16.jpg) small-l
