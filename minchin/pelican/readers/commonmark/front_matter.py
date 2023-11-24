"""
Functionality to pull front matter from Source file.
"""


def read_front_matter(self, raw_text, md):
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
    metadata = {}

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
    else:
        front_matter_text = list(raw_text.splitlines())

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
            # print(i, line, kv, name, value)

            if name in formatted_fields:
                # formatted metadata is special case and join all list
                # values
                if isinstance(value, list | set):
                    formatted_values = "\n".join(value)
                else:
                    formatted_values = value
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
            content = "\n".join(raw_text[i:])
            break

    # if using Pelican-style (parsed here) front matter, just render the
    # "body" in markdown. If we're using the Markdown-IT front-matter
    # plugin, we render the whole thing as it won't print the front matter.
    if _front_matter_extension_active:
        md_base_content = raw_text
    else:
        md_base_content = content

    return md_base_content, metadata
