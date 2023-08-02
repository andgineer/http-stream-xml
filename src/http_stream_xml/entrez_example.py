"""Illustrates usage of streamed XML (partial) parsing.

Gets gene's info from NCBI entrez API (PubMed)
https://www.ncbi.nlm.nih.gov/
"""
from typing import Iterable, Optional

import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

from http_stream_xml.xml_stream import XmlStreamExtractor


def requests_retry_session(
    retries: int = 3,
    backoff_factor: float = 1.0,
    status_forcelist: Iterable[int] = (500, 502, 504),
    session: Optional[requests.Session] = None,
) -> requests.Session:
    """Retry policy configuration."""
    session = session or requests.Session()
    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session


def get_gene_info(gene_id: str) -> XmlStreamExtractor:
    """Get gene's info from NCBI entrez API (PubMed)."""
    extractor = XmlStreamExtractor(["Gene-ref_desc", "Entrezgene_summary", "Gene-ref_syn"])

    host = "eutils.ncbi.nlm.nih.gov"
    url = f"/entrez/eutils/efetch.fcgi?db=gene&id={gene_id}&retmode=xml"
    request = requests_retry_session().get(
        f"https://{host}{url}", stream=True, verify=False, timeout=60
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
