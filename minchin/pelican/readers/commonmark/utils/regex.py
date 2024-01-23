import re


def tag_regex(tag_symbols):
    """
    Compile tag symbol regex.

    Used for pulling out inline tags.
    """
    pattern = rf"(?<!\S)([{tag_symbols}][-+*#/\w]+)"
    return re.compile(pattern)


def tag_only_line_regex(tag_symbols):
    """
    Compile tag-only line regex.

    Used to find and remove tag-only lines within the body of the document.
    """
    pattern = rf"^\s*([{tag_symbols}][-+*#/\w]+\s*)+$"
    return re.compile(pattern)


def markdown_header_regex():
    """
    Compile header hashmark regex.

    Used to find when we have just the multiple hashmarks used to denote a
    Markdown header.
    """
    pattern = r"#+$"
    return re.compile(pattern)
