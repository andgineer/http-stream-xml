"""Stream XML tags extractor.

Do not need to parse all a XML document if you only need tags from beginning of it.
"""
import xml.sax
from typing import Any, Dict, Optional, Sequence
from xml.sax.xmlreader import XMLReader


class ExtractionCompleted(Exception):
    """Raised when all tags are found."""


class XmlStreamExtractor:
    """Extract given tags from XML streamed to it by chunks (in method feed).

    When all tags are found, extraction_completed is True.
    Found tags would be available in dict tags.
    """

    def __init__(self, tags_to_collect: Sequence[str]) -> None:
        """Initialize XML parser with given tags to collect."""
        self.stream_handler = StreamHandler(tags_to_collect)
        self.parser: XMLReader = xml.sax.make_parser()
        self.parser.setContentHandler(self.stream_handler)  # type: ignore
        self.extraction_completed = False

    def feed(self, chunk: str) -> None:
        """Feed next part of XML into the parser.

        :param chunk: XML document part
        :return: None
        """
        try:
            self.parser.feed(chunk)  # type: ignore
        except ExtractionCompleted:
            self.extraction_completed = True

    @property
    def tags(self) -> Dict[str, str]:
        """Return found tags."""
        parser_tags = self.stream_handler.tags
        return {tag: "".join(values) for tag, values in parser_tags.items()}


class StreamHandler(xml.sax.handler.ContentHandler):
    """XML parser handler to collect given tags.

    When all tags are found, raises ExtractionCompleted.
    """

    def __init__(self, tags_to_collect: Sequence[str]) -> None:
        """Initialize XML parser handler with given tags to collect."""
        self.tags_to_collect = tags_to_collect

        self.tags: Dict[str, Any] = {}
        self.tag_started: Optional[str] = None
        super().__init__()

    def startElement(self, name: str, attrs: Any) -> None:
        """Start tag handler."""
        if name in self.tags_to_collect:
            self.tag_started = name
            self.tags[name] = []

    def extraction_completed(self) -> bool:
        """Check if all tags are found."""
        return len(self.tags) == len(self.tags_to_collect)

    def endElement(self, name: str) -> None:
        """End tag handler."""
        if name in self.tags_to_collect:
            self.tag_started = None
            if self.extraction_completed():
                raise ExtractionCompleted()

    def characters(self, content: Any) -> None:
        """Tag content handler."""
        if self.tag_started:
            self.tags[self.tag_started].append(content)
