from pathlib import Path

from core.file_compare import compare_files
from core.file_loader import normalize_aamva_binary
from core.encoder import AAMVAEncoder
from core.parser import AAMVAParser


def test_identical_files_match():
    sample = Path(__file__).resolve().parents[1] / "barcode_content.bin"
    result = compare_files(sample, sample)

    assert result.byte_identical
    assert result.all_fields_match
    assert result.subfiles_match


def test_detects_field_difference():
    left = Path(__file__).resolve().parents[1] / "barcode_content.bin"
    raw = left.read_bytes()
    text = normalize_aamva_binary(raw).replace("ANDERSON", "SMITH")
    right = Path(__file__).resolve().parents[1] / "output" / "compare_test_left.bin"
    right.parent.mkdir(exist_ok=True)
    right.write_bytes(text.encode("latin-1"))

    result = compare_files(left, right)

    assert not result.byte_identical
    assert any(
        comparison.code == "DCS" and comparison.status == "different"
        for comparison in result.field_comparisons
    )


def test_roundtrip_reported_as_identical(tmp_path):
    penstate = Path("/Users/brij/Downloads/original_penstate.bin")
    if not penstate.exists():
        return

    from core.file_loader import load_aamva_file

    parser = AAMVAParser()
    fields = parser.parse(load_aamva_file(penstate))
    payload = AAMVAEncoder().encode(fields, parser.header)

    generated = tmp_path / "generated.bin"
    generated.write_bytes(payload.encode("latin-1"))

    result = compare_files(penstate, generated)

    assert result.byte_identical
    assert result.summary == "Files are byte-identical."
