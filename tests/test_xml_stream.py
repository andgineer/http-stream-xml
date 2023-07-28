import pytest
from io import StringIO
from xml.sax import SAXParseException

from http_stream_xml.xml_stream import XmlStreamExtractor


def test_simple_extraction():
    xml_data_1st_chunk = """
    <root>
        <name>John Doe</name>
        <age>30</age>"""
    xml_data_2nd_chunk = """
        <city>New York</city>
    </root>
    """

    tags_to_collect = {"name", "age"}
    extractor = XmlStreamExtractor(tags_to_collect)

    xml_data = f"{xml_data_1st_chunk}{xml_data_2nd_chunk}"
    chunk_size = len(xml_data_1st_chunk) // 2
    read_size = 0
    with StringIO(xml_data) as f:
        while True:
            chunk = f.read(chunk_size)
            read_size += chunk_size
            if not chunk or "age" in extractor.tags:
                break
            extractor.feed(chunk)

    expected_tags = {"name": "John Doe", "age": "30"}
    assert extractor.tags == expected_tags
    assert read_size < len(xml_data)


def test_no_tags_found():
    xml_data = """
    <root>
        <city>New York</city>
        <country>United States</country>
    </root>
    """

    tags_to_collect = {"name", "age"}
    extractor = XmlStreamExtractor(tags_to_collect)

    with StringIO(xml_data) as f:
        while chunk := f.read(1024):
            extractor.feed(chunk)
    expected_tags = {}
    assert extractor.tags == expected_tags