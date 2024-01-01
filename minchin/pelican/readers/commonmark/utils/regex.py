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


_base_wikilink_regex = (
    r"\[\[\s*(?P<filename>[^|\]]+)(\|\s*(?P<linkname>[^|\]\n\r]+))?\]\]"
)
wikilink_regex = re.compile(_base_wikilink_regex)
wikilink_file_regex = re.compile(r"!" + _base_wikilink_regex)
