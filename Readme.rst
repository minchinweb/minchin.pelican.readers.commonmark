CommonMark Reader for Pelican
=============================

*Powered by Markdown-IT*

This plugin is intended to be a roughly drop-in replacement for Pelican's
built-in Markdown Reader (the "reader" is the part of Pelican that turns your
source files into something Pelican can assemble into a website.) As this uses
a CommonMark implementation of Markdown, there are be subtle differences when
compared to the output of Pelican's built in Markdown Reader; if you are
particular about your site output, it may require building the site with the
two readers, and running a diff on the two outputs, and tweaking your source
files (or adding Markdown plugins here) until the output is what you want.

When I set out to build this plugin, I (naively) thought I would stick to a
"pure" CommonMark/Markdown implementation, but I quickly realized that I like
the extensions to Markdown I use, and I wasn't ready to give them up. That
said, I've tried to keep them generally mild. The default configuration will
automatically include all the plugins that I use by default, although you can
add or remove from that list as you wish. Currently enabled CommonMark
extensions:

- front matter
- footnotes
- defintion list
- tables

Changes Required from "Vanilla" Pelican
---------------------------------------

This plugin uses the Markdown-IT front matter by default. This expects front
matter (metadata) to be at the top of the file, between lines of three dashes
(e.g. ``---``). ("Vanilla" Pelican doesn't require these marker lines.)

An example::

  ---
  title: Frontmatter Test
  Category: test
  date: 2023-11-19 14:56
  ---

  This is a test of the frontmatter plugin.

If you don't want to (or can't) update your source files, you can provide a
customized ``COMMONMARK`` settings (in your ``pelicanconf.py``) that doesn't
include the frontmatter plugin.

If the frontmatter plugin is not active, the plugin should parse metadata in
the same matter as "vanilla" Pelican.

Pelican Settings
----------------

COMMONMARK = {"extensions": [<plugin classes>], "enable": [<str of name of features>]}
  (To be defined). Used to configure which CommonMark extensions are loaded by
  the plugin. The default is available at
  `minchin.pelican.readers.commonmark.constants.COMMONMARK_DEFAULT_CONFIG`.

  This is a dictionary, expecting two keys: ``extensions`` and ``enable``, each
  with a list as the key. For *extensions*, the list items should be the
  classes of the Markdown-IT plugins (aka "extensions") you want to use. For
  *enable*, it should be the names (as strings) of the Markdown-IT features you
  want to enable (e.g. ``"table"``).

COMMONMARK_VERSION
  Version of the plugin. Inserted by the plugin (if not provided).

COMMONMARK_DEV_URL
  Homepage URL of the plugin. Inserted by the plugin (if not provided).

COMMONMARK_HTML_PARSER = "html.parser"
  Will be set to "lxml" is it is installed. This is the parser that Beautiful
  Soup uses.

COMMONMARK_MARKDOWN_LOG_LEVEL = logging.WARNING
  If you want to see the debugging for the Markdown-IT library change this to
  ``logging.DEBUG`` (but be warned that it is *very* verbose).

COMMONMARK_INLINE_TAG_SYMBOLS = "#"
  Tag symbols used before inline tags. If a line contains only tags, it will be
  removed from the body of the entry.
