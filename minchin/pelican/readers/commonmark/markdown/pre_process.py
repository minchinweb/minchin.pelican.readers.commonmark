"""
Functionality run before the Markdown render is run.

- pull front matter from Source file.
- take tag only lines and add them to metadata and remove them from the body
"""

import logging
import re

import yaml

from pelican.contents import Tag

from ..constants import LOG_PREFIX
from ..utils.regex import markdown_header_regex, tag_only_line_regex, tag_regex

logger = logging.getLogger(__name__)


def read_front_matter(self, raw_text, metadata, md):
    """
    Read front matter and split from main body text.

    Args:
        self (pelican.reader.BaseReader): used to pull settings, and
        process_metadata() function.
        raw_text (str): Raw, unprocessed source text (likely in raw Markdown)
        md (markdown_it.MarkdownIT): Markdown renderer

    Returns:
        content (str): Raw source text, now without metadata
        metadata (dict): Metadata of the source text.
    """
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
        md_tokens = md.parse(raw_text)
        for my_token in md_tokens:
            if my_token.type == "front_matter":
                front_matter_text = my_token.content
                front_matter_text = front_matter_text.splitlines()
                # assumes a single Front Matter block
                break

        logger.log(5, "%s raw Front Matter: %s" % (LOG_PREFIX, front_matter_text))

        # Use YAML to read front matter
        front_matter_joined_test = "\n".join(front_matter_text)
        metadata = yaml.load(front_matter_joined_test, Loader=yaml.Loader)

        if metadata is None:
            metadata = {}

        for k, v in metadata.copy().items():
            if k in formatted_fields:
                # formatted metadata is special case and join all list
                # values
                if isinstance(v, list | set):
                    formatted_values = "\n".join(v)
                else:
                    formatted_values = v
                formatted = md.render(formatted_values)
                # drop final newline
                formatted = formatted.strip()
                # if anything but "summary", drop it out of the <p> tag
                if (
                    k != "summary"
                    and formatted.startswith("<p>")
                    and formatted.endswith("</p>")
                ):
                    formatted = formatted[3:-4].strip()
                metadata[k] = self.process_metadata(k, formatted)
            # elif not DUPLICATES_DEFINITIONS_ALLOWED.get(k, True):
            #     if len(v) > 1:
            #         logger.warning(
            #             '%s Duplicate definition of "%s" '
            #             'for "%s". Using first one.',
            #             LOG_PREFIX,
            #             k,
            #             filename,
            #         )
            #     metadata[k] = self.process_metadata(k, v[0])
            # elif len(v) > 1:
            #     # handle list metadata as list of string
            #     metadata[k] = self.process_metadata(k, v)
            else:
                # otherwise, handle metadata as single string
                # metadata[k] = self.process_metadata(k, v[0])
                metadata[k] = self.process_metadata(k, v)

        md_base_content = raw_text

    else:
        # This is kept here, and is assumed to work, but not well tested. Use
        # with caution.
        front_matter_text = list(raw_text.splitlines())

        for i, line in enumerate(front_matter_text):
            kv = line.split(":", 1)
            if len(kv) == 2:
                name, value = kv[0], kv[1]
                name = name.lower().strip()
                value = value.strip()
                # value = value.split(",")
                # logger.warning("%s %s %s %s" % (LOG_PREFIX, filename, name, value))
                # print(i, line, kv, name, value)

                if name in formatted_fields:
                    # formatted metadata is special case and join all list
                    # values
                    if isinstance(value, list | set):
                        formatted_values = "\n".join(value)
                    else:
                        formatted_values = value
                    formatted = md.render(formatted_values)
                    # drop final newline
                    formatted = formatted.strip()
                    # if "title", drop it out of the <p> tag
                    if (
                        name == "title"
                        and formatted.startswith("<p>")
                        and formatted.endswith("</p>")
                    ):
                        formatted = formatted[3:-4].strip()
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
                content = "\n".join(raw_text[i:])
                break

        md_base_content = content

    logging.log(5, "%s processed Metadata: %s" % (LOG_PREFIX, metadata))

    # if using Pelican-style (parsed here) front matter, just render the
    # "body" in markdown. If we're using the Markdown-IT front-matter
    # plugin, we render the whole thing as it won't print the front matter.
    return md_base_content, metadata


def remove_tag_only_lines(self, raw_text):
    """
    Read front matter and split from main body text.

    Args:
        self (pelican.reader.BaseReader): used to pull settings
        raw_text (str): Raw, unprocessed source text (likely in raw Markdown)

    Returns:
        content (str): Raw source text, now without tags
        metadata (dict): Metadata of the source text.
    """
    # what level to log this function at
    # 5 is below "DEBUG" level
    LOG_LEVEL = 5

    # find all tags
    tag_symbols = self.settings["COMMONMARK_INLINE_TAG_SYMBOLS"]
    found_raw_tags = [tag for tag in re.findall(tag_regex(tag_symbols), raw_text)]
    logger.log(LOG_LEVEL, "tags 1 %s" % found_raw_tags)

    # reject tag if it is only a series of hashmarks (used for headers in
    # Markdown)
    found_raw_tags = [
        tag for tag in found_raw_tags if not markdown_header_regex().match(tag)
    ]
    logger.log(LOG_LEVEL, "tags 2 %s" % found_raw_tags)

    # convert to lowercase
    found_raw_tags = [tag.lower() for tag in found_raw_tags]
    logger.log(LOG_LEVEL, "tags 3 %s" % found_raw_tags)

    # remove the tag symbol from the front of the tag.
    # Assume it is only a single tag symbol
    tag_symbols_tuple = tuple(char for char in tag_symbols)
    found_raw_tags = [
        # tag.lstrip(tag_symbols) for tag in found_raw_tags
        tag[1:]
        for tag in found_raw_tags
        if tag.startswith(tag_symbols_tuple)
    ]
    logger.log(LOG_LEVEL, "tags 4 %s" % found_raw_tags)

    # remove empty tags, like blank strings
    found_raw_tags = [tag for tag in found_raw_tags if tag]
    logger.log(LOG_LEVEL, "tags 5 %s" % found_raw_tags)

    # remove duplicates
    found_raw_tags = set(found_raw_tags)
    logger.log(LOG_LEVEL, "tags 6 %s" % found_raw_tags)

    # convert to Pelican tags
    found_tags = [Tag(tag, self.settings) for tag in found_raw_tags]
    logger.log(LOG_LEVEL, "tags 7 %r" % found_raw_tags)

    # remove tag-only lines
    raw_text_2 = []
    multi_tag_regex = tag_only_line_regex(tag_symbols)
    # logger.log(LOG_LEVEL, "tags 8 %s" % raw_text)
    for line in raw_text.splitlines():
        logger.log(
            LOG_LEVEL, "tags 9 %s %s" % (bool(multi_tag_regex.match(line)), line)
        )
        if multi_tag_regex.match(line):
            # line = ""
            raw_text_2.append("")
            logger.log(LOG_LEVEL, "tags 9a skipping this line!")
        else:
            raw_text_2.append(line)

    # convert "raw text" back from a list to a string
    raw_text_3 = "\n".join(raw_text_2)

    return raw_text_3, found_tags
