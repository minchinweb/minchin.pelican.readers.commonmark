from pelican import signals

from .constants import __version__  # NOQA
from .reader import add_commonmark_reader

def register():
    """Register the plugin pieces with Pelican."""
    signals.readers_init.connect(add_commonmark_reader)
