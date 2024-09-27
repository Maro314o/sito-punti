def insert_underscore_name(nominativo: str) -> str:
    return "_".join(nominativo.split())


def remove_underscore_name(nominativo: str) -> str:
    return " ".join(nominativo.split("_"))
