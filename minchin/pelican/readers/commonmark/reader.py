import logging

from bs4 import BeautifulSoup
from markdown_it import MarkdownIt

from pelican.readers import DUPLICATES_DEFINITIONS_ALLOWED, BaseReader
from pelican.utils import pelican_open

from .constants import LOG_PREFIX
from .front_matter import read_front_matter
from .markdown import render_fence, render_image, render_link_open
from .post_process import h1_as_title, remove_duplicate_h1
from .reader_utils import get_file_extensions, load_enables, load_extensions

logger = logging.getLogger(__name__)


class MDITReader(BaseReader):
    enabled = True
    file_extensions = get_file_extensions()
    extensions = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        settings = self.settings["COMMONMARK"]

    def read(self, filename):
        # setup our CommonMark (Markdown) processor
        md = MarkdownIt("commonmark")
        md = load_extensions(md, self.settings)
        md = load_enables(md, self.settings)
        # add in our processors for links, etc
        md.add_render_rule("link_open", render_link_open)
        md.add_render_rule("image", render_image)
        md.add_render_rule("fence", render_fence)

        # ---
        # open our source file
        with pelican_open(filename) as fp:
            # text = list(fp.splitlines())
            raw_text = fp

        content, metadata = read_front_matter(self, raw_text, md)

        # add path to metadata
        metadata["path"] = filename

        html_content = md.render(content)

        html_content, metadata = h1_as_title(html_content, metadata, self.settings)
        html_content = remove_duplicate_h1(html_content, metadata, self.settings)

        # print(metadata)
        # print(md_content)
        # print()
        return html_content, metadata


def add_commonmark_reader(readers):
    for ext in MDITReader.file_extensions:
        readers.reader_classes[ext] = MDITReader
