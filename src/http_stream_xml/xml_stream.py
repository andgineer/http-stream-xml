"""Stream XML tags extractor.

Do not need to parse all a XML document if you only need tags from beginning of it.
"""
import contextlib
import xml.sax
from xml.sax.xmlreader import XMLReader


class XmlStreamExtractor:
    """Extract given tags from XML streamed to it by chunks (in method feed).

    Raise StopIteration when all tag are found.

    Found tags would be available in dict tags
    """

    def __init__(self, tags_to_collect):
        """Initialize XML parser with given tags to collect."""
        self.stream_handler = StreamHandler(tags_to_collect)
        self.parser: XMLReader = xml.sax.make_parser()
        self.parser.setContentHandler(self.stream_handler)

    def feed(self, chunk):
        """Feed next part of XML into the parser.

        :param chunk: XML document part
        :return: None
        """
        with contextlib.suppress(StopIteration):
            self.parser.feed(chunk)

    @property
    def tags(self):
        """Return found tags."""
        parser_tags = self.stream_handler.tags
        return {tag: "".join(values) for tag, values in parser_tags.items()}


class StreamHandler(xml.sax.handler.ContentHandler):
    """XML parser handler to collect given tags."""

    def __init__(self, tags_to_collect):
        """Initialize XML parser handler with given tags to collect."""
        self.tags_to_collect = tags_to_collect

        self.tags = {}
        self.tag_started = None
        super().__init__()

    def startElement(self, name, attrs):
        """Start tag handler."""
        if name in self.tags_to_collect:
            self.tag_started = name
            self.tags[name] = []

    def extraction_completed(self):
        """Check if all tags are found."""
        return len(self.tags) == len(self.tags_to_collect)

    def endElement(self, name):
        """End tag handler."""
        if name in self.tags_to_collect:
            self.tag_started = None
            if self.extraction_completed():
                raise StopIteration

    def characters(self, content):
        """Tag content handler."""
        if self.tag_started:
            self.tags[self.tag_started].append(content)
