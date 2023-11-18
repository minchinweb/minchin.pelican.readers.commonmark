import mdit_py_plugins.deflist
import mdit_py_plugins.footnote

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
    ],
    "enable": [
        "table",
    ],
}
