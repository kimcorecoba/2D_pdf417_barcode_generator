from .header import HeaderBuilder
from .config import EncoderConfig
from .subfile import SubfileBuilder
from .body import BodyBuilder


class AAMVAEncoder:

    def encode(self, fields, header=None):

        from core.aamva_versions import (
            ISSUER_ID,
            AAMVA_VERSION,
        )

        if header:
            config = EncoderConfig(
                issuer_id=header.iin,
                version=header.version,
                jurisdiction_version=header.jurisdiction_version,
                number_of_entries=header.number_of_entries,
            )
            subfile_types = self._resolve_subfile_types(fields, header)
        else:
            config = EncoderConfig(
                issuer_id=ISSUER_ID,
                version=AAMVA_VERSION,
            )
            subfile_types = self._resolve_subfile_types(fields, None)

        header_text = HeaderBuilder().build(config)
        body_builder = BodyBuilder()

        bodies = [
            body_builder.build_subfile(subfile_type, fields, config)
            for subfile_type in subfile_types
        ]

        designator_block_size = 10 * len(subfile_types)
        offset = len(header_text) + designator_block_size

        subfile_designators = []
        for subfile_type, body in zip(subfile_types, bodies):
            subfile_designators.append(
                SubfileBuilder().build(
                    file_type=subfile_type,
                    offset=offset,
                    length=len(body),
                )
            )
            offset += len(body)

        payload = header_text + "".join(subfile_designators) + "".join(bodies)
        return payload

    def _resolve_subfile_types(self, fields, header) -> list[str]:
        if header and header.subfiles:
            return [subfile.file_type for subfile in header.subfiles]

        subfile_types = []
        seen = set()

        for field in fields:
            if field.subfile not in seen:
                subfile_types.append(field.subfile)
                seen.add(field.subfile)

        if not subfile_types:
            return ["DL"]

        return subfile_types
