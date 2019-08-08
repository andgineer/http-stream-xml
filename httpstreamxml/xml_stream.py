import xml.sax


class XmlStreamExtractor:
    """
    Extract given tags from XML streamed to it by chunks (in method feed).
    Raise StopIteration when all tag are found.

    Found tags are available in dict tags
    """
    def __init__(self, tags_to_collect):
        self.stream_handler = StreamHandler(tags_to_collect)
        self.parser = xml.sax.make_parser()
        self.parser.setContentHandler(self.stream_handler)

    def feed(self, chunk):
        self.parser.feed(chunk)

    @property
    def tags(self):
        parser_tags = self.stream_handler.tags
        return {tag: ''.join(values) for tag, values in parser_tags.items()}


class StreamHandler(xml.sax.handler.ContentHandler):
    def __init__(self, tags_to_collect):
        self.tags_to_collect = tags_to_collect

        self.tags = {}
        self.tag_started = None
        super().__init__()

    def startElement(self, name, attrs):
        if name in self.tags_to_collect :
            self.tag_started = name
            self.tags[name] = []

    def endElement(self, name):
        if name in self.tags_to_collect:
            self.tag_started = None
            if len(self.tags) == len(self.tags_to_collect):
                raise StopIteration

    def characters(self, content):
        if self.tag_started:
            self.tags[self.tag_started].append(content)
