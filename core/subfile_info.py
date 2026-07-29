from dataclasses import dataclass


@dataclass
class SubfileInfo:
    file_type: str
    offset: int = 0
    length: int = 0
