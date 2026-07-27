from core.models import Field
from core.aamva import FIELD_DEFINITIONS
from core.header_parser import HeaderParser


class AAMVAParser:
    
    def __init__(self):
        self.header = None

    def parse(self, raw_text: str) -> list[Field]:

        self.header = HeaderParser().parse(raw_text)
        

        

        fields = []

        lines = []

        for line in raw_text.splitlines():

            line = line.rstrip("\r")

            if not line:
                continue

            # Skip the AAMVA header
            if line == "@":
                continue

            if line.lstrip().startswith("ANSI"):
                line = line.lstrip()
                marker = "DL"

                # Find the second "DL":
                # 1st = subfile designator ("DL00310277")
                # 2nd = beginning of the actual data ("DLDCAD")
                first = line.find(marker)
                second = line.find(marker, first + 2)

                if second != -1:
                    line = line[second:]
                else:
                    continue

            if line.startswith("DL"):

                # Raw AAMVA payload: DL + offset + length
                if len(line) >= 10 and line[2:10].isdigit():
                    line = line[10:]

                # Decoded text: first field immediately follows DL
                else:
                    line = line[2:]

                if not line:
                    continue

            lines.append(line)
            
        for line in lines:
            
                

            if len(line) < 4:
                continue
            
            
            
            code = line[:3]
   

            if code not in FIELD_DEFINITIONS:

                fields.append(
                    Field(
                        code=code,
                        name="Unknown Field",
                        value = line[3:],
                        original_value=line[3:],
                        required=False,
                    )
                )

                continue

            value = line[3:]
            
            
            

            name, required = FIELD_DEFINITIONS[code]

            

            field = Field(
                code=code,
                name=name,
                value=value,
                original_value=value,
                required=required,
            )

           

            

            fields.append(field)
               
        return fields