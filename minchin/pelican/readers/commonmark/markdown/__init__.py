"""
Functions related to rendering the Markdown (technically, CommonMark).
"""

import logging

from pygments import highlight
from pygments.formatters.html import HtmlFormatter
from pygments.lexers import get_lexer_by_name, guess_lexer
from pygments.lexers.special import TextLexer
from pygments.util import ClassNotFound

from ..constants import LOG_PREFIX, PELICAN_LINK_PLACEHOLDERS, SOURCE_EXTS, STATIC_EXTS

logger = logging.getLogger(__name__)

EXPANDED_PELICAN_LINK_PLACEHOLDERS = [
    "{" + x.lower() + "}" for x in PELICAN_LINK_PLACEHOLDERS
]
EXPANDED_PELICAN_LINK_PLACEHOLDERS = tuple(EXPANDED_PELICAN_LINK_PLACEHOLDERS)


def _maintain_pelican_placeholders(original_url) -> str:
    """
    Maintains the placeholders Pelican has for internal linking.

    This is needed as the brackets {} get converted otherwise by the
    Markdown-IT generator.
    """

    new_url = original_url
    for placeholder in PELICAN_LINK_PLACEHOLDERS:
        new_url = new_url.replace("%7B" + placeholder + "%7D", "{" + placeholder + "}")
        new_url = new_url.replace("%7C" + placeholder + "%7C", "{" + placeholder + "}")
    return new_url


def _relative_links_for_pelican(original_url):
    """
    If given a relative URL, convert to a format Pelican can link to.

    We assume that any link NOT starting with `http://`, `https://` or `//` is
    a relative link. If that link is to a Markdown (or ReStructured Text) file,
    we preface the destination URL with `{filename}` so Pelican will link to
    the file, whereever it ends up in the rendered site. If the file is at
    image, then we preface with "{static}" instead.
    """

    test_url = original_url.lower()
    # remove in-page targets
    test_url, _, _ = test_url.partition("#")
    # remove query strings
    test_url, _, _ = test_url.partition("?")

    # assumed external links
    if test_url.startswith((
        "http://",
        "https://",
        "//",
        "mailto:",
        "tel:",
        "geo:",
        "#",
    )):
        new_url = original_url

    # assumed in-page links (i.e. `#test`)
    elif test_url == "" and original_url.startswith("#"):
        new_url = original_url

    # don't double up on placeholders
    elif test_url.startswith(EXPANDED_PELICAN_LINK_PLACEHOLDERS):
        new_url = original_url

    elif test_url.endswith(SOURCE_EXTS):
        new_url = "{filename}" + original_url

    elif test_url.endswith(STATIC_EXTS):
        new_url = "{static}" + original_url

    else:
        logger.warning(
            '%s Don\'t know what to do with link target "%s".'
            % (LOG_PREFIX, original_url)
        )
        # early exit
        return original_url

    if new_url == original_url:
        logger.debug('%s Link "%s" unchanged.' % (LOG_PREFIX, new_url))
    else:
        logger.debug('%s Link "%s" --> "%s"' % (LOG_PREFIX, original_url, new_url))
    return new_url


def render_link_open(self, tokens, idx, options, env):
    """
    Changes how the opening of link tags are rendered; i.e. `<a>` html tags.

    In particular, this maintains the placeholders Pelican has for links.
    """

    tokens[idx].attrSet(
        "href", _maintain_pelican_placeholders(tokens[idx].attrGet("href"))
    )
    tokens[idx].attrSet(
        "href", _relative_links_for_pelican(tokens[idx].attrGet("href"))
    )
    # pass token to default renderer.
    return self.renderToken(tokens, idx, options, env)


def render_image(self, tokens, idx, options, env):
    """
    Changes how images are rendered; i.e. `<img>` html tags.

    In particular, this maintains the placeholders Pelican has for image
    sources.
    """

    tokens[idx].attrSet(
        "src", _maintain_pelican_placeholders(tokens[idx].attrGet("src"))
    )
    tokens[idx].attrSet("src", _relative_links_for_pelican(tokens[idx].attrGet("src")))
    # pass token to default renderer.
    return self.image(tokens, idx, options, env)


def _get_lexer(info, content):
    """
    Determine Pygments lexer.
    """

    try:
        if info and info != "":
            lexer = get_lexer_by_name(info)
        else:
            lexer = guess_lexer(content)
    except ClassNotFound:
        lexer = TextLexer()
    return lexer


def render_fence(self, tokens, idx, options, env):
    """
    Changes how fences (e.g. code blocks) are rendered.

    In particular, applies Pygments html classes, to allow code highlighting.
    """

    token = tokens[idx]
    lexer = _get_lexer(token.info, token.content)

    logger.log(
        5, '%s token.content: "%s", lexer: %s' % (LOG_PREFIX, token.content, lexer)
    )

    # if no code to highlight, bail here
    if not token.content:
        return ""

    output = highlight(
        token.content,
        lexer,
        HtmlFormatter(cssclass="codehilite highlight", wrapcode=True),
    )
    return output
