Changelog for CommonMark
========================

*This is the changelog for ``minchin.pelican.readers.commonmark``, a plugin for
Pelican.*

- :feature:`-` include subscript Markdown extention, on by default (i.e.
  ``~sub~script``). *Note: no superscript support quite yet.*
- :release:`2.0.3 <2025-06-07>`
- :bug:`-` Apply ``highlight`` CSS class to code, so Pelican themes will
  highlight code blocks.

- :release:`2.0.2 <2025-05-19>`
- :bug:`-` Remove warning on internal page links (i.e. ``<a href="#test">``)
- :bug:`-` Hide warnings on disabled built-in Markdown reader (issue starting
  with Pelican v4.10?).

- :release:`2.0.1 <2024-09-30>`
- :bug:`1` Don't complain about local links

- :release:`2.0.0 <2024-03-30>`
- :support:`-` document support for Fancy Tasklists (Markdown) plugin.
- :support:`-` separate Wikilinks processing into it's own (Pelican) `plugin
  <https://github.com/MinchinWeb/minchin.pelican.plugins.wikilinks>`_ (as it
  can't be run as part of the reader because processing the URL of each page is
  needed.)
