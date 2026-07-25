from dataclasses import dataclass


@dataclass
class Field:
    code: str
    name: str
    value: str = ""

    required: bool = False

    valid: bool = True

    message: str = ""

    original_value: str = ""

    changed: bool = False