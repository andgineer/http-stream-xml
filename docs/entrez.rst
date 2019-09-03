Class Genes (NCBI Entrez API)
=============================

.. automodule:: httpstreamxml.entrez

.. autoclass:: httpstreamxml.entrez.Genes
   :members:

.. autoclass:: httpstreamxml.entrez.GeneFields


Usage example
-------------

.. code-block:: python

    from httpstreamxml import entrez


    print(entrez.genes['myo5b'][entrez.GeneFields.description])
