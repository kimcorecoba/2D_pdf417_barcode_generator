from pathlib import Path

from core.file_loader import load_aamva_file, normalize_aamva_binary
from core.parser import AAMVAParser


def test_load_bin_file_parses_fields():
    raw = load_aamva_file(Path(__file__).resolve().parents[1] / "barcode_content.bin")

    parser = AAMVAParser()
    fields = parser.parse(raw)

    assert parser.header is not None
    assert parser.header.iin == "636000"
    assert len(fields) == 4

    field_map = {field.code: field.value for field in fields}
    assert field_map["DCS"] == "ANDERSON"
    assert field_map["DAC"] == "ARIONA"
    assert field_map["DBA"] == "11222030"
    assert field_map["DZZ"] == "TEST VALUE"


def test_normalize_handles_aamva_control_bytes():
    data = b"@\r\n\x1e\rANSI 636000100001\r\nDL00320094\r\nDBA11222030\r\n"

    text = normalize_aamva_binary(data)

    assert "ANSI 636000100001" in text
    assert "DBA11222030" in text
