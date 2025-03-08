"""Illustrates usage of streamed XML (partial) parsing.

Gets gene's info from NCBI entrez API (PubMed)
https://www.ncbi.nlm.nih.gov/
"""

from typing import Union

from http_stream_xml.entrez import requests_retry_session
from http_stream_xml.xml_stream import XmlStreamExtractor


def get_gene_info(gene_id: Union[str, int]) -> XmlStreamExtractor:
    """Get gene's info from NCBI entrez API (PubMed)."""
    extractor = XmlStreamExtractor(["Gene-ref_desc", "Entrezgene_summary", "Gene-ref_syn"])

    host = "eutils.ncbi.nlm.nih.gov"
    url = f"/entrez/eutils/efetch.fcgi?db=gene&id={gene_id}&retmode=xml"
    request = requests_retry_session().get(
        f"https://{host}{url}",
        stream=True,
        verify=False,
        timeout=60,
    )

    fetched_bytes = 0
    for line in request.iter_lines(chunk_size=1024):
        if line:
            fetched_bytes += len(line)
            extractor.feed(line)
            if extractor.extraction_completed:
                break
        print(f"fetched {fetched_bytes} bytes, found tags {extractor.tags.keys()}")

    return extractor


if __name__ == "__main__":
    extractor = get_gene_info("5465")
    print(f"\nResult: {extractor.tags.keys()}\n\n{extractor.tags}")
