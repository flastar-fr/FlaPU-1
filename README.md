# FlaPU
This project is an assembler and a schematic creator for a computer I've made in Minecraft following the 
[MattBatwings tutorial](https://youtube.com/playlist?list=PL5LiOvrbVo8nPTtdXAdSmDWzu85zzdgRT&si=a6HbzOcxNyvRuehc).
This project uses the exact same instruction set, the exact same instruction memory 
(however you could need to rotate the generated instructions if you want to use it in the original model from MattBatwings).

The assembler program support almost every feature from the original version except hexadecimal values 
and defining a definition after using it. I will probably at that later. Tell me if I forgot something else.


## How to use it ?
You have to put your .as file into ``asm_programs`` folder and the outputed schematic will be in ``schem_programs``.

You have 3 options :
1. You modify directly the default program name in the code and execute the file ``__main__.py``
2. You can launch a small menu with the command ``python __main__.py -m`` which will prompt you to enter a program name
3. You can directly pass the program name like this ``python __main__.py program_name``

Important notes :
- You must NOT put the .as extension in the program name. It will take it automatically.
- To make the schematic creator works you will need the [mcschematic library](https://github.com/Sloimayyy/mcschematic).

## World download ?
You have access to the schematic of my computer in this repo.

As you can see, all components come from the original BatPU-2  
(except register file and control ROM which I chose to keep the simpler version from the video) 
so there is nothing groundbreaking.
I just made the connectivity following the videos (may some part could change a bit, but it doesn't matter much).

For me, it was just a project to understand how computers work more than how to build a computer in Minecraft, 
so I decided to copy the already made components (which I took the time to understand the redstone behind) to go faster.

I'm already thinking for a second version which will be all made by myself. 
From the specs choice to the components.