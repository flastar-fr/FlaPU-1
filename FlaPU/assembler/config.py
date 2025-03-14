instructions_address_bits: int = 10
registers_bits: int = 8

assembled_name: dict[str, str] = {
    "NOP": "0000",
    "HLT": "0001",
    "ADD": "0010",
    "SUB": "0011",
    "NOR": "0100",
    "AND": "0101",
    "XOR": "0110",
    "RSH": "0111",
    "LDI": "1000",
    "ADI": "1001",
    "JMP": "1010",
    "BRH": "1011",
    "CAL": "1100",
    "RET": "1101",
    "LOD": "1110",
    "STR": "1111"
}

flags: dict[str, str] = {"zero": "00", "notzero": "01", "carry": "10", "notcarry": "11",
                         "=": "00", "!=": "01", ">=": "10", "<": "11"}
