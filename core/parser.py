from core.models import Field
from core.aamva import FIELD_DEFINITIONS
from core.header_parser import HeaderParser


class AAMVAParser:
    
    def __init__(self):
        self.header = None

    def parse(self, raw_text: str) -> list[Field]:

        self.header = HeaderParser().parse(raw_text)
        header = self.header
        

        #if header: # We'll use the header later.
            #pass

        fields = []

        lines = []

        for line in raw_text.splitlines():

            line = line.strip()

            if not line:
                continue

            # Skip the AAMVA header
            if line == "@":
                continue

            if line.startswith("ANSI"):
                continue

            if line.startswith("DL"):
                continue

            lines.append(line)
            
        for line in lines:

            line = line.strip()

            if len(line) < 4:
                continue

            code = line[:3]

            if code not in FIELD_DEFINITIONS:

                fields.append(
                    Field(
                        code=code,
                        name="Unknown Field",
                        value=line[3:].strip(),
                        original_value=line[3:].strip(),
                        required=False,
                    )
                )

                continue

            value = line[3:].strip()

            name, required = FIELD_DEFINITIONS[code]

            fields.append(
                Field(
                    code=code,
                    name=name,
                    value=value,
                    original_value=value,
                    required=required,
                )
            )

        return fields