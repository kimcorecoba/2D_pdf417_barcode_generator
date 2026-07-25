DATE_FIELDS = {
    "DBA",
    "DBB",
    "DBD",
}


def validate_field(element, value):

    if element.required and not value:
        raise ValueError(
            f"Required field {element.code} is missing."
        )

    if not value:
        return

    if (
        element.max_length is not None
        and len(value) > element.max_length
    ):
        raise ValueError(
            f"{element.code} exceeds the maximum "
            f"length of {element.max_length} characters."
        )

    if element.code in DATE_FIELDS:

        if len(value) != 8 or not value.isdigit():
           raise ValueError(
               f"{element.code} must be an 8-digit date (MMDDYYYY)."
            ) 

    if (
        element.allowed_values is not None
        and value not in element.allowed_values
    ):
        raise ValueError(
            f"Invalid value for {element.code}."
        )
            
    