http-stream-xml
===============

Parse XML in HTTP response on the fly, by chunks.

It's essential if you want only beginning of huge document.

For example if you deal with `NCBI <https://www.ncbi.nlm.nih.gov/>`_ PubMed biomedical
articles corpus with Entrez API. The Enrez API tends to return very big documents
(megabytes).
And even if you need just some headers you have to download whole document just to parse it.

The http-stream-xml library helps you to partially download response and parse them.

It does not matter if the server use
`HTTP protocol chunks <https://en.wikipedia.org/wiki/Chunked_transfer_encoding>`_.

Installation
------------

.. code-block:: bash

    pip install http-stream-xml --upgrade

Usage sample
------------

Implement custom loader
~~~~~~~~~~~~~~~~~~~~~~~

`XML streaming chunks load <https://sorokin.engineer/posts/en/xml_streaming_chunks_load.html>`_

Step by step instruction how to implement custom XML loader on Entrez gene DB example.

Use Entrez PubMed loader
~~~~~~~~~~~~~~~~~~~~~~~~

`Entrez gene streaming with http-stream-xml <https://sorokin.engineer/posts/en/entrez_gene_streaming_with_http_stream_xml.html>`_

Use entrez class to receives data from `NCBI <https://www.ncbi.nlm.nih.gov/>`_ PubMed biomedical articles corpus
with downloading only small part of Entrez response, just to extract some summary data.

So you do not have to download whole huge Entrez answer to get just basic gene description.

API
---

.. toctree::
   :maxdepth: 2

   entrez
   xml

Source code
-----------

`GitHub <https://github.com/andgineer/http-stream-xml>`_


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
