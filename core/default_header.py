from core.header_info import HeaderInfo


def default_header():
    return HeaderInfo(
        iin="636000",
        version="10",
        jurisdiction_version="00",
        file_type="DL",
    )