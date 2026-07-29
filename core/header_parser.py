from core.header_info import HeaderInfo
from core.subfile_info import SubfileInfo


class HeaderParser:

    def parse(self, raw_text: str) -> HeaderInfo | None:

        text = raw_text.replace("\r", "").replace("\n", "")

        marker = "ANSI "

        start = text.find(marker)

        if start == -1:
            return None

        start += len(marker)

        iin = text[start:start + 6]
        version = text[start + 6:start + 8]
        jurisdiction_version = text[start + 8:start + 10]
        number_of_entries = int(text[start + 10:start + 12])

        subfile_start = start + 12
        subfiles = []

        for _ in range(number_of_entries):
            if subfile_start + 10 > len(text):
                break

            file_type = text[subfile_start:subfile_start + 2]
            offset = int(text[subfile_start + 2:subfile_start + 6])
            length = int(text[subfile_start + 6:subfile_start + 10])

            subfiles.append(
                SubfileInfo(
                    file_type=file_type,
                    offset=offset,
                    length=length,
                )
            )
            subfile_start += 10

        file_type = subfiles[0].file_type if subfiles else "DL"

        return HeaderInfo(
            iin=iin,
            version=version,
            jurisdiction_version=jurisdiction_version,
            number_of_entries=number_of_entries,
            file_type=file_type,
            subfiles=subfiles,
        )
