"""
Functionality for after the Markdown has been renders, to prepare it for
Pelican.
"""
import logging

from bs4 import BeautifulSoup

from .constants import LOG_PREFIX

logger = logging.getLogger(__name__)


def h1_as_title(content, metadata, settings):
    """
    If no title (in metadata), use the first H1 in the output.

    TODO: add control switch??

    Args:
        content (str): HTML rendered body of source.
        metadata (dict): Metadata of content.
        settings (dict): Pelican settings

    Returns:
        content (str): (Updated) HTML rendered body of source.
        metadata (dict): (Updated) metadata of content.
    """

    # if we already have a title, do nothing
    if "title" in metadata.keys():
        return content, metadata

    soup = BeautifulSoup(content, settings["COMMONMARK_HTML_PARSER"])
    try:
        title_tag = soup.select("h1")[0]
    except:
        logger.info('%s Cannot pull H1 from "%s".' % (LOG_PREFIX, metadata["path"]))
    else:
        my_title = title_tag.text.strip()
        logger.info(
            '%s title set to "%s" for "%s"' % (LOG_PREFIX, my_title, metadata["path"])
        )
        metadata["title"] = my_title

        # Remove tag from body (we assume the theme will display it)
        title_tag.decompose()
        content = soup.prettify()

    return content, metadata
