"""
Gets gene's info from NCBI entrez API (PubMed)
https://www.ncbi.nlm.nih.gov/

Downloads only necessary part of Entrez response, just enough to get all the tags
you interested in (parameter fields, values from GeneFields).
So we do not wait for full 2Mb entrez response but only for first 5-6Kb.

The easiest way to use - global genes object pre-created globally in this module:

    entrez.genes['ppara'][GeneFields.summary]

If we use genes[] it searches for gene name case-insensitive (see canonical_gene_name).
On other hand, all methods in the class search for gene name case-sensitive.

Caches results inside the class instance.
"""
import requests
from src.httpstreamxml.xml_stream import XmlStreamExtractor
import logging
from time import time
import urllib3


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


# Get you own Entrez key https://ncbiinsights.ncbi.nlm.nih.gov/2017/11/02/new-api-keys-for-the-e-utilities/
API_KEY = None

# Max fetched part of XML in case we do not found all necessary tags. So we are sure
# if we had not found all the tags there is no sense to look more than this far.
# If we find all the tag early we would stop even early than that limit.
MAX_BYTES_TO_FETCH = 10*1024

# How long we wait for Entrez response. It does not matter how many bytes we got at the moment.
FETCH_TIMEOUT_SECONDS = 2

# Internal consts
ENTREZ_HOST = 'eutils.ncbi.nlm.nih.gov'
ENTREZ_GENE_DETAILS = '/entrez/eutils/efetch.fcgi?db=gene&id={gene_id}&retmode=xml{key_param}'
ENTREZ_API_KEY_PARAM = '&api_key={api_key}'
ENTREZ_GENE_ID = '/entrez/eutils/esearch.fcgi?db=gene&term={gene_name}[Gene+Name]+AND+homo+sapience[Organism]&retmode=json{key_param}'

log = logging.getLogger('')


class GeneFields:
    """
    Mapping of gene fields to tag names in entrez's result XML
    """
    summary = 'Entrezgene_summary'
    description = 'Gene-ref_desc'
    synonyms = 'Gene-ref_syn'
    locus = 'Gene-ref_locus'


