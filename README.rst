http-stream-xml
===============

|made_with_python| |build_status| |coverage| |pypi_version| |pypi_license| |readthedocs|

Parse XML from HTTP responses on the fly, chunk by chunk.

This works with `HTTP protocol chunks <https://en.wikipedia.org/wiki/Chunked_transfer_encoding>`_
or partial downloads of large HTTP responses.

I use it to work with the `NCBI (PubMed) Entrez API <https://www.ncbi.nlm.nih.gov/>`_.

See usage examples in these blog articles:
* `XML streaming chunks load <https://sorokin.engineer/posts/en/xml_streaming_chunks_load.html>`_
* `Entrez gene streaming with http-stream-xml <https://sorokin.engineer/posts/en/entrez_gene_streaming_with_http_stream_xml.html>`_

Documentation
-------------
`Documentation <https://http-stream-xml.sorokin.engineer/>`_

Scripts
-------
Install `invoke <https://docs.pyinvoke.org/en/stable/>`_ preferably with pipx:

.. code-block:: bash

    pipx install invoke

To get available scripts:

.. code-block:: bash

    inv --list

Coverage report
---------------
* `Codecov <https://app.codecov.io/gh/andgineer/http-stream-xml/tree/master/src/http_stream_xml>`_
* `Coveralls <https://coveralls.io/github/andgineer/http-stream-xml>`_

.. |build_status| image:: https://github.com/andgineer/http-stream-xml//workflows/ci/badge.svg
    :target: https://github.com/andgineer/http-stream-xml/actions
    :alt: Latest release

.. |pypi_version| image:: https://img.shields.io/pypi/v/http-stream-xml.svg?style=flat-square
    :target: https://pypi.org/p/http-stream-xml
    :alt: Latest release

.. |pypi_license| image:: https://img.shields.io/pypi/l/http-stream-xml.svg?style=flat-square
    :target: https://pypi.python.org/pypi/http-stream-xml
    :alt: MIT license

.. |readthedocs| image:: https://readthedocs.org/projects/http-stream-xml/badge/?version=latest
    :target: https://http-stream-xml.sorokin.engineer/
    :alt: Documentation Status

.. |made_with_python| image:: https://img.shields.io/badge/Made%20with-Python-1f425f.svg
    :target: https://www.python.org/
    :alt: Made with Python

.. |codecov| image:: https://codecov.io/gh/andgineer/http-stream-xml/branch/master/graph/badge.svg
    :target: https://app.codecov.io/gh/andgineer/http-stream-xml/tree/master/src%2Fhttp_stream_xml
    :alt: Code coverage

.. |coverage| image:: https://raw.githubusercontent.com/andgineer/http-stream-xml/python-coverage-comment-action-data/badge.svg
    :target: https://htmlpreview.github.io/?https://github.com/andgineer/http-stream-xml/blob/python-coverage-comment-action-data/htmlcov/index.html
    :alt: Coverage report
