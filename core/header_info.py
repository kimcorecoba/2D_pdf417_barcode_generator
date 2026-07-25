from dataclasses import dataclass


@dataclass
class HeaderInfo:
    iin: str
    version: str
    jurisdiction_version: str
    file_type: str