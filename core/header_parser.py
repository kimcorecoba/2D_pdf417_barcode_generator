from core.header_info import HeaderInfo


class HeaderParser:

    def parse(self, raw_text: str):

        print("\n===== RAW INPUT TO HEADER PARSER =====")
        print("repr:", repr(raw_text))
        print("length:", len(raw_text))
        print("hex:", raw_text.encode("ascii", errors="replace").hex())
        print("=====================================\n")
 
        text = raw_text.replace("\r", "").replace("\n", "")
        
        

        marker = "ANSI "

        start = text.find(marker)

        if start == -1:
            return None

        start += len(marker)

        iin = text[start:start + 6]

        version = text[start + 6:start + 8]

        jurisdiction_version = text[start + 8:start + 10]

        number_of_entries = int(
            text[start + 10:start + 12]
        )

        subfile_start = start + 12

        file_type = text[
            subfile_start:
            subfile_start + 2
        ]

        return HeaderInfo(
            iin=iin,
            version=version,
            jurisdiction_version=jurisdiction_version,
            number_of_entries=number_of_entries,
            file_type=file_type,
        )
        return None