from .data_elements import DATA_ELEMENTS
from .validator import validate_field


class BodyBuilder:
    """
    Builds AAMVA subfile bodies using imported field order.
    """

    def build_subfile(
        self,
        subfile_type: str,
        fields,
        config,
    ) -> str:
        entries = []

        for field in fields:
            if field.subfile != subfile_type:
                continue

            if not field.value and not field.present_in_source:
                continue

            if field.value:
                element = DATA_ELEMENTS.get(field.code)
                if element is not None:
                    validate_field(element, field.value)
                elif len(field.value) > 250:
                    raise ValueError(
                        f"{field.code} exceeds the maximum length of 250 characters."
                    )

            entries.append(f"{field.code}{field.value}")

        if not entries:
            return ""

        if subfile_type in {"DL", "ID"}:
            body = subfile_type + entries[0]
            if len(entries) > 1:
                body += config.data_element_separator.join([""] + entries[1:])
        else:
            body = config.data_element_separator.join(entries)

        body += config.segment_terminator
        return body
