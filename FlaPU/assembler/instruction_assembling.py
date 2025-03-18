from .config import assembled_name, instructions_address_bits, chars
from .instruction_parser import is_number


def assemble_reg_imm(name: str, operands: list[str]) -> str:
    base_instruction_assembled: str = assembled_name[name]
    binary_operand_receive: str = get_register_binary(operands[0])
    binary_operand_value: str = get_assembled_immediate(operands[1], 8)
    assembled_line: str = f"{base_instruction_assembled}{binary_operand_receive}{binary_operand_value}"

    return assembled_line


def assemble_reg3(name: str, operands: list[str]) -> str:
    base_instruction_assembled: str = assembled_name[name]

    assembled_line: str = base_instruction_assembled
    for register in operands:
        binary_register: str = get_register_binary(register)
        assembled_line += binary_register

    return assembled_line

def assemble_address(name: str, operands: list[str]) -> str:
    base_instruction_assembled: str = assembled_name[name]
    binary_address_value: str = convert_int_to_binary(int(operands[0]))
    binary_operand_value_normalized: str = normalize_length(binary_address_value, instructions_address_bits)
    assembled_line: str = f"{base_instruction_assembled}00{binary_operand_value_normalized}"

    return assembled_line


def assemble_reg2_imm_opt(name: str, operands: list[str]) -> str:
    max_amount_operands_needed: int = 3

    base_instruction_assembled: str = assembled_name[name]

    assembled_line: str = base_instruction_assembled
    assembled_line += get_register_binary(operands[0])
    assembled_line += get_register_binary(operands[1])
    if len(operands) == max_amount_operands_needed:
        assembled_line += get_assembled_immediate(operands[2], 4, True)
    else:
        assembled_line += "0000"

    return assembled_line


def assemble_no_operand(name: str) -> str:
    return f"{assembled_name[name]}000000000000"


def normalize_length(to_normalize: str, size_to_get: int) -> str:
    return "0" * (size_to_get - len(to_normalize)) +  to_normalize


def extract_int_register(register_name: str) -> int:
    return int(register_name[1:])


def convert_int_to_binary(value: int) -> str:
    return bin(value)[2:]


def get_register_binary(register_name: str) -> str:
    register_number = extract_int_register(register_name)
    binary_register_number = convert_int_to_binary(register_number)

    return normalize_length(binary_register_number, 4)


def get_assembled_immediate(immediate_value: str, amount_bits: int, signed: bool = False) -> str:
    if is_number(immediate_value, True):
        int_operand_value: int = int(immediate_value)
    else:
        int_operand_value: int = chars[immediate_value[1:2].upper()]

    if signed and int_operand_value < 0:
        return format(int_operand_value & (2**amount_bits - 1), f'0{amount_bits}b')

    binary_operand_value: str = convert_int_to_binary(int_operand_value)

    return normalize_length(binary_operand_value, amount_bits)
