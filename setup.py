import setuptools

with open("README.rst", "r") as fh:
    long_description = fh.read()

import sys; sys.path.insert(0, '../'); import httpstreamxml

setuptools.setup(
    name='http-stream-xml',
    version=httpstreamxml.version(),
    author="Andrey Sorokin",
    author_email="filbert@ya.ru",
    description="Parse XML in HTTP response on the fly, by chunks",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    url="https://http-stream-xml.readthedocs.io/en/latest/",
    packages=setuptools.find_packages(),
    include_package_data=True,
    keywords='http stream xml chunked',
    classifiers=[
     "Programming Language :: Python :: 3",
     "License :: OSI Approved :: MIT License",
     "Operating System :: OS Independent",
    ],
 )