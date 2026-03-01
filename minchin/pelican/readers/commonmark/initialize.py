import logging

from .constants import (
    COMMONMARK_DEFAULT_CONFIG,
    DEFAULT_TAG_SYMBOLS,
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
    logger.debug("%s massaging settings, setting defaults.", LOG_PREFIX)

    if "COMMONMARK" not in pelican.settings.keys():
        pelican.settings["COMMONMARK"] = COMMONMARK_DEFAULT_CONFIG
        logger.debug("%s COMMONMARK (plugin settings) set to default.", LOG_PREFIX)
    else:
        logger.debug(
            "%s COMMONMARK (plugin settings) previously set manually.", LOG_PREFIX
        )

    if "COMMONMARK_HTML_PARSER" not in pelican.settings.keys():
        if lxml:
            pelican.settings["COMMONMARK_HTML_PARSER"] = "lxml"
        else:
            pelican.settings["COMMONMARK_HTML_PARSER"] = "html.parser"
        logger.debug(
            '%s COMMONMARK_HTML_PARSER set to "%s"',
            LOG_PREFIX, pelican.settings["COMMONMARK_HTML_PARSER"]
        )
    else:
        logger.debug(
            '%s COMMONMARK_HTML_PARSER previously set manually. Is "%s".',
            LOG_PREFIX, pelican.settings["COMMONMARK_HTML_PARSER"]
        )

    if "COMMONMARK_INLINE_TAG_SYMBOLS" not in pelican.settings.keys():
        pelican.settings["COMMONMARK_INLINE_TAG_SYMBOLS"] = DEFAULT_TAG_SYMBOLS
        logger.debug(
            '%s COMMONMARK_INLINE_TAG_SYMBOLS set to default ("%s").',
            LOG_PREFIX, pelican.settings["COMMONMARK_INLINE_TAG_SYMBOLS"]
        )
    else:
        logger.debug(
            '%s COMMONMARK_INLINE_TAG_SYMBOLS (plugin settings) previously set manually to "%s".',
            LOG_PREFIX, pelican.settings["COMMONMARK_INLINE_TAG_SYMBOLS"]
        )

    if (
        "COMMONMARK_MARKDOWN_LOG_LEVEL" in pelican.settings.keys()
        and pelican.settings["COMMONMARK_MARKDOWN_LOG_LEVEL"]
    ):
        logging.getLogger("markdown_it").setLevel(
            pelican.settings["COMMONMARK_MARKDOWN_LOG_LEVEL"]
        )
    else:
        pelican.settings["COMMONMARK_MARKDOWN_LOG_LEVEL"] = logging.WARNING
    logger.debug(
        '%s COMMONMARK_MARKDOWN_LOG_LEVEL set to "%s"',
        LOG_PREFIX, pelican.settings["COMMONMARK_MARKDOWN_LOG_LEVEL"]
    )

    # doesn't work, as we can't access it later through the Pelican settings
    if "COMMONMARK_DEBUG_LINKS" not in pelican.settings.keys():
        pelican.settings["COMMONMARK_DEBUG_LINKS"] = True
    logger.debug(
        '%s COMMONMARK_DEBUG_LINKS set to "%s"',
        LOG_PREFIX, pelican.settings["COMMONMARK_DEBUG_LINKS"]
    )
    global COMMONMARK_DEBUG_LINKS
    COMMONMARK_DEBUG_LINKS = pelican.settings["COMMONMARK_DEBUG_LINKS"]

def commonmark_version(pelican):
    """
    Insert CommonMark (plugin) version into Pelican context.
    """

    if "COMMONMARK_VERSION" not in pelican.settings.keys():
        pelican.settings["COMMONMARK_VERSION"] = __version__
        logger.debug(
            '%s Adding CommonMark version "%s" to context.',
            LOG_PREFIX, pelican.settings["COMMONMARK_VERSION"]
        )
    else:
        logger.debug(
            '%s COMMONMARK_VERSION already defined. Is "%s".',
            LOG_PREFIX, pelican.settings["COMMONMARK_VERSION"]
        )

    if "COMMONMARK_DEV_URL" not in pelican.settings.keys():
        pelican.settings["COMMONMARK_DEV_URL"] = __url__
        logger.debug(
            '%s Adding CommonMark Dev URL "%s" to context.',
            LOG_PREFIX, pelican.settings["COMMONMARK_DEV_URL"]
        )
    else:
        logger.debug(
            '%s COMMONMARK_DEV_URL already defined. Is "%s".',
            LOG_PREFIX, pelican.settings["COMMONMARK_DEV_URL"]
        )
