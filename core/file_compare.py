from dataclasses import dataclass, field
from pathlib import Path

from core.file_loader import load_aamva_file
from core.parser import AAMVAParser


@dataclass
class FieldComparison:
    code: str
    subfile: str
    left_value: str | None
    right_value: str | None
    status: str


@dataclass
class FileComparisonResult:
    left_path: str
    right_path: str
    byte_identical: bool
    left_size: int
    right_size: int
    left_subfiles: list
    right_subfiles: list
    subfiles_match: bool
    field_order_match: bool
    field_comparisons: list[FieldComparison] = field(default_factory=list)
    differing_byte_count: int = 0
    matching_field_count: int = 0
    total_field_count: int = 0

    @property
    def all_fields_match(self) -> bool:
        return all(
            comparison.status == "same"
            for comparison in self.field_comparisons
        )

    @property
    def summary(self) -> str:
        if self.byte_identical:
            return "Files are byte-identical."

        parts = [
            f"Files differ ({self.left_size} vs {self.right_size} bytes, "
            f"{self.differing_byte_count} byte difference"
            f"{'' if self.differing_byte_count == 1 else 's'})."
        ]

        if not self.subfiles_match:
            parts.append("Subfile headers differ.")

        if not self.field_order_match:
            parts.append("Field order differs.")

        if not self.all_fields_match:
            diff_count = sum(
                1
                for comparison in self.field_comparisons
                if comparison.status != "same"
            )
            parts.append(f"{diff_count} field difference(s).")
        else:
            parts.append("All field values match.")

        return " ".join(parts)


def compare_files(left_path: str | Path, right_path: str | Path) -> FileComparisonResult:
    left_path = Path(left_path)
    right_path = Path(right_path)

    left_bytes = left_path.read_bytes()
    right_bytes = right_path.read_bytes()

    left_parser = AAMVAParser()
    right_parser = AAMVAParser()
    left_fields = left_parser.parse(load_aamva_file(left_path))
    right_fields = right_parser.parse(load_aamva_file(right_path))

    left_subfiles = (
        left_parser.header.subfiles
        if left_parser.header
        else []
    )
    right_subfiles = (
        right_parser.header.subfiles
        if right_parser.header
        else []
    )

    subfiles_match = _subfiles_match(left_subfiles, right_subfiles)
    field_order_match = (
        [(field.subfile, field.code) for field in left_fields]
        == [(field.subfile, field.code) for field in right_fields]
    )

    left_map = {
        (field.subfile, field.code): field.value
        for field in left_fields
    }
    right_map = {
        (field.subfile, field.code): field.value
        for field in right_fields
    }

    ordered_keys = []
    seen = set()
    for field_item in left_fields + right_fields:
        key = (field_item.subfile, field_item.code)
        if key not in seen:
            ordered_keys.append(key)
            seen.add(key)

    field_comparisons = []
    matching_field_count = 0

    for subfile, code in ordered_keys:
        left_value = left_map.get((subfile, code))
        right_value = right_map.get((subfile, code))

        if left_value is None:
            status = "only_right"
        elif right_value is None:
            status = "only_left"
        elif left_value == right_value:
            status = "same"
            matching_field_count += 1
        else:
            status = "different"

        field_comparisons.append(
            FieldComparison(
                code=code,
                subfile=subfile,
                left_value=left_value,
                right_value=right_value,
                status=status,
            )
        )

    differing_byte_count = _count_byte_differences(left_bytes, right_bytes)

    return FileComparisonResult(
        left_path=str(left_path),
        right_path=str(right_path),
        byte_identical=left_bytes == right_bytes,
        left_size=len(left_bytes),
        right_size=len(right_bytes),
        left_subfiles=left_subfiles,
        right_subfiles=right_subfiles,
        subfiles_match=subfiles_match,
        field_order_match=field_order_match,
        field_comparisons=field_comparisons,
        differing_byte_count=differing_byte_count,
        matching_field_count=matching_field_count,
        total_field_count=len(field_comparisons),
    )


def _subfiles_match(left_subfiles, right_subfiles) -> bool:
    if len(left_subfiles) != len(right_subfiles):
        return False

    for left, right in zip(left_subfiles, right_subfiles):
        if (
            left.file_type != right.file_type
            or left.offset != right.offset
            or left.length != right.length
        ):
            return False

    return True


def _count_byte_differences(left_bytes: bytes, right_bytes: bytes) -> int:
    max_len = max(len(left_bytes), len(right_bytes))
    differences = 0

    for index in range(max_len):
        left_byte = left_bytes[index] if index < len(left_bytes) else None
        right_byte = right_bytes[index] if index < len(right_bytes) else None
        if left_byte != right_byte:
            differences += 1

    return differences
