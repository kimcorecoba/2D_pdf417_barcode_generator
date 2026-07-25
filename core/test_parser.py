from core.parser import AAMVAParser

raw = """
DCSANDERSON
DACARIONA
DBB11221994
DAQ102756038
DAYBLU
"""

parser = AAMVAParser()

fields = parser.parse(raw)

for field in fields:
    print(field)