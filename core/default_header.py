from core.header_info import HeaderInfo


def default_header():
    return HeaderInfo(
        iin="636000",
        version="10",
        jurisdiction_version="00",
        number_of_entries=1,
        file_type="DL",
    )