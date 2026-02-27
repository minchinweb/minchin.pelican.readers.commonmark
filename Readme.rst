CommonMark Reader for Pelican
=============================

*Powered by Markdown-IT-Py*

This plugin is intended to be a roughly drop-in replacement for Pelican's
built-in Markdown Reader (the "reader" is the part of Pelican that turns your
source files into something Pelican can assemble into a website). As this uses
a CommonMark implementation of Markdown (specifically, `markdown-it-py
<https://github.com/executablebooks/markdown-it-py>`_, there are be subtle
differences when compared to the output of Pelican's built in Markdown Reader
(which relies on `Python-Markdown <https://python-markdown.github.io/>`_);
if you are particular about your site output, it may require building the site
with the two readers, and running a diff on the two outputs, and tweaking your
source files (or adding Markdown plugins here) until the output is what you
want.

When I set out to build this plugin, I (naively) thought I would stick to a
"pure" CommonMark/Markdown implementation, but I quickly realized that I like
the extensions to Markdown I use, and I wasn't ready to give them up. That
said, I've tried to keep them generally mild. The default configuration will
automatically include all the plugins that I use by default, although you can
add or remove from that list as you wish. Currently enabled CommonMark
extensions (and features) are:

- front matter
- footnotes
- defintion list
- tables
- strikethrough/delete
- subscript
- superscript

Changes Required from "Vanilla" Pelican
---------------------------------------

This (Pelican) plugin uses the Markdown-IT front matter (plugin) by default.
This expects front matter (i.e. metadata) to be at the top of the file, between
lines of three dashes (e.g. ``---``). ("Vanilla" Pelican doesn't require these
marker lines.) Front matter is then phrased as YAML.

An example::

  ---
  title: Front matter Test
  Category: test
  date: 2023-11-19 14:56
  ---

  This is a test of the front matter plugin.

If you don't want to (or can't) update your source files, you can provide a
customized ``COMMONMARK`` settings (in your ``pelicanconf.py``) that doesn't
include the frontmatter plugin.

If the frontmatter plugin is not active, the plugin should parse metadata in
the same matter as "vanilla" Pelican. Note that this has been less tested, as I
personally use the front matter plugin.

To rely on "vanilla Pelican" front matter (generally, not recommended):

.. code-block:: python

    # pelicanconf.py

    from minchin.pelican.readers.commonmark.constants import COMMONMARK_DEFAULT_CONFIG

    # other Pelican settings

    # start with default configuration
    COMMONMARK = COMMONMARK_DEFAULT_CONFIG
    # add remove Markdown-IT's front matter plugin
    for i, plugin in enumerate(COMMONMARK["extensions"]):
        if plugin.__name__ == "front_matter_plugin":
            del a["extensions"][i]

Additional Features
-------------------

In addition to the "base" CommonMark parser/render, this Reader offers the
following additional features:

- Title from H1: if a post's title isn't defined in the metadata block, it will
  try and pull a title from the first H1 tag in the body of the entry.
- Remove duplicated H1 title: If the first H1 tag in the post matches the title
  as defined in the metadata block, it will remove the H1 tag. It is assumed
  that the theme will include the title as a H1 tag in the generated site.
- Relative links ready for Pelican: relative links included in the body of
  posts will have ``{filename}`` or ``{static}`` prefixed to them, so that
  Pelican can maintain these links even if the generated site has a different
  layout from your source files.
- Code block highlighting: Pygments is called to allow code block syntax
  highlighting. Generated site HTML will display code highlighting if you
  include (or link to) a Pygments CSS file.
- removes "tag only" lines from the body of your entries.
- "cleans" dates provided in front matter, so they are provided to Pelican as
  ``datetimes`` rather than strings.

Pelican Settings
----------------

COMMONMARK = {"extensions": [<plugin classes>], "enable": [<str of name of features>]}
  (To be defined). Used to configure which CommonMark extensions are loaded by
  the plugin. The default is available at
  ``minchin.pelican.readers.commonmark.constants.COMMONMARK_DEFAULT_CONFIG``.

  This is a dictionary, expecting two keys: ``extensions`` and ``enable``, each
  with a list as the key. For *extensions*, the list items should be the
  classes of the Markdown-IT plugins (aka "extensions") you want to use. For
  *enable*, it should be the names (as strings) of the Markdown-IT features you
  want to enable (e.g. ``"table"``).

COMMONMARK_VERSION
  Version of the plugin. Idea is to have it available to displayed by the
  theme. Inserted by the plugin (if not provided).

COMMONMARK_DEV_URL
  Homepage URL of the plugin. Idea is to have it available to be used by the
  theme. Inserted by the plugin (if not provided).

COMMONMARK_HTML_PARSER = "html.parser"
  Will be set to "lxml" is it is installed. This is the parser that Beautiful
  Soup uses.

COMMONMARK_MARKDOWN_LOG_LEVEL = logging.WARNING
  If you want to see the debugging for the Markdown-IT library change this to
  ``logging.DEBUG`` (but be warned that it is *very* verbose).

COMMONMARK_INLINE_TAG_SYMBOLS = "#"
  Tag symbols used before inline tags. If a line contains only tags, it will be
  removed from the body of the entry.

Extended Abilities
------------------

I have written a *markdown-it-py* plugin to support "fancy"
tasklists/checkboxes, but it is not activated by default.

This requires separate installation and activation within *Pelican*, which you
might do like this:

.. code-block:: python

    # pelicanconf.py

    from minchin.pelican.readers.commonmark.constants import COMMONMARK_DEFAULT_CONFIG
    import minchin.md_it.fancy_tasklists

    # other Pelican settings

    # start with default configuration
    COMMONMARK = COMMONMARK_DEFAULT_CONFIG
    # add fancy tasklists
    COMMONMARK["extensions"].append(
        minchin.md_it.fancy_tasklists.fancy_tasklists_plugin,
    )

See `sample rendered checkboxes
<https://github.com/MinchinWeb/seafoam/blob/master/docs/screenshots/2.10.0/fancy-checkboxes.png>`_.


I have also ported a plugin to support inserted text using double pluses
(``++inserted++``), but this is not activated by default. To enable:

.. code-block:: python

    # pelicanconf.py, as above

    import minchin.md_it.insert

    # add insert plugin
    COMMONMARK["extensions"].append(
        minchin.md_it.insert.insert_plugin,
    )



Prior Art
---------

This plugin relies on much work that has gone before, both explicitly for code
and implicitely for the encouragement of this even being possible. This list is
sadly incomplete, but in particlar:

- Johnathan Sundqvist's `Obisidian Plugin for Pelican
  <https://github.com/jonathan-s/pelican-obsidian>`_ (and forks) -- in
  particular, for providing inspiration on how to deal with Wiki-style links

.. To Implement/Fix
.. ----------------


