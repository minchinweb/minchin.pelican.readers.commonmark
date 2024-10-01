"""
Functionality for after the Markdown has been renders, to prepare it for
Pelican.
"""

import logging
from pathlib import Path

from bs4 import BeautifulSoup

from ..constants import LOG_PREFIX

logger = logging.getLogger(__name__)


def h1_as_title(content, metadata, settings):
    """
    If no title (in metadata), use the first H1 in the output.

    TODO: add a control switch??

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

    relative_path = Path(metadata["path"]).relative_to(settings["PATH"])

    soup = BeautifulSoup(content, settings["COMMONMARK_HTML_PARSER"])
    try:
        title_tag = soup.select("h1")[0]
    except:
        # TODO: fix raw except
        logger.info('%s Cannot pull H1 from "%s".' % (LOG_PREFIX, relative_path))
    else:
        my_title = title_tag.text.strip()
        logger.info(
            '%s title set to "%s" for "%s"' % (LOG_PREFIX, my_title, relative_path)
        )
        metadata["title"] = my_title

        # Remove tag from body (we assume the theme will display it)
        title_tag.decompose()
        content = soup.prettify()

    return content, metadata


def remove_duplicate_h1(content, metadata, settings):
    """
    Remove duplicate H1 tag.

    If the first H1 tag of the generated content matches the title, remove it
    (on the assumption that the template will add the title back).

    TODO: add a control switch??

    Args:
        content (str): HTML rendered body of source.
        metadata (dict): Metadata of content.
        settings (dict): Pelican settings

    Returns:
        content (str): (Updated) HTML rendered body of source.
    """

    # if we don't have a title, do nothing
    if not "title" in metadata.keys():
        return content
    else:
        metadata_title = metadata["title"]
        # metadata_title = metadata_title.strip()
        # # if "title", drop it out of the <p> tag
        # if metadata_title.startswith("<p>") and metadata_title.endswith("</p>"):
        #     metadata_title = metadata_title[3:-4]

    soup = BeautifulSoup(content, settings["COMMONMARK_HTML_PARSER"])
    try:
        title_tag = soup.select("h1")[0]
    except IndexError:
        return content
    else:
        h1_title = title_tag.text.strip()
        # replace m-dash for "raw" version
        h1_title = h1_title.replace("—", "--")
        logger.debug(
            '%s Compare titles: "%s" and "%s"' % (LOG_PREFIX, metadata_title, h1_title)
        )
        if metadata_title == h1_title:
            title_tag.decompose()
            content = soup.prettify()

            relative_path = Path(metadata["path"]).relative_to(settings["PATH"])
            logger.info(
                '%s duplicate H1 (aka "title") removed from "%s"'
                % (LOG_PREFIX, relative_path)
            )

    return content
