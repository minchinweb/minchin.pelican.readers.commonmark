"""
Functions related to rendering the Markdown (technically, CommonMark).
"""

from pygments import highlight
from pygments.formatters.html import HtmlFormatter
from pygments.lexers import get_lexer_by_name, guess_lexer
from pygments.lexers.special import TextLexer
from pygments.util import ClassNotFound


def _maintain_pelican_placeholders(original_url) -> str:
    """
    Maintains the placeholders Pelican has for internal linking.

    This is needed as the brackets {} get converted otherwise by the
    Markdown-IT generator.
    """

    new_url = original_url
    for placeholder in (
        "author",
        "category",
        "index",
        "tag",
        "filename",
        "static",
        "attach",
    ):
        new_url = new_url.replace("%7B" + placeholder + "%7D", "{" + placeholder + "}")
        new_url = new_url.replace("%7C" + placeholder + "%7C", "{" + placeholder + "}")
    return new_url


def render_link_open(self, tokens, idx, options, env):
    """
    Changes how the opening of link tags are rendered; i.e. `<a>` html tags.

    In particular, this maintains the placeholders Pelican has for links.
    """

    tokens[idx].attrSet(
        "href", _maintain_pelican_placeholders(tokens[idx].attrGet("href"))
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
        lexer = TextLexer
    return lexer


def render_fence(self, tokens, idx, options, env):
    """
    Changes how fences (e.g. code blocks) are rendered.

    In particular, applies Pygments html classes, to allow code highlighting.
    """

    token = tokens[idx]
    lexer = _get_lexer(token.info, token.content)
    output = highlight(
        token.content,
        lexer,
        HtmlFormatter(cssclass="codehilite", wrapcode=True),
    )
    return output
