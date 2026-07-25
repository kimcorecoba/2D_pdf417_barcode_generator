from core.models import Field
from core.date_validator import is_valid_date


class Validator:

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

        return fields