from abc import ABC, abstractmethod
from typing import Type

from .config import assembled_name, flags, instructions_address_bits

from .instruction_parser import (is_operand_amount_valid, is_address_operand_correct, are_valid_reg2_imm_opt,
                                are_operands_regs_correct, are_valid_reg_n_imm, is_register_correct,
                                is_immediate_value_correct)
from .flag_exception import FlagException
from .exceptions.immediate_value_exception import ImmediateOperandsException
from .exceptions.register_operands_exception import RegisterOperandsException
from .instruction_assembling import (normalize_length, convert_int_to_binary, get_register_binary,
                                    assemble_address, assemble_no_operand, assemble_reg2_imm_opt,
                                    assemble_reg_imm, assemble_reg3)


class Instruction(ABC):
    amount_operands_needed: int
    name: str

    def __init__(self, operands: list[str]):
        self.operands: list[str] = operands

    @abstractmethod
    def assemble(self) -> str:
        pass

    @abstractmethod
    def are_operands_correct(self, register_amount: int) -> bool:
        pass


class NOPInstruction(Instruction):
    amount_operands_needed: int = 0
    name: str = "NOP"

    def __init__(self, operands: list[str]):
        super().__init__(operands)

    def assemble(self) -> str:
        return assemble_no_operand(self.name)

    def are_operands_correct(self, amount_available_registers: int) -> bool:
        is_operand_amount_valid(self.operands, self.amount_operands_needed, self.name)

        return True


class HLTInstruction(Instruction):
    amount_operands_needed: int = 0
    name: str = "HLT"

    def __init__(self, operands: list[str]):
        super().__init__(operands)

    def assemble(self) -> str:
        return assemble_no_operand(self.name)

    def are_operands_correct(self, amount_available_registers: int) -> bool:
        is_operand_amount_valid(self.operands, self.amount_operands_needed, self.name)

        return True


class ADDInstruction(Instruction):
    amount_operands_needed: int = 3
    name: str = "ADD"

    def __init__(self, operands: list[str]):
        super().__init__(operands)

    def assemble(self) -> str:
        return assemble_reg3(self.name, self.operands)

    def are_operands_correct(self, amount_available_registers: int) -> bool:
        return are_operands_regs_correct(self.operands,
                                         amount_available_registers,
                                         self.amount_operands_needed,
                                         self.name)


class SUBInstruction(Instruction):
    amount_operands_needed: int = 3
    name: str = "SUB"

    def __init__(self, operands: list[str]):
        super().__init__(operands)

    def assemble(self) -> str:
        return assemble_reg3(self.name, self.operands)

    def are_operands_correct(self, amount_available_registers: int) -> bool:
        return are_operands_regs_correct(self.operands,
                                         amount_available_registers,
                                         self.amount_operands_needed,
                                         self.name)


class NORInstruction(Instruction):
    amount_operands_needed: int = 3
    name: str = "NOR"

    def __init__(self, operands: list[str]):
        super().__init__(operands)

    def assemble(self) -> str:
        return assemble_reg3(self.name, self.operands)

    def are_operands_correct(self, amount_available_registers: int) -> bool:
        return are_operands_regs_correct(self.operands,
                                         amount_available_registers,
                                         self.amount_operands_needed,
                                         self.name)


class ANDInstruction(Instruction):
    amount_operands_needed: int = 3
    name: str = "AND"

    def __init__(self, operands: list[str]):
        super().__init__(operands)

    def assemble(self) -> str:
        return assemble_reg3(self.name, self.operands)

    def are_operands_correct(self, amount_available_registers: int) -> bool:
        return are_operands_regs_correct(self.operands,
                                         amount_available_registers,
                                         self.amount_operands_needed,
                                         self.name)


class XORInstruction(Instruction):
    amount_operands_needed: int = 3
    name: str = "XOR"

    def __init__(self, operands: list[str]):
        super().__init__(operands)

    def assemble(self) -> str:
        return assemble_reg3(self.name, self.operands)

    def are_operands_correct(self, amount_available_registers: int) -> bool:
        return are_operands_regs_correct(self.operands,
                                         amount_available_registers,
                                         self.amount_operands_needed,
                                         self.name)


class RSHInstruction(Instruction):
    amount_operands_needed: int = 2
    name: str = "RSH"

    def __init__(self, operands: list[str]):
        super().__init__(operands)

    def assemble(self) -> str:
        base_instruction_assembled: str = assembled_name[self.name]
        binary_operand_receive: str = get_register_binary(self.operands[0])
        binary_operand_take: str = get_register_binary(self.operands[1])
        assembled_line: str = f"{base_instruction_assembled}{binary_operand_receive}0000{binary_operand_take}"

        return assembled_line

    def are_operands_correct(self, amount_available_registers: int) -> bool:
        return are_operands_regs_correct(self.operands,
                                         amount_available_registers,
                                         self.amount_operands_needed,
                                         self.name)


