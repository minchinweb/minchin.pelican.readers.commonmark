from markdown_it import MarkdownIt
from mdit_py_plugins.deflist import deflist_plugin
from mdit_py_plugins.footnote import footnote_plugin
from pygments import highlight
from pygments.formatters.html import HtmlFormatter
from pygments.lexers import get_lexer_by_name, guess_lexer
from pygments.lexers.special import TextLexer
from pygments.util import ClassNotFound

from pelican.readers import BaseReader, MarkdownReader
from pelican.utils import pelican_open

from .constants import LOG_PREFIX
import logging

logger = logging.getLogger(__name__)


class MDITReader(BaseReader):
    enabled = True
    # file_extensions = ["md", "markdown", "mkd", "mdown"]
    file_extensions = []  # placeholder
    extensions = None

    # use the same file extensions as the build-in Markdown Reader
    _pelican_markdown_reader= MarkdownReader({"MARKDOWN": {}})
    file_extensions = _pelican_markdown_reader.file_extensions
    del _pelican_markdown_reader


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        settings = self.settings["COMMONMARK"]


    def read(self, filename):
        def replace_pelican_placeholders(original_url) -> str:
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
                new_url = new_url.replace(
                    "%7B" + placeholder + "%7D", "{" + placeholder + "}"
                )
                new_url = new_url.replace(
                    "%7C" + placeholder + "%7C", "{" + placeholder + "}"
                )
            return new_url

        def render_pelican_link(self, tokens, idx, options, env):
            tokens[idx].attrSet(
                "href", replace_pelican_placeholders(tokens[idx].attrGet("href"))
            )
            # pass token to default renderer.
            return self.renderToken(tokens, idx, options, env)

        def render_pelican_image(self, tokens, idx, options, env):
            tokens[idx].attrSet(
                "src", replace_pelican_placeholders(tokens[idx].attrGet("src"))
            )
            # pass token to default renderer.
            return self.image(tokens, idx, options, env)

        def get_lexer(info, content):
            try:
                if info and info != "":
                    lexer = get_lexer_by_name(info)
                else:
                    lexer = guess_lexer(content)
            except ClassNotFound:
                lexer = TextLexer
            return lexer

        def render_fence(self, tokens, idx, options, env):
            token = tokens[idx]
            lexer = get_lexer(token.info, token.content)
            output = highlight(
                token.content,
                lexer,
                HtmlFormatter(cssclass="codehilite", wrapcode=True),
            )
            return output
        

        with pelican_open(filename) as fp:
            text = list(fp.splitlines())

        content = None
        metadata = {}
        for i, line in enumerate(text):
            kv = line.split(":", 1)
            if len(kv) == 2:
                name, value = kv[0].lower(), kv[1].strip()
                metadata[name] = self.process_metadata(name, value)
            else:
                content = "\n".join(text[i:])
                break

        md = (
            MarkdownIt("commonmark")
        )
        
        # add plugins
        if "plugins" in self.settings["COMMONMARK"] and self.settings["COMMONMARK"]["plugins"]:
            for my_plugin in self.settings["COMMONMARK"]["plugins"]:
                logger.info(
                    '%s Enabling Markdown-IT plugin: "%s"'
                    % (LOG_PREFIX, str(my_plugin))
                )
                md = md.use(my_plugin)
        else:
            logger.warning(
                '%s Unable to set Markdown-IT plugins: "%s"'
                % (LOG_PREFIX, "plugins" in self.settings["COMMONMARK"])
            )
            logger.warning('%s' % (self.settings["COMMONMARK"]))

        # enable tables, etc
        if "enable" in self.settings["COMMONMARK"] and self.settings["COMMONMARK"]["enable"]:
            for my_enable in self.settings["COMMONMARK"]["enable"]:
                logger.info(
                    '%s Enabling Markdown-IT feature: "%s"'
                    % (LOG_PREFIX, str(my_enable))
                )
                md = md.enable(my_enable)  
        else:
            logger.warning(
                '%s Unable to enable Markdown-IT features. "%s"'
                % (LOG_PREFIX, "enable" in self.settings["COMMONMARK"])
            )
            logger.warning('%s' % (self.settings["COMMONMARK"]))

        # add in our processors for links
        md.add_render_rule("link_open", render_pelican_link)

        md.add_render_rule("image", render_pelican_image)
        md.add_render_rule("fence", render_fence)

        output = md.render(content)

        return output, metadata


def add_commonmark_reader(readers):
    for ext in MDITReader.file_extensions:
        readers.reader_classes[ext] = MDITReader
