from core.models import Field
from core.aamva import FIELD_DEFINITIONS
from core.header_parser import HeaderParser


def _field_from_code(code: str, value: str, subfile: str) -> Field:
    if code not in FIELD_DEFINITIONS:
        return Field(
            code=code,
            name="Unknown Field",
            value=value,
            original_value=value,
            required=False,
            subfile=subfile,
            present_in_source=True,
        )

    name, required = FIELD_DEFINITIONS[code]
    return Field(
        code=code,
        name=name,
        value=value,
        original_value=value,
        required=required,
        subfile=subfile,
        present_in_source=True,
    )


class AAMVAParser:

    def __init__(self):
        self.header = None

    def parse(self, raw_text: str) -> list[Field]:
        self.header = HeaderParser().parse(raw_text)
        subfile_types = (
            [subfile.file_type for subfile in self.header.subfiles]
            if self.header and self.header.subfiles
            else ["DL"]
        )

        return self._parse_lines(raw_text, subfile_types)

    def _parse_lines(self, raw_text: str, subfile_types: list[str]) -> list[Field]:
        fields = []
        subfile_index = 0
        current_subfile = subfile_types[0]

        for line in raw_text.splitlines():
            line = line.rstrip("\r")

            if not line or line == "@":
                continue

            if line.lstrip().startswith("ANSI"):
                line = self._extract_first_body_line(line.lstrip(), subfile_types)
                if not line:
                    continue

            if self._is_designator_line(line):
                continue

            current_subfile, subfile_index = self._resolve_subfile(
                line,
                subfile_types,
                subfile_index,
                current_subfile,
            )

            code, value = self._parse_field_line(line, current_subfile)
            if not code:
                continue

            fields.append(_field_from_code(code, value, current_subfile))

        return fields

    def _resolve_subfile(
        self,
        line: str,
        subfile_types: list[str],
        subfile_index: int,
        current_subfile: str,
    ) -> tuple[str, int]:
        if subfile_index + 1 >= len(subfile_types):
            return current_subfile, subfile_index

        next_subfile = subfile_types[subfile_index + 1]

        if len(line) < 3:
            return current_subfile, subfile_index

        if line[:3].startswith(next_subfile) and not self._is_designator_line(line):
            return next_subfile, subfile_index + 1

        return current_subfile, subfile_index

    def _parse_field_line(self, line: str, subfile: str) -> tuple[str, str]:
        if (
            line.startswith(subfile)
            and len(line) >= 5
            and line[2] == subfile[0]
            and subfile in {"DL", "ID"}
        ):
            return line[2:5], line[5:]

        if len(line) < 3:
            return "", ""

        return line[:3], line[3:]

    def _extract_first_body_line(
        self,
        line: str,
        subfile_types: list[str],
    ) -> str:
        marker = subfile_types[0]
        first = line.find(marker)
        second = line.find(marker, first + 2) if first != -1 else -1

        if second != -1:
            return line[second:]

        return ""

    def _is_designator_line(self, line: str) -> bool:
        if len(line) != 10:
            return False

        return line[2:10].isdigit() and line[:2].isalpha()