class LDIInstruction(Instruction):
    amount_operands_needed: int = 2
    name: str = "LDI"

    def __init__(self, operands: list[str]):
        super().__init__(operands)

    def assemble(self) -> str:
        return assemble_reg_imm(self.name, self.operands)

    def are_operands_correct(self, amount_available_registers: int) -> bool:
        return are_valid_reg_n_imm(self.operands,
                                   amount_available_registers,
                                   self.amount_operands_needed,
                                   self.name)


class ADIInstruction(Instruction):
    amount_operands_needed: int = 2
    name: str = "ADI"

    def __init__(self, operands: list[str]):
        super().__init__(operands)

    def assemble(self) -> str:
        return assemble_reg_imm(self.name, self.operands)

    def are_operands_correct(self, amount_available_registers: int) -> bool:
        return are_valid_reg_n_imm(self.operands,
                                   amount_available_registers,
                                   self.amount_operands_needed,
                                   self.name)


class INCInstruction(Instruction):
    amount_operands_needed: int = 1
    name: str = "INC"

    def __init__(self, operands: list[str]):
        super().__init__(operands)

    def assemble(self) -> str:
        adi_instruction: ADIInstruction = ADIInstruction(self.operands + ["1"])
        return adi_instruction.assemble()

    def are_operands_correct(self, amount_available_registers: int) -> bool:
        is_operand_amount_valid(self.operands, self.amount_operands_needed, self.name)

        if not is_register_correct(self.operands[0], amount_available_registers):
            raise RegisterOperandsException("Operand is not classified as a valid register !")

        return True


class DECInstruction(Instruction):
    amount_operands_needed: int = 1
    name: str = "DEC"

    def __init__(self, operands: list[str]):
        super().__init__(operands)

    def assemble(self) -> str:
        adi_instruction: ADIInstruction = ADIInstruction(self.operands + ["255"])
        return adi_instruction.assemble()

    def are_operands_correct(self, amount_available_registers: int) -> bool:
        is_operand_amount_valid(self.operands, self.amount_operands_needed, self.name)

        if not is_register_correct(self.operands[0], amount_available_registers):
            raise RegisterOperandsException("Operand is not classified as a valid register !")

        return True

class JMPInstruction(Instruction):
    amount_operands_needed: int = 1
    name: str = "JMP"

    def __init__(self, operands: list[str]):
        super().__init__(operands)

    def assemble(self) -> str:
        return assemble_address(self.name, self.operands)

    def are_operands_correct(self, amount_available_registers: int) -> bool:
        return is_address_operand_correct(self.operands, self.amount_operands_needed, self.name)


class BRHInstruction(Instruction):
    amount_operands_needed: int = 2
    name: str = "BRH"

    def __init__(self, operands: list[str]):
        super().__init__(operands)

    def assemble(self) -> str:
        base_instruction_assembled: str = assembled_name[self.name]
        binary_flag: str = flags[self.operands[0]]
        binary_address_value: str = convert_int_to_binary(int(self.operands[1]))
        binary_operand_value_normalized: str = normalize_length(binary_address_value, instructions_address_bits)
        assembled_line: str = f"{base_instruction_assembled}{binary_flag}{binary_operand_value_normalized}"

        return assembled_line

    def are_operands_correct(self, amount_available_registers: int) -> bool:
        is_operand_amount_valid(self.operands, self.amount_operands_needed, self.name)

        if self.operands[0] not in flags:
            raise FlagException(f"Operand {self.operands[0]} is not a valid flag !")

        if not is_immediate_value_correct(self.operands[1], instructions_address_bits):
            raise ImmediateOperandsException("Operand is not a valid address !")

        return True


class CMPInstruction(Instruction):
    amount_operands_needed: int = 2
    name: str = "CMP"

    def __init__(self, operands: list[str]):
        super().__init__(operands)

    def assemble(self) -> str:
        sub_instruction: SUBInstruction = SUBInstruction(self.operands + ["r0"])
        return sub_instruction.assemble()

    def are_operands_correct(self, amount_available_registers: int) -> bool:
        return are_operands_regs_correct(self.operands,
                                         amount_available_registers,
                                         self.amount_operands_needed,
                                         self.name)


class CALInstruction(Instruction):
    amount_operands_needed: int = 1
    name: str = "CAL"

    def __init__(self, operands: list[str]):
        super().__init__(operands)

    def assemble(self) -> str:
        return assemble_address(self.name, self.operands)

    def are_operands_correct(self, amount_available_registers: int) -> bool:
        return is_address_operand_correct(self.operands, self.amount_operands_needed, self.name)


