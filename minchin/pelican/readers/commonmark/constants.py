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

IMAGE_EXTS = tuple(
    [
        ".gif",
        ".tif",
        ".tiff",
        ".webp",
        ".jpg",
        ".jpeg",
        ".png",
        # ".pdf",
        ".svg",
    ]
)
VIDEO_EXTS = tuple(
    [
        ".mp4",
    ]
)
AUDIO_EXTS = tuple(
    [
        ".mp3",
        ".flac",
    ]
)
_OTHER_STATIC_EXTS = tuple(
    [
        ".pdf",
    ]
)

STATIC_EXTS = IMAGE_EXTS + VIDEO_EXTS + AUDIO_EXTS + _OTHER_STATIC_EXTS

PELICAN_LINK_PLACEHOLDERS = [
    "author",
    "category",
    "index",
    "tag",
    "filename",
    "static",
    "attach",
]

DEFAULT_TAG_SYMBOLS = "#"

GENERATOR_PAGE_LISTS = [
    "articles",
    "translations",
    "hidden_articles",
    "hidden_translations",
    "drafts",
    "draft_translations",
    "pages",
    "hidden_pages",
    "draft_pages",
    "staticfiles",
]
