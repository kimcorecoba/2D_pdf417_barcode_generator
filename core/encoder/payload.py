from .header import HeaderBuilder
from .config import EncoderConfig
from .subfile import SubfileBuilder
from .body import BodyBuilder

class AAMVAEncoder:

    def encode(self, fields, header=None):
        print(type(header))
        print(header)

        from core.aamva_versions import (
            ISSUER_ID,
            AAMVA_VERSION,
            FILE_TYPE,
        )

        if header:
           config = EncoderConfig(
                issuer_id=header.iin,
                version=header.version,
                jurisdiction_version=header.jurisdiction_version,
                number_of_entries=header.number_of_entries,
            )
            
        else:
            config = EncoderConfig(
                issuer_id=ISSUER_ID,
                version=AAMVA_VERSION,
            )
       

        header_text = HeaderBuilder().build(config)
        
        print("\n=== Fields being encoded ===")

        for field in fields:
            print(f"{field.code}: {repr(field.value)}")

        print("============================\n")

        body_text = BodyBuilder().build(
            fields,
            config,
        )
        
        print("\n=== PayloadBuilder ===")
        print("len(body_text) =", len(body_text))
        print("Last 40 chars:", repr(body_text[-40:]))
        print("======================")
        print("\n===== GENERATED BODY =====")
        print(body_text)
        print("==========================\n")
        
        subfile_length = (
            2               # "DL"
            + len(body_text)
                     # Segment Terminator (CR)
        )

        placeholder = SubfileBuilder().build(
            file_type=header.file_type if header else config.file_type,
            offset=0,
            length=subfile_length,
        )

        subfile_offset = len(header_text) + len(placeholder)

        subfile = SubfileBuilder().build(
            file_type=header.file_type if header else config.file_type,
            offset=subfile_offset,
            length=subfile_length,
        )

        payload = (
            header_text
            + subfile
            + body_text
        )
        
        print("Header length:", len(header_text))
        print("Subfile length:", len(subfile))
        print("Body length:", len(body_text))
        print("Calculated offset:", subfile_offset)
        
        print("\n===== GENERATED PAYLOAD (repr) =====")
        print(repr(payload))
        print("Payload length:", len(payload))
        print("====================================\n")
        
        print("\n===== GENERATED PAYLOAD (hex) =====")
        print(payload.encode("ascii").hex())
        print("===================================\n")
        
        return payload