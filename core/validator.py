from core.models import Field
from core.date_validator import is_valid_date
from datetime import datetime
import re

VALID_EYE_COLORS = {
    "BLK", "BLU", "BRO", "GRY",
    "GRN", "HAZ", "MAR", "PNK",
    "DIC", "UNK"
}

VALID_STATE_CODES = {
    "AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE",
    "FL", "GA", "HI", "ID", "IL", "IN", "IA", "KS",
    "KY", "LA", "ME", "MD", "MA", "MI", "MN", "MS",
    "MO", "MT", "NE", "NV", "NH", "NJ", "NM", "NY",
    "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC",
    "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV",
    "WI", "WY", "DC"
}


def validate_height(value: str) -> tuple[bool, str]:
    stripped = value.strip()

    unit_match = re.match(
        r"^(\d+)\s*(IN|CM)$",
        stripped,
        re.IGNORECASE,
    )
    if unit_match:
        number = int(unit_match.group(1))
        unit = unit_match.group(2).upper()

        if unit == "IN" and not (36 <= number <= 96):
            return False, "Height must be between 36 IN and 96 IN."

        if unit == "CM" and not (91 <= number <= 244):
            return False, "Height must be between 91 CM and 244 CM."

        return True, ""

    # New York and some older jurisdictions use feet+inches: 503 = 5'03"
    fii_match = re.match(r"^(\d)(\d{2})$", stripped)
    if fii_match:
        feet = int(fii_match.group(1))
        inches = int(fii_match.group(2))

        if not (3 <= feet <= 8):
            return False, "Height must use 3-8 feet in FII format (e.g. 503)."

        if not (0 <= inches <= 11):
            return False, "Height inches must be 00-11 in FII format (e.g. 503)."

        return True, ""

    return (
        False,
        "Height must be formatted like 076 IN, 180 CM, or NY FII (e.g. 503).",
    )


class Validator:
    
    def validate_relationships(self, fields):

        field_map = {
            field.code: field
            for field in fields
        }
        
        dbb = field_map.get("DBB")
        dbd = field_map.get("DBD")
        dba = field_map.get("DBA")
        if not all([dbb, dbd, dba]):
            return

        if not (dbb.valid and dbd.valid and dba.valid):
            return
        birth_date = datetime.strptime(dbb.value, "%m%d%Y").date()
        issue_date = datetime.strptime(dbd.value, "%m%d%Y").date()
            
        if issue_date <= birth_date:
            dbd.valid = False
            dbd.message = "Issue date must be after date of birth."    
            
    def validate(self, fields: list[Field]):

        for field in fields:

            field.valid = True
            field.message = ""

            if field.required and not field.value.strip():
                field.valid = False
                field.message = "Required field is missing"

            if field.code == "DBB":

                if not is_valid_date(field.value):
                    field.valid = False
                    field.message = "Date must be MMDDYYYY"


            if field.code == "DBA":

                if not is_valid_date(field.value):
                    field.valid = False
                    field.message = "Date must be MMDDYYYY"

            if field.code == "DBD":

                if not is_valid_date(field.value):
                    field.valid = False
                    field.message = "Date must be MMDDYYYY"
                    
            if field.code == "DBC" and field.value:

                if field.value not in ("1", "2", "9"):
                    field.valid = False
                    field.message = "Sex must be 1 (Male), 2 (Female), or 9 (Not Specified)"
                    
            if field.code == "DAY" and field.value:

                

                if field.value.upper() not in VALID_EYE_COLORS:
                    field.valid = False
                    field.message = "Invalid eye color."
                    
            if field.code == "DAJ" and field.value:

                

                if field.value.upper() not in VALID_STATE_CODES:
                    field.valid = False
                    field.message = "Invalid state code."
                    
            if field.code == "DAK" and field.value:
                
                zip_code = field.value.strip()

                if not (
                    (len(zip_code) == 5 and zip_code.isdigit())
                    or
                    (len(zip_code) == 9 and zip_code.isdigit())
                ):
                    field.valid = False
                    field.message = "ZIP Code must be 5 or 9 digits." 
            
            if field.code == "DAU" and field.value:

                valid, message = validate_height(field.value)
                if not valid:
                    field.valid = False
                    field.message = message

            if field.code == "DAW" and field.value:

                weight = field.value.strip()

                if not weight.isdigit():
                    field.valid = False
                    field.message = "Weight must contain only digits."

                elif not (20 <= int(weight) <= 700):
                    field.valid = False
                    field.message = "Weight must be between 20 and 700 pounds."  
            
        self.validate_relationships(fields)   

        return fields