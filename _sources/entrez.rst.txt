Class Genes (NCBI Entrez API)
=============================

.. automodule:: http_stream_xml.entrez

.. autoclass:: http_stream_xml.entrez.Genes
   :members:

.. autoclass:: http_stream_xml.entrez.GeneFields


Usage example
-------------

.. code-block:: python

    from http_stream_xml import entrez


    print(entrez.genes['myo5b'][entrez.GeneFields.description])
