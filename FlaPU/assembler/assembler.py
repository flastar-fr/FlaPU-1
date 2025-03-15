from typing import Type

from .exceptions.assembling_exception import AssemblingException
from .file_manipulations import extract_file_content, write_to_file
from .exceptions.immediate_value_exception import ImmediateOperandsException
from .exceptions.register_operands_exception import RegisterOperandsException
from .instructions import Instruction, available_instructions
from .instruction_parser import split_instruction_line
from .preprocessor import Preprocessor


class Assembler:
    def __init__(self, amount_registers: int) -> None:
        self.amount_available_registers: int = amount_registers

    def assemble_line(self, instruction_line: str) -> str:
        try:
            instruction: Instruction = self.parse_line(instruction_line)
            instruction.are_operands_correct(self.amount_available_registers)
        except (RegisterOperandsException, ImmediateOperandsException, AssemblingException) as e:
            new_message: str = f"Cannot assemble line : '{instruction_line}'. {str(e)}"
            raise RegisterOperandsException(new_message) from e

        return instruction.assemble()

    def assemble_file(self, asm_file_path: str, machine_code_file_path: str) -> None:
        instructions: list[str] = extract_file_content(asm_file_path)

        print(instructions)
        instructions = Preprocessor.preprocess_lines(instructions)
        print(instructions)

        machine_code_instructions: list[str] = self._assemble_lines(instructions)

        write_to_file(machine_code_file_path, machine_code_instructions)

    def _assemble_lines(self, instructions: list[str]) -> list[str]:
        machine_code_instructions: list[str] = []
        for instruction_line, instruction in enumerate(instructions):
            try:
                machine_code_instructions.append(self.assemble_line(instruction))

            except (RegisterOperandsException, ImmediateOperandsException, AssemblingException) as e:
                new_message: str = f"{str(e)} (line {instruction_line + 1})"
                raise type(e)(new_message) from e

        return machine_code_instructions

    @staticmethod
    def parse_line(line: str) -> Instruction:
        tokens: list[str] = split_instruction_line(line)

        operation: str = tokens[0]
        operation_operands: list[str] = tokens[1:]

        if operation not in available_instructions:
            raise AssemblingException(f"Undefined assembler instruction '{operation}'.")

        instruction_class: Type[Instruction] = available_instructions[operation]

        return instruction_class(operation_operands)
