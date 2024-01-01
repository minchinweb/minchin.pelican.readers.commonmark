from functools import partial
from itertools import chain
import logging
import os
from pathlib import Path

from ..constants import (
    AUDIO_EXTS,
    GENERATOR_PAGE_LISTS,
    IMAGE_EXTS,
    LOG_PREFIX,
    VIDEO_EXTS,
)
from .regex import wikilink_file_regex, wikilink_regex

logger = logging.getLogger(__name__)

"""
# Test cases
[[my link]]
[[ my work ]]
[[ my work | is finished ]]

![[ a file.jpg ]]
![[file.jpg]]
"""


def _populate_link_pairs(generators):
    """
    Create a dictionary of filenames to final URLs.

    Needs to be run after the source material has been loaded into Pelican, so
    we can use Pelican's calculated URLS, rather than trying to guess what they
    should be.
    """
    logger.info("%s Starting `populate_link_pairs()`.", LOG_PREFIX)
    # for `link_pairs`, the key is the filename (without extension) and the
    # value is the (final) URL that page will be found at.
    link_pairs = {}
    for generator in generators:

        target_list = []
        for my_item in GENERATOR_PAGE_LISTS:
            try:
                target_list.append(getattr(generator, my_item))
            except AttributeError:
                pass

        for file in chain(*target_list):
            link_pairs[Path(file.path).stem] = file.url

    from pprint import pprint

    pprint(link_pairs)
    logger.info("%s %d link pairs found", LOG_PREFIX, len(link_pairs))

    return link_pairs


def _get_file_and_linkname(match):
    """
    Given a "raw" regex match, returns the cleaned up filename (key) and
    linkname (as displayed).
    """
    group = match.groupdict()
    filename = group["filename"].strip()
    linkname = group["linkname"] if group["linkname"] else filename
    linkname = linkname.strip()
    return filename, linkname


def _wikilink_replacement(link_pairs, SITEURL, match):
    filename, linkname = _get_file_and_linkname(match)
    print(f"{filename=}, {linkname=}, {SITEURL=}, {link_pairs=}")
    path = link_pairs.get(filename)

    link_structure = (
        '<a href="{href}" class="wikilinks {wikilinks_class}">{linkname}</a>'.format(
            href=SITEURL + "/" + path if path else "#",
            wikilinks_class="wikilink-found" if path else "wikilink-missing",
            linkname=linkname,
        )
    )

    return link_structure


def _wikilink_file_replacement(link_pairs, SITEURL, match):
    filename, linkname = _get_file_and_linkname(match)

    path = link_pairs.get(filename)
    ext = Path(filename).suffix

    if ext in IMAGE_EXTS:
        link_structure_raw = (
            '<img src="{href}" class="wikilinks {wikilinks_class}" alt="{linkname}" />'
        )
    elif ext in AUDIO_EXTS:
        link_structure_raw = (
            '<audio control src="{href}" class="wikilinks {wikilinks_class}" />'
        )
    elif ext in VIDEO_EXTS:
        link_structure_raw = (
            '<video control src="{href}" class="wikilinks {wikilinks_class}" />'
        )
    else:
        link_structure_raw = (
            '<a href="{href}" class="wikilinks-file {wikilinks_class}">{linkname}</a>'
        )

    link_structure = link_structure_raw.fromat(
        href=SITEURL + "/" + path if path else "#",
        wikilinks_class="wikilink-found" if path else "wikilink-missing",
        linkname=linkname,
    )

    return link_structure


def replace_wikilinks(generators):
    """
    Given a text (i.e. the body of a article or a page), replaces all "raw"
    wikilinks within it, and returns the "fixed" text.

    Doesn't differentiate between wikilinks in the main body of those in code
    blocks, etc.
    """

    link_pairs = _populate_link_pairs(generators)

    for generator in generators:
        for my_item in GENERATOR_PAGE_LISTS:
            try:
                my_article_list = getattr(generator, my_item)
            except AttributeError:
                continue

            for my_article in my_article_list:
                SITEURL = my_article.settings["SITEURL"]

                _file_replacement = partial(
                    _wikilink_file_replacement, link_pairs, SITEURL
                )
                _link_replacement = partial(_wikilink_replacement, link_pairs, SITEURL)

                text = my_article._content
                text = wikilink_file_regex.sub(repl=_file_replacement, string=text)
                text = wikilink_regex.sub(repl=_link_replacement, string=text)
                my_article._content = text
