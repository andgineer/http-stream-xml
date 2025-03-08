"""Check real eutils.ncbi.nlm.nih.gov without mocking."""

import pytest

from http_stream_xml.examples.http_stream_example import get_gene_info


@pytest.mark.slow
def test_streamed_xml_parsing():
    extractor = get_gene_info(5465)

    assert "Gene-ref_desc" in extractor.tags.keys()
    assert "Gene-ref_syn" in extractor.tags.keys()
    assert "Entrezgene_summary" in extractor.tags.keys()
