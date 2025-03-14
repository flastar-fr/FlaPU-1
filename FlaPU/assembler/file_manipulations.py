def extract_file_content(file_path: str) -> list[str]:
    content: list[str] = []
    with open(file_path, "r") as f:
        for line in f:
            stripped_line: str = line.strip()
            if stripped_line != "":
                content.append(stripped_line)
    return content


def write_to_file(file_path: str, content: list[str]) -> None:
    with open(file_path, "w") as f:
        f.write("\n".join(content))
