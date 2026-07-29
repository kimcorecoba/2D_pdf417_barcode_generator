from pathlib import Path


def normalize_aamva_binary(data: bytes) -> str:
    """Convert raw AAMVA barcode bytes to text the parser understands."""
    text = data.decode("latin-1")
    text = text.replace("\x00", "")
    text = text.replace("\x1e\r", "\n")
    text = text.replace("\x1e\n", "\n")
    text = text.replace("\x1e", "\n")
    text = text.replace("\r\n", "\n")
    text = text.replace("\r", "\n")
    return text


def load_aamva_file(path: str | Path) -> str:
    """Load AAMVA payload from a .txt or .bin file."""
    file_path = Path(path)
    suffix = file_path.suffix.lower()

    if suffix == ".bin":
        return normalize_aamva_binary(file_path.read_bytes())

    return file_path.read_text(encoding="utf-8")
