import mdit_py_plugins.deflist
import mdit_py_plugins.footnote
import mdit_py_plugins.front_matter

__title__ = "minchin.pelican.readers.commonmark"
__version__ = "2.0.0"
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

STATIC_EXTS = tuple(
    [
        # images
        ".gif",
        ".tif",
        ".tiff",
        ".webp",
        ".jpg",
        ".jpeg",
        ".png",
        ".svg",
        # video
        ".mp4",
        # audio
        ".mp3",
        ".flac",
        # other
        ".pdf",
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
