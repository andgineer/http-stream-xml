"""Illustrates usage of streamed XML (partial) parsing.

Gets gene's info from NCBI entrez API (PubMed)
https://www.ncbi.nlm.nih.gov/
"""
import requests

from http_stream_xml.xml_stream import XmlStreamExtractor

extractor = XmlStreamExtractor(["Gene-ref_desc", "Entrezgene_summary", "Gene-ref_syn"])

host = "eutils.ncbi.nlm.nih.gov"
url = "/entrez/eutils/efetch.fcgi?db=gene&id=5465&retmode=xml"
request = requests.get(f"https://{host}{url}", stream=True, verify=False, timeout=10)

fetched_bytes = 0
for line in request.iter_lines(chunk_size=1024):
    if line:
        fetched_bytes += len(line)
        extractor.feed(line)
        if extractor.extraction_completed:
            break
        print(f"fetched {fetched_bytes} bytes, found tags {extractor.tags.keys()}")

print(f"\nResult: {extractor.tags.keys()}\n\n{extractor.tags}")
