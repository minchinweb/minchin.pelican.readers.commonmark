from datetime import date, datetime

from pelican.contents import Author, Tag
from pelican.readers import _DISCARD, MarkdownReader, ensure_metadata_list
from pelican.utils import SafeDatetime, get_date


def get_markdown_file_extensions():
    """
    Return the list of file extensions the Reader should load for.

    By default, we use the same ones used by the default Markdown Reader.
    Default list (as of Pelican 4.9.1) is `md`, `markdown`, `mkd`, and `mdown`.

    TODO: Allow this to be configured?
    """

    _pelican_markdown_reader = MarkdownReader({"MARKDOWN": {}})
    return _pelican_markdown_reader.file_extensions

def clean_dates(value, settings=dict()):
    """
    Given a value, tries to turn it into a datetime.

    This is needed because our YAML frontmatter reader will transform some
    strings directly into datetime.datetime (or datetime.date), but the
    BaseReader always expects to be provided a string.
    """
    if isinstance(value, SafeDatetime):
        return value
    elif isinstance(value, date):
        return SafeDatetime(value.year, value.month, value.day)
    elif isinstance(value, datetime):
        return SafeDatetime(
            value.year,
            value.month,
            value.day,
            value.hour,
            value.minute,
            value.second,
            value.microsecond,
            value.tzinfo,
            fold=value.fold,
        )
    elif isinstance(value, str):
        return get_date(value.replace("_", " "))
    else:
        # raise error?
        return value


def clean_tags(value, settings=dict()):
    """
    Given a value (a list), tries to turn it into a list of tags.

    This is needs because our YAML frontmatter reader will transform an empty
    list into `None`.
    """
    if value is None:
        return _DISCARD

    return [Tag(tag, settings) for tag in ensure_metadata_list(value)] or _DISCARD


def clean_authors(value, settings=dict()):
    """
    Given a value (a list), tries to turn it into a list of authors.

    This is needs because our YAML frontmatter reader will transform an empty
    list into `None`.
    """
    if value is None:
        return _DISCARD

    return [Author(tag, settings) for tag in ensure_metadata_list(value)] or _DISCARD
