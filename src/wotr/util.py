def indent(text: str, amount: int) -> str:
    return "\n".join(" " * amount + line for line in text.splitlines())
