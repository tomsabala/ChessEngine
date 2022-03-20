# ChessEngine
## general Info.
I've started this project as a place to be challenged in, after I've been exposed to this kind of project.
For sources I took help from two kind of articles:
1) [A step-by-step guide to building a simple chess AI](https://www.freecodecamp.org/news/simple-chess-ai-step-by-step-1d55a9266977/)
2) [Writing a chess program in one day](https://andreasstckl.medium.com/writing-a-chess-program-in-one-day-30daff4610ec)

and of course the wiki chess programming page:
https://www.chessprogramming.org/Main_Page

## Implementaion:
I used python with two main packages:   
- numpy
- pygame 

I ran into a guy who used this package GUI for the same project exect, so I took help from his code guide building the interface and it was defenatlly a kick for the start.
You visit his youtube channel at this link: https://www.youtube.com/channel/UCaEohRz5bPHywGBwmR18Qww

p.s In the next step i would like to move to a more comfturble GUI workframe.

## TODO
At current point, the engine able to play one on one game and allows the player choose the opponents level rank from 0 to 4
where -0- replies a randome player, -1- one step forward computing engine, ... , -4- four steps computing ahead.

My next steps would be:
1) changing engine computing implementation, so he won't stop thinking between each turn.
2) reboosting algorithm to be more efficient.
3) add strategies to engine evaluation position method.
4) add annimation and more detailed interface.
