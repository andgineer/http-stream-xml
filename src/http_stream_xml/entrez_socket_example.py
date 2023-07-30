from http_stream_xml.socket_stream import SocketStream
from http_stream_xml.xml_stream import XmlStreamExtractor

stream = SocketStream(
    host="eutils.ncbi.nlm.nih.gov", url="/entrez/eutils/efetch.fcgi?db=gene&id=5465&retmode=xml"
)
stream.connect()
extractor = XmlStreamExtractor(["Gene-ref_desc", "Entrezgene_summary", "Gene-ref_syn"])

for chunk in stream.fetch():
    extractor.feed(chunk)
    print(f"fetched {stream.fetched_bytes} bytes, found tags {extractor.tags.keys()}")
    if extractor.extraction_completed:
        break

print(f"\nResult: {extractor.tags.keys()}\n\n{extractor.tags}")
