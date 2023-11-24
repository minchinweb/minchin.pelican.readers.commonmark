"""
Functions to extend the CommonMark Reader functionality.
"""
import logging

from pelican.readers import DUPLICATES_DEFINITIONS_ALLOWED, BaseReader, MarkdownReader

from .constants import LOG_PREFIX

logger = logging.getLogger(__name__)


def get_file_extensions():
    """
    Return the list of file extensions the Reader should load for.

    By default, we use the same ones used by the default Markdown Reader.
    Default list (as of Pelican 4.9.1) is `md`, `markdown`, `mkd`, and `mdown`.

    TODO: Allow this to be configured?
    """

    _pelican_markdown_reader = MarkdownReader({"MARKDOWN": {}})
    return _pelican_markdown_reader.file_extensions


def load_extensions(md, settings):
    """
    Loads out desired extensions to Markdown, i.e. Markdown-IT plugins.

    Args:
        md (markdown_it.MarkdownIT): Markdown render
        settings (dict): Pelican settings

    Returns:
        markdown_it.MarkdownIT: (Updated) Markdown render
    """

    commonmark_settings = settings["COMMONMARK"]

    if "extensions" in commonmark_settings and commonmark_settings["extensions"]:
        for my_extension in commonmark_settings["extensions"]:
            logger.info(
                '%s Enabling Markdown-IT plugin: "%s"' % (LOG_PREFIX, str(my_extension))
            )
            md = md.use(my_extension)
    else:
        logger.warning(
            '%s Unable to set Markdown-IT extensions: "%s"'
            % (LOG_PREFIX, "extensions" in commonmark_settings)
        )
        logger.warning("%s" % (commonmark_settings))

    return md


def load_enables(md, settings):
    """
    Enables desired features of Markdown-IT, e.g. tables.

    Args:
        md (markdown_it.MarkdownIT): Markdown render
        settings (dict): Pelican settings

    Returns:
        markdown_it.MarkdownIT: (Updated) Markdown render
    """

    commonmark_settings = settings["COMMONMARK"]
    if "enable" in commonmark_settings and commonmark_settings["enable"]:
        for my_enable in commonmark_settings["enable"]:
            logger.info(
                '%s Enabling Markdown-IT feature: "%s"' % (LOG_PREFIX, str(my_enable))
            )
            md = md.enable(my_enable)
    else:
        logger.warning(
            '%s Unable to enable Markdown-IT features. "%s"'
            % (LOG_PREFIX, "enable" in commonmark_settings)
        )
        logger.warning("%s" % (commonmark_settings))

    return md
