import logging

from .constants import (
    COMMONMARK_DEFAULT_CONFIG,
    COMMONMARK_MARKDOWN_DEBUG,
    LOG_PREFIX,
    __url__,
    __version__,
)

try:
    import lxml
except ImportError:
    lxml = None

logger = logging.getLogger(__name__)


def check_settings(pelican):
    """
    Insert defaults in Pelican settings, as needed.
    """
    logger.debug("%s massaging settings, setting defaults." % LOG_PREFIX)

    if not "COMMONMARK" in pelican.settings.keys():
        pelican.settings["COMMONMARK"] = COMMONMARK_DEFAULT_CONFIG
        logger.debug("%s COMMONMARK (plugin settings) set to default." % (LOG_PREFIX))
    else:
        logger.debug(
            "%s COMMONMARK (plugin settings) previously set manually." % (LOG_PREFIX)
        )

    if not "COMMONMARK_HTML_PARSER" in pelican.settings.keys():
        if lxml:
            pelican.settings["COMMONMARK_HTML_PARSER"] = "lxml"
        else:
            pelican.settings["COMMONMARK_HTML_PARSER"] = "html.parser"
        logger.debug(
            '%s COMMONMARK_HTML_PARSER set to "%s"'
            % (LOG_PREFIX, pelican.settings["COMMONMARK_HTML_PARSER"])
        )
    else:
        logger.debug(
            '%s COMMONMARK_HTML_PARSER previously set manually. Is "%s".'
            % (LOG_PREFIX, pelican.settings["COMMONMARK_HTML_PARSER"])
        )

    if "COMMONMARK_MARKDOWN_LOG_LEVEL" in pelican.settings.keys() and pelican.settings["COMMONMARK_MARKDOWN_LOG_LEVEL"]:
        logging.getLogger("markdown_it").setLevel(pelican.settings["COMMONMARK_MARKDOWN_LOG_LEVEL"])
    else:
        pelican.settings["COMMONMARK_MARKDOWN_LOG_LEVEL"] = logging.WARNING
    logger.debug(
        '%s COMMONMARK_MARKDOWN_LOG_LEVEL set to "%s"'
        % (LOG_PREFIX, pelican.settings["COMMONMARK_MARKDOWN_LOG_LEVEL"])
    )


def commonmark_version(pelican):
    """
    Insert CommonMark (plugin) version into Pelican context.
    """

    if "COMMONMARK_VERSION" not in pelican.settings.keys():
        pelican.settings["COMMONMARK_VERSION"] = __version__
        logger.debug(
            '%s Adding CommonMark version "%s" to context.'
            % (LOG_PREFIX, pelican.settings["COMMONMARK_VERSION"])
        )
    else:
        logger.debug(
            '%s COMMONMARK_VERSION already defined. Is "%s".'
            % (LOG_PREFIX, pelican.settings["COMMONMARK_VERSION"])
        )

    if "COMMONMARK_DEV_URL" not in pelican.settings.keys():
        pelican.settings["COMMONMARK_DEV_URL"] = __url__
        logger.debug(
            '%s Adding CommonMark Dev URL "%s" to context.'
            % (LOG_PREFIX, pelican.settings["COMMONMARK_DEV_URL"])
        )
    else:
        logger.debug(
            '%s COMMONMARK_DEV_URL already defined. Is "%s".'
            % (LOG_PREFIX, pelican.settings["COMMONMARK_DEV_URL"])
        )
