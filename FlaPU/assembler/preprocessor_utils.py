def is_instruction_has_definition(instruction_tokens: list[str], definitions: list[str]) -> str:
    definition_found: bool = False
    i: int = 0
    definition_in_instruction: str = ""

    while not definition_found and i < len(definitions):
        definition: str = definitions[i]
        if definition in instruction_tokens:
            definition_found = True
            definition_in_instruction = definition

        i += 1

    return definition_in_instruction


def replace_definition_value(tokens: list[str], definitions_table: dict[str, str], selected_definition: str) -> str:
    token_to_merge: str = definitions_table[selected_definition]
    index_token_to_replace: int = tokens.index(selected_definition)
    tokens[index_token_to_replace] = token_to_merge
    return " ".join(tokens)
