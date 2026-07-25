from core.header_info import HeaderInfo


class HeaderParser:

    def parse(self, raw_text: str):

        lines = raw_text.splitlines()

        for line in lines:

            line = line.strip()

            if line.startswith("ANSI"):

                data = line[4:].strip()

                iin = data[0:6]
                version = data[6:8]
                jurisdiction_version = data[8:12]

                next_line = lines[lines.index(line) + 1].strip()
                file_type = next_line[:2]

                return HeaderInfo(
                    iin=iin,
                    version=version,
                    jurisdiction_version=jurisdiction_version,
                    file_type=file_type,
                )
        return None