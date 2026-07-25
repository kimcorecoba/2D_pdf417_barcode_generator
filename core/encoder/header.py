from .config import EncoderConfig


class HeaderBuilder:
    """
    Implements the AAMVA 2020 DL/ID Card Design Standard
    Annex D.12.3 - Header.
    """

    def build(
        self,
        config: EncoderConfig,
    ) -> str:
        """
        Build the AAMVA header.
        """

        return (
           f"{config.compliance_indicator}"
           f"{config.data_element_separator}"
           f"{config.record_separator}"
           f"{config.segment_terminator}"
           f"{self._build_header_line(config)}"
        )

    def _build_header_line(
        self,
        config: EncoderConfig,
    ) -> str:
        """
        Build the fixed AAMVA header line.
        """

        return (
            f"ANSI "
            f"{config.issuer_id}"
            f"{config.version}"
            f"{config.jurisdiction_version}"
            f"{config.number_of_entries:02d}"
        )