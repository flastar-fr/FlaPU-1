# FlaPU
This project is an assembler and a schematic creator for a computer I've made in Minecraft following the 
[MattBatwings tutorial](https://youtube.com/playlist?list=PL5LiOvrbVo8nPTtdXAdSmDWzu85zzdgRT&si=a6HbzOcxNyvRuehc).
This project uses the exact same instruction set, the exact same instruction memory 
(however you could need to rotate the generated instructions if you want to use it in the original model from MattBatwings).


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
A world download for my version of the computer will probably be dropped here when I will have finished to clean up everything, 
and I'm already thinking about a 2nd version for later.
