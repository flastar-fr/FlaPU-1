from .config import memory_mapped_addresses
from .instruction_parser import split_instruction_line
from .exceptions.preprocessing_exception import PreprocessingException
from .preprocessor_utils import is_instruction_has_definition, replace_definition_value
from .instruction_parser import parse_labels


class Preprocessor:
    @classmethod
    def preprocess_lines(cls, instructions: list[str]) -> list[str]:
        instructions = cls.remove_comments(instructions)
        instructions = cls.clean_instructions(instructions)
        instructions = cls.associate_definitions(instructions)
        cls.replace_labels(instructions)

        return instructions

    @classmethod
    def associate_definitions(cls, instructions: list[str]) -> list[str]:
        final_instructions: list[str] = []
        definitions_table: dict[str, str] = memory_mapped_addresses.copy()

        for instruction in instructions:
            tokens: list[str] = split_instruction_line(instruction)
            definition_in_instruction: str = is_instruction_has_definition(tokens, list(definitions_table.keys()))
            if tokens[0] == "define":
                if len(tokens) != 3:
                    raise PreprocessingException(f"Invalid definition line {instruction}")
                definitions_table[tokens[1]] = tokens[2]
            elif definition_in_instruction != "":
                new_instruction: str = replace_definition_value(tokens, definitions_table, definition_in_instruction)
                final_instructions.append(new_instruction)
            else:
                final_instructions.append(instruction)

        return final_instructions

    @staticmethod
    def replace_labels(instructions: list[str]) -> None:
        labels_table: dict[str, int] = {}
        labels_addresses: dict[str, list[int]] = {}
        parse_labels(instructions, labels_table, labels_addresses)

        for label, address in labels_table.items():
            instructions[address] = instructions[address].replace(f"{label} ", "")

        for label, addresses in labels_addresses.items():
            if label not in labels_table:
                raise PreprocessingException(f"Label '{label}' is not defined.")
            for address in addresses:
                instructions[address] = instructions[address].replace(label, str(labels_table[label]))

    @staticmethod
    def remove_comments(instructions: list[str]) -> list[str]:
        final_instructions: list[str] = []
        for instruction in instructions:
            comment_symbol_index: int = instruction.find("//")
            if comment_symbol_index == -1:
                final_instructions.append(instruction)
            else:
                pure_instruction: str = instruction[:comment_symbol_index]
                if pure_instruction != "":
                    final_instructions.append(pure_instruction.strip())

        return final_instructions

    @staticmethod
    def clean_instructions(instructions: list[str]) -> list[str]:
        final_instructions: list[str] = []
        i: int = 0
        last_got_added: int = -2

        while i < len(instructions):
            tokens: list[str] = split_instruction_line(instructions[i])

            if tokens[0][0] == "." and len(tokens) == 1:
                label: str = tokens[0]
                final_instructions.append(f"{label} {instructions[i + 1]}")

                last_got_added = i
            elif last_got_added + 1 != i:
                final_instructions.append(" ".join(tokens))

            i += 1

        return final_instructions
