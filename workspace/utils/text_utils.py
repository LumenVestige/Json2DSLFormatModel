import string


def text_is_empty(str: string) -> bool:
    if str is None:
        return True
    if len(str) == 0:
        return True
    return False
