from pathlib import Path

from core.encoder import AAMVAEncoder
from core.file_loader import load_aamva_file
from core.parser import AAMVAParser


def test_single_subfile_header():
    raw = load_aamva_file(
        Path(__file__).resolve().parents[1] / "test_sample.txt"
    )

    parser = AAMVAParser()
    fields = parser.parse(raw)

    payload = AAMVAEncoder().encode(fields, parser.header)

    assert parser.header.number_of_entries == 1
    assert len(parser.header.subfiles) == 1
    assert parser.header.subfiles[0].file_type == "DL"
    assert "DL0031" in payload
    assert payload.endswith("\r")
    assert "DBA11222030" in payload


def test_two_subfile_header_matches_penstate_original():
    original_path = Path("/Users/brij/Downloads/original_penstate.bin")
    if not original_path.exists():
        return

    raw = load_aamva_file(original_path)
    parser = AAMVAParser()
    fields = parser.parse(raw)
    payload = AAMVAEncoder().encode(fields, parser.header)

    assert parser.header.number_of_entries == 2
    assert [subfile.file_type for subfile in parser.header.subfiles] == ["DL", "ZP"]
    assert payload.encode("latin-1") == original_path.read_bytes()


def test_two_subfile_preserves_empty_jurisdiction_fields():
    original_path = Path("/Users/brij/Downloads/original_arizona.bin")
    if not original_path.exists():
        return

    raw = load_aamva_file(original_path)
    parser = AAMVAParser()
    fields = parser.parse(raw)
    payload = AAMVAEncoder().encode(fields, parser.header)

    za_fields = [field for field in fields if field.subfile == "ZA"]
    assert [(field.code, field.value) for field in za_fields] == [
        ("ZAZ", "AAN"),
        ("ZAB", ""),
        ("ZAC", ""),
    ]
    assert payload.encode("latin-1") == original_path.read_bytes()


def test_import_preserves_field_order():
    original_path = Path("/Users/brij/Downloads/original_penstate.bin")
    if not original_path.exists():
        return

    parser = AAMVAParser()
    fields = parser.parse(load_aamva_file(original_path))

    assert [field.code for field in fields[:5]] == [
        "DAQ", "DCS", "DDE", "DAC", "DDF"
    ]
    assert [field.code for field in fields if field.subfile == "ZP"] == [
        "ZPZ", "ZPB", "ZPC", "ZPD"
    ]
