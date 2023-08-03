from unittest import mock
from unittest.mock import Mock, patch

import pytest

import http_stream_xml.entrez
from http_stream_xml.entrez import GeneFields, Genes


@pytest.fixture
def mock_genes():
    return Genes()


@pytest.fixture
def mock_session():
    """Patch requests.Session to return a mock object."""
    with patch(
        "http_stream_xml.entrez.requests.Session", return_value=Mock(autospec=True)
    ) as mock:
        http_stream_xml.entrez.requests_retry_session.cache_clear()
        yield mock
        http_stream_xml.entrez.requests_retry_session.cache_clear()


def test_canonical_gene_name(mock_genes):
    assert mock_genes.canonical_gene_name("Test") == "test"


@mock.patch.object(Genes, "get_gene_details", return_value={})
def test_getitem_from_cache(mock_get_gene_details, mock_genes):
    mock_genes.db = {
        "test": {
            "Entrezgene_summary": "Test Gene",
            "Gene-ref_desc": "Test description",
            "Gene-ref_syn": "Test synonym",
            "Gene-ref_locus": "Test locus",
        }
    }
    result = mock_genes["test"]
    assert result == {
        "Entrezgene_summary": "Test Gene",
        "Gene-ref_desc": "Test description",
        "Gene-ref_syn": "Test synonym",
        "Gene-ref_locus": "Test locus",
    }
    mock_get_gene_details.assert_not_called()  # Check that the method was not called


@mock.patch.object(
    Genes,
    "get_gene_details",
    return_value={
        "Entrezgene_summary": "Test Gene",
        "Gene-ref_desc": "Test description",
        "Gene-ref_syn": "Test synonym",
        "Gene-ref_locus": "Test locus",
    },
)
def test_getitem_from_cache_incomplete_cache(mock_get_gene_details, mock_genes):
    """Check that the site request repeated is there are not enough fields from prev request."""
    mock_genes.db = {
        "test": {
            "Entrezgene_summary": "Test Gene",
        }
    }
    result = mock_genes["test"]
    assert result == {
        "Entrezgene_summary": "Test Gene",
        "Gene-ref_desc": "Test description",
        "Gene-ref_syn": "Test synonym",
        "Gene-ref_locus": "Test locus",
    }
    mock_get_gene_details.assert_called_once_with("test")


def test_get_gene_id(mock_session, mock_genes):
    mock_response = Mock()
    mock_response.json.return_value = {"esearchresult": {"idlist": ["123456"]}}
    mock_session.return_value.get.return_value = mock_response

    gene_id = mock_genes.get_gene_id("test")
    assert gene_id == "123456"


def test_get_gene_details(mock_session, mock_genes):
    mock_response = Mock()
    mock_response.json.return_value = {"esearchresult": {"idlist": ["123456"]}}
    mock_session.return_value.get.return_value = mock_response

    with patch.object(mock_genes, "get_gene_details_by_id") as mock_details:
        mock_details.return_value = {"Entrezgene_summary": "Test Gene"}
        gene = mock_genes.get_gene_details("test")
        assert gene == {"Entrezgene_summary": "Test Gene"}


def test_get_gene_details_by_id(mock_session, mock_genes):
    mock_response = Mock()
    mock_response.iter_lines.return_value = [b"<Entrezgene_summary>Test Gene</Entrezgene_summary>"]
    mock_session.return_value.get.return_value = mock_response

    gene = mock_genes.get_gene_details_by_id("123456")
    assert gene == {GeneFields.summary: "Test Gene"}


def test_api_key_query_param(mock_genes):
    mock_genes.api_key = "test_key"
    result = mock_genes.api_key_query_param()
    assert result == "&api_key=test_key"


def test_search_id_url(mock_genes):
    url = mock_genes.search_id_url("test")
    assert (
        url
        == "/entrez/eutils/esearch.fcgi?db=gene&term=test[Gene+Name]+AND+homo+sapience[Organism]&retmode=json"
    )


def test_get_details_url(mock_genes):
    url = mock_genes.get_details_url("123456")
    assert url == "/entrez/eutils/efetch.fcgi?db=gene&id=123456&retmode=xml"
