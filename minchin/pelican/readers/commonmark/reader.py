import logging

from bs4 import BeautifulSoup
from markdown_it import MarkdownIt

from pelican.readers import (
    _DISCARD,
    DUPLICATES_DEFINITIONS_ALLOWED,
    METADATA_PROCESSORS,
    BaseReader,
    MarkdownReader,
)
from pelican.utils import file_suffix, pelican_open

from .constants import LOG_PREFIX
from .markdown import render_fence, render_image, render_link_open
from .markdown.post_process import h1_as_title, remove_duplicate_h1
from .markdown.pre_process import read_front_matter, remove_tag_only_lines
from .utils.pelican import (
    clean_authors,
    clean_dates,
    clean_tags,
    get_markdown_file_extensions,
)
from .utils.reader import load_enables, load_extensions

logger = logging.getLogger(__name__)

# use custom date cleaner
# TODO: Allow runtime appending to this list
METADATA_PROCESSORS_MDIT = METADATA_PROCESSORS.copy()
METADATA_PROCESSORS_MDIT["date"] = clean_dates
METADATA_PROCESSORS_MDIT["modified"] = clean_dates
METADATA_PROCESSORS_MDIT["tags"] = clean_tags
METADATA_PROCESSORS_MDIT["authors"] = clean_authors
# TODO: Move this back to the TaskNotes plugin
METADATA_PROCESSORS_MDIT["threshold"] = clean_dates
METADATA_PROCESSORS_MDIT["threshold_date"] = clean_dates
METADATA_PROCESSORS_MDIT["scheduled"] = clean_dates
METADATA_PROCESSORS_MDIT["due"] = clean_dates
METADATA_PROCESSORS_MDIT["cancelled"] = clean_dates
METADATA_PROCESSORS_MDIT["completed"] = clean_dates


class MDITReader(BaseReader):
    enabled = True
    file_extensions = get_markdown_file_extensions()
    extensions = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        settings = self.settings["COMMONMARK"]

    def read(self, source_path):
        # rename variable so signature matches BaseReader
        filename = source_path

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

        # preprocess
        content, tag_list = remove_tag_only_lines(self, raw_text)
        content, metadata = read_front_matter(
            self=self,
            raw_text=content,
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
        # TODO: at both keys??
        metadata["source_path"] = filename

        # process (the Markdown)
        html_content = md.render(content)

        # postprocess
        html_content, metadata = h1_as_title(html_content, metadata, self.settings)
        html_content = remove_duplicate_h1(html_content, metadata, self.settings)

        # Remove frame `<html>` and `<body>` tags, as we assume those will be
        # added by the theme and we just want the HTML fragment here. These
        # will be added by certain BeautifulSoup parsers (`lxml`, `html5lib`)
        # if there are missing.
        soup = BeautifulSoup(html_content, self.settings["COMMONMARK_HTML_PARSER"])
        try:
            html_content = soup.body.encode_contents()
        except AttributeError as e:
            # raise Exception(
            #     "Your 'soup' doesn't have a `body` tag. Try a different parser "
            #     "for BeautifulSoup? (Like the `lxml` one?)"
            # ) from e
            pass
        else:
            # back to UTF-8 (from bytes)
            html_content = html_content.decode()
        # if we don't have a `body` tag, nothing needs to be done here

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


def silence_builtin_reader_warning(readers):
    """
    Pelican's built-in Markdown Reader (which we are not using) with throw
    an warning message for each Markdown file not processed through it
    (i.e. for all of them). This skips those.

    This became an issue after Pelican v4.9.1 and by v4.11.0.

    Ugg...monkey-patching...
    """

    def check_file_patched(source_path: str) -> None:
        """Log a warning if a file is processed by a disabled reader."""
        reader = readers.disabled_readers.get(file_suffix(source_path), None)
        if reader and not isinstance(reader, MarkdownReader):
            logger.warning(f"{source_path}: {reader.disabled_message()}")
            print(reader)

    readers.check_file = check_file_patched
