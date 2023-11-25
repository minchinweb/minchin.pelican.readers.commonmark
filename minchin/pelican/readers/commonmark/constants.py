import logging

import mdit_py_plugins.deflist
import mdit_py_plugins.footnote
import mdit_py_plugins.front_matter

__title__ = "minchin.pelican.readers.commonmark"
__version__ = "2.0.0-dev"
__description__ = "CommonMark Reader for Pelican (via Markdown-IT)"
__author__ = "W. Minchin"
__email__ = "w_minchin@hotmail.com"
__url__ = "http://blog.minchin.ca/label/commonmark-pelican/"
__license__ = "MIT License"

LOG_PREFIX = "[CommonMark]"

COMMONMARK_DEFAULT_CONFIG = {
    "extensions": [
        mdit_py_plugins.deflist.deflist_plugin,
        mdit_py_plugins.footnote.footnote_plugin,
        mdit_py_plugins.front_matter.front_matter_plugin,
    ],
    "enable": [
        "table",
    ],
}

COMMONMARK_MARKDOWN_DEBUG = [
    #     (logging.DEBUG, 'entering fence'),
    #     (logging.DEBUG, 'entering hr'),
    #     (logging.DEBUG, 'entering blockquote'),
    #     (logging.DEBUG, 'entering lheading'),
    #     (logging.DEBUG, 'entering paragraph'),
    #     (logging.DEBUG, 'entering list'),
    #     (logging.DEBUG, 'entering html_block'),
    #     (logging.DEBUG, 'entering reference'),
]

SOURCE_EXTS = tuple(
    [
        ".md",
        ".markdown",
        ".mkd",
        ".mdown",
        ".rst",
        ".rest",
        ".htm",
        ".html",
    ]
)

STATIC_EXTS = tuple(
    [
        ".gif",
        ".tif",
        ".tiff",
        ".webp",
        ".jpg",
        ".jpeg",
        ".png",
        ".pdf",
        ".svg",
        ".mp3",
        ".mp4",
    ]
)

PELICAN_LINK_PLACEHOLDERS = [
    "author",
    "category",
    "index",
    "tag",
    "filename",
    "static",
    "attach",
]
