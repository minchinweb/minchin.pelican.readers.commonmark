import logging

from bs4 import BeautifulSoup
from markdown_it import MarkdownIt
from pygments import highlight
from pygments.formatters.html import HtmlFormatter
from pygments.lexers import get_lexer_by_name, guess_lexer
from pygments.lexers.special import TextLexer
from pygments.util import ClassNotFound

from pelican.readers import DUPLICATES_DEFINITIONS_ALLOWED, BaseReader, MarkdownReader
from pelican.utils import pelican_open

from .constants import LOG_PREFIX

logger = logging.getLogger(__name__)


class MDITReader(BaseReader):
    enabled = True
    # file_extensions = ["md", "markdown", "mkd", "mdown"]
    extensions = None

    # use the same file extensions as the build-in Markdown Reader
    _pelican_markdown_reader = MarkdownReader({"MARKDOWN": {}})
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

        # setup our CommonMark (Markdown) processor
        md = MarkdownIt("commonmark")

        # add extensions, aka Markdown-IT plugins
        if (
            "extensions" in self.settings["COMMONMARK"]
            and self.settings["COMMONMARK"]["extensions"]
        ):
            for my_extension in self.settings["COMMONMARK"]["extensions"]:
                logger.info(
                    '%s Enabling Markdown-IT plugin: "%s"'
                    % (LOG_PREFIX, str(my_extension))
                )
                md = md.use(my_extension)
        else:
            logger.warning(
                '%s Unable to set Markdown-IT extensions: "%s"'
                % (LOG_PREFIX, "extensions" in self.settings["COMMONMARK"])
            )
            logger.warning("%s" % (self.settings["COMMONMARK"]))

        # enable tables, etc
        if (
            "enable" in self.settings["COMMONMARK"]
            and self.settings["COMMONMARK"]["enable"]
        ):
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
            logger.warning("%s" % (self.settings["COMMONMARK"]))

        # add in our processors for links
        md.add_render_rule("link_open", render_pelican_link)

        md.add_render_rule("image", render_pelican_image)
        md.add_render_rule("fence", render_fence)

        # ---
        # open our source file
        with pelican_open(filename) as fp:
            # text = list(fp.splitlines())
            text = fp

        # process metadata
        metadata = {}
        content = None

        formatted_fields = self.settings["FORMATTED_FIELDS"]

        # check if we have the front-matter extension (aka plugin) active
        _front_matter_extension_active = False
        if "extensions" in self.settings["COMMONMARK"]:
            for my_extension in self.settings["COMMONMARK"]["extensions"]:
                if my_extension.__name__ == "front_matter_plugin":
                    _front_matter_extension_active = True
                    break

        front_matter_text = ""
        if _front_matter_extension_active:
            # TODO: pull front matter and body without having to render the
            # Markdown twice
            md_tokens = md.parse(text)
            for my_token in md_tokens:
                if my_token.type == "front_matter":
                    front_matter_text = my_token.content
                    front_matter_text = front_matter_text.splitlines()
                    # assumes a single Front Matter block
                    break
        else:
            front_matter_text = list(text.splitlines())

        # TODO: use a YAML reader from front matter?
        # c.f. https://github.com/Python-Markdown/markdown/blob/master/markdown/extensions/meta.py
        for i, line in enumerate(front_matter_text):
            kv = line.split(":", 1)
            if len(kv) == 2:
                name, value = kv[0], kv[1]
                name = name.lower().strip()
                value = value.strip()
                # value = value.split(",")
                # logger.warning("%s %s %s %s" % (LOG_PREFIX, filename, name, value))

                if name in formatted_fields:
                    # formatted metadata is special case and join all list values
                    formatted_values = "\n".join(value)
                    formatted = md.render(formatted_values)
                    metadata[name] = self.process_metadata(name, formatted)
                # elif not DUPLICATES_DEFINITIONS_ALLOWED.get(name, True):
                #     if len(value) > 1:
                #         logger.warning(
                #             '%s Duplicate definition of "%s" '
                #             'for "%s". Using first one.',
                #             LOG_PREFIX,
                #             name,
                #             filename,
                #         )
                #     metadata[name] = self.process_metadata(name, value[0])
                # elif len(value) > 1:
                #     # handle list metadata as list of string
                #     metadata[name] = self.process_metadata(name, value)
                else:
                    # otherwise, handle metadata as single string
                    # metadata[name] = self.process_metadata(name, value[0])
                    metadata[name] = self.process_metadata(name, value)
            else:
                # after first line that isn't in key:value format, dump the
                # rest into "content"
                content = "\n".join(text[i:])
                break

        # if using Pelican-style (parsed here) front matter, just render the
        # "body" in markdown. If we're using the Markdown-IT front-matter
        # plugin, we render the whole thing as it won't print the front matter.
        if _front_matter_extension_active:
            md_base_content = text
        else:
            md_base_content = content

        md_content = md.render(md_base_content)

        # TODO: add control switch
        # if no title, use the first H1 in the output
        if "title" not in metadata.keys():
            soup = BeautifulSoup(md_content, self.settings["COMMONMARK_HTML_PARSER"])
            try:
                title_tag = soup.select("h1")[0]
            except:
                logger.info('%s Cannot pull H1 from "%s".' % (LOG_PREFIX, filename))
            else:
                my_title = title_tag.text.strip()
                logger.info(
                    '%s title set to "%s" for "%s"' % (LOG_PREFIX, my_title, filename)
                )
                metadata["title"] = my_title

                # Remove tag from body (we assume the theme will display it)
                title_tag.decompose()
                md_content = soup.prettify()

        return md_content, metadata


def add_commonmark_reader(readers):
    for ext in MDITReader.file_extensions:
        readers.reader_classes[ext] = MDITReader
