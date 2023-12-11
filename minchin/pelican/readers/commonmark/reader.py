from copy import copy
import logging

from bs4 import BeautifulSoup
from markdown_it import MarkdownIt

from pelican.readers import (
    _DISCARD,
    DUPLICATES_DEFINITIONS_ALLOWED,
    METADATA_PROCESSORS,
    BaseReader,
)
from pelican.utils import pelican_open

from .constants import LOG_PREFIX
from .markdown import render_fence, render_image, render_link_open
from .post_process import h1_as_title, remove_duplicate_h1
from .pre_process import read_front_matter, remove_tag_only_lines
from .reader_utils import (
    clean_authors,
    clean_dates,
    clean_tags,
    get_file_extensions,
    load_enables,
    load_extensions,
)

logger = logging.getLogger(__name__)

# use custom date cleaner
METADATA_PROCESSORS_MDIT = METADATA_PROCESSORS.copy()
METADATA_PROCESSORS_MDIT["date"] = clean_dates
METADATA_PROCESSORS_MDIT["modified"] = clean_dates
METADATA_PROCESSORS_MDIT["tags"] = clean_tags
METADATA_PROCESSORS_MDIT["authors"] = clean_authors


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

        content, tag_list = remove_tag_only_lines(self, raw_text)
        content, metadata = read_front_matter(
            self=self,
            raw_text=raw_text,
            # metadata=copy(metadata),
            metadata=dict(),
            md=md,
        )

        # add back in the found tags
        if tag_list and ("tags" not in metadata.keys() or metadata["tags"] == _DISCARD):
            metadata["tags"] = []
        for tag in tag_list:
            metadata["tags"].append(tag)

        # add path to metadata
        metadata["path"] = filename

        html_content = md.render(content)

        html_content, metadata = h1_as_title(html_content, metadata, self.settings)
        html_content = remove_duplicate_h1(html_content, metadata, self.settings)

        return html_content, metadata

    def process_metadata(self, name, value):
        # here because we need to handle dates, passed to us as dates
        # also, lowercase key name for processing

        if name.lower() in METADATA_PROCESSORS_MDIT:
            value_2 = METADATA_PROCESSORS_MDIT[name.lower()](value, self.settings)
        else:
            value_2 = value

        logger.log(
            5,
            '%s process metadata: "%s": "%s" %s --> "%s" %s / %s'
            % (
                LOG_PREFIX,
                name,
                value,
                type(value),
                value_2,
                type(value_2),
                name in METADATA_PROCESSORS_MDIT,
            ),
        )

        return value_2


def add_commonmark_reader(readers):
    for ext in MDITReader.file_extensions:
        readers.reader_classes[ext] = MDITReader
