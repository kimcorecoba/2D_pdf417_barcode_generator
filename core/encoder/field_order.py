"""
Default DL field order for new records without an imported template.
Encoding uses the field list order from import or the editor instead.
"""

from .data_elements import DATA_ELEMENTS

DEFAULT_DL_FIELD_ORDER = [
    DATA_ELEMENTS["DBA"],
    DATA_ELEMENTS["DCS"],
    DATA_ELEMENTS["DAC"],
    DATA_ELEMENTS["DBD"],
    DATA_ELEMENTS["DBB"],
    DATA_ELEMENTS["DBC"],
    DATA_ELEMENTS["DAY"],
    DATA_ELEMENTS["DAQ"],
    DATA_ELEMENTS["DAK"],
]
