from io import StringIO
from xml.sax import SAXParseException

import pytest

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
    chunk_size = len(xml_data_1st_chunk) // 2 + 1
    read_size = 0
    with StringIO(xml_data) as f:
        while True:
            chunk = f.read(chunk_size)
            read_size += chunk_size
            if not chunk or extractor.extraction_completed:
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


def test_empty_xml():
    xml_data = ""

    tags_to_collect = {"name", "age"}
    extractor = XmlStreamExtractor(tags_to_collect)

    with StringIO(xml_data) as f:
        while chunk := f.read(1024):
            extractor.feed(chunk)
    expected_tags = {}
    assert extractor.tags == expected_tags


def test_no_closing_tags():
    xml_data = """
    <root>
        <name>John Doe
        <age>30
    </root>
    """

    tags_to_collect = {"name", "age"}
    extractor = XmlStreamExtractor(tags_to_collect)

    with pytest.raises(SAXParseException):
        with StringIO(xml_data) as f:
            while chunk := f.read(1024):
                extractor.feed(chunk)


def test_nested_tags():
    xml_data_1st_chunk = """
    <root>
        <person>
            <name>John Doe</name>
            <age>30</age>"""
    xml_data_2nd_chunk = """
    </person>
    </root>
    """

    tags_to_collect = {"name", "age"}
    extractor = XmlStreamExtractor(tags_to_collect)
    xml_data = f"{xml_data_1st_chunk}{xml_data_2nd_chunk}"
    chunk_size = len(xml_data_1st_chunk) // 2 + 1

    with StringIO(xml_data) as f:
        while (chunk := f.read(chunk_size)) and not extractor.extraction_completed:
            extractor.feed(chunk)
    expected_tags = {"name": "John Doe", "age": "30"}
    assert extractor.tags == expected_tags


def test_tags_with_attributes():
    xml_data = """
    <root>
        <name id="1">John Doe</name>
        <age id="2">30</age>
    </root>
    """

    tags_to_collect = {"name", "age"}
    extractor = XmlStreamExtractor(tags_to_collect)

    with StringIO(xml_data) as f:
        while chunk := f.read(1024):
            extractor.feed(chunk)
    expected_tags = {"name": "John Doe", "age": "30"}
    assert extractor.tags == expected_tags


def test_repeated_tags():
    xml_data = """
    <root>
        <name>John Doe</name>
        <age>30</age>
        <name>Jane Doe</name>
        <age>28</age>
    </root>
    """

    tags_to_collect = {"name", "age"}
    extractor = XmlStreamExtractor(tags_to_collect)

    with StringIO(xml_data) as f:
        while chunk := f.read(1024):
            extractor.feed(chunk)
    expected_tags = {"name": "John Doe", "age": "30"}
    assert extractor.tags == expected_tags


def test_xml_stream_with_cdata():
    xml_data = """
    <root>
        <name><![CDATA[John & Doe]]></name>
        <age>30</age>
    </root>
    """
    extractor = XmlStreamExtractor(["name", "age"])
    extractor.feed(xml_data)
    assert extractor.tags == {"name": "John & Doe", "age": "30"}


def test_xml_stream_with_special_chars():
    xml_data = """
    <root>
        <name>John &amp; &lt;Doe&gt;</name>
        <age>30</age>
    </root>
    """
    extractor = XmlStreamExtractor(["name", "age"])
    extractor.feed(xml_data)
    assert extractor.tags == {"name": "John & <Doe>", "age": "30"}
