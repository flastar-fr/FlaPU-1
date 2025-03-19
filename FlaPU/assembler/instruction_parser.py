from .config import instructions_address_bits, registers_bits, chars

from .exceptions.immediate_value_exception import ImmediateOperandsException
from .exceptions.register_operands_exception import RegisterOperandsException


def split_instruction_line(line: str) -> list[str]:
    stripped_line: str = line.strip()

    tokens: list[str] = stripped_line.split()
    final_tokens: list[str] = []

    i = 0
    while i < len(tokens):
        token: str = tokens[i]
        if token not in {"'", '"'}:
            final_tokens.append(token)
        else:
            final_tokens.append("' '")
            i += 1

        i += 1

    return final_tokens


def parse_labels(instructions: list[str],
                 labels_table: dict[str, int],
                 labels_addresses: dict[str, list[int]]) -> tuple[dict[str, int], dict[str, list[int]]]:
    for address, instruction in enumerate(instructions):
        tokens: list[str] = split_instruction_line(instruction)

        parse_labels_line(tokens, labels_table, labels_addresses, address)

    return labels_table, labels_addresses


def parse_labels_line(tokens: list[str], labels_table: dict[str, int], labels_addresses: dict[str, list[int]], address: int) -> None:
    before_instruction: bool = True
    for i, token in enumerate(tokens):
        is_a_label: bool = token.startswith(".")
        if is_a_label:
            if before_instruction:
                labels_table[token] = address
            else:
                if token in labels_addresses:
                    labels_addresses[token].append(address)
                else:
                    labels_addresses[token] = [address]
        else:
            before_instruction = False


def is_register_correct(register_name: str, register_amount: int) -> bool:
    is_valid_register_prefix: bool = register_name.startswith("r")
    is_valid_register_amount: bool = register_name[1:].isnumeric()

    if not (is_valid_register_prefix and is_valid_register_amount):
        return False

    return int(register_name[1:]) < register_amount

def is_immediate_value_correct(immediate_value: str, amount_bits: int, signed: bool = False) -> bool:
    is_single_quoted: bool = immediate_value.startswith("'") and immediate_value.endswith("'")
    is_double_quoted: bool = immediate_value.startswith('"') and immediate_value.endswith('"')
    if is_single_quoted or is_double_quoted:
        if immediate_value[1:2].upper() in chars:
            return True

    is_binary_number: bool = immediate_value.startswith("0b")
    if is_binary_number:
        are_all_one_zero = all([value in {"0", "1"} for value in immediate_value[2:]])

        return are_all_one_zero

    if not is_number(immediate_value, signed):
        return False

    return int(immediate_value) < 2**amount_bits


def is_number(value: str, signed: bool = False) -> bool:
    valid_digits: set[str] = {"0", "1", "2", "3", "4", "5", "6", "7", "8", "9"}

    if signed and value[0] == "-":
        return all([value in valid_digits for value in value[1:]]) and not value == ""

    return all([value in valid_digits for value in value]) and not value == ""


def are_all_registers(registers: list[str], register_amount: int) -> bool:
    need_to_continue: bool = True
    i: int = 0
    while need_to_continue and i < len(registers):
        if not is_register_correct(registers[i], register_amount):
            need_to_continue = False

        i += 1

    return is_register_correct(registers[i - 1], register_amount)


def are_operands_regs_correct(operands: list[str],
                              amount_available_registers: int,
                              amount_operands_needed: int,
                              name: str) -> bool:
    is_operand_amount_valid(operands, amount_operands_needed, name)

    if not are_all_registers(operands, amount_available_registers):
        raise RegisterOperandsException("Operands are not all classified as valid registers !")

    return True


def are_valid_reg_n_imm(operands: list[str], amount_available_registers: int, amount_operands_needed: int, name: str) -> bool:
    is_operand_amount_valid(operands, amount_operands_needed, name)

    if not is_register_correct(operands[0], amount_available_registers):
        raise RegisterOperandsException("Register operand is not classified as a valid register !")

    if not is_immediate_value_correct(operands[1], registers_bits, True):
        raise ImmediateOperandsException("Immediate value operand is not valid !")

    return True


def are_valid_reg2_imm_opt(operands: list[str],
                           name: str,
                           amount_operands_needed: int,
                           amount_available_registers: int) -> bool:
    max_amount_operands_needed: int = 3

    if not (amount_operands_needed <= len(operands) <= max_amount_operands_needed):
        raise RegisterOperandsException(f"Operands amount for {name} instruction does not match "
                                        f"{amount_operands_needed} minimum needed registers !")

    are_all_registers(operands, amount_available_registers)
    if len(operands) == max_amount_operands_needed:
        if not is_immediate_value_correct(operands[2], 4, True):
            raise ImmediateOperandsException("Immediate value operand is not valid !")

    return True


def is_address_operand_correct(operands: list[str], amount_operands_needed: int, name: str) -> bool:
    is_operand_amount_valid(operands, amount_operands_needed, name)

    if not is_immediate_value_correct(operands[0], instructions_address_bits):
        raise ImmediateOperandsException("Operand is not a valid address !")

    return True


def is_operand_amount_valid(operands: list[str], amount_operands_needed: int, name: str) -> bool:
    if len(operands) != amount_operands_needed:
        raise RegisterOperandsException(f"Operands amount for {name} instruction does not match "
                                        f"{amount_operands_needed} needed registers !")

    return True
