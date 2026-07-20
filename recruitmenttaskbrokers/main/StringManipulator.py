def stripPolishCharacters(text: str) -> str | None:
    """
    Converts polish letters to ASCII counterparts
    :param text: Text to convert
    :return: Text with ASCII characters, or None if text is None
    """
    if str is None:
        return None
    repl = str.maketrans("ąćęłńóśźżĄĆĘŁŃÓŚŹŻ", "acelnoszzACELNOSZZ")
    return text.translate(repl)

