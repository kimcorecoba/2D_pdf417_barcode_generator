from .field_order import MANDATORY_FIELD_ORDER
from .data_elements import DATA_ELEMENTS
from .validator import validate_field




class BodyBuilder:
    """
    Builds the DL subfile body.
    """

    def build(self, fields, config) -> str:

        field_lookup = {
            field.code: field.value
            for field in fields
        }

        body = []

        # Emit fields in AAMVA order
        for element in MANDATORY_FIELD_ORDER:

            value = field_lookup.get(element.code)
            validate_field(element, value)

            if not value:

                continue

            
           
            body.append(f"{element.code}{value}")

        # Emit any remaining fields afterwards
        ordered_codes = {
            element.code
            for element in MANDATORY_FIELD_ORDER
        }

        for field in fields:
            
            if not field.value:
                continue

            if field.code in ordered_codes:
                continue

            element = DATA_ELEMENTS.get(field.code)

            if (
                element is not None
                and element.max_length is not None
                and len(field.value) > element.max_length
            ):
                raise ValueError(
                    f"{field.code} exceeds the maximum "
                    f"length of {element.max_length} characters."
                )

            entry = f"{field.code}{field.value}"
            print(f"{field.code}: {len(entry)} bytes -> {repr(entry)}")
            body.append(entry)

        result = (
            config.data_element_separator.join(body)
            + config.segment_terminator
        )

        print("\n=== BodyBuilder ===")
        print("len(result) =", len(result))
        print("Last 40 chars:", repr(result[-40:]))
        print("===================\n")

        return result