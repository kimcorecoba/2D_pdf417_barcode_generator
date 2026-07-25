"""
Definitions of AAMVA data elements used by the encoder.
"""


class DataElement:

    def __init__(
        self,
        code: str,
        required: bool = True,
        max_length: int | None = None,
        allowed_values: set[str] | None = None,
    ):
        self.code = code
        self.required = required
        self.max_length = max_length
        self.allowed_values = allowed_values


DATA_ELEMENTS = {
    "DBA": DataElement("DBA", max_length=8),
    "DCS": DataElement("DCS", max_length=40),
    "DAC": DataElement("DAC", max_length=80),
    "DCF": DataElement(
        "DCF",
        required=False,
        max_length=25,
    ),
    "DBD": DataElement("DBD", max_length=8),
    "DBB": DataElement("DBB", max_length=8),
    "DBC": DataElement(
        "DBC",
        max_length=1,
        allowed_values={"1", "2", "9"},
    ),
    "DAY": DataElement(
        "DAY",
        max_length=3,
        allowed_values={
            "BLK",
            "BLU",
            "BRO",
            "GRY",
            "GRN",
            "HAZ",
            "MAR",
            "PNK",
            "DIC",
            "UNK",
        },
    ),
    "DAZ": DataElement(
        "DAZ",
        max_length=3,
        allowed_values={
            "BAL",
            "BLK",
            "BLN",
            "BRO",
            "GRY",
            "RED",
            "SDY",
            "WHI",
        },
    ),
    "DAQ": DataElement("DAQ", max_length=25),
    "DAK": DataElement("DAK", max_length=11),
    "DAG": DataElement(
        "DAG",
        required=False,
        max_length=35,
    ),

    "DAI": DataElement(
        "DAI",
        required=False,
        max_length=20,
    ),

    "DAJ": DataElement(
        "DAJ",
        required=False,
        max_length=2,
    ),
    
    "DAD": DataElement(
        "DAD",
        required=False,
        max_length=40,
    ),

    "DCT": DataElement(
    
    "DCT",
        required=False,
        max_length=150,
    ),
    
    "DCU": DataElement(
        "DCU",
        required=False,
        max_length=5,
    ),
    
    "DAW": DataElement(
        "DAW",
        required=False,
        max_length=3,
),

    "DAX": DataElement(
       "DAX",
       required=False,
       max_length=3,
    ),
}   