from dataclasses import dataclass


@dataclass
class HeaderInfo:
    iin: str
    version: str
    jurisdiction_version: str
    number_of_entries: int
    file_type: str