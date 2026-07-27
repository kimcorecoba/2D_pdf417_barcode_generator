class SubfileBuilder:
    """
    Builds the AAMVA Subfile Designator.
    """

    def build(
        self,
        file_type: str,
        offset: int,
        length: int,
    ) -> str:
        
        
        return (
            f"{file_type}"
            f"{offset:04d}"
            f"{length:04d}"
        )