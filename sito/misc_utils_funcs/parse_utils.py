def insert_underscore_name(nominativo):
    return "_".join(nominativo.split())


def remove_underscore_name(nominativo):
    return " ".join(nominativo.split("_"))
