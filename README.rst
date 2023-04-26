http-stream-xml
===============

|made_with_python| |build_status| |pypi_version| |pypi_license| |readthedocs|

Parse XML in HTTP response on the fly, by chunks.

It could be `HTTP protocol chunks <https://en.wikipedia.org/wiki/Chunked_transfer_encoding>`_
Or just partial download of big HTTP response.


I use it to work with `NCBI (PubMed) Entrez API <https://www.ncbi.nlm.nih.gov/>`_.

Installation
------------

.. code-block:: bash

    pip install http-stream-xml --upgrade

Documentation
-------------
`Documentation <https://http-stream-xml.sorokin.engineer/en/latest/>`_

.. |build_status| image:: https://github.com/andgineer/redis-redirect//workflows/ci/badge.svg
    :target: (https://github.com/andgineer/redis-redirect//actions
    :alt: Latest release

.. |pypi_version| image:: https://img.shields.io/pypi/v/http-stream-xml.svg?style=flat-square
    :target: https://pypi.org/p/http-stream-xml
    :alt: Latest release

.. |pypi_license| image:: https://img.shields.io/pypi/l/http-stream-xml.svg?style=flat-square
    :target: https://pypi.python.org/pypi/http-stream-xml
    :alt: MIT license

.. |readthedocs| image:: https://readthedocs.org/projects/http-stream-xml/badge/?version=latest
    :target: https://http-stream-xml.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

.. |made_with_python| image:: https://img.shields.io/badge/Made%20with-Python-1f425f.svg
    :target: https://www.python.org/
    :alt: Made with Python
