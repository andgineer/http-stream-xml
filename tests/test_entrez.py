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
    with patch("http_stream_xml.entrez.requests.Session", return_value=Mock(autospec=True)) as mock:
        http_stream_xml.entrez.requests_retry_session.cache_clear()
        yield mock
        http_stream_xml.entrez.requests_retry_session.cache_clear()


def test_canonical_gene_name(mock_genes):
    assert mock_genes.canonical_gene_name("Test") == "test"


def test_gene_add_locus():
    genes = Genes(
        fields=[
            GeneFields.summary,
            GeneFields.description,
            GeneFields.synonyms,
        ]
    )
    assert GeneFields.locus in genes.fields


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


def test_genes_invalid_fields():
    with pytest.raises(ValueError, match="Expected non-empty list of fields"):
        Genes(fields=[])


def test_genes_cache_behavior():
    # Initialize with exactly the fields we're mocking
    genes = Genes(fields=["Entrezgene_summary", "Gene-ref_desc", "Gene-ref_locus"])

    with patch.object(genes, "get_gene_details") as mock_details:
        mock_details.return_value = {
            "Entrezgene_summary": "Test Gene",
            "Gene-ref_desc": "Test description",
            "Gene-ref_locus": "test_gene",
        }

        # First call should hit the API
        result1 = genes["TEST_GENE"]
        assert mock_details.call_count == 1

        # Second call should use cache
        result2 = genes["test_gene"]
        assert mock_details.call_count == 1
        assert result1 == result2


def test_genes_incomplete_cache_refresh():
    genes = Genes(fields=[GeneFields.summary, GeneFields.description, GeneFields.locus])
    genes.db = {"test": {GeneFields.summary: "Test summary"}}

    with patch.object(genes, "get_gene_details") as mock_details:
        mock_details.return_value = {
            GeneFields.summary: "New summary",
            GeneFields.description: "Test description",
            GeneFields.locus: "test",
        }

        result = genes["test"]
        assert mock_details.call_count == 1
        assert len(result) == 3


def test_genes_api_key_handling():
    genes = Genes(api_key="test_key")
    url = genes.search_id_url("test_gene")
    assert "api_key=test_key" in url

    genes = Genes(api_key=None)
    url = genes.search_id_url("test_gene")
    assert "api_key" not in url


@patch("http_stream_xml.entrez.requests_retry_session")
def test_genes_timeout_handling(mock_session):
    genes = Genes(timeout=1)
    mock_response = Mock()
    mock_response.json.return_value = {"esearchresult": {"idlist": []}}
    mock_session.return_value.get.return_value = mock_response

    result = genes.get_gene_id("test_gene")
    assert mock_session.return_value.get.call_args[1]["timeout"] == 1
