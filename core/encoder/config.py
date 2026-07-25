from dataclasses import dataclass

from .constants import (
    COMPLIANCE_INDICATOR,
    DATA_ELEMENT_SEPARATOR,
    RECORD_SEPARATOR,
    SEGMENT_TERMINATOR,
)

from core.aamva_versions import FILE_TYPE



@dataclass(frozen=True)
class EncoderConfig:
    issuer_id: str
    version: str

    jurisdiction_version: str = "00"
    number_of_entries: int = 1

    compliance_indicator: str = COMPLIANCE_INDICATOR
    data_element_separator: str = DATA_ELEMENT_SEPARATOR
    record_separator: str = RECORD_SEPARATOR
    segment_terminator: str = SEGMENT_TERMINATOR
    file_type: str = FILE_TYPE