class Genes:
    def __init__(self, fields=None, timeout=FETCH_TIMEOUT_SECONDS, max_bytes_to_fetch=MAX_BYTES_TO_FETCH, api_key=None):
        """
        :param fields:  tags to extract - user GeneFields for convenient names of gene fields
        :param timeout: do not wait for Entrez response more than timeout seconds
        :param max_bytes_to_fetch: do not fetch more than max_bytes_to_fetch even if we had not got all the fields
        :param api_key: Entrez API key, see details in https://ncbiinsights.ncbi.nlm.nih.gov/2017/11/02/new-api-keys-for-the-e-utilities/
                        if None, will use module constant API_KEY.
                        if the cons is also null will use Entrez without key (they said it will has some limitations in this case)
        """
        self.host = ENTREZ_HOST
        if api_key is None:
            self.api_key = API_KEY
        else:
            self.api_key = api_key
        if fields is None:
            self.fields = [GeneFields.summary, GeneFields.description, GeneFields.synonyms, GeneFields.locus]
        elif not isinstance(fields, list) or len(fields) == 0:
            raise ValueError('Expected non-empty list of fields to extract in fields parameter.')
        elif GeneFields.locus not in fields:
            # we need locus to distinguish genes if we found more that one ID for the gene name
            self.fields = fields + [GeneFields.locus]
        else:
            self.fields = fields
        self.timeout = timeout
        self.max_bytes_to_fetch = max_bytes_to_fetch
        self.clear_cache()  # in-memory cache of genes already requested from NCBI.Entrez

    def clear_cache(self):
        """
        Clear all previously cached genes data so all information from this moment will be requested from NCBI server
        """
        self.db = {}

    def canonical_gene_name(self, gene_name):
        return gene_name.lower()

    def __getitem__(self, gene_name):
        gene_name = self.canonical_gene_name(gene_name)
        if gene_name in self.db \
                and len(self.db[gene_name]) >= len(self.fields):  # if not all fields was found we repeat info gathering in hope this time we get all we need
            return self.db[gene_name]
        gene = self.get_gene_details(gene_name)
        if gene:
            self.db[gene_name] = gene
        return gene

    def api_key_query_param(self):
        return ENTREZ_API_KEY_PARAM.format(self.api_key) if self.api_key is not None else ''

    def search_id_url(self, gene_name):
        return ENTREZ_GENE_ID.format(gene_name=gene_name, key_param=self.api_key_query_param())

    def get_details_url(self, gene_id):
        return ENTREZ_GENE_DETAILS.format(gene_id=gene_id, key_param=self.api_key_query_param())

    def get_gene_id(self, gene_name):
        url = self.search_id_url(gene_name)
        response = requests.get(
            'https://{host}{url}'.format(
                host=self.host,
                url=url,
            ),
            verify=False
        )
        try:
            resp = response.json()
            resp = resp['esearchresult']
        except ValueError:
            log.error(f'NCBI.Entrez not JSON response for gene "{gene_name}" ID request:\n{response.text}')
            return
        except KeyError:
            log.error(f'NCBI.Entrez response do not contains search result:\n{resp}')
            return
        if not 'idlist' in resp or not resp['idlist']:
            log.error(f'NCBI.Entrez no gene "{gene_name}" ID in response:\n{resp}')
            return
        ids = resp['idlist']
        if len(ids) > 1:
            log.debug(f'NCBI.Entrez: we found more than one ID for gene "{gene_name}" in response: {ids}')
            for id in ids:
                gene = self.get_gene_details_by_id(id)
                if self.canonical_gene_name(gene[GeneFields.locus]) == gene_name:  # we assume input name are already canonical
                    self.db[gene_name] = gene  # cache response so we won't request it twice
                    ids[0] = id
                    break
                else:
                    log.debug(f'Wrong id={id} - locus is "{gene[GeneFields.locus]}"')
        log.debug(f'NCBI.Entrez: we found gene "{gene_name}" ID: {ids[0]}')
        return ids[0]

    def get_gene_details(self, gene_name):
        gene_id = self.get_gene_id(gene_name)
        if gene_id:
            return self.get_gene_details_by_id(gene_id=gene_id)
        else:
            return {}

    def get_gene_details_by_id(self, gene_id):
        """
        Download gene's details from NCBI entrez API, using gene's ID - see get_gene_id to obtain it
        """
        url = self.get_details_url(gene_id)
        request = requests.get(
            'https://{host}{url}'.format(
                host=self.host,
                url=url,
            ),
            stream=True,
            verify=False
        )
        extractor = XmlStreamExtractor(self.fields)

        start = time()
        fetched_bytes = 0
        for line in request.iter_lines(chunk_size=1024):
            if line is not None:
                fetched_bytes += len(line)
                try:
                    extractor.feed(line)
                except StopIteration:
                    break
                # too much noise so I removed that
                # log.debug(f'NCBI.Entrez: fetched {fetched_bytes} bytes from gene details, found tags {extractor.tags.keys()}')
            elapsed = (time() - start)  # in seconds and decimal parts of seconds
            if elapsed > self.timeout:
                log.error('NCBI.Entrez gene details fetch timeout')
                break
            if fetched_bytes > self.max_bytes_to_fetch:
                log.debug(f'NCBI.Entrez fetched {fetched_bytes}. Not all fields was found but no sense to fetch more.')
                break

        log.debug('''NCBI.Entrez reesult for gene {gene_id}: extracted tags {names}'''.format(
            gene_id=gene_id,
            names=', '.join([tag for tag in extractor.tags.keys()]),
            )
        )
        return extractor.tags


genes = Genes()


if __name__ == '__main__':
    logging.basicConfig(level=logging.ERROR, format='%(message)s')

    for gene_name in ['slc9a3', 'slc9a3r1', 'pdzk1', 'myo5b', 'slc36a1', 'magi1', 'stx3', 'guca2b', 'ush1c', 'slc5a1']:
        gene = genes[gene_name]
        if not gene:
            print(f'!!! Fail to get gene details for "{gene_name}"')
        else:
            print(f'\nGot gene detailes for "{gene_name}"')
            print(genes[gene_name][GeneFields.description])
