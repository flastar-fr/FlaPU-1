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

memory_mapped_addresses: dict[str, str] = {
    "pixel_x": "240",
    "pixel_y": "241",
    "draw_pixel": "242",
    "clear_pixel": "243",
    "load_pixel": "244",
    "buffer_screen": "245",
    "clear_screen_buffer": "246",
    "write_char": "247",
    "buffer_chars": "248",
    "clear_chars_buffer": "249",
    "show_number": "250",
    "clear_number": "251",
    "signed_mode": "252",
    "unsigned_mode": "253",
    "rng": "254",
    "controller_input": "255"
}

chars: dict[str, int] = {" ": 0, "A": 1, "B": 2, "C": 3, "D": 4, "E": 5,
                         "F": 6, "G": 7, "H": 8, "I": 9, "J": 10,
                         "K": 11, "L": 12, "M": 13, "N": 14, "O": 15,
                         "P": 16, "Q": 17, "R": 18, "S": 19, "T": 20,
                         "U": 21, "V": 22, "W": 23, "X": 24, "Y": 25, "Z": 26,
                         ".": 27, "!": 28, "?": 29}
