from core.models import Field
from core.aamva import FIELD_DEFINITIONS


def driver_license_fields():
    fields = []

    for code, (name, required) in FIELD_DEFINITIONS.items():
        fields.append(
            Field(
                code=code,
                name=name,
                required=required,
            )
        )

    return fields