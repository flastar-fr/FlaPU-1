import os
import sys

from argparse import ArgumentError

from assembler.assembler import Assembler
from schematic.schematic import create_schematic


default_program: str = "test"

asm_folder: str = "asm_programs"
mc_folder: str = "mc_programs"
schem_folder: str = "schem_programs"



def launch_program(program_name: str) -> None:
    full_as_file: str = f"{os.path.join(asm_folder, program_name)}.as"
    full_mc_file: str = f"{os.path.join(mc_folder, program_name)}.mc"
    full_schem_file: str = os.path.join(schem_folder, program_name)

    if not os.path.exists(full_as_file):
        raise FileNotFoundError(f"The file {full_as_file} does not exist.")

    assembler = Assembler(16)
    assembler.assemble_file(full_as_file, full_mc_file)
    create_schematic(1024, full_mc_file, full_schem_file)


def launch_menu() -> None:
    program_name: str = input("Enter a program name : ")
    launch_program(program_name)


if __name__ == '__main__':
    match len(sys.argv):
        case 1:
            launch_program(default_program)
        case 2:
            if sys.argv[1] == "-m":
                launch_menu()
            else:
                launch_program(sys.argv[1])
        case _:
            raise ArgumentError(None, "Invalid argument")
