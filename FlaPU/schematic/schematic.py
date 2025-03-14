from mcschematic import MCSchematic, Version

from .schematic_exception import SchematicException


def place_instruction(instruction: str, x: int, y: int, z: int, schematic: MCSchematic, facing: str) -> None:
    if len(instruction) != 16:
        raise SchematicException(f"Instruction : {instruction} is not long of 16 characters.")

    for i, bit in enumerate(instruction):
        if bit == "1":
            schematic.setBlock((x, y, z), f'minecraft:repeater[facing={facing}]')
        elif bit == "0":
            schematic.setBlock((x, y, z), 'minecraft:purple_wool')
        else:
            raise SchematicException(f"Instruction : {instruction} does not only contain '1' or '0'.")

        y -= 2

        if i == (len(instruction) // 2) - 1:
            y -= 2


def load_machine_code(file_path: str, max_instructions: int) -> list[str]:
    with open(file_path, "r") as f:
        machine_code: list[str] = [line.strip() for line in f.readlines()]

    if len(machine_code) > max_instructions:
        raise SchematicException(f"File : {file_path} contains more than {max_instructions} instructions.")

    while len(machine_code) != max_instructions:
        machine_code.append("0000000000000000")

    return machine_code


def place_instruction_and_handle_exception(instruction: str,
                                           final_x: int,
                                           y: int,
                                           final_z: int,
                                           schematic: MCSchematic,
                                           facing: str,
                                           instruction_line: int):
    try:
        place_instruction(instruction, final_x, y, final_z, schematic, facing)
    except SchematicException as e:
        new_message: str = f"{str(e)} (line {instruction_line + 1})"
        raise SchematicException(new_message) from e


def determine_side_and_facing(address: int, total_instructions: int) -> tuple[bool, str, int]:
    half_instructions: int = total_instructions // 2
    quarter_instructions: int = total_instructions // 4
    three_quarters_instructions: int = quarter_instructions * 3

    facing: str = "north" if address < half_instructions else "south"
    facing_offset: int = 2 if address >= half_instructions else 0
    if quarter_instructions <= address < half_instructions or address >= three_quarters_instructions:
        return True, facing, facing_offset
    return False, facing, facing_offset


def calculate_x_offset(index: int, x_offset_stagger: int) -> int:
    return (index // 16) % 16 * 2 + x_offset_stagger


def update_stagger(side: bool, x_offset_stagger: int) -> int:
    if x_offset_stagger in {1, -1}:
        return 0
    return 1 if not side else -1


def create_schematic(max_instructions: int, machine_code_file_path: str, schem_file_path: str) -> None:
    schematic = MCSchematic()
    machine_code = load_machine_code(machine_code_file_path, max_instructions)

    start_x, y, start_z = -33, -1, 4
    x_other_side_pos: int = 3
    z, x_offset_stagger = start_z, 0
    z_distance_instructions = 7

    for i, instruction in enumerate(machine_code):
        is_other_side, facing, z_facing_offset = determine_side_and_facing(i, max_instructions)
        x = x_other_side_pos if is_other_side else start_x
        final_x = x + calculate_x_offset(i, x_offset_stagger)
        final_z = z + z_facing_offset

        place_instruction_and_handle_exception(instruction, final_x, y, final_z, schematic, facing, i + 1)

        z += z_distance_instructions
        x_offset_stagger = update_stagger(is_other_side, x_offset_stagger)

        if (i + 1) % 16 == 0:
            z = start_z

    schematic.save('.', schem_file_path, version=Version.JE_1_18_2)
