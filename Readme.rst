CommonMark Reader for Pelican
=============================

*Powered by Markdown-IT*


## Pelican Settings

COMMONMARK = {"plugins": [<plugin classes>], "enable": [<str of name of features>]}
  (To be defined). Used to configure which plugins and extensions are loaded by
  the plugin. The default is available at
  `minchin.pelican.readers.commonmark.constants.COMMONMARK_DEFAULT_CONFIG`.

  This is a dictionary, expecting two keys: ``plugins`` and ``enable``, each
  with a list as the key. For *plugins*, the list items should be the classes of
  the Markdown-IT plugins you want to use. For *enable*, it should be the names
  (as strings) of the Markdown-IT features you want to enable (e.g. `"table"`).

COMMONMARK_VERSION
  Version of the plugin. Inserted by the plugin (if not provided).

COMMONMARK_DEV_URL
  Homepage URL of the plugin. Inserted by the plugin (if not provided).
