from dataclasses import dataclass, field

from core.subfile_info import SubfileInfo


@dataclass
class HeaderInfo:
    iin: str
    version: str
    jurisdiction_version: str
    number_of_entries: int
    file_type: str
    subfiles: list[SubfileInfo] = field(default_factory=list)