class RETInstruction(Instruction):
    amount_operands_needed: int = 0
    name: str = "RET"

    def __init__(self, operands: list[str]):
        super().__init__(operands)

    def assemble(self) -> str:
        return assemble_no_operand(self.name)

    def are_operands_correct(self, amount_available_registers: int) -> bool:
        is_operand_amount_valid(self.operands, self.amount_operands_needed, self.name)

        return True


class LODInstruction(Instruction):
    amount_operands_needed: int = 2
    max_amount_operands_needed: int = 3
    name: str = "LOD"

    def __init__(self, operands: list[str]):
        super().__init__(operands)

    def assemble(self) -> str:
        return assemble_reg2_imm_opt(self.name, self.operands)

    def are_operands_correct(self, amount_available_registers: int) -> bool:
        return are_valid_reg2_imm_opt(self.operands,
                                      self.name,
                                      self.amount_operands_needed,
                                      amount_available_registers)


class STRInstruction(Instruction):
    amount_operands_needed: int = 2
    max_amount_operands_needed: int = 3
    name: str = "STR"

    def __init__(self, operands: list[str]):
        super().__init__(operands)

    def assemble(self) -> str:
        return assemble_reg2_imm_opt(self.name, self.operands)

    def are_operands_correct(self, amount_available_registers: int) -> bool:
        return are_valid_reg2_imm_opt(self.operands,
                                      self.name,
                                      self.amount_operands_needed,
                                      amount_available_registers)


class MOVInstruction(Instruction):
    amount_operands_needed: int = 2
    name: str = "MOV"

    def __init__(self, operands: list[str]):
        super().__init__(operands)

    def assemble(self) -> str:
        add_instruction: ADDInstruction = ADDInstruction([self.operands[0], "r0", self.operands[1]])
        return add_instruction.assemble()

    def are_operands_correct(self, amount_available_registers: int) -> bool:
        return are_operands_regs_correct(self.operands,
                                         amount_available_registers,
                                         self.amount_operands_needed,
                                         self.name)


class LSHInstruction(Instruction):
    amount_operands_needed: int = 2
    name: str = "LSH"

    def __init__(self, operands: list[str]):
        super().__init__(operands)

    def assemble(self) -> str:
        add_instruction: ADDInstruction = ADDInstruction([self.operands[0], self.operands[0], self.operands[1]])
        return add_instruction.assemble()

    def are_operands_correct(self, amount_available_registers: int) -> bool:
        return are_operands_regs_correct(self.operands,
                                         amount_available_registers,
                                         self.amount_operands_needed,
                                         self.name)


class NOTInstruction(Instruction):
    amount_operands_needed: int = 2
    name: str = "NOT"

    def __init__(self, operands: list[str]):
        super().__init__(operands)

    def assemble(self) -> str:
        nor_instruction: NORInstruction = NORInstruction([self.operands[0], "r0", self.operands[1]])
        return nor_instruction.assemble()

    def are_operands_correct(self, amount_available_registers: int) -> bool:
        return are_operands_regs_correct(self.operands,
                                         amount_available_registers,
                                         self.amount_operands_needed,
                                         self.name)


class NEGInstruction(Instruction):
    amount_operands_needed: int = 2
    name: str = "NEG"

    def __init__(self, operands: list[str]):
        super().__init__(operands)

    def assemble(self) -> str:
        sub_instruction: SUBInstruction = SUBInstruction(["r0"] + self.operands)
        return sub_instruction.assemble()

    def are_operands_correct(self, amount_available_registers: int) -> bool:
        return are_operands_regs_correct(self.operands,
                                         amount_available_registers,
                                         self.amount_operands_needed,
                                         self.name)


available_instructions: dict[str, Type[Instruction]] = {"NOP": NOPInstruction, "HLT": HLTInstruction,
                                                        "ADD": ADDInstruction, "SUB": SUBInstruction,
                                                        "NOR": NORInstruction, "AND": ANDInstruction,
                                                        "XOR": XORInstruction, "RSH": RSHInstruction,
                                                        "LDI": LDIInstruction, "ADI": ADIInstruction,
                                                        "INC": INCInstruction, "DEC": DECInstruction,
                                                        "JMP": JMPInstruction, "BRH": BRHInstruction,
                                                        "CMP": CMPInstruction, "CAL": CALInstruction,
                                                        "RET": RETInstruction, "LOD": LODInstruction,
                                                        "STR": STRInstruction, "MOV": MOVInstruction,
                                                        "LSH": LSHInstruction, "NOT": NOTInstruction,
                                                        "NEG": NEGInstruction}
