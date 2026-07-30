from core.models import Field
from core.validator import Validator, validate_height


def test_validate_height_accepts_in_format():
    valid, _ = validate_height("076 IN")
    assert valid

    valid, _ = validate_height("076IN")
    assert valid


def test_validate_height_accepts_cm_format():
    valid, _ = validate_height("180 CM")
    assert valid


def test_validate_height_accepts_ny_fii_format():
    valid, _ = validate_height("503")
    assert valid

    valid, _ = validate_height("602 ")
    assert valid

    valid, _ = validate_height("511")
    assert valid


def test_validate_height_rejects_invalid_fii():
    valid, message = validate_height("512")
    assert not valid
    assert "00-11" in message

    valid, _ = validate_height("999")
    assert not valid


def test_validator_marks_ny_fii_height_valid():
    field = Field(code="DAU", name="Height", value="503")
    Validator().validate([field])
    assert field.valid
