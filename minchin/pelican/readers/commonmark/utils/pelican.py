from datetime import date, datetime
import logging

from pelican.contents import Author, Tag
from pelican.readers import _DISCARD, MarkdownReader, ensure_metadata_list
from pelican.utils import SafeDatetime, get_date

from ..constants import LOG_PREFIX

logger = logging.getLogger(__name__)


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
    logger.log(5, f"{LOG_PREFIX} clean_dates() in {value} {type(value)}")

    return_value = None
    return_case = 0
    if isinstance(value, SafeDatetime):
        return_value = value
        return_case = 1
    # need to do datetime before date
    elif isinstance(value, datetime):
        return_value = SafeDatetime(
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
        return_case = 3
    elif isinstance(value, date):
        return_value = SafeDatetime(value.year, value.month, value.day)
        return_case = 2
    elif isinstance(value, str):
        return_value = get_date(value.replace("_", " "))
        return_case = 4
    else:
        # raise error?
        return_value = value
        return_case = 5

    logger.log(5, f"{LOG_PREFIX} clean_dates() out {return_value} {type(return_value)} via {return_case}")
    return return_value

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